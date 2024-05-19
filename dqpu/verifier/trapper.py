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

from typing import Optional, Sequence, Tuple

from ..q import Circuit, ExperimentResult


class TrapInfo:
    def __init__(self, trap_method, q_idx):
        self.trap_method = trap_method
        self.qubit = q_idx

    def dump(self, format="json"):
        if format != "json":
            raise Exception("Format not supported")

        return {"method": self.trap_method, "qubit": self.qubit}

    def loads(data, format="json"):
        raise Exception("Abstract")


class Trapper:
    """Trapper class"""

    def __init__(self):
        raise Exception("Abstract")

    def trap(
        self, qc: Circuit, level: Optional[int] = None
    ) -> Tuple[Circuit, Sequence[TrapInfo]]:
        """Add traps to the quantum circuits `qc`"""
        raise Exception("Abstract")

    def untrap(self, trapped_qc, traps: Sequence[TrapInfo]) -> Circuit:
        """Remove traps from the quantum circuits `trapped_qc`"""
        raise Exception("Abstract")

    def untrap_results(
        self, traps: Sequence[TrapInfo], results: ExperimentResult
    ) -> ExperimentResult:
        """Get the results for the original circuit, stripping away trap qubits"""
        qbits = list(map(lambda x: x.qubit, traps))
        qbits.sort(reverse=True)
        n_results: ExperimentResult = {}

        for bs, counts in results.items():
            n_bs = bs
            for q in qbits:
                n_bs = n_bs[::-1][:q] + n_bs[::-1][q + 1 :]
                n_bs = n_bs[::-1]

            if n_bs in n_results:
                n_results[n_bs] += counts
            else:
                n_results[n_bs] = counts

        return n_results

    def verify(self, traps: Sequence[TrapInfo], results: ExperimentResult) -> bool:
        raise Exception("Abstract")
