"""Flag patterns that Jane Street's Hardcaml agent guidelines call bad practice.

usage: python3 -I hardcaml_lint.py [--json] [--skip H002,H004] <file-or-dir>...

On Hardcaml v0.17.x (stock opam), `--` naming and `Bits.to_int` are the only APIs that exist,
so run with `--skip H002,H004` there.

Line-based heuristics, not a parser: an empty report is not proof of compliance, and the
operator-precedence rule only sees expressions that fit on one line. Exit status is 1 if any
finding has severity "error", else 0.
"""

import json
import pathlib
import re
import sys
from dataclasses import asdict, dataclass

BINARY_OPS = {
    "+:", "-:", "*:", "*+", "&:", "|:", "^:", "@:",
    "<:", ">:", "<=:", ">=:", "==:", "<>:", "<+", ">+", "<=+", ">=+",
    "+:.", "-:.", "&:.", "|:.", "^:.", "<:.", ">:.", "<=:.", ">=:.", "==:.", "<>:.",
}
OP_TOKEN = re.compile(r"(?<![\w~<>=!|&^@*+\-:.])([+\-*&|^@<>=]{1,3}[:+]\.?)(?![\w:+])")
SEGMENT_BREAK = re.compile(r";|,|\bin\b|\blet\b|\bthen\b|\belse\b|\bwhen_\b|\bif_?\b|->|<--\.?|\[|\]")


@dataclass
class Finding:
    file: str
    line: int
    rule: str
    severity: str
    message: str


LINE_RULES = [
    ("H001", "error", re.compile(r"~enable:\s*vdd\b"),
     "`~enable:vdd` is the default; omit it (design guideline: Signal and Always API)"),
    ("H002", "error", re.compile(r"--\s*\""),
     "`--` naming is dangerous; use `let%hw` / `let%hw_var` (design guideline)"),
    ("H003", "error", re.compile(r"\bof_int_trunc\b"),
     "`of_int_trunc` is broken and dangerous; use `of_unsigned_int` / `of_signed_int`"),
    ("H004", "error", re.compile(r"(?<!Float\.)(?<!Int63\.)(?<!Int64\.)(?<!Int32\.)(?<!Nativeint\.)(?<!Char\.)(?<!Int\.)\bto_int(_trunc)?\b"),
     "use `Bits.to_unsigned_int` / `Bits.to_signed_int`, not `to_int` / `to_int_trunc` (simulation guideline)"),
    ("H005", "error",
     re.compile(r"\[@@deriving[^\]]*\bsexp_of\b[^\]]*\bhardcaml\b|\[@@deriving[^\]]*\bhardcaml\b[^\]]*\bsexp_of\b"),
     "`[@@deriving hardcaml]` already includes `sexp_of`; do not list both"),
    ("H006", "error", re.compile(r"\(~:\)"),
     "write unary operators in operator form with parens around the argument: `~:(x)`"),
    ("H009", "warning", re.compile(r"\bHardcaml_event_driven_sim\b|\bLws_event_driven\b|\bEvsim\b"),
     "event-driven sim backend: use only if existing code does or the user asked (simulation guideline)"),
    ("H010", "warning", re.compile(r"^\s*let\s+_[a-z]\w*\s*="),
     "unused value left in code (design guideline: leaving unused values is bad practice)"),
]

RESIZE = re.compile(r"\b[us]resize\b")
COMMENT = re.compile(r"\(\*")


def code_lines(text):
    """Blank out strings and (possibly nested, multi-line) comments, keeping line structure."""
    out, depth, i, n = [], 0, 0, len(text)
    while i < n:
        two = text[i:i + 2]
        if two == "(*":
            depth, i = depth + 1, i + 2
            out.append("  ")
        elif two == "*)" and depth:
            depth, i = depth - 1, i + 2
            out.append("  ")
        elif depth:
            out.append("\n" if text[i] == "\n" else " ")
            i += 1
        elif text[i] == '"':
            j = i + 1
            while j < n and text[j] != '"':
                j += 2 if text[j] == "\\" else 1
            out.append('""' + "".join("\n" for c in text[i + 1:j] if c == "\n"))
            i = j + 1
        elif two == "{|":
            j = text.find("|}", i + 2)
            j = n if j < 0 else j
            out.append("{||}" + "\n" * text[i:j].count("\n"))
            i = j + 2
        else:
            out.append(text[i])
            i += 1
    return "".join(out).split("\n")


def mixed_operators(code):
    """True if one paren level of one expression segment holds 2+ distinct Hardcaml binary ops."""
    depth, segments = 0, {}
    pos = 0
    for m in re.finditer(r"[()]", code):
        _collect(code[pos:m.start()], depth, segments)
        depth += 1 if m.group() == "(" else -1
        segments.setdefault(depth, [[]])
        if m.group() == "(":
            segments[depth].append([])
        pos = m.end()
    _collect(code[pos:], depth, segments)
    return any(len(set(seg)) >= 2 for groups in segments.values() for seg in groups)


def _collect(text, depth, segments):
    groups = segments.setdefault(depth, [[]])
    for i, piece in enumerate(SEGMENT_BREAK.split(text)):
        if i > 0:
            groups.append([])
        groups[-1].extend(op for op in OP_TOKEN.findall(piece) if op in BINARY_OPS)


def lint_file(path):
    findings = []
    text = path.read_text(errors="replace")
    lines = text.split("\n")
    for n, (raw, code) in enumerate(zip(lines, code_lines(text)), 1):
        for rule, severity, pattern, message in LINE_RULES:
            if pattern.search(code):
                findings.append(Finding(str(path), n, rule, severity, message))
        if RESIZE.search(code):
            context = raw + (lines[n - 2] if n >= 2 else "")
            if not COMMENT.search(context):
                findings.append(Finding(str(path), n, "H007", "warning",
                                        "prefer `uextend`/`sextend`/`sel_bottom`; if `uresize`/`sresize` is needed, justify it in a comment"))
        if mixed_operators(code):
            findings.append(Finding(str(path), n, "H008", "error",
                                    "mixed Hardcaml operators without parentheses; precedence differs from Verilog, always parenthesize"))
    return findings


def main(argv):
    as_json = "--json" in argv
    skip = set()
    if "--skip" in argv:
        i = argv.index("--skip")
        skip = set(argv[i + 1].split(","))
        argv = argv[:i] + argv[i + 2:]
    targets = [pathlib.Path(a) for a in argv if a != "--json"]
    if not targets:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    files = sorted(
        f for t in targets
        for f in ([t] if t.is_file() else list(t.rglob("*.ml")) + list(t.rglob("*.mli")))
        if "_build" not in f.parts
    )
    findings = [f for path in files for f in lint_file(path) if f.rule not in skip]
    if as_json:
        print(json.dumps({"files": len(files), "findings": [asdict(f) for f in findings]}, indent=2))
    else:
        for f in findings:
            print(f"{f.file}:{f.line}: {f.rule} {f.severity}: {f.message}")
        errors = sum(f.severity == "error" for f in findings)
        print(f"{len(files)} files, {errors} errors, {len(findings) - errors} warnings", file=sys.stderr)
    return 1 if any(f.severity == "error" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
