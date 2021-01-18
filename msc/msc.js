// Test data.
const testNodes = [[1, 2], [35, 63], [4, 3], [47, 423], [10, 10], [17, 17], [100, 100]];

// Maybe have a slider to adjust the radius?
const RADIUS = 100;

const distance = (nodeOne, nodeTwo) => {
    const oneX = nodeOne[0];
    const oneY = nodeOne[1];
    const twoX = nodeTwo[0];
    const twoY = nodeTwo[1];
    return Math.sqrt((oneX - twoX)**2 + (oneY - twoY)**2);
}

const createMSC = nodes => {
    if (nodes.length === 0) {
        console.log("No nodes.");
    } else {
        // Declare clusters map.
        var clusters = new Map(); // key: value => clusterCenter: [nodes belong to said cluster]

        // Initialize every node to be a cluster centroid containing itself.
        for (let node of nodes) {
            clusters.set(node, node);
        }

        var centroidChanged = true;

        // Keep shifting the centroids until none of the centroids shift any longer.
        while (centroidChanged) {
            centroidChanged = false;

            const newClusters = new Map();

            // For each cluster centroid, average all nodes within RADIUS. This is the new centroid center.
            for (let centroid of clusters.keys()) {
                var sumX = 0;
                var sumY = 0;
                var count = 0;
                const nodesInCluster = [];

                // Calculate the distnace from the centroid to every node.
                for (let node of nodes) {
                    const dist = distance(centroid, node);
                    // If the node is within RADIUS of the centroid, add it to the averaging of the new centroid.
                    if (dist <= RADIUS) {
                        sumX += node[0];
                        sumY += node[1];
                        count++;
                        nodesInCluster.push(node);
                    }
                }
                const avgX = sumX / count;
                const avgY = sumY / count;
                const newCentroid = [avgX, avgY];

                // If at least one centroid has shifted, then change the flag so that the algo will run again.
                if (centroid[0] !== newCentroid[0] || centroid[1] !== newCentroid[1]) {
                    centroidChanged = true;
                }

                newClusters.set(newCentroid, nodesInCluster);

                console.log(newCentroid);
            }

            clusters = newClusters;
        }

        console.log(clusters);
        return clusters;
    }
}

createMSC(testNodes);
