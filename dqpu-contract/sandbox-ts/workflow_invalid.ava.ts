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

import { Worker, NearAccount, NEAR } from 'near-workspaces';
import anyTest, { TestFn } from 'ava';
import { Job } from '../src/model';
import { setDefaultResultOrder } from 'dns'; setDefaultResultOrder('ipv4first'); // temp fix for node >v17
import { createTestObject } from './factory';

// Global context
const test = createTestObject();

test('add a job and mark as invalid', async (t) => {
    const { root, contract, alice, owner } = t.context.accounts;

    t.is(await contract.view('get_number_of_jobs', {}), 0);

    const failCreation = alice.call(contract, 'submit_job', {
        qubits: 2, deep: 8, shots: 128, job_file: 'a12bff'
    });
    await t.throwsAsync(async () => { await failCreation });

    // const alice_initial_balance = await alice.balance();

    const jid: string = await alice.call(contract, 'submit_job', {
        qubits: 2, deep: 8, shots: 128, job_file: 'a12bff'
    }, { attachedDeposit: NEAR.parse('1 N') }); //, gas: NEAR.parse('0.01 N') });

    // t.is((await alice.balance()).total, alice_initial_balance.total.sub(NEAR.parse('1N').sub(NEAR.parse('0.001 N'))));
    t.is(jid, '1');

    t.is(await contract.view('get_number_of_jobs', {}), 1);

    t.is(await contract.view('get_job_status', { id: jid }), 'pending-validation');

    await owner.call(contract, 'set_job_validity', {
        id: jid, valid: false
    });

    // t.is((await alice.balance()).total, alice_initial_balance.total);

    t.is(await contract.view('get_job_status', { id: jid }), 'invalid');

    const j: Job = await contract.view('get_job', { id: jid });
    t.is(j.reward_amount.toString(), NEAR.parse('1 N').toBigInt().toString());
    t.is(j.shots, 128);
});

