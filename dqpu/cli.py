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

from .blockchain import (
    IPFSGateway,
    NearBlockchain,
)  # , start_ipfs_daemon, stop_ipfs_daemon
from .q import Circuit

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
]


def default_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--network", help="network to use (mainnet | testnet)", default="testnet"
    )
    parser.add_argument("-a", "--account", help="account path or name", required=True)
    return parser


def cli():  # noqa: C901
    parser = default_parser()

    parser.add_argument("action", help="action to run", choices=ACTIONS)

    parser.add_argument("-i", "--id", help="identifier of job")
    parser.add_argument("-v", "--validity", help="validity status", type=str)

    group_submit = parser.add_argument_group("submit")
    group_submit.add_argument("-f", "--file", help="openqasm2 file to submit")
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

    nb = NearBlockchain(args.account, args.network)
    ipfs = IPFSGateway()  # noqa: F841

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
        pass

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
        print(nb.set_result_validity(args.id, valid=args.validity == "true"))

    elif args.action == "submit-result":
        res_file = ipfs.upload(args.result_file)

        if args.deposit is None:
            args.deposit = nb.get_job(args.id).reward_amount / 10

        print(nb.submit_job_result(args.id, result_file=res_file, deposit=args.deposit))

    # stop_ipfs_daemon(ipfs_process)
