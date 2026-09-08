TRACK = {
    "slug": "devops",
    "name": "DevOps & Infrastructure",
    "tagline": "How software runs in production: Linux, Git, Docker, CI/CD, and Observability.",
    "description": (
        "Start from absolute zero. Learn the Linux terminal, Git workflows, Docker containerization, "
        "automated CI/CD deployment pipelines, and production observability."
    ),
    "icon": "▲",
    "accent": "#52c41a",
    "order": 5,
    "required_xp": 1100,
    "levels": [
        # =========================================================================
        # LEVEL 1: LINUX & TERMINAL FOUNDATIONS
        # =========================================================================
        {
            "index": 1,
            "title": "Linux & Terminal Foundations from Zero",
            "summary": "Shell navigation, streams (stdin, stdout, stderr), redirection, pipes, and exit codes.",
            "xp_reward": 85,
            "lessons": [
                {
                    "title": "The Shell & The Linux Filesystem",
                    "minutes": 6,
                    "body": """Every production cloud server (AWS, GCP, DigitalOcean) runs Linux without a graphical desktop. The terminal is your command center.

### Core Navigation Commands
- `pwd` (**P**rint **W**orking **D**irectory): Where am I right now?
- `ls -la`: List all files, including hidden dotfiles (`.env`, `.git`), with permissions and sizes.
- `cd /var/log`: Change directory. `cd ..` goes up one level; `cd ~` goes to your home folder.
- `cat app.log`: Print the entire file to the screen.
- `tail -n 50 -f app.log`: Follow the last 50 lines in real-time as new logs are written.
- `grep "ERROR" app.log`: Search for lines containing `"ERROR"`.""",
                },
                {
                    "title": "Streams, Redirection & Exit Codes",
                    "minutes": 6,
                    "body": """In Unix, **everything is a file**, and processes communicate via three standard streams:
1. `stdin` (0): Standard Input (keyboard or piped data)
2. `stdout` (1): Standard Output (normal output messages)
3. `stderr` (2): Standard Error (error messages and diagnostic logs)

### Stream Redirection
- `command > output.txt`: Overwrites `output.txt` with stdout.
- `command >> output.txt`: Appends stdout to `output.txt`.
- `command 2>&1`: Redirects stderr into stdout.

### The Unix Pipe (`|`)
Connect the stdout of one command directly into the stdin of another:
```bash
cat access.log | grep "500" | wc -l
# Reads log -> filters 500 errors -> counts matching lines
```

### Exit Codes: The Language of Success
When a command finishes, it returns an integer **exit code**:
- `0`: **Success** (no error).
- Non-zero (`1`, `2`, `127`): **Failure / Error**.
In bash, inspect the last command's exit code with `echo $?`.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Unix Exit Code for Success",
                    "prompt": "What numeric exit code does a Unix command return when it finishes successfully without any errors?",
                    "hint": "Zero or non-zero?",
                    "explanation": "Exit code 0 universally indicates success in Unix/Linux. Any non-zero code indicates an error.",
                    "xp": 20,
                    "config": {"options": ["0", "1", "200", "-1"]},
                    "solution": {"answer": 0},
                },
                {
                    "kind": "multi",
                    "difficulty": "easy",
                    "title": "Standard Unix Streams",
                    "prompt": "Which of the following are the standard I/O streams present in every Linux process?",
                    "hint": "File descriptors 0, 1, and 2.",
                    "explanation": "Standard input (stdin, 0), standard output (stdout, 1), and standard error (stderr, 2).",
                    "xp": 25,
                    "config": {
                        "options": [
                            "stdin (standard input)",
                            "stdout (standard output)",
                            "stderr (standard error)",
                            "stdlog (standard logging)",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2]},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Command Pipeline Operator",
                    "prompt": "What single character is used in Linux shells to pipe the output of one command into the input of another?",
                    "hint": "The vertical bar symbol.",
                    "explanation": "The pipe operator `|` connects stdout of the left command to stdin of the right command.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. |"},
                    "solution": {"regex": True, "accept": [r"^\|$"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Filter Log Lines by Level",
                    "prompt": "Write `filter_logs(log_lines, target_level)` that simulates `grep` filtering on log lines.\nEach log line has the format `\"[LEVEL] message\"` (e.g. `\"[ERROR] Database connection lost\"`).\n\nReturn a list of messages (without the `[LEVEL]` prefix and leading whitespace) matching `target_level` (case-insensitive).\n\n```python\nlogs = [\n    \"[INFO] Server started\",\n    \"[ERROR] Connection timed out\",\n    \"[INFO] User logged in\",\n    \"[ERROR] Out of memory\"\n]\nfilter_logs(logs, \"ERROR\")\n# -> [\"Connection timed out\", \"Out of memory\"]\n```",
                    "hint": "Check if line starts with `f\"[{target_level.upper()}]\"` and strip the prefix.",
                    "explanation": "Filtering log messages by severity level is a foundational CLI and debugging pattern.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def filter_logs(log_lines, target_level):\n    # Return list of message strings matching target_level\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "filter_logs",
                        "cases": [
                            {
                                "args": [
                                    ["[INFO] Server started", "[ERROR] Timeout", "[ERROR] Disk full"],
                                    "ERROR",
                                ],
                                "expect": ["Timeout", "Disk full"],
                            },
                            {
                                "args": [["[INFO] Ok"], "WARN"],
                                "expect": [],
                            },
                            {
                                "args": [
                                    ["[warn] High CPU", "[WARN] High Memory"],
                                    "warn",
                                ],
                                "expect": ["High CPU", "High Memory"],
                                "hidden": True,
                            },
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 2: GIT & VERSION CONTROL
        # =========================================================================
        {
            "index": 2,
            "title": "Git Version Control from Zero",
            "summary": "Working tree, staging area, commits, branching, merging, and resolving conflicts.",
            "xp_reward": 95,
            "lessons": [
                {
                    "title": "The Three Trees of Git",
                    "minutes": 6,
                    "body": """Git is not just a backup tool; it is a content-addressable directed acyclic graph (DAG) of project snapshots.

Git tracks your files across three distinct states:
1. **Working Directory**: The sandbox where you actively edit files on your filesystem.
2. **Staging Area (Index)**: The draft area where you prepare the exact changes for the next snapshot (`git add filename`).
3. **Repository History (HEAD)**: The permanent, immutable database of commits (`git commit -m "feat: add login"`).

```bash
# Typical daily cycle:
git status            # What changed?
git diff              # View unstaged line changes
git add src/auth.py   # Stage specific file
git commit -m "..."   # Record permanent snapshot
```""",
                },
                {
                    "title": "Branches, Merging & Conflicts",
                    "minutes": 6,
                    "body": """A **branch** in Git is simply a movable pointer to a commit. Creating a branch is virtually instantaneous:

```bash
git switch -c feature/user-profile   # Create and switch to new branch
# ... write code and commit ...
git switch main                      # Return to main branch
git merge feature/user-profile       # Merge changes into main
```

### What Causes a Merge Conflict?
When two branches modify the **exact same lines of the same file** in different ways, Git stops and asks the human to choose:

```git
<<<<<<< HEAD (current main)
const timeoutMs = 5000;
=======
const timeoutMs = 10000;
>>>>>>> feature/user-profile
```
To resolve: edit the file to keep the desired code, remove the marker lines (`<<<<<<<`, `=======`, `>>>>>>>`), and run `git add` + `git commit`.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "Moving Files to Staging Area",
                    "prompt": "Which Git command moves modified files from your working directory into the staging area (index) in preparation for a commit?",
                    "hint": "git ...",
                    "explanation": "`git add` stages changes for the next commit.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "git add",
                            "git commit",
                            "git push",
                            "git checkout",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Current Commit Reference",
                    "prompt": "What special four-letter keyword in Git points to the current active branch or commit checkout?",
                    "hint": "All uppercase.",
                    "explanation": "HEAD points to the currently checked-out commit or branch tip.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. HEAD"},
                    "solution": {"regex": True, "accept": [r"^HEAD$"]},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Git Best Practices",
                    "prompt": "Which of the following are recognized Git best practices for maintainable projects?",
                    "hint": "Think about commit sizes, commit messages, and secret management.",
                    "explanation": "Committing small logical units, writing clear imperative commit messages, and never committing secrets (.env files) are industry standards.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "Write clear, imperative commit messages describing what and why",
                            "Make small, focused commits rather than giant multi-thousand-line dumps",
                            "Always commit API keys and database passwords to version control",
                            "Use .gitignore to exclude node_modules, build artifacts, and secrets",
                        ]
                    },
                    "solution": {"answers": [0, 1, 3]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Detect Git Conflict Markers",
                    "prompt": "Write `has_conflict_markers(file_content)` that returns `True` if a file content string contains unresolved Git merge conflict markers (`<<<<<<<` or `>>>>>>>`), and `False` otherwise.\n\n```python\nhas_conflict_markers(\"console.log('clean');\") -> False\nhas_conflict_markers(\"<<<<<<< HEAD\\nvar a = 1;\\n=======\\nvar a = 2;\\n>>>>>>> feat\") -> True\n```",
                    "hint": "Check if `\"<<<<<<<\" in file_content or \">>>>>>>\" in file_content`.",
                    "explanation": "Automated CI checks frequently scan for stray merge conflict markers before building.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def has_conflict_markers(file_content):\n    # Return True if conflict markers are present\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "has_conflict_markers",
                        "cases": [
                            {"args": ["console.log('clean');"], "expect": False},
                            {"args": ["<<<<<<< HEAD\na = 1\n=======\na = 2\n>>>>>>> feat"], "expect": True},
                            {"args": [""], "expect": False},
                            {"args": ["<<<<<<< only start"], "expect": True},
                            {"args": ["clean text\nwith newlines"], "expect": False, "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 3: CONTAINERS & DOCKER FOUNDATIONS
        # =========================================================================
        {
            "index": 3,
            "title": "Containers & Docker Foundations",
            "summary": "VMs vs containers, namespaces, cgroups, Dockerfile instructions, layer caching, and port mapping.",
            "xp_reward": 105,
            "lessons": [
                {
                    "title": "The 'Works on My Machine' Dilemma: VMs vs Containers",
                    "minutes": 6,
                    "body": """Why does code that runs perfectly on your laptop crash the moment it deploys to production?
- Different Python / Node versions.
- Missing system libraries (e.g. `libpq-dev`).
- Different OS architectures (macOS vs Ubuntu Linux).

### Virtual Machines vs Containers
- **Virtual Machines (VMs)**: Each VM bundles a complete guest Operating System (several gigabytes), boots slowly, and runs on a hypervisor.
- **Containers (Docker)**: Lightweight processes that **share the host Linux kernel**. They provide isolated environments using Linux **Namespaces** (isolates PID, network, mounts) and **Control Groups (cgroups)** (limits CPU and RAM).

A container starts in 0.5 seconds and consumes almost zero idle overhead!""",
                },
                {
                    "title": "Dockerfile Anatomy & Layer Caching",
                    "minutes": 6,
                    "body": """A **Dockerfile** is the blueprint for creating a container image:

```dockerfile
# 1. Base image
FROM python:3.12-slim

# 2. Working directory inside container
WORKDIR /app

# 3. Layer Caching optimization: copy dependencies first!
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy application source code
COPY . .

# 5. Expose network port and define startup command
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

> [!TIP]
> **Why copy `requirements.txt` before application code?**
> Docker caches each build step (layer). If you edit one line of Python code, Docker reuses the cached `pip install` layer instead of redownloading 50 packages on every build!""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Docker Layer Caching Optimization",
                    "prompt": "Why should you COPY `package.json` or `requirements.txt` and install dependencies BEFORE copying the rest of your application code in a Dockerfile?",
                    "hint": "Think about what happens on rebuild when application code changes.",
                    "explanation": "Dependencies change much less frequently than application code. Copying them first allows Docker to reuse the cached dependency installation layer across builds.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "To take advantage of Docker layer caching and avoid reinstalling dependencies on every code change",
                            "Because Docker refuses to build if application code is copied first",
                            "To make the container run with root permissions",
                            "To automatically compress the image size by 90%",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "multi",
                    "difficulty": "easy",
                    "title": "Standard Dockerfile Instructions",
                    "prompt": "Which of the following are valid built-in Dockerfile instructions?",
                    "hint": "Keywords used to define image layers.",
                    "explanation": "FROM, WORKDIR, RUN, and CMD are core Dockerfile instructions. INSTALL is not a Dockerfile keyword (RUN is used).",
                    "xp": 25,
                    "config": {
                        "options": [
                            "FROM",
                            "WORKDIR",
                            "RUN",
                            "INSTALL",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2]},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Port Publishing Flag",
                    "prompt": "In the `docker run` command, which short flag publishes a container's internal port to the host machine (e.g. `-p 8080:80`)?",
                    "hint": "A single letter flag.",
                    "explanation": "-p (or --publish) maps host_port:container_port.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. -p"},
                    "solution": {"regex": True, "accept": [r"^-p$", r"^--publish$"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Generate Docker Run Command",
                    "prompt": "Write `build_docker_cmd(image, host_port, container_port, name)` returning a formatted bash command string:\n`\"docker run -d --name {name} -p {host_port}:{container_port} {image}\"`\n\n```python\nbuild_docker_cmd(\"postgres:17\", 5432, 5432, \"db\")\n# -> \"docker run -d --name db -p 5432:5432 postgres:17\"\n```",
                    "hint": "Use an f-string to assemble the arguments.",
                    "explanation": "Building clean CLI command strings is a common automation scripting task.",
                    "xp": 35,
                    "config": {
                        "language": "python",
                        "starter": "def build_docker_cmd(image, host_port, container_port, name):\n    # Return formatted docker run command string\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "build_docker_cmd",
                        "cases": [
                            {
                                "args": ["postgres:17", 5432, 5432, "db"],
                                "expect": "docker run -d --name db -p 5432:5432 postgres:17",
                            },
                            {
                                "args": ["nginx:alpine", 80, 80, "web"],
                                "expect": "docker run -d --name web -p 80:80 nginx:alpine",
                            },
                            {
                                "args": ["redis:latest", 6379, 6379, "cache"],
                                "expect": "docker run -d --name cache -p 6379:6379 redis:latest",
                                "hidden": True,
                            },
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 4: CI/CD AUTOMATION & SAFE DEPLOYS
        # =========================================================================
        {
            "index": 4,
            "title": "CI/CD Automation & Safe Deployments",
            "summary": "Continuous Integration, automated pipelines, GitHub Actions, Blue/Green deploys, and rollbacks.",
            "xp_reward": 115,
            "lessons": [
                {
                    "title": "What is CI/CD & Why Automate?",
                    "minutes": 6,
                    "body": """Manual deployments (SSH into server, run `git pull`, restart server) fail predictably: humans make typos, forget environment variables, or skip unit tests.

### Continuous Integration (CI)
Every time a developer opens a Pull Request:
1. A clean virtual machine spins up in the cloud.
2. Checks out the code and installs dependencies.
3. Runs linters, type checks (`tsc` / `mypy`), and the entire automated test suite.
4. If **any test fails**, merging is blocked automatically!

### Continuous Deployment (CD)
Once code is merged into `main`, the CD pipeline builds the Docker image, pushes it to a registry, and deploys it to the target cluster without manual intervention.""",
                },
                {
                    "title": "Safe Zero-Downtime Deployment Strategies",
                    "minutes": 6,
                    "body": """How do you deploy a new version when 5,000 active users are making requests right now?

### 1. Blue/Green Deployment
- **Blue**: The live environment serving current production traffic (v1.0).
- **Green**: An identical, parallel environment where you deploy and verify v2.0.
- Once verified, the load balancer switches all traffic to Green instantly!
- If an unexpected bug is spotted: switch back to Blue in 100 milliseconds!

### 2. Rolling Updates
Gradually replace containers one-by-one:
- Start 1 new v2.0 container.
- Wait for its health check to pass.
- Terminate 1 old v1.0 container.
- Repeat until 100% of containers are running v2.0.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Blue/Green Deployment Mechanics",
                    "prompt": "What is the defining characteristic of a Blue/Green deployment strategy?",
                    "hint": "Two identical environments.",
                    "explanation": "Blue/Green maintains two identical environments; new code is deployed to the idle environment, and traffic is switched at the router/load balancer level.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "Maintaining two identical production environments and instantly switching router traffic between them",
                            "Deploying code only on Tuesdays to avoid outages",
                            "Restarting the server without saving logs",
                            "Stopping all web traffic for 1 hour while updating the database",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "GitHub Actions Directory",
                    "prompt": "In what repository directory path are GitHub Actions workflow YAML files located?",
                    "hint": "Dot github slash...",
                    "explanation": ".github/workflows stores CI/CD pipeline definitions.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. .github/workflows"},
                    "solution": {"regex": True, "accept": [r"^\.?github/workflows/?$"]},
                },
                {
                    "kind": "multi",
                    "difficulty": "easy",
                    "title": "Essential CI Pipeline Steps",
                    "prompt": "Which of the following quality checks belong in an automated Pull Request CI pipeline?",
                    "hint": "Think about what verifies code correctness before merging.",
                    "explanation": "Linting, running automated tests, and scanning for security vulnerabilities ensure high code quality.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "Running unit and integration tests",
                            "Checking code linting and style formatting",
                            "Scanning dependencies for known security vulnerabilities",
                            "Posting the developer's home address on Twitter",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Evaluate Deployment Health",
                    "prompt": "Write `evaluate_health(error_rate_pct, p99_latency_ms)` that determines whether a new deployment should continue or trigger an automatic rollback:\n- If `error_rate_pct >= 2.0` OR `p99_latency_ms >= 500`: return `\"rollback\"`\n- Else if `error_rate_pct >= 0.5` OR `p99_latency_ms >= 250`: return `\"degraded\"`\n- Otherwise return `\"healthy\"`\n\n```python\nevaluate_health(0.1, 120) -> \"healthy\"\nevaluate_health(3.5, 100) -> \"rollback\"\nevaluate_health(0.6, 200) -> \"degraded\"\n```",
                    "hint": "Check rollback conditions first, then degraded, then healthy.",
                    "explanation": "Automated rollback logic protects uptime when canary deployments degrade.",
                    "xp": 40,
                    "config": {
                        "language": "python",
                        "starter": "def evaluate_health(error_rate_pct, p99_latency_ms):\n    # Return 'healthy', 'degraded', or 'rollback'\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "evaluate_health",
                        "cases": [
                            {"args": [0.1, 120], "expect": "healthy"},
                            {"args": [3.5, 100], "expect": "rollback"},
                            {"args": [0.1, 600], "expect": "rollback"},
                            {"args": [0.6, 200], "expect": "degraded"},
                            {"args": [0.0, 50], "expect": "healthy", "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 5: PRODUCTION OBSERVABILITY & SRE
        # =========================================================================
        {
            "index": 5,
            "title": "Production Observability & SRE",
            "summary": "Logs vs metrics vs traces, structured JSON logging, health checks, and the 4 Golden Signals.",
            "xp_reward": 125,
            "lessons": [
                {
                    "title": "The 3 Pillars of Observability",
                    "minutes": 6,
                    "body": """You cannot fix what you cannot see. When an outage occurs at 3 AM, how do you diagnose the root cause?

### 1. Logs
Discrete, timestamped records of events:
- In 12-factor apps, **never write to local log files**! Print structured JSON logs directly to `stdout`/`stderr`.
- A log collector (Datadog, Grafana Loki, CloudWatch) aggregates streams centrally.

### 2. Metrics
Aggregatable numerical values measured over time:
- CPU utilization (%), HTTP request rate (req/sec), 5xx error rate (%).
- Stored efficiently in time-series databases (Prometheus).

### 3. Distributed Tracing
Tracks a single request as it hops across multiple microservices (API gateway $\\rightarrow$ Auth service $\\rightarrow$ Database), visualizing exactly which database query took 800ms!""",
                },
                {
                    "title": "The 4 Golden Signals & Health Endpoints",
                    "minutes": 6,
                    "body": """Google Site Reliability Engineering (SRE) identifies the **Four Golden Signals**:
1. **Latency**: How long requests take to respond.
2. **Traffic**: Demand on your system (requests per second).
3. **Errors**: The rate of requests that fail (HTTP 5xx).
4. **Saturation**: How full your system is (memory % or connection pool usage).

### Health Check Endpoints (`/healthz`)
Load balancers ping a `/healthz` or `/health` endpoint every 5 seconds:
- Returns `200 OK`: Instance is healthy.
- Fails or times out 3 times in a row: Load balancer immediately stops sending user traffic to that container!""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "12-Factor App Logging Destination",
                    "prompt": "According to modern 12-Factor App principles, where should production containerized applications write their logs?",
                    "hint": "Standard output streams.",
                    "explanation": "Applications should treat logs as unbuffered event streams written directly to stdout/stderr.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "Standard output (stdout) and standard error (stderr)",
                            "A hardcoded file on local disk /tmp/app.log",
                            "Directly inside the PostgreSQL database table",
                            "Sent as email attachments to the sysadmin",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "The 4 Golden Signals of SRE",
                    "prompt": "Which of the following are Google SRE's 'Four Golden Signals' of system health?",
                    "hint": "Latency, Traffic, Errors, and...",
                    "explanation": "The 4 Golden Signals are Latency, Traffic, Errors, and Saturation.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "Latency",
                            "Traffic",
                            "Errors",
                            "Saturation",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2, 3]},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Standard Health Endpoint Path",
                    "prompt": "What common endpoint URL path (often ending with a 'z') is polled by container orchestrators like Kubernetes to check container health?",
                    "hint": "/health...",
                    "explanation": "/healthz is the standard Kubernetes liveness and readiness probe path.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. /healthz"},
                    "solution": {"regex": True, "accept": [r"^/healthz$", r"^/health$"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Calculate 5xx Error Rate Percentage",
                    "prompt": "Write `calculate_error_rate(status_codes)` that computes the percentage of HTTP 5xx server errors in a list of status codes.\n- 5xx errors are codes where `500 <= code <= 599`\n- Return the percentage as a float rounded to 2 decimal places (e.g. `12.5`)\n- If `status_codes` is empty, return `0.0`\n\n```python\ncalculate_error_rate([200, 200, 500, 200]) -> 25.0\ncalculate_error_rate([200, 404]) -> 0.0\ncalculate_error_rate([]) -> 0.0\n```",
                    "hint": "Count codes between 500 and 599, divide by `len(status_codes)`, multiply by 100, and use `round(val, 2)`.",
                    "explanation": "Calculating error rates is fundamental for automated alerting and SLO tracking.",
                    "xp": 40,
                    "config": {
                        "language": "python",
                        "starter": "def calculate_error_rate(status_codes):\n    # Return percentage of 5xx errors rounded to 2 decimals\n    ...\n",
                    },
                    "solution": {
                        "entrypoint": "calculate_error_rate",
                        "cases": [
                            {"args": [[200, 200, 500, 200]], "expect": 25.0},
                            {"args": [[200, 404]], "expect": 0.0},
                            {"args": [[]], "expect": 0.0},
                            {"args": [[500, 502, 503]], "expect": 100.0},
                            {"args": [[200, 201, 301, 400, 500]], "expect": 20.0, "hidden": True},
                        ],
                    },
                },
            ],
        },
    ],
}
