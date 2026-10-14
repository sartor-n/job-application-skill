"""Behavioral invariants for readiness, persistence and host-independent scripts.

Run: python -m unittest discover -s tests -p 'test_workflow.py' -v
All generated data lives in temporary fixture directories, never the real profile.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
sys.path.insert(0, str(SKILL / "tests"))
from check_profile import validate_profile
from check_readiness import AREAS, fingerprints, tailoring_errors
from record_learning import record, show
import test_parser


def write_yaml(path, value):
    Path(path).write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2), encoding="utf-8")


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="job-application-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.pdir = self.root / "profile"
        self.pdir.mkdir()
        (self.pdir / "knowledge").mkdir()
        self.app = self.root / "applications" / "first"
        self.app.mkdir(parents=True)
        self.profile = {
            "schema_version": 2, "onboarding_complete": True,
            "identity": {"name": "Test Candidate", "headline": "Product Manager"},
            "contact": {"email": "", "show_phone": False},
            "markets": [{"code": "UK", "page_limit": 2, "english": "british"}],
            "style": {}, "render": {"filename_pattern": "{name} - {company} - {position} {doc}"},
        }
        write_yaml(self.pdir / "profile.yaml", self.profile)
        write_yaml(self.pdir / "archetypes.yaml", {
            "archetypes": [{"tag": "IC", "target_titles": ["Senior Product Manager"]}]})
        self.story = "I interviewed support colleagues and redesigned handoff notes, ending the recurring ownership disputes."
        self.history = "Product Manager at Example, January 2023 to present, following a support analyst role."
        self.strength = "I translate ambiguous service problems into clear decisions, as the handoff redesign demonstrates."
        self.goals = "I want a senior IC product role with customer discovery and growth in technical judgment."
        self.wishes = "I prefer hybrid work and direct customer access; I am not seeking line-management responsibility."
        self.boundaries = "I contributed to delivery with engineers; I did not manage the engineering team."
        master = ("---\nread_only: true\n---\n# Master CV: Test Candidate\n\n# PROFILE\n"
                  + self.strength + "\n\n# WORK EXPERIENCE\n\n## Product Manager | Example [ALL]\n"
                  + "01/2023 - Present\n\n" + self.history + "\n\n* " + self.story + "\n")
        (self.pdir / "master_cv.md").write_text(master, encoding="utf-8")
        (self.pdir / "preferences.md").write_text(
            "# Preferences\n\n## Career Direction and Hopes\n" + self.goals
            + "\n\n## Working Preferences and Tradeoffs\n" + self.wishes
            + "\n\n## Claim Boundaries\n" + self.boundaries + "\n", encoding="utf-8")
        quotes = (self.history, self.story, self.strength, self.goals, self.wishes, self.boundaries)
        self.background = {"schema_version": 2, "reviewed_at": "2026-09-25", "areas": {}, "blocking_questions": []}
        for index, area in enumerate(AREAS):
            self.background["areas"][area] = {
                "status": "ready", "summary": quotes[index],
                "evidence": [{"path": "master_cv.md" if index < 3 else "preferences.md", "quote": quotes[index]}],
            }
        write_yaml(self.pdir / "readiness.yaml", self.background)
        self.metadata = {
            "company": "Example", "position": "Product Manager", "market": "UK", "archetype": "IC",
            "status": "roasted", "tailoring_approved": True,
        }
        write_json(self.app / "metadata.json", self.metadata)
        write_json(self.app / "learning.json", {"schema_version": 1, "entries": []})
        (self.app / "job_description.md").write_text("# Job\nMust have: product discovery and service improvement.\n", encoding="utf-8")
        (self.app / "roast.md").write_text("# Fit\nThe service redesign supports this discovery role and the desired IC direction.\n", encoding="utf-8")
        (self.app / "resume.md").write_text(
            "# Test Candidate\n**Product Manager**\n\n# PROFILE\n" + self.strength
            + "\n\n# WORK EXPERIENCE\n## Product Manager | Example\n01/2023 - Present\n* " + self.story + "\n",
            encoding="utf-8")
        self.assessment = {
            "schema_version": 2, "reviewed_at": "2026-09-25", **fingerprints(self.pdir, self.app),
            "goals_fit": {"status": "aligned", "summary": "An IC remit with discovery supports the user's desired next step."},
            "blocking_questions": [],
            "requirements": [{"requirement": "Product discovery and service improvement", "importance": "must_have",
                              "status": "supported", "note": "The support interviews and handoff redesign demonstrate this work.",
                              "evidence": [{"path": "master_cv.md", "quote": self.story}]}],
        }
        self.save_assessment()

    def save_assessment(self, refresh=False):
        if refresh:
            self.assessment.update(fingerprints(self.pdir, self.app))
        write_yaml(self.app / "readiness.yaml", self.assessment)

    def entry(self, identifier="learning-one", scope="global", kind="preference", **fields):
        value = {"id": identifier, "date": "2026-09-25", "kind": kind, "scope": scope,
                 "statement": "Emphasise mentoring where relevant.", "source": "Remember to emphasise mentoring where relevant.",
                 "confirmed": scope != "pending"}
        value.update(fields)
        return value

    def run_script(self, name, *arguments, skill=SKILL, extra_env=None):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", JOB_APPLICATIONS_DIR=str(self.root))
        env.update(extra_env or {})
        return subprocess.run([sys.executable, "-B", str(skill / "scripts" / name), *map(str, arguments)],
                              cwd=self.root, env=env, text=True, capture_output=True)

    def test_sparse_profile_cannot_pass_with_completed_flag(self):
        (self.pdir / "readiness.yaml").unlink()
        (self.pdir / "master_cv.md").write_text("---\nread_only: true\n---\n# PROFILE\nI work in product.\n", encoding="utf-8")
        (self.pdir / "preferences.md").write_text("# Preferences\n", encoding="utf-8")
        errors, _ = validate_profile(self.pdir)
        self.assertTrue(any("actual career" in message for message in errors), errors)
        self.assertTrue(any("readiness.yaml missing" in message for message in errors), errors)

    def test_qualitative_outcome_and_no_private_contact_number_can_pass(self):
        self.assertEqual(validate_profile(self.pdir)[0], [])
        self.assertEqual(tailoring_errors(self.pdir, self.app), [])

    def test_completed_flag_is_not_required_for_ready_baseline(self):
        self.profile["onboarding_complete"] = False
        write_yaml(self.pdir / "profile.yaml", self.profile)
        self.assertEqual(validate_profile(self.pdir)[0], [])

    def test_early_career_project_evidence_is_valid(self):
        path = self.pdir / "master_cv.md"
        path.write_text(path.read_text().replace("# WORK EXPERIENCE", "# PROJECTS"), encoding="utf-8")
        self.assertEqual(validate_profile(self.pdir)[0], [])

    def test_only_missing_coverage_area_is_reported(self):
        self.background["areas"]["career_direction"]["status"] = "missing"
        write_yaml(self.pdir / "readiness.yaml", self.background)
        errors, _ = validate_profile(self.pdir)
        self.assertEqual(errors, ["career_direction: background is not ready"])

    def test_ready_boolean_cannot_replace_real_evidence(self):
        self.background["areas"]["experience_and_outcomes"]["evidence"] = []
        write_yaml(self.pdir / "readiness.yaml", self.background)
        self.assertTrue(validate_profile(self.pdir)[0])

    def test_fabricated_source_excerpt_is_rejected(self):
        self.background["areas"]["strengths"]["evidence"][0]["quote"] = "I managed a team of fifty engineers."
        write_yaml(self.pdir / "readiness.yaml", self.background)
        self.assertTrue(any("not found" in message for message in validate_profile(self.pdir)[0]))

    def test_legacy_profile_is_blocked_without_replacing_answers(self):
        self.profile["schema_version"] = 1
        write_yaml(self.pdir / "profile.yaml", self.profile)
        before = {path: path.read_bytes() for path in self.pdir.rglob("*") if path.is_file()}
        self.assertTrue(validate_profile(self.pdir)[0])
        self.assertEqual(before, {path: path.read_bytes() for path in self.pdir.rglob("*") if path.is_file()})

    def test_unknown_must_have_blocks_even_after_proceed(self):
        self.assessment["requirements"][0]["status"] = "unknown"
        self.save_assessment()
        self.assertTrue(any("unknown" in message for message in tailoring_errors(self.pdir, self.app)))

    def test_confirmed_gap_can_proceed_honestly(self):
        item = self.assessment["requirements"][0]
        item.update(status="confirmed_gap", note="The user confirmed no direct experience and chose to apply despite the gap.", evidence=[])
        self.assessment["goals_fit"]["status"] = "tradeoff"
        self.save_assessment()
        self.assertEqual(tailoring_errors(self.pdir, self.app), [])

    def test_unknown_nonmaterial_nice_to_have_must_be_omitted(self):
        self.assessment["requirements"][0].update(status="unknown", importance="nice_to_have", omit_from_claims=True)
        self.save_assessment()
        self.assertEqual(tailoring_errors(self.pdir, self.app), [])
        self.assessment["requirements"][0]["omit_from_claims"] = False
        self.save_assessment()
        self.assertTrue(tailoring_errors(self.pdir, self.app))

    def test_unrecorded_decision_blocks(self):
        self.metadata["tailoring_approved"] = "true"
        write_json(self.app / "metadata.json", self.metadata)
        self.assertTrue(any("decision" in message for message in tailoring_errors(self.pdir, self.app)))

    def test_changed_goals_require_reassessment(self):
        path = self.pdir / "preferences.md"
        path.write_text(path.read_text() + "\nI now want line-management responsibility.\n", encoding="utf-8")
        self.assertTrue(any("stale" in message for message in tailoring_errors(self.pdir, self.app)))
        self.save_assessment(refresh=True)
        self.assertEqual(tailoring_errors(self.pdir, self.app), [])

    def test_changed_jd_and_local_feedback_invalidate_assessment(self):
        for change in ("jd", "feedback"):
            with self.subTest(change=change):
                if change == "jd":
                    (self.app / "job_description.md").write_text("# Job\nThe target role changed.\n", encoding="utf-8")
                else:
                    record(self.entry(scope="application"), self.pdir, self.app)
                self.assertTrue(any("job_fingerprint" in message for message in tailoring_errors(self.pdir, self.app)))
                self.save_assessment(refresh=True)

    def test_jd_cannot_be_candidate_evidence(self):
        self.assessment["requirements"][0]["evidence"] = [{"application_path": "job_description.md", "quote": "product discovery"}]
        self.save_assessment()
        self.assertTrue(tailoring_errors(self.pdir, self.app))

    def test_application_local_candidate_evidence_is_usable_without_global_promotion(self):
        record(self.entry(kind="fact", scope="application", statement="I facilitated the research workshop.",
                          source="For this application only: I facilitated the research workshop."), self.pdir, self.app)
        self.assessment["requirements"][0]["evidence"] = [{"application_path": "learning.json", "quote": "I facilitated the research workshop."}]
        self.save_assessment(refresh=True)
        self.assertEqual(tailoring_errors(self.pdir, self.app), [])
        self.assertEqual(list((self.pdir / "knowledge").iterdir()), [])

    def test_tailoring_renderer_refuses_before_writing_outputs(self):
        self.background["areas"]["career_direction"]["status"] = "missing"
        write_yaml(self.pdir / "readiness.yaml", self.background)
        out = self.root / "should-not-exist"
        result = self.run_script("render_cv.py", "--resume", self.app / "resume.md", "--tailoring", "--out-dir", out)
        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertFalse(out.exists())

    def test_ready_tailoring_parse_and_legacy_render_only_parse(self):
        result = self.run_script("render_cv.py", "--resume", self.app / "resume.md", "--tailoring", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        (self.pdir / "readiness.yaml").unlink()
        result = self.run_script("render_cv.py", "--resume", self.app / "resume.md", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_application_and_pending_feedback_never_touch_profile(self):
        before = {path: path.read_bytes() for path in self.pdir.rglob("*") if path.is_file()}
        record(self.entry("local", "application", kind="fact"), self.pdir, self.app)
        record(self.entry("uncertain", "pending"), self.pdir, self.app)
        self.assertEqual(before, {path: path.read_bytes() for path in self.pdir.rglob("*") if path.is_file()})
        selected = show(self.pdir, self.app)
        self.assertEqual([item["id"] for item in selected["application"]], ["local"])
        self.assertEqual([item["id"] for item in selected["pending"]], ["uncertain"])
        self.assertEqual(show(self.pdir)["durable"], [])

    def test_role_and_market_scopes_apply_only_where_intended(self):
        record(self.entry("lead", "archetype", scope_value="LEAD"), self.pdir, self.app)
        record(self.entry("uk", "market", scope_value="UK"), self.pdir, self.app)
        self.assertEqual(show(self.pdir, archetype="IC", market="US")["durable"], [])
        self.assertEqual([item["id"] for item in show(self.pdir, archetype="LEAD", market="UK")["durable"]], ["lead", "uk"])

    def test_correction_survives_new_process_and_protects_master(self):
        original = (self.pdir / "master_cv.md").read_bytes()
        record(self.entry("old", kind="fact", statement="I led the launch."), self.pdir, self.app)
        record(self.entry("corrected", kind="correction", statement="I contributed to the launch; I did not lead it.",
                          source="Remember this correction: I contributed to the launch; I did not lead it.", supersedes=["old"]), self.pdir, self.app)
        result = self.run_script("record_learning.py", "show", "--archetype", "IC", "--market", "UK")
        self.assertEqual(result.returncode, 0, result.stderr)
        active = json.loads(result.stdout)["durable"]
        self.assertEqual([item["id"] for item in active], ["corrected"])
        self.assertTrue((self.pdir / active[0]["evidence_file"]).is_file())
        self.assertEqual(original, (self.pdir / "master_cv.md").read_bytes())

    def test_pending_scope_is_promoted_only_after_confirmation(self):
        record(self.entry("pending", "pending"), self.pdir, self.app)
        bad = self.entry("promoted", confirmed=False, supersedes=["pending"])
        with self.assertRaises(ValueError):
            record(bad, self.pdir, self.app)
        record(self.entry("promoted", supersedes=["pending"]), self.pdir, self.app)
        self.assertEqual(show(self.pdir, self.app)["pending"], [])
        self.assertEqual([item["id"] for item in show(self.pdir)["durable"]], ["promoted"])

    def test_one_off_override_does_not_erase_global_preference(self):
        record(self.entry("global-rule"), self.pdir, self.app)
        record(self.entry("local-rule", "application", supersedes=["global-rule"]), self.pdir, self.app)
        self.assertEqual(show(self.pdir, self.app)["durable"], [])
        self.assertEqual([item["id"] for item in show(self.pdir)["durable"]], ["global-rule"])

    def test_duplicate_record_is_idempotent_and_conflict_is_not_overwritten(self):
        value = self.entry()
        record(value, self.pdir, self.app)
        before = (self.pdir / "preferences.md").read_bytes()
        self.assertEqual(record(value, self.pdir, self.app)["status"], "unchanged")
        self.assertEqual(before, (self.pdir / "preferences.md").read_bytes())
        with self.assertRaises(ValueError):
            record(dict(value, statement="A different preference."), self.pdir, self.app)
        self.assertEqual(before, (self.pdir / "preferences.md").read_bytes())

    def test_new_application_preserves_quotes_and_creates_gates(self):
        result = self.run_script("new_application.py", "--company", 'A "Quoted" Company', "--role", 'PM "Data"', "--date", "2026-09-25")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        folder = Path(next(line[8:] for line in result.stdout.splitlines() if line.startswith("FOLDER: ")))
        meta = json.loads((folder / "metadata.json").read_text())
        self.assertEqual(meta["company"], 'A "Quoted" Company')
        self.assertIs(meta["tailoring_approved"], False)
        self.assertTrue((folder / "readiness.yaml").is_file())
        self.assertEqual(json.loads((folder / "learning.json").read_text())["entries"], [])

    def test_both_host_installation_layouts_use_same_profile(self):
        for host in (".claude", ".codex"):
            with self.subTest(host=host):
                target = self.root / "host" / host / "skills" / "job-application"
                shutil.copytree(SKILL, target, ignore=shutil.ignore_patterns("__pycache__"))
                result = self.run_script("check_readiness.py", "--application", self.app, skill=target)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_yaml_dependency_fails_clearly(self):
        env = dict(os.environ, JOB_APPLICATIONS_DIR=str(self.root), PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run([sys.executable, "-S", "-B", str(SKILL / "scripts" / "paths.py")],
                                cwd=self.root, env=env, text=True, capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("PyYAML is required", result.stderr)

    def test_existing_parser_regressions(self):
        for check in (test_parser.test_example_resume_structure, test_parser.test_custom_all_caps_section_and_date_forms,
                      test_parser.test_inline_runs):
            with self.subTest(check=check.__name__):
                check()


if __name__ == "__main__":
    unittest.main()
