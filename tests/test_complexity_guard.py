from __future__ import annotations

from contextlib import redirect_stdout
import copy
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "five-step-engineering/scripts/complexity_guard.py"
SPEC = importlib.util.spec_from_file_location("complexity_guard", SCRIPT)
assert SPEC and SPEC.loader
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


class GitRepo:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.git("init", "-q")
        self.git("config", "user.email", "guard@example.com")
        self.git("config", "user.name", "Complexity Guard")

    def git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args],
            cwd=self.root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return result.stdout.strip()

    def write(self, path: str, content: str) -> None:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def config(self, value: dict | None = None) -> dict:
        current = copy.deepcopy(value or guard.default_config())
        self.write(guard.DEFAULT_CONFIG_PATH, json.dumps(current, indent=2, sort_keys=True) + "\n")
        return current

    def commit(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-qm", message)
        return self.git("rev-parse", "HEAD")


class ComplexityGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = GitRepo(Path(self.temp.name))

    def report(self, base: str, head: str, external: Path | None = None) -> dict:
        return guard.evaluate(
            self.repo.root,
            base,
            head,
            guard.DEFAULT_CONFIG_PATH,
            external,
        )

    def earned_decision(self, base: str, deltas: list[dict], **changes: object) -> dict:
        value: dict = {
            "id": "feature-order-export",
            "base_commit": base,
            "target": "Export orders in the requested interoperable format",
            "force": "A verified consumer requires the new export capability",
            "simplest_rejected_alternative": "The existing endpoint cannot represent the required format",
            "observed_deltas": deltas,
            "evidence": ["The integration test exercises the consumer contract"],
            "owner": "The orders component owns this capability and its lifecycle",
            "lifecycle": "permanent",
            "removal_or_review_condition": "Review when the consumer contract is retired or replaced",
        }
        value.update(changes)
        return value

    def test_unchanged_transition_passes(self) -> None:
        self.repo.config()
        self.repo.write("src/app.py", "print('ok')\n")
        commit = self.repo.commit("initial")

        report = self.report(commit, commit)

        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["unearned_deltas"], [])

    def test_pure_deletion_passes(self) -> None:
        self.repo.config()
        self.repo.write("src/obsolete.py", "value = 1\n")
        base = self.repo.commit("initial")
        (self.repo.root / "src/obsolete.py").unlink()
        head = self.repo.commit("delete obsolete path")

        report = self.report(base, head)

        self.assertEqual(report["status"], "pass")
        self.assertLess(report["observations"]["delta"]["tracked_files"], 0)

    def test_rename_is_observed_without_becoming_growth(self) -> None:
        self.repo.config()
        self.repo.write("src/old_name.py", "value = 1\n")
        base = self.repo.commit("initial")
        self.repo.git("mv", "src/old_name.py", "src/new_name.py")
        head = self.repo.commit("rename module")

        report = self.report(base, head)

        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["observations"]["changed_files"]["renamed"], 1)

    def test_unearned_file_growth_is_unresolved(self) -> None:
        self.repo.config()
        base = self.repo.commit("initial")
        self.repo.write("src/new.py", "value = 1\n")
        head = self.repo.commit("add unexplained structure")

        report = self.report(base, head)

        self.assertEqual(report["status"], "unresolved")
        self.assertEqual(report["unearned_deltas"][0]["id"], "tracked_files")

    def test_exact_earned_decision_resolves_growth(self) -> None:
        config = self.repo.config()
        base = self.repo.commit("initial")
        self.repo.write("src/export.py", "def export():\n    return 'csv'\n")
        provisional = self.repo.commit("add required export")
        deltas = self.report(base, provisional)["unearned_deltas"]
        config["last_decision"] = self.earned_decision(base, deltas)
        self.repo.config(config)
        head = self.repo.commit("record earned complexity")

        report = self.report(base, head)

        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["decision_issues"], [])

    def test_placeholder_decision_does_not_resolve_growth(self) -> None:
        config = self.repo.config()
        base = self.repo.commit("initial")
        self.repo.write("src/export.py", "value = 1\n")
        provisional = self.repo.commit("add export")
        deltas = self.report(base, provisional)["unearned_deltas"]
        config["last_decision"] = self.earned_decision(base, deltas, force="TBD")
        self.repo.config(config)
        head = self.repo.commit("add placeholder decision")

        report = self.report(base, head)

        self.assertEqual(report["status"], "unresolved")
        self.assertTrue(any("placeholder" in issue for issue in report["decision_issues"]))

    def test_temporary_decision_requires_registered_item(self) -> None:
        config = self.repo.config()
        base = self.repo.commit("initial")
        self.repo.write("src/adapter.py", "value = 1\n")
        provisional = self.repo.commit("add temporary adapter")
        deltas = self.report(base, provisional)["unearned_deltas"]
        config["last_decision"] = self.earned_decision(
            base,
            deltas,
            lifecycle="temporary",
        )
        self.repo.config(config)
        head = self.repo.commit("record incomplete temporary decision")

        report = self.report(base, head)

        self.assertEqual(report["status"], "unresolved")
        self.assertTrue(any("registered temporary item" in issue for issue in report["decision_issues"]))

    def test_expired_temporary_item_blocks_promotion(self) -> None:
        config = self.repo.config()
        config["temporary_items"] = [
            {
                "id": "legacy-format-adapter",
                "owner": "The migration owner tracks removal of the adapter",
                "paths": ["src/legacy.py"],
                "review_by": "2000-01-01",
                "removal_condition": "Remove after all clients use the current format",
                "decision_id": "migration-compatibility-window",
            }
        ]
        self.repo.config(config)
        commit = self.repo.commit("track temporary adapter")

        report = self.report(commit, commit)

        self.assertEqual(report["status"], "unresolved")
        self.assertEqual(report["expired_temporary_items"][0]["id"], "legacy-format-adapter")

    def test_entropy_and_line_growth_are_diagnostic_only(self) -> None:
        self.repo.config()
        self.repo.write("src/a.py", "a = 1\n")
        self.repo.write("src/b.py", "b = 1\n")
        base = self.repo.commit("initial")
        self.repo.write("src/a.py", "a = 1\na2 = 2\n")
        self.repo.write("src/b.py", "b = 1\nb2 = 2\n")
        head = self.repo.commit("change two existing files")

        report = self.report(base, head)

        self.assertEqual(report["status"], "pass")
        self.assertGreater(report["observations"]["change_entropy"]["normalized"], 0)
        self.assertGreater(report["observations"]["delta"]["nonblank_lines"], 0)

    def test_external_hard_check_failure_blocks(self) -> None:
        config = self.repo.config()
        config["external_hard_checks"] = ["dependency-cycles"]
        self.repo.config(config)
        commit = self.repo.commit("require cycle check")
        external = self.repo.root / "external.json"
        external.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "checks": [
                        {
                            "id": "dependency-cycles",
                            "status": "fail",
                            "evidence": "A cycle crosses the domain boundary",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

        report = self.report(commit, commit, external)

        self.assertEqual(report["status"], "unresolved")
        self.assertEqual(report["hard_check_failures"][0]["id"], "dependency-cycles")

    def test_missing_external_report_is_evaluator_error(self) -> None:
        config = self.repo.config()
        config["external_hard_checks"] = ["dependency-cycles"]
        self.repo.config(config)
        commit = self.repo.commit("require cycle check")

        report = self.report(commit, commit)

        self.assertEqual(report["status"], "evaluator_error")

    def test_excluded_generated_file_does_not_create_growth(self) -> None:
        self.repo.config()
        base = self.repo.commit("initial")
        self.repo.write("vendor/generated.py", "generated = True\n")
        head = self.repo.commit("add generated vendor file")

        report = self.report(base, head)

        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["observations"]["delta"]["tracked_files"], 0)

    def test_policy_change_requires_governance_decision(self) -> None:
        config = self.repo.config()
        base = self.repo.commit("initial")
        config["scope"]["exclude"].append("generated/**")
        self.repo.config(config)
        head = self.repo.commit("weaken tracked scope")

        report = self.report(base, head)

        self.assertEqual(report["status"], "unresolved")
        self.assertIn("governance_policy", {item["id"] for item in report["unearned_deltas"]})

    def test_sensitive_change_requires_decision(self) -> None:
        self.repo.config()
        self.repo.write("pyproject.toml", "[project]\nname='sample'\n")
        base = self.repo.commit("initial")
        self.repo.write("pyproject.toml", "[project]\nname='sample'\ndependencies=[]\n")
        head = self.repo.commit("change manifest")

        report = self.report(base, head)

        self.assertEqual(report["status"], "unresolved")
        self.assertIn("sensitive_paths", {item["id"] for item in report["unearned_deltas"]})

    def test_missing_base_ref_returns_evaluator_exit_code(self) -> None:
        self.repo.config()
        head = self.repo.commit("initial")
        output = io.StringIO()
        with redirect_stdout(output):
            code = guard.main(
                [
                    "check",
                    "--repo",
                    str(self.repo.root),
                    "--base",
                    "missing",
                    "--head",
                    head,
                ]
            )

        self.assertEqual(code, 3)
        self.assertEqual(json.loads(output.getvalue())["status"], "evaluator_error")

    def test_invalid_head_configuration_is_evaluator_error(self) -> None:
        self.repo.config()
        base = self.repo.commit("initial")
        self.repo.write(guard.DEFAULT_CONFIG_PATH, "{not json}\n")
        head = self.repo.commit("break configuration")
        output = io.StringIO()
        with redirect_stdout(output):
            code = guard.main(
                [
                    "check",
                    "--repo",
                    str(self.repo.root),
                    "--base",
                    base,
                    "--head",
                    head,
                ]
            )

        self.assertEqual(code, 3)
        self.assertEqual(json.loads(output.getvalue())["status"], "evaluator_error")

    def test_accept_records_only_an_exact_decision(self) -> None:
        self.repo.config()
        base = self.repo.commit("initial")
        self.repo.write("src/export.py", "value = 1\n")
        head = self.repo.commit("add export")
        deltas = self.report(base, head)["unearned_deltas"]
        decision = self.repo.root / "decision.json"
        decision.write_text(json.dumps(self.earned_decision(base, deltas)), encoding="utf-8")
        output = io.StringIO()
        with redirect_stdout(output):
            code = guard.main(
                [
                    "accept",
                    "--repo",
                    str(self.repo.root),
                    "--base",
                    base,
                    "--head",
                    head,
                    "--decision",
                    str(decision),
                ]
            )

        self.assertEqual(code, 0)
        saved = json.loads((self.repo.root / guard.DEFAULT_CONFIG_PATH).read_text())
        self.assertEqual(saved["last_decision"]["id"], "feature-order-export")

    def test_init_refuses_to_overwrite_existing_files(self) -> None:
        self.repo.config()

        with self.assertRaises(guard.GuardError):
            guard._init(self.repo.root, True, "v1.0.0")

    def test_init_writes_a_pinned_workflow_and_checklist(self) -> None:
        code = guard._init(self.repo.root, True, "v1.0.0")

        self.assertEqual(code, 0)
        workflow = (self.repo.root / ".github/workflows/five-step-engineering.yml").read_text()
        checklist = (self.repo.root / ".github/pull_request_template.md").read_text()
        self.assertIn("ZepinLi/five-step-engineering@v1.0.0", workflow)
        self.assertIn("actions/checkout@11d5960a", workflow)
        self.assertIn("Positive structural deltas", checklist)


if __name__ == "__main__":
    unittest.main()
