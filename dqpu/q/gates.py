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

import math

import numpy as np

from .gate import Gate

# import cupy as np

c_one = complex(1, 0)
c_zero = complex(0, 0)
ket_zero = np.array([c_one, c_zero])
ket_one = np.array([c_zero, c_one])


# Standard gates


class Gates:
    R = Gate(
        "R",
        lambda k: np.array(
            [[1, 0], [1, math.e ** ((2 * math.pi * complex(0, 1)) / 2**k)]]
        ),
    )
    I = Gate("I", np.array([[1, 0], [0, 1]]))  # noqa: E741
    X = Gate("X", np.array([[0, 1], [1, 0]]))
    Y = Gate("Y", np.array([[0, -1.0j], [+1.0j, 0]]))
    Z = Gate("Z", np.array([[1, 0], [0, -1]]))
    S = Gate("S", np.array([[1, 0], [0, +1.0j]]))
    T = Gate("T", np.array([[1, 0], [0, math.e ** (+1.0j * math.pi / 4)]]))
    H = Gate("H", 1 / np.sqrt(2) * np.array([[1, 1], [1, -1]]))

    CR = Gate(
        "CR", lambda k: np.kron(Gates.I.matrix, Gates.R.parametrized(k).matrix), 2
    )

    CX = Gate(
        "CX", np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]), 2
    )

    CZ = Gate(
        "CZ", np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]), 2
    )

    SWAP = Gate(
        "SWAP", np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]), 2
    )

    P0 = I  # Gate('P0', np.array([[1, 0], [0, 0]]))
    P1 = I  # Gate('P1', np.array([[0, 0], [0, 1]]))

    Gates1 = [
        I,
        X,
        # Y,
        Z,
        # S,
        # T,
        H,
    ]
    Gates2 = [CX, CZ, SWAP]
