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

from typing import Any

from qiskit.circuit import Measure, Parameter
from qiskit.circuit.library import CXGate, IGate, PhaseGate, SXGate, UGate
from qiskit.providers import BackendV2 as Backend
from qiskit.providers import Options
from qiskit.transpiler import Target

from .dqpujob import DQPUJob


class DQPUBackend(Backend):
    def __init__(self, provider, network: str = "testnet"):
        super().__init__()

        self.network = network
        self.provider = provider

        # Create Target
        self._target = Target("Target for My Backend")
        # Instead of None for this and below instructions you can define
        # a qiskit.transpiler.InstructionProperties object to define properties
        # for an instruction.
        lam = Parameter("λ")
        p_props = {(qubit,): None for qubit in range(5)}
        self._target.add_instruction(PhaseGate(lam), p_props)
        sx_props = {(qubit,): None for qubit in range(5)}
        self._target.add_instruction(SXGate(), sx_props)
        phi = Parameter("φ")
        theta = Parameter("ϴ")
        u_props = {(qubit,): None for qubit in range(5)}
        self._target.add_instruction(UGate(theta, phi, lam), u_props)
        cx_props = {edge: None for edge in [(0, 1), (1, 2), (2, 3), (3, 4)]}
        self._target.add_instruction(CXGate(), cx_props)
        meas_props = {(qubit,): None for qubit in range(5)}
        self._target.add_instruction(Measure(), meas_props)
        id_props = {(qubit,): None for qubit in range(5)}
        self._target.add_instruction(IGate(), id_props)

        # Set option validators
        self.options.set_validator("shots", (1, 8192))

    @property
    def target(self):
        return self._target

    @property
    def max_circuits(self):
        return 1

    @classmethod
    def _default_options(cls):
        return Options(shots=1024)

    def run(self, circuits, **kwargs):
        # serialize circuits submit to backend and create a job
        for kwarg in kwargs:
            if not hasattr(kwarg, self.options):
                print(  # warnings.warn(
                    "Option %s is not used by this backend" % kwarg,
                    # UserWarning,
                    # stacklevel=2,
                )
        # options = {
        #     "shots": kwargs.get("shots", self.options.shots),
        # }
        # job_json = convert_to_wire_format(circuit, options)
        # job_handle = submit_to_backend(job_jsonb)
        job_handle = ""
        job_json: Any = {}
        return DQPUJob(self, job_handle, job_json, circuits)
