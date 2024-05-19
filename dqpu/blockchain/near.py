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

import asyncio
import json
import os
from typing import Optional

from py_near.account import Account

from .blockchain import Blockchain

# export type JobStatus = 'pending-validation' | 'waiting' | 'validating-result'
# | 'executed' | 'invalid';

# class Job:
#     id: string
#     owner_id: AccountId
#     reward_amount: bigint
#     sampler_deposit: bigint
#     status: JobStatus

#     qubits: number
#     depth: number
#     shots: number

#     job_file: string
#     result_file: string

#     verifier_id: AccountId
#     sampler_id: AccountId


def to_near(v):
    return int(v * 1000000000000000000000000)


def from_near(v):
    return int(v) / 1000000000000000000000000.0


def asyncio_run_nested(v):
    try:
        return asyncio.run(v())
    except:
        import nest_asyncio

        get_ipython()  # type: ignore # noqa: F821
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(v())


class NearBlockchain(Blockchain):
    def __init__(self, account: str, network="testnet"):
        self.network = network

        if self.network == "testnet":
            self.contract = "dqpu_7.testnet"
            self.rpc_addr = "https://rpc.testnet.near.org"
        else:
            self.rpc_addr = "https://rpc.mainnet.near.org"

        self.account = self.load_account(account)

    def balance(self):
        async def v():
            return await self.account.get_balance()

        return from_near(asyncio.run(v()))

    def load_account(self, account: str):
        fn = account
        if "/" not in account:
            fn = os.path.expanduser(
                os.path.join("~", ".near-credentials", self.network, account + ".json")
            )

        with open(fn, "r") as wf:
            w = json.loads(wf.read())

            acc = Account(w["account_id"], w["private_key"], self.rpc_addr)

            async def v():
                await acc.startup()

            asyncio_run_nested(v)

            return acc

        raise Exception("No wallet")

    def view(self, view_name: str, params):
        async def v():
            return await self.account.view_function(self.contract, view_name, params)

        return asyncio_run_nested(v).result

    def call(self, function_name: str, params, amount=0):
        async def v():
            return await self.account.function_call(
                self.contract,
                function_name,
                params,
                amount=to_near(amount),
            )

        r = asyncio_run_nested(v)

        if "Failure" in r.status:
            raise Exception(r.status["Failure"])
        return r.transaction.hash

    # Submit a new quantum job
    def submit_job(self, qubits, depth, shots, job_file, reward):
        return self.call(
            "submit_job",
            {"qubits": qubits, "depth": depth, "shots": shots, "job_file": job_file},
            reward,
        )

    # Remove a pending-validation or waiting job
    def remove_job(self, id):
        return self.call("remove_job", {"id": id})

    # Called by validators, set the validity of a pending-validation job
    def set_job_validity(
        self, id: int, valid: bool, trapped_file: Optional[str] = None
    ):
        return self.call(
            "set_job_validity", {"id": id, "valid": valid, "trapped_file": trapped_file}
        )

    # Submit a result for a waiting job, with the caution
    def submit_job_result(self, id: int, result_file: str, deposit: int):
        return self.call(
            "submit_job_result", {"id": id, "result_file": result_file}, deposit
        )

    # Called by validators, set the validity of a job result for a 'validating-result' job
    def set_result_validity(self, id: int, valid: bool, trap_file: str = ""):
        return self.call(
            "set_result_validity", {"id": id, "valid": valid, "trap_file": trap_file}
        )

    # Get latest quantum job list
    def get_latest_jobs(self, limit=50):
        return self.view("get_latest_jobs", {"limit": limit})

    def get_jobs(self, index=0, limit=50):
        return self.view("get_jobs", {"from_index": index, "limit": limit})

    # Get a single quantum job by its id
    def get_job(self, id: str):
        return self.view("get_job", {"id": id})

    # Get a quantum job status by its id
    def get_job_status(self, id: str):
        return self.view("get_job_status", {"id": id})

    def get_number_of_jobs(self):
        return self.view("get_number_of_jobs", {})

    def get_number_of_verifiers(self):
        return self.view("get_number_of_verifiers", {})

    def get_handled_amount(self):
        return self.view("get_handled_amount", {})

    # Clear all jobs
    def clear_jobs(self):
        return self.call("clear_jobs", {})

    def get_jobs_stats(self, limit=1000):
        return self.view("get_jobs_stats", {"limit": limit})

    # Add a verifier
    def add_verifier(self, account):
        return self.call("add_verifier", {"account": account})

    # Remove a verifier
    def remove_verifier(self, account):
        return self.call("remove_verifier", {"account": account})

    # Return true if the account is a verifier
    def is_a_verifier(self, account):
        return self.view("is_a_verifier", {"account": account})

    def get_verifiers(self):
        return self.view("get_verifiers", {})

    # Change contract owner
    def set_owner(self, account):
        return self.call("set_owner", {"new_owner": account})
