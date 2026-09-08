TRACK = {
    "slug": "databases",
    "name": "Database Design",
    "tagline": "Schemas that survive contact with real traffic.",
    "description": (
        "Normalisation and when to break it, indexes and why yours isn't used, "
        "transactions and isolation, and the query patterns that quietly melt production."
    ),
    "icon": "▤",
    "accent": "#3b9dff",
    "order": 4,
    "required_xp": 1400,
    "levels": [
        {
            "index": 1,
            "title": "Modelling and normalisation",
            "summary": "Keys, relationships, 3NF, and the denormalisation you do on purpose.",
            "xp_reward": 100,
            "lessons": [
                {
                    "title": "Normal forms, in plain language",
                    "minutes": 7,
                    "body": """Normalisation means: **store each fact exactly once**.

- **1NF** — no repeating groups. `tags` as a comma-separated string is a 1NF violation, and it's why you can't index or join on it.
- **2NF** — no column depending on only *part* of a composite key.
- **3NF** — no column depending on another non-key column. If `orders` stores `customer_email`, and email lives on `customers`, you now have two copies that will disagree.

The interview one-liner: *every non-key column depends on the key, the whole key, and nothing but the key.*

```sql
-- not normalised: product name and price copied onto every line
CREATE TABLE order_lines (
  order_id   BIGINT,
  product_id BIGINT,
  product_name TEXT,     -- duplicated from products
  unit_price NUMERIC     -- ...but see below
);
```

`product_name` is a genuine bug: rename the product and history rewrites itself. `unit_price` is **not** — the price *at time of sale* is a different fact from the current price, and it belongs on the line. Recognising that difference is the actual skill.""",
                },
                {
                    "title": "Denormalise deliberately",
                    "minutes": 6,
                    "body": """Normalise first. Denormalise only with a measurement in hand and a plan for keeping copies in sync.

Legitimate reasons:

- **Point-in-time facts** — price paid, shipping address used, tax rate applied.
- **Counter caches** — `posts.comment_count` when the count is read a thousand times per write. Maintain it in the same transaction or a trigger, never in application code that can crash halfway.
- **Read models** — a flattened table or materialised view feeding a dashboard.

Constraints are how you keep it honest, and they belong in the database, not only in the app:

```sql
CREATE TABLE memberships (
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  team_id BIGINT NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
  role    TEXT   NOT NULL CHECK (role IN ('owner','admin','member')),
  PRIMARY KEY (user_id, team_id)
);
```

Two apps, a migration script and a psql session all write to your database. Only the database can enforce a rule for all four.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Which copy is a bug",
                    "prompt": "An `order_lines` table stores `product_name` and `unit_price` copied from `products`. Which one is a genuine normalisation problem?",
                    "hint": "One of them is a different fact, not a duplicate one.",
                    "explanation": "`unit_price` records the price *at the time of sale* — a distinct fact that must not change when the catalogue does. `product_name` is a true duplicate and will drift on rename.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "Only product_name",
                            "Only unit_price",
                            "Both are bugs",
                            "Neither — copying is always fine for speed",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Tags in a string",
                    "prompt": "A table stores tags as `'python,web,sql'` in one TEXT column. Which normal form does this break? (Answer like `2NF`.)",
                    "hint": "Repeating groups in one column.",
                    "explanation": "1NF requires atomic values. The fix is a `tags` table plus a join table — which also gives you an index and real referential integrity.",
                    "xp": 25,
                    "config": {"placeholder": "e.g. 3NF"},
                    "solution": {"regex": True, "accept": [r"1\s*nf", r"first\s+normal\s+form"]},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Constraints worth having",
                    "prompt": "Which of these belong in the database schema rather than only in application code?",
                    "hint": "Which rules must hold no matter who is writing?",
                    "explanation": "Uniqueness, foreign keys and value checks are integrity rules — enforce them where every writer passes. Formatting an amount for display is a presentation concern.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "A unique index on users.email",
                            "A foreign key from orders.user_id to users.id",
                            "CHECK (quantity > 0)",
                            "Formatting prices as '$12.00' for the UI",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Find the duplicated facts",
                    "prompt": "Given a list of row dicts, write `duplicated_columns(rows, key)` returning the **sorted** list of column names whose value is fully determined by `key` and appears in more than one row for the same key value — i.e. columns that are duplicated per key.\n\nIgnore the `key` column itself. A column that ever disagrees for the same key is **not** a candidate.\n\n```\nrows = [\n  {'product_id': 1, 'name': 'Pen', 'price': 2},\n  {'product_id': 1, 'name': 'Pen', 'price': 3},\n  {'product_id': 2, 'name': 'Cup', 'price': 5},\n]\nduplicated_columns(rows, 'product_id') -> ['name']\n```",
                    "hint": "For each column, group values by the key. A column qualifies if every key maps to exactly one distinct value and some key has more than one row.",
                    "explanation": "This is functional-dependency detection — the mechanical form of 'is this column duplicated from another table?'. Real schema linters do exactly this over a sample of production data.",
                    "xp": 50,
                    "config": {"language": "python", "starter": "def duplicated_columns(rows, key):\n    ...\n"},
                    "solution": {
                        "entrypoint": "duplicated_columns",
                        "cases": [
                            {
                                "args": [
                                    [
                                        {"product_id": 1, "name": "Pen", "price": 2},
                                        {"product_id": 1, "name": "Pen", "price": 3},
                                        {"product_id": 2, "name": "Cup", "price": 5},
                                    ],
                                    "product_id",
                                ],
                                "expect": ["name"],
                            },
                            {"args": [[], "id"], "expect": []},
                            {
                                "args": [[{"id": 1, "a": 1}, {"id": 2, "a": 2}], "id"],
                                "expect": [],
                            },
                            {
                                "args": [
                                    [{"id": 1, "a": 1, "b": 9}, {"id": 1, "a": 1, "b": 9}],
                                    "id",
                                ],
                                "expect": ["a", "b"],
                            },
                        ],
                    },
                },
            ],
        },
        {
            "index": 2,
            "title": "Indexes and query plans",
            "summary": "B-trees, composite order, selectivity, and reading EXPLAIN.",
            "xp_reward": 110,
            "lessons": [
                {
                    "title": "Why your index isn't used",
                    "minutes": 7,
                    "body": """A B-tree index is a sorted structure. That single fact explains almost every gotcha.

**Composite order is left-to-right.** An index on `(tenant_id, created_at)` serves:

- `WHERE tenant_id = 5` ✅
- `WHERE tenant_id = 5 ORDER BY created_at` ✅ (sorted for free)
- `WHERE created_at > now() - '1 day'` ❌ — you skipped the leading column

**Rule:** equality columns first, then the range/sort column.

**Wrapping the column kills it.**

```sql
WHERE lower(email) = 'a@b.com'          -- seq scan
CREATE INDEX ON users (lower(email));   -- ...unless you index the expression
WHERE created_at::date = '2024-01-01'   -- seq scan
WHERE created_at >= '2024-01-01' AND created_at < '2024-01-02'  -- index scan
```

**Leading wildcards can't be used.** `LIKE '%foo'` cannot; `LIKE 'foo%'` can. For full-text, use a GIN index and `tsvector`.

**Low selectivity is not worth indexing.** A boolean `is_active` that is true for 95% of rows will be ignored — the planner correctly judges a sequential scan cheaper. A *partial* index (`WHERE is_active = false`) is the fix.

Every index also costs write throughput and disk. Index what you filter, join and sort on; then delete the ones `pg_stat_user_indexes` says nobody uses.""",
                },
                {
                    "title": "Reading EXPLAIN ANALYZE",
                    "minutes": 6,
                    "body": """```
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;
```

Read it **inside out** — the deepest node runs first. What to look for:

- `Seq Scan` on a large table with a selective `WHERE` → missing index.
- **Estimated vs actual rows** off by 100x → stale statistics; `ANALYZE` the table. Bad estimates cause bad plan choices, which is the root of most "it was fast yesterday".
- `Nested Loop` with a big outer row count → often should be a hash join.
- `rows removed by filter` in the millions → you are reading far more than you return.
- High `shared read` in BUFFERS → going to disk instead of cache.

The number that matters is `actual time` on the top node, and where inside the tree it accumulates. A plan that looks ugly but returns in 3ms needs no work.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Composite index order",
                    "prompt": "Your hottest query is:\n\n```sql\nSELECT * FROM events\nWHERE tenant_id = $1 AND created_at >= $2\nORDER BY created_at DESC\nLIMIT 50;\n```\n\nWhich index serves it best?",
                    "hint": "Equality first, then the range/sort column.",
                    "explanation": "`(tenant_id, created_at)` lets the planner seek to the tenant and then walk `created_at` in order — the filter, the range and the ORDER BY are all satisfied by one index scan, so the LIMIT stops early.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "(created_at, tenant_id)",
                            "(tenant_id, created_at)",
                            "Two separate single-column indexes",
                            "(tenant_id) only",
                        ]
                    },
                    "solution": {"answer": 1},
                },
                {
                    "kind": "multi",
                    "difficulty": "hard",
                    "title": "Index-defeating predicates",
                    "prompt": "Assume a plain B-tree index on `users(email)` and `users(created_at)`. Which predicates **cannot** use those indexes?",
                    "hint": "Anything that wraps the column or starts with a wildcard.",
                    "explanation": "Wrapping the column in a function and a leading `%` both destroy the sorted-prefix property the B-tree relies on. A range on `created_at` and a prefix `LIKE` both use it fine.",
                    "xp": 40,
                    "config": {
                        "options": [
                            "WHERE lower(email) = 'a@b.com'",
                            "WHERE email LIKE '%@gmail.com'",
                            "WHERE created_at >= '2024-01-01'",
                            "WHERE email LIKE 'admin%'",
                        ]
                    },
                    "solution": {"answers": [0, 1]},
                },
                {
                    "kind": "short",
                    "difficulty": "medium",
                    "title": "The plan node you don't want",
                    "prompt": "In `EXPLAIN ANALYZE`, which node type on a large table, combined with a highly selective WHERE clause, is the classic sign of a missing index? (Two words.)",
                    "hint": "It reads every row.",
                    "explanation": "A `Seq Scan` reads the whole table. Selective filter + big table + Seq Scan = add an index (or check why the planner distrusts the one you have).",
                    "xp": 25,
                    "config": {"placeholder": "a plan node"},
                    "solution": {"regex": True, "accept": [r"seq(uential)?\s*scan", r"seqscan", r"full\s+table\s+scan"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Would this index be used?",
                    "prompt": "Write `covers(index_cols, equality_cols, sort_col)` returning `True` if a B-tree index on `index_cols` (a list, in order) can satisfy a query that filters on **all** of `equality_cols` (a set-like list) and then sorts by `sort_col`.\n\nRule: the index works when its leading columns are exactly the equality columns (in any order among themselves) and the very next index column is `sort_col`. `sort_col` may be `None`, meaning no sort is needed.\n\n```\ncovers(['tenant_id','created_at'], ['tenant_id'], 'created_at') -> True\ncovers(['created_at','tenant_id'], ['tenant_id'], 'created_at') -> False\n```",
                    "hint": "Compare the first `len(equality_cols)` index columns as a set, then check position `len(equality_cols)`.",
                    "explanation": "This encodes the left-to-right prefix rule. It is exactly the check to run in your head before adding an index — most 'unused index' incidents are a violated prefix.",
                    "xp": 50,
                    "config": {"language": "python", "starter": "def covers(index_cols, equality_cols, sort_col):\n    ...\n"},
                    "solution": {
                        "entrypoint": "covers",
                        "cases": [
                            {"args": [["tenant_id", "created_at"], ["tenant_id"], "created_at"], "expect": True},
                            {"args": [["created_at", "tenant_id"], ["tenant_id"], "created_at"], "expect": False},
                            {"args": [["a", "b", "c"], ["b", "a"], "c"], "expect": True},
                            {"args": [["a"], ["a"], None], "expect": True},
                            {"args": [["a", "b"], ["a"], None], "expect": True},
                            {"args": [["a", "b"], ["a", "b", "c"], None], "expect": False, "hidden": True},
                        ],
                    },
                },
            ],
        },
        {
            "index": 3,
            "title": "Transactions, isolation, and N+1",
            "summary": "ACID in practice, the anomalies, and the query pattern that kills endpoints.",
            "xp_reward": 120,
            "lessons": [
                {
                    "title": "Isolation levels and the anomalies they stop",
                    "minutes": 7,
                    "body": """ACID: **A**tomic (all or nothing), **C**onsistent (constraints hold), **I**solated (concurrent transactions don't corrupt each other), **D**urable (committed means survived).

Isolation is the one with knobs:

| Level | Dirty read | Non-repeatable read | Phantom | Write skew |
| --- | --- | --- | --- | --- |
| Read Committed *(Postgres default)* | no | **yes** | **yes** | **yes** |
| Repeatable Read | no | no | no* | **yes** |
| Serializable | no | no | no | no |

\\* Postgres's Repeatable Read uses snapshots, so it avoids phantoms too — but not write skew.

**Write skew**, the one that bites: two transactions each read "there are 2 doctors on call", each decide it's safe for their doctor to go off call, and both commit. Neither saw a conflicting *write* — they read overlapping data and wrote disjoint rows.

Fixes, in ascending cost: `SELECT ... FOR UPDATE` on the rows you're deciding from; a database constraint that makes the bad state unrepresentable; or `SERIALIZABLE` (and code that retries on serialization failure).

**Keep transactions short.** Never hold one open across an HTTP call to a third party — you're holding locks for the length of someone else's outage.""",
                },
                {
                    "title": "N+1: the endpoint killer",
                    "minutes": 6,
                    "body": """```python
for post in Post.objects.all():        # 1 query
    print(post.author.name)            # + 1 query per post
```

100 posts → 101 round trips. Each is maybe 0.5 ms of query and 1 ms of network. The endpoint is now slower than the sum of its work, and it degrades linearly with data.

The fix in Django:

```python
Post.objects.select_related("author")            # SQL JOIN, for FK / one-to-one
Post.objects.prefetch_related("tags")            # 2nd query + join in Python, for M2M / reverse FK
```

How to catch it before production:

- Assert query counts in tests: `with self.assertNumQueries(2):`
- Log queries in dev (`django-debug-toolbar`, or `CONN_HEALTH_CHECKS` + query logging) and watch the count per request.
- Alarm on requests exceeding a query-count budget.

The same trap exists in every ORM and in GraphQL resolvers, where it's solved with a DataLoader that batches per tick.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "hard",
                    "title": "Two doctors, one shift",
                    "prompt": "Two transactions each check `SELECT count(*) FROM oncall WHERE on_call = true` (it returns 2), then each sets a *different* doctor to off-call. Both commit. Now nobody is on call.\n\nWhat is this anomaly called?",
                    "hint": "They read overlapping rows but wrote different ones.",
                    "explanation": "Write skew. No row was written twice, so Read Committed and even snapshot-based Repeatable Read allow it. `SELECT ... FOR UPDATE`, a constraint, or SERIALIZABLE prevents it.",
                    "xp": 40,
                    "config": {"options": ["Dirty read", "Phantom read", "Write skew", "Lost update"]},
                    "solution": {"answer": 2},
                },
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Pick the prefetch",
                    "prompt": "`Post` has a ForeignKey to `Author` and a ManyToMany to `Tag`. You render 50 posts with the author name and all tags.\n\nWhat is the minimal fix?",
                    "hint": "One of these is a JOIN; the other needs a second query.",
                    "explanation": "`select_related` JOINs single-valued relations (FK, one-to-one). Many-to-many can't be JOINed without row multiplication, so `prefetch_related` issues one extra query and stitches in Python. Three queries total instead of 101.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "select_related('author', 'tags')",
                            "prefetch_related('author', 'tags')",
                            "select_related('author').prefetch_related('tags')",
                            "Add an index on post.author_id",
                        ]
                    },
                    "solution": {"answer": 2},
                },
                {
                    "kind": "short",
                    "difficulty": "medium",
                    "title": "Lock the rows you decided from",
                    "prompt": "Which SQL clause do you append to a SELECT to take a row-level write lock, so a concurrent transaction must wait before modifying those rows?",
                    "hint": "Three words after SELECT ... .",
                    "explanation": "`FOR UPDATE` locks the selected rows until the transaction ends. It's the cheapest reliable fix for read-then-write races such as inventory decrements.",
                    "xp": 25,
                    "config": {"placeholder": "SQL clause"},
                    "solution": {"regex": True, "accept": [r"(select\s+.*\s+)?for\s+update(\s+nowait|\s+skip\s+locked)?"]},
                },
                {
                    "kind": "code",
                    "difficulty": "hard",
                    "title": "Count the queries",
                    "prompt": "Write `query_count(n_posts, strategy)` returning how many SQL queries a listing of `n_posts` posts issues, where each post shows its author (FK) and its tags (M2M).\n\n- `\"naive\"` → 1 + 2 per post\n- `\"select_related\"` → 1 (join for author) + 1 per post (tags)\n- `\"optimized\"` → 2 total (join for author + one prefetch for tags), regardless of n\n\nAny other strategy returns `-1`. `n_posts` of 0 still costs the base queries.",
                    "hint": "Just encode the three formulas.",
                    "explanation": "Turning the N+1 discussion into arithmetic makes the cost obvious: at 50 posts naive is 101 queries, optimised is 2 — and the optimised number does not move as data grows.",
                    "xp": 45,
                    "config": {"language": "python", "starter": "def query_count(n_posts, strategy):\n    ...\n"},
                    "solution": {
                        "entrypoint": "query_count",
                        "cases": [
                            {"args": [50, "naive"], "expect": 101},
                            {"args": [50, "select_related"], "expect": 51},
                            {"args": [50, "optimized"], "expect": 2},
                            {"args": [0, "naive"], "expect": 1},
                            {"args": [0, "optimized"], "expect": 2},
                            {"args": [10, "magic"], "expect": -1, "hidden": True},
                        ],
                    },
                },
            ],
        },
    ],
}
