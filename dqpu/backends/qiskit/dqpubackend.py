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

import warnings
from typing import Optional

from qiskit import qasm2
from qiskit.providers import BackendV2 as Backend
from qiskit.providers import Options, convert_to_target
from qiskit.providers.models import BackendConfiguration

from ...blockchain import IPFSGateway, NearBlockchain
from ..base import submit_job
from .dqpujob import DQPUJob

BASIS_GATES = sorted(
    [
        "x",
        "y",
        "z",
        "h",
        "cx",
        # "swap",
        # "cswap",
        # "rx",
        # "ry",
        # "rz",
        # "id",
        # "ccx",
        # "u1",
        # "u2",
        # "u3",
        # "rxx",
        # "ryy",
        # "rzz",
        "s",
        "sdg",
        "t",
        "tdg",
        # "sx",
        # "sxdg",
        # "unitary",
        # "ecr",
    ]
)


class DQPUBackend(Backend):
    def __init__(self, network: str = "testnet", provider=None):
        super().__init__()

        self.network = network
        # self.provider = provider
        self.near_blockchain: Optional[NearBlockchain] = None
        self.ipfs_gateway = IPFSGateway()

        # Create Target
        self._target = convert_to_target(self.configuration())

        # Set option validators
        self.options.set_validator("shots", (1, 8192))
        self.options.set_validator("reward", (0.00001, 10.0))

    def load_account(self, account: str):
        """Load near account given its id or file path"""
        self.near_blockchain = NearBlockchain(account, self.network)

    def configuration(self):
        return BackendConfiguration(
            backend_name="dqpu",
            backend_version="0.1",
            n_qubits=1000,
            basis_gates=BASIS_GATES,
            gates=[],
            local=False,
            simulator=True,
            conditional=True,
            open_pulse=False,
            memory=True,
            max_shots=8192,
            coupling_map=None,
            # , supported_instructions=None, dynamic_reprate_enabled=False,
            # rep_delay_range=None, default_rep_delay=None, max_experiments=None,
            # sample_name=None, n_registers=None, register_map=None, configurable=None,
            # credits_required=None, online_date=None, display_name=None, description=None,
            # tags=None, dt=None, dtm=None, processor_type=None, parametric_pulses=None
        )

    @property
    def target(self):
        return self._target

    @property
    def max_circuits(self):
        return 1

    @classmethod
    def _default_options(cls):
        return Options(shots=1024, reward=0.0001)

    def run(self, circuit, **kwargs):
        # serialize circuits submit to backend and create a job
        for kwarg in kwargs:
            if not hasattr(self.options, kwarg):
                warnings.warn(
                    "Option %s is not used by this backend" % kwarg,
                    # warnings.UserWarning,
                    stacklevel=2,
                )
        options = {
            "shots": kwargs.get("shots", self.options.shots),
            "reward": kwargs.get("reward", self.options.reward),
        }

        qasm_data = qasm2.dumps(circuit)
        job_id = submit_job(
            self.near_blockchain,
            self.ipfs_gateway,
            qasm_data,
            circuit.num_qubits,
            circuit.depth(),
            options,
        )
        return DQPUJob(self, job_id, options, circuit)
