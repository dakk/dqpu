# DQPU Near Contract

This smart contract handles quantum jobs workflow as described in [../README.md](../README.md).


## Usage

### 1. Build and Test the Contract
You can automatically compile and test the contract by running:

```bash
npm run build
```

### 2. Create an Account and Deploy the Contract
You can create a new account and deploy the contract by running:

```bash
near create-account <your-account.testnet> --useFaucet
near deploy <your-account.testnet> build/release/dqpu.wasm --initFunction init --initArgs '{"owner": "dqpu_owner.testnet"}'
```

Or initialize it separately:

```bash
near call <contractId> init '{"owner": ""}' --accountId <accountId>
```

### 3. Retrieve data from view

```bash
# Use near-cli to get the greeting
near view <your-account.testnet> view_name
```

<br />

### 4. Perform a call

`Call` methods can only be invoked using a NEAR account, since the account needs to pay GAS for the transaction.

```bash
# Use near-cli to set a new greeting
near call <your-account.testnet> call_name '{"param":"value"}' --accountId <your-account.testnet>
```

**Tip:** If you would like to call `call_name` using another account, first login into NEAR using:

```bash
# Use near-cli to login your NEAR account
near login
```

and then use the logged account to sign the transaction: `--accountId <another-account>`.


#### Add a job

```bash
near call dqpu_7.testnet submit_job '{"qubits":2,"depth":2,"shots":128,"job_file": "ttt"}' --accountId dqpu_owner.testnet --deposit 1
```


### 5. Delete a contract

```bash
near delete dqpu_VERSION.testnet dqpu_owner.testnet
```


## Fake data creator

```bash
npx near deploy dqpu_7.testnet build/dqpu.wasm --initFunction init --initArgs '{"owner":"dqpu_owner.testnet"}'
npx near create-account dqpu_alice.testnet --useFaucet
npx near create-account dqpu_bob.testnet --useFaucet
```

```bash
npx near call dqpu_7.testnet submit_job '{"qubits":12,"depth":2,"shots":128,"job_file": "ttt"}' --accountId dqpu_alice.testnet --amount 0.001
npx near call dqpu_7.testnet submit_job '{"qubits":21,"depth":2,"shots":1024,"job_file": "ttt"}' --accountId dqpu_alice.testnet --amount 0.003
npx near call dqpu_7.testnet submit_job '{"qubits":8,"depth":2,"shots":512,"job_file": "ttt"}' --accountId dqpu_alice.testnet --amount 0.0013
npx near call dqpu_7.testnet submit_job '{"qubits":15,"depth":2,"shots":1024,"job_file": "ttt"}' --accountId dqpu_alice.testnet --amount 0.001
npx near call dqpu_7.testnet submit_job '{"qubits":11,"depth":2,"shots":1024,"job_file": "ttt"}' --accountId dqpu_alice.testnet --amount 0.001
npx near call dqpu_7.testnet submit_job '{"qubits":26,"depth":2,"shots":1024,"job_file": "ttt"}' --accountId dqpu_alice.testnet --amount 0.008
```

```bash
npx near call dqpu_7.testnet set_job_validity '{"id": 1, "valid": true, "trapped_file": "tt"}' --accountId dqpu_owner.testnet
npx near call dqpu_7.testnet set_job_validity '{"id": 2, "valid": false}' --accountId dqpu_owner.testnet
npx near call dqpu_7.testnet set_job_validity '{"id": 3, "valid": true, "trapped_file": "tt"}' --accountId dqpu_owner.testnet
npx near call dqpu_7.testnet set_job_validity '{"id": 4, "valid": true, "trapped_file": "tt"}' --accountId dqpu_owner.testnet
npx near call dqpu_7.testnet set_job_validity '{"id": 5, "valid": true, "trapped_file": "tt"}' --accountId dqpu_owner.testnet
```

```bash
npx near call dqpu_7.testnet submit_job_result '{"id": 1, "result_file": "ttr"}' --accountId dqpu_bob.testnet --amount 0.0002
npx near call dqpu_7.testnet submit_job_result '{"id": 3, "result_file": "ttr"}' --accountId dqpu_bob.testnet --amount 0.0002
npx near call dqpu_7.testnet submit_job_result '{"id": 4, "result_file": "ttr"}' --accountId dqpu_bob.testnet --amount 0.0002
```


```bash
npx near call dqpu_7.testnet set_result_validity '{"id": 1, "valid": true}' --accountId dqpu_owner.testnet 
npx near call dqpu_7.testnet set_result_validity '{"id": 3, "valid": true}' --accountId dqpu_owner.testnet
```


```bash
npx near view dqpu_7.testnet get_jobs_stats '{}'
```



## Future Ideas

- Introduce an incentivized system for creating quantum datasets; we may create automatic random challenges from the sha of the circuit, but we need a farmable token for this
- Add a job "hash"
- Add a "increase_job_reward" call