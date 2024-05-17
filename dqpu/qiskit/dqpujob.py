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

import time

from qiskit.providers import JobError, JobTimeoutError
from qiskit.providers import JobV1 as Job
from qiskit.providers.jobstatus import JobStatus
from qiskit.result import Result


class DQPUJob(Job):
    def __init__(self, backend, job_id, job_json, circuits):
        super().__init__(backend, job_id)
        self._backend = backend
        self.job_json = job_json
        self.circuits = circuits

    def _wait_for_result(self, timeout=None, wait=5):
        start_time = time.time()
        result = None
        while True:
            elapsed = time.time() - start_time
            if timeout and elapsed >= timeout:
                raise JobTimeoutError("Timed out waiting for result")
            result = {"status": "waiting"}  # get_job_status(self._job_id)
            if result["status"] == "complete":
                break
            if result["status"] == "error":
                raise JobError("Job error")
            time.sleep(wait)
        return result

    def result(self, timeout=None, wait=5):
        result = self._wait_for_result(timeout, wait)
        results = [
            {"success": True, "shots": len(result["counts"]), "data": result["counts"]}
        ]
        return Result.from_dict(
            {
                "results": results,
                "backend_name": self._backend.configuration().backend_name,
                "backend_version": self._backend.configuration().backend_version,
                "job_id": self._job_id,
                "qobj_id": ", ".join(x.name for x in self.circuits),
                "success": True,
            }
        )

    def status(self):
        result = {"status": "waiting"}  # get_job_status(self._job_id)
        if result["status"] == "running":
            status = JobStatus.RUNNING
        elif result["status"] == "complete":
            status = JobStatus.DONE
        else:
            status = JobStatus.ERROR
        return status


def submit(self):
    raise NotImplementedError
