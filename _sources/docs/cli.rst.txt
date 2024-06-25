Cli tool
========

DQPU offer a cli tool able to interact with the smart contract.


Generic params:
- `-n/--network`: Default: near-testnet
- `-a/--account`: Account name / uri

Commands:

Submit a circuit job 
--------------------

.. code:: bash
   
    $ dqpu-cli -a dqpu_alice.testnet submit --file ~/test.qasm --shots 1024 --reward 0.0001
    JOBID


Submit a random circuit 
-----------------------

.. code:: bash
   
    $ dqpu-cli -a dqpu_alice.testnet submit-random
    JOBID


Submit a job result 
--------------------

.. code:: bash
   
    $ dpqu-cli -a dqpu_bob.testnet submit-result -i 8 -rf ~/test.qasm


Remove a job 
--------------------

.. code:: bash
   
    $ dpqu-cli remove -i JOBID


Get job information 
--------------------

.. code:: bash
    
    $ dpqu-cli info -i JOBID
    Job: JOBID
    Status: WAITING
    Qubits: 4
    Depth: 9
    Circuit uri: ipfs://.../test.qasm


Get job status 
--------------------

.. code:: bash
   
    $ dpqu-cli status -i JOBID
    EXECUTED


Get job result 
--------------------

.. code:: bash
   
    $ dpqu-cli get-result -i JOBID
    { "0010": 1024 }


Set job validity 
--------------------

.. code:: bash
   
    $ dpqu-cli -a dqpu_owner.testnet set-validity -i 9 -v false


Set job result validity 
--------------------

.. code:: bash
   
    $ dpqu-cli -a dqpu_owner.testnet set-result-validity -i 8 -v true -t trap.json

