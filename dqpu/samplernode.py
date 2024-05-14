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

from .blockchain import NearBlockchain
from .cli import default_parser


def sampler_node():
    parser = default_parser()
    args = parser.parse_args()  # noqa: F841

    nb = NearBlockchain(args.account, args.network)

    # Start contract polling for new jobs
    running = True

    while running:
        print(nb.get_latest_jobs())
        time.sleep(4)
