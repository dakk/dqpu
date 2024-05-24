---
html_theme.sidebar_secondary.remove:
sd_hide_title: true
---

<!-- CSS overrides on the homepage only -->
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



<!-- Keep in markdown to generate headerlink -->
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
