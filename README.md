# dqpu

![CI Status](https://github.com/dakk/dqpu/actions/workflows/ci.yaml/badge.svg)
![Contract CI Status](https://github.com/dakk/dqpu/actions/workflows/ci-contract.yaml/badge.svg)
![PyPI - Version](https://img.shields.io/pypi/v/dqpu)
![License: Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-blue)
[![Downloads](https://static.pepy.tech/badge/dqpu)](https://pepy.tech/project/dqpu)

A Web3-Powered (Near), Decentralized Quantum Simulator with Verifiable Computation. 

DQPU (Decentralized Quantum Processing Unit) introduces a novel, decentralized approach to quantum computing that leverages the power of blockchain and smart contracts. It addresses the challenge of securely and reliably delegating the execution of quantum computations in a trustless and transparent manner, encouraging competition between independent quantum resource providers.


## Workflow

The DQPU system is composed of 3 actors:

- *Clients*: users who need to perform a quantum sampling paying a reward
- *Verifiers*: delegates who check for data validity and detect cheating users; they receive a reward for checking quantum sampling result validity
- *Samplers*: users who run quantum samplers (either simulator or real quantum computers) and receive
a reward for doing sampling

The following process outlines how clients can submit quantum circuits for sampling using the DQPU contract:

1. **Client Submits Job**: A *Client* sends a quantum circuit along with a reward to the DQPU smart contract. The circuit data is uploaded to a distributed file storage system like IPFS. The smart contract adds the job to a queue in a 'pending-validation' state with the associated reward.

2. **Verifier Validates Circuit**: A *Verifier*[^1] validates the submitted circuit. This might involve checks for syntax errors or ensuring the circuit is within allowed parameters. The verifier also adds special verification elements (traps) into the circuit and add the new circuit to the contract[^2]. Once validated, the job moves to a 'waiting' state, becomes 'invalid' otherwise.

3. **Simulation or Hardware Execution**: A *Sampler* retrieves a job from the waiting list. It then either simulates the circuit on a software program or executes it on real quantum hardware, depending on the job requirements and available resources. The simulation or execution result is submitted back to the smart contract with a security deposit (a percentage of the reward). The job status changes to 'validating'.

4. **Verifier Checks Result**: The same *Verifier* from step 2 examines the returned result. The *Verifier* specifically checks the traps inserted earlier to ensure the result hasn't been tampered with. If the trap verification succeeds, the job status is updated to 'executed' and the trap is disclosed by the *Verifier*. The *Sampler* account receives the reward, while the *Verifier* receives a percentage of this reward.
If the trap verification fails, the job returns in 'waiting' state (and the *Verifier* receives the security deposit of the *Sampler*).

5. **Client Receives Result**: Once the job is marked as 'executed', the *Client* can retrieve the final result from the smart contract.

[^1]: In this first version of the contract, *Verifiers* are trusted entities designated by the smart contract creator.
[^2]: This step will become private in future versions of the protocol.
[^3]: In the next version of the protocol, the client will also add its trap in order to check *verifier*'s loyalty.


## Smart Contract Web UI

A web interface showing the smart contract status is available here: [https://dqpu.io/app](https://dqpu.io/app)


## Installation

```pip install dqpu```

Or install the latest development version:

```bash
git clone https://github.com/dakk/dqpu
cd dqpu
python setup.py install
```

Install IPFS:
- https://docs.ipfs.tech/install/command-line/#install-official-binary-distributions

## Usage: simulating a quantum circuit

The workflow described before is hidden to the final user: DQPU can be used seamleassy as any other quantum backend as any other quantum sampler. Currently DQPU implements a **qiskit** wrapper, a low level library for accessing the system primitives and a cli tool.

### Qiskit example

```python
import time
import qiskit
from qiskit.providers.jobstatus import JobStatus 
from dqpu.backends.qiskit import DQPUBackend

# Create a quantum circuit
qc = qiskit.QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Inizialize the DQPU backend and load the account
backend = DQPUBackend()
backend.load_account("dqpu_alice.testnet")

# Run the sampling
circ = transpile(qc, backend)
job = backend.run(circ, shots=1024)

# Wait for the job
while job.status() is JobStatus.RUNNING:
    print(f'Job {job.job_id()} is still running, please wait')
    time.sleep(1)

# Get the result
counts = job.result().get_counts(circ)
print(counts)
```

### Low-level example

```python
import time
from dqpu.blockchain import NearBlockchain, IPFSGateway
from dqpu.backends.base import submit_job, job_status, job_result

# Load account and initialize ipfs
nb = NearBlockchain('dqpu_alice.testnet')
ipfs = IPFSGateway()  # noqa: F841

f = open('test.qasm', 'r')
qasm_data = f.read()
jid = submit_job(nb, ipfs, qasm_data)
  
while job_status(nb, jid) != 'executed':
  print(f'Job {job.job_id()} is still running, please wait')
  time.sleep(1)

counts = job_result(nb, ipfs, jid)
print(counts)
```


### Cli tool usage

Read [dqpu.io/docs/cli](https://dqpu.io/docs/cli.html) for details.


## Usage: running a sampler / verifier node node

Read [dqpu.io/nodes](https://dqpu.io/nodes) for details.


## Contributing

Read [CONTRIBUTING](CONTRIBUTING.md) for details.

## License

This software is licensed with [Apache License 2.0](LICENSE).


## Cite

```
@software{dqpu2024,
  author = {Davide Gessa},
  title = {dqpu: A Web3-Powered, Decentralized Quantum Simulator with Verifiable Computation },
  url = {https://github.com/dakk/dqpu},
  year = {2024},
}
```

## About the author

Davide Gessa (dakk)
- https://twitter.com/dagide
- https://mastodon.social/@dagide 
- https://dakk.github.io/
- https://medium.com/@dakk