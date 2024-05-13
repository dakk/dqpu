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

```near call dqpu_4.testnet submit_job '{"qubits":2,"deep":2,"shots":128,"job_file": "ttt"}' --accountId dqpu_owner.testnet --deposit 1```


### 5. Delete a contract

```
near delete dqpu_VERSION.testnet dqpu_owner.testnet
```