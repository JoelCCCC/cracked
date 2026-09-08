TRACK = {
    "slug": "devops",
    "name": "DevOps & Infrastructure",
    "tagline": "Ship on a Friday and sleep fine.",
    "description": (
        "Containers, CI/CD, deployment strategies, observability and incident response — "
        "the operational half of being a senior engineer."
    ),
    "icon": "⚙",
    "accent": "#f2c744",
    "order": 5,
    "required_xp": 1900,
    "levels": [
        {
            "index": 1,
            "title": "Containers and reproducible builds",
            "summary": "Layers, caching, small images, and the twelve-factor rules that matter.",
            "xp_reward": 100,
            "lessons": [
                {
                    "title": "A Dockerfile that builds in seconds",
                    "minutes": 7,
                    "body": """Every instruction is a cached layer. Change a layer and **everything after it rebuilds**. So order from least to most volatile.

```dockerfile
# 1. build stage
FROM python:3.12-slim AS build
WORKDIR /app
COPY requirements.txt .                 # deps change rarely...
RUN pip install --no-cache-dir -r requirements.txt
COPY . .                                # ...source changes constantly

# 2. runtime stage: no compilers, no build cache
FROM python:3.12-slim
WORKDIR /app
RUN useradd --create-home app
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=build /app /app
USER app
CMD ["gunicorn", "config.wsgi", "-b", "0.0.0.0:8000"]
```

Four things that do most of the work:

1. **Copy the manifest before the source.** Otherwise every one-line change reinstalls all dependencies.
2. **Multi-stage.** Build tools never reach the runtime image — smaller, and a smaller attack surface.
3. **Non-root `USER`.** A container escape starting as root is a much worse day.
4. **`.dockerignore`.** Keep `.git`, `node_modules` and `.env` out of the build context.

Pin base images by digest for anything you actually care about reproducing.""",
                },
                {
                    "title": "Config, state, and the twelve factors that matter",
                    "minutes": 6,
                    "body": """Three rules cover most of it:

**Config in the environment.** Same image in dev, staging and prod; only env vars differ. Secrets come from a secret manager at runtime — never baked into the image, never in git. If a secret ever lands in a commit, rotate it; deleting the commit is not a fix, the object is still in every clone.

**Processes are stateless and disposable.** Anything on local disk vanishes on restart. Sessions go in Redis or a cookie; uploads go to object storage. The process must handle `SIGTERM` by draining and exiting quickly, because the orchestrator will kill it.

**Logs are an event stream on stdout.** The process should not know about log files or rotation — the platform collects. Log **structured JSON** with a request id so you can correlate across services:

```json
{"level":"info","msg":"order.created","request_id":"a1b2","order_id":42,"duration_ms":38}
```

Grepping unstructured strings works at one service. It stops working at ten.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Why is every build slow",
                    "prompt": "A Dockerfile does `COPY . .` and then `RUN pip install -r requirements.txt`. Every one-line source change triggers a full dependency reinstall.\n\nWhy?",
                    "hint": "Layers cache in order.",
                    "explanation": "`COPY . .` invalidates its layer on any source change, and every later layer — including the install — is rebuilt. Copying `requirements.txt` first keeps the install layer cached until dependencies actually change.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "pip has no cache inside containers",
                            "The COPY invalidates the cache for every layer after it",
                            "Docker rebuilds all layers whenever the Dockerfile is read",
                            "The base image is re-pulled each build",
                        ]
                    },
                    "solution": {"answer": 1},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Never in the image",
                    "prompt": "Which of these should **not** be baked into a container image?",
                    "hint": "Anything secret, or anything that differs per environment.",
                    "explanation": "Secrets and per-environment config are injected at runtime; the `.git` directory is pure bloat and leaks history. Application source is exactly what the image is for.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "Database passwords",
                            "The production API hostname",
                            "The application source code",
                            "The .git directory",
                        ]
                    },
                    "solution": {"answers": [0, 1, 3]},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "The polite shutdown signal",
                    "prompt": "Which POSIX signal does an orchestrator send first to ask a container to shut down gracefully, before it eventually sends SIGKILL?",
                    "hint": "It is catchable; SIGKILL is not.",
                    "explanation": "`SIGTERM`. Trap it, stop accepting new work, finish in-flight requests, exit. Ignore it and you get SIGKILLed after the grace period, dropping live requests on every deploy.",
                    "xp": 20,
                    "config": {"placeholder": "a signal name"},
                    "solution": {"regex": True, "accept": [r"sig\s*term", r"15", r"sigterm\s*\(?15\)?"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Which layers rebuild",
                    "prompt": "Write `layers_rebuilt(instructions, changed_step)` returning the number of layers that must rebuild.\n\n`instructions` is a list of Dockerfile instruction strings. `changed_step` is the 0-based index of the first invalidated layer, or `-1` if nothing changed.\n\nEverything from `changed_step` onward rebuilds.\n\n```\nlayers_rebuilt(['FROM x','COPY req','RUN pip','COPY .'], 1) -> 3\nlayers_rebuilt(['FROM x','COPY req'], -1) -> 0\n```",
                    "hint": "It is `len - changed_step`, with guards for -1 and out-of-range.",
                    "explanation": "Cache invalidation cascades forward and never backward — which is the whole reason to order a Dockerfile from stable to volatile.",
                    "xp": 40,
                    "config": {"language": "python", "starter": "def layers_rebuilt(instructions, changed_step):\n    ...\n"},
                    "solution": {
                        "entrypoint": "layers_rebuilt",
                        "cases": [
                            {"args": [["FROM x", "COPY req", "RUN pip", "COPY ."], 1], "expect": 3},
                            {"args": [["FROM x", "COPY req"], -1], "expect": 0},
                            {"args": [["FROM x"], 0], "expect": 1},
                            {"args": [[], -1], "expect": 0},
                            {"args": [["a", "b", "c"], 5], "expect": 0, "hidden": True},
                        ],
                    },
                },
            ],
        },
        {
            "index": 2,
            "title": "CI/CD and safe deploys",
            "summary": "Pipelines, blue-green vs canary, migrations that don't break rollback.",
            "xp_reward": 110,
            "lessons": [
                {
                    "title": "Deployment strategies",
                    "minutes": 7,
                    "body": """| Strategy | How | Rollback | Cost |
| --- | --- | --- | --- |
| **Recreate** | stop old, start new | redeploy old | downtime |
| **Rolling** | replace instances gradually | roll back gradually | two versions live at once |
| **Blue-green** | full second environment, flip the router | instant flip back | 2x infrastructure |
| **Canary** | 1% → 10% → 100%, watching metrics | drop the canary | needs good metrics |

Rolling and canary both mean **two versions of your code run simultaneously**. That is the constraint that shapes everything else — most importantly your database migrations.

**Feature flags** separate *deploy* from *release*. Ship the code dark, turn it on for 1% of users, turn it off in seconds without a deploy. A flag you never delete is technical debt, so put an expiry on it when you create it.""",
                },
                {
                    "title": "Expand / contract migrations",
                    "minutes": 7,
                    "body": """Renaming a column in one migration breaks every old process still running. Do it in phases, each independently deployable and rollback-safe:

1. **Expand** — add the new column, nullable. Deploy. Nothing reads it yet.
2. **Backfill** — copy data in batches. Never one `UPDATE` over 50M rows; that holds locks and bloats WAL.
3. **Dual-write** — application writes both columns, reads the old one. Deploy.
4. **Flip reads** — read the new column. Deploy. Now the old one is unused.
5. **Contract** — drop the old column, after you're sure you won't roll back.

Postgres specifics worth memorising:

- `ADD COLUMN` with a non-volatile default is fast in modern Postgres; adding a `NOT NULL` to an existing column requires a validated check or a full scan.
- `CREATE INDEX CONCURRENTLY` avoids locking writes — and cannot run inside a transaction, so it needs `atomic = False` in a Django migration.
- Set a short `lock_timeout` on migrations. A DDL statement waiting on a lock queues *every* subsequent query behind it and takes the site down.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "hard",
                    "title": "Rename without downtime",
                    "prompt": "You must rename `users.name` to `users.full_name` on a service that deploys with a rolling update.\n\nWhat is the safe first step?",
                    "hint": "During a rolling deploy, old and new code both run.",
                    "explanation": "Expand first: add the new column so old code (which knows nothing about it) keeps working. A single rename breaks every old instance the moment it lands.",
                    "xp": 40,
                    "config": {
                        "options": [
                            "ALTER TABLE users RENAME COLUMN name TO full_name",
                            "Add full_name as a new nullable column and deploy",
                            "Take the site down for five minutes",
                            "Drop name and recreate it under the new name",
                        ]
                    },
                    "solution": {"answer": 1},
                },
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Index on a live table",
                    "prompt": "You need a new index on a 200M-row Postgres table that is taking writes right now. Which is safe?",
                    "hint": "One form of CREATE INDEX does not block writes.",
                    "explanation": "`CREATE INDEX CONCURRENTLY` builds without an exclusive lock (two passes, slower, cannot run in a transaction). A plain `CREATE INDEX` blocks all writes for the duration.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "CREATE INDEX — it is fast enough",
                            "CREATE INDEX CONCURRENTLY",
                            "Add it inside the same transaction as the data migration",
                            "There is no safe way; take a maintenance window",
                        ]
                    },
                    "solution": {"answer": 1},
                },
                {
                    "kind": "short",
                    "difficulty": "medium",
                    "title": "Deploy is not release",
                    "prompt": "What mechanism lets you ship code to production while keeping it switched off, then enable it for 1% of users without another deploy? (Two words.)",
                    "hint": "Also called a toggle.",
                    "explanation": "Feature flags decouple deploy from release, which is what makes canarying, instant kill-switches and trunk-based development practical.",
                    "xp": 25,
                    "config": {"placeholder": "two words"},
                    "solution": {"regex": True, "accept": [r"feature\s+(flags?|toggles?|switch(es)?)", r"flags?", r"toggles?"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Canary rollout schedule",
                    "prompt": "Write `rollout(total_instances, steps)` returning the cumulative instance count at each canary step.\n\n`steps` is a list of percentages (e.g. `[1, 10, 50, 100]`). For each, return `ceil(total * pct / 100)`, and never decrease or exceed `total`.\n\n```\nrollout(10, [1, 10, 50, 100]) -> [1, 1, 5, 10]\n```",
                    "hint": "`-(-a // b)` is integer ceiling division. Clamp with max/min against the running value.",
                    "explanation": "Rounding up matters: `ceil` guarantees a 1% canary on a 10-instance fleet is still one real instance rather than zero, which would make the canary a no-op.",
                    "xp": 45,
                    "config": {"language": "python", "starter": "import math\n\ndef rollout(total_instances, steps):\n    ...\n"},
                    "solution": {
                        "entrypoint": "rollout",
                        "cases": [
                            {"args": [10, [1, 10, 50, 100]], "expect": [1, 1, 5, 10]},
                            {"args": [100, [1, 25, 100]], "expect": [1, 25, 100]},
                            {"args": [3, [50, 100]], "expect": [2, 3]},
                            {"args": [5, []], "expect": []},
                            {"args": [0, [50]], "expect": [0]},
                            {"args": [10, [100, 50]], "expect": [10, 10], "hidden": True},
                        ],
                    },
                },
            ],
        },
        {
            "index": 3,
            "title": "Observability and incidents",
            "summary": "Metrics vs logs vs traces, SLOs, and what to do at 3am.",
            "xp_reward": 120,
            "lessons": [
                {
                    "title": "The three signals",
                    "minutes": 7,
                    "body": """- **Metrics** — cheap numeric time series. Answer *is something wrong?* Alert on these.
- **Logs** — discrete events with detail. Answer *what exactly happened to this request?*
- **Traces** — one request's path across services with timing per span. Answer *where did the time go?*

**Percentiles, not averages.** An average latency of 120 ms hides a p99 of 4 s. The average is the experience of nobody; p99 is the experience of your loudest users, and at scale, of a lot of them.

The four **golden signals** for any service: latency, traffic, errors, saturation.

**SLO and error budget.** Pick a target — "99.9% of requests succeed in 30 days". That allows ~43 minutes of failure per month. That budget is a *decision tool*: budget left → ship faster; budget burnt → freeze features and fix reliability. It ends the argument about whether to prioritise stability by turning it into arithmetic.

Alert on **symptoms users feel** (error rate, latency, budget burn rate), not on causes (CPU at 90%). A CPU alert at 3am that no user noticed is how on-call rotations die.""",
                },
                {
                    "title": "Incident response, briefly",
                    "minutes": 6,
                    "body": """**Mitigate first, diagnose second.** Roll back, flip the flag, shed load, fail over. The cause can be found once users are served again — restore service, then investigate.

Roles, even for a two-person team: an **incident commander** (decides, does not debug), a **communicator** (updates the status page), and **hands on keyboard**. The commander's job is to stop five people from independently poking production.

Afterwards, write a **blameless postmortem**: timeline, impact, contributing factors, and action items with owners and dates. Blameless is not politeness — the moment naming a person is the outcome, people stop reporting near-misses and you lose your best early-warning signal.

The question that matters is never "who ran the command" but "why was it possible for one command to do this, and why did it take 40 minutes to notice".""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Where did the time go",
                    "prompt": "One endpoint is slow, but only sometimes, and it calls four internal services. Which signal identifies the slow hop fastest?",
                    "hint": "Per-request, per-service timing.",
                    "explanation": "A distributed trace breaks one request into spans with durations, so the slow service is visible immediately. Metrics tell you *that* it is slow; logs make you correlate by hand.",
                    "xp": 30,
                    "config": {"options": ["Metrics", "Logs", "Distributed traces", "Core dumps"]},
                    "solution": {"answer": 2},
                },
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "First move in an incident",
                    "prompt": "Checkout errors jump to 30% four minutes after a deploy. What do you do first?",
                    "hint": "Users are failing right now.",
                    "explanation": "Mitigate first — roll back. The deploy is the obvious correlate, restoring service is free of risk to the investigation, and the artefacts (logs, traces, the bad build) are all still there afterwards.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "Roll back the deploy, then investigate",
                            "Read the diff until you find the bug",
                            "Scale up the service in case it is load",
                            "Wait ten minutes to see if it recovers",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "short",
                    "difficulty": "medium",
                    "title": "How much can you break",
                    "prompt": "What do you call the amount of unreliability an SLO permits — the thing you spend on shipping risk and stop spending when it runs out? (Two words.)",
                    "hint": "SLO of 99.9% gives you 43 minutes a month of it.",
                    "explanation": "The error budget. Framing reliability as a budget converts a values argument into a number both product and infra can agree on.",
                    "xp": 25,
                    "config": {"placeholder": "two words"},
                    "solution": {"regex": True, "accept": [r"error\s+budget", r"the\s+error\s+budget"]},
                },
                {
                    "kind": "code",
                    "difficulty": "hard",
                    "title": "Compute the p99",
                    "prompt": "Write `percentile(latencies, p)` returning the nearest-rank percentile of a list of numbers.\n\nNearest rank: sort ascending, take index `ceil(p/100 * n) - 1`, clamped to `[0, n-1]`. Return `None` for an empty list.\n\n```\npercentile([1,2,3,4,5,6,7,8,9,10], 90) -> 9\npercentile([5], 50) -> 5\n```",
                    "hint": "Sort, then `-(-p * n // 100) - 1` with clamping.",
                    "explanation": "Nearest-rank is what most monitoring systems report and is trivially exact for a full sample. At real scale you'd use a t-digest or HDR histogram, since you cannot keep every latency in memory.",
                    "xp": 50,
                    "config": {"language": "python", "starter": "def percentile(latencies, p):\n    ...\n"},
                    "solution": {
                        "entrypoint": "percentile",
                        "cases": [
                            {"args": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 90], "expect": 9},
                            {"args": [[5], 50], "expect": 5},
                            {"args": [[], 99], "expect": None},
                            {"args": [[3, 1, 2], 100], "expect": 3},
                            {"args": [[3, 1, 2], 1], "expect": 1},
                            {"args": [list(range(1, 101)), 99], "expect": 99, "hidden": True},
                        ],
                    },
                },
            ],
        },
    ],
}
