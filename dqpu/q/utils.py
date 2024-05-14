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

import numpy as np


def qiskit_execute(c):
    from qiskit import transpile
    from qiskit_aer import AerSimulator

    qc = c.toQiskitCircuit()
    qc.measure_all()

    sim = AerSimulator(method="statevector")
    qc.save_statevector()
    circ = transpile(qc, sim)
    job = sim.run(circ, shots=1024)
    result = job.result()
    counts = result.get_counts()
    outputstate = result.get_statevector(circ, decimals=3)

    # i = 0
    # for x in outputstate:
    #     print (f'{fixbinlen(bin(i)[2:], c.n)} => {np.absolute(x) ** 2}')
    #     i+=1
    return outputstate, counts


def fixbinlen(v, nq=3):
    return ("0" * (nq - len(v)) + v)[::-1]


def states_string_rep(nq=3):
    state_strs = [bin(x) for x in range(2**nq)]
    for i in range(len(state_strs)):
        state_strs[i] = fixbinlen(state_strs[i][2:], nq)

    # state_strs = ['' for _ in range(2**nq)]
    # basis_strs = ['0', '1']

    # for q in range(nq):
    # 	for i in range(len(state_strs)):
    # 		b = basis_strs[((i//(2**q))) % 2]
    # 		state_strs[i] =  state_strs[i] + b

    return state_strs


def basis_state_probs(svec):
    return np.array([np.absolute(s) ** 2 for s in svec])


def print_output(nq, out):
    xx = basis_state_probs(out)
    yy = states_string_rep(nq)

    for i in range(2**nq):
        print(yy[i], xx[i])


def plot_output(nq, out):
    import matplotlib.pyplot as plt

    nq = int(np.log2(out.shape[0]))
    fig, ax = plt.subplots(1, 1)
    ax.bar(range(2**nq), basis_state_probs(out))
    ax.set_xticks(range(2**nq))
    ax.set_xticklabels(states_string_rep(nq))
    ax.set_ylim(-0, 1)
    ax.grid(True)
    ax.set_ylabel(r"$P(S_c)$")
    ax.set_xlabel(r"$S_c$")
    plt.show()
