// Test data.
const testNodes = [[1, 2], [35, 63], [4, 3], [47, 423], [10, 10], [17, 17], [100, 100]];

const distance = (nodeOne, nodeTwo) => {
    const oneX = nodeOne[0];
    const oneY = nodeOne[1];
    const twoX = nodeTwo[0];
    const twoY = nodeTwo[1];
    return Math.sqrt((oneX - twoX)**2 + (oneY - twoY)**2);
}

const createMST = nodes => {
    if (nodes.length === 0) {
        console.log("No nodes.");
    } else {
        // Declare edges map.
        const edges = new Map();

        // Initialize array of reached nodes and array of unreached nodes. All nodes start as unreached.
        const reached = [];
        const unreached = [...nodes];

        // Initialize MST with first node.
        reached.push(unreached[0]);
        unreached.splice(0, 1);

        // Create MST.
        while (unreached.length > 0) {
            var min_dist = Infinity;
            var curr_idx;
            var min_idx;

            for (let i = 0; i < reached.length; i++) {
                const nodeOne = reached[i];
                for (let j = 0; j < unreached.length; j++) {
                    const nodeTwo = unreached[j];
                    const dist = distance(nodeOne, nodeTwo);

                    if (dist < min_dist) {
                        min_dist = dist;
                        curr_idx = i;
                        min_idx = j;
                    }
                }
            }

            edges.set(reached[curr_idx], unreached[min_idx]);

            reached.push(unreached[min_idx]);
            unreached.splice(min_idx, 1);
        }

        console.log(edges);
        return edges;
    }
}

createMST(testNodes);
