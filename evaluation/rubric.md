# InterPrep Explanation Evaluation Rubric

## Summary

This rubric provides a structured framework for evaluating user explanations during technical interview practice sessions. The system assesses three parts: **Problem Identification**, **Complexity Analysis**, and **Clarity of Explanation**. It generates scores and actionable feedback to help users improve their interview performance.

---

## 1. Scoring Overview

### 1.1 Total Score Calculation

- **Total Score:** 100 points  
  - **Problem Identification:** 35 points  
  - **Complexity Analysis:** 35 points  
  - **Clarity:** 30 points  

### 1.2 Performance Levels

- **Excellent:** 90–100 points  
- **Good:** 75–89 points  
- **Satisfactory:** 60–74 points  
- **Needs Improvement:** 40–59 points  
- **Poor:** Below 40 points  

---

## 2. Problem Identification (35 points)

### 2.1 Pattern Recognition (15 points)

**Scoring Criteria**

- **15 points:** Correctly identifies the primary algorithmic pattern and explains why  
- **12 points:** Identifies the pattern correctly with minor explanation gaps  
- **8 points:** Identifies a related but not optimal pattern  
- **4 points:** Vague pattern identification  
- **0 points:** No pattern identified or completely incorrect  

**Key Indicators to Detect**

- Mentions of algorithm names (DFS, BFS, DP, Binary Search, etc.)
- Problem type keywords (“traversal”, “optimization”, “search”, “subproblems”)
- Pattern justification phrases (“This is a graph problem because...”)

**Example Feedback Templates**

- **Excellent:**  
  > “Great job identifying this as a dynamic programming problem and explaining the overlapping subproblems!”
- **Needs Work:**  
  > “Consider what data structure would best represent this problem. Is there a pattern in how subproblems relate?”

---

### 2.2 Problem Understanding (10 points)

**Scoring Criteria**

- **10 points:** Restates problem correctly, identifies all constraints and goals  
- **8 points:** Good understanding with one minor element missed  
- **5 points:** Basic understanding but missing key constraints  
- **2 points:** Misunderstands significant aspects  
- **0 points:** No demonstration of understanding  

**Key Indicators**

- Input/output clarification  
- Constraint mentions (size limits, value ranges)  
- Edge case awareness  
- Goal statement (“We need to find…”, “The objective is…”)  

---

### 2.3 Approach Selection (10 points)

**Scoring Criteria**

- **10 points:** Proposes optimal approach with justification  
- **8 points:** Good approach, minor optimization possible  
- **5 points:** Working but suboptimal approach  
- **2 points:** Approach would work but highly inefficient  
- **0 points:** Approach wouldn’t solve the problem  

**Key Indicators**

- Algorithm choice reasoning  
- Trade-off discussions  
- Alternative approach mentions  
- Optimization considerations  

---

## 3. Complexity Analysis (35 points)

### 3.1 Time Complexity (15 points)

**Scoring Criteria**

- **15 points:** Correct Big-O with clear derivation  
- **12 points:** Correct complexity, minor explanation issues  
- **8 points:** Close but off by a factor (e.g., O(n) vs O(n log n))  
- **4 points:** Attempts analysis but significantly wrong  
- **0 points:** No time complexity mentioned  

**Key Phrases to Detect**

- “O(n)”, “O(log n)”, “O(n²)”, etc.  
- “Linear time”, “Quadratic”, “Logarithmic”  
- “For each element…”, “Nested loops…”  
- “In the worst case…”  

---

### 3.2 Space Complexity (15 points)

**Scoring Criteria**

- **15 points:** Correct space analysis including auxiliary space  
- **12 points:** Correct but doesn’t distinguish input vs auxiliary  
- **8 points:** Partially correct, misses some space usage  
- **4 points:** Attempts but mostly incorrect  
- **0 points:** No space complexity mentioned  

**Key Indicators**

- Stack space for recursion  
- Data structure space (arrays, hashmaps, etc.)  
- “Additional space”, “In-place”, “Auxiliary space”  

---

### 3.3 Best/Average/Worst Case Analysis (5 points)

**Scoring Criteria**

- **5 points:** Discusses different cases when relevant  
- **3 points:** Mentions but doesn’t elaborate  
- **0 points:** No case analysis when needed  

---

## 4. Clarity of Explanation (30 points)

### 4.1 Structure and Flow (10 points)

**Scoring Criteria**

- **10 points:** Logical progression from problem to solution  
- **8 points:** Good structure with minor jumps  
- **5 points:** Somewhat disorganized but followable  
- **2 points:** Very disorganized, hard to follow  
- **0 points:** No discernible structure  

**Evaluation Metrics**

- Presence of introduction/conclusion  
- Step-by-step explanation  
- Transition phrases (“First…”, “Next…”, “Finally…”)  
- Logical ordering of concepts  

---

### 4.2 Technical Communication (10 points)

**Scoring Criteria**

- **10 points:** Uses correct terminology consistently  
- **8 points:** Mostly correct with occasional imprecision  
- **5 points:** Mix of correct and incorrect terms  
- **2 points:** Frequent misuse of technical terms  
- **0 points:** No technical vocabulary used  

**Key Elements**

- Correct data structure names  
- Algorithm terminology  
- Programming concepts (iteration, recursion, etc.)  
- Mathematical terms when applicable  

---

### 4.3 Completeness (10 points)

**Scoring Criteria**

- **10 points:** Covers all essential aspects including edge cases  
- **8 points:** Good coverage, misses 1–2 minor points  
- **5 points:** Covers basics but lacks depth  
- **2 points:** Significant gaps in explanation  
- **0 points:** Incomplete or cuts off mid-explanation  

**Checklist Items**

- Problem restatement  
- Approach explanation  
- Implementation strategy  
- Complexity analysis  
- Edge case handling  
- Testing/validation mention  

---

## 5. Edge Case and Error Handling (Bonus/Penalty System)

### 5.1 Bonus Points (up to +10)

- Identifies non-obvious edge cases: **+3 per case** (max 2)  
- Discusses error handling: **+2**  
- Mentions testing strategy: **+2**  

### 5.2 Penalty Points (up to -10)

- Misses critical edge cases: **-3 per case**  
- Incorrect fundamental assumptions: **-5**  
- Off-by-one errors mentioned but not corrected: **-2**  

### 5.3 Common Edge Cases by Pattern

**Arrays/Strings**

- Empty input  
- Single element  
- All same elements  
- Negative numbers  
- Integer overflow  

**Graphs**

- Disconnected components  
- Cycles  
- Single node  
- No edges  

**Dynamic Programming**

- Base cases  
- Negative values  
- Zero values  
- Maximum constraints  

---

## 6. Feedback Generation Rules

### 6.1 Feedback Priority

1. **Critical Errors** (wrong pattern, incorrect complexity)  
2. **Major Gaps** (missing complexity analysis, no edge cases)  
3. **Improvements** (optimization opportunities, clarity)  
4. **Positive Reinforcement** (what was done well)  

### 6.2 Feedback Structure Template

```text
Score: [XX/100]

Strengths:
- [Positive point 1]
- [Positive point 2]

Areas for Improvement:
- [Critical issue with suggestion]
- [Major gap with resource]

Specific Feedback:
- Problem Identification: [Specific comment]
- Complexity Analysis: [Specific comment]
- Clarity: [Specific comment]

Recommended Focus:
[1–2 specific areas to practice]

---

## 7. Sample Evaluations

### **Example 1: Two Sum Problem**

**User Explanation**

> “So this is basically an array problem where I need to find two numbers that add up to a target. I’ll use a nested loop to check every pair. The time complexity would be O(n²) because of the nested loops, and space is O(1) since I’m not using extra space.”

**Rubric Score**

- **Problem Identification:** 28/35  
  *Correct pattern, good understanding, suboptimal approach*
- **Complexity Analysis:** 30/35  
  *Correct analysis for chosen approach*
- **Clarity:** 25/30  
  *Clear but could mention hash table optimization*
- **Total:** **83/100 (Good)**

**Feedback**

> “Good job identifying this as an array problem and correctly analyzing your nested loop approach! Consider using a hash table to optimize from O(n²) to O(n) time complexity. You explained your current approach clearly, but mentioning why you chose it over alternatives would strengthen your answer.”

---

### **Example 2: Binary Tree Traversal**

**User Explanation**

> “I need to traverse the tree... um... I’ll use recursion. Each node gets visited once so it’s... linear?”

**Rubric Score**

- **Problem Identification:** 15/35  
  *Vague pattern, unclear understanding*
- **Complexity Analysis:** 8/35  
  *Incomplete, missing space analysis*
- **Clarity:** 10/30  
  *Too brief, lacks structure*
- **Total:** **33/100 (Poor)**

**Feedback**

> “You’re on the right track with recursion for tree traversal! Be specific about which traversal type (inorder, preorder, postorder) and why. Your time complexity intuition is correct — O(n) for n nodes — but also discuss O(h) space for the recursion stack where h is tree height. Practice explaining your approach step-by-step.”

---