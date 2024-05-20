from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram

from dqpu.backends.qiskit import DQPUBackend

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)

backend = DQPUBackend()
backend.load_account("dqpu_alice.testnet")

circ = transpile(qc, backend)
job = backend.run(circ, shots=1024)

counts = job.result().get_counts(circ)
plot_histogram(counts)


from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)

backend = AerSimulator()

circ = transpile(qc, backend)
job = backend.run(circ, shots=1024)

counts = job.result().get_counts(circ)
plot_histogram(counts)
