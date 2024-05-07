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

from .gate import Gate


# Abstract class representing a circuit; it doesn't hold a quantum state
class Measure:
    def __init__(self):
        pass


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

    def apply(self, g, qb):
        self.gates.append((g, qb))

    def measure(self, qb, cb=None):
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
                elif a.iden == "SW":
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
