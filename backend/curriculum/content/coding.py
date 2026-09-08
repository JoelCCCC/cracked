TRACK = {
    "slug": "coding",
    "name": "Coding Foundations",
    "tagline": "Write code that other people can read, and that doesn't break.",
    "description": (
        "The base layer everything else sits on: data, control flow, functions, errors, "
        "and the habits that separate someone who can code from someone who ships."
    ),
    "icon": "{}",
    "accent": "#7c5cff",
    "order": 1,
    "required_xp": 0,
    "levels": [
        {
            "index": 1,
            "title": "Data and control flow",
            "summary": "Pick the right container, loop without off-by-ones, return early.",
            "xp_reward": 80,
            "lessons": [
                {
                    "title": "Choose the container before you write the loop",
                    "minutes": 6,
                    "body": """Most slow code is the right algorithm on the wrong container.

| You need | Use | Lookup cost |
| --- | --- | --- |
| Ordered items, index access | `list` | O(1) by index, O(n) by value |
| "Have I seen this?" | `set` | O(1) |
| Key to value | `dict` | O(1) |
| Fixed record | `tuple` / dataclass | O(1) |
| Push/pop both ends | `deque` | O(1) |

The classic mistake:

```python
# O(n*m) - `seen` is a list, so `in` scans it every time
seen = []
for x in items:
    if x not in seen:
        seen.append(x)
```

One character of type change makes it linear:

```python
seen = set()
out = []
for x in items:
    if x not in seen:
        seen.add(x)
        out.append(x)
```

**Rule of thumb:** if you write `in` inside a loop, the thing on the right had better be a `set` or a `dict`.""",
                },
                {
                    "title": "Guard clauses beat nesting",
                    "minutes": 5,
                    "body": """Deeply nested `if` blocks hide the happy path. Invert the condition and return early.

```python
# before
def charge(order):
    if order is not None:
        if order.items:
            if order.customer.active:
                return process(order)
            else:
                raise Error("inactive")
        else:
            raise Error("empty")
    else:
        raise Error("missing")

# after
def charge(order):
    if order is None:
        raise Error("missing")
    if not order.items:
        raise Error("empty")
    if not order.customer.active:
        raise Error("inactive")
    return process(order)
```

Same behaviour, one level of indentation, and every failure reason is visible in the first six lines. Reviewers notice this immediately.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Membership in a hot loop",
                    "prompt": "You loop over 1,000,000 records and check `if record_id in collection` each time.\n\nWhich container keeps the loop linear overall?",
                    "hint": "Think about what the `in` operator has to do for each type.",
                    "explanation": "`set` (and `dict`) hash the value, so membership is O(1). `list` and `tuple` scan element by element, making the whole loop O(n*m).",
                    "xp": 20,
                    "config": {"options": ["list", "tuple", "set", "It makes no difference in Python"]},
                    "solution": {"answer": 2},
                },
                {
                    "kind": "multi",
                    "difficulty": "easy",
                    "title": "Spot the guard clauses",
                    "prompt": "Which of these are true reasons to prefer guard clauses over nested conditionals?",
                    "hint": "Two of these are real; two are wishful thinking.",
                    "explanation": "Guard clauses flatten indentation and put failure cases up front. They do not change complexity, and they do not remove the need for tests.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "The happy path ends up at the lowest indentation level",
                            "Every failure reason is visible at the top of the function",
                            "They make the function asymptotically faster",
                            "They remove the need to unit-test the error paths",
                        ]
                    },
                    "solution": {"answers": [0, 1]},
                },
                {
                    "kind": "code",
                    "difficulty": "easy",
                    "title": "Deduplicate, keep order",
                    "prompt": "Write `dedupe(items)` returning a new list with duplicates removed, **preserving first-seen order**.\n\n```\ndedupe([3, 1, 3, 2, 1]) -> [3, 1, 2]\n```\n\nIt must stay fast on a list of 100k items, so no `in` against a list.",
                    "hint": "Track what you've seen in a set, build the output in a list.",
                    "explanation": "A `set` for membership plus a `list` for order is the canonical shape. `list(dict.fromkeys(items))` is the one-liner version and also O(n).",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def dedupe(items):\n    # your code here\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "dedupe",
                        "cases": [
                            {"args": [[3, 1, 3, 2, 1]], "expect": [3, 1, 2]},
                            {"args": [[]], "expect": []},
                            {"args": [[1, 1, 1]], "expect": [1]},
                            {"args": [["a", "b", "a", "c"]], "expect": ["a", "b", "c"]},
                            {"args": [list(range(500)) + list(range(500))], "expect": list(range(500)), "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Flatten one level",
                    "prompt": "Write `flatten(rows)` that takes a list of lists and returns a single flat list, in order.\n\n```\nflatten([[1, 2], [], [3]]) -> [1, 2, 3]\n```",
                    "hint": "A nested loop is fine. Appending inside two loops is O(total elements).",
                    "explanation": "Two loops (or `[x for row in rows for x in row]`) is linear in the number of elements. Repeated `out = out + row` would be quadratic because it copies each time.",
                    "xp": 30,
                    "config": {"language": "python", "starter": "def flatten(rows):\n    ...\n"},
                    "solution": {
                        "entrypoint": "flatten",
                        "cases": [
                            {"args": [[[1, 2], [], [3]]], "expect": [1, 2, 3]},
                            {"args": [[]], "expect": []},
                            {"args": [[[], []]], "expect": []},
                            {"args": [[["a"], ["b", "c"]]], "expect": ["a", "b", "c"]},
                        ],
                    },
                },
            ],
        },
        {
            "index": 2,
            "title": "Functions, errors, and contracts",
            "summary": "Small surfaces, honest failures, no silent corruption.",
            "xp_reward": 90,
            "lessons": [
                {
                    "title": "A function has a contract",
                    "minutes": 6,
                    "body": """Every function makes a promise: *given these inputs, I return this, or I raise this.* Break the promise quietly and you get bugs that surface three layers away.

Three rules that carry most of the weight:

1. **One job.** If the docstring needs the word "and", split it.
2. **No surprise mutation.** A function named `total(cart)` must not empty the cart. If you mutate, say so in the name: `sort_in_place`, `drain_queue`.
3. **Fail loudly, at the boundary.** Validate input where it enters your system, then trust it inside.

```python
def apply_discount(price: Decimal, percent: int) -> Decimal:
    if not 0 <= percent <= 100:
        raise ValueError(f"percent out of range: {percent}")
    return price * (100 - percent) / 100
```

The alternative, `return price` when percent is bogus, produces a wrong invoice and no stack trace. Wrong-and-silent is the most expensive failure mode there is.""",
                },
                {
                    "title": "Catch narrow, or don't catch",
                    "minutes": 5,
                    "body": """`except Exception:` around a block you don't understand is how a system starts lying to you.

```python
# swallows typos, KeyboardInterrupt-adjacent bugs, everything
try:
    user = fetch(uid)
except Exception:
    user = None
```

If `fetch` raises `AttributeError` because of a typo in *your* code, you now get `None` and a confusing failure much later.

```python
try:
    user = fetch(uid)
except UserNotFound:
    user = None          # a real, expected case
```

Catch the exceptions you have a plan for. Let the rest hit your error reporter, where a human sees the stack trace.

**Corollary:** an empty `except: pass` should always come with a comment explaining why losing that error is safe.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "The worst failure mode",
                    "prompt": "Ranked by cost to the business, which failure is usually the *most* expensive?",
                    "hint": "Which one does nobody notice until much later?",
                    "explanation": "A loud crash gets fixed today. Silently wrong data spreads into reports, invoices and downstream systems before anyone notices, and then has to be back-filled.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "The process crashes with a stack trace",
                            "The request returns a 400 with a clear message",
                            "The function returns a plausible but wrong value",
                            "The endpoint is slow",
                        ]
                    },
                    "solution": {"answer": 2},
                },
                {
                    "kind": "short",
                    "difficulty": "medium",
                    "title": "Name the smell",
                    "prompt": "A function called `get_user(id)` also writes a row to the audit table and updates a cache.\n\nWhat design principle is being violated? (Two or three words.)",
                    "hint": "It is doing more than one thing.",
                    "explanation": "Single responsibility (a.k.a. separation of concerns). A `get_` name promises a read; hidden writes make the function impossible to call safely from a read path.",
                    "xp": 25,
                    "config": {"placeholder": "e.g. some principle"},
                    "solution": {
                        "regex": True,
                        "accept": [
                            r"(the\s+)?single[- ]responsibility(\s+principle)?",
                            r"srp",
                            r"separation\s+of\s+concerns",
                            r"command[- /]query\s+separation",
                            r"cqs",
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Validate at the boundary",
                    "prompt": "Write `parse_port(value)`:\n\n- accepts an `int` or a numeric string\n- returns the port as an `int` when it is in `1..65535`\n- returns `None` for anything else (empty string, `\"abc\"`, `0`, `70000`, `None`)\n\nIt must not raise.",
                    "hint": "Convert inside a narrow try/except, then range-check.",
                    "explanation": "Parse-then-validate at the edge, and return a single well-defined 'no value' result. Callers now never have to guess whether the port is trustworthy.",
                    "xp": 35,
                    "config": {"language": "python", "starter": "def parse_port(value):\n    ...\n"},
                    "solution": {
                        "entrypoint": "parse_port",
                        "cases": [
                            {"args": ["8080"], "expect": 8080},
                            {"args": [443], "expect": 443},
                            {"args": ["0"], "expect": None},
                            {"args": ["70000"], "expect": None},
                            {"args": ["abc"], "expect": None},
                            {"args": [""], "expect": None},
                            {"args": [None], "expect": None},
                            {"args": [65535], "expect": 65535, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "No surprise mutation",
                    "prompt": "Write `with_tag(record, tag)` that returns a **new** dict with `tag` appended to `record['tags']`, leaving the input dict and its list untouched.\n\n```\nr = {'id': 1, 'tags': ['a']}\nwith_tag(r, 'b')  -> {'id': 1, 'tags': ['a', 'b']}\nr                 -> {'id': 1, 'tags': ['a']}\n```\n\nIf `tags` is missing, treat it as empty.",
                    "hint": "`{**record}` copies one level; the list inside still needs its own copy.",
                    "explanation": "`{**record}` is a shallow copy, so `new['tags']` would be the *same* list object. Building `[*record.get('tags', []), tag]` gives the new dict its own list.",
                    "xp": 40,
                    "config": {"language": "python", "starter": "def with_tag(record, tag):\n    ...\n"},
                    "solution": {
                        "entrypoint": "with_tag",
                        "cases": [
                            {"args": [{"id": 1, "tags": ["a"]}, "b"], "expect": {"id": 1, "tags": ["a", "b"]}},
                            {"args": [{"id": 2}, "x"], "expect": {"id": 2, "tags": ["x"]}},
                            {"args": [{"tags": []}, "z"], "expect": {"tags": ["z"]}},
                        ],
                    },
                },
            ],
        },
        {
            "index": 3,
            "title": "Testing and debugging like a pro",
            "summary": "Reproduce, bisect, assert. Stop reading code hoping to spot it.",
            "xp_reward": 100,
            "lessons": [
                {
                    "title": "The debugging loop",
                    "minutes": 6,
                    "body": """Staring at code is the slowest debugging technique. Use the loop:

1. **Reproduce** it deterministically. A bug you can't trigger on demand can't be verified as fixed.
2. **Shrink** the input until it is tiny. Half the time the shrunk case reveals the cause outright.
3. **Bisect** the space, not the lines: which commit (`git bisect`), which layer, which of the two halves of the data.
4. **Form one hypothesis**, and design the cheapest observation that would *disprove* it.
5. **Fix, then write the failing test first** so the bug can't come back.

The discipline is step 4. "Let me add some prints and see" is fine; "let me change three things and rerun" is how you end up with two bugs.

A binary search over a 2,000-line change takes 11 steps. Reading it takes an afternoon.""",
                },
                {
                    "title": "What a good test asserts",
                    "minutes": 5,
                    "body": """A test is a claim about behaviour, not a transcript of implementation.

```python
# brittle: breaks when you rename an internal helper
def test_checkout():
    assert cart._compute_lines.call_count == 2

# durable: states the promise
def test_checkout_applies_percentage_discount():
    cart = Cart([Item("book", Decimal("10.00"))])
    assert cart.total(discount_percent=10) == Decimal("9.00")
```

Cover these four before anything else:

- the **happy path**
- the **boundary** (0, 1, empty, max)
- the **error** case (what does it raise?)
- the **regression** (the exact input from the bug report)

Coverage percentage is a weak signal. "Would this suite catch the bug we shipped last month?" is a strong one.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "First move on a new bug",
                    "prompt": "A user reports intermittent wrong totals in production. You have logs and a staging environment.\n\nWhat is the highest-value first step?",
                    "hint": "You cannot verify a fix for something you cannot trigger.",
                    "explanation": "Deterministic reproduction comes first: it makes every later step (shrinking, bisecting, verifying the fix) possible. Everything else is guessing.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "Read the checkout module carefully looking for the mistake",
                            "Find a deterministic reproduction, even a slow one",
                            "Add defensive rounding to the total calculation",
                            "Roll back the last deploy",
                        ]
                    },
                    "solution": {"answer": 1},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Cases worth testing",
                    "prompt": "You just wrote `split_evenly(total, n)` which divides money across n people. Which cases belong in the first test?",
                    "hint": "Happy path, boundary, error, regression.",
                    "explanation": "The boundary (n = 1), the error (n = 0), and the case that exposes rounding (10 / 3) are exactly where the bugs live. Timing is not a correctness test.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "n = 1",
                            "n = 0",
                            "total = 10, n = 3 (does not divide evenly)",
                            "It runs in under 1 millisecond",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2]},
                },
                {
                    "kind": "short",
                    "difficulty": "medium",
                    "title": "Bisect the history",
                    "prompt": "A regression appeared somewhere in the last 1,024 commits and you have a script that answers good/bad.\n\nAt most how many builds do you need with `git bisect`?",
                    "hint": "Binary search over 1024.",
                    "explanation": "Each build halves the range: log2(1024) = 10. That is why a good/bad script is worth writing even when it takes twenty minutes.",
                    "xp": 25,
                    "config": {"placeholder": "a number"},
                    "solution": {"regex": True, "accept": [r"10", r"ten"]},
                },
                {
                    "kind": "code",
                    "difficulty": "hard",
                    "title": "Split money without losing a cent",
                    "prompt": "Write `split_evenly(total_cents, n)` that divides an integer number of cents across `n` people.\n\n- every share differs by at most 1 cent\n- the shares sum exactly to `total_cents`\n- larger shares come first\n- `n <= 0` returns `[]`\n\n```\nsplit_evenly(1000, 3) -> [334, 333, 333]\n```",
                    "hint": "Integer-divide, then hand the remainder out one cent at a time.",
                    "explanation": "`q, r = divmod(total, n)` then give the first `r` people `q + 1`. This is the standard way to avoid the floating-point rounding that quietly loses cents at scale.",
                    "xp": 45,
                    "config": {"language": "python", "starter": "def split_evenly(total_cents, n):\n    ...\n"},
                    "solution": {
                        "entrypoint": "split_evenly",
                        "cases": [
                            {"args": [1000, 3], "expect": [334, 333, 333]},
                            {"args": [10, 5], "expect": [2, 2, 2, 2, 2]},
                            {"args": [7, 2], "expect": [4, 3]},
                            {"args": [5, 0], "expect": []},
                            {"args": [0, 3], "expect": [0, 0, 0]},
                            {"args": [100, 7], "expect": [15, 15, 14, 14, 14, 14, 14], "hidden": True},
                        ],
                    },
                },
            ],
        },
    ],
}
