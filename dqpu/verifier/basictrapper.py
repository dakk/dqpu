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

import copy
import random
from typing import Optional, Sequence, Tuple, cast

from ..q import Circuit, ExperimentResult, Gates
from .trapper import TrapInfo, Trapper


# TODO: make it base for other strategies, or move helpers to Trapper
class BasicTrapInfo(TrapInfo):
    def __init__(self, q_idx, val, prob=1.0):
        super().__init__("basic", q_idx)
        self.value_expected = val
        self.probability = prob

    def __repr__(self):
        return (
            f"qubit {self.qubit} expect to have value {self.value_expected} "
            f"with probability {self.probability} trapped with {self.trap_method}"
        )

    def dump(self, format="json"):
        if format != "json":
            raise Exception("Format not supported")

        data = super().dump(format)
        data["value_expected"] = self.value_expected
        data["probability"] = self.probability
        return data

    @staticmethod
    def loads(data, format="json"):
        if format != "json":
            raise Exception("Format not supported")

        return BasicTrapInfo(data["qubit"], data["value_expected"], data["probability"])


class BasicTrapper(Trapper):
    """A basic trapper, just adds `n` qubits initialized in a random choice of |0> and |1>"""

    def __init__(self):
        pass

    def trap(
        self, qc: Circuit, level: Optional[int] = None
    ) -> Tuple[Circuit, Sequence[BasicTrapInfo]]:
        """Add traps to the quantum circuit"""
        if level is None:
            level = 1

        qc = copy.deepcopy(qc)

        traps: Sequence[BasicTrapInfo] = []
        gates = qc.gates
        for i in range(level):
            qc.n_qbits += 1
            i_r = random.randint(0, qc.n_qbits - 1)

            def remap_qbit(q_idx):
                return q_idx + 1 if q_idx >= i_r else q_idx

            def remap_gate(gq):
                a, p = gq
                p = list(map(remap_qbit, p))
                return (a, p)

            def remap_trap(t):
                t.qubit = remap_qbit(t.qubit)
                return t

            gates = list(map(remap_gate, gates))
            traps = list(map(remap_trap, traps))

            v_e = False
            if not random.choice([True, False]):
                v_e = True
                gates.insert(random.randint(0, len(gates) - 1), (Gates.X, [i_r]))

            traps.append(BasicTrapInfo(i_r, v_e))

        qc.gates = gates
        return (qc, traps)

    def untrap(self, trapped_qc, traps: Sequence[TrapInfo]) -> Circuit:
        """Remove traps from the quantum circuits `trapped_qc`"""
        raise Exception("TODO")

    def verify(self, traps: Sequence[TrapInfo], results: ExperimentResult) -> bool:
        """Get bitstring result for trap qubits, and check for the result"""
        tl = {}

        for t in traps:
            tl[t.qubit] = {"0": 0, "1": 0}

        for bs, counts in results.items():
            bs = bs[::-1]  # This is for qiskit
            for t in traps:
                idx = t.qubit

                if bool(int(bs[idx])):
                    tl[idx]["1"] += counts
                else:
                    tl[idx]["0"] += counts

        for t in traps:
            v = tl[t.qubit]
            v_prob = abs((v["1"] - v["0"]) / (v["1"] + v["0"]))

            t_ = cast(BasicTrapInfo, t)
            if v_prob < t_.probability - 0.05 and v_prob > t_.probability + 0.05:
                return False

            vmax = False if v["0"] > v["1"] else True
            if vmax != t_.value_expected:
                return False

        return True
