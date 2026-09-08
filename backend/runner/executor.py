"""Runs learner-submitted code against a challenge's test cases.

Security note: this executes the submission as a subprocess of the API server
with rlimits and a wall-clock timeout. That is adequate for local development
and a trusted cohort. Before exposing this to the open internet, move the
`_spawn` call into a container/gVisor/Firecracker sandbox with no network.
Set ENABLE_CODE_RUNNER=0 to turn code grading off entirely.
"""

from __future__ import annotations

import json
import os
import resource
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field

from django.conf import settings

PY_HARNESS = r'''
import json, os, sys, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.setrecursionlimit(20000)
payload = json.load(sys.stdin)
out = {"cases": []}
try:
    import solution
except BaseException:
    out["error"] = "Your code failed to load:\n" + traceback.format_exc(limit=2)
    print(json.dumps(out)); raise SystemExit(0)

fn = getattr(solution, payload["entrypoint"], None)
if not callable(fn):
    out["error"] = "Define a function named `%s`." % payload["entrypoint"]
    print(json.dumps(out)); raise SystemExit(0)

for case in payload["cases"]:
    row = {"args": case.get("args", []), "expect": case.get("expect")}
    try:
        got = fn(*case.get("args", []))
        row["got"] = json.loads(json.dumps(got, default=repr))
        row["passed"] = row["got"] == row["expect"]
    except BaseException as exc:
        row["got"] = None
        row["passed"] = False
        row["error"] = "%s: %s" % (type(exc).__name__, exc)
    out["cases"].append(row)
print(json.dumps(out))
'''

JS_HARNESS = r'''
const fs = require('fs');
const payload = JSON.parse(fs.readFileSync(0, 'utf8'));
const out = { cases: [] };
let solution;
try {
  solution = require('./solution.js');
} catch (err) {
  out.error = 'Your code failed to load:\n' + (err && err.message);
  console.log(JSON.stringify(out));
  process.exit(0);
}
const fn = solution[payload.entrypoint] ?? global[payload.entrypoint];
if (typeof fn !== 'function') {
  out.error = 'Export a function named `' + payload.entrypoint + '` (module.exports = { ' + payload.entrypoint + ' }).';
  console.log(JSON.stringify(out));
  process.exit(0);
}
for (const c of payload.cases) {
  const row = { args: c.args ?? [], expect: c.expect ?? null };
  try {
    const got = fn(...(c.args ?? []));
    row.got = JSON.parse(JSON.stringify(got ?? null));
    row.passed = JSON.stringify(row.got) === JSON.stringify(row.expect ?? null);
  } catch (err) {
    row.got = null;
    row.passed = false;
    row.error = String(err && err.message ? err.message : err);
  }
  out.cases.push(row);
}
console.log(JSON.stringify(out));
'''

LANGUAGES = {
    "python": {"file": "solution.py", "harness": ("harness.py", PY_HARNESS)},
    "javascript": {"file": "solution.js", "harness": ("harness.js", JS_HARNESS)},
}


@dataclass
class RunResult:
    passed: bool
    error: str = ""
    cases: list = field(default_factory=list)

    def as_dict(self):
        return {"passed": self.passed, "error": self.error, "cases": self.cases}


def _limits():
    cpu = int(settings.CODE_RUNNER_TIMEOUT_SECONDS) + 1
    resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))
    resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_FSIZE, (4 * 1024 * 1024,) * 2)
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    os.setsid()


def _interpreter(language):
    if language == "python":
        return [sys.executable, "-I", "-B"]
    node = shutil.which("node")
    return [node] if node else None


def run(language: str, source: str, entrypoint: str, cases: list) -> RunResult:
    if not settings.ENABLE_CODE_RUNNER:
        return RunResult(False, error="Code grading is disabled on this server.")
    spec = LANGUAGES.get(language)
    if not spec:
        return RunResult(False, error=f"Unsupported language: {language}")
    argv = _interpreter(language)
    if not argv:
        return RunResult(False, error=f"No interpreter available for {language}.")

    workdir = tempfile.mkdtemp(prefix="cracked-run-")
    try:
        with open(os.path.join(workdir, spec["file"]), "w") as fh:
            fh.write(source)
        harness_name, harness_src = spec["harness"]
        with open(os.path.join(workdir, harness_name), "w") as fh:
            fh.write(harness_src)

        payload = json.dumps({"entrypoint": entrypoint, "cases": cases})
        try:
            proc = subprocess.run(
                argv + [harness_name],
                cwd=workdir,
                input=payload,
                capture_output=True,
                text=True,
                timeout=settings.CODE_RUNNER_TIMEOUT_SECONDS,
                preexec_fn=_limits,
                env={"PATH": "/usr/bin:/bin", "HOME": workdir, "NODE_PATH": workdir},
            )
        except subprocess.TimeoutExpired:
            return RunResult(False, error="Timed out. Look for an infinite loop or a runaway recursion.")

        stdout = (proc.stdout or "").strip().splitlines()
        if not stdout:
            return RunResult(False, error=(proc.stderr or "Your program produced no output.")[-2000:])
        try:
            data = json.loads(stdout[-1])
        except json.JSONDecodeError:
            return RunResult(False, error=(proc.stderr or proc.stdout)[-2000:])

        if data.get("error"):
            return RunResult(False, error=data["error"])
        rows = data.get("cases", [])
        return RunResult(passed=bool(rows) and all(r.get("passed") for r in rows), cases=rows)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
