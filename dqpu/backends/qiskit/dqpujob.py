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

from ...verifier import BasicTrapInfo, BasicTrapper
from ..base import job_remove, job_result, job_status


class DQPUJob(Job):
    def __init__(self, backend, job_id, options, circuit):
        super().__init__(backend, job_id)
        self._backend = backend
        self.job_id = job_id
        self.options = options
        self.circuit = circuit
        self._results = None

    def submit(self):
        pass

    def _wait_for_result(self, timeout=None, wait=5):
        start_time = time.time()

        while True:
            elapsed = time.time() - start_time
            if timeout and elapsed >= timeout:
                raise JobTimeoutError("Timed out waiting for result")
            status = job_status(self._backend.near_blockchain, self.job_id)
            if status == "executed":
                break
            if status == "invalid":
                raise JobError("Job has been marked as invalid")
            time.sleep(wait)

        if self._results is None:
            self._results = job_result(
                self._backend.near_blockchain, self._backend.ipfs_gateway, self.job_id
            )
        return self._results

    def result(self, timeout=None, wait=5):
        counts, trap_list = self._wait_for_result(timeout, wait)

        # TODO: handle different trap classes
        traps = list(map(BasicTrapInfo.loads, trap_list))
        counts = BasicTrapper().untrap_results(traps, counts)

        results = [
            {
                "success": True,
                "header": {"name": self.circuit.name},
                "shots": len(counts),
                "data": {"counts": counts},
            }
        ]
        return Result.from_dict(
            {
                "results": results,
                "backend_name": self._backend.configuration().backend_name,
                "backend_version": self._backend.configuration().backend_version,
                "job_id": self.job_id,
                "qobj_id": self.circuit.name,
                "success": True,
            }
        )

    def remove(self):
        return job_remove(self._backend.near_blockchain, self.job_id)

    def status(self):
        status = job_status(self._backend.near_blockchain, self.job_id)
        if status == "executed":
            status = JobStatus.DONE
        elif status == "invalid":
            status = JobStatus.ERROR
        else:
            status = JobStatus.RUNNING
        return status


def submit(self):
    raise NotImplementedError
