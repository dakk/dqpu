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

import time

from .blockchain import IPFSGateway, NearBlockchain
from .cli import default_parser


def verifier_node():
    parser = default_parser()
    args = parser.parse_args()  # noqa: F841

    nb = NearBlockchain(args.account, args.network)
    ipfs = IPFSGateway()  # noqa: F841

    # Start contract polling for new jobs
    running = True
    current_limit = 256

    while running:
        latest_jobs = nb.get_latest_jobs(limit=current_limit)

        # If there is a new job that needs validation, process it
        for j in latest_jobs:
            if j["status"] == "pending-validation":
                print(
                    f"Processing pending-validation job {j['id']} from {j['owner_id']}"
                )
                jf = ipfs.get(j["job_file"])
                print(jf)
            elif (
                j["status"] == "validating-result"
                and j["verifier_id"] == nb.account.account_id
            ):
                print(
                    f"Processing validating-result job {j['id']} from {j['owner_id']} "
                    + f"sampled by {j['sampler_id']}"
                )

        current_limit = 48
        time.sleep(32)
