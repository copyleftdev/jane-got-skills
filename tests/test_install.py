import os
import pathlib
import subprocess
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]
SKILLS = sorted(p.name for p in (REPO / "skills").iterdir() if (p / "SKILL.md").is_file())


def run(target, *args):
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_SKILLS_DIR"}
    p = subprocess.run([str(REPO / "install.sh"), "--dir", str(target), *args],
                       capture_output=True, text=True, env=env)
    return p.returncode, p.stdout + p.stderr


class Install(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name) / "skills"

    def tearDown(self):
        self.tmp.cleanup()

    def test_fresh_install_links_every_skill(self):
        code, out = run(self.dir)
        self.assertEqual(code, 0, out)
        for name in SKILLS:
            link = self.dir / name
            self.assertTrue(link.is_symlink(), name)
            self.assertEqual(pathlib.Path(os.readlink(link)), REPO / "skills" / name)
        self.assertEqual(out.count("linked"), len(SKILLS))

    def test_idempotent(self):
        run(self.dir)
        code, out = run(self.dir)
        self.assertEqual(code, 0)
        self.assertEqual(out.count("ok "), len(SKILLS))

    def test_foreign_symlink_needs_force(self):
        self.dir.mkdir(parents=True)
        other = pathlib.Path(self.tmp.name) / "elsewhere"
        other.mkdir()
        (self.dir / SKILLS[0]).symlink_to(other)
        code, out = run(self.dir)
        self.assertEqual(code, 1)
        self.assertIn("use --force", out)
        self.assertEqual(pathlib.Path(os.readlink(self.dir / SKILLS[0])), other)
        code, out = run(self.dir, "--force")
        self.assertEqual(code, 0, out)
        self.assertEqual(pathlib.Path(os.readlink(self.dir / SKILLS[0])), REPO / "skills" / SKILLS[0])

    def test_real_directory_is_never_touched_even_with_force(self):
        real = self.dir / SKILLS[0]
        real.mkdir(parents=True)
        (real / "mine.txt").write_text("keep me")
        code, out = run(self.dir, "--force")
        self.assertEqual(code, 1)
        self.assertIn("left untouched", out)
        self.assertEqual((real / "mine.txt").read_text(), "keep me")

    def test_list_changes_nothing(self):
        code, out = run(self.dir, "--list")
        self.assertEqual(code, 0)
        self.assertFalse(self.dir.exists())
        self.assertEqual(out.count("not installed"), len(SKILLS))

    def test_uninstall_removes_only_our_links(self):
        run(self.dir)
        foreign = self.dir / "someone-elses-skill"
        foreign.symlink_to(pathlib.Path(self.tmp.name))
        code, out = run(self.dir, "--uninstall")
        self.assertEqual(code, 0, out)
        self.assertEqual(sorted(p.name for p in self.dir.iterdir()), ["someone-elses-skill"])

    def test_selecting_skills(self):
        code, out = run(self.dir, SKILLS[0])
        self.assertEqual(code, 0, out)
        self.assertEqual([p.name for p in self.dir.iterdir()], [SKILLS[0]])
        self.assertEqual(run(self.dir, "no-such-skill")[0], 2)


if __name__ == "__main__":
    unittest.main()
