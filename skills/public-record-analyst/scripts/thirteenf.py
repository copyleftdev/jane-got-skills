"""Fetch, summarise and reconcile SEC Form 13F-HR filings without misreading them.

usage:
  python3 -I thirteenf.py fetch <cik> <out_dir> [--accession 0001595888-26-000108]
      needs SEC_USER_AGENT, e.g. "YourOrg research you@yourorg.example" (SEC fair-access policy)
  python3 -I thirteenf.py summarize <infotable.xml> --filed YYYY-MM-DD [--top 10] [--json]
  python3 -I thirteenf.py reconcile <primary_doc.xml> <infotable.xml> --filed YYYY-MM-DD

What the summary separates, because the headline total mixes them:
  shares   rows without putCall, sshPrnamtType SH: long equity positions at market value
  calls    putCall=Call: reported at the value of the UNDERLYING shares, not the option premium
  puts     putCall=Put: same; a put is economically short the underlying
  prn      principal-amount rows (convertible bonds etc.)
Positions are keyed by CUSIP, never by issuer name: one name ("ISHARES TR") covers dozens of funds.
Units: 13F values were reported in thousands of dollars until the SEC's 2023 amendments took effect
(filings on or after 2023-01-03 report whole dollars), so --filed decides the multiplier.
"""

import json
import os
import pathlib
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict

DOLLARS_FROM = "2023-01-03"
SEC = "https://www.sec.gov"
DATA = "https://data.sec.gov"


def multiplier(filed):
    return 1 if filed >= DOLLARS_FROM else 1000


def _local(tag):
    return tag.rsplit("}", 1)[-1]


def _child(node, name):
    for c in node:
        if _local(c.tag) == name:
            return c
    return None


def _text(node, name, default=""):
    c = _child(node, name)
    return c.text.strip() if c is not None and c.text else default


def rows(infotable_path):
    for _, node in ET.iterparse(infotable_path):
        if _local(node.tag) != "infoTable":
            continue
        amt = _child(node, "shrsOrPrnAmt")
        yield {
            "issuer": _text(node, "nameOfIssuer"),
            "class": _text(node, "titleOfClass"),
            "cusip": _text(node, "cusip"),
            "value": int(_text(node, "value", "0")),
            "amount": int(_text(amt, "sshPrnamt", "0")) if amt is not None else 0,
            "amount_type": _text(amt, "sshPrnamtType") if amt is not None else "",
            "put_call": _text(node, "putCall"),
        }
        node.clear()


def kind(row):
    if row["put_call"] in ("Call", "Put"):
        return row["put_call"].lower() + "s"
    return "prn" if row["amount_type"] == "PRN" else "shares"


def summarize(infotable_path, filed, top=10):
    m = multiplier(filed)
    totals, counts = defaultdict(int), defaultdict(int)
    by_issuer = {k: defaultdict(int) for k in ("shares", "calls", "puts", "prn")}
    n = 0
    for r in rows(infotable_path):
        k = kind(r)
        dollars = r["value"] * m
        totals[k] += dollars
        counts[k] += 1
        by_issuer[k][(r["cusip"], f'{r["issuer"]} / {r["class"]} ({r["cusip"]})')] += dollars
        n += 1
    total = sum(totals.values())

    def top_of(k):
        return [(label, v) for (_, label), v in sorted(by_issuer[k].items(), key=lambda kv: -kv[1])[:top]]

    return {
        "rows": n,
        "total": total,
        "by_kind": {k: {"rows": counts[k], "value": totals[k], "share": totals[k] / total if total else 0}
                    for k in ("shares", "calls", "puts", "prn")},
        "top_shares": top_of("shares"),
        "top_calls": top_of("calls"),
        "top_puts": top_of("puts"),
        "units_multiplier": m,
    }


def cover_totals(primary_doc_path):
    root = ET.parse(primary_doc_path).getroot()
    found = {}
    for node in root.iter():
        name = _local(node.tag)
        if name in ("tableEntryTotal", "tableValueTotal", "periodOfReport") and node.text:
            found[name] = node.text.strip()
    return found


def reconcile(primary_doc_path, infotable_path, filed):
    cover = cover_totals(primary_doc_path)
    raw_rows = raw_value = 0
    for r in rows(infotable_path):
        raw_rows += 1
        raw_value += r["value"]
    problems = []
    if int(cover["tableEntryTotal"]) != raw_rows:
        problems.append(f"cover says {cover['tableEntryTotal']} rows, table has {raw_rows}")
    if int(cover["tableValueTotal"]) != raw_value:
        problems.append(f"cover says value {cover['tableValueTotal']}, rows sum to {raw_value}")
    return {"cover": cover, "rows": raw_rows, "raw_value_sum": raw_value,
            "dollars": raw_value * multiplier(filed), "problems": problems}


def _get(url, ua):
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept-Encoding": "identity"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = resp.read()
    time.sleep(0.2)
    return body


def fetch(cik, out_dir, accession=None):
    ua = os.environ.get("SEC_USER_AGENT", "").strip()
    if not ua:
        raise ValueError("set SEC_USER_AGENT to a descriptive string with a contact address (SEC fair-access policy)")
    cik10 = f"{int(cik):010d}"
    sub = json.loads(_get(f"{DATA}/submissions/CIK{cik10}.json", ua))
    recent = sub["filings"]["recent"]
    picks = [i for i, f in enumerate(recent["form"]) if f == "13F-HR"
             and (accession is None or recent["accessionNumber"][i] == accession)]
    if not picks:
        raise ValueError("no matching 13F-HR in the recent filings list")
    i = picks[0]
    acc = recent["accessionNumber"][i]
    base = f"{SEC}/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}"
    names = [it["name"] for it in json.loads(_get(f"{base}/index.json", ua))["directory"]["item"]]
    table = next(n for n in names if n.endswith(".xml") and n != "primary_doc.xml")
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "primary_doc.xml").write_bytes(_get(f"{base}/primary_doc.xml", ua))
    (out / "infotable.xml").write_bytes(_get(f"{base}/{table}", ua))
    meta = {"cik": cik10, "accession": acc, "filed": recent["filingDate"][i],
            "period": recent["reportDate"][i], "source": base}
    (out / "meta.json").write_text(json.dumps(meta, indent=2))
    return meta


def _fmt_bn(x):
    return f"${x / 1e9:,.1f}bn"


def main(argv):
    args = list(argv)
    flags = {}
    for flag in ("--filed", "--top", "--accession"):
        if flag in args:
            i = args.index(flag)
            flags[flag] = args[i + 1]
            del args[i:i + 2]
    as_json = "--json" in args
    args = [a for a in args if a != "--json"]
    try:
        if args[:1] == ["fetch"] and len(args) == 3:
            print(json.dumps(fetch(args[1], args[2], flags.get("--accession")), indent=2))
        elif args[:1] == ["summarize"] and len(args) == 2 and "--filed" in flags:
            s = summarize(args[1], flags["--filed"], int(flags.get("--top", 10)))
            if as_json:
                print(json.dumps(s, indent=2))
                return 0
            print(f"{s['rows']:,} rows, headline total {_fmt_bn(s['total'])} (do not read this as exposure)")
            for k, v in s["by_kind"].items():
                note = {"calls": "  underlying value, not premium", "puts": "  underlying value; economically short"}.get(k, "")
                print(f"  {k:<6} {v['rows']:>6,} rows  {_fmt_bn(v['value']):>11}  {v['share']:6.1%}{note}")
            print("largest share positions:")
            for name, v in s["top_shares"]:
                print(f"  {_fmt_bn(v):>9}  {name}")
        elif args[:1] == ["reconcile"] and len(args) == 3 and "--filed" in flags:
            r = reconcile(args[1], args[2], flags["--filed"])
            print(json.dumps(r, indent=2))
            return 1 if r["problems"] else 0
        else:
            print(__doc__.strip(), file=sys.stderr)
            return 2
    except (ValueError, KeyError, StopIteration, ET.ParseError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
