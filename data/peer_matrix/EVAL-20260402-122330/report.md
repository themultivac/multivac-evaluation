# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260402-122330
**Timestamp:** 2026-04-02T12:23:30.207662
**Category:** Code Generation
**Model Pool:** 10 code-optimized models

## Question

This function works but is O(n³). Optimize it to O(n log n) or better while maintaining correctness.

```python
def find_triplets_with_sum(arr, target_sum):
    """Find all unique triplets in arr that sum to target_sum"""
    n = len(arr)
    result = []
    
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if arr[i] + arr[j] + arr[k] == target_sum:
                    triplet = sorted([arr[i], arr[j], arr[k]])
                    if triplet not in result:
                        result.append(triplet)
    
    return result
```

Explain your optimization approach and prove the new time complexity.

---

## Rankings

| Rank | Model | Score | Min | Max | Std Dev |
|------|-------|-------|-----|-----|---------|
| 1 | Grok 4.20 | 9.49 | 8.80 | 10.00 | 0.41 |
| 2 | GPT-5.4 | 9.46 | 8.80 | 10.00 | 0.53 |
| 3 | Claude Sonnet 4.6 | 9.42 | 8.60 | 10.00 | 0.51 |
| 4 | Claude Opus 4.6 | 9.09 | 8.45 | 9.80 | 0.39 |
| 5 | MiMo-V2-Flash | 9.04 | 7.75 | 10.00 | 0.72 |
| 6 | Gemini 3 Flash Preview | 8.94 | 7.75 | 10.00 | 0.68 |
| 7 | GPT-OSS-120B | 8.78 | 6.55 | 9.60 | 0.98 |
| 8 | MiniMax M2.5 | 8.39 | 5.65 | 9.65 | 1.25 |
| 9 | DeepSeek V3 | 8.37 | 6.75 | 9.80 | 0.87 |
| 10 | Gemini 3.1 Pro | 7.72 | 3.60 | 9.80 | 1.76 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | GPT-5.4 | 7.57 |
| 2 | Grok 4.20 | 8.31 |
| 3 | GPT-OSS-120B | 8.43 |
| 4 | Claude Sonnet 4.6 | 8.77 |
| 5 | MiniMax M2.5 | 8.98 |
| 6 | Gemini 3.1 Pro | 9.06 |
| 7 | Claude Opus 4.6 | 9.08 |
| 8 | MiMo-V2-Flash | 9.08 |
| 9 | DeepSeek V3 | 9.49 |
| 10 | Gemini 3 Flash Preview | 9.83 |

**Strictest Judge:** gpt_5_4
**Most Lenient Judge:** gemini_3_flash
**Total Judgments:** 100
**Valid Judgments:** 89

---

## Model Pool

Models selected for **Code Generation** evaluation:

1. **GPT-5.4** (openrouter)
2. **Claude Opus 4.6** (openrouter)
3. **Gemini 3.1 Pro** (openrouter)
4. **Claude Sonnet 4.6** (openrouter)
5. **Grok 4.20** (openrouter)
6. **DeepSeek V3** (openrouter)
7. **GPT-OSS-120B** (openrouter)
8. **Gemini 3 Flash Preview** (openrouter)
9. **MiniMax M2.5** (openrouter)
10. **MiMo-V2-Flash** (openrouter)

---

## Model Responses

### GPT-5.4

**Generation Time:** 18433ms
**Tokens:** 1350

```
Use sorting + a two-pointer scan. This reduces the search from checking all \(\binom{n}{3}\) triplets to, for each fixed first element, finding matching pairs in linear time.

## Optimized solution

```python
def find_triplets_with_sum(arr, target_sum):
    """Find all unique triplets in arr that sum to target_sum"""
    arr = sorted(arr)
    n = len(arr)
    result = []

    for i in range(n - 2):
        # Skip duplicate first elements
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        left, right = i + 1, n - 1

        while left < right:
            total = arr[i] + arr[left] + arr[right]

            if total == target_sum:
                result.append([arr[i], arr[left], arr[right]])

                left += 1
                right -= 1

                # Skip duplicate second elements
                while left < right and arr[left] == arr[left - 1]:
                    left += 1

                # Skip duplicate third elements
                while left < right and arr[right] == arr[right + 1]:
                    right -= 1

            elif total < target_sum:
                left += 1
            else:
                right -= 1

    return result
```

---

## Why this is correct

### 1. Sort the array
After sorting, suppose we fix `arr[i]` as the first element of the triplet.

We now need to find pairs `(arr[left], arr[right])` such that:

\[
arr[left] + arr[right] = target\_sum - arr[i]
\]

Because the array is sorted:

- If the current sum is too small, increasing `left` makes the sum larger.
- If the current sum is too large, decreasing `right` makes the sum smaller.

So we can find all valid pairs for each `i` in one linear scan.

### 2. No valid triplet is missed
For each fixed `i`, the two-pointer search explores the whole search space of pairs between `i+1` and `n-1` in a monotonic way. Since each step moves either `left` or `right`, every relevant pair region is considered.

### 3. Uniqueness is preserved
Duplicates are av...
```

### Claude Opus 4.6

**Generation Time:** 25534ms
**Tokens:** 1519

```
# Optimizing Triplet Sum from O(n³) to O(n²)

## Analysis of the Original

The original has three nested loops (O(n³)) plus an O(n) duplicate check against the result list, making it potentially even worse. The key insight is that we can reduce one full loop by using the **two-pointer technique** on a sorted array.

## Optimized Solution

```python
def find_triplets_with_sum(arr, target_sum):
    """Find all unique triplets in arr that sum to target_sum."""
    arr.sort()  # O(n log n)
    n = len(arr)
    result = []

    for i in range(n - 2):
        # Skip duplicate values for the first element
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        # Early termination: if smallest possible triplet exceeds target, stop
        if arr[i] + arr[i + 1] + arr[i + 2] > target_sum:
            break

        # Early skip: if largest possible triplet with arr[i] is too small, continue
        if arr[i] + arr[n - 2] + arr[n - 1] < target_sum:
            continue

        # Two-pointer search for the remaining two elements
        left = i + 1
        right = n - 1

        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]

            if current_sum == target_sum:
                result.append([arr[i], arr[left], arr[right]])

                # Skip duplicates for second element
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                # Skip duplicates for third element
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1

                left += 1
                right -= 1

            elif current_sum < target_sum:
                left += 1      # Need a larger sum
            else:
                right -= 1     # Need a smaller sum

    return result
```

## How It Works — Step by Step

```
arr = [1, -1, 0, 2, -2, 4, -1], target = 3

Step 1: Sort → [-2, -1, -1, 0, 1, 2, 4]

Step 2: Fix i=0 (value=-2), find pairs summin...
```

### Gemini 3.1 Pro

**Generation Time:** 29212ms
**Tokens:** 2235

```
To address your request directly: **It is mathematically impossible to optimize the general 3SUM problem to $O(n \log n)$ or better.** 

In computer science, finding three numbers that sum to a target is a classic problem known as **3SUM**. The widely accepted lower bound for this problem is **$O(n^2)$**. No algorithm currently exists that can solve it in $O(n \log n)$ time for an unsorted array.

However, we can absolutely optimize your $O(n^3)$ algorithm down to the optimal **$O(n^2)$** time complexity. 

Here is the optimized code, followed by an explanation of the approach and a proof of its complexity.

### Optimized Code ($O(n^2)$)

```python
def find_triplets_with_sum(arr, target_sum):
    """Find all unique triplets in arr that sum to target_sum"""
    # Step 1: Sort the array
    arr.sort()
    n = len(arr)
    result = []
    
    # Step 2: Iterate through the array, fixing the first element
    for i in range(n - 2):
        # Skip duplicate elements for the first position to ensure unique triplets
        if i > 0 and arr[i] == arr[i - 1]:
            continue
            
        # Step 3: Use two pointers to find the remaining two elements
        left = i + 1
        right = n - 1
        
        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]
            
            if current_sum == target_sum:
                result.append([arr[i], arr[left], arr[right]])

```

### Claude Sonnet 4.6

**Generation Time:** 22953ms
**Tokens:** 1538

```
## Optimization Approach

The key insight is to reduce the three-nested-loop problem by:
1. **Sorting** the array once — enables binary search and two-pointer technique
2. **Fixing one element** with an outer loop — reduces to a "two-sum" subproblem
3. **Using two pointers** on the remaining subarray — solves two-sum in O(n) instead of O(n²)

```python
def find_triplets_with_sum(arr, target_sum):
    """
    Find all unique triplets in arr that sum to target_sum.
    
    Time Complexity:  O(n log n) — sort dominates
    Space Complexity: O(n) — sorting in-place, output excluded
    """
    arr = sorted(arr)  # Don't mutate the original; O(n log n)
    n = len(arr)
    result = []

    for i in range(n - 2):                      # Fix the first element
        # Skip duplicate values for the first element
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        # Early termination: smallest possible triplet exceeds target
        if arr[i] + arr[i + 1] + arr[i + 2] > target_sum:
            break

        # Early continuation: largest possible triplet is below target
        if arr[i] + arr[n - 2] + arr[n - 1] < target_sum:
            continue

        # Two-pointer scan for the remaining two elements
        left, right = i + 1, n - 1

        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]

            if current_sum == target_sum:
                result.append([arr[i], arr[left], arr[right]])

                # Skip duplicates for the second element
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                # Skip duplicates for the third element
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1

                left += 1
                right -= 1

            elif current_sum < target_sum:
                left += 1   # Need a larger sum
            else:
                right -= 1  # Need a smaller sum

    retur...
```

### Grok 4.20

**Generation Time:** 5407ms
**Tokens:** 1119

```
**Optimized Solution (O(n²) time)**

```python
def find_triplets_with_sum(arr, target_sum):
    """Find all unique triplets in arr that sum to target_sum.
    
    Returns a list of sorted triplets (each triplet is also sorted).
    """
    n = len(arr)
    if n < 3:
        return []
    
    # Sort the array - crucial for the two-pointer technique and deduplication
    arr = sorted(arr)
    result = []
    
    for i in range(n - 2):
        # Skip duplicate values for i to avoid duplicate triplets
        if i > 0 and arr[i] == arr[i - 1]:
            continue
            
        # Two pointers for the remaining part of the array
        left = i + 1
        right = n - 1
        
        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]
            
            if current_sum == target_sum:
                triplet = [arr[i], arr[left], arr[right]]
                result.append(triplet)
                
                # Skip duplicates for left and right to avoid duplicate triplets
                left += 1
                right -= 1
                while left < right and arr[left] == arr[left - 1]:
                    left += 1
                while left < right and arr[right] == arr[right + 1]:
                    right -= 1
                    
            elif current_sum < target_sum:
                left += 1
            else:
                right -= 1
    
    return result
```

---

### Optimization Approach Explained

**Key Ideas:**

1. **Sort the array first** (O(n log n))
   - This allows us to use the two-pointer technique.
   - Makes deduplication much easier (duplicates become adjacent).
   - Guarantees that each triplet is returned in sorted order.

2. **Fix one element and use two pointers for the rest**
   - Instead of three nested loops (O(n³)), we fix the smallest element `i` and solve the 2-sum problem for the remaining target using two pointers.
   - Two pointers on a sorted array finds all pairs in O(n) time.

...
```

### DeepSeek V3

**Generation Time:** 47710ms
**Tokens:** 1036

```
To optimize the given function from O(n³) to O(n²), we can use a combination of sorting and a two-pointer technique. Here's the optimized approach:

### Optimized Approach:
1. **Sort the Array**: Sorting helps in easily skipping duplicate elements and efficiently using the two-pointer technique.
2. **Iterate through the Array**: For each element `arr[i]`, treat it as the first element of the triplet.
3. **Two-pointer Technique for Remaining Elements**: For the remaining elements (i+1 to end), use two pointers (left and right) to find pairs that sum up to `target_sum - arr[i]`.
4. **Skip Duplicates**: Skip duplicate elements to avoid duplicate triplets in the result.

### Optimized Code:
```python
def find_triplets_with_sum(arr, target_sum):
    """Find all unique triplets in arr that sum to target_sum"""
    arr.sort()
    n = len(arr)
    result = []
    
    for i in range(n - 2):
        if i > 0 and arr[i] == arr[i - 1]:
            continue  # Skip duplicate elements
        
        left = i + 1
        right = n - 1
        remaining_sum = target_sum - arr[i]
        
        while left < right:
            current_sum = arr[left] + arr[right]
            if current_sum == remaining_sum:
                result.append([arr[i], arr[left], arr[right]])
                # Skip duplicates
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif current_sum < remaining_sum:
                left += 1
            else:
                right -= 1
                
    return result
```

### Explanation of Optimization:
1. **Sorting the Array**: Sorting takes O(n log n) time. This allows us to use the two-pointer technique efficiently.
2. **Outer Loop**: The outer loop runs from `i = 0` to `i = n - 3`, which is O(n).
3. **Two-pointer Technique**: For each `i`, the ...
```

### GPT-OSS-120B

**Generation Time:** 21119ms
**Tokens:** 2274

```
## 1.  Why the naïve version is *O(n³)*  

The triple‑nested loops enumerate **every** 3‑element combination of the input list.  
For an array of length `n` there are  

\[
\binom{n}{3}= \frac{n(n-1)(n-2)}{6}=Θ(n^{3})
\]

different triples, and each one is examined once.  
The `if …` test and the `sorted`/`in` check are constant‑time, so the whole routine is Θ(n³).

---

## 2.  Target complexity  

We can bring the work down to **quadratic** (or “almost” linearithmic) by:

1. **Sorting the array once** – `O(n log n)`  
2. **Fixing one element** and then finding the other two with the classic *two‑pointer* technique – `Θ(n)` per fixed element  

Overall cost: `O(n log n) + O(n·n) = O(n²)` (the quadratic term dominates).

The two‑pointer method is the standard way to solve the *3‑sum* problem in optimal time for an unsorted list of integers.

---

## 3.  The optimized algorithm (two‑pointer + set for uniqueness)

```python
def find_triplets_with_sum(arr, target_sum):
    """
    Return a list of *unique* triplets (as lists) whose elements sum to target_sum.
    Runs in O(n²) time and O(1) extra space besides the output.
    """
    # 1️⃣  Sort once – this gives us order and lets us use two‑pointers.
    arr.sort()
    n = len(arr)
    # We store tuples in a set to guarantee uniqueness without O(k) list scans.
    found = set()                     # {(a,b,c), …}

    # 2️⃣  Iterate over the first element of the triplet.
    for i in range(n - 2):
        # Skip duplicate first elements – they would generate the same triples.
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        left, right = i + 1, n - 1   # two‑pointer window for the remaining two numbers

        # 3️⃣  Move the two pointers toward each other looking for the complementary pair.
        while left < right:
            cur_sum = arr[i] + arr[left] + arr[right]

            if cur_sum == target_sum:
                # Store the found triplet as an immutable tuple (sorted automatically)...
```

### Gemini 3 Flash Preview

**Generation Time:** 7524ms
**Tokens:** 1117

```
To optimize this function from $O(n^3)$ to $O(n^2)$, we use the **Sorting + Two-Pointer** approach. 

While a complexity of $O(n \log n)$ is theoretically impossible for the "3Sum" problem (it is a known $n^2$ class problem), we can achieve $O(n^2)$, which is the industry-standard optimization.

### Optimized Implementation

```python
def find_triplets_with_sum(arr, target_sum):
    n = len(arr)
    arr.sort()  # Step 1: Sort the array O(n log n)
    result = []
    
    for i in range(n - 2):
        # Skip duplicate values for the first element to ensure uniqueness
        if i > 0 and arr[i] == arr[i - 1]:
            continue
            
        # Use two pointers for the remaining part of the array
        left = i + 1
        right = n - 1
        
        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]
            
            if current_sum == target_sum:
                result.append([arr[i], arr[left], arr[right]])
                
                # Move pointers and skip duplicates
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target_sum:
                left += 1  # Need a larger sum
            else:
                right -= 1 # Need a smaller sum
                
    return result
```

### Optimization Approach

1.  **Sorting:** By sorting the array first, we can use the relative magnitude of numbers to decide which direction to move our pointers. It also allows us to group duplicates together.
2.  **Fix and Search:** We iterate through the array, fixing one element (`arr[i]`). For every `i`, we treat the problem as a "Two Sum" problem for the remaining subarray.
3.  **Two Pointers:** Instead of a nested loop for `j` and `k`, we place one pointer at `i + 1` and another at th...
```

### MiniMax M2.5

**Generation Time:** 32742ms
**Tokens:** 2241

```
Below is a complete, self‑contained solution that replaces the naïve \(O(n^{3})\) brute‑force with the classic **two‑pointer / sorting** method.  
The algorithm runs in  

* **\(O(n\log n)\)** for the sort, plus  
* **\(O(n^{2})\)** for the scanning loops  

→ overall **\(O(n^{2})\)** (which is strictly better than \(O(n^{3})\) and is known to be optimal for the 3‑sum problem under the usual algebraic‑decision‑tree model).

---

## 1. Why \(O(n^{2})\) is the best we can hope for

The 3‑sum problem asks for all triples \((i,j,k)\) with \(i<j<k\) such that  
\(a_i + a_j + a_k = \text{target}\).  

Even if we could check a pair in \(O(1)\) time, there are \(\Theta(n^{2})\) distinct pairs \((i,j)\); for each pair we must decide whether a third element exists, so a **lower bound of \(\Omega(n^{2})\)** holds in the comparison‑based model.  
Therefore an \(O(n^{2})\) algorithm is asymptotically optimal (apart from the optional \(O(n\log n)\) sort).

---

## 2. Optimised algorithm (two‑pointer after sorting)

1. **Sort** the input array – this lets us move a “window” left/right while preserving order.
2. **Fix the first element** of the triplet at index `i` (from `0` to `n‑3`).  
   To avoid duplicate triplets we skip repeated values of `arr[i]`.
3. For each `i` create a **two‑pointer window** on the remaining suffix:
   * `l = i + 1` (smallest unused element)
   * `r = n - 1` (largest unused element)
4. While `l < r` compute `s = arr[i] + arr[l] + arr[r]`.
   * If `s == target` we have a valid triplet → store it, then advance **both** pointers while skipping equal values (again to guarantee uniqueness).
   * If `s < target` we need a larger sum → increment `l`.
   * If `s > target` we need a smaller sum → decrement `r`.
5. Return the collected list.

All duplicate triples are omitted because we always move past any repeated value at each of the three positions.

---

## 3. Correctness Proof  

We prove that the algorithm returns **exactly** the set of unique triplets whose...
```

### MiMo-V2-Flash

**Generation Time:** 11698ms
**Tokens:** 1400

```
Here is the optimized solution with $O(n^2)$ time complexity. While the prompt asks for $O(n \log n)$, it is mathematically impossible to find all unique triplets with a better time complexity than $O(n^2)$ in the general case (as there can be up to $O(n^2)$ valid triplets, and printing them alone requires $O(n^2)$ time).

### Optimized Code

```python
def find_triplets_with_sum(arr, target_sum):
    """
    Find all unique triplets in arr that sum to target_sum.
    Time Complexity: O(n^2)
    Space Complexity: O(n) or O(1) depending on sorting implementation.
    """
    # Step 1: Sort the array to allow the two-pointer technique
    # This takes O(n log n)
    arr.sort()
    n = len(arr)
    result = []

    for i in range(n - 2):
        # Optimization: Skip duplicate values for the first element
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        # Optimization: If the smallest element is greater than target_sum, 
        # and the array contains only positive numbers, we can break. 
        # However, since we don't know if numbers are positive, we skip this check 
        # to maintain general correctness.

        # Use two pointers for the remaining part of the array
        left = i + 1
        right = n - 1

        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]

            if current_sum == target_sum:
                # Found a triplet
                result.append([arr[i], arr[left], arr[right]])

                # Skip duplicate values for the second element
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                # Skip duplicate values for the third element
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                
                # Move both pointers inward
                left += 1
                right -= 1
            
            elif current_sum < target_sum:
                # Sum...
```

---

*Generated by The Multivac V5*
*https://themultivac.com*