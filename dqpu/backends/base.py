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

import json
import tempfile


def submit_job(nb, ipfs, qasm_data, num_qubits, depth, options):
    fp = tempfile.NamedTemporaryFile(mode="w", delete=False)
    fp.write(qasm_data)
    fp.close()

    job_file = ipfs.upload(fp.name)

    nb.submit_job(num_qubits, depth, options["shots"], job_file, options["reward"])
    return nb.get_latest_jobs()[-1]["id"]


def job_status(nb, jid):
    return nb.get_job_status(jid)


def job_remove(nb, jid):
    return nb.remove_job(jid)


def job_result(nb, ipfs, jid):
    j = nb.get_job(jid)
    data = json.loads(ipfs.get(j["result_file"]))
    trap_list = json.loads(ipfs.get(j["trap_file"]))
    return data, trap_list
