---
html_theme.sidebar_secondary.remove:
sd_hide_title: true
---
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.9.0/css/fontawesome.min.css" integrity="sha512-TPigxKHbPcJHJ7ZGgdi2mjdW9XHsQsnptwE+nOUWkoviYBn0rAAt0A5y3B1WGqIHrKFItdhZRteONANT07IipA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
<style>
.bd-main .bd-content .bd-article-container {
  max-width: 70rem; /* Make homepage a little wider instead of 60em */
}
/* Extra top/bottom padding to the sections */
article.bd-article section {
  padding: 3rem 0 7rem;
}
/* Override all h1 headers except for the hidden ones */
h1:not(.sd-d-none) {
  font-weight: bold;
  font-size: 48px;
  text-align: center;
  margin-bottom: 4rem;
}
/* Override all h3 headers that are not in hero */
h3:not(#hero h3) {
  font-weight: bold;
  text-align: center;
}
</style>

(homepage)=
# DQPU: Decentralized Quantum Processing Unit

<div id="hero">

<div id="hero-left">  <!-- Start Hero Left -->
  <h2 style="font-size: 60px; font-weight: bold; margin: 2rem auto 0;">DQPU</h2>
  <h3 style="font-weight: bold; margin-top: 0;">The Decentralized QPU</h3>
  <p>DQPU (Decentralized Quantum Processing Unit) lets you run your quantum programs in a trustless and decentralized network of quantum resource providers, leveraging the power of blockchain and smart contracts.</p>

<div class="homepage-button-container">
  <div class="homepage-button-container-row">
      <a href="./docs/qiskit_example.html" class="homepage-button primary-button">Get Started</a>
      <a href="https://dqpu.io/app" target="_blank" class="homepage-button secondary-button">App UI</a>
  </div>
  <div class="homepage-button-container-row">
      <a href="./docs/index.html" class="homepage-button-link">See Documentation →</a>
      <a href="https://github.com/dakk/dqpu" class="homepage-button-link">See Source Code →</a>
  </div>
</div>
</div>  <!-- End Hero Left -->
<div id="hero-right">

```bash
pip install dqpu
```

```python
from dqpu.backends.qiskit import DQPUBackend

backend = DQPUBackend()
backend.load_account("dqpu_alice.testnet")

job = backend.run(quantum_circuit, shots=1024)
counts = job.result().get_counts(circ)
```

</div>

</div>  <!-- End Hero -->



# Workflow

<p>The DQPU system is composed of 3 actors:</p>
<br>

::::{grid} 1 1 3 3

:::{grid-item}

<div align="center">
<i class="fa fa-user fa-5x"></i><br><br>

<b>Clients</b>: users who need to perform a quantum sampling
</div>

:::

:::{grid-item}
<div align="center">
<i class="fa fa-user-shield fa-5x"></i><br><br>
<b>Verifiers</b>: delegates who check for data validity and detect cheating users
</div>
:::

:::{grid-item}
<div align="center">
<i class="fa fa-cogs fa-5x"></i><br><br>
<b>Samplers</b>: users who run quantum samplers
</div>
:::

::::


The following process outlines how clients can submit quantum circuits for sampling using the DQPU contract:

1. **Client Submits Job**: A *Client* sends a quantum circuit along with a reward to the DQPU smart contract. The circuit data is uploaded to a distributed file storage system like IPFS. The smart contract adds the job to a queue in a 'pending-validation' state with the associated reward.

2. **Verifier Validates Circuit**: A *Verifier* validates the submitted circuit. This might involve checks for syntax errors or ensuring the circuit is within allowed parameters. The verifier also adds special verification elements (traps) into the circuit and add the new circuit to the contract. Once validated, the job moves to a 'waiting' state, becomes 'invalid' otherwise.

3. **Simulation or Hardware Execution**: A *Sampler* retrieves a job from the waiting list. It then either simulates the circuit on a software program or executes it on real quantum hardware, depending on the job requirements and available resources. The simulation or execution result is submitted back to the smart contract with a security deposit (a percentage of the reward). The job status changes to 'validating'.

4. **Verifier Checks Result**: The same *Verifier* from step 2 examines the returned result. The *Verifier* specifically checks the traps inserted earlier to ensure the result hasn't been tampered with. If the trap verification succeeds, the job status is updated to 'executed' and the trap is disclosed by the *Verifier*. The *Sampler* account receives the reward, while the *Verifier* receives a percentage of this reward.
If the trap verification fails, the job returns in 'waiting' state (and the *Verifier* receives the security deposit of the *Sampler*).

5. **Client Receives Result**: Once the job is marked as 'executed', the *Client* can retrieve the final result from the smart contract.


# Support DQPU

::::{grid} 1 1 2 2

:::{grid-item}

<h3>Contributions</h3>

Contributions and issue reports are very welcome at
[the GitHub repository](https://github.com/dakk/dqpu).
:::

:::{grid-item}

<h3>Citation</h3>

```
  @software{dqpu2024,
      author = {Davide Gessa},
      title = {dqpu: A Web3-Powered, Decentralized Quantum Simulator with Verifiable Computation },
      url = {https://github.com/dakk/dqpu},
      year = {2024},
  }
```

:::

:::{toctree}
:maxdepth: 1
:hidden:

Getting Started<docs/qiskit_example.ipynb>
Documentation<docs/index>
Node operator<nodes/index>
API<api/index>
App UI<https://dqpu.io/app>
:::
