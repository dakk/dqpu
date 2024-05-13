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

import { NEAR } from 'near-workspaces';
import { setDefaultResultOrder } from 'dns'; setDefaultResultOrder('ipv4first'); // temp fix for node >v17
import { createTestObject } from './factory.ts';

// Global context
const test = createTestObject();

test('add a job and submit an invalid result', async (t) => {
    const { root, contract, alice, bob, owner } = t.context.accounts;

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
        id: jid, valid: true
    });

    // t.is((await alice.balance()).total, alice_initial_balance.total);

    t.is(await contract.view('get_job_status', { id: jid }), 'waiting');

    // Low deposit
    await t.throwsAsync(async () => { await bob.call(contract, 'submit_job_result', {
        id: jid, result_file: 'b21aa'
    }, { attachedDeposit: NEAR.parse('0.01 N') }); });


    await bob.call(contract, 'submit_job_result', {
        id: jid, result_file: 'b21aa'
    }, { attachedDeposit: NEAR.parse('0.1 N') });

    t.is(await contract.view('get_job_status', { id: jid }), 'validating-result');

    await owner.call(contract, 'set_result_validity', {
        id: jid, valid: false
    });

    t.is(await contract.view('get_job_status', { id: jid }), 'waiting');

    // TODO: bob should have INIT - reward/10
    // t.is((await alice.balance()).total, alice_initial_balance.total.sub(NEAR.parse('1N').sub(NEAR.parse('0.001 N'))));
});

