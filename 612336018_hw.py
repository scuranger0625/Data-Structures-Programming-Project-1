import math

beta = 0

# ############################
#         Function
# ############################

# Entangling function to initialize links
def Entangling(length):
    return 0.5 + 0.5 * math.exp(-beta * length)

# Purification function to calculate fidelity after purification
def PurificationFidelity(Fidelity1, Fidelity2):
    return (Fidelity1 * Fidelity2) / (Fidelity1 * Fidelity2 + (1 - Fidelity1) * (1 - Fidelity2))

# Swapping function to calculate fidelity after entanglement swapping
def SwappingFidelity(Fidelity1, Fidelity2):
    return Fidelity1 * Fidelity2

def main():
    # Variable declarations
    nodeNum = int(input())
    alpha, swapProb = map(float, input().split())
    
    global beta
    beta = float(input())  # Load beta
    
    # Arrays to hold data for each link and node
    length = [0] * 1000
    quantumMemories = [0] * 100
    linkFidelity = [0.0] * 1000
    linkProb = [0.0] * 1000
    linkNum = [0] * 1000

    # Load quantum memory data for each node
    for i in range(nodeNum):
        nodeID, quantumMemories[i] = map(int, input().split())

    # Load link distances
    for i in range(nodeNum - 1):
        linkID, length[i] = map(float, input().split())

    # Initialize one entangled link between each pair of adjacent nodes
    for i in range(nodeNum - 1):
        linkNum[i] = 1  # Initialize with 1 entangled connection
        linkFidelity[i] = Entangling(length[i])  # calculate each linkFidelity
        linkProb[i] = swapProb  # Initialize success probability with swapProb
        quantumMemories[i] -= 1
        quantumMemories[i + 1] -= 1

    # Greedy strategy to improve fidelity with memory constraints
    while True:
        # Track the best link to upgrade fidelity
        bestLinkID = -1
        maxFidelityGain = 0

        # Find the link that gives the highest fidelity gain when purified
        for i in range(nodeNum - 1):
            node1 = i
            node2 = i + 1

            # Check if both nodes connected to the link have enough available memory
            if quantumMemories[node1] > 0 and quantumMemories[node2] > 0:
                newFidelity = PurificationFidelity(linkFidelity[i], Entangling(length[i]))
                fidelityGain = newFidelity - linkFidelity[i]

                if fidelityGain > maxFidelityGain:
                    maxFidelityGain = fidelityGain
                    bestLinkID = i

        if bestLinkID != -1:
            # Update the best link by adding one more entangled link for purification
            linkNum[bestLinkID] += 1
            linkFidelity[bestLinkID] = PurificationFidelity(linkFidelity[bestLinkID], Entangling(length[bestLinkID]))
            linkProb[bestLinkID] = min(linkProb[bestLinkID] * 1.1, 1.0)  # 確保成功率不會超過 1.0
            # Decrement memory after confirming a link is added
            quantumMemories[bestLinkID] -= 1
            quantumMemories[bestLinkID + 1] -= 1

        else:
            # Break the loop if no more memory is available to add entangled links
            break

    # Output the final number of entangled links between nodes
    for i in range(nodeNum - 1):
        print(f"{i} {i + 1} {linkNum[i]}")

if __name__ == "__main__":
    main()
