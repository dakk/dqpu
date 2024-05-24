Node operator
===============

Sampler Node
------------

A sampler node continuously pool the DQPU smart contract waiting for new job. When a new job appear,
the sampler checks if it can perform the sampling with its hardware. 

Every sampler node can implement its own `Sampler` class, adding supports to other simulators or 
to real quantum hardware. DQPU package offer 3 implementation:

- AerSimulator: statevector simulator from qiskit
- DaskSimulator: statevector simulator using Dask distributed computing library
- NumpySimulator: statevector simulator using Numpy

After every sampled job, the node receives the reward.

.. code:: bash

   dqpu-sampler -a sampler_account --max-deposit 0.1 --sampler aersimulator --max-qubits 21

Read more on :ref:`sampler_node`.


Verifier Node
-------------

A verifier node continuously pool the DQPU smart contract waiting for new 'pending-validation' and 'validating-result' jobs. When a new job appear, the verifiers:
- 'pending-validation' job are checked for quantum circuit validity, and trap qubits are inserted
- 'validating-result' job are checked for trap verification

After every validation, the verifier receives a percentage of the job reward.

Verifier are special users initially selected by the smart contract creator; this will change in the future.

.. code:: bash
   
   dqpu-verifier -a verifier_account

Read more on :ref:`verifier_node`.


.. toctree::
   :maxdepth: 2
   :caption: Nodes

   sampler_node
   verifier_node


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`