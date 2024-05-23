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
import random
import sys
import time
import traceback

from requests.exceptions import ReadTimeout

from .blockchain import IPFSGateway, NearBlockchain, from_near, to_near
from .cli import default_parser
from .sampler import SAMPLERS
from .utils import create_dqpu_dirs, repeat_until_done


def filter_jobs(jobs, args):
    filtered = []
    for j in jobs:
        if j["status"] != "waiting":
            continue

        # Check if reward/10 is < of max_deposit
        if int(j["reward_amount"]) / 10 > to_near(float(args.max_deposit)):
            print("reward / 10 is greater than max_deposit, skipping")
            continue

        # Check for max qubits
        if int(j["qubits"]) > int(args.max_qubits):
            print(
                f"qubits {j['qubits']} is greater than max_qubits {args.max_qubits}"
                + ", skipping"
            )
            continue

        # Check for min qubits
        if int(j["qubits"]) < int(args.min_qubits):
            print(
                f"qubits {j['qubits']} is lower than min_qubits {args.min_qubits}"
                + ", skipping"
            )
            continue

        filtered.append(j)

    return filtered


def handle_job(j, ipfs, nb, sampler_name, base_dir):
    # Get the qasm file
    try:
        jf = ipfs.get(j["job_file"], timeout=10)
    except ReadTimeout:  # TODO: move on ipfs.get raising a new exception
        print(f"\tTimeout getting file {j['job_file']}, skipping for now")
        return False

    print(f"\tGot file {j['job_file']}")

    # Load into a Sampler object (selected by params)
    # qc = Circuit.fromQasmCircuit(jf)
    sampler = SAMPLERS[sampler_name](jf)

    # Do the simulation
    print(f"\tStarting sampler {sampler_name}")
    t_start = time.time()
    counts = sampler.sample(j["shots"])
    t_duration = int(time.time() - t_start)
    if t_duration > 120:
        t_duration_s = (
            f"{int(t_duration / 60.)} minutes and {int(t_duration % 60)} seconds"
        )
    else:
        t_duration_s = f"{t_duration} seconds"

    # Upload the result
    result_f = f"{base_dir}/sampler/cache/{j['id']}_result.json"
    with open(result_f, "w") as cf:
        cf.write(json.dumps(counts))

    print(f"\tSampling done in {t_duration_s}, uploading {result_f}")
    jf_result = ipfs.upload(result_f)
    print(f"\tResult file uploaded {jf_result}")

    # Submit the result with the deposit
    try:
        sub_res = nb.submit_job_result(
            j["id"],
            jf_result,
            deposit=from_near(j["reward_amount"]) / 10 + 0.00001,
        )
        print(f"\t{sub_res}")
        return True
    except Exception as e:
        print("Failed to submit:", e)
        return False


def sampler_node():  # noqa: C901
    parser = default_parser()

    parser.add_argument("-d", "--max-deposit", help="maximum deposit", default=0.1)
    parser.add_argument(
        "-q", "--max-qubits", help="maximum number of simulable qubits", default=21
    )
    parser.add_argument("--min-qubits", help="minimum number of qubits", default=1)
    parser.add_argument(
        "-s",
        "--sampler",
        help="sampler to use",
        default="aersimulator",
        choices=SAMPLERS.keys(),
    )

    args = parser.parse_args()  # noqa: F841
    base_dir = create_dqpu_dirs()

    nb = NearBlockchain(args.account, args.network)
    ipfs = IPFSGateway(gateway="http://" + args.ipfs_gateway)  # noqa: F841

    # Start contract polling for new jobs
    running = True
    n_sampled = 0
    first_run = True

    print(f"Testing selected sampler: {args.sampler}")
    sampler_ok = SAMPLERS[args.sampler].test()
    if sampler_ok:
        print(f"Sampler {args.sampler} is working correctly.")
    else:
        print(f"Sampler {args.sampler} is not working correctly, exiting.")
        sys.exit()

    print("Sampler node started.")
    waiting_jobs = 0

    while running:
        if first_run:
            first_run = False
            latest_jobs = repeat_until_done(lambda: nb.get_all_jobs(True))
        else:
            i = 0
            while (
                repeat_until_done(lambda: nb.get_jobs_stats())["waiting"]
                == waiting_jobs
            ) and i < 5:
                time.sleep(random.randint(0, 5))
                i += 1
            latest_jobs = repeat_until_done(lambda: nb.get_latest_jobs())

        waiting_jobs = repeat_until_done(lambda: nb.get_jobs_stats()["waiting"])

        filtered_jobs = filter_jobs(latest_jobs, args)
        random.shuffle(filtered_jobs)
        fj_s = ", ".join(map(lambda j: j["id"], filtered_jobs))
        print(f"Found {len(filtered_jobs)} jobs matching sampler criteria: {fj_s}")
        i = 0

        # If there is a new job that needs execution, process it
        for j in filtered_jobs:
            i += 1
            print(
                f"[{i}/{len(filtered_jobs)}] Processing job {j['id']} with {j['qubits']} "
                + f"qubits for {j['shots']} shots"
            )
            try:
                if handle_job(j, ipfs, nb, args.sampler, base_dir):
                    n_sampled += 1
                    waiting_jobs -= 1
            except Exception as e:
                print("Failed to handle job:", e)
                traceback.print_exc()

        repeat_until_done(
            lambda: print(
                f"Account balance is {nb.balance():0.5f} N, sampled jobs {n_sampled}"
            )
        )
