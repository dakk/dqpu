# dqpu

![CI Status](https://github.com/dakk/dqpu/actions/workflows/ci.yaml/badge.svg)
![License: Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-blue)

A Web3-Powered (Near), Decentralized Quantum Simulator with Verifiable Computation. 



## Workflow

The DQPU system is composed of 3 actors:

- *Clients*: users who need to perform a quantum sampling paying a reward
- *Verifiers*: delegates who check for data validity and detect cheating users; they receive a reward for checking quantum sampling result validity
- *Samplers*: users who run quantum samplers (either simulator or real quantum computers) and receive
a reward for doing sampling

The following process outlines how clients can submit quantum circuits for sampling using the DQPU contract:

1. **Client Submits Job**: A *Client* sends a quantum circuit along with a reward to the DQPU smart contract. The circuit data is uploaded to a distributed file storage system like IPFS. The smart contract adds the job to a queue in a 'pending' state with the associated reward.

2. **Verifier Validates Circuit**: A *Verifier*[^1] validates the submitted circuit. This might involve checks for syntax errors or ensuring the circuit is within allowed parameters. The verifier also adds special verification elements (traps) into the circuit. Once validated, the job moves to a 'waiting' state.

3. **Simulation or Hardware Execution**: A *Sampler* retrieves a job from the waiting list. It then either simulates the circuit on a software program or executes it on real quantum hardware, depending on the job requirements and available resources. The simulation or execution result is submitted back to the smart contract with a cautional deposit (a percentage of the reward). The job status changes to 'validating'.

4. **Verifier Checks Result**: The same *Verifier* from step 2 examines the returned result. The *Verifier* specifically checks the traps inserted earlier to ensure the result hasn't been tampered with. If the trap verification succeeds, the job status is updated to 'executed' and the *Sampler* account receives the reward, while the *Verifier* receives a percentage of this reward.
If the trap verification fails, the job returns in 'waiting' state (and the *Verifier* receives the cautional deposit of the *Sampler*).

5. **Client Receives Result**: Once the job is marked as 'executed', the *Client* can retrieve the final result from the smart contract.

[^1]: In this first version of the contract, *Verifiers* are trusted entities designated by the smart contract creator.


## Installation

```python setup.py install```

## Usage: running a sampling job

The workflow described before is hidden to the final user: DQPU can be used seamleassy as any other quantum backend as any other quantum sampler. Currently DQPU implements a **qiskit** wrapper, a low level library for accessing the system primitives and a cli tool.

### Qiskit example

```python
import time
import qiskit
from qiskit.providers.jobstatus import JobStatus 
from dqpu.qiskit import DQPUProvider, DQPUService

# Create a quantum circuit
qc = qiskit.QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

# Inizialize the service by providing the Near account
service = DQPUService()
service.setAccount("...")

# Run the sampling
backend = DQPUProvider().get_backend('dqpu_simulator')
job = backend.run(qc, reward="0.001")

# Wait for the job
while job.status() is JobStatus.RUNNING:
    print(f'Job {job.job_id()} is still running, please wait')
    time.sleep(1)

# Get the result
counts = job.result.get_counts()
print(counts)
```

### Low-level example

```python
from dqpu import *

# TODO
```


### Cli tool usage

```bash
$ dpqu-cli submit test.qasm --reward 0.01 --shots 1024
JOBID

$ dpqu-cli info JOBID
Job: JOBID
Status: WAITING
Qubits: 4
Deep: 9
Circuit uri: ipfs://.../test.qasm

$ dpqu-cli status JOBID
EXECUTED

$ dpqu-cli get-result JOBID
{ "0010": 1024 }
```


## Usage: running a sampler node

A sampler node continuously pool the DQPU smart contract waiting for new job. When a new job appear,
the sampler checks if it can perform the sampling with its hardware. 

Every sampler node can implement its own `Sampler` class, adding supports to other simulators or 
to real quantum hardware. DQPU package offer 3 implementation:
- AerSimulator: statevector simulator from qiskit
- DaskSimulator: statevector simulator using Dask distributed computing library
- NumpySimulator: statevector simulator using Numpy

After every sampled job, the node receives the reward.

```bash
dqpu-sampler --min-reward 0.0009 --sampler aersimulator
```


## Usage: running a verifier node

A verifier node continuously pool the DQPU smart contract waiting for new 'pending' and 'validating' jobs. When a new job appear, the verifiers:
- 'pending' job are checked for quantum circuit validity, and trap qubits are inserted
- 'validating' job are checked for trap verification

After every validation, the verifier receives a percentage of the job reward.

Verifier are special users initially selected by the smart contract creator; this will change in the future.

```bash
dqpu-verifier
```



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