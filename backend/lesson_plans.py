LESSON_PLANS = {
                "arrays": """
Arrays rely on efficient scanning, prefix computation, and index manipulation.

**Core Concepts**
- Prefix and suffix arrays
- Two-pass scans and amortized O(n) reasoning
- Trade-offs of in-place updates vs auxiliary space

**Recommended Problems**
- 53 Maximum Subarray
- 238 Product of Array Except Self
- 121 Best Time to Buy and Sell Stock

**What to Practice Next**
- Explain how iteration patterns eliminate nested loops.
- Show how prefix or suffix logic reduces repeated computation.
""",
                "hashmap": """
Hash-based solutions optimize constant-time lookups and avoid redundant scans.

**Core Concepts**
- Key/value design and frequency counting
- Avoiding O(n²) double loops using sets and maps
- Understanding collisions conceptually

**Recommended Problems**
- 1 Two Sum
- 49 Group Anagrams
- 560 Subarray Sum Equals K

**What to Practice Next**
- Practice stating how you reduce a brute-force approach to O(n) by storing decisions already made.
""",
                "two_pointers": """
Two pointers solve problems on sorted or directionally constrained data.

**Core Concepts**
- Shrinking ranges by moving boundary pointers
- Leveraging sorted structure to avoid rescans
- Identifying when movement is optimal

**Recommended Problems**
- 11 Container With Most Water
- 15 3Sum
- 167 Two Sum II

**What to Practice Next**
- Describe pointer movement decisions clearly.
- Justify why each pointer move is safe and optimal.
""",
                "sliding_window": """
Sliding windows track a moving subset of elements under a constraint.

**Core Concepts**
- Left/right boundary management
- Maintaining validity while expanding and contracting
- Understanding O(n) amortized work

**Recommended Problems**
- 3 Longest Substring Without Repeating Characters
- 76 Minimum Window Substring
- 209 Minimum Size Subarray Sum

**What to Practice Next**
- Explain how you maintain window state and when you shrink to restore constraints.
""",
                "binary_search": """
Binary search works when answers or states follow a monotonic pattern.

**Core Concepts**
- Midpoint choice and boundary updates
- Checking invariant correctness
- Using search on answers, not only arrays

**Recommended Problems**
- 704 Binary Search
- 33 Search in Rotated Sorted Array
- 875 Koko Eating Bananas

**What to Practice Next**
- Avoid vague terms like "cut in half"; explain exact boundary logic.
- Emphasize termination conditions and off-by-one safety.
""",
                "linked_list": """
Linked lists amplify pointer reasoning and structural manipulation.

**Core Concepts**
- Maintaining prev, curr, next references
- Dummy node usage to simplify edges
- Tortoise-and-hare cycle detection

**Recommended Problems**
- 206 Reverse Linked List
- 141 Linked List Cycle
- 19 Remove Nth Node From End

**What to Practice Next**
- Say your pointers out loud; practice describing how they move and why.
""",
                "tree": """
Trees demand recursive reasoning and traversal clarity.

**Core Concepts**
- DFS orderings (pre/in/post)
- Levels and BFS when breadth matters
- Height and balance implications

**Recommended Problems**
- 104 Maximum Depth of Binary Tree
- 226 Invert Binary Tree
- 230 Kth Smallest Element in BST

**What to Practice Next**
- Describe the recursive frame: what you pass down, what you compute, and what you return.
""",
                "graph": """
Graph problems combine traversal discipline with state tracking.

**Core Concepts**
- Adjacency list modeling
- Visited sets to prevent cycles
- Topological ordering when direction matters

**Recommended Problems**
- 200 Number of Islands
- 133 Clone Graph
- 207 Course Schedule

**What to Practice Next**
- Be explicit about visited states and direction; ambiguity loses points fast.
""",
                "heap": """
Heaps optimize ordered retrieval without full sorting.

**Core Concepts**
- Partial ordering and priority queues
- O(log n) push/pop mechanics
- Using heaps on fixed-size windows

**Recommended Problems**
- 215 Kth Largest Element in an Array
- 347 Top K Frequent Elements
- 295 Find Median From Data Stream

**What to Practice Next**
- Practice explaining when heap usage beats sorting and what "partial order" buys you.
""",
                "dp": """
Dynamic programming turns exponential recursion into linear or near-linear progression.

**Core Concepts**
- State definition: what dp[i] represents
- Transitions based on previous states
- Memoization vs tabulation tradeoffs

**Recommended Problems**
- 70 Climbing Stairs
- 198 House Robber
- 300 Longest Increasing Subsequence

**What to Practice Next**
- Always state the recurrence before presenting the solution; that alone boosts clarity scores.
- Briefly compare your DP approach to the brute-force recursive version and explain what work you are saving.
""",
                "backtracking": """
Backtracking explores choices, recurses, and undoes invalid paths.

**Core Concepts**
- Base case specification
- State variables carried through recursion
- Exponential branching and pruning

**Recommended Problems**
- 46 Permutations
- 39 Combination Sum
- 51 N-Queens

**What to Practice Next**
- Explain what each parameter tracks, how you revert choices, and why runtime is exponential.
"""
}