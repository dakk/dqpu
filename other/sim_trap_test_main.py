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

# import random
# import time

# from .q import Circuit, Gates, utils
# from .sampler import DaskSimulatorSampler
# from .verifier import BasicTrapper


# def main():
#     n = 4
#     depth = 2
#     qc = Circuit(n, 1)

#     for x in range(n):
#         qc.apply(Gates.H, x)

#     for y in range(depth - 1):
#         for x in range(n):
#             if random.choice([True, False]):
#                 qc.apply(
#                     random.choice([Gates.X, Gates.H, Gates.Y, Gates.Z, Gates.T]), x
#                 )
#             else:
#                 r1 = random.randint(0, n - 1)
#                 r2 = random.randint(0, n - 1)

#                 while r1 == r2:
#                     r1 = random.randint(0, n - 1)
#                     r2 = random.randint(0, n - 1)

#                 qc.apply(Gates.CX, (r1, r2))

#     for x in range(n):
#         qc.apply(Gates.H, x)

#     hs = DaskSimulatorSampler(qc)

#     s = time.time()
#     a = hs.compute()
#     print(a.compute())
#     print("time spent qse", time.time() - s)

#     trapper = BasicTrapper()
#     print(qc.to_qiskit_circuit().draw())
#     (qc2, t) = trapper.trap(qc)

#     s = time.time()
#     qsk, counts = utils.qiskit_execute(qc2)
#     print(qsk)
#     print("time spent qsk", time.time() - s)

#     print(qc2.to_qiskit_circuit().draw())
#     print(t)
#     print(counts)

#     print(trapper.verify(t, counts))

#     print(trapper.untrap_results(t, counts))

#     s = time.time()
#     qsk, counts = utils.qiskit_execute(qc)
#     print(counts)
