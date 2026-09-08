TRACK = {
    "slug": "algorithms",
    "name": "Algorithms & Data Structures",
    "tagline": "Complexity you can reason about, from basic linear scans to dynamic programming.",
    "description": (
        "Start from absolute zero. Learn how to measure code speed with Big-O, master fundamental "
        "patterns like two pointers, binary search, sliding window, and conquer recursion and dynamic programming step-by-step."
    ),
    "icon": "∑",
    "accent": "#22c1a4",
    "order": 2,
    "required_xp": 200,
    "levels": [
        # =========================================================================
        # LEVEL 1: BIG-O INTUITION & ALGORITHMIC THINKING
        # =========================================================================
        {
            "index": 1,
            "title": "Algorithmic Thinking & Big-O Intuition",
            "summary": "Why wall-clock time lies, counting operations, O(1) vs O(n), and space vs time trade-offs.",
            "xp_reward": 80,
            "lessons": [
                {
                    "title": "What is an Algorithm & Why Seconds Lie",
                    "minutes": 6,
                    "body": """An **algorithm** is simply a step-by-step recipe to solve a specific problem.

When comparing two algorithms, measuring seconds with a stopwatch is misleading:
- A fast MacBook runs slow code faster than a budget phone runs clean code.
- Background processes and operating system noise cause random spikes in seconds.
- An algorithm might run in 0.001 seconds on 10 items, but completely freeze your server on 100,000 items!

### Big-O Notation
Instead of counting seconds, computer science measures **how the number of basic operations grows as the input size $n$ increases**:

| Big-O | Name | Operations on $n = 1,000,000$ | Everyday Analogy |
| :--- | :--- | :--- | :--- |
| **$O(1)$** | Constant | 1 operation | Looking up someone's shoe size when you already have their index card |
| **$O(\\log n)$** | Logarithmic | ~20 operations | Looking up a name in an alphabetized phonebook by opening in the middle |
| **$O(n)$** | Linear | 1,000,000 operations | Reading a book cover to cover, page by page |
| **$O(n \\log n)$** | Linearithmic | ~20,000,000 operations | Efficient sorting (Python's Timsort / MergeSort) |
| **$O(n^2)$** | Quadratic | $10^{12}$ (1 Trillion!) | Comparing every person in a stadium to every other person |

> [!NOTE]
> In Big-O, we only care about the **dominant term** as $n \\rightarrow \\infty$. We discard constant numbers and lower terms:
> - $5n + 100 \\rightarrow O(n)$
> - $n^2 + 500n \\rightarrow O(n^2)$""",
                },
                {
                    "title": "Spotting Hidden Loops & The Space/Time Trade-off",
                    "minutes": 6,
                    "body": """A frequent trap for beginners is writing an $O(n^2)$ quadratic algorithm without realizing they wrote a second loop.

```python
# Looks like one loop, but it is secretly O(n^2)!
unique_items = []
for x in items:              # Loop 1: runs n times
    if x not in unique_items: # HIDDEN LOOP: 'in' on a list scans every element!
        unique_items.append(x)
```

Because `x not in unique_items` scans the entire list of up to $n$ items, the total operations are:
$$1 + 2 + 3 + \\dots + n \\approx \\frac{n^2}{2} = O(n^2)$$

### Trading Memory (Space) for Speed (Time)
Computers have two scarce resources: **CPU time** and **RAM memory**.
By using an auxiliary hash set (`seen = set()`), membership checking becomes instant $O(1)$:

```python
seen = set()
unique_items = []
for x in items:          # Loop 1: runs n times
    if x not in seen:    # O(1) hash check!
        seen.add(x)
        unique_items.append(x)
```
This runs in **$O(n)$ linear time**! We traded a small amount of extra memory to make the code 100,000x faster on large datasets.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Halving the Search Space",
                    "prompt": "An algorithm repeatedly halves the remaining search space on each step. What is its time complexity as a function of input size n?",
                    "hint": "Think of opening a phonebook in the middle each time.",
                    "explanation": "Repeatedly dividing by 2 is the mathematical definition of the logarithm base 2: O(log n).",
                    "xp": 20,
                    "config": {"options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"]},
                    "solution": {"answer": 1},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Identifying Linear O(n) Operations",
                    "prompt": "Which of the following operations run in O(n) time on a standard Python list of length n?",
                    "hint": "Which operations must inspect every element from start to end?",
                    "explanation": "`sum(nums)` and `item in nums` must scan all n elements. Index access `nums[0]` is O(1) constant time.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "sum(nums)",
                            "nums[0] (accessing the first element)",
                            "target in nums (linear search)",
                            "min(nums) (finding the minimum element)",
                        ]
                    },
                    "solution": {"answers": [0, 2, 3]},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Constant Time Symbol",
                    "prompt": "What Big-O notation represents an operation that takes the exact same number of steps regardless of input size?",
                    "hint": "O followed by parentheses and a number.",
                    "explanation": "O(1) represents constant time.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. O(n)"},
                    "solution": {"regex": True, "accept": [r"o\(1\)", r"O\(1\)"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Two Sum (Linear Pass)",
                    "prompt": "Write `two_sum(nums, target)` returning the indices `[i, j]` (with `i < j`) of two numbers that add up to `target`.\nIf no pair exists, return `[]`.\n\nMust run in **O(n)** time using a dictionary lookup.\n\n```python\ntwo_sum([2, 7, 11, 15], 9) -> [0, 1]\ntwo_sum([3, 2, 4], 6) -> [1, 2]\ntwo_sum([1, 2, 3], 99) -> []\n```",
                    "hint": "For each number at index `i`, its required partner is `needed = target - num`. Check if `needed` is already in your `{number: index}` dictionary.",
                    "explanation": "Storing visited numbers in a dictionary enables instant O(1) pair matching in a single linear pass.",
                    "xp": 40,
                    "config": {
                        "language": "python",
                        "starter": "def two_sum(nums, target):\n    # Return [i, j] such that nums[i] + nums[j] == target\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "two_sum",
                        "cases": [
                            {"args": [[2, 7, 11, 15], 9], "expect": [0, 1]},
                            {"args": [[3, 2, 4], 6], "expect": [1, 2]},
                            {"args": [[1, 2, 3], 99], "expect": []},
                            {"args": [[0, 4, 3, 0], 0], "expect": [0, 3]},
                            {"args": [[-1, -2, -3, -4], -7], "expect": [2, 3], "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 2: LINEAR PATTERNS & TWO POINTERS
        # =========================================================================
        {
            "index": 2,
            "title": "Linear Patterns & Two Pointers",
            "summary": "Index mathematics, converging pointers from both ends, palindromes, and in-place reversal.",
            "xp_reward": 90,
            "lessons": [
                {
                    "title": "The Two Pointers Pattern Explained",
                    "minutes": 6,
                    "body": """In linear collections (arrays, lists, strings), the naive way to test pairs is using nested loops ($O(n^2)$).
The **Two Pointers** pattern allows you to inspect elements from opposite ends or at different speeds in a single pass ($O(n)$).

### Converging Pointers
Place one pointer at the start (`left = 0`) and one pointer at the end (`right = len(arr) - 1`).
Move them towards each other:

```python
left = 0
right = len(items) - 1

while left < right:
    # Process items[left] and items[right]
    left += 1
    right -= 1
```

### Palindrome Checking
A **palindrome** is a sequence that reads the exact same forward and backwards (like `"radar"` or `"racecar"`).
Using two pointers, we compare the outermost characters:
1. Compare `text[0]` with `text[-1]`. If different $\\rightarrow$ Not a palindrome.
2. Advance inward: compare `text[1]` with `text[-2]`.
3. Stop when pointers meet in the middle!""",
                },
                {
                    "title": "In-Place Swapping Without Extra Memory",
                    "minutes": 5,
                    "body": """Many interview questions ask you to modify an array **in-place**, meaning with $O(1)$ extra space.

In Python, you can swap two variables or array positions in a single atomic expression:
```python
arr[left], arr[right] = arr[right], arr[left]
```

### Reversing an Array in $O(n)$ Time and $O(1)$ Space:
```python
def reverse_array(arr):
    left = 0
    right = len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
    return arr
```
Every element is visited once, requiring only $\\frac{n}{2}$ swaps.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Two Pointers Convergence",
                    "prompt": "When running a two-pointer converging loop on an array of length n, when should the loop terminate?",
                    "hint": "What happens when left crosses right?",
                    "explanation": "When left >= right, all pairs have been examined and the pointers have met or crossed.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "When left >= right",
                            "When left == 0",
                            "When right == len(arr)",
                            "Only after n^2 steps",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "code",
                    "difficulty": "easy",
                    "title": "Palindrome Verification",
                    "prompt": "Write `is_palindrome(s)` returning `True` if string `s` is a palindrome, and `False` otherwise.\nAn empty string or single character is a palindrome.\n\n```python\nis_palindrome(\"racecar\") -> True\nis_palindrome(\"python\") -> False\nis_palindrome(\"noon\") -> True\nis_palindrome(\"\") -> True\n```",
                    "hint": "Compare characters from both ends using `s == s[::-1]` or two pointers.",
                    "explanation": "A palindrome is symmetric: characters from left and right mirror each other.",
                    "xp": 30,
                    "config": {
                        "language": "python",
                        "starter": "def is_palindrome(s):\n    # Return True if s is palindrome, else False\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "is_palindrome",
                        "cases": [
                            {"args": ["racecar"], "expect": True},
                            {"args": ["python"], "expect": False},
                            {"args": ["noon"], "expect": True},
                            {"args": [""], "expect": True},
                            {"args": ["a"], "expect": True},
                            {"args": ["deified"], "expect": True, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Reverse a List In-Place",
                    "prompt": "Write `reverse_list(nums)` that takes a list of integers and returns it reversed.\n\n```python\nreverse_list([1, 2, 3, 4, 5]) -> [5, 4, 3, 2, 1]\nreverse_list([42]) -> [42]\nreverse_list([]) -> []\n```",
                    "hint": "Use two pointers `lo = 0, hi = len(nums) - 1` and swap `nums[lo], nums[hi] = nums[hi], nums[lo]` while incrementing `lo` and decrementing `hi`.",
                    "explanation": "Swapping from both ends inverts the sequence in O(n) time.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def reverse_list(nums):\n    # Reverse and return the list\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "reverse_list",
                        "cases": [
                            {"args": [[1, 2, 3, 4, 5]], "expect": [5, 4, 3, 2, 1]},
                            {"args": [[42]], "expect": [42]},
                            {"args": [[]], "expect": []},
                            {"args": [[10, 20]], "expect": [20, 10]},
                            {"args": [[1, 3, 5, 7, 9]], "expect": [9, 7, 5, 3, 1], "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Python Negative Index",
                    "prompt": "In Python, what negative integer index points directly to the last element of any non-empty list?",
                    "hint": "A minus sign followed by a digit.",
                    "explanation": "In Python, `list[-1]` accesses the final element.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. -1"},
                    "solution": {"regex": True, "accept": [r"^-1$"]},
                },
            ],
        },

        # =========================================================================
        # LEVEL 3: BINARY SEARCH & DIVIDE AND CONQUER
        # =========================================================================
        {
            "index": 3,
            "title": "Logarithmic Speed: Binary Search",
            "summary": "Halving the search space, avoiding off-by-one errors, and finding insertion points.",
            "xp_reward": 100,
            "lessons": [
                {
                    "title": "Binary Search: The Logarithmic Divide",
                    "minutes": 6,
                    "body": """Imagine searching for a specific number in a sorted array of 1,000,000 items:
- **Linear Scan**: Check index 0, then index 1, ... up to 1,000,000 steps.
- **Binary Search**: Check the exact middle item. Is your target bigger or smaller? Discard the whole half that cannot contain it! Repeat!

On 1,000,000 items:
$$\\log_2(1,000,000) \\approx 20 \\text{ steps!}$$

> [!IMPORTANT]
> **Precondition**: Binary search **only works if the data is already sorted**. If the array is unsorted, you cannot know which half to discard.

### Bug-Free Binary Search Template:
```python
def binary_search(nums, target):
    lo = 0
    hi = len(nums) - 1
    
    while lo <= hi:  # <= ensures 1-element windows are checked
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1  # Target is in the right half
        else:
            hi = mid - 1  # Target is in the left half
            
    return -1  # Target does not exist in array
```""",
                },
                {
                    "title": "Finding Insertion Points (Lower Bound)",
                    "minutes": 5,
                    "body": """Often in real systems, the target value is not present, but you need to find **where it belongs** to maintain sorted order (like inserting a new timestamp into a log).

When binary search finishes with `lo > hi`:
- `lo` holds the exact index where `target` should be inserted!
- Python's standard library provides this in the `bisect` module (`bisect.bisect_left`).""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Binary Search Precondition",
                    "prompt": "What must be true about an array before you can apply Binary Search to it?",
                    "hint": "What allows you to safely discard an entire half?",
                    "explanation": "Binary search strictly requires the array to be sorted.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "The array must be sorted",
                            "The array must contain only positive integers",
                            "The array must have an even number of elements",
                            "The array must contain no duplicate values",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Binary Search Implementation",
                    "prompt": "Write `binary_search(sorted_nums, target)` returning the index of `target`, or `-1` if not found.\n\nMust run in **O(log n)** time.\n\n```python\nbinary_search([1, 3, 5, 7, 9], 7) -> 3\nbinary_search([1, 3, 5, 7, 9], 4) -> -1\nbinary_search([], 10) -> -1\n```",
                    "hint": "Maintain `lo = 0, hi = len(sorted_nums) - 1`. While `lo <= hi`, compute `mid = (lo + hi) // 2`.",
                    "explanation": "Binary search halves the search interval each step, finding elements in O(log n) time.",
                    "xp": 40,
                    "config": {
                        "language": "python",
                        "starter": "def binary_search(sorted_nums, target):\n    # Return index of target in sorted_nums or -1\n    lo = 0\n    hi = len(sorted_nums) - 1\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "binary_search",
                        "cases": [
                            {"args": [[1, 3, 5, 7, 9], 7], "expect": 3},
                            {"args": [[1, 3, 5, 7, 9], 1], "expect": 0},
                            {"args": [[1, 3, 5, 7, 9], 9], "expect": 4},
                            {"args": [[1, 3, 5, 7, 9], 4], "expect": -1},
                            {"args": [[], 10], "expect": -1},
                            {"args": [list(range(0, 500, 2)), 498], "expect": 249, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Find Insertion Index",
                    "prompt": "Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.\n\nMust be **O(log n)** time.\n\n```python\nsearch_insert([1, 3, 5, 6], 5) -> 2\nsearch_insert([1, 3, 5, 6], 2) -> 1\nsearch_insert([1, 3, 5, 6], 7) -> 4\nsearch_insert([1, 3, 5, 6], 0) -> 0\n```",
                    "hint": "When the binary search `while lo <= hi` loop terminates without finding the target, `lo` is the insertion position.",
                    "explanation": "At loop termination, lo points to the smallest index greater than target, which is the exact insertion slot.",
                    "xp": 40,
                    "config": {
                        "language": "python",
                        "starter": "def search_insert(nums, target):\n    # Return index of target or where it should be inserted\n    lo = 0\n    hi = len(nums) - 1\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "search_insert",
                        "cases": [
                            {"args": [[1, 3, 5, 6], 5], "expect": 2},
                            {"args": [[1, 3, 5, 6], 2], "expect": 1},
                            {"args": [[1, 3, 5, 6], 7], "expect": 4},
                            {"args": [[1, 3, 5, 6], 0], "expect": 0},
                            {"args": [[2, 4, 6, 8, 10], 9], "expect": 4, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Steps on 1024 Items",
                    "prompt": "In the worst case, how many comparison steps will Binary Search make on a sorted list of 1024 items?",
                    "hint": "What power of 2 equals 1024? 2^10 = 1024.",
                    "explanation": "log2(1024) = 10 steps.",
                    "xp": 25,
                    "config": {"placeholder": "an integer number of steps"},
                    "solution": {"regex": True, "accept": [r"^10$"]},
                },
            ],
        },

        # =========================================================================
        # LEVEL 4: HASH MAPS & SLIDING WINDOWS
        # =========================================================================
        {
            "index": 4,
            "title": "Hash Maps, Frequency & Sliding Windows",
            "summary": "O(1) hash tables, frequency counting, anagram detection, and fixed-size sliding windows.",
            "xp_reward": 110,
            "lessons": [
                {
                    "title": "Frequency Counters and Anagrams",
                    "minutes": 6,
                    "body": """A **frequency map** records how many times each item appears in a collection:

```python
counts = {}
for char in text:
    counts[char] = counts.get(char, 0) + 1
```

### Checking Anagrams
Two words are **anagrams** if they contain the exact same characters with the exact same frequencies (e.g. `"silent"` and `"listen"`).

Instead of sorting both strings ($O(n \\log n)$), we can compare their frequency dictionaries in **$O(n)$ linear time**:
```python
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    counts = {}
    for c in s:
        counts[c] = counts.get(c, 0) + 1
    for c in t:
        if c not in counts or counts[c] == 0:
            return False
        counts[c] -= 1
    return True
```""",
                },
                {
                    "title": "The Sliding Window Pattern",
                    "minutes": 6,
                    "body": """When asked to compute an aggregate over contiguous subarrays of length $k$:
- **Naive approach**: Recalculate the sum of each $k$-length window from scratch $\\rightarrow O(n \\times k)$.
- **Sliding Window**: Compute the initial window sum of size $k$. When sliding the window by 1:
  - Add the new incoming element on the right.
  - Subtract the outgoing element from the left.
  
$$O(1) \\text{ update per slide} \\implies O(n) \\text{ total time!}$$

```python
# Fixed size sliding window:
window_sum = sum(nums[:k])
max_sum = window_sum

for i in range(k, len(nums)):
    window_sum += nums[i] - nums[i - k]  # Add incoming, subtract outgoing
    if window_sum > max_sum:
        max_sum = window_sum
```""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Hash Map Lookup Complexity",
                    "prompt": "What is the average time complexity of looking up a key in a hash map / dictionary?",
                    "hint": "Hashing computes the memory address directly.",
                    "explanation": "Hash lookups execute in O(1) constant average time.",
                    "xp": 20,
                    "config": {"options": ["O(1)", "O(log n)", "O(n)", "O(n^2)"]},
                    "solution": {"answer": 0},
                },
                {
                    "kind": "code",
                    "difficulty": "easy",
                    "title": "Valid Anagram Verification",
                    "prompt": "Write `is_anagram(s, t)` returning `True` if string `t` is an anagram of `s`, and `False` otherwise.\n\n```python\nis_anagram(\"anagram\", \"nagaram\") -> True\nis_anagram(\"rat\", \"car\") -> False\nis_anagram(\"listen\", \"silent\") -> True\n```",
                    "hint": "Check if character counts match using a dictionary or Python's `collections.Counter`.",
                    "explanation": "Comparing character frequency maps verifies whether two strings have identical characters.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def is_anagram(s, t):\n    # Return True if s and t are anagrams\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "is_anagram",
                        "cases": [
                            {"args": ["anagram", "nagaram"], "expect": True},
                            {"args": ["rat", "car"], "expect": False},
                            {"args": ["listen", "silent"], "expect": True},
                            {"args": ["a", "ab"], "expect": False},
                            {"args": ["rail safety", "fairy tales"], "expect": True, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Max Subarray Sum of Size K",
                    "prompt": "Write `max_subarray_sum(nums, k)` that finds the maximum sum of any contiguous subarray of size `k`.\nIf `len(nums) < k` or `k <= 0`, return `0`.\n\nMust run in **O(n) time** using a sliding window.\n\n```python\nmax_subarray_sum([2, 1, 5, 1, 3, 2], 3) -> 9  (from [5, 1, 3])\nmax_subarray_sum([2, 3, 4, 1, 5], 2) -> 7      (from [3, 4])\n```",
                    "hint": "Compute initial `sum(nums[:k])`. Then loop from `k` to `len(nums)`, adding `nums[i]` and subtracting `nums[i-k]`.",
                    "explanation": "Sliding the window updates the sum in O(1) per step, yielding O(n) total time.",
                    "xp": 45,
                    "config": {
                        "language": "python",
                        "starter": "def max_subarray_sum(nums, k):\n    if len(nums) < k or k <= 0:\n        return 0\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "max_subarray_sum",
                        "cases": [
                            {"args": [[2, 1, 5, 1, 3, 2], 3], "expect": 9},
                            {"args": [[2, 3, 4, 1, 5], 2], "expect": 7},
                            {"args": [[1, 2], 5], "expect": 0},
                            {"args": [[4, 2, 1, 7, 8, 1, 2, 8, 1, 0], 3], "expect": 16},
                            {"args": [[5], 1], "expect": 5, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Sliding Window Applications",
                    "prompt": "Which of the following problems are natural fits for the Sliding Window pattern?",
                    "hint": "Look for requirements asking for contiguous subarrays or substrings.",
                    "explanation": "Contiguous subarray and substring questions are classic sliding window problems.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "Find maximum average of any contiguous subarray of length k",
                            "Find the longest substring without repeating characters",
                            "Find the shortest path in a graph",
                            "Find the most frequent number in an unsorted list",
                        ]
                    },
                    "solution": {"answers": [0, 1]},
                },
            ],
        },

        # =========================================================================
        # LEVEL 5: RECURSION & DYNAMIC PROGRAMMING
        # =========================================================================
        {
            "index": 5,
            "title": "Recursion & Dynamic Programming",
            "summary": "Base cases, call stacks, memoization ('cache the recursion'), and overlapping subproblems.",
            "xp_reward": 120,
            "lessons": [
                {
                    "title": "Recursion: Base Cases & The Call Stack",
                    "minutes": 6,
                    "body": """A **recursive function** is a function that calls itself to solve smaller instances of the exact same problem.

Every recursive function requires two essential parts:
1. **Base Case**: The simplest possible input where the answer is known without further recursion (terminates the loop).
2. **Recursive Step**: Calling the function on a smaller input that brings you closer to the base case.

```python
def factorial(n):
    if n <= 1:                   # Base case
        return 1
    return n * factorial(n - 1)  # Recursive step
```

> [!CAUTION]
> If you omit the base case, the function calls itself indefinitely until Python runs out of memory and crashes with `RecursionError: maximum recursion depth exceeded`.""",
                },
                {
                    "title": "Dynamic Programming: Cache the Recursion",
                    "minutes": 7,
                    "body": """Dynamic Programming (DP) sounds intimidating, but in practice it means:
**"Never recompute a subproblem you have already solved."**

Take the naive Fibonacci definition:
$$fib(n) = fib(n-1) + fib(n-2)$$

Computing $fib(5)$ calculates $fib(3)$ multiple times across different branches of the call tree, creating an exponential $O(2^n)$ explosion. At $n = 45$, it hangs for minutes.

### Memoization (Top-Down DP)
Store each answer in a dictionary cache. If we have seen this argument before, return the cached result in $O(1)$:

```python
def fib(n, memo=None):
    if memo is None:
        memo = {}
    if n <= 0:
        return 0
    if n == 1:
        return 1
    if n in memo:
        return memo[n]  # Cache hit!
        
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
```
With memoization, the time collapses from exponential $O(2^n)$ down to linear **$O(n)$**!""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Naive Fibonacci Complexity",
                    "prompt": "What is the time complexity of naive recursive Fibonacci without memoization: `fib(n) = fib(n-1) + fib(n-2)`?",
                    "hint": "Each call branches into two recursive calls.",
                    "explanation": "Because each function call branches into two child calls without caching, the call tree doubles at each depth: O(2^n).",
                    "xp": 25,
                    "config": {"options": ["O(1)", "O(n)", "O(n log n)", "O(2^n)"]},
                    "solution": {"answer": 3},
                },
                {
                    "kind": "code",
                    "difficulty": "easy",
                    "title": "Factorial Calculation",
                    "prompt": "Write `factorial(n)` that calculates $n! = n \\times (n-1) \\times \\dots \\times 1$.\nBy mathematical definition, `factorial(0) = 1` and `factorial(1) = 1`.\n\n```python\nfactorial(3) -> 6\nfactorial(5) -> 120\nfactorial(0) -> 1\n```",
                    "hint": "Base case: `if n <= 1: return 1`. Otherwise: `return n * factorial(n - 1)`.",
                    "explanation": "Factorial is the quintessential recursion introductory problem.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def factorial(n):\n    # Return n!\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "factorial",
                        "cases": [
                            {"args": [3], "expect": 6},
                            {"args": [5], "expect": 120},
                            {"args": [0], "expect": 1},
                            {"args": [1], "expect": 1},
                            {"args": [7], "expect": 5040, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Fast Linear Fibonacci",
                    "prompt": "Write `fib(n)` returning the $n$-th Fibonacci number ($0, 1, 1, 2, 3, 5, 8, \\dots$):\n- `fib(0) = 0`\n- `fib(1) = 1`\n\nMust run in **O(n) time** (able to calculate `fib(30)` instantly).\n\n```python\nfib(0) -> 0\nfib(1) -> 1\nfib(6) -> 8\n```",
                    "hint": "Use an iterative loop tracking `a, b = 0, 1` or a memo dictionary.",
                    "explanation": "Iterative tabulation or memoization computes Fibonacci in linear O(n) time.",
                    "xp": 40,
                    "config": {
                        "language": "python",
                        "starter": "def fib(n):\n    # Return n-th Fibonacci number in O(n)\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "fib",
                        "cases": [
                            {"args": [0], "expect": 0},
                            {"args": [1], "expect": 1},
                            {"args": [6], "expect": 8},
                            {"args": [10], "expect": 55},
                            {"args": [30], "expect": 832040, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Climbing Stairs (Dynamic Programming)",
                    "prompt": "You are climbing a staircase with `n` steps. Each time you can climb either **1 step or 2 steps**.\nIn how many distinct ways can you climb to the top?\n\n```python\nclimb_stairs(2) -> 2  (1+1, or 2)\nclimb_stairs(3) -> 3  (1+1+1, 1+2, 2+1)\nclimb_stairs(4) -> 5\n```",
                    "hint": "Notice that the number of ways to reach step `n` is `ways(n-1) + ways(n-2)`.",
                    "explanation": "Because you can only reach step n from step n-1 or step n-2, dp[n] = dp[n-1] + dp[n-2].",
                    "xp": 45,
                    "config": {
                        "language": "python",
                        "starter": "def climb_stairs(n):\n    # Return number of distinct ways to reach step n\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "climb_stairs",
                        "cases": [
                            {"args": [1], "expect": 1},
                            {"args": [2], "expect": 2},
                            {"args": [3], "expect": 3},
                            {"args": [4], "expect": 5},
                            {"args": [5], "expect": 8},
                            {"args": [20], "expect": 10946, "hidden": True},
                        ],
                    },
                },
            ],
        },
    ],
}
