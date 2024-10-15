
# Quantum Network Simulation

## Description:

This program simulates a quantum network of entangled nodes, where each pair of adjacent nodes is connected by an entangled link. The goal is to maximize the fidelity of the entangled links between nodes through a process called **Purification**, while ensuring that the success probability of the links remains valid (strictly less than 1). The program uses a **greedy strategy** to iteratively find and improve the fidelity of the entangled links, taking into account memory constraints of each node.

---

## How It Works:

1. **Initialization:**
   - The program reads input parameters, including the number of nodes, quantum memory capacity of each node, link distances between nodes, and the initial success probability for entanglement swapping.
   - For each adjacent pair of nodes, one entangled link is initialized between them with a calculated fidelity based on the link distance.

2. **Greedy Strategy:**
   - The program iteratively searches for the link that can achieve the highest fidelity improvement through purification.
   - If a link is found, the program will perform purification on that link, which increases its fidelity at the cost of quantum memory for both nodes.
   - The success probability of each link is updated after purification. It is ensured that the success probability remains strictly less than 1 (via `fmin()` function).

3. **Termination:**
   - The program terminates when no further improvements can be made due to memory constraints (i.e., when there is not enough memory left in the connected nodes to perform further purifications).

4. **Output:**
   - The program prints the final number of entangled links between each adjacent pair of nodes after purification.

---

## Input Format:

1. **First Line:**
   - `nodeNum` (integer): Number of nodes in the quantum network.
   - `alpha` (double): Alpha parameter (unused in the current program but can be used for future extensions).
   - `beta` (double): Beta parameter, which affects the entangling function used to calculate initial link fidelity.
   - `swapProb` (double): Initial success probability for entanglement swapping.

2. **Next `nodeNum` Lines:**
   - Each line contains two integers:
     - `nodeID` (integer): The ID of the node.
     - `quantumMemories` (integer): The number of quantum memories available at this node.

3. **Next `nodeNum - 1` Lines:**
   - Each line contains two values:
     - `linkID` (integer): The ID of the link connecting two adjacent nodes.
     - `length` (double): The distance between the two adjacent nodes.

---

## Output Format:

The program outputs the number of entangled links between each adjacent pair of nodes in the format:

```
[node1] [node2] [linkNum]
```

Where:
- `node1` is the ID of the first node.
- `node2` is the ID of the adjacent second node.
- `linkNum` is the total number of entangled links after purification between the two nodes.

---

## Example Input:

```
5 0.1 0.002 0.9
0 10
1 8
2 12
3 9
4 11
0 3.0
1 4.5
2 2.7
3 1.2
```

## Example Output:

```
0 1 2
1 2 3
2 3 1
3 4 1
```

---

## Key Functions:

1. **Entangling(length):**
   - Calculates the initial fidelity of a link based on its distance using the formula:
     ```
     fidelity = 0.5 + 0.5 * e^(-beta * length)
     ```

2. **PurificationFidelity(Fidelity1, Fidelity2):**
   - Calculates the new fidelity after performing purification on two links:
     ```
     newFidelity = (Fidelity1 * Fidelity2) / (Fidelity1 * Fidelity2 + (1 - Fidelity1) * (1 - Fidelity2))
     ```

3. **SwappingFidelity(Fidelity1, Fidelity2):**
   - Calculates the fidelity after entanglement swapping:
     ```
     newFidelity = Fidelity1 * Fidelity2
     ```

---

## Greedy Strategy:

- The program searches for the link that offers the highest fidelity gain and updates it by performing purification, which consumes memory from the connected nodes.
- This process continues until no more improvements can be made due to memory constraints.

---

## Big-O Complexity:

The overall time complexity of this program is **O(m \* n²)**, where:
- `n` is the number of nodes in the network.
- `m` is the number of available quantum memories.

Each iteration of the `while` loop processes every link, and this repeats until the quantum memories of the nodes are exhausted.

---

## Notes for Future Extensions:

1. **Multi-hop Purification:**
   - The current implementation handles purification for adjacent nodes only. The program can be extended to allow purification across non-adjacent nodes.

2. **Enhanced Memory Management:**
   - Future versions may implement more advanced memory management techniques to balance memory usage more efficiently.

3. **Incorporation of Alpha:**
   - The alpha parameter is currently unused but can be incorporated to adjust the entanglement behavior based on the physical properties of the quantum network.

---

## Compilation and Execution:

- To compile:
  ```bash
  gcc quantum_network.c -o quantum_network -lm
  ```

- To run:
  ```bash
  ./quantum_network
  ```

Make sure to provide the input in the required format to avoid any errors.

---

## License:

This program is open-source under the MIT License.

