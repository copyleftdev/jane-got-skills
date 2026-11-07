import collections
import pathlib
import subprocess
import sys
import unittest

HERE = pathlib.Path(__file__).parent
LINT = HERE.parent / "hardcaml_lint.py"
sys.path.insert(0, str(HERE.parent))
import hardcaml_lint  # noqa: E402


class LintTest(unittest.TestCase):
    def test_every_rule_fires_on_its_canary(self):
        rules = collections.Counter(f.rule for f in hardcaml_lint.lint_file(HERE / "fixtures/bad.ml"))
        self.assertEqual(rules, collections.Counter(
            {"H001": 1, "H002": 1, "H003": 1, "H004": 1, "H005": 1, "H006": 1,
             "H007": 1, "H008": 2, "H009": 1, "H010": 1}))

    def test_clean_file_has_no_findings(self):
        self.assertEqual(hardcaml_lint.lint_file(HERE / "fixtures/good.ml"), [])

    def test_exit_status(self):
        run = lambda f: subprocess.run([sys.executable, "-I", str(LINT), str(HERE / "fixtures" / f)],
                                       capture_output=True).returncode
        self.assertEqual(run("bad.ml"), 1)
        self.assertEqual(run("good.ml"), 0)

    def test_skip_drops_named_rules(self):
        out = subprocess.run([sys.executable, "-I", str(LINT), "--json", "--skip", "H002,H004",
                              str(HERE / "fixtures/bad.ml")], capture_output=True, text=True).stdout
        rules = {f["rule"] for f in __import__("json").loads(out)["findings"]}
        self.assertNotIn("H002", rules)
        self.assertNotIn("H004", rules)
        self.assertIn("H001", rules)

    def test_parenthesized_and_single_op_expressions_pass(self):
        for code in ["(a +: b) -: d", "(a <: b) &: (e >: f)", "a +: b", "a +: b +: c",
                     "mux2 (a ==:. 3) x y", "x <-- (y +:. 1)", "f (a +: b) (c -: d)"]:
            self.assertFalse(hardcaml_lint.mixed_operators(code), code)

    def test_mixed_unparenthesized_ops_fail(self):
        for code in ["a +: b -: d", "a |: b &: c", "(a +: b *: c)", "x <-- a +: b -:. 1"]:
            self.assertTrue(hardcaml_lint.mixed_operators(code), code)


if __name__ == "__main__":
    unittest.main()
