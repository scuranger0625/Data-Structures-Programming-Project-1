#include <stdio.h>
#include <math.h>

double beta = 0;

//############################
//         Function
//############################

// Entangling function to initialize links
double Entangling(double length) {
    return 0.5 + 0.5 * exp(-beta * length);
}

// Purification function to calculate fidelity after purification
double PurificationFidelity(double Fidelity1, double Fidelity2) {
     return (Fidelity1 * Fidelity2) / (Fidelity1 * Fidelity2 + (1 - Fidelity1) * (1 - Fidelity2));
}

// Swapping function to calculate fidelity after entanglement swapping
double SwappingFidelity(double Fidelity1, double Fidelity2) {
    return Fidelity1 * Fidelity2;
}

int main() {
    // Variable declarations
    int nodeNum;
    double alpha, swapProb;

    // Load input variables
    scanf("%d %lf %lf %lf", &nodeNum, &alpha, &beta, &swapProb);

    // Arrays to hold data for each link and node
    double length[1000];
    int quantumMemories[100];
    long double linkFidelity[1000], linkProb[1000];
    int linkNum[1000];

    // Load quantum memory data for each node
    for (int i = 0; i < nodeNum; i++) {
        int nodeID;
        scanf("%d %d", &nodeID, &quantumMemories[i]);
    }

    // Load link distances
    for (int i = 0; i < nodeNum - 1; i++) {
        int linkID;
        scanf("%d %lf", &linkID, &length[i]);
    }

    // Initialize one entangled link between each pair of adjacent nodes
    for (int i = 0; i < nodeNum - 1; i++) {
        linkNum[i] = 1;  // Initialize with 1 entangled connection
        linkFidelity[i] = Entangling(length[i]); // calculate each linkFidelity
        linkProb[i] = swapProb;  // Initialize success probability with swapProb
        quantumMemories[i]--;
        quantumMemories[i + 1]--;
    }

    // Greedy strategy to improve fidelity with memory constraints
    while (1) {
        // Track the best link to upgrade fidelity
        int bestLinkID = -1;
        double maxFidelityGain = 0;

        // Find the link that gives the highest fidelity gain when purified
        for (int i = 0; i < nodeNum - 1; i++) {
            int node1 = i;
            int node2 = i + 1;

            // Check if both nodes connected to the link have enough available memory
            if (quantumMemories[node1] > 0 && quantumMemories[node2] > 0) {
                double newFidelity = PurificationFidelity(linkFidelity[i], Entangling(length[i]));
                double fidelityGain = newFidelity - linkFidelity[i];

                if (fidelityGain > maxFidelityGain) {
                    maxFidelityGain = fidelityGain;
                    bestLinkID = i;
                }
            }
        }

        if (bestLinkID != -1) {
            // Update the best link by adding one more entangled link for purification
            linkNum[bestLinkID]++;
            linkFidelity[bestLinkID] = PurificationFidelity(linkFidelity[bestLinkID], Entangling(length[bestLinkID]));
            linkProb[bestLinkID] = fmin(linkProb[bestLinkID] * 1.1, 1.0);  // 確保成功率不會超過 1.0
            // Decrement memory after confirming a link is added
            quantumMemories[bestLinkID]--;
            quantumMemories[bestLinkID + 1]--;
            
        } else {
            // Break the loop if no more memory is available to add entangled links
            break;
        }
    }

    // Output the final number of entangled links between nodes
    for (int i = 0; i < nodeNum - 1; i++) {
        printf("%d %d %d\n", i, i + 1, linkNum[i]);
    }

    return 0;
}
