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

import argparse
import json
import random
from hashlib import sha256

from .blockchain import (
    IPFSGateway,
    NearBlockchain,
)  # , start_ipfs_daemon, stop_ipfs_daemon
from .q import Circuit
from .utils import create_dqpu_dirs

# from qiskit import qasm2
# from qiskit.circuit.random import random_circuit


ACTIONS = [
    "list",
    "submit",
    "remove",
    "info",
    "status",
    "get-result",
    "set-validity",
    "set-result-validity",
    "submit-result",
    "submit-random",
    "clear-jobs",
    "add-verifier",
    "remove-verifier",
    "is-a-verifier",
    "verifiers",
]


def default_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--network", help="network to use (mainnet | testnet)", default="testnet"
    )
    parser.add_argument(
        "-ig",
        "--ipfs-gateway",
        help="ipfs gateway (default 127.0.0.1:8080)",
        default="127.0.0.1:8080",
    )
    parser.add_argument("-a", "--account", help="account path or name", required=True)
    return parser


def cli():  # noqa: C901
    parser = default_parser()

    parser.add_argument("action", help="action to run", choices=ACTIONS)

    parser.add_argument("-i", "--id", help="identifier of job")
    parser.add_argument("-v", "--validity", help="validity status", type=str)
    parser.add_argument("-vv", "--verifier", help="verifier account", type=str)
    parser.add_argument(
        "-mq",
        "--max-qubits",
        help="max qubits for the random submit",
        type=int,
        default=21,
    )
    parser.add_argument(
        "-nq",
        "--min-qubits",
        help="min qubits for the random submit",
        type=int,
        default=5,
    )

    group_submit = parser.add_argument_group("submit")
    group_submit.add_argument("-f", "--file", help="openqasm2 file to submit")
    group_submit.add_argument("-t", "--trap", help="the trap file", default="")
    group_submit.add_argument(
        "-s", "--shots", help="number of shots to request", type=int, default=1024
    )
    group_submit.add_argument(
        "-r",
        "--reward",
        help="reward for the execution of the job",
        type=float,
        default=0.001,
    )

    # group_remove = parser.add_argument_group("remove")

    # group_job_validity = parser.add_argument_group("set-job-validity")

    group_submit_result = parser.add_argument_group("submit-result")
    group_submit_result.add_argument(
        "-rf", "--result-file", help="json containing sampling result"
    )
    group_submit_result.add_argument(
        "-d",
        "--deposit",
        help="cautional deposit for the execuition of the job",
        type=float,
        default=None,
    )

    args = parser.parse_args()  # noqa: F841
    base_dir = create_dqpu_dirs()

    nb = NearBlockchain(args.account, args.network)
    ipfs = IPFSGateway(gateway="http://" + args.ipfs_gateway)  # noqa: F841

    # ipfs_process = start_ipfs_daemon()

    if args.action == "list":
        print(json.dumps(nb.get_latest_jobs(), indent=2))

    elif args.action == "submit":
        # Parse the qasm
        qf = open(args.file, "r")
        qasm_data = qf.read()
        circ = Circuit.fromQasmCircuit(qasm_data)

        # Calcualte qubits, depth
        qubits = circ.n_qbits
        depth = len(circ.gates)

        # Upload job_file
        job_file = ipfs.upload(args.file)

        print(nb.submit_job(qubits, depth, args.shots, job_file, args.reward))
        print(nb.get_latest_jobs()[0]["id"])

    elif args.action == "submit-random":
        nq = random.randint(int(args.min_qubits), int(args.max_qubits))
        dpt = random.randint(5, 300)

        print(f"Creating a random circuit of {nq} qubits (depth {dpt})...")

        qc = Circuit.random(nq, dpt)
        qasm_data = qc.toQasmCircuit()

        # qc = random_circuit(nq, dpt, max_operands=2, measure=True)
        # qasm_data = qasm2.dumps(qc)

        dig = sha256(qasm_data.encode("ascii")).hexdigest()[0:8]

        circuit_file = base_dir + f"/cache/random_circuit_{nq}_{dpt}_{dig}.qasm"
        with open(circuit_file, "w") as f:
            f.write(qasm_data)

        print("Submitting...")

        # Upload job_file
        job_file = ipfs.upload(circuit_file)
        print(f"Circuit file is {job_file}")

        shots = random.choice([256, 512, 1024, 2048, 4096, 8192, 16384])
        sh_fact = int(round((shots + 1024) / 1024))
        reward = random.randint(1 * nq * sh_fact, 10 * nq * sh_fact) / 30000.0

        print(f"Submitting with a reward of {reward:.6f} for {shots} shots")

        print(nb.submit_job(nq, dpt, shots, job_file, reward))
        print(f"Account balance is {nb.balance():0.5f} N")
        print(nb.get_latest_jobs()[-1]["id"])

    elif args.action == "remove":
        print(nb.remove_job(args.id))

    elif args.action == "info":
        print(json.dumps(nb.get_job(args.id), indent=2))

    elif args.action == "status":
        print(json.dumps(nb.get_job_status(args.id), indent=2))

    elif args.action == "get-result":
        print(ipfs.get(nb.get_job(args.id).result_file))

    elif args.action == "set-validity":
        jid_file = nb.get_job(args.id)["job_file"]

        # TODO: add trap

        print(
            nb.set_job_validity(
                args.id, valid=args.validity == "true", trapped_file=jid_file
            )
        )

    elif args.action == "set-result-validity":
        if args.validity == "true":
            trap_file = ipfs.upload(args.trap)
            print(nb.set_result_validity(args.id, valid=True, trap_file=trap_file))
        else:
            print(nb.set_result_validity(args.id, valid=False))

    elif args.action == "submit-result":
        res_file = ipfs.upload(args.result_file)

        if args.deposit is None:
            args.deposit = nb.get_job(args.id).reward_amount / 10

        print(nb.submit_job_result(args.id, result_file=res_file, deposit=args.deposit))

    elif args.action == "clear-jobs":
        print(nb.clear_jobs())

    elif args.action == "add-verifier":
        print(nb.add_verifier(args.verifier))

    elif args.action == "remove-verifier":
        print(nb.remove_verifier(args.verifier))

    elif args.action == "is-a-verifier":
        print(nb.is_a_verifier(args.verifier))

    elif args.action == "verifiers":
        print(nb.get_verifiers())

    # stop_ipfs_daemon(ipfs_process)
