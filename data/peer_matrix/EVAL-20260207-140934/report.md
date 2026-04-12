# Multivac Evaluation Report

**Evaluation ID:** EVAL-20260207-140934
**Timestamp:** 2026-02-07T14:09:34.986015
**Category:** Programming & Code
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
| 1 | Claude Opus 4.5 | 9.64 | 8.75 | 10.00 | 0.44 |
| 2 | Claude Sonnet 4.5 | 9.50 | 8.80 | 9.80 | 0.35 |
| 3 | DeepSeek V3.2 | 9.49 | 8.80 | 9.80 | 0.44 |
| 4 | Grok 3 (Direct) | 9.49 | 8.80 | 9.80 | 0.36 |
| 5 | Gemini 3 Flash Preview | 9.31 | 8.60 | 9.80 | 0.44 |
| 6 | GPT-5.2-Codex | 9.23 | 8.35 | 9.80 | 0.57 |
| 7 | Grok Code Fast 1 | 9.09 | 7.75 | 9.80 | 0.70 |
| 8 | Gemini 3 Pro Preview | 6.92 | 3.60 | 8.40 | 1.62 |
| 9 | GLM 4.7 | 6.80 | 2.00 | 9.55 | 3.36 |
| 10 | MiniMax M2.1 | 6.28 | 2.00 | 9.80 | 3.96 |

---

## Meta Analysis

### Judge Strictness

| Rank | Judge | Avg Score Given |
|------|-------|-----------------|
| 1 | Grok Code Fast 1 | 7.87 |
| 2 | GPT-5.2-Codex | 7.90 |
| 3 | Grok 3 (Direct) | 8.33 |
| 4 | Claude Sonnet 4.5 | 8.93 |
| 5 | MiniMax M2.1 | 8.95 |
| 6 | Claude Opus 4.5 | 9.17 |
| 7 | DeepSeek V3.2 | 9.34 |
| 8 | Gemini 3 Flash Preview | 9.63 |
| 9 | GLM 4.7 | 9.71 |

**Strictest Judge:** grok_code_fast
**Most Lenient Judge:** glm_4_7
**Total Judgments:** 100
**Valid Judgments:** 70

---

## Model Pool

Models selected for **Programming & Code** evaluation:

1. **Grok Code Fast 1** (openrouter)
2. **Claude Opus 4.5** (openrouter)
3. **Gemini 3 Flash Preview** (openrouter)
4. **Claude Sonnet 4.5** (openrouter)
5. **Gemini 3 Pro Preview** (openrouter)
6. **MiniMax M2.1** (openrouter)
7. **GLM 4.7** (openrouter)
8. **DeepSeek V3.2** (openrouter)
9. **GPT-5.2-Codex** (openrouter)
10. **Grok 3 (Direct)** (xai)

---

## Model Responses

### Grok Code Fast 1

**Generation Time:** 7540ms
**Tokens:** 1568

```
### Optimization Approach

The original function uses three nested loops to check all possible triplets, resulting in O(n³) time complexity. This is inefficient for large inputs. To optimize, we can leverage a standard algorithm for the 3Sum problem, which involves:

1. **Sorting the array first**: This allows us to use a two-pointer technique to find triplets efficiently while handling duplicates. Sorting ensures that we can skip over duplicate values to avoid redundant computations and maintain uniqueness.
2. **Iterating through each element as the first in the triplet**: For each element `arr[i]`, we use two pointers (left and right) to find pairs that, combined with `arr[i]`, sum to the target.
3. **Handling duplicates**: After sorting, we skip duplicate values for `arr[i]`, and within the two-pointer loop, we skip duplicates for the left and right pointers to ensure unique triplets.
4. **Early termination**: If the current `arr[i]` is the same as the previous one, we skip it. Similarly for the two-pointer movement.

This approach reduces the time complexity to O(n²) after sorting, as the two-pointer phase (nested inside the loop over i) is O(n²) total.

### Optimized Code

```python
def find_triplets_with_sum(arr, target_sum):
    """Find all unique triplets in arr that sum to target_sum"""
    arr.sort()  # Sort the array in-place for two-pointer technique
    n = len(arr)
    result = []
    
    for i in range(n - 2):
        # Skip duplicates for the first element
        if i > 0 and arr[i] == arr[i - 1]:
            continue
        
        left, right = i + 1, n - 1
        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]
            if current_sum == target_sum:
                result.append([arr[i], arr[left], arr[right]])
                # Skip duplicates for left and right
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == ...
```

### Claude Opus 4.5

**Generation Time:** 24559ms
**Tokens:** 2241

```
# Optimizing Triplet Sum from O(n³) to O(n²)

## Analysis of the Original Problem

The original solution uses three nested loops, checking every possible combination. We can optimize this using the **two-pointer technique** after sorting.

## Optimized Solution

```python
def find_triplets_with_sum(arr: list[int], target_sum: int) -> list[list[int]]:
    """
    Find all unique triplets in arr that sum to target_sum.
    
    Approach: Sort + Two Pointers
    Time Complexity: O(n²)
    Space Complexity: O(1) excluding output (O(n) for sorting in Python)
    
    Args:
        arr: List of integers
        target_sum: Target sum for triplets
        
    Returns:
        List of unique triplets that sum to target_sum
    """
    n = len(arr)
    if n < 3:
        return []
    
    arr_sorted = sorted(arr)  # O(n log n)
    result = []
    
    for i in range(n - 2):  # O(n) iterations
        # Skip duplicates for first element
        if i > 0 and arr_sorted[i] == arr_sorted[i - 1]:
            continue
        
        # Early termination: smallest possible sum too large
        if arr_sorted[i] + arr_sorted[i + 1] + arr_sorted[i + 2] > target_sum:
            break
        
        # Early skip: largest possible sum with arr_sorted[i] too small
        if arr_sorted[i] + arr_sorted[n - 2] + arr_sorted[n - 1] < target_sum:
            continue
        
        # Two-pointer search for remaining two elements
        left = i + 1
        right = n - 1
        remaining = target_sum - arr_sorted[i]
        
        while left < right:  # O(n) total for each i
            two_sum = arr_sorted[left] + arr_sorted[right]
            
            if two_sum == remaining:
                result.append([arr_sorted[i], arr_sorted[left], arr_sorted[right]])
                
                # Skip duplicates for second element
                while left < right and arr_sorted[left] == arr_sorted[left + 1]:
                    left += 1
                # Skip duplicates for thi...
```

### Gemini 3 Flash Preview

**Generation Time:** 6210ms
**Tokens:** 1043

```
To optimize this function from $O(n^3)$ to $O(n^2)$, we use the **Sorting + Two-Pointer** approach. 

While a theoretical $O(n \log n)$ solution for the "3Sum" problem does not currently exist (it is a known $3SUM$-hard problem), $O(n^2)$ is the industry-standard optimization that significantly outperforms the cubic approach.

### The Optimized Code

```python
def find_triplets_with_sum(arr, target_sum):
    """Find all unique triplets in arr that sum to target_sum in O(n^2)"""
    arr.sort()  # Step 1: Sort the array O(n log n)
    n = len(arr)
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
                
                # Skip duplicate values for the second and third elements
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

---

### Optimization Approach

1.  **Sorting:** By sorting the array first, we can use the relative magnitudes of numbers to decide which direction to move, eliminating the need for a third nested loop.
2.  **Two-Pointer Technique:** For every element `i`, we set a `left` pointer at `i + 1` and a `right` pointer at the end of the array. 
    *   If the sum is too small, we in...
```

### Claude Sonnet 4.5

**Generation Time:** 18786ms
**Tokens:** 1479

```
# Optimized Solution: O(n²) Time Complexity

Here's the optimized version using sorting and two-pointer technique:

```python
def find_triplets_with_sum(arr, target_sum):
    """Find all unique triplets in arr that sum to target_sum"""
    n = len(arr)
    if n < 3:
        return []
    
    # Sort the array - O(n log n)
    arr_sorted = sorted(arr)
    result = []
    
    # Iterate through the array - O(n)
    for i in range(n - 2):
        # Skip duplicate values for first element
        if i > 0 and arr_sorted[i] == arr_sorted[i - 1]:
            continue
        
        # Two-pointer approach for remaining two elements - O(n)
        left = i + 1
        right = n - 1
        
        while left < right:
            current_sum = arr_sorted[i] + arr_sorted[left] + arr_sorted[right]
            
            if current_sum == target_sum:
                result.append([arr_sorted[i], arr_sorted[left], arr_sorted[right]])
                
                # Skip duplicates for second element
                while left < right and arr_sorted[left] == arr_sorted[left + 1]:
                    left += 1
                # Skip duplicates for third element
                while left < right and arr_sorted[right] == arr_sorted[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
                
            elif current_sum < target_sum:
                left += 1  # Need larger sum
            else:
                right -= 1  # Need smaller sum
    
    return result
```

## Optimization Approach

### Key Insights:
1. **Sorting enables two-pointer technique**: Once sorted, we can efficiently find pairs that sum to a target
2. **Reduce one dimension**: Fix one element, then find pairs in the remaining array
3. **Skip duplicates intelligently**: Use sorted order to avoid duplicate triplets without checking membership

### Algorithm Steps:

1. **Sort the array** - O(n log n)
2. **Fix first element** (iterate i f...
```

### Gemini 3 Pro Preview

**Generation Time:** 20140ms
**Tokens:** 2235

```
Here is the optimized solution.

It is important to note that the **theoretical lower bound for the general 3-Sum problem is $O(n^2)$**. It is mathematically impossible to solve this in $O(n \log n)$ because, in the worst-case scenario, there can be $O(n^2)$ valid triplets to return, and simply constructing the output takes that long.

However, the solution below reduces the complexity from **$O(n^3)$** to **$O(n^2)$**, which is the standard optimal solution for this problem.

```python
def find_triplets_with_sum(arr, target_sum):
    """
    Find all unique triplets in arr that sum to target_sum.
    Time Complexity: O(n^2)
    Space Complexity: O(1) (excluding output storage)
    """
    arr.sort()  # Step 1: Sort the array
    n = len(arr)
    result = []
    
    for i in range(n - 2):
        # Skip duplicates for the first element to ensure uniqueness
        if i > 0 and arr[i] == arr[i - 1]:
            continue
            
        # Step 2: Use Two-Pointer technique for the remaining two numbers
        left = i + 1
        right = n - 1
        
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
                
                # Move both pointers inward after finding a match
                left +=
```

### MiniMax M2.1

**Generation Time:** 33370ms
**Tokens:** 2246

```

```

### GLM 4.7

**Generation Time:** 42335ms
**Tokens:** 2212

```

```

### DeepSeek V3.2

**Generation Time:** 40508ms
**Tokens:** 959

```
Looking at your `O(n³)` solution, we can optimize it using sorting and two-pointer technique. Here's the optimized version:

```python
def find_triplets_with_sum(arr, target_sum):
    """Find all unique triplets in arr that sum to target_sum"""
    n = len(arr)
    arr.sort()  # Sort the array first
    result = []
    
    for i in range(n - 2):
        # Skip duplicate values for the first element
        if i > 0 and arr[i] == arr[i - 1]:
            continue
            
        left = i + 1
        right = n - 1
        remaining_sum = target_sum - arr[i]
        
        while left < right:
            current_sum = arr[left] + arr[right]
            
            if current_sum == remaining_sum:
                result.append([arr[i], arr[left], arr[right]])
                
                # Skip duplicates for left pointer
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                # Skip duplicates for right pointer  
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

## Optimization Approach:

1. **Sorting First** (`O(n log n)`):
   - We sort the array initially. This allows us to use the two-pointer technique.

2. **Fixed First Element + Two Pointers** (`O(n²)`):
   - Fix the first element `arr[i]`
   - Use two pointers (`left` and `right`) to find pairs that sum to `target_sum - arr[i]`
   - This reduces the inner two loops to `O(n)` per outer loop iteration

3. **Duplicate Skipping**:
   - After sorting, identical elements are adjacent
   - We skip duplicate values for all three positions to ensure unique triplets without needing to check `if triplet not in result`

## Time Complexity Analysis:

1. **Sorting**: `O(n log n)`
2. **Main Algorithm...
```

### GPT-5.2-Codex

**Generation Time:** 11666ms
**Tokens:** 811

```
Below is the standard **3‑Sum optimization** using sorting + two pointers. It reduces the runtime from **O(n³)** to **O(n²)** (which is even better than O(n log n)) while still returning **unique triplets**.

---

## ✅ Optimized Solution (O(n²))

```python
def find_triplets_with_sum(arr, target_sum):
    arr.sort()
    n = len(arr)
    result = []

    for i in range(n - 2):
        # skip duplicate fixed elements
        if i > 0 and arr[i] == arr[i - 1]:
            continue

        left, right = i + 1, n - 1
        while left < right:
            s = arr[i] + arr[left] + arr[right]
            if s == target_sum:
                result.append([arr[i], arr[left], arr[right]])

                # skip duplicates for left and right
                left += 1
                right -= 1
                while left < right and arr[left] == arr[left - 1]:
                    left += 1
                while left < right and arr[right] == arr[right + 1]:
                    right -= 1

            elif s < target_sum:
                left += 1
            else:
                right -= 1

    return result
```

---

## ✅ Why This Works

### 1. **Sort the array**
Sorting allows us to use the **two‑pointer** technique and easily skip duplicates.

### 2. **Fix one element**
For each index `i`, we search for two elements after `i` that sum to:

```
target_sum - arr[i]
```

### 3. **Two‑pointer search**
The inner loop runs in linear time because each pointer moves only forward or backward.

---

## ✅ Time Complexity Proof

- Sorting: **O(n log n)**
- Outer loop: **n**
- Inner two‑pointer loop: **O(n)** per iteration

Total:

```
O(n log n) + O(n * n) = O(n²)
```

So the optimized runtime is **O(n²)**.

---

## ✅ Correctness
- Sorting ensures triplets are considered in order.
- Duplicate skipping ensures uniqueness.
- Two‑pointer guarantees all valid pairs are found for each fixed `i`.

---

If you'd like, I can also provide a version that returns indices instead of values or ha...
```

### Grok 3 (Direct)

**Generation Time:** 12318ms
**Tokens:** 1159

```
Let's optimize this function from O(n³) to O(n²) using a two-pointer approach after sorting the array. While O(n log n) is theoretically possible for some variations of the 3Sum problem, for the general case of finding all unique triplets with a target sum, O(n²) is typically the best practical complexity we can achieve while maintaining correctness and readability.

Here's the optimized solution:

```python
def find_triplets_with_sum(arr, target_sum):
    """
    Find all unique triplets in arr that sum to target_sum
    Time Complexity: O(n²)
    Space Complexity: O(1) or O(n) depending on output size
    """
    n = len(arr)
    if n < 3:
        return []
        
    # Sort the array first - O(n log n)
    arr.sort()
    result = []
    
    # Iterate through array with first pointer
    for i in range(n - 2):
        # Skip duplicates for i
        if i > 0 and arr[i] == arr[i - 1]:
            continue
            
        # Use two pointers for remaining two numbers
        left = i + 1
        right = n - 1
        
        while left < right:
            current_sum = arr[i] + arr[left] + arr[right]
            
            if current_sum == target_sum:
                result.append([arr[i], arr[left], arr[right]])
                # Skip duplicates for left and right
                while left < right and arr[left] == arr[left + 1]:
                    left += 1
                while left < right and arr[right] == arr[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif current_sum < target_sum:
                left += 1
            else:
                right -= 1
                
    return result
```

### Optimization Approach Explanation:
1. **Sorting**: First, we sort the array in O(n log n) time. This allows us to use two pointers efficiently and handle duplicates easily.
2. **Two-Pointer Technique**: Instead of using three nested loops, we fix one element (i) and use two pointers (left and ...
```

---

*Generated by The Multivac V5*
*https://multivac.com*