// Copyright 2024 Davide Gessa
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { NearBindgen, near, call, view, UnorderedMap, assert, initialize } from 'near-sdk-js';
import { AccountId } from 'near-sdk-js/lib/types';
import { Job, JobStatus } from './model';

const MAX_JOBS_STORED = 128;

// TODO: add max_job handling

@NearBindgen({ requireInit: true })
class DQPU {
    owner: AccountId = '';
    jobs = new UnorderedMap<Job>('jid-1');
    verifiers = new UnorderedMap<AccountId>('vid-1');
    latest_jid: bigint = BigInt(0);
    money_handled: bigint = BigInt(0);

    @initialize({ privateFunction: true })
    init({ owner }: { owner: AccountId }) {
        this.owner = owner;
        this.verifiers.set(this.owner, this.owner);
    }

    // Submit a new quantum job
    @call({ payableFunction: true })
    submit_job({ qubits, deep, shots, job_file }: { qubits: number, deep: number, shots: number, job_file: string }) {
        this.latest_jid += BigInt(1);

        const reward: bigint = near.attachedDeposit() as bigint;
        assert(reward > BigInt(0), 'Reward amount should be greater than 0');

        const j: Job = {
            id: this.latest_jid.toString(),
            owner_id: near.predecessorAccountId(),
            reward_amount: reward,
            sampler_deposit: BigInt(0),
            status: 'pending-validation',

            qubits: qubits,
            deep: deep,
            shots: shots,

            job_file: job_file,
            result_file: '',

            verifier_id: '',
            sampler_id: '',
        };

        this.jobs.set(j.id, j);
        this.money_handled += j.reward_amount;

        return this.latest_jid;
    }

    // Remove a pending-validation or waiting job
    @call({})
    remove_job({ id }: { id: string }) {
        const j = this.jobs.get(id);

        assert(j.owner_id == near.predecessorAccountId(), 'Only the job creator can remove it');
        assert(j.status == 'pending-validation' || j.status == 'waiting', 'Only waiting or pending-validation job can be removed');

        // Send the reward back to the client
        const promise = near.promiseBatchCreate(j.owner_id);
        near.promiseBatchActionTransfer(promise, j.reward_amount);
        
        this.jobs.remove(id);
    }


    // Called by validators, set the validity of a pending-validation job
    @call({})
    set_job_validity({ id, valid }: { id: string, valid: boolean }) {
        assert(this.verifiers.get(near.predecessorAccountId()) != null, 'Only a verifier can set job validity');

        // Set job validity
        const j: Job = this.jobs.get(id);

        assert(j.status == 'pending-validation', `Job ${id} is not in 'pending-validation' state`);

        j.verifier_id = near.predecessorAccountId();

        if (valid)
            j.status = 'waiting';
        else {
            j.status = 'invalid';

            // Send the reward back to the client
            const promise = near.promiseBatchCreate(j.owner_id);
            near.promiseBatchActionTransfer(promise, j.reward_amount);
        }

        this.jobs.set(j.id, j);
    }

    // Submit a result for a waiting job, with the caution
    @call({ payableFunction: true })
    submit_job_result({ id, result_file }: { id: string, result_file: string }) {
        const j: Job = this.jobs.get(id);

        let deposit: bigint = near.attachedDeposit() as bigint;

        assert(deposit >= (j.reward_amount / BigInt(10)), `Deposit should be greater than ${j.reward_amount / BigInt(10)}`);
        assert(j.status == 'waiting', `Job ${id} is not in 'waiting' state`);

        j.result_file = result_file;
        j.status = 'validating-result';
        j.sampler_id = near.predecessorAccountId();
        j.sampler_deposit = deposit;
        this.money_handled += deposit;

        this.jobs.set(j.id, j);
    }

    // Called by validators, set the validity of a job result for a 'validating-result' job
    @call({})
    set_result_validity({ id, valid }: { id: string, valid: boolean }) {
        assert(this.verifiers.get(near.predecessorAccountId()) != null, 'Only a verifier can set job validity');

        // Set job validity
        const j: Job = this.jobs.get(id);

        assert(j.status == 'validating-result', `Job ${id} is not in 'validating-result' state`);

        if (valid) {
            j.status = 'executed';

            // Send the sampler deposit to verifier
            const promise = near.promiseBatchCreate(j.verifier_id);
            near.promiseBatchActionTransfer(promise, j.sampler_deposit);

            // Send the reward to the sampler
            const promise2 = near.promiseBatchCreate(j.sampler_id);
            near.promiseBatchActionTransfer(promise2, j.reward_amount);            
        } else {
            j.status = 'waiting';
            j.sampler_id = '';

            // Send the sampler deposit to verifier
            const promise = near.promiseBatchCreate(near.predecessorAccountId());
            near.promiseBatchActionTransfer(promise, j.sampler_deposit);

            j.sampler_deposit = BigInt(0);
        }

        this.jobs.set(j.id, j);
    }


    // Get latest quantum job list
    @view({})
    get_jobs({ from_index = 0, limit = 50 }: { from_index: number, limit: number }): Job[] {
        const ret: Job[] = [];

        for (const id of this.jobs.keys({ start: from_index, limit })) {
            const j: Job = this.jobs.get(id);
            ret.push(j);
        }

        return ret
    }

    // Get a single quantum job by its id
    @view({})
    get_job({ id }: { id: string }): Job {
        return this.jobs.get(id);
    }

    // Get a quantum job status by its id
    @view({})
    get_job_status({ id }: { id: string }): JobStatus {
        const j: Job = this.jobs.get(id);
        return j.status;
    }

    @view({})
    get_number_of_jobs(): number {
        return this.jobs.length;
    }

    @view({})
    get_handled_amount(): bigint {
        return this.money_handled;
    }


    // Add a verifier
    @call({})
    add_verifier(account: AccountId) {
        assert(near.predecessorAccountId() == this.owner, 'Only callable by owner');
        this.verifiers.set(account, account);
    }

    // Remove a verifier
    @call({})
    remove_verifier(account: AccountId) {
        assert(near.predecessorAccountId() == this.owner, 'Only callable by owner');
        this.verifiers.remove(account);
    }

    // Return true if the caller is a verifier
    @view({})
    is_a_verifier(account: AccountId): boolean {
        return this.verifiers.get(account) != null;
    }

    // Change contract owner
    @call({})
    set_owner(new_owner: AccountId) {
        assert(near.predecessorAccountId() == this.owner, 'Only callable by owner');
        this.owner = new_owner;
    }

    // Clear all jobs
    @call({})
    clear_jobs() {
        assert(near.predecessorAccountId() == this.owner, 'Only callable by owner');
        this.jobs.clear();
    }
}