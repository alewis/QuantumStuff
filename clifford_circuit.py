"""
clifford_circuit.py
My first attempt at using cirq to model quantum stuff.

At each timestep (moment?) we do the following operations upon each
qubit (open boundary conditions are assumed), depending upon the input
parameters [a, b, c, d, e, f] (each a list with one boolean entry per qubit):
  1. If a, set to |0>.
  2. If b, c, d, e, apply CNOT, H, S, T.
  3. If f, measure in the Z basis.

Written in cirq 0.6.1.
"""

import cirq
import random

###############################################################################
# GLOBAL VARIABLES
###############################################################################
NQUBITS = 4   # Length of the chain.
NSTEPS = 1    # Number of timesteps to run.
###############################################################################




def random_params(nqubits):
    """
    Randomly populates lists of params, each one to act as a toggle for
    its eponymous operation.
    """

    reset_state = [random.random() for x in range(nqubits)]
    apply_CNOT = [random.random() for x in range(nqubits)]
    apply_H = [random.random() for x in range(nqubits)]
    apply_S = [random.random() for x in range(nqubits)]
    apply_T = [random.random() for x in range(nqubits)]
    do_measurement = [random.random() for x in range(nqubits)]
    output = [reset_state, apply_CNOT, apply_H, apply_S, apply_T,
              do_measurement]
    return output


def build_circuit(qubits, params):
    """
    Constructs a circuit representing a single timestep of quantum stuff.
    params is a list of 6 lists, each containing nqubits floats in [0, 1).
    These parameterize the circuit, such that each operation is performed
    only if its relevant parameter is >= 0.5.

    In order, we check the parameters, and if they are big enough we:
    -Set each qubit to zero.
    -Apply a CNOT gate between this qubit and its right neighbour.
    -Apply H, then S, then T gates.
    -Measure in the Z basis.

    Returns the constructed circuit.
    """
    circuit = cirq.Circuit()

    circuit.append(cirq.reset(q) for q, p in zip(qubits, params[0])
                   if p >= 0.5)

    for qi, q in enumerate(qubits[:-1]):
        if params[1][qi] >= 0.5:
            circuit.append(cirq.CNOT(q, qubits[qi+1]))

    circuit.append(cirq.H(q) for q, p in zip(qubits, params[2])
                   if p >= 0.5)
    circuit.append(cirq.S(q) for q, p in zip(qubits, params[3])
                   if p >= 0.5)
    circuit.append(cirq.T(q) for q, p in zip(qubits, params[4])
                   if p >= 0.5)
    circuit.append(cirq.measure(q) for q, p in zip(qubits, params[5])
                   if p >= 0.5)

    return circuit


def main(nsteps=NSTEPS, nqubits=NQUBITS):

    simulator = cirq.Simulator()
    qubits = [cirq.LineQubit(x) for x in range(nqubits)]

    for timestep in range(NSTEPS):
        params = random_params(nqubits)
        circuit = build_circuit(qubits, params)

        print("**************************************************************")
        print("t = ", timestep)
        print(circuit)

        result = simulator.simulate(circuit, qubit_order=qubits)
        print(result)


if __name__ == '__main__':
    main()
