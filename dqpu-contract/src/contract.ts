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

@NearBindgen({ requireInit: true })
class DQPU {
  owner: AccountId = '';
  jobs = new UnorderedMap<Job>('jid-1');
  verifiers = new UnorderedMap<AccountId>('vid-1');
  latest_jid: bigint = BigInt(0);
  money_handled: bigint = BigInt(0);

  @initialize({ privateFunction: true })
  init() {
    this.owner = near.predecessorAccountId();
    this.verifiers.set(this.owner, this.owner);
  }

  // Submit a new quantum job
  @call({ payableFunction: true })
  submit_job({ qubits, deep, shots, job_file }: { qubits: number, deep: number, shots: number, job_file: string }) {
    this.latest_jid += BigInt(1);

    const j: Job = {
      id: this.latest_jid,
      owner_id: near.predecessorAccountId(),
      reward_amount: near.attachedDeposit() as bigint,
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

    this.jobs.set(`${j.id}`, j);
    this.money_handled += j.reward_amount;

    return this.latest_jid;
  }

  // Called by validators, set the validity of a pending-validation job
  @call({})
  set_job_validity({ job_id, valid }: { job_id: string, valid: boolean }) {
    // TODO: Check if the predecessorAccountId() is a verifier

    // Set job validity
    const j: Job = this.get_job(job_id);

    assert(j.status == 'pending-validation', `Job ${job_id} is not in 'pending-validation' state`);

    j.verifier_id = near.predecessorAccountId();

    if (valid)
      j.status = 'waiting';
    else
      j.status = 'invalid';

    this.jobs.set(`${j.id}`, j);
  }

  // Submit a result for a waiting job, with the caution
  @call({ payableFunction: true })
  submit_job_result({ job_id, result_file }: { job_id: string, result_file: string }) {
    const j: Job = this.get_job(job_id);

    let deposit: bigint = near.attachedDeposit() as bigint;

    assert(deposit >= (j.reward_amount / BigInt(10)), `Deposit should be greater than ${j.reward_amount / BigInt(10)}`);
    assert(j.status == 'waiting', `Job ${job_id} is not in 'waiting' state`);

    j.result_file = result_file;
    j.status = 'validating-result';
    j.sampler_id = near.predecessorAccountId();
    j.sampler_deposit = deposit;
    this.money_handled += deposit;

    this.jobs.set(`${j.id}`, j);
  }

  // Called by validators, set the validity of a job result for a 'validating-result' job
  @call({})
  set_result_validity({ job_id, valid }: { job_id: string, valid: boolean }) {
    // TODO: Check if the predecessorAccountId() is a verifier

    // Set job validity
    const j: Job = this.get_job(job_id);

    assert(j.status == 'validating-result', `Job ${job_id} is not in 'validating-result' state`);

    if (valid) {
      j.status = 'executed';
    } else {
      j.status = 'waiting';
      j.sampler_id = '';

      // Send the sampler deposit to verifier
      const promise = near.promiseBatchCreate(near.predecessorAccountId());
      near.promiseBatchActionTransfer(promise, j.sampler_deposit);

      j.sampler_deposit = BigInt(0);
    }

    this.jobs.set(`${j.id}`, j);
  }


  // Get latest quantum job list
  @view({})
  get_jobs({ from_index = 0, limit = 50 }: { from_index: number, limit: number }): Job[] {
    const ret: Job[] = [];

    for (const job_id of this.jobs.keys({ start: from_index, limit })) {
      const j: Job = this.get_job(job_id);
      ret.push(j);
    }

    return ret
  }

  // Get a single quantum job by its id
  @view({})
  get_job(job_id: string): Job {
    return this.jobs.get(job_id);
  }

  // Get a quantum job status by its id
  @view({})
  get_job_status(job_id: string): JobStatus {
    const j: Job = this.jobs.get(job_id);
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
  @call({ privateFunction: true })
  add_verifier(verifier_id: AccountId) {
    assert(near.predecessorAccountId() == this.owner, 'Only callable by owner');
    this.verifiers.set(verifier_id, verifier_id);
  }

  // Remove a verifier
  @call({ privateFunction: true })
  remove_verifier(verifier_id: AccountId) {
    assert(near.predecessorAccountId() == this.owner, 'Only callable by owner');
    this.verifiers.remove(verifier_id);
  }

  // Change contract owner
  @call({ privateFunction: true })
  set_owner(new_owner: AccountId) {
    assert(near.predecessorAccountId() == this.owner, 'Only callable by owner');
    this.owner = new_owner;
  }
}