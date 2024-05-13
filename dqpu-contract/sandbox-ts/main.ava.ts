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

import { setDefaultResultOrder } from 'dns'; setDefaultResultOrder('ipv4first'); // temp fix for node >v17
import { createTestObject } from './factory';

// Global context
const test = createTestObject();

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

    t.is(await contract.view('get_number_of_verifiers', {}), 1);

    await owner.call(contract, 'add_verifier', { account: alice.accountId });

    am_i = await contract.view('is_a_verifier', { account: alice.accountId });
    t.is(am_i, true);

    am_i = await contract.view('is_a_verifier', { account: owner.accountId });
    t.is(am_i, true);

    t.is(await contract.view('get_number_of_verifiers', {}), 2);
});
