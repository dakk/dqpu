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

// Global context
const test = anyTest as TestFn<{ worker: Worker, accounts: Record<string, NearAccount> }>;

test.beforeEach(async (t) => {
    // Create sandbox, accounts, deploy contracts, etc.
    const worker = t.context.worker = await Worker.init();

    // Deploy contract
    const root = worker.rootAccount;
    const contract = await root.createSubAccount('test-account');
    const owner = await root.createSubAccount('test-account-owner');
    const alice = await root.createSubAccount('test-account-alice');
    const bob = await root.createSubAccount('test-account-bob');

    // Get wasm file path from package.json test script in folder above
    await contract.deploy(
        process.argv[2],
    );

    await contract.call(contract, "init", { owner: owner.accountId });

    // Save state for test runs, it is unique for each test
    t.context.accounts = { root, contract, owner, alice, bob };
});

test.afterEach.always(async (t) => {
    // Stop Sandbox server
    await t.context.worker.tearDown().catch((error) => {
        console.log('Failed to stop the Sandbox:', error);
    });
});

test('returns the number of handled amount', async (t) => {
    const { contract } = t.context.accounts;
    const amount: string = await contract.view('get_handled_amount', {});
    t.is(amount, '0');
});

test('returns the number of jobs', async (t) => {
    const { contract } = t.context.accounts;
    const amount: number = await contract.view('get_number_of_jobs', {});
    t.is(amount, 0);
});

test('add a verifier and check the status', async (t) => {
    const { root, contract, alice, owner } = t.context.accounts;
    let am_i: boolean = await contract.view('is_a_verifier', { account: alice.accountId });
    t.is(am_i, false);

    await owner.call(contract, 'add_verifier', { account: alice.accountId });

    am_i = await contract.view('is_a_verifier', { account: alice.accountId });
    t.is(am_i, true);

    am_i = await contract.view('is_a_verifier', { account: owner.accountId });
    t.is(am_i, true);
});

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
    }, { attachedDeposit: NEAR.parse('1 N')}); //, gas: NEAR.parse('0.01 N') });

    // t.is((await alice.balance()).total, alice_initial_balance.total.sub(NEAR.parse('1N').sub(NEAR.parse('0.001 N'))));
    t.is(jid, '1');

    t.is(await contract.view('get_number_of_jobs', {}), 1);

    t.is(await contract.view('get_job_status', {id: jid}), 'pending-validation');

    await owner.call(contract, 'set_job_validity', { 
        id: jid, valid: false
    });

    // t.is((await alice.balance()).total, alice_initial_balance.total);

    t.is(await contract.view('get_job_status', {id: jid}), 'invalid');

    const j: Job = await contract.view('get_job', {id: jid});
    t.is(j.reward_amount.toString(), NEAR.parse('1 N').toBigInt().toString());
    t.is(j.shots, 128);
});

