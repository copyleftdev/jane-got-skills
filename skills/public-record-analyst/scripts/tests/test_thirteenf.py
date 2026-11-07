import contextlib
import io
import os
import pathlib
import shutil
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import thirteenf as tf  # noqa: E402

TABLE = HERE / "fixtures" / "infotable_q2_2026_first30.xml"
COVER = HERE / "fixtures" / "primary_doc_slice.xml"


class Units(unittest.TestCase):
    def test_boundary(self):
        self.assertEqual(tf.multiplier("2023-01-02"), 1000)
        self.assertEqual(tf.multiplier("2023-01-03"), 1)

    def test_same_table_differs_by_1000x_across_the_boundary(self):
        old = tf.summarize(TABLE, "2022-11-14")["total"]
        new = tf.summarize(TABLE, "2026-08-14")["total"]
        self.assertEqual(old, 1000 * new)


class Summary(unittest.TestCase):
    def setUp(self):
        self.s = tf.summarize(TABLE, "2026-08-14")

    def test_kinds_partition_the_rows_and_the_total(self):
        kinds = self.s["by_kind"]
        self.assertEqual(sum(v["rows"] for v in kinds.values()), self.s["rows"])
        self.assertEqual(sum(v["value"] for v in kinds.values()), self.s["total"])
        self.assertEqual(kinds["calls"]["rows"] + kinds["puts"]["rows"], 8)

    def test_total_matches_raw_sum(self):
        self.assertEqual(self.s["total"], 282_004_615)

    def test_positions_are_keyed_by_cusip_not_issuer_name(self):
        rows = list(tf.rows(TABLE))
        names = {}
        for r in rows:
            if tf.kind(r) == "shares":
                names.setdefault(r["issuer"], set()).add(r["cusip"])
        labels = [label for label, _ in tf.summarize(TABLE, "2026-08-14", top=100)["top_shares"]]
        for issuer, cusips in names.items():
            for c in cusips:
                self.assertEqual(sum(c in label for label in labels), 1, f"{issuer} {c}")


class Reconcile(unittest.TestCase):
    def test_slice_reconciles_with_its_cover(self):
        self.assertEqual(tf.reconcile(COVER, TABLE, "2026-08-14")["problems"], [])

    def test_canary_dropped_row_is_caught(self):
        with tempfile.TemporaryDirectory() as d:
            text = TABLE.read_text()
            start = text.index("\t<ns1:infoTable>")
            end = text.index("</ns1:infoTable>", start) + len("</ns1:infoTable>\n")
            bad = pathlib.Path(d) / "bad.xml"
            bad.write_text(text[:start] + text[end:])
            problems = tf.reconcile(COVER, bad, "2026-08-14")["problems"]
            self.assertEqual(len(problems), 2, problems)


class Fetch(unittest.TestCase):
    def test_refuses_without_user_agent(self):
        env = os.environ.pop("SEC_USER_AGENT", None)
        try:
            with self.assertRaises(ValueError):
                tf.fetch("1595888", tempfile.mkdtemp())
        finally:
            if env is not None:
                os.environ["SEC_USER_AGENT"] = env

    @unittest.skipUnless(os.environ.get("SEC_USER_AGENT") and os.environ.get("LIVE_SEC") == "1",
                         "live SEC check: set SEC_USER_AGENT and LIVE_SEC=1")
    def test_live_q2_2026_reconciles(self):
        d = tempfile.mkdtemp()
        try:
            meta = tf.fetch("1595888", d, "0001595888-26-000108")
            r = tf.reconcile(pathlib.Path(d) / "primary_doc.xml", pathlib.Path(d) / "infotable.xml", meta["filed"])
            self.assertEqual(r["problems"], [])
            self.assertEqual(r["rows"], 14718)
        finally:
            shutil.rmtree(d)


class Cli(unittest.TestCase):
    def test_summarize_requires_filed(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(tf.main(["summarize", str(TABLE)]), 2)

    def test_reconcile_exit_codes(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(tf.main(["reconcile", str(COVER), str(TABLE), "--filed", "2026-08-14"]), 0)


if __name__ == "__main__":
    unittest.main()
