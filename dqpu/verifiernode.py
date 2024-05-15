# Copyright 2024 Davide Gessa

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import pickle
import random
import time

from .blockchain import IPFSGateway, NearBlockchain
from .cli import default_parser
from .q import Circuit
from .utils import create_dqpu_dirs
from .verifier import BasicTrapper  # BasicTrapInfo,


def verifier_node():
    parser = default_parser()
    args = parser.parse_args()  # noqa: F841

    base_dir = create_dqpu_dirs()

    nb = NearBlockchain(args.account, args.network)
    ipfs = IPFSGateway()  # noqa: F841

    # Start contract polling for new jobs
    running = True
    current_limit = 256
    n_vresult = 0
    n_verified = 0

    print("Verifier node started.")

    while running:
        latest_jobs = nb.get_latest_jobs(limit=current_limit)

        # If there is a new job that needs validation, process it
        for j in latest_jobs:
            if j["status"] == "pending-validation":
                print(
                    f"Processing pending-validation job {j['id']} from {j['owner_id']}"
                )
                jf = ipfs.get(j["job_file"])

                # Parse the file using q.Circuit.fromQasm
                try:
                    qc = Circuit.fromQasmCircuit(jf.decode("ascii"))
                except Exception as e:
                    print("\t", "Failed to parse", j["id"], e)
                    nb.set_job_validity(j["id"], False)
                    continue

                # Add a trap
                trapper = BasicTrapper()
                (qc2, t) = trapper.trap(qc)

                # Save trap info to a file
                with open(f"{base_dir}/{j['id']}_qc_trap.qasm", "wb") as outp:
                    pickle.dump(t, outp, pickle.HIGHEST_PROTOCOL)

                # Save qasm to file
                trapped_qasm_file = f"{base_dir}/{j['id']}_qc_trapped.qasm"

                with open(trapped_qasm_file, "w") as f:
                    f.write(qc2.toQasmCircuit())

                # Upload the file
                jf_trapped = ipfs.upload(trapped_qasm_file)
                print("\t", "Trapped file uploaded", jf_trapped)

                # Send the set_validity
                try:
                    print("\t", nb.set_job_validity(j["id"], True, jf_trapped))
                    n_verified += 1
                except Exception as e:
                    print('\tFailed to set',e)

            elif (
                j["status"] == "validating-result"
                and j["verifier_id"] == nb.account.account_id
            ):
                print(
                    f"Processing validating-result job {j['id']} from {j['owner_id']} "
                    + f"sampled by {j['sampler_id']}"
                )

                # Get the result data
                rf = ipfs.get(j["result_file"])

                try:
                    counts = json.loads(rf)
                except:
                    print("\t", "Invalid result data")
                    continue

                # Check if shots match
                ctot = sum(counts.values())
                if j["shots"] > ctot:
                    print("\t", "Invalid number of shots")
                    print(nb.set_result_validity(j["id"], False))
                    continue

                # Load the trap from file
                with open(f"{base_dir}/{j['id']}_qc_trap.qasm", "rb") as inp:
                    t = pickle.load(inp)

                # Check trap validity
                trapper = BasicTrapper()
                validity = trapper.verify(t, counts)

                # Send the set_result_validity
                try:
                    print("\t", nb.set_result_validity(j["id"], validity))
                    n_vresult += 1
                except Exception as e:
                    print('\tFailed to set',e)

        current_limit = 48
        print(
            f"Account balance is {nb.balance():0.5f} N, job verified {n_verified}, "
            + f"result verified {n_vresult}"
        )
        time.sleep(random.randint(0, 60))
