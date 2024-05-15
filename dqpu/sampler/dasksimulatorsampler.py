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

# import dask.array as da
# import numpy as np
# from dask.distributed import Client  # , progress
# from scipy.linalg import norm

# from ..q import Gate, Measure
# from .sampler import Sampler

# client = Client(
#     processes=False, threads_per_worker=1, n_workers=1, memory_limit="612MB"
# )


# class DaskSimulatorSampler(Sampler):
#     def __init__(self, circuit, dtype=np.csingle):
#         self.circuit = circuit
#         self.hs = None
#         self.measures = []
#         self.dtype = dtype

#     def compute(self):
#         self.hs = da.zeros(((2,) * self.circuit.n_qbits), dtype=self.dtype)
#         self.hs[(0,) * self.circuit.n_qbits] = 1
#         self.measures = []
#         projectors = [
#             da.array([[1, 0], [0, 0]], dtype=self.dtype),
#             da.array([[0, 0], [0, 1]], dtype=self.dtype),
#         ]

#         for x in self.circuit:
#             a, p = x

#             if isinstance(a, Gate) and a.nq == 2:
#                 pa, pb = p
#                 self.hs = da.tensordot(a._tensor, self.hs, ((2, 3), (pa, pb)))
#                 self.hs = da.moveaxis(self.hs, (0, 1), (pa, pb))

#             elif isinstance(a, Gate) and a.nq == 1:
#                 self.hs = da.tensordot(a.matrix, self.hs, (1, p))
#                 self.hs = da.moveaxis(self.hs, 0, p)

#             elif isinstance(a, Measure):

#                 def project(i, j):
#                     projected = da.tensordot(projectors[j], self.hs, (1, i))
#                     return da.moveaxis(projected, 0, i)

#                 pa, pb = p
#                 projected = project(pa, 0)
#                 norm_projected = norm(projected.flatten())
#                 if da.random.random() < norm_projected**2:
#                     self.hs = projected / norm_projected
#                     self.measures.append((pa, pb, 0))
#                 else:
#                     projected = project(p[0], 1)
#                     self.hs = projected / norm(projected)
#                     self.measures.append((pa, pb, 1))

#         return self.hs.flatten()

#     def compute_sep(self):  # noqa: C901
#         def tensor_product(matrix1, matrix2):
#             m, n = matrix1.shape
#             p, q = matrix2.shape
#             result = da.zeros((m * p, n * q), dtype=matrix1.dtype)
#             for i in range(m):
#                 for j in range(n):
#                     result[i * p : (i + 1) * p, j * q : (j + 1) * q] = (
#                         matrix1[i, j] * matrix2
#                     )
#             return result

#         def perform_quantum_gate(state_vector, gate, qbit):
#             matrices = []
#             for index in range(self.circuit.n_qbits):
#                 matrices.append(gate if index == qbit else np.identity(2))

#             mat = matrices[self.circuit.n_qbits - 1]
#             for index in range(self.circuit.n_qbits - 2, -1, -1):
#                 mat = tensor_product(matrices[index], mat)

#             state_vector = da.dot(state_vector, mat)
#             return state_vector

#         def perform_controlled_gate(state_vector, gate, control_qubit, target_qubit):
#             matrices = []
#             for index in range(self.circuit.n_qbits):
#                 if index == control_qubit:
#                     matrices.append(np.identity(2))
#                 elif index == target_qubit:
#                     matrices.append(gate)
#                 else:
#                     matrices.append(np.identity(2))

#             mat = matrices[self.circuit.n_qbits - 1]
#             for index in range(self.circuit.n_qbits - 2, -1, -1):
#                 mat = tensor_product(matrices[index], mat)

#             new_state_vector = da.zeros_like(state_vector)
#             for i in range(len(state_vector)):
#                 for j in range(len(mat)):
#                     new_state_vector[i] += state_vector[j] * mat[j][i]
#             return new_state_vector

#         self.hs = da.zeros((2**self.circuit.n_qbits), dtype=self.dtype)
#         self.hs[0] = 1
#         projectors = [
#             da.array([[1, 0], [0, 0]], dtype=self.dtype),
#             da.array([[0, 0], [0, 1]], dtype=self.dtype),
#         ]

#         for x in self.circuit:
#             a, p = x

#             if isinstance(a, Gate) and a.nq == 2:
#                 pa, pb = p
#                 self.hs = perform_controlled_gate(
#                     self.hs, a.matrix.reshape(4, 4)[2:, 2:], pa, pb
#                 )

#             elif isinstance(a, Gate) and a.nq == 1:
#                 self.hs = perform_quantum_gate(self.hs, a.matrix, p)

#             elif isinstance(a, Measure):

#                 def project(i, j):
#                     projected = da.tensordot(projectors[j], self.hs, (1, i))
#                     return da.moveaxis(projected, 0, i)

#                 pa, pb = p
#                 projected = project(pa, 0)
#                 norm_projected = norm(projected.flatten())
#                 if da.random.random() < norm_projected**2:
#                     self.hs = projected / norm_projected
#                     self.measures.append((pa, pb, 0))
#                 else:
#                     projected = project(p[0], 1)
#                     self.hs = projected / norm(projected)
#                     self.measures.append((pa, pb, 1))

#         return self.hs.flatten().compute()
