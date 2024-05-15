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

import random

import openqasm3
from openqasm3 import ast as oast

from .gate import Gate
from .gates import Gates


# Abstract class representing a circuit; it doesn't hold a quantum state
class Measure:
    def __init__(self):
        self.iden = "measure"


class Barrier:
    def __init__(self):
        pass


class Circuit:
    def __init__(self, qbn, cbn):
        self.n_qbits = qbn
        self.n_cbits = cbn
        self.gates = []

    def __iter__(self):
        yield from self.gates

    @staticmethod
    def random(n, dp, measure=False):
        qc = Circuit(n, n)

        for y in range(dp - 1):
            for x in range(n):
                if random.choice([True, False]) or n == 1:
                    qc.apply(
                        random.choice([Gates.X, Gates.H, Gates.Y, Gates.Z, Gates.T]),
                        [x],
                    )
                else:
                    r1 = random.randint(0, n - 1)
                    r2 = random.randint(0, n - 1)

                    while r1 == r2:
                        r1 = random.randint(0, n - 1)
                        r2 = random.randint(0, n - 1)

                    qc.apply(
                        random.choice([Gates.CX, Gates.CZ]), (r1, r2)
                    )  # Gates.SWAP,

        if measure:
            for x in range(n):
                qc.measure(x)

        return qc

    def apply(self, g, qb):
        self.gates.append((g, qb))

    def measure(self, qb, cb=None):
        if cb is None:
            cb = qb
        self.gates.append((Measure(), (qb, cb)))

    def draw(self):
        print(f"QC({self.n_qbits},{self.n_cbits})", end=" ==> ")
        for x in self.gates:
            if isinstance(x[0], Measure):
                print(f"Measure({x[1]})", end=" -- ")
            elif isinstance(x[0], Gate):
                print(f"{x[0].iden}({x[1]})", end=" -- ")
        print()

    def buildGraph(self):
        import matplotlib.pyplot as plt
        import networkx as nx

        G = nx.Graph()

        for x in self.gates:
            a, p = x

            if isinstance(a, Gate) and a.nq > 1:
                G.add_edge(p[0], p[1])

        options = {
            "font_size": 12,
            "node_size": 300,
            # "node_color": "white",
            # "edgecolors": "black",
            "linewidths": 1,
            "width": 1,
        }
        nx.draw_networkx(G, **options)

        # Set margins for the axes so that nodes aren't clipped
        ax = plt.gca()
        ax.margins(0.0010)
        plt.axis("off")
        plt.show()

    @staticmethod
    def fromQasmCircuit(qasm_data: str):  # noqa: C901
        def qubit_to_i(q):
            if not isinstance(q, oast.IndexedIdentifier):
                raise Exception("only indexed identifier allowed")
            if len(q.indices) != 1:
                raise Exception("only indexed identifier with 1 elemtn allowed")
            return q.indices[0][0].value

        qa = openqasm3.parser.parse(qasm_data)

        n_q = None
        n_c = None
        gates = []
        end = False

        for s in qa.statements:
            if end:
                raise Exception("Last statement should me a measurement")

            if isinstance(s, oast.QubitDeclaration):
                if n_q is not None:
                    raise Exception("Only one qubit register is allowed")
                n_q = s.size.value
            elif isinstance(s, oast.ClassicalDeclaration):
                if n_c is not None:
                    raise Exception("Only one classical register is allowed")
                n_c = s.type.size.value
            elif isinstance(s, oast.QuantumGate):
                p = list(map(qubit_to_i, s.qubits))
                gn = s.name.name.upper()
                if not hasattr(Gates, gn):
                    raise Exception(f"Unknown gate {gn}")

                g = getattr(Gates, gn)
                gates.append((g, p))
            elif isinstance(s, oast.QuantumMeasurementStatement):
                end = True
            elif isinstance(s, oast.Include):
                pass
            else:
                raise Exception(f"Unhandled {s}")

        qc = Circuit(n_q, n_c)
        qc.gates = gates
        return qc

    def toQasmCircuit(self):
        qasm = "OPENQASM 2.0;\n"
        qasm += 'include "qelib1.inc";\n'
        qasm += "qreg q[" + str(self.n_qbits) + "];\n"
        qasm += "creg c[" + str(self.n_qbits) + "];\n"

        for x in self.gates:
            # TODO: handle parameters
            a, p = x

            qbs = ", ".join(map(lambda g: "q[" + str(g) + "]", p))
            qasm += f"{a.iden.lower()} {qbs};\n"

        qasm += "measure q -> c;"

        return qasm

    def toQiskitCircuit(self):  # noqa: C901
        from qiskit import QuantumCircuit

        qc = QuantumCircuit(self.n_qbits, 0)

        for x in self.gates:
            a, p = x

            if isinstance(a, Gate):
                if a.iden == "CX":
                    qc.cx(p[0], p[1])
                elif a.iden == "CZ":
                    qc.cz(p[0], p[1])
                elif a.iden == "SWAP":
                    qc.swap(p[0], p[1])
                elif a.iden == "X":
                    qc.x(p)
                elif a.iden == "I":
                    qc.i(p)
                elif a.iden == "Z":
                    qc.z(p)
                elif a.iden == "Y":
                    qc.y(p)
                elif a.iden == "H":
                    qc.h(p)
                elif a.iden == "S":
                    qc.s(p)
                elif a.iden == "T":
                    qc.t(p)

            elif isinstance(a, Measure):
                qc.measure(p, p)

        return qc
