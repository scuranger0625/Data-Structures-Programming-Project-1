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

# Bypassing function to simulate bypassing a link (here we assume a direct entanglement between far nodes)
def BypassingFidelity(Fidelity1, Fidelity2):
    return min(Fidelity1 + 0.1 * Fidelity1, 1.0)  # A simple model where bypassing increases fidelity by 10%

# Purification then Swapping function
def PurificationThenSwappingFidelity(Fidelity1, Fidelity2):
    purifiedFidelity = PurificationFidelity(Fidelity1, Fidelity2)
    return SwappingFidelity(purifiedFidelity, Fidelity2)

def main():
    # Variable declarations
    nodeNum = int(input("Enter the number of nodes: "))
    alpha, swapProb = map(float, input("Enter alpha and swap probability: ").split())
    
    global beta
    beta = float(input("Enter beta: "))  # Load beta
    
    # Arrays to hold data for each link and node
    length = [0] * 1000
    quantumMemories = [0] * 100
    linkFidelity = [0.0] * 1000
    linkProb = [0.0] * 1000
    linkNum = [0] * 1000

    # Load quantum memory data for each node
    for i in range(nodeNum):
        nodeID, quantumMemories[i] = map(int, input("Enter node ID and quantum memories: ").split())

    # Load link distances
    for i in range(nodeNum - 1):
        linkID, length[i] = map(float, input(f"Enter link ID and length for link {i}: ").split())

    # Initialize one entangled link between each pair of adjacent nodes
    for i in range(nodeNum - 1):
        linkNum[i] = 1  # Initialize with 1 entangled connection
        linkFidelity[i] = Entangling(length[i])  # calculate each linkFidelity
        linkProb[i] = swapProb  # Initialize success probability with swapProb
        quantumMemories[i] -= 1
        quantumMemories[i + 1] -= 1

    # Output initial success probabilities and fidelities
    print("\nInitial state:")
    for i in range(nodeNum - 1):
        print(f"Link {i}-{i+1}: Fidelity = {linkFidelity[i]:.4f}, Success Probability = {linkProb[i]:.4f}")

    # Greedy strategy to improve fidelity with memory constraints
    while True:
        # Track the best link to upgrade fidelity
        bestLinkID = -1
        maxFidelityGain = 0
        bestMethod = ""  # 用來記錄最好的方法是什麼

        # Find the link that gives the highest fidelity gain when using any of the methods
        for i in range(nodeNum - 1):
            node1 = i
            node2 = i + 1

            # Check if both nodes connected to the link have enough available memory
            if quantumMemories[node1] > 0 and quantumMemories[node2] > 0:
                # Purification
                newFidelityPurification = PurificationFidelity(linkFidelity[i], Entangling(length[i]))
                fidelityGainPurification = newFidelityPurification - linkFidelity[i]

                # Swapping
                newFidelitySwapping = SwappingFidelity(linkFidelity[i], Entangling(length[i]))
                fidelityGainSwapping = newFidelitySwapping - linkFidelity[i]

                # Bypassing
                newFidelityBypassing = BypassingFidelity(linkFidelity[i], Entangling(length[i]))
                fidelityGainBypassing = newFidelityBypassing - linkFidelity[i]

                # Purification then Swapping
                newFidelityPTS = PurificationThenSwappingFidelity(linkFidelity[i], Entangling(length[i]))
                fidelityGainPTS = newFidelityPTS - linkFidelity[i]

                # Compare all strategies and choose the one with the highest fidelity gain
                strategies = {
                    "Purification": fidelityGainPurification,
                    "Swapping": fidelityGainSwapping,
                    "Bypassing": fidelityGainBypassing,
                    "Purification then Swapping": fidelityGainPTS
                }

                best_strategy = max(strategies, key=strategies.get)
                fidelityGain = strategies[best_strategy]

                # If this link offers the best gain, record it
                if fidelityGain > maxFidelityGain:
                    maxFidelityGain = fidelityGain
                    bestLinkID = i
                    bestMethod = best_strategy

        if bestLinkID != -1:
            # Update the best link by adding one more entangled link for the best method
            linkNum[bestLinkID] += 1

            if bestMethod == "Purification":
                linkFidelity[bestLinkID] = PurificationFidelity(linkFidelity[bestLinkID], Entangling(length[bestLinkID]))
            elif bestMethod == "Swapping":
                linkFidelity[bestLinkID] = SwappingFidelity(linkFidelity[bestLinkID], Entangling(length[bestLinkID]))
            elif bestMethod == "Bypassing":
                linkFidelity[bestLinkID] = BypassingFidelity(linkFidelity[bestLinkID], Entangling(length[bestLinkID]))
            elif bestMethod == "Purification then Swapping":
                linkFidelity[bestLinkID] = PurificationThenSwappingFidelity(linkFidelity[bestLinkID], Entangling(length[bestLinkID]))

            linkProb[bestLinkID] = min(linkProb[bestLinkID] * 1.1, 1.0)  # 確保成功率不會超過 1.0

            # Decrement memory after confirming a link is added
            quantumMemories[bestLinkID] -= 1
            quantumMemories[bestLinkID + 1] -= 1

            # Output the updated state for this link
            print(f"\nUpdated link {bestLinkID}-{bestLinkID + 1} using {bestMethod}:")
            print(f"Fidelity = {linkFidelity[bestLinkID]:.4f}, Success Probability = {linkProb[bestLinkID]:.4f}")

        else:
            # Break the loop if no more memory is available to add entangled links
            break

    # Output the final number of entangled links and success probabilities between nodes
    print("\nFinal state:")
    for i in range(nodeNum - 1):
        print(f"Link {i}-{i + 1}: Entangled links = {linkNum[i]}, Final Fidelity = {linkFidelity[i]:.4f}, Final Success Probability = {linkProb[i]:.4f}")

if __name__ == "__main__":
    main()
