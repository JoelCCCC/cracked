"""Turns a raw submission into a verdict. Never leaks the stored answer."""

from __future__ import annotations

import re

from curriculum.models import Challenge
from runner import executor


def _normalize(text):
    return re.sub(r"\s+", " ", str(text or "")).strip()


def grade(challenge: Challenge, submission: dict) -> tuple[bool, dict]:
    kind = challenge.kind
    solution = challenge.solution or {}

    if kind == Challenge.Kind.MCQ:
        choice = submission.get("choice")
        if choice is None:
            choice = submission.get("answer")
        if choice is not None:
            try:
                choice = int(choice)
            except (ValueError, TypeError):
                pass
        return choice == solution.get("answer"), {}

    if kind == Challenge.Kind.MULTI:
        chosen = submission.get("choices")
        if chosen is None:
            chosen = submission.get("answers")
        if not isinstance(chosen, list):
            return False, {"error": "Pick at least one option."}
        parsed = []
        for x in chosen:
            try:
                parsed.append(int(x))
            except (ValueError, TypeError):
                parsed.append(x)
        return set(parsed) == set(solution.get("answers", [])), {}

    if kind == Challenge.Kind.SHORT:
        given = _normalize(submission.get("text"))
        if not given:
            return False, {"error": "Write an answer first."}
        flags = re.IGNORECASE if solution.get("ignore_case", True) else 0
        for pattern in solution.get("accept", []):
            if solution.get("regex"):
                if re.fullmatch(pattern, given, flags):
                    return True, {}
            elif _normalize(pattern).lower() == given.lower():
                return True, {}
        return False, {}

    if kind == Challenge.Kind.CODE:
        source = submission.get("source") or ""
        if not source.strip():
            return False, {"error": "Write some code first."}
        language = (challenge.config or {}).get("language", "python")
        result = executor.run(
            language=language,
            source=source,
            entrypoint=solution.get("entrypoint", "solve"),
            cases=solution.get("cases", []),
        )
        detail = result.as_dict()
        # Only reveal the cases flagged public, plus a pass/fail tally.
        visible = [c for c, spec in zip(detail["cases"], solution.get("cases", [])) if not spec.get("hidden")]
        detail["cases"] = visible
        detail["passed_count"] = sum(1 for c in result.cases if c.get("passed"))
        detail["total_count"] = len(result.cases)
        return result.passed, detail

    return False, {"error": f"Unknown challenge type: {kind}"}
