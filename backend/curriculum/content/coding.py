TRACK = {
    "slug": "coding",
    "name": "Coding Foundations",
    "tagline": "From absolute zero to writing clean, reliable code with confidence.",
    "description": (
        "No prior experience assumed. Learn variables, data types, logic, loops, collections, "
        "functions, and error handling. Progress step-by-step with real code execution."
    ),
    "icon": "{}",
    "accent": "#7c5cff",
    "order": 1,
    "required_xp": 0,
    "levels": [
        # =========================================================================
        # LEVEL 1: ABSOLUTE ZERO - VARIABLES, TYPES & EXPRESSIONS
        # =========================================================================
        {
            "index": 1,
            "title": "Absolute Zero: Variables, Types & Math",
            "summary": "What is code, how Python evaluates expressions, variables as labels, and core types.",
            "xp_reward": 80,
            "lessons": [
                {
                    "title": "What is Code & How Python Thinks",
                    "minutes": 5,
                    "body": """Computers are fundamentally simple: they execute instructions one by one, from top to bottom, without guessing or assuming anything.

### What is a Variable?
A variable is simply a **named label** that points to a piece of data stored in memory. Think of it like putting a sticky note on a box:

```python
score = 100
player_name = "Alex"
```

Here:
- `score` is the variable name.
- `=` is the **assignment operator** (it means *"store the value on the right into the name on the left"*).
- `100` is the value being stored.

> [!NOTE]
> `=` does **not** mean "equal to" in Python (that's `==`). It means **assign**.

### Rules for Variable Names
1. Names can contain letters, numbers, and underscores (`_`).
2. Names **cannot start with a number** (`1st_place` is invalid, `first_place` is valid).
3. Python convention is **snake_case** for variables: all lowercase with underscores between words (`user_age`, `total_price`).
4. Python is **case-sensitive**: `score`, `Score`, and `SCORE` are three completely different variables.""",
                },
                {
                    "title": "The 4 Core Data Types",
                    "minutes": 6,
                    "body": """Every piece of data in Python has a **type**. Python automatically determines the type based on what you assign:

| Type Name | What it represents | Examples |
| :--- | :--- | :--- |
| `int` | Whole integers (positive or negative) | `42`, `-7`, `0` |
| `float` | Numbers with a decimal point | `3.14`, `-0.5`, `2.0` |
| `str` | Text (strings of characters inside quotes) | `"hello"`, `'python'` |
| `bool` | Logical truth values (only two exist) | `True`, `False` |

### Checking Types with `type()`
You can inspect the type of any value using Python's built-in `type()` function:

```python
x = 25
print(type(x))  # <class 'int'>

y = "25"
print(type(y))  # <class 'str'> (notice quotes make it text!)
```

### Type Conversion (Casting)
You can convert values from one type to another using `int()`, `float()`, and `str()`:

```python
age_text = "25"
age_num = int(age_text)  # Converts string "25" into integer 25
price = float("19.99")    # Converts string "19.99" into float 19.99
```""",
                },
                {
                    "title": "Basic Math and Modern F-Strings",
                    "minutes": 5,
                    "body": """Python can act like a calculator using standard arithmetic operators:

```python
a = 10
b = 3

a + b   # Addition: 13
a - b   # Subtraction: 7
a * b   # Multiplication: 30
a / b   # Normal division: 3.3333333333333335 (always returns a float)
a // b  # Floor division: 3 (discards the fractional part)
a % b   # Modulo (remainder): 1 (10 divided by 3 has remainder 1)
a ** b  # Exponentiation: 10^3 = 1000
```

### Formatted Strings (f-strings)
To combine text with variables, modern Python uses **f-strings** (prefix the string with `f` and put variables inside `{}`):

```python
name = "Lavid"
level = 1
message = f"Welcome {name}, you are currently at Level {level}!"
print(message)
# "Welcome Lavid, you are currently at Level 1!"
```

f-strings can also evaluate math directly inside `{}`:

```python
item_price = 20
tax = 0.1
print(f"Total: ${item_price * (1 + tax):.2f}")  # Total: $22.00
```""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Integer Division vs Modulo",
                    "prompt": "What does the expression `14 % 4` evaluate to in Python?",
                    "hint": "The `%` operator computes the remainder after division.",
                    "explanation": "14 divided by 4 is 3 with a remainder of 2 (4 * 3 + 2 = 14). So `14 % 4` is `2`.",
                    "xp": 20,
                    "config": {"options": ["3.5", "3", "2", "0"]},
                    "solution": {"answer": 2},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "String Type Identification",
                    "prompt": "In Python, what is the exact name of the built-in type for text enclosed in quotes (e.g. `\"hello\"`)?",
                    "hint": "Three letters, lowercase.",
                    "explanation": "The type is `str`.",
                    "xp": 15,
                    "solution": {"accept": ["str", "'str'", "str()"], "ignore_case": True},
                },
                {
                    "kind": "code",
                    "difficulty": "easy",
                    "title": "Your First Function: Add Two Numbers",
                    "prompt": "Write a function `add(a, b)` that takes two numbers and returns their sum.\n\n```python\nadd(3, 5) -> 8\nadd(-2, 7) -> 5\n```",
                    "hint": "Use the `return` statement with the `+` operator: `return a + b`",
                    "explanation": "Functions use `def function_name(args):` and return data to the caller using `return`.",
                    "xp": 25,
                    "config": {
                        "language": "python",
                        "starter": "def add(a, b):\n    # Return the sum of a and b\n    return ...\n",
                    },
                    "solution": {
                        "entrypoint": "add",
                        "cases": [
                            {"args": [3, 5], "expect": 8},
                            {"args": [-2, 7], "expect": 5},
                            {"args": [0, 0], "expect": 0},
                            {"args": [100, 250], "expect": 350},
                            {"args": [12345, 67890], "expect": 80235, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "easy",
                    "title": "Formatted Greeting",
                    "prompt": "Write a function `greet(name)` that takes a string `name` and returns a personalized greeting string in the format:\n`\"Hello, <name>!\"`\n\n```python\ngreet(\"Lavid\") -> \"Hello, Lavid!\"\ngreet(\"World\") -> \"Hello, World!\"\n```",
                    "hint": "Use an f-string: `return f\"Hello, {name}!\"`",
                    "explanation": "f-strings `f\"Hello, {name}!\"` cleanly insert variables into strings.",
                    "xp": 25,
                    "config": {
                        "language": "python",
                        "starter": "def greet(name):\n    # Return formatted greeting\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "greet",
                        "cases": [
                            {"args": ["Lavid"], "expect": "Hello, Lavid!"},
                            {"args": ["World"], "expect": "Hello, World!"},
                            {"args": ["Python"], "expect": "Hello, Python!"},
                            {"args": ["Engineer"], "expect": "Hello, Engineer!", "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 2: MAKING DECISIONS - CONDITIONALS AND LOGIC
        # =========================================================================
        {
            "index": 2,
            "title": "Making Decisions: Conditionals & Logic",
            "summary": "Boolean operators, comparison checks, if/elif/else branching, and guard clauses.",
            "xp_reward": 90,
            "lessons": [
                {
                    "title": "Comparison Operators and Boolean Logic",
                    "minutes": 6,
                    "body": """In programming, you often need to branch based on questions: *Is the user logged in? Is the score above 100?*

### Comparison Operators
Comparisons always evaluate to either `True` or `False`:

```python
x = 10
x == 10  # True  (Equality: note the double equals!)
x != 5   # True  (Not equal)
x > 20   # False (Greater than)
x < 15   # True  (Less than)
x >= 10  # True  (Greater than or equal)
x <= 9   # False (Less than or equal)
```

### Combining Conditions with `and`, `or`, `not`
- **`and`**: Returns `True` only if **both** sides are `True`.
- **`or`**: Returns `True` if **at least one** side is `True`.
- **`not`**: Inverts the boolean (`not True` is `False`).

```python
age = 22
has_license = True

can_drive = age >= 18 and has_license  # True
is_minor = not (age >= 18)             # False
```""",
                },
                {
                    "title": "If, Elif, Else Branching",
                    "minutes": 6,
                    "body": """Conditional statements allow your program to take different paths depending on conditions:

```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
```

### How Python Evaluates Branches:
1. It tests conditions from top to bottom.
2. The **first** branch whose condition is `True` executes.
3. Once a branch executes, all subsequent `elif` and `else` blocks are **completely skipped**.
4. If none of the `if` or `elif` conditions match, the `else` block runs as the default fallback.

### Indentation Matters!
In Python, indentation (typically 4 spaces) defines the code block. Misaligned indentation causes an `IndentationError`.""",
                },
                {
                    "title": "Guard Clauses Beat Deep Nesting",
                    "minutes": 5,
                    "body": """When writing functions, deeply nested `if` statements make code difficult to read:

```python
# Deeply nested anti-pattern (Hard to follow):
def check_admission(age, paid):
    if age >= 18:
        if paid:
            return "Admitted"
        else:
            return "Payment required"
    else:
        return "Must be 18"
```

### The Clean Approach: Guard Clauses (Early Returns)
Check for invalid or edge cases first, return immediately, and keep the happy path flat:

```python
# Clean, readable code:
def check_admission(age, paid):
    if age < 18:
        return "Must be 18"
    if not paid:
        return "Payment required"
    return "Admitted"
```

Both functions do the exact same thing, but the guard clause version eliminates nested indentations and places failure conditions up front.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Evaluating Truthiness",
                    "prompt": "In Python, which of the following values evaluates to `False` in an `if` condition (falsy)?",
                    "hint": "Empty containers and zero are falsy.",
                    "explanation": "In Python, `0`, `\"\"` (empty string), `[]` (empty list), `{}` (empty dict), `None`, and `False` are all falsy.",
                    "xp": 20,
                    "config": {"options": ["1", "\"False\"", "[]", "[0]"]},
                    "solution": {"answer": 2},
                },
                {
                    "kind": "multi",
                    "difficulty": "easy",
                    "title": "Valid Comparison Operators",
                    "prompt": "Which of these are valid Python comparison operators?",
                    "hint": "Check equality vs assignment.",
                    "explanation": "`==`, `!=`, and `>=` are comparison operators. Single `=` is variable assignment.",
                    "xp": 20,
                    "config": {"options": ["==", "!=", "=", ">="]},
                    "solution": {"answers": [0, 1, 3]},
                },
                {
                    "kind": "code",
                    "difficulty": "easy",
                    "title": "Check Even or Odd",
                    "prompt": "Write a function `is_even(n)` that returns `True` if the integer `n` is even, and `False` if it is odd.\n\n```python\nis_even(4) -> True\nis_even(7) -> False\nis_even(0) -> True\n```",
                    "hint": "Use the modulo operator `%`. An even number divided by 2 has remainder 0: `n % 2 == 0`.",
                    "explanation": "Any number where `n % 2 == 0` is divisible by 2 with no remainder, making it even.",
                    "xp": 30,
                    "config": {
                        "language": "python",
                        "starter": "def is_even(n):\n    # Return True if n is even, False otherwise\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "is_even",
                        "cases": [
                            {"args": [4], "expect": True},
                            {"args": [7], "expect": False},
                            {"args": [0], "expect": True},
                            {"args": [-2], "expect": True},
                            {"args": [-5], "expect": False},
                            {"args": [1000002], "expect": True, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "easy",
                    "title": "Value Clamp",
                    "prompt": "Write a function `clamp(val, low, high)` that restricts `val` to be within the range `[low, high]`:\n- If `val < low`, return `low`.\n- If `val > high`, return `high`.\n- Otherwise, return `val`.\n\n```python\nclamp(5, 1, 10)  -> 5\nclamp(-3, 0, 10) -> 0\nclamp(15, 0, 10) -> 10\n```",
                    "hint": "Use simple `if / elif / else` or guard clauses.",
                    "explanation": "Clamping is a standard utility function in games, graphics, and data normalization.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def clamp(val, low, high):\n    # Restrict val between low and high\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "clamp",
                        "cases": [
                            {"args": [5, 1, 10], "expect": 5},
                            {"args": [-3, 0, 10], "expect": 0},
                            {"args": [15, 0, 10], "expect": 10},
                            {"args": [10, 0, 10], "expect": 10},
                            {"args": [0, 0, 10], "expect": 0},
                            {"args": [42, 50, 100], "expect": 50, "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 3: REPETITION - LOOPS AND ITERATION
        # =========================================================================
        {
            "index": 3,
            "title": "Repetition: Loops and Iteration",
            "summary": "For loops, while loops, range generation, break/continue, and accumulators.",
            "xp_reward": 100,
            "lessons": [
                {
                    "title": "For Loops and the range() Function",
                    "minutes": 6,
                    "body": """Loops allow you to repeat a block of code multiple times without copy-pasting.

### The `for` Loop
A `for` loop iterates over a sequence (like numbers or items in a list):

```python
for item in ["apple", "banana", "cherry"]:
    print(item)
```

### The `range()` Generator
When you want to repeat code a specific number of times, use `range()`:

- `range(5)` generates numbers `0, 1, 2, 3, 4` (starts at 0, stops **before** 5).
- `range(1, 6)` generates numbers `1, 2, 3, 4, 5` (from start up to stop-1).
- `range(0, 10, 2)` generates `0, 2, 4, 6, 8` (starts at 0, steps by 2).

```python
# Print numbers 1 to 5
for i in range(1, 6):
    print(i)
```

> [!IMPORTANT]
> The stop index is always **exclusive**. `range(0, 5)` loops 5 times: 0, 1, 2, 3, 4. Forgetting this causes the infamous **off-by-one bug**.""",
                },
                {
                    "title": "While Loops and Loop Control",
                    "minutes": 6,
                    "body": """### While Loops
A `while` loop continues running as long as its condition remains `True`:

```python
count = 3
while count > 0:
    print(count)
    count -= 1  # Decrement count so the loop eventually terminates
print("Blastoff!")
```

> [!CAUTION]
> If you forget to update the variable inside the loop, the condition may stay `True` forever, creating an **infinite loop** that hangs your program!

### Loop Control: `break` and `continue`
- **`break`**: Immediately exits the loop entirely.
- **`continue`**: Skips the rest of the current iteration and jumps directly to the next iteration.

```python
for n in range(1, 10):
    if n == 5:
        break  # Stops the loop when n reaches 5
    if n % 2 == 0:
        continue  # Skips even numbers
    print(n)  # Prints: 1, 3
```""",
                },
                {
                    "title": "The Accumulator Pattern",
                    "minutes": 5,
                    "body": """One of the most common programming patterns is the **Accumulator Pattern**:
1. Initialize a variable outside the loop (e.g. `total = 0` or `result = []`).
2. Loop over your data.
3. Update the accumulator on each iteration.
4. Return or use the accumulated result after the loop finishes.

```python
def sum_numbers(numbers):
    total = 0  # 1. Initialize
    for num in numbers:  # 2. Iterate
        total += num  # 3. Accumulate (same as total = total + num)
    return total  # 4. Final result
```""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Range Generation Output",
                    "prompt": "What values does `list(range(2, 6))` produce in Python?",
                    "hint": "Starts at the first argument and stops strictly before the second argument.",
                    "explanation": "`range(2, 6)` starts at 2 and stops before 6, producing `[2, 3, 4, 5]`.",
                    "xp": 20,
                    "config": {"options": ["[2, 3, 4, 5, 6]", "[2, 3, 4, 5]", "[1, 2, 3, 4, 5]", "[2, 4, 6]"]},
                    "solution": {"answer": 1},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Skipping Loop Iteration",
                    "prompt": "What Python keyword is used inside a loop to skip the rest of the current iteration and move to the next one?",
                    "hint": "Begins with letter 'c'.",
                    "explanation": "`continue` skips the rest of the current loop iteration.",
                    "xp": 15,
                    "solution": {"accept": ["continue"], "ignore_case": True},
                },
                {
                    "kind": "code",
                    "difficulty": "easy",
                    "title": "Sum from 1 to N",
                    "prompt": "Write a function `sum_to_n(n)` that returns the sum of all integers from 1 up to and including `n`.\n\n```python\nsum_to_n(3) -> 1 + 2 + 3 = 6\nsum_to_n(5) -> 1 + 2 + 3 + 4 + 5 = 15\nsum_to_n(1) -> 1\n```",
                    "hint": "Use an accumulator variable starting at 0, and loop `for i in range(1, n + 1):` adding `i` to your total.",
                    "explanation": "Looping through `range(1, n + 1)` and accumulating sum is the classic accumulator pattern.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def sum_to_n(n):\n    # Return sum of integers from 1 to n\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "sum_to_n",
                        "cases": [
                            {"args": [3], "expect": 6},
                            {"args": [5], "expect": 15},
                            {"args": [1], "expect": 1},
                            {"args": [10], "expect": 55},
                            {"args": [100], "expect": 5050, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "easy",
                    "title": "Count Matching Occurrences",
                    "prompt": "Write a function `count_occurrences(items, target)` that loops through the list `items` and counts how many times `target` appears.\n\n```python\ncount_occurrences([1, 2, 3, 2, 2], 2) -> 3\ncount_occurrences([\"a\", \"b\", \"a\"], \"a\") -> 2\ncount_occurrences([1, 2, 3], 99) -> 0\n```",
                    "hint": "Start a count at 0. Loop `for x in items:`, if `x == target: count += 1`. Return count.",
                    "explanation": "Linear counting loop tests equality against each item.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def count_occurrences(items, target):\n    # Count how many times target appears in items\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "count_occurrences",
                        "cases": [
                            {"args": [[1, 2, 3, 2, 2], 2], "expect": 3},
                            {"args": [["a", "b", "a"], "a"], "expect": 2},
                            {"args": [[1, 2, 3], 99], "expect": 0},
                            {"args": [[], 5], "expect": 0},
                            {"args": [[7, 7, 7, 7, 7], 7], "expect": 5, "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 4: CORE COLLECTIONS - LISTS, TUPLES, SETS, AND DICTIONARIES
        # =========================================================================
        {
            "index": 4,
            "title": "Collections: Lists, Tuples, Sets & Dicts",
            "summary": "Sequences, key-value mappings, set theory, and container lookup performance.",
            "xp_reward": 100,
            "lessons": [
                {
                    "title": "Lists vs Tuples: Indexing and Slicing",
                    "minutes": 6,
                    "body": """Collections hold multiple items together in a single structure.

### Lists (`list`)
Lists are ordered, zero-indexed, and **mutable** (can be modified in-place):

```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")      # Add to end: ["apple", "banana", "cherry", "date"]
fruits[0]                  # "apple" (First item)
fruits[-1]                 # "date" (Last item)
fruits[1:3]                # ["banana", "cherry"] (Slice from index 1 up to 3)
```

### Tuples (`tuple`)
Tuples look like lists with parentheses `(1, 2)`, but they are **immutable** (cannot be changed after creation):

```python
point = (10, 20)
# point[0] = 15  --> TypeError: 'tuple' object does not support item assignment
```

Use tuples when representing a fixed record (like coordinates `(lat, lon)` or RGB colors `(255, 0, 0)`).""",
                },
                {
                    "title": "Dictionaries: Instant Key-Value Lookups",
                    "minutes": 6,
                    "body": """A dictionary (`dict`) maps unique **keys** to **values**, like a real dictionary maps words to definitions:

```python
user = {
    "username": "lavid",
    "level": 4,
    "is_active": True,
}

# Accessing values
print(user["username"])  # "lavid"

# Safe access with default fallback using .get()
score = user.get("score", 0)  # Returns 0 instead of crashing if "score" doesn't exist!

# Adding or updating keys
user["level"] = 5
user["email"] = "lavid@dev.com"

# Iterating over key-value pairs
for key, value in user.items():
    print(f"{key} => {value}")
```

Dictionaries provide average **O(1) instant lookup time** by hashing keys.""",
                },
                {
                    "title": "Sets & Fast Membership: The O(1) Rule",
                    "minutes": 6,
                    "body": """A `set` is an unordered collection of **unique elements**:

```python
numbers = {1, 2, 3, 3, 2, 1}
print(numbers)  # {1, 2, 3} (Duplicates are automatically removed!)
```

### The Cardinal Performance Rule: List vs Set Lookups
When checking if an item exists with `if item in collection`:

| Collection | Lookup Speed | Why |
| :--- | :--- | :--- |
| `list` | **O(n) Linear Scan** | Python must check every element one by one from start to end. |
| `set` | **O(1) Instant Hash** | Python computes the hash of the element and jumps directly to its memory slot. |

```python
# Slow: O(n^2) on 100,000 items
seen = []
for x in large_list:
    if x not in seen:  # Scans seen list every time!
        seen.append(x)

# Fast: O(n) linear overall
seen = set()
for x in large_list:
    if x not in seen:  # Instant O(1) hash check!
        seen.add(x)
```""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Fast Membership Lookup",
                    "prompt": "You are checking `if user_id in collection` inside a loop that runs 500,000 times.\n\nWhich container keeps the lookup O(1) instead of scanning element by element?",
                    "hint": "Think about hash-based collections.",
                    "explanation": "`set` and `dict` use hash tables for O(1) constant-time lookups. `list` and `tuple` require an O(n) sequential scan.",
                    "xp": 20,
                    "config": {"options": ["list", "tuple", "set", "deque"]},
                    "solution": {"answer": 2},
                },
                {
                    "kind": "multi",
                    "difficulty": "easy",
                    "title": "Mutable Containers",
                    "prompt": "Which of the following Python data structures can be modified in-place (are mutable)?",
                    "hint": "Tuples and strings cannot be changed after creation.",
                    "explanation": "`list`, `dict`, and `set` are mutable. `tuple` and `str` are immutable.",
                    "xp": 25,
                    "config": {"options": ["list", "tuple", "dict", "set"]},
                    "solution": {"answers": [0, 2, 3]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Deduplicate Preserving First-Seen Order",
                    "prompt": "Write `dedupe(items)` returning a new list with duplicate elements removed, **preserving first-seen order**.\n\nMust run in O(n) time, so do not check `in` against a list.\n\n```python\ndedupe([3, 1, 3, 2, 1]) -> [3, 1, 2]\ndedupe([\"a\", \"b\", \"a\"]) -> [\"a\", \"b\"]\n```",
                    "hint": "Maintain a `seen = set()` for O(1) membership checks, and an `out = []` list to preserve insertion order.",
                    "explanation": "Combining a `set` for lookup with a `list` for ordered output is the canonical O(n) deduplication pattern.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def dedupe(items):\n    # Deduplicate preserving order\n    seen = set()\n    out = []\n    ...\n",
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
                    "difficulty": "easy",
                    "title": "Character Frequency Counter",
                    "prompt": "Write a function `char_counts(text)` that takes a string `text` and returns a dictionary with the count of each character.\n\n```python\nchar_counts(\"aba\") -> {\"a\": 2, \"b\": 1}\nchar_counts(\"\") -> {}\n```",
                    "hint": "Loop `for char in text:`. You can use `counts[char] = counts.get(char, 0) + 1`.",
                    "explanation": "Using a dictionary accumulator with `dict.get(key, 0)` is the fundamental counting pattern in Python.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def char_counts(text):\n    counts = {}\n    # Count character frequencies\n    ...\n    return counts\n",
                    },
                    "solution": {
                        "entrypoint": "char_counts",
                        "cases": [
                            {"args": ["aba"], "expect": {"a": 2, "b": 1}},
                            {"args": [""], "expect": {}},
                            {"args": ["hello"], "expect": {"h": 1, "e": 1, "l": 2, "o": 1}},
                            {"args": ["mississippi"], "expect": {"m": 1, "i": 4, "s": 4, "p": 2}, "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 5: FUNCTIONS, SCOPES, AND DEFENSIVE CODING
        # =========================================================================
        {
            "index": 5,
            "title": "Functions, Contracts & Error Handling",
            "summary": "Function signatures, scope, default argument traps, exceptions, and try/except/finally.",
            "xp_reward": 110,
            "lessons": [
                {
                    "title": "Parameters, Defaults, and The Mutable Trap",
                    "minutes": 6,
                    "body": """Functions let you package logic into reusable building blocks.

### Default Arguments
You can assign default values to parameters:

```python
def greet(name, title="Engineer"):
    return f"Welcome, {title} {name}!"

greet("Lavid")               # "Welcome, Engineer Lavid!"
greet("Lavid", title="Lead") # "Welcome, Lead Lavid!"
```

### The Infamous Mutable Default Argument Trap
In Python, default arguments are evaluated **once when the function is defined**, not every time it is called:

```python
# BUG: The list is shared across every call to the function!
def add_item(item, basket=[]):
    basket.append(item)
    return basket

print(add_item("apple"))  # ["apple"]
print(add_item("banana")) # ["apple", "banana"] (Unexpectedly shared!)
```

### The Proper Python Pattern:
Always use `None` as the default for mutable containers:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```""",
                },
                {
                    "title": "Exceptions & Honest Failure",
                    "minutes": 6,
                    "body": """Errors happen in software: files are missing, network requests timeout, or users pass invalid input. Python uses **exceptions** to signal errors.

### The `try / except` Block
Instead of letting an error crash your entire program, you can catch and handle it:

```python
try:
    number = int(input_text)
    result = 100 / number
except ValueError:
    print("Invalid format: input must be numeric!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

### Never Use a Bare `except:`
```python
# DANGEROUS ANTI-PATTERN:
try:
    do_something()
except:
    pass  # Silently hides syntax errors, typos, and even Ctrl+C interrupts!
```

Always catch the **specific exception type** you expect (`ValueError`, `KeyError`, `FileNotFoundError`). Catching generic errors hides bugs that take hours to track down.""",
                },
                {
                    "title": "Raising Exceptions and Enforcing Contracts",
                    "minutes": 5,
                    "body": """When your function receives invalid input, do not silently fail or return a meaningless value. **Raise an explicit exception**:

```python
def calculate_tax(income, rate):
    if income < 0:
        raise ValueError("Income cannot be negative")
    if not (0 <= rate <= 1):
        raise ValueError("Rate must be between 0.0 and 1.0")
    return income * rate
```

Explicit errors protect caller code from silently corrupting state downstream. As the Zen of Python states:
> *"Errors should never pass silently. Unless explicitly silenced."*""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Mutable Default Argument Behavior",
                    "prompt": "What happens if you define `def collect(val, items=[]): items.append(val); return items` and call `collect(1)` followed by `collect(2)`?",
                    "hint": "Default parameters are created once at definition time.",
                    "explanation": "The default list is created once and reused across all function calls, returning `[1, 2]` on the second call.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "Both calls return `[1]` and `[2]` independently",
                            "The second call returns `[1, 2]` because the list is shared",
                            "Python throws a SyntaxError at definition time",
                            "The function crashes on the second call with an AttributeError",
                        ]
                    },
                    "solution": {"answer": 1},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Triggering Exceptions",
                    "prompt": "What Python keyword is used to intentionally trigger an exception (e.g. `_____ ValueError(\"invalid\")`)?",
                    "hint": "Five letters, starts with 'r'.",
                    "explanation": "The `raise` statement raises an exception.",
                    "xp": 15,
                    "solution": {"accept": ["raise"], "ignore_case": True},
                },
                {
                    "kind": "code",
                    "difficulty": "easy",
                    "title": "Safe Division with Fallback",
                    "prompt": "Write a function `safe_divide(a, b, default=0)` that returns `a / b`.\nIf `b == 0`, it should return `default` instead of crashing with a `ZeroDivisionError`.\n\n```python\nsafe_divide(10, 2) -> 5.0\nsafe_divide(10, 0) -> 0\nsafe_divide(10, 0, default=-1) -> -1\n```",
                    "hint": "Use a guard clause `if b == 0: return default` or a `try/except ZeroDivisionError` block.",
                    "explanation": "Guard clauses or catching `ZeroDivisionError` protects against arithmetic failure.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def safe_divide(a, b, default=0):\n    # Return a / b or default if b is 0\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "safe_divide",
                        "cases": [
                            {"args": [10, 2], "expect": 5.0},
                            {"args": [10, 0], "expect": 0},
                            {"args": [10, 0, -1], "expect": -1},
                            {"args": [0, 5], "expect": 0.0},
                            {"args": [100, 4], "expect": 25.0, "hidden": True},
                        ],
                    },
                },
                {
                    "kind": "code",
                    "difficulty": "easy",
                    "title": "Safe Integer Parsing",
                    "prompt": "Write a function `parse_int(text, fallback=0)` that attempts to convert `text` into an integer using `int(text)`.\nIf conversion fails (e.g. for text like `\"invalid\"` or `\"3.14\"`), return `fallback`.\n\n```python\nparse_int(\"42\") -> 42\nparse_int(\"abc\") -> 0\nparse_int(\"abc\", fallback=-1) -> -1\n```",
                    "hint": "Use `try: return int(text) except ValueError: return fallback`.",
                    "explanation": "Handling `ValueError` gracefully is the textbook pattern for user input sanitization.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def parse_int(text, fallback=0):\n    # Safely convert text to int or return fallback\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "parse_int",
                        "cases": [
                            {"args": ["42"], "expect": 42},
                            {"args": ["abc"], "expect": 0},
                            {"args": ["abc", -1], "expect": -1},
                            {"args": ["-15"], "expect": -15},
                            {"args": ["", 99], "expect": 99, "hidden": True},
                        ],
                    },
                },
            ],
        },
    ],
}
