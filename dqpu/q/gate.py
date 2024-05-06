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


class Gate:
    def __init__(self, iden, matrix, nq=1):
        self.iden = iden
        self.nq = nq
        self._matrix = matrix

        try:
            self._tensor = np.reshape(self._matrix, (2, 2, 2, 2))
        except:
            self._tensor = None

    @property
    def matrix(self):
        if callable(self._matrix):
            raise Exception("This gate needs parameter")

        return self._matrix

    def parametrized(self, p):
        return Gate(self.iden, self._matrix(p), self.nq)


class GateCombination:
    def __init__(self, iden, gates, nq):
        self.iden = iden
        self.nq = nq
        self.gates = []  # Pairs of (Gate, qbidx)
