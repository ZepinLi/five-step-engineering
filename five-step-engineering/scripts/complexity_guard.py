#!/usr/bin/env python3
"""Enforce an earned-complexity invariant over a Git transition.

The guard deliberately measures only facts it can observe. It reports coarse
signals such as line growth and change entropy, but blocks only explicit
structural events, expired temporary work, declared external checks, and
unjustified changes to its own policy.
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import fnmatch
import hashlib
import json
import math
import shlex
import subprocess
import sys
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
DEFAULT_CONFIG_PATH = ".five-step-engineering.json"
DEFAULT_REPORT_PATH = ".five-step-engineering-report.json"
PLACEHOLDERS = {"n/a", "na", "none", "todo", "tbd", "unknown", "required"}


class GuardError(RuntimeError):
    """The evaluator could not produce a trustworthy verdict."""


def default_config() -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "scope": {
            "include": ["**"],
            "exclude": [
                ".git/**",
                "**/.git/**",
                "node_modules/**",
                "**/node_modules/**",
                "vendor/**",
                "**/vendor/**",
                "dist/**",
                "**/dist/**",
                "build/**",
                "**/build/**",
                "coverage/**",
                "**/coverage/**",
                DEFAULT_REPORT_PATH,
            ],
            "sensitive": [
                ".github/workflows/**",
                "migrations/**",
                "**/migrations/**",
                "package.json",
                "**/package.json",
                "pyproject.toml",
                "**/pyproject.toml",
                "Cargo.toml",
                "**/Cargo.toml",
                "go.mod",
                "**/go.mod",
            ],
        },
        "external_hard_checks": [],
        "temporary_items": [],
        "last_decision": None,
    }


def _run_git(repo: Path, args: Sequence[str], *, check: bool = True) -> bytes:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo,
            capture_output=True,
            check=False,
        )
    except OSError as exc:
        raise GuardError(f"cannot execute git: {exc}") from exc
    if check and result.returncode:
        message = result.stderr.decode("utf-8", "replace").strip()
        raise GuardError(f"git {' '.join(args)} failed: {message or result.returncode}")
    return result.stdout


def _resolve_commit(repo: Path, ref: str) -> str:
    raw = _run_git(repo, ["rev-parse", "--verify", f"{ref}^{{commit}}"])
    value = raw.decode().strip()
    if len(value) != 40:
        raise GuardError(f"{ref!r} did not resolve to a full commit")
    return value


def _json_bytes(raw: bytes, source: str) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GuardError(f"invalid JSON in {source}: {exc}") from exc
    if not isinstance(value, dict):
        raise GuardError(f"{source} must contain a JSON object")
    return value


def _config_at(repo: Path, ref: str, path: str) -> dict[str, Any] | None:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path}"],
        cwd=repo,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        return None
    return _json_bytes(result.stdout, f"{ref}:{path}")


def _string_list(value: Any, field: str, *, allow_empty: bool = True) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise GuardError(f"{field} must be a list of non-empty strings")
    if not allow_empty and not value:
        raise GuardError(f"{field} must not be empty")
    if len(set(value)) != len(value):
        raise GuardError(f"{field} must not contain duplicates")
    return list(value)


def _meaningful(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise GuardError(f"{field} must be a string")
    normalized = " ".join(value.split())
    if len(normalized) < 8 or normalized.lower() in PLACEHOLDERS:
        raise GuardError(f"{field} is missing or placeholder evidence")
    return normalized


def _validate_temporary_item(value: Any, field: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise GuardError(f"{field} must be an object")
    allowed = {"id", "owner", "paths", "review_by", "removal_condition", "decision_id"}
    unknown = set(value) - allowed
    if unknown:
        raise GuardError(f"{field} has unknown fields: {sorted(unknown)}")
    item_id = _meaningful(value.get("id"), f"{field}.id")
    owner = _meaningful(value.get("owner"), f"{field}.owner")
    paths = _string_list(value.get("paths", []), f"{field}.paths")
    review_by = value.get("review_by")
    if not isinstance(review_by, str):
        raise GuardError(f"{field}.review_by must be an ISO date")
    try:
        dt.date.fromisoformat(review_by)
    except ValueError as exc:
        raise GuardError(f"{field}.review_by must be an ISO date") from exc
    removal = _meaningful(value.get("removal_condition"), f"{field}.removal_condition")
    decision_id = _meaningful(value.get("decision_id"), f"{field}.decision_id")
    return {
        "id": item_id,
        "owner": owner,
        "paths": paths,
        "review_by": review_by,
        "removal_condition": removal,
        "decision_id": decision_id,
    }


def validate_config(value: Mapping[str, Any]) -> dict[str, Any]:
    allowed = {
        "schema_version",
        "scope",
        "external_hard_checks",
        "temporary_items",
        "last_decision",
    }
    unknown = set(value) - allowed
    if unknown:
        raise GuardError(f"configuration has unknown fields: {sorted(unknown)}")
    if value.get("schema_version") != SCHEMA_VERSION:
        raise GuardError(f"configuration schema_version must be {SCHEMA_VERSION}")
    scope = value.get("scope")
    if not isinstance(scope, dict) or set(scope) - {"include", "exclude", "sensitive"}:
        raise GuardError("scope must contain only include, exclude, and sensitive")
    include = _string_list(scope.get("include"), "scope.include", allow_empty=False)
    exclude = _string_list(scope.get("exclude", []), "scope.exclude")
    sensitive = _string_list(scope.get("sensitive", []), "scope.sensitive")
    hard_checks = _string_list(
        value.get("external_hard_checks", []), "external_hard_checks"
    )
    raw_items = value.get("temporary_items", [])
    if not isinstance(raw_items, list):
        raise GuardError("temporary_items must be a list")
    items = [
        _validate_temporary_item(item, f"temporary_items[{index}]")
        for index, item in enumerate(raw_items)
    ]
    ids = [item["id"] for item in items]
    if len(ids) != len(set(ids)):
        raise GuardError("temporary_items ids must be unique")
    decision = value.get("last_decision")
    if decision is not None and not isinstance(decision, dict):
        raise GuardError("last_decision must be null or an object")
    return {
        "schema_version": SCHEMA_VERSION,
        "scope": {"include": include, "exclude": exclude, "sensitive": sensitive},
        "external_hard_checks": hard_checks,
        "temporary_items": items,
        "last_decision": copy.deepcopy(decision),
    }


def _matches(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def _in_scope(path: str, scope: Mapping[str, list[str]]) -> bool:
    return _matches(path, scope["include"]) and not _matches(path, scope["exclude"])


def _tree_blobs(repo: Path, ref: str, scope: Mapping[str, list[str]]) -> list[tuple[str, str]]:
    raw = _run_git(repo, ["ls-tree", "-r", "-z", ref])
    result: list[tuple[str, str]] = []
    for record in raw.split(b"\0"):
        if not record:
            continue
        try:
            metadata, path_raw = record.split(b"\t", 1)
            _mode, kind, oid = metadata.decode("ascii").split()
            path = path_raw.decode("utf-8", "surrogateescape")
        except (ValueError, UnicodeDecodeError) as exc:
            raise GuardError("unexpected git ls-tree output") from exc
        if kind == "blob" and _in_scope(path, scope):
            result.append((path, oid))
    return result


def _read_exact(stream: Any, size: int) -> bytes:
    chunks: list[bytes] = []
    remaining = size
    while remaining:
        chunk = stream.read(remaining)
        if not chunk:
            raise GuardError("git cat-file ended before the declared blob size")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def _snapshot(repo: Path, ref: str, scope: Mapping[str, list[str]]) -> dict[str, int]:
    blobs = _tree_blobs(repo, ref, scope)
    text_files = 0
    nonblank_lines = 0
    with subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=repo,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ) as process:
        if process.stdin is None or process.stdout is None:
            process.kill()
            raise GuardError("could not open git cat-file pipes")
        for _path, oid in blobs:
            process.stdin.write(f"{oid}\n".encode("ascii"))
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii", "replace").strip().split()
            if len(header) != 3 or header[1] != "blob":
                raise GuardError(f"cannot read Git blob {oid}")
            content = _read_exact(process.stdout, int(header[2]))
            if process.stdout.read(1) != b"\n":
                raise GuardError("unexpected git cat-file record terminator")
            if b"\0" in content[:8192]:
                continue
            text_files += 1
            nonblank_lines += sum(1 for line in content.splitlines() if line.strip())
        process.stdin.close()
        process.wait(timeout=10)
        if process.returncode:
            error = process.stderr.read().decode("utf-8", "replace") if process.stderr else ""
            raise GuardError(f"git cat-file failed: {error.strip()}")
    return {
        "tracked_files": len(blobs),
        "text_files": text_files,
        "nonblank_lines": nonblank_lines,
    }


def _changed_files(repo: Path, base: str, head: str) -> dict[str, Any]:
    raw = _run_git(repo, ["diff", "--name-status", "-z", "--find-renames", base, head])
    fields = raw.split(b"\0")
    index = 0
    counts = {"added": 0, "deleted": 0, "modified": 0, "renamed": 0}
    paths: list[str] = []
    while index < len(fields) and fields[index]:
        token = fields[index]
        index += 1
        if b"\t" in token:
            status_raw, first_raw = token.split(b"\t", 1)
        else:
            status_raw = token
            if index >= len(fields):
                raise GuardError("unexpected git diff --name-status output")
            first_raw = fields[index]
            index += 1
        status = status_raw.decode("ascii", "replace")
        first = first_raw.decode("utf-8", "surrogateescape")
        if status.startswith(("R", "C")):
            if index >= len(fields):
                raise GuardError("rename record has no destination")
            second = fields[index].decode("utf-8", "surrogateescape")
            index += 1
            paths.extend([first, second])
            counts["renamed"] += 1
        else:
            paths.append(first)
            key = {"A": "added", "D": "deleted", "M": "modified"}.get(status[:1], "modified")
            counts[key] += 1
    return {**counts, "paths": sorted(set(paths))}


def _churn(repo: Path, base: str, head: str) -> dict[str, int]:
    raw = _run_git(repo, ["diff", "--numstat", "-z", "--no-renames", base, head])
    result: dict[str, int] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        parts = record.split(b"\t", 2)
        if len(parts) != 3:
            raise GuardError("unexpected git diff --numstat output")
        added_raw, deleted_raw, path_raw = parts
        path = path_raw.decode("utf-8", "surrogateescape")
        if added_raw == b"-" or deleted_raw == b"-":
            result[path] = 1
        else:
            result[path] = int(added_raw) + int(deleted_raw)
    return result


def _entropy(churn: Mapping[str, int]) -> dict[str, Any]:
    positive = {path: value for path, value in churn.items() if value > 0}
    total = sum(positive.values())
    if not total:
        return {"raw_bits": 0.0, "normalized": 0.0, "files": 0, "total_churn": 0}
    raw = -sum((value / total) * math.log2(value / total) for value in positive.values())
    normalized = raw / math.log2(len(positive)) if len(positive) > 1 else 0.0
    return {
        "raw_bits": round(raw, 6),
        "normalized": round(normalized, 6),
        "files": len(positive),
        "total_churn": total,
    }


def _policy_view(config: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "scope": config["scope"],
        "external_hard_checks": config["external_hard_checks"],
    }


def _candidate_deltas(
    base_snapshot: Mapping[str, int],
    head_snapshot: Mapping[str, int],
    changed: Mapping[str, Any],
    base_config: Mapping[str, Any],
    head_config: Mapping[str, Any],
) -> list[dict[str, Any]]:
    deltas: list[dict[str, Any]] = []
    if head_snapshot["tracked_files"] > base_snapshot["tracked_files"]:
        deltas.append(
            {
                "id": "tracked_files",
                "before": base_snapshot["tracked_files"],
                "after": head_snapshot["tracked_files"],
            }
        )
    sensitive_patterns = sorted(
        set(base_config["scope"]["sensitive"]) | set(head_config["scope"]["sensitive"])
    )
    sensitive = [
        path
        for path in changed["paths"]
        if path != DEFAULT_CONFIG_PATH and _matches(path, sensitive_patterns)
    ]
    if sensitive:
        deltas.append({"id": "sensitive_paths", "paths": sorted(sensitive)})
    if _policy_view(base_config) != _policy_view(head_config):
        changed_sections = [
            key
            for key in ("scope", "external_hard_checks")
            if base_config[key] != head_config[key]
        ]
        deltas.append({"id": "governance_policy", "sections": changed_sections})
    base_items = {item["id"]: item for item in base_config["temporary_items"]}
    head_items = {item["id"]: item for item in head_config["temporary_items"]}
    if base_items != head_items:
        deltas.append(
            {
                "id": "temporary_registry",
                "added": sorted(set(head_items) - set(base_items)),
                "removed": sorted(set(base_items) - set(head_items)),
                "changed": sorted(
                    key for key in set(base_items) & set(head_items) if base_items[key] != head_items[key]
                ),
            }
        )
    return deltas


def _canonical_delta(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _decision_issues(
    decision: Any,
    candidates: Sequence[Mapping[str, Any]],
    base_commit: str,
    temporary_items: Sequence[Mapping[str, Any]],
) -> list[str]:
    if not candidates:
        return []
    if not isinstance(decision, dict):
        return ["a current earned-complexity decision is required"]
    issues: list[str] = []
    allowed = {
        "id",
        "base_commit",
        "target",
        "force",
        "simplest_rejected_alternative",
        "observed_deltas",
        "evidence",
        "owner",
        "lifecycle",
        "removal_or_review_condition",
    }
    unknown = set(decision) - allowed
    if unknown:
        issues.append(f"last_decision has unknown fields: {sorted(unknown)}")
    for field in ("id", "target", "force", "simplest_rejected_alternative", "owner"):
        try:
            _meaningful(decision.get(field), f"last_decision.{field}")
        except GuardError as exc:
            issues.append(str(exc))
    if decision.get("base_commit") != base_commit:
        issues.append("last_decision.base_commit does not match the evaluated base commit")
    evidence = decision.get("evidence")
    if not isinstance(evidence, list) or not evidence:
        issues.append("last_decision.evidence must be a non-empty list")
    else:
        for index, item in enumerate(evidence):
            try:
                _meaningful(item, f"last_decision.evidence[{index}]")
            except GuardError as exc:
                issues.append(str(exc))
    lifecycle = decision.get("lifecycle")
    if lifecycle not in {"permanent", "temporary"}:
        issues.append("last_decision.lifecycle must be permanent or temporary")
    elif lifecycle == "temporary" and not any(
        item["decision_id"] == decision.get("id") for item in temporary_items
    ):
        issues.append("a temporary decision must own a registered temporary item")
    try:
        _meaningful(
            decision.get("removal_or_review_condition"),
            "last_decision.removal_or_review_condition",
        )
    except GuardError as exc:
        issues.append(str(exc))
    declared = decision.get("observed_deltas")
    if not isinstance(declared, list):
        issues.append("last_decision.observed_deltas must be a list")
    elif sorted(_canonical_delta(item) for item in declared) != sorted(
        _canonical_delta(item) for item in candidates
    ):
        issues.append("last_decision.observed_deltas does not exactly match observed structural deltas")
    return issues


def _expired_items(config: Mapping[str, Any], today: dt.date | None = None) -> list[dict[str, Any]]:
    current = today or dt.datetime.now(dt.timezone.utc).date()
    return [
        item
        for item in config["temporary_items"]
        if dt.date.fromisoformat(item["review_by"]) < current
    ]


def _external_checks(
    config: Mapping[str, Any], external_report: Path | None
) -> tuple[list[dict[str, Any]], list[str]]:
    required = set(config["external_hard_checks"])
    if not required:
        return [], []
    if external_report is None:
        return [], ["external hard checks are declared but no external report was supplied"]
    try:
        raw = external_report.read_bytes()
    except OSError as exc:
        return [], [f"cannot read external report: {exc}"]
    try:
        report = _json_bytes(raw, str(external_report))
    except GuardError as exc:
        return [], [str(exc)]
    if report.get("schema_version") != SCHEMA_VERSION or not isinstance(report.get("checks"), list):
        return [], ["external report must use schema_version 1 and contain checks"]
    by_id: dict[str, dict[str, Any]] = {}
    for index, check in enumerate(report["checks"]):
        if not isinstance(check, dict) or not isinstance(check.get("id"), str):
            return [], [f"external checks[{index}] is invalid"]
        if check.get("status") not in {"pass", "fail"}:
            return [], [f"external check {check['id']} has an invalid status"]
        by_id[check["id"]] = check
    missing = sorted(required - set(by_id))
    errors = [f"required external checks are missing: {missing}"] if missing else []
    failures = [by_id[item] for item in sorted(required) if item in by_id and by_id[item]["status"] == "fail"]
    return failures, errors


def _fingerprint(report: Mapping[str, Any]) -> str:
    payload = {
        "status": report["status"],
        "unearned_deltas": report["unearned_deltas"],
        "expired_temporary_items": [item["id"] for item in report["expired_temporary_items"]],
        "hard_check_failures": [item.get("id") for item in report["hard_check_failures"]],
        "evaluator_errors": report.get("evaluator_errors", []),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()[:16]


def evaluate(
    repo: Path,
    base_ref: str,
    head_ref: str,
    config_path: str,
    external_report: Path | None = None,
    *,
    head_config_override: Mapping[str, Any] | None = None,
    decision_override: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    base_commit = _resolve_commit(repo, base_ref)
    head_commit = _resolve_commit(repo, head_ref)
    base_raw = _config_at(repo, base_commit, config_path)
    head_raw = head_config_override or _config_at(repo, head_commit, config_path)
    if head_raw is None:
        raise GuardError(f"{config_path} is missing from {head_ref}")
    head_config = validate_config(head_raw)
    base_config = validate_config(base_raw) if base_raw is not None else validate_config(default_config())
    base_snapshot = _snapshot(repo, base_commit, base_config["scope"])
    head_snapshot = _snapshot(repo, head_commit, head_config["scope"])
    changed = _changed_files(repo, base_commit, head_commit)
    churn = {
        path: value
        for path, value in _churn(repo, base_commit, head_commit).items()
        if _in_scope(path, base_config["scope"]) or _in_scope(path, head_config["scope"])
    }
    candidates = _candidate_deltas(
        base_snapshot, head_snapshot, changed, base_config, head_config
    )
    decision = decision_override if decision_override is not None else head_config["last_decision"]
    decision_issues = _decision_issues(
        decision, candidates, base_commit, head_config["temporary_items"]
    )
    unearned = list(candidates) if decision_issues else []
    expired = _expired_items(head_config)
    hard_failures, evaluator_errors = _external_checks(head_config, external_report)
    status = "evaluator_error" if evaluator_errors else (
        "unresolved" if unearned or expired or hard_failures else "pass"
    )
    script = shlex.quote(str(Path(sys.argv[0])))
    rerun = (
        f"python3 {script} check --repo {shlex.quote(str(repo))} "
        f"--base {shlex.quote(base_ref)} --head {shlex.quote(head_ref)} "
        f"--config {shlex.quote(config_path)}"
    )
    if external_report is not None:
        rerun += f" --external-report {shlex.quote(str(external_report))}"
    report: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "status": status,
        "base_commit": base_commit,
        "head_commit": head_commit,
        "observations": {
            "base": base_snapshot,
            "head": head_snapshot,
            "delta": {
                key: head_snapshot[key] - base_snapshot[key]
                for key in base_snapshot
            },
            "changed_files": changed,
            "change_entropy": _entropy(churn),
        },
        "unearned_deltas": unearned,
        "expired_temporary_items": expired,
        "hard_check_failures": hard_failures,
        "diagnostics": [
            {
                "id": "line_growth",
                "severity": "observe",
                "value": head_snapshot["nonblank_lines"] - base_snapshot["nonblank_lines"],
                "note": "Line count is a diagnostic, never a design verdict.",
            },
            {
                "id": "change_entropy",
                "severity": "observe",
                "value": _entropy(churn)["normalized"],
                "note": "Higher dispersion can reveal cross-cutting change; it is not intrinsically bad.",
            },
        ],
        "decision_issues": decision_issues,
        "evaluator_errors": evaluator_errors,
        "failure_fingerprint": "",
        "rerun_command": rerun,
    }
    report["failure_fingerprint"] = _fingerprint(report)
    return report


def _error_report(message: str, base: str, head: str, command: str) -> dict[str, Any]:
    report = {
        "schema_version": SCHEMA_VERSION,
        "status": "evaluator_error",
        "base_commit": base,
        "head_commit": head,
        "observations": {},
        "unearned_deltas": [],
        "expired_temporary_items": [],
        "hard_check_failures": [],
        "diagnostics": [],
        "decision_issues": [],
        "evaluator_errors": [message],
        "failure_fingerprint": "",
        "rerun_command": command,
    }
    report["failure_fingerprint"] = _fingerprint(report)
    return report


def _markdown_summary(report: Mapping[str, Any]) -> str:
    icon = {"pass": "✅", "unresolved": "⏳", "evaluator_error": "❌"}[report["status"]]
    lines = [
        "## Five-Step Engineering complexity guard",
        "",
        f"{icon} **{report['status']}** · `{report['failure_fingerprint']}`",
        "",
    ]
    if report["unearned_deltas"]:
        lines.append("### Unearned structural deltas")
        lines.extend(f"- `{item['id']}`" for item in report["unearned_deltas"])
        lines.append("")
    if report["expired_temporary_items"]:
        lines.append("### Expired temporary items")
        lines.extend(f"- `{item['id']}` — review was due {item['review_by']}" for item in report["expired_temporary_items"])
        lines.append("")
    if report["hard_check_failures"]:
        lines.append("### Failed external checks")
        lines.extend(f"- `{item.get('id', 'unknown')}`" for item in report["hard_check_failures"])
        lines.append("")
    for issue in report.get("decision_issues", []):
        lines.append(f"- Decision: {issue}")
    for issue in report.get("evaluator_errors", []):
        lines.append(f"- Evaluator: {issue}")
    if report["status"] != "pass":
        lines.extend(
            [
                "",
                "The gate blocks promotion, not problem solving. Resolve the smallest item through a nested five-step loop, then rerun:",
                "",
                f"`{report['rerun_command']}`",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def _emit(report: Mapping[str, Any], report_path: Path | None, summary_path: Path | None) -> None:
    encoded = json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(encoded, encoding="utf-8")
    if summary_path is not None:
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        with summary_path.open("a", encoding="utf-8") as handle:
            handle.write(_markdown_summary(report))
    sys.stdout.write(encoded)


def _workflow(action_ref: str) -> str:
    return f"""name: complexity-guard

on:
  pull_request:

permissions:
  contents: read

jobs:
  complexity-guard:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
        with:
          fetch-depth: 0
      - uses: ZepinLi/five-step-engineering@{action_ref}
        with:
          base-ref: ${{{{ github.event.pull_request.base.sha }}}}
          head-ref: ${{{{ github.event.pull_request.head.sha }}}}
"""


CHECKLIST = """## Five-Step Engineering

- [ ] The real constraint and simplest direct baseline are named.
- [ ] Positive structural deltas are recorded in `.five-step-engineering.json`.
- [ ] Superseded paths and temporary investigative structure were removed.
- [ ] Every retained temporary item has an owner, review date, and removal condition.
- [ ] Relevant behavior, architecture, and failure checks pass.
"""


def _init(repo: Path, write: bool, action_ref: str) -> int:
    files = {
        repo / DEFAULT_CONFIG_PATH: json.dumps(default_config(), indent=2, sort_keys=True) + "\n",
        repo / ".github/workflows/five-step-engineering.yml": _workflow(action_ref),
        repo / ".github/pull_request_template.md": CHECKLIST,
    }
    if not write:
        for path, content in files.items():
            print(f"--- {path.relative_to(repo)}")
            print(content, end="")
        return 0
    existing = [str(path.relative_to(repo)) for path in files if path.exists()]
    if existing:
        raise GuardError(f"refusing to overwrite existing files: {existing}")
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return 0


def _load_worktree_config(repo: Path, path: str) -> dict[str, Any]:
    target = repo / path
    try:
        return validate_config(_json_bytes(target.read_bytes(), str(target)))
    except OSError as exc:
        raise GuardError(f"cannot read {target}: {exc}") from exc


def _accept(args: argparse.Namespace) -> int:
    repo = Path(args.repo).resolve()
    config = _load_worktree_config(repo, args.config)
    decision = _json_bytes(Path(args.decision).read_bytes(), args.decision)
    report = evaluate(
        repo,
        args.base,
        args.head,
        args.config,
        Path(args.external_report) if args.external_report else None,
        head_config_override=config,
        decision_override=decision,
    )
    if report["evaluator_errors"] or report["expired_temporary_items"] or report["hard_check_failures"]:
        _emit(report, None, None)
        return 3 if report["evaluator_errors"] else 2
    if report["unearned_deltas"]:
        _emit(report, None, None)
        return 2
    config["last_decision"] = decision
    target = repo / args.config
    target.write_text(json.dumps(config, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    _emit(report, None, None)
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="print or create an opt-in project configuration")
    init.add_argument("--repo", default=".")
    init.add_argument("--write", action="store_true")
    init.add_argument("--action-ref", default="v1.0.0")

    for name in ("inspect", "check"):
        command = subparsers.add_parser(name)
        command.add_argument("--repo", default=".")
        command.add_argument("--base", required=True)
        command.add_argument("--head", required=True)
        command.add_argument("--config", default=DEFAULT_CONFIG_PATH)
        command.add_argument("--external-report")
        command.add_argument("--report")
        command.add_argument("--summary")

    accept = subparsers.add_parser("accept", help="validate and record an earned-complexity decision")
    accept.add_argument("--repo", default=".")
    accept.add_argument("--base", required=True)
    accept.add_argument("--head", required=True)
    accept.add_argument("--config", default=DEFAULT_CONFIG_PATH)
    accept.add_argument("--external-report")
    accept.add_argument("--decision", required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.command == "init":
        try:
            return _init(Path(args.repo).resolve(), args.write, args.action_ref)
        except GuardError as exc:
            parser.error(str(exc))
    if args.command == "accept":
        try:
            return _accept(args)
        except (GuardError, OSError) as exc:
            parser.error(str(exc))

    repo = Path(args.repo).resolve()
    command = " ".join(shlex.quote(item) for item in sys.argv)
    try:
        report = evaluate(
            repo,
            args.base,
            args.head,
            args.config,
            Path(args.external_report) if args.external_report else None,
        )
    except GuardError as exc:
        report = _error_report(str(exc), args.base, args.head, command)
    _emit(
        report,
        Path(args.report) if args.report else None,
        Path(args.summary) if args.summary else None,
    )
    if report["status"] == "evaluator_error":
        return 3
    if args.command == "check" and report["status"] == "unresolved":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
