TRACK = {
    "slug": "databases",
    "name": "Database Design",
    "tagline": "How databases actually store, index, query, and protect your data.",
    "description": (
        "Start from absolute zero. Learn why relational databases exist, master SQL queries and joins, "
        "understand B-Tree indexes, and protect data integrity with transactions and ACID."
    ),
    "icon": "⊞",
    "accent": "#f5a623",
    "order": 4,
    "required_xp": 750,
    "levels": [
        # =========================================================================
        # LEVEL 1: DATABASES FROM ZERO & SCHEMAS
        # =========================================================================
        {
            "index": 1,
            "title": "Databases from Zero: Relational Thinking & Schemas",
            "summary": "Why spreadsheets and flat files fail, tables, columns, data types, and primary keys.",
            "xp_reward": 85,
            "lessons": [
                {
                    "title": "Why Databases? Moving Beyond Spreadsheets & Files",
                    "minutes": 6,
                    "body": """When starting out, it's tempting to store data in a JSON file or an Excel spreadsheet. Here is why production systems cannot do that:

1. **Concurrent Writes**: What happens when two users click "Buy" at the exact same millisecond? In a flat file, one write overwrites the other, corrupting data.
2. **Crash Resilience**: If power cuts out mid-save, a flat file is left corrupted and unreadable. Databases use Write-Ahead Logs (WAL) to guarantee zero corruption.
3. **Query Scale**: To find one user in a 10-million line JSON file, you must load all 5 gigabytes into RAM and scan every line. A database uses indexes to find the row in 0.2 milliseconds!

### The Relational Model
A relational database (like PostgreSQL) organizes data into **Tables**:
- Each **Table** represents an entity (e.g. `users`, `orders`).
- Each **Row** (or record) represents a single instance of that entity.
- Each **Column** represents a specific attribute with a rigid data type.""",
                },
                {
                    "title": "Data Types & The Golden Primary Key Rule",
                    "minutes": 6,
                    "body": """Every column in a relational table has an enforced data type:

| Type | When to use | Example |
| :--- | :--- | :--- |
| `INTEGER` / `BIGINT` | Counters, quantities, numerical IDs | `42` |
| `VARCHAR(n)` | Short text with a reasonable limit | `"alice@example.com"` |
| `TEXT` | Long text of unpredictable size | Product description, comments |
| `BOOLEAN` | Binary flags | `true` / `false` |
| `TIMESTAMP WITH TIME ZONE` | Exact point in universal time | `2026-09-08 14:30:00Z` |

### Primary Keys: The Identity of a Row
Every table must have a **Primary Key (PK)**:
- It **uniquely identifies** every row in the table.
- It can **never be NULL**.
- It should **never change** over the life of the record.

Most tables use an auto-incrementing integer (`SERIAL` / `BIGSERIAL`) or a `UUID`.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Primary Key Invariant",
                    "prompt": "What are the two mandatory properties of any Primary Key in a relational database?",
                    "hint": "Can two rows share a primary key? Can a primary key be empty?",
                    "explanation": "A primary key must be unique across all rows and cannot be NULL.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "Must be unique and cannot be NULL",
                            "Must be an alphabetical string and unique",
                            "Must be greater than 100",
                            "Must change whenever the row is updated",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Why Not Flat Files?",
                    "prompt": "Which of the following are major architectural risks when storing production data in flat CSV or JSON files?",
                    "hint": "Think about crashes, speed, and simultaneous users.",
                    "explanation": "Concurrent writes corrupt flat files, searching requires scanning the entire file, and power losses cause data loss.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "Concurrent writes by multiple threads can corrupt the file",
                            "Finding a single record requires reading the entire file from disk",
                            "JSON files take up too much color on monitors",
                            "No automatic rollback if a power failure occurs mid-write",
                        ]
                    },
                    "solution": {"answers": [0, 1, 3]},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Disallowing Null Values",
                    "prompt": "What SQL constraint keyword prevents a column from ever holding a NULL value?",
                    "hint": "Two words: NOT ...",
                    "explanation": "The `NOT NULL` constraint prevents null values from being inserted.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. NOT NULL"},
                    "solution": {"regex": True, "accept": [r"NOT\s+NULL", r"not\s+null"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Validate Row Against Schema",
                    "prompt": "Write `validate_row(row, schema)` that verifies whether a row dictionary matches expected column types.\n`schema` is a dict of `{col_name: type_name_str}` (e.g. `\"int\"`, `\"str\"`, `\"bool\"`).\n\nA row is valid (`True`) if:\n1. It contains all columns required by `schema`.\n2. Each value's type matches: `type(row[col]).__name__ == expected_type_str`.\nOtherwise return `False`.\n\n```python\nschema = {\"id\": \"int\", \"name\": \"str\"}\nvalidate_row({\"id\": 1, \"name\": \"Alex\"}, schema) -> True\nvalidate_row({\"id\": \"1\", \"name\": \"Alex\"}, schema) -> False\nvalidate_row({\"id\": 1}, schema) -> False\n```",
                    "hint": "Check `col in row and type(row[col]).__name__ == expected_type` for each column in schema.",
                    "explanation": "Schema validation enforces column types before persistence.",
                    "xp": 40,
                    "config": {
                        "language": "python",
                        "starter": "def validate_row(row, schema):\n    # Return True if row values match schema types\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "validate_row",
                        "cases": [
                            {"args": [{"id": 1, "name": "Alex"}, {"id": "int", "name": "str"}], "expect": True},
                            {"args": [{"id": "1", "name": "Alex"}, {"id": "int", "name": "str"}], "expect": False},
                            {"args": [{"id": 1}, {"id": "int", "name": "str"}], "expect": False},
                            {"args": [{"id": 10, "active": True}, {"id": "int", "active": "bool"}], "expect": True},
                            {"args": [{}, {"id": "int"}], "expect": False, "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 2: SQL FOUNDATIONS: QUERYING & AGGREGATIONS
        # =========================================================================
        {
            "index": 2,
            "title": "SQL Foundations: SELECT, Filtering & Aggregating",
            "summary": "Writing clean queries, WHERE operators, sorting, LIMIT/OFFSET, and GROUP BY aggregations.",
            "xp_reward": 95,
            "lessons": [
                {
                    "title": "The Anatomy of a SELECT Query",
                    "minutes": 6,
                    "body": """SQL (Structured Query Language) is declarative: you describe **what** data you want, and the database engine plans the fastest way to get it.

```sql
SELECT id, name, email, score
FROM users
WHERE score >= 100 AND active = true
ORDER BY score DESC
LIMIT 10 OFFSET 20;
```

### Order of SQL Execution
Although written starting with `SELECT`, the database executes queries in this order:
1. `FROM`: Which table to read
2. `WHERE`: Filter rows
3. `GROUP BY`: Aggregate into groups
4. `HAVING`: Filter grouped aggregates
5. `SELECT`: Pick which columns to return
6. `ORDER BY`: Sort the results
7. `LIMIT / OFFSET`: Take a slice""",
                },
                {
                    "title": "Aggregations & GROUP BY",
                    "minutes": 6,
                    "body": """Aggregate functions summarize multiple rows into a single scalar value:
- `COUNT(*)`: Total number of matching rows
- `SUM(column)`: Total sum of numeric values
- `AVG(column)`: Mean average
- `MIN(column)` / `MAX(column)`: Minimum and maximum

### Grouping Rows
To calculate metrics per category, use `GROUP BY`:

```sql
SELECT department, COUNT(*) as employee_count, AVG(salary) as avg_salary
FROM employees
GROUP BY department
HAVING AVG(salary) > 80000;
```

> [!IMPORTANT]
> - `WHERE` filters individual rows **before** aggregation.
> - `HAVING` filters groups **after** aggregation.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "WHERE vs HAVING",
                    "prompt": "What is the key difference between the WHERE clause and the HAVING clause in SQL?",
                    "hint": "When does grouping happen relative to each clause?",
                    "explanation": "WHERE filters raw individual rows before GROUP BY; HAVING filters the aggregated groups after grouping.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "WHERE filters rows before grouping; HAVING filters aggregated groups",
                            "HAVING filters rows before grouping; WHERE filters aggregated groups",
                            "WHERE can only be used with numbers; HAVING can only be used with strings",
                            "There is no difference; they are aliases",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "multi",
                    "difficulty": "easy",
                    "title": "Standard SQL Aggregate Functions",
                    "prompt": "Which of the following are built-in standard SQL aggregate functions?",
                    "hint": "Functions that collapse multiple rows into one value.",
                    "explanation": "COUNT, SUM, and AVG are aggregate functions. SORT is a clause (ORDER BY), not a function.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "COUNT()",
                            "SUM()",
                            "AVG()",
                            "SORT()",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2]},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "SQL Sorting Clause",
                    "prompt": "What two-word SQL clause is used to sort query results in ascending or descending order?",
                    "hint": "ORDER ...",
                    "explanation": "ORDER BY sorts the returned rows.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. ORDER BY"},
                    "solution": {"regex": True, "accept": [r"order\s+by", r"ORDER\s+BY"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Filter and Sort In-Memory Rows",
                    "prompt": "Write `filter_and_sort(records, min_score, sort_key)` that simulates a SQL query in Python:\n- Keep only records where `record[\"score\"] >= min_score`\n- Sort the remaining records in **descending** order of `record[sort_key]`\n- Return the sorted list of dicts\n\n```python\nrecords = [\n    {\"id\": 1, \"score\": 80},\n    {\"id\": 2, \"score\": 95},\n    {\"id\": 3, \"score\": 40}\n]\nfilter_and_sort(records, 50, \"score\")\n# -> [{\"id\": 2, \"score\": 95}, {\"id\": 1, \"score\": 80}]\n```",
                    "hint": "Filter using a list comprehension, then sort with `sorted(..., key=lambda r: r[sort_key], reverse=True)`.",
                    "explanation": "Filtering and sorting simulates the core behavior of WHERE and ORDER BY clauses.",
                    "xp": 40,
                    "config": {
                        "language": "python",
                        "starter": "def filter_and_sort(records, min_score, sort_key):\n    # Filter and sort records\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "filter_and_sort",
                        "cases": [
                            {
                                "args": [
                                    [{"id": 1, "score": 80}, {"id": 2, "score": 95}, {"id": 3, "score": 40}],
                                    50,
                                    "score",
                                ],
                                "expect": [{"id": 2, "score": 95}, {"id": 1, "score": 80}],
                            },
                            {
                                "args": [[{"id": 1, "score": 10}], 50, "score"],
                                "expect": [],
                            },
                            {
                                "args": [[{"id": 1, "score": 100}, {"id": 2, "score": 100}], 100, "id"],
                                "expect": [{"id": 2, "score": 100}, {"id": 1, "score": 100}],
                                "hidden": True,
                            },
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 3: RELATIONSHIPS, FOREIGN KEYS & JOINS
        # =========================================================================
        {
            "index": 3,
            "title": "Relationships, Foreign Keys & JOINs",
            "summary": "1-to-many, many-to-many junction tables, foreign keys, INNER JOIN, and LEFT JOIN.",
            "xp_reward": 105,
            "lessons": [
                {
                    "title": "Relational Modeling: 1-to-Many & Many-to-Many",
                    "minutes": 6,
                    "body": """Data in the real world is interconnected. Instead of cramming arrays into a single column, we use **Foreign Keys (FK)**.

### 1-to-Many (Parent-Child)
One `author` has many `books`.
- The `books` table contains an `author_id` column referencing `authors(id)`.
- The database enforces referential integrity: you cannot insert a book referencing an `author_id` that does not exist.

### Many-to-Many
One `student` enrolls in many `courses`, and each `course` has many `students`.
We resolve this using a **Junction Table** (`enrollments`):
```
students (id, name)
   │
   └── enrollments (student_id, course_id, enrolled_at)
             │
courses (id, title)
```""",
                },
                {
                    "title": "INNER JOIN vs LEFT JOIN",
                    "minutes": 6,
                    "body": """When querying related tables, we **JOIN** them on their shared key:

### INNER JOIN
Returns rows **only when there is a match in both tables**:
```sql
SELECT users.name, orders.total
FROM users
INNER JOIN orders ON orders.user_id = users.id;
```
If a user has never placed an order, they will **not** appear in the results.

### LEFT JOIN (LEFT OUTER JOIN)
Returns **all rows from the left table**, plus matching rows from the right table. If no match exists, columns from the right table are `NULL`:
```sql
SELECT users.name, orders.total
FROM users
LEFT JOIN orders ON orders.user_id = users.id;
```
Now users with zero orders still appear, with `orders.total` being `NULL`!""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Preserving Unmatched Left Rows",
                    "prompt": "You want to list all registered users along with their most recent order, including users who have never placed an order. What JOIN type should you use?",
                    "hint": "Which join preserves all rows from the primary table?",
                    "explanation": "LEFT JOIN keeps all rows from the left table (users) even if no corresponding row exists in the right table (orders).",
                    "xp": 20,
                    "config": {
                        "options": [
                            "LEFT JOIN",
                            "INNER JOIN",
                            "CROSS JOIN",
                            "NATURAL JOIN",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Constraint Enforcing Referential Integrity",
                    "prompt": "What two-word SQL constraint links a column in one table to the primary key of another table?",
                    "hint": "FOREIGN ...",
                    "explanation": "A FOREIGN KEY constraint guarantees referential integrity.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. FOREIGN KEY"},
                    "solution": {"regex": True, "accept": [r"foreign\s+key", r"FOREIGN\s+KEY"]},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Junction Table Characteristics",
                    "prompt": "Which of the following statements are true about a Junction Table (Join Table)?",
                    "hint": "How do you model many-to-many relationships?",
                    "explanation": "A junction table resolves many-to-many relationships and holds foreign keys referencing both participating tables.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "It is used to represent Many-to-Many relationships",
                            "It typically contains at least two Foreign Key columns",
                            "It can store relationship-specific metadata (such as created_at or role)",
                            "It eliminates the need for primary keys anywhere in the database",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "In-Memory INNER JOIN",
                    "prompt": "Write `inner_join(left_list, right_list, join_key)` that performs an in-memory inner join on two lists of dictionaries.\n- Match rows where `left_row[join_key] == right_row[join_key]`\n- Merge the matching dictionaries into a single combined dictionary `{**left, **right}`\n- Return a list of all merged dictionaries\n\n```python\nusers = [{\"id\": 1, \"name\": \"Alex\"}, {\"id\": 2, \"name\": \"Sam\"}]\norders = [{\"id\": 10, \"user_id\": 1, \"amt\": 50}]\ninner_join(users, orders, \"id\") # Note: matching key is specified\n```",
                    "hint": "Index right_list by join_key in a dictionary for O(n + m) performance, or use nested loops.",
                    "explanation": "Inner join matches records on equivalent keys, producing combined row records.",
                    "xp": 45,
                    "config": {
                        "language": "python",
                        "starter": "def inner_join(left_list, right_list, join_key):\n    # Return merged dicts matching on join_key\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "inner_join",
                        "cases": [
                            {
                                "args": [
                                    [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}],
                                    [{"id": 1, "score": 90}, {"id": 3, "score": 70}],
                                    "id",
                                ],
                                "expect": [{"id": 1, "name": "A", "score": 90}],
                            },
                            {
                                "args": [[{"id": 1}], [{"id": 2}], "id"],
                                "expect": [],
                            },
                            {
                                "args": [
                                    [{"k": "x", "val": 1}, {"k": "y", "val": 2}],
                                    [{"k": "y", "desc": "yes"}, {"k": "x", "desc": "no"}],
                                    "k",
                                ],
                                "expect": [
                                    {"k": "x", "val": 1, "desc": "no"},
                                    {"k": "y", "val": 2, "desc": "yes"},
                                ],
                                "hidden": True,
                            },
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 4: INDEXES, B-TREES & QUERY OPTIMIZATION
        # =========================================================================
        {
            "index": 4,
            "title": "Indexes, B-Trees & Query Optimization",
            "summary": "Seq Scan vs Index Scan, how B-Trees work, composite index prefix rules, and EXPLAIN ANALYZE.",
            "xp_reward": 115,
            "lessons": [
                {
                    "title": "How Databases Search: Seq Scan vs B-Tree",
                    "minutes": 6,
                    "body": """Without an index, finding a user by email requires a **Sequential Scan (Seq Scan)**:
The database must read every single 8KB disk block from the hard drive, scanning row by row ($O(n)$).
On 50 million rows, this takes 15 seconds!

### What is a B-Tree Index?
A B-Tree (Balanced Tree) is a sorted, self-balancing tree stored on disk:
- Each node contains sorted keys and pointers to child blocks.
- Looking up a value requires following pointers from root to leaf in $O(\\log n)$ steps (typically just 3 or 4 disk reads!).
- Searching 50 million rows drops from 15 seconds to **0.5 milliseconds**!

```sql
CREATE INDEX idx_users_email ON users(email);
```

> [!CAUTION]
> Indexes are not free! Every index accelerates `SELECT` queries, but slightly **slows down `INSERT`, `UPDATE`, and `DELETE`** because the database must keep the B-Tree balanced on every write.""",
                },
                {
                    "title": "Composite Indexes & The Leftmost Prefix Rule",
                    "minutes": 6,
                    "body": """When queries filter on multiple columns, you can create a composite (multi-column) index:

```sql
CREATE INDEX idx_orders_org_created ON orders(org_id, created_at);
```

### The Leftmost Prefix Rule
Think of a multi-column index like a phonebook sorted by `(Last Name, First Name)`:
- Can you quickly find everyone named `"Smith"`? **Yes** (leftmost column match).
- Can you find `"John Smith"`? **Yes** (full match).
- Can you quickly find everyone with the first name `"John"`, regardless of last name? **NO!** You have to read the entire phonebook!

An index on `(A, B)` speeds up queries on:
- `WHERE A = ?`
- `WHERE A = ? AND B = ?`
It **does NOT** speed up `WHERE B = ?` alone!""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Composite Index Leftmost Prefix",
                    "prompt": "You have a composite B-Tree index on `orders(customer_id, order_date)`. Which of the following queries CANNOT use this index efficiently?",
                    "hint": "Remember the phonebook sorted by (Last Name, First Name).",
                    "explanation": "Querying by `order_date` alone violates the leftmost prefix rule because the index is sorted primarily by `customer_id`.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "SELECT * FROM orders WHERE order_date = '2026-01-01'",
                            "SELECT * FROM orders WHERE customer_id = 42",
                            "SELECT * FROM orders WHERE customer_id = 42 AND order_date = '2026-01-01'",
                            "SELECT * FROM orders WHERE customer_id = 42 ORDER BY order_date DESC",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Index Write Cost",
                    "prompt": "What is the primary operational trade-off of adding multiple indexes to a database table?",
                    "hint": "What happens when a new row is added?",
                    "explanation": "Indexes speed up read queries, but slow down writes (INSERT, UPDATE, DELETE) and consume extra disk space.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "Faster reads, but slower write operations and extra disk usage",
                            "Faster writes, but slower read operations",
                            "Database connections get capped at 10",
                            "All text columns become case-insensitive",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Query Plan Command",
                    "prompt": "What SQL command keyword is placed before a query to inspect the database query planner's execution steps?",
                    "hint": "EXPLAIN ...",
                    "explanation": "EXPLAIN (or EXPLAIN ANALYZE) shows the execution plan.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. EXPLAIN"},
                    "solution": {"regex": True, "accept": [r"explain(\s+analyze)?", r"EXPLAIN(\s+ANALYZE)?"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Check Leftmost Prefix Compatibility",
                    "prompt": "Write `can_use_index(index_cols, query_cols)` that returns `True` if a query can efficiently utilize a composite index, according to the leftmost prefix rule.\n\n`index_cols` and `query_cols` are lists of column name strings.\nThe index is usable if `query_cols` contains the first column `index_cols[0]`.\n\n```python\ncan_use_index([\"org_id\", \"created_at\"], [\"org_id\"]) -> True\ncan_use_index([\"org_id\", \"created_at\"], [\"org_id\", \"created_at\"]) -> True\ncan_use_index([\"org_id\", \"created_at\"], [\"created_at\"]) -> False\ncan_use_index([\"a\", \"b\", \"c\"], [\"b\", \"c\"]) -> False\n```",
                    "hint": "Check if `len(index_cols) > 0` and `index_cols[0] in query_cols`.",
                    "explanation": "A composite index requires the leading leftmost column to be present in filter predicates.",
                    "xp": 40,
                    "config": {
                        "language": "python",
                        "starter": "def can_use_index(index_cols, query_cols):\n    # Return True if index can be used by query_cols\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "can_use_index",
                        "cases": [
                            {"args": [["org_id", "created_at"], ["org_id"]], "expect": True},
                            {"args": [["org_id", "created_at"], ["org_id", "created_at"]], "expect": True},
                            {"args": [["org_id", "created_at"], ["created_at"]], "expect": False},
                            {"args": [["a", "b", "c"], ["b", "c"]], "expect": False},
                            {"args": [[], ["x"]], "expect": False, "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 5: TRANSACTIONS, ACID & CONCURRENCY
        # =========================================================================
        {
            "index": 5,
            "title": "Transactions, ACID & Concurrency",
            "summary": "The bank transfer dilemma, ACID properties, isolation anomalies, and locking with SELECT FOR UPDATE.",
            "xp_reward": 125,
            "lessons": [
                {
                    "title": "The Bank Transfer Dilemma & ACID",
                    "minutes": 7,
                    "body": """Imagine transferring $100 from Alice to Bob:
1. Deduct $100 from Alice (`UPDATE accounts SET balance = balance - 100 WHERE id = 1`)
2. Credit $100 to Bob (`UPDATE accounts SET balance = balance + 100 WHERE id = 2`)

What if the server crashes or loses power between step 1 and step 2? $100 has vanished into thin air!

### The ACID Guarantees
To prevent this, databases provide **Transactions**:
- **Atomicity (All-or-Nothing)**: Either all operations in the transaction succeed, or the entire transaction is rolled back as if nothing ever happened.
- **Consistency**: The database transitions from one valid state to another, never violating constraints.
- **Isolation**: Concurrent transactions running at the same time cannot see uncommitted changes from each other.
- **Durability**: Once a transaction is committed, its changes survive crashes and power outages.

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```""",
                },
                {
                    "title": "Isolation Anomalies & Row-Level Locking",
                    "minutes": 6,
                    "body": """When hundreds of users access the database simultaneously:
- **Dirty Read**: Reading uncommitted data that might be rolled back.
- **Non-Repeatable Read**: Re-reading a row in the same transaction and seeing different data because another transaction modified it.
- **Lost Update (Race Condition)**: Two users read balance `$100`, both deduct `$20`, and both write `$80`. The balance should be `$60`!

### Pessimistic Locking with SELECT FOR UPDATE
To safely modify a balance, lock the specific row until your transaction completes:

```sql
BEGIN;
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
-- Other transactions trying to read FOR UPDATE on id 1 will block and wait!
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;
```""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Atomicity Guarantee",
                    "prompt": "A transaction contains 5 UPDATE statements. The 4th statement fails with a syntax error. What does the Atomicity property guarantee?",
                    "hint": "All or nothing.",
                    "explanation": "Atomicity guarantees that all changes are rolled back, leaving the database exactly as it was before the transaction started.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "All changes are rolled back completely",
                            "The first 3 updates remain saved in the database",
                            "The database automatically retries the 4th statement 10 times",
                            "The table is deleted",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Transaction Abort Command",
                    "prompt": "What SQL command cancels an ongoing transaction and discards all modifications made within it?",
                    "hint": "ROLL...",
                    "explanation": "ROLLBACK reverts all changes in the current transaction.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. ROLLBACK"},
                    "solution": {"regex": True, "accept": [r"rollback", r"ROLLBACK"]},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Consequences of Missing Transactions",
                    "prompt": "Which problems can happen if multi-step financial operations are run without database transactions?",
                    "hint": "Think about network timeouts, power loss, and parallel requests.",
                    "explanation": "Without transactions, crashes cause partial updates, and concurrent requests cause race conditions and lost updates.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "Partial state updates if a crash happens midway",
                            "Lost updates due to concurrent race conditions",
                            "Money created or destroyed between accounts",
                            "The database server uninstalls itself",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Atomic Account Transfer Simulation",
                    "prompt": "Write `atomic_transfer(accounts, from_id, to_id, amount)` that simulates an atomic bank transfer.\n`accounts` is a dict `{account_id: balance}`.\n\nRules:\n1. Both `from_id` and `to_id` must exist in `accounts`.\n2. `amount` must be `> 0`.\n3. `accounts[from_id]` must be `>= amount`.\n4. If all checks pass: deduct `amount` from `from_id`, add `amount` to `to_id`, and return `True`.\n5. If any check fails: **make no modifications** to `accounts` and return `False`.\n\n```python\naccs = {1: 100, 2: 50}\natomic_transfer(accs, 1, 2, 30) -> True   # accs is now {1: 70, 2: 80}\natomic_transfer(accs, 1, 2, 200) -> False  # Insufficient funds, accs unchanged\n```",
                    "hint": "Perform all validation checks BEFORE modifying any balances.",
                    "explanation": "Simulating all-or-nothing execution ensures consistency even during failures.",
                    "xp": 45,
                    "config": {
                        "language": "python",
                        "starter": "def atomic_transfer(accounts, from_id, to_id, amount):\n    # Atomically transfer amount or return False\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "atomic_transfer",
                        "cases": [
                            {"args": [{1: 100, 2: 50}, 1, 2, 30], "expect": True},
                            {"args": [{1: 100, 2: 50}, 1, 2, 200], "expect": False},
                            {"args": [{1: 100}, 1, 99, 50], "expect": False},
                            {"args": [{1: 100, 2: 50}, 1, 2, -10], "expect": False},
                            {"args": [{1: 50, 2: 50}, 1, 2, 50], "expect": True, "hidden": True},
                        ],
                    },
                },
            ],
        },
    ],
}
