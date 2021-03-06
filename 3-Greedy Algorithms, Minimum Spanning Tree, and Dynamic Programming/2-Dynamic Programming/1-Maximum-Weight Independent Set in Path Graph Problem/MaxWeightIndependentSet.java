/**
 * Given a path graph, with each vertex having a non-negative weight, find the
 * maximum-weight independent set (MWIS), where an independent set is a subset
 * of the vertices, so that no two vertices are adjacent.
 *
 * Algorithm: (Dynamic programming)
 * Denote S to be the optimal solution, i.e., the MWIS in the given path graph,
 * and v_n to be the last vertex of the given path graph.
 * Consider whether v_n is in S:
 * 1. v_n is NOT in S:
 *    Let G' = G - v_n
 *    => S is the MWIS in G'.
 *    => S = the MWIS in G'
 * 2. v_n is in S:
 *    => v_n-1 is NOT in S.
 *    Let G'' = G - v_n - v_n-1
 *    => {S - v_n} is the MWIS in G''.
 *    => S = the MWIS in G'' + v_n
 *
 * i.e.,
 * Let S(i) be the optimal solution for the subproblem with the first i vertices
 * in the given path graph, then
 * S(i) = max{S(i - 1), S(i - 2) + v_i}
 */

import java.util.HashSet;
import java.util.Set;

public class MaxWeightIndependentSet {

    /**
     * Subproblem solutions.
     * Since there are only O(n) distinct subproblems, the first time we solve a
     * subproblem, we can cache its solution in a global take for O(1) lookup
     * time later on.
     */
    private int[] subproblems;

    /**
     * Finds the maximum-weight independent set (MWIS) in a path graph with the
     * given weights in an improved bottom-up way.
     * @param weights weights of the path graph
     * @return MWIS in the given path graph
     */
    public Set<Integer> findMWIS(int[] weights) {
        // Check whether the input array is null or empty
        if ((weights == null) || (weights.length == 0)) {
            return new HashSet<>();
        }

        if (weights.length == 1) {
            Set<Integer> mwis = new HashSet<>();
            mwis.add(1);
            return mwis;
        }

        // Initialization
        subproblems = new int[weights.length];
        subproblems[0] = weights[0];
        subproblems[1] = Math.max(weights[0], weights[1]);
        // Bottom-up calculation
        for (int curr = 2; curr < weights.length; ++curr) {
            subproblems[curr] = Math.max(subproblems[curr - 1], subproblems[curr - 2] + weights[curr]);
        }
        return reconstructMWIS(weights);
        // Overall running time complexity: O(n)
    }

    /**
     * Private helper method to reconstruct MWIS according to the optimal
     * solution using backtracking.
     * @param weights weights of the path graph
     * @return MWIS of the given path graph
     */
    private Set<Integer> reconstructMWIS(int[] weights) {
        Set<Integer> mwis = new HashSet<>();
        int curr = subproblems.length - 1;
        while (curr >= 2) {
            if (subproblems[curr - 1] >= (subproblems[curr - 2] + weights[curr])) {
                // Case 1: The current vertex is not included.
                --curr;
            } else {
                // Case 2: The current vertex is included.
                mwis.add(curr);
                // So the previous vertex must not be included.
                curr -= 2;
            }
        }
        if (curr == 1) {
            if (weights[0] >= weights[1]) {
                mwis.add(0);
            } else {
                mwis.add(1);
            }
        } else if (curr == 0) {
            mwis.add(0);
        }
        return mwis;
        // Running time complexity: O(n)
    }

}
