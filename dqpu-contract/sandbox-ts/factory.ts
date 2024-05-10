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

export function createTestObject() {
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

    return test;
}