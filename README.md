# dqpu

A Web3-Powered, Decentralized Quantum Simulator with Verifiable Computation. 


## Workflow

The DQPU system is composed of 3 actors:

- Clients: users who need to perform a quantum sampling in exchange of a reward
- Verifiers: delegated who check for data validity and detect cheating users
- Samplers: users who run quantum samplers (either simulator or real quantum computers) and receive
a reward for doing sampling

The following process outlines how clients can submit quantum circuits for sampling using the DQPU contract:

1. **Client Submits Job**: A client sends a quantum circuit along with a reward to the DQPU smart contract. The circuit data is uploaded to a distributed file storage system like IPFS. The smart contract adds the job to a queue in a 'pending' state with the associated reward.

2. **Verifier Validates Circuit**: A verifier designated by the smart contract validates the submitted circuit. This might involve checks for syntax errors or ensuring the circuit is within allowed parameters. The verifier also adds special verification elements (traps) into the circuit. Once validated, the job moves to a 'waiting' state.

3. **Simulation or Hardware Execution**: A sampler retrieves a job from the waiting list. It then either simulates the circuit on a software program or executes it on real quantum hardware, depending on the job requirements and available resources. The simulation or execution result is submitted back to the smart contract. The job status changes to 'validating'.

4. **Verifier Checks Result**: The same verifier from step 2 examines the returned result. The verifier specifically checks the traps inserted earlier to ensure the result hasn't been tampered with. If the trap verification succeeds, the job status is updated to 'executed' and the simulator account receives the reward.

5. **Client Receives Result**: Once the job is marked as 'executed', the client can retrieve the final result from the smart contract.


## Usage

The workflow described before is hidden to the final user: DQPU can be used seamleassy as any other quantum backend as any other quantum sampler. Currently DQPU implements a **qiskit** wrapper, and a raw library for accessing the system primitives.

### Qiskit example

```python
import time
import qiskit
from qiskit.providers.jobstatus import JobStatus 
from dqpu.qiskit import DQPUProvider

qc = qiskit.QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)

backend = DQPUProvider().get_backend('dqpu_simulator')
job = backend.run(qc)

while job.status() is JobStatus.RUNNING:
    print(f'Job {job.job_id()} is still running, please wait')
    time.sleep(1)

counts = job.result.get_counts()
print(counts)
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