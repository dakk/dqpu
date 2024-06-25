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

import unittest

from dqpu.q import Circuit


class TestQ_Qasm_parsing(unittest.TestCase):  # noqa: N801
    def test_1(self):
        original = (
            "OPENQASM 2.0;\n"
            'include "qelib1.inc";\n'
            "qreg q[2];\n"
            "creg c[2];\n"
            "h q[0];\n"
            "cx q[0], q[1];\n"
            "measure q -> c;"
        )

        qc = Circuit.from_qasm_circuit(original)
        qc_a = qc.to_qasm_circuit()
        self.assertEqual(original, qc_a)

    def test_2(self):
        original = (
            "OPENQASM 2.0;\n"
            'include "qelib1.inc";\n'
            "qreg q[2];\n"
            "creg c[2];\n"
            "p(pi/32) q[0];\n"
            "cx q[0], q[1];\n"
            "measure q -> c;"
        )

        qc = Circuit.from_qasm_circuit(original)
        qc_a = qc.to_qasm_circuit()
        self.assertEqual(original, qc_a)
