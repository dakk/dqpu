DQPU
====================================

DQPU is a Web3-Powered (Near), Decentralized Quantum Simulator with Verifiable Computation. 

DQPU (Decentralized Quantum Processing Unit) introduces a novel, decentralized approach to quantum computing that leverages the power of blockchain and smart contracts. It addresses the challenges of securely and reliably executing quantum computations in a trustless and transparent manner, while fostering a competitive ecosystem for quantum resource providers.


Workflow
--------

The DQPU system is composed of 3 actors:

-  *Clients*: users who need to perform a quantum sampling paying a
   reward
-  *Verifiers*: delegates who check for data validity and detect
   cheating users; they receive a reward for checking quantum sampling
   result validity
-  *Samplers*: users who run quantum samplers (either simulator or real
   quantum computers) and receive a reward for doing sampling

The following process outlines how clients can submit quantum circuits
for sampling using the DQPU contract:

1. **Client Submits Job**: A *Client* sends a quantum circuit along with
   a reward to the DQPU smart contract. The circuit data is uploaded to
   a distributed file storage system like IPFS. The smart contract adds
   the job to a queue in a ‘pending-validation’ state with the
   associated reward.

2. **Verifier Validates Circuit**: A *Verifier*\  [1]_ validates the
   submitted circuit. This might involve checks for syntax errors or
   ensuring the circuit is within allowed parameters. The verifier also
   adds special verification elements (traps) into the circuit and add
   the new circuit to the contract [2]_. Once validated, the job moves
   to a ‘waiting’ state, becomes ‘invalid’ otherwise.

3. **Simulation or Hardware Execution**: A *Sampler* retrieves a job
   from the waiting list. It then either simulates the circuit on a
   software program or executes it on real quantum hardware, depending
   on the job requirements and available resources. The simulation or
   execution result is submitted back to the smart contract with a
   security deposit (a percentage of the reward). The job status changes
   to ‘validating’.

4. **Verifier Checks Result**: The same *Verifier* from step 2 examines
   the returned result. The *Verifier* specifically checks the traps
   inserted earlier to ensure the result hasn’t been tampered with. If
   the trap verification succeeds, the job status is updated to
   ‘executed’ and the trap is disclosed by the *Verifier*. The *Sampler*
   account receives the reward, while the *Verifier* receives a
   percentage of this reward. If the trap verification fails, the job
   returns in ‘waiting’ state (and the *Verifier* receives the security
   deposit of the *Sampler*).

5. **Client Receives Result**: Once the job is marked as ‘executed’, the
   *Client* can retrieve the final result from the smart contract.

Smart Contract Web UI
---------------------

A web interface showing the smart contract status is available here:
https://dakk.github.io/dqpu/app/

Installation
------------

``pip install dqpu``

Or install the latest development version:

.. code:: bash

   git clone https://github.com/dakk/dqpu
   cd dqpu
   python setup.py install

Install IPFS: -
https://docs.ipfs.tech/install/command-line/#install-official-binary-distributions


.. toctree::
   :maxdepth: 2
   :caption: DQPU

   api
   qiskit_example.ipynb


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Cite
======

.. code-block:: latex

   @software{dqpu2024,
      author = {Davide Gessa},
      title = {dqpu: A Web3-Powered, Decentralized Quantum Simulator with Verifiable Computation },
      url = {https://github.com/dakk/dqpu},
      year = {2024},
   }