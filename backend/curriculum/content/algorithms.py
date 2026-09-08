TRACK = {
    "slug": "algorithms",
    "name": "Algorithms & Data Structures",
    "tagline": "Complexity you can reason about under interview pressure.",
    "description": (
        "Big-O as a decision tool, the four patterns that solve most problems "
        "(hashing, two pointers, binary search, graph traversal), and dynamic programming "
        "without the mystique."
    ),
    "icon": "∑",
    "accent": "#22c1a4",
    "order": 2,
    "required_xp": 400,
    "levels": [
        {
            "index": 1,
            "title": "Complexity, honestly",
            "summary": "Read the loop, name the growth, know when it stops mattering.",
            "xp_reward": 90,
            "lessons": [
                {
                    "title": "Big-O in ninety seconds",
                    "minutes": 6,
                    "body": """Big-O describes how runtime grows as input grows. Constants are dropped, the dominant term wins.

| Shape in the code | Complexity | n = 1e6 feels like |
| --- | --- | --- |
| Hash lookup, arithmetic | O(1) | instant |
| Halve the range each step | O(log n) | instant |
| One pass | O(n) | fast |
| Sort | O(n log n) | fine |
| Nested loop over the same input | O(n²) | ~forever |
| Subsets | O(2ⁿ) | impossible past n≈25 |

How to read it: **count the loops that depend on n, and multiply.**

```python
for i in range(n):        # n
    for j in range(n):    # * n
        work()            # => O(n^2)
```

Watch for hidden loops: `x in list`, `list.remove`, `str +=` inside a loop, and slicing (`a[1:]` copies).

**Space** matters too. An O(n) hash map to make a loop O(n) is usually the right trade; an O(n²) memo table on a million rows is not.""",
                },
                {
                    "title": "Amortized and average vs worst",
                    "minutes": 5,
                    "body": """Three different numbers get called "the" complexity:

- **Worst case** — the guarantee. Use it for anything user-facing with adversarial input.
- **Average case** — over random inputs. Hash tables are O(1) here, O(n) worst.
- **Amortized** — averaged over a sequence. `list.append` is O(1) amortized: occasionally it copies the whole array to grow, but the doubling makes the cost per append constant.

Where this bites in practice:

- Quicksort is O(n log n) average, O(n²) worst on already-sorted input with a naive pivot.
- Hash maps degrade to O(n) under collisions — the basis of real hash-flooding DoS attacks.
- Amortized guarantees are useless when you need a *latency bound per operation* (a trading loop, an audio callback). There, the occasional resize is the problem.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Read the growth",
                    "prompt": "```python\ndef f(items):\n    out = []\n    for x in items:\n        if x not in out:\n            out.append(x)\n    return out\n```\n\nWhat is the worst-case time complexity?",
                    "hint": "`x not in out` is not free.",
                    "explanation": "`in` on a list scans it. With all-distinct input `out` grows to n, so the scans sum to 1+2+...+n = O(n²).",
                    "xp": 20,
                    "config": {"options": ["O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)"]},
                    "solution": {"answer": 2},
                },
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Which one is a lie",
                    "prompt": "Which statement is **false**?",
                    "hint": "One of these confuses average with worst case.",
                    "explanation": "Hash map lookup is O(1) *average*; the worst case is O(n) when every key collides. The other three statements are correct.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "`list.append` is O(1) amortized",
                            "Dict lookup is O(1) in the worst case",
                            "Binary search needs the input sorted",
                            "Comparison sorting cannot beat O(n log n)",
                        ]
                    },
                    "solution": {"answer": 1},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Two-sum in one pass",
                    "prompt": "Write `two_sum(nums, target)` returning the **indices** `[i, j]` (i < j) of the two numbers adding to `target`, or `[]` if none exist.\n\nMust be O(n). Exactly one valid pair per test.\n\n```\ntwo_sum([2, 7, 11, 15], 9) -> [0, 1]\n```",
                    "hint": "As you walk the list, remember value -> index. Look for `target - x` in that map.",
                    "explanation": "The nested-loop version is O(n²). Storing seen values in a dict turns the inner search into an O(1) lookup, so one pass suffices. This trade — memory for time — is the single most common interview move.",
                    "xp": 40,
                    "config": {"language": "python", "starter": "def two_sum(nums, target):\n    ...\n"},
                    "solution": {
                        "entrypoint": "two_sum",
                        "cases": [
                            {"args": [[2, 7, 11, 15], 9], "expect": [0, 1]},
                            {"args": [[3, 2, 4], 6], "expect": [1, 2]},
                            {"args": [[1, 2], 99], "expect": []},
                            {"args": [[0, 4, 3, 0], 0], "expect": [0, 3]},
                            {"args": [[-1, -2, -3], -5], "expect": [1, 2], "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Binary search, no off-by-one",
                    "prompt": "Write `search(sorted_nums, target)` returning the index of `target` or `-1`.\n\nO(log n). Do not use `list.index`.",
                    "hint": "`lo, hi = 0, len(a) - 1` with `while lo <= hi`, and `mid = (lo + hi) // 2`.",
                    "explanation": "The two classic bugs are the loop condition (`<` vs `<=`) and forgetting `mid ± 1`, which loops forever. Writing it from memory correctly is a real interview filter.",
                    "xp": 40,
                    "config": {"language": "python", "starter": "def search(sorted_nums, target):\n    ...\n"},
                    "solution": {
                        "entrypoint": "search",
                        "cases": [
                            {"args": [[1, 3, 5, 7, 9], 7], "expect": 3},
                            {"args": [[1, 3, 5, 7, 9], 1], "expect": 0},
                            {"args": [[1, 3, 5, 7, 9], 9], "expect": 4},
                            {"args": [[1, 3, 5, 7, 9], 4], "expect": -1},
                            {"args": [[], 1], "expect": -1},
                            {"args": [[5], 5], "expect": 0},
                            {"args": [list(range(0, 2000, 2)), 1998], "expect": 999, "hidden": True},
                        ],
                    },
                },
            ],
        },
        {
            "index": 2,
            "title": "The four patterns",
            "summary": "Hashing, two pointers, sliding window, and stacks cover most problems.",
            "xp_reward": 100,
            "lessons": [
                {
                    "title": "Pattern recognition beats cleverness",
                    "minutes": 7,
                    "body": """Interview problems are mostly a small set of shapes wearing different costumes.

**Hash map** — "count", "seen before", "group by", "anagram", "pair that sums to". Trade O(n) space for O(1) lookup.

**Two pointers** — a *sorted* array or a comparison from both ends. Palindromes, pair-sum on sorted input, merging.

```python
lo, hi = 0, len(a) - 1
while lo < hi:
    s = a[lo] + a[hi]
    if s == target: return [lo, hi]
    if s < target:  lo += 1
    else:           hi -= 1
```

**Sliding window** — "longest/shortest contiguous subarray with property P". Grow the right edge, shrink the left while the window is invalid.

**Stack** — nesting and "the most recent unmatched thing": bracket matching, next-greater-element, expression parsing.

When you see a new problem, spend ten seconds asking *which of these four is it* before writing anything.""",
                },
                {
                    "title": "The sliding window template",
                    "minutes": 5,
                    "body": """One template covers nearly every window problem:

```python
def longest_ok(s):
    left = 0
    best = 0
    state = {}                     # whatever "validity" needs
    for right, ch in enumerate(s):
        state[ch] = state.get(ch, 0) + 1
        while not valid(state):    # shrink until legal again
            state[s[left]] -= 1
            if state[s[left]] == 0:
                del state[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
```

Each index enters and leaves the window at most once, so despite the nested `while` this is **O(n)**, not O(n²). Being able to say that sentence out loud in an interview is worth as much as the code.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Name the pattern",
                    "prompt": "\"Find the length of the longest substring without repeating characters.\"\n\nWhich pattern fits?",
                    "hint": "Contiguous, longest, one property to maintain.",
                    "explanation": "Contiguous + longest + a maintainable validity condition is the sliding-window signature. It runs in O(n) with a set or count map for the window.",
                    "xp": 25,
                    "config": {"options": ["Binary search", "Sliding window", "Backtracking", "Union-find"]},
                    "solution": {"answer": 1},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Balanced brackets",
                    "prompt": "Write `is_balanced(s)` returning `True` if every `()`, `[]`, `{}` in `s` is properly nested and closed. Other characters are ignored.\n\n```\nis_balanced(\"a[b(c)d]\") -> True\nis_balanced(\"([)]\")      -> False\n```",
                    "hint": "Push openers, and on a closer check the top of the stack matches.",
                    "explanation": "A stack is the right structure whenever correctness depends on the *most recent unmatched* item. Empty stack on a closer, or a non-empty stack at the end, both mean unbalanced.",
                    "xp": 40,
                    "config": {"language": "python", "starter": "def is_balanced(s):\n    ...\n"},
                    "solution": {
                        "entrypoint": "is_balanced",
                        "cases": [
                            {"args": ["a[b(c)d]"], "expect": True},
                            {"args": ["([)]"], "expect": False},
                            {"args": [""], "expect": True},
                            {"args": ["((("], "expect": False},
                            {"args": [")("], "expect": False},
                            {"args": ["{[()]}"], "expect": True},
                            {"args": ["no brackets here"], "expect": True, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "hard",
                    "title": "Longest unique substring",
                    "prompt": "Write `longest_unique(s)` returning the **length** of the longest substring with no repeated characters.\n\n```\nlongest_unique(\"abcabcbb\") -> 3\nlongest_unique(\"bbbbb\")    -> 1\nlongest_unique(\"pwwkew\")   -> 3\n```\n\nO(n) required — the tests include a long string.",
                    "hint": "Keep `last_seen[char]`. When you hit a repeat inside the window, jump `left` past it.",
                    "explanation": "Storing the last index of each char lets `left` jump directly instead of crawling, and each index is visited once, giving O(n) time and O(alphabet) space.",
                    "xp": 55,
                    "config": {"language": "python", "starter": "def longest_unique(s):\n    ...\n"},
                    "solution": {
                        "entrypoint": "longest_unique",
                        "cases": [
                            {"args": ["abcabcbb"], "expect": 3},
                            {"args": ["bbbbb"], "expect": 1},
                            {"args": ["pwwkew"], "expect": 3},
                            {"args": [""], "expect": 0},
                            {"args": ["abcdef"], "expect": 6},
                            {"args": ["ab" * 20000], "expect": 2, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Group anagrams",
                    "prompt": "Write `group_anagrams(words)` returning a list of groups, where each group holds words that are anagrams of each other.\n\n- keep words in their input order inside a group\n- order groups by the first word's position in the input\n\n```\ngroup_anagrams([\"eat\",\"tea\",\"tan\",\"ate\"]) -> [[\"eat\",\"tea\",\"ate\"],[\"tan\"]]\n```",
                    "hint": "The sorted letters of a word make a natural key. Python dicts keep insertion order.",
                    "explanation": "Canonical-key grouping: map each item to a normal form, bucket by it. O(n · k log k) for k-length words, and dict insertion order gives the required group ordering for free.",
                    "xp": 45,
                    "config": {"language": "python", "starter": "def group_anagrams(words):\n    ...\n"},
                    "solution": {
                        "entrypoint": "group_anagrams",
                        "cases": [
                            {"args": [["eat", "tea", "tan", "ate"]], "expect": [["eat", "tea", "ate"], ["tan"]]},
                            {"args": [[]], "expect": []},
                            {"args": [["a"]], "expect": [["a"]]},
                            {"args": [["ab", "ba", "abc"]], "expect": [["ab", "ba"], ["abc"]]},
                        ],
                    },
                },
            ],
        },
        {
            "index": 3,
            "title": "Graphs and dynamic programming",
            "summary": "BFS/DFS as reflexes, and DP as 'cache the recursion'.",
            "xp_reward": 120,
            "lessons": [
                {
                    "title": "BFS or DFS?",
                    "minutes": 6,
                    "body": """Any "grid", "network", "dependency", "reachable" or "shortest steps" problem is a graph problem.

- **BFS** (queue) — visits by distance. Use it for **shortest path in an unweighted graph**. Nothing else gives that for free.
- **DFS** (stack or recursion) — goes deep. Use it for connectivity, cycle detection, topological order, flood fill.
- **Dijkstra** — BFS with a priority queue, for non-negative weights.

```python
from collections import deque

def bfs(start, neighbors):
    seen = {start}
    q = deque([(start, 0)])
    while q:
        node, dist = q.popleft()
        for nxt in neighbors(node):
            if nxt not in seen:
                seen.add(nxt)
                q.append((nxt, dist + 1))
    return seen
```

**Mark visited when you enqueue, not when you dequeue.** Doing it at dequeue lets the same node enter the queue many times, which is the most common BFS bug.""",
                },
                {
                    "title": "DP is just memoized recursion",
                    "minutes": 7,
                    "body": """Dynamic programming has a reputation it doesn't deserve. The recipe:

1. Write the brute-force recursion.
2. Notice it recomputes the same arguments.
3. Cache on the arguments. Done — that's top-down DP.
4. *Optionally* flip it into a bottom-up loop for speed and no recursion limit.

```python
from functools import cache

@cache
def ways(n):                    # climb 1 or 2 stairs
    if n < 0: return 0
    if n == 0: return 1
    return ways(n - 1) + ways(n - 2)
```

Exponential becomes linear by adding one line.

To design a DP directly, name three things: the **state** (what the arguments mean), the **transition** (how a state is built from smaller ones), and the **base case**. If the state is right, the transition is usually one line. Most failed DP attempts are a wrong state, not a wrong loop.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Shortest path, unweighted",
                    "prompt": "You need the minimum number of moves between two cells in an unweighted grid with walls. Which traversal gives it directly?",
                    "hint": "Which one explores in order of distance?",
                    "explanation": "BFS explores in non-decreasing distance order, so the first time it reaches the target it has the minimum. DFS finds *a* path, not the shortest.",
                    "xp": 25,
                    "config": {"options": ["DFS", "BFS", "Either works equally", "Neither; you need Dijkstra"]},
                    "solution": {"answer": 1},
                },
                {
                    "kind": "short",
                    "difficulty": "medium",
                    "title": "The classic BFS bug",
                    "prompt": "In BFS, at which moment should you mark a node as visited to avoid it being enqueued multiple times?\n\nAnswer with one word: when you *enqueue* it, or when you *dequeue* it?",
                    "hint": "Think about a node with several neighbours pointing at it.",
                    "explanation": "Marking at enqueue time is the fix. Marking at dequeue lets several predecessors push the same node before it is ever popped, blowing up the queue.",
                    "xp": 25,
                    "config": {"placeholder": "enqueue or dequeue"},
                    "solution": {"regex": True, "accept": [r"(when\s+you\s+)?en\s*-?queue(d|ing)?", r"on\s+enqueue", r"push(ing)?"]},
                },
                {
                    "kind": "code",
                    "difficulty": "hard",
                    "title": "Count islands",
                    "prompt": "Write `count_islands(grid)` where `grid` is a list of lists of `0`/`1`. Return the number of connected groups of `1`s (4-directional adjacency).\n\n```\ncount_islands([[1,1,0],[0,1,0],[0,0,1]]) -> 2\n```\n\nYou may modify the grid.",
                    "hint": "Scan for an unvisited 1, then flood-fill it away; count how many times you had to start.",
                    "explanation": "Flood fill: each cell is visited once, so it is O(rows·cols). Use an explicit stack rather than recursion if the grid could be large enough to blow the recursion limit.",
                    "xp": 60,
                    "config": {"language": "python", "starter": "def count_islands(grid):\n    ...\n"},
                    "solution": {
                        "entrypoint": "count_islands",
                        "cases": [
                            {"args": [[[1, 1, 0], [0, 1, 0], [0, 0, 1]]], "expect": 2},
                            {"args": [[]], "expect": 0},
                            {"args": [[[0, 0], [0, 0]]], "expect": 0},
                            {"args": [[[1, 1], [1, 1]]], "expect": 1},
                            {"args": [[[1, 0, 1], [0, 0, 0], [1, 0, 1]]], "expect": 4},
                            {"args": [[[1, 0, 1, 1], [1, 0, 0, 1], [0, 0, 1, 1]]], "expect": 2, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "hard",
                    "title": "Coin change, minimum coins",
                    "prompt": "Write `min_coins(coins, amount)` returning the fewest coins summing exactly to `amount`, or `-1` if impossible. Unlimited supply of each coin.\n\n```\nmin_coins([1, 2, 5], 11) -> 3   # 5 + 5 + 1\nmin_coins([2], 3)       -> -1\nmin_coins([1, 2, 5], 0) -> 0\n```",
                    "hint": "`best[a] = 1 + min(best[a - c])` over coins that fit. Start with best[0] = 0.",
                    "explanation": "State = amount, transition = one coin off, base = 0 needs 0 coins. O(amount · len(coins)). Greedy (always take the biggest coin) is wrong for denominations like [1, 3, 4] with amount 6.",
                    "xp": 60,
                    "config": {"language": "python", "starter": "def min_coins(coins, amount):\n    ...\n"},
                    "solution": {
                        "entrypoint": "min_coins",
                        "cases": [
                            {"args": [[1, 2, 5], 11], "expect": 3},
                            {"args": [[2], 3], "expect": -1},
                            {"args": [[1, 2, 5], 0], "expect": 0},
                            {"args": [[1, 3, 4], 6], "expect": 2},
                            {"args": [[186, 419, 83, 408], 6249], "expect": 20, "hidden": True},
                        ],
                    },
                },
            ],
        },
    ],
}
