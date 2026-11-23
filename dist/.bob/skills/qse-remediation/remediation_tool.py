#!/usr/bin/env python3
"""QSE remediation helper: parse QSE findings, group by file, persist state/evidence, build report.

Change log:
- Fri Nov 20 17:05:41 CET 2026: Initial version (init/show/backup/record/record-validation/status/report).

Standard library only. State lives in <result-dir>/remediation/ so work survives across sessions:
  state.json          findings, statuses, validation results (source of truth)
  changelog.md        append-only human-readable change log
  originals/<path>    pristine copy of every file before its first edit
  remediation_report.md  generated final report
"""
import argparse
import datetime
import difflib
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
STATUSES = ("applied", "skipped", "rejected", "deferred")


# Current UTC-offset timestamp helper - Fri Nov 20 17:05:41 CET 2026
def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


# SHA-256 of a file, None if missing - Fri Nov 20 17:05:41 CET 2026
def sha256(path):
    if not os.path.isfile(path):
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


# Paths of the state directory and its files - Fri Nov 20 17:05:41 CET 2026
def paths(args):
    rem = os.path.join(args.result_dir, "remediation")
    return {
        "dir": rem,
        "state": os.path.join(rem, "state.json"),
        "changelog": os.path.join(rem, "changelog.md"),
        "originals": os.path.join(rem, "originals"),
        "report": os.path.join(rem, "remediation_report.md"),
    }


# Load persisted state or abort with a hint - Fri Nov 20 17:05:41 CET 2026
def load_state(args):
    p = paths(args)["state"]
    if not os.path.isfile(p):
        sys.exit("No state found at %s - run 'init' first." % p)
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# Persist state atomically - Fri Nov 20 17:05:41 CET 2026
def save_state(args, state):
    p = paths(args)
    os.makedirs(p["dir"], exist_ok=True)
    tmp = p["state"] + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    os.replace(tmp, p["state"])


# Append a line to the change log - Fri Nov 20 17:05:41 CET 2026
def log_change(args, text):
    p = paths(args)
    os.makedirs(p["dir"], exist_ok=True)
    new = not os.path.isfile(p["changelog"])
    with open(p["changelog"], "a", encoding="utf-8") as f:
        if new:
            f.write("# QSE Remediation Change Log\n\n")
        f.write("- %s  %s\n" % (now(), text))


# Locate findings files per the QSE naming convention - Fri Nov 20 17:05:41 CET 2026
def find_findings_files(result_dir):
    found = sorted(glob.glob(os.path.join(result_dir, "quantum_safe_cryptography_analysis_findings_*.json")))
    api = os.path.join(result_dir, "quantum_safe_api_discovery_findings.json")
    if os.path.isfile(api):
        found.append(api)
    return found


# Recursively collect crypto artifacts that carry vulnerabilities - Fri Nov 20 17:05:41 CET 2026
def walk(node, ctx, out):
    if isinstance(node, list):
        for n in node:
            walk(n, ctx, out)
        return
    if not isinstance(node, dict):
        return
    ctx = dict(ctx)
    if node.get("file_type"):
        ctx["language"] = node["file_type"]
    if node.get("full_name"):
        ctx["file"] = node["full_name"]
    if "crypto_properties" in node or "crypto_vulnerabilities" in node:
        out.append((ctx, node))
        return
    for v in node.values():
        walk(v, ctx, out)


# Convert one raw artifact into a normalized finding - Fri Nov 20 17:05:41 CET 2026
def normalize(ctx, art, source):
    vulns, lines, fname = [], [], None
    for v in art.get("crypto_vulnerabilities") or []:
        for ref in v.get("references") or []:
            loc = (ref.get("context") or {}).get("location") or {}
            if loc.get("line"):
                lines.append(int(loc["line"]))
            fname = fname or loc.get("fileName")
        vulns.append({
            "id": v.get("vulnerabilityId"),
            "classification": v.get("classification"),
            "severity": (v.get("vulnerabilityScore") or "unknown").lower(),
            "message": v.get("debugMessage"),
            "type": v.get("type"),
            "doc": v.get("vulnerabilityDocumentationReference"),
        })
    file = ctx.get("file") or art.get("file_path") or fname or "UNKNOWN"
    line = art.get("call_line") or (min(lines) if lines else None)
    sev = min((SEV_ORDER.get(v["severity"], 9) for v in vulns), default=9)
    return {
        "file": file,
        "line": line,
        "title": art.get("title") or (art.get("crypto_properties") or {}).get("name"),
        "language": ctx.get("language"),
        "source_findings_file": source,
        "crypto_properties": art.get("crypto_properties"),
        "vulnerabilities": vulns,
        "worst_severity": next((k for k, n in SEV_ORDER.items() if n == sev), "informational"),
        "raw": art,
        "status": "pending",
        "notes": [],
    }


# init: parse findings and (re)build state, preserving prior statuses - Fri Nov 20 17:05:41 CET 2026
def cmd_init(args):
    files = find_findings_files(args.result_dir)
    if not files:
        sys.exit("No findings file in %s (expected quantum_safe_cryptography_analysis_findings_<LANG>.json "
                 "or quantum_safe_api_discovery_findings.json)." % args.result_dir)
    p = paths(args)
    state = json.load(open(p["state"], encoding="utf-8")) if os.path.isfile(p["state"]) else {
        "created": now(), "findings": [], "validations": [], "sources": {}}
    existing = {(f["file"], f["line"], f["title"]): f for f in state["findings"]}
    meta = {}
    for fp in files:
        with open(fp, encoding="utf-8") as f:
            data = json.load(f)
        lang_hint = None
        m = re.search(r"findings_([A-Za-z0-9+_-]+)\.json$", os.path.basename(fp))
        if m and "analysis" in fp:
            lang_hint = m.group(1)
        for k in ("scanId", "applicationId", "applicationVersion", "scanTime", "repositoryUrl"):
            meta.setdefault(k, data.get(k))
        state["sources"][os.path.basename(fp)] = {"sha256": sha256(fp), "scanId": data.get("scanId")}
        arts = []
        walk(data, {"language": lang_hint}, arts)
        for ctx, art in arts:
            fnd = normalize(ctx, art, os.path.basename(fp))
            key = (fnd["file"], fnd["line"], fnd["title"])
            if key in existing:
                existing[key]["raw"], existing[key]["vulnerabilities"] = fnd["raw"], fnd["vulnerabilities"]
                continue
            fnd["id"] = "F-%03d" % (len(state["findings"]) + 1)
            state["findings"].append(fnd)
            existing[key] = fnd
    state["meta"] = meta
    state["git_head"] = subprocess.run(["git", "-C", args.workspace, "rev-parse", "HEAD"],
                                       capture_output=True, text=True).stdout.strip() or None
    save_state(args, state)
    log_change(args, "init: %d finding(s) from %s" % (len(state["findings"]), ", ".join(map(os.path.basename, files))))
    cmd_status(args)


# Group findings by source file, worst severity first - Fri Nov 20 17:05:41 CET 2026
def by_file(state):
    groups = {}
    for f in state["findings"]:
        groups.setdefault(f["file"], []).append(f)
    for fl in groups.values():
        fl.sort(key=lambda x: (x["line"] or 0))
    return dict(sorted(groups.items()))


# status: summary of remediation progress per file - Fri Nov 20 17:05:41 CET 2026
def cmd_status(args):
    state = load_state(args)
    print("Scan: %s  app: %s  findings: %d" % (state["meta"].get("scanId"), state["meta"].get("applicationId"),
                                               len(state["findings"])))
    for file, fl in by_file(state).items():
        print("\n%s" % file)
        for f in fl:
            cwes = ",".join(v["classification"] or "?" for v in f["vulnerabilities"]) or "informational"
            print("  %s  line %-5s %-9s %-10s %s  [%s]" % (f["id"], f["line"], f["worst_severity"], f["status"],
                                                          f["title"], cwes))
    pend = [f for f in state["findings"] if f["status"] == "pending" and f["vulnerabilities"]]
    print("\nPending findings with vulnerabilities: %d" % len(pend))


# Resolve a finding path to a file on disk - Fri Nov 20 17:05:41 CET 2026
def resolve(args, rel):
    cand = os.path.join(args.workspace, rel)
    if os.path.isfile(cand):
        return cand
    tail = rel.split("/", 1)[-1]
    hits = glob.glob(os.path.join(args.workspace, "**", tail), recursive=True)
    return hits[0] if len(hits) == 1 else cand


# show: print findings of one file with numbered source context - Fri Nov 20 17:05:41 CET 2026
def cmd_show(args):
    state = load_state(args)
    groups = by_file(state)
    if args.file not in groups:
        sys.exit("Unknown file. Known: %s" % ", ".join(groups))
    disk = resolve(args, args.file)
    src = open(disk, encoding="utf-8", errors="replace").read().splitlines() if os.path.isfile(disk) else []
    print("FILE %s (on disk: %s)" % (args.file, disk if src else "NOT FOUND"))
    for f in groups[args.file]:
        print("\n=== %s  %s  line %s  status=%s" % (f["id"], f["title"], f["line"], f["status"]))
        print("crypto_properties: %s" % json.dumps(f["crypto_properties"]))
        for v in f["vulnerabilities"]:
            print("  - %s %s (%s): %s  %s" % (v["id"], v["classification"], v["severity"], v["message"], v["doc"]))
        if src and f["line"]:
            lo, hi = max(1, f["line"] - args.context), min(len(src), f["line"] + args.context)
            for i in range(lo, hi + 1):
                print("%s%5d | %s" % (">" if i == f["line"] else " ", i, src[i - 1]))


# backup: store pristine copy before first edit (never overwritten) - Fri Nov 20 17:05:41 CET 2026
def cmd_backup(args):
    state = load_state(args)
    disk = resolve(args, args.file)
    if not os.path.isfile(disk):
        sys.exit("File not found: %s" % disk)
    dest = os.path.join(paths(args)["originals"], args.file)
    if os.path.exists(dest):
        print("Backup already exists (kept): %s" % dest)
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(disk, "rb") as s, open(dest, "wb") as d:
        d.write(s.read())
    state.setdefault("files", {})[args.file] = {"original_sha256": sha256(disk), "backed_up": now()}
    save_state(args, state)
    log_change(args, "backup: %s (sha256 %s)" % (args.file, sha256(disk)[:12]))
    print("Backed up to %s" % dest)


# record: set finding status and log it; 'applied' requires a backup - Fri Nov 20 17:05:41 CET 2026
def cmd_record(args):
    state = load_state(args)
    ids = [i.strip() for i in args.ids.split(",") if i.strip()]
    byid = {f["id"]: f for f in state["findings"]}
    for i in ids:
        if i not in byid:
            sys.exit("Unknown finding id: %s" % i)
    for i in ids:
        f = byid[i]
        if args.status == "applied":
            if not os.path.exists(os.path.join(paths(args)["originals"], f["file"])):
                sys.exit("No backup for %s - run 'backup --file %s' BEFORE editing." % (f["file"], f["file"]))
            f["after_sha256"] = sha256(resolve(args, f["file"]))
        f["status"] = args.status
        f["notes"].append({"time": now(), "status": args.status, "summary": args.summary})
        log_change(args, "%s %s %s:%s (%s) - %s" % (args.status.upper(), f["id"], f["file"], f["line"],
                                                    f["title"], args.summary))
    save_state(args, state)
    print("Recorded %s for %s" % (args.status, ", ".join(ids)))


# record-validation: persist a validation command result as evidence - Fri Nov 20 17:05:41 CET 2026
def cmd_validation(args):
    state = load_state(args)
    state["validations"].append({"time": now(), "file": args.file, "command": args.command,
                                 "exit_code": args.exit_code, "summary": args.summary})
    save_state(args, state)
    log_change(args, "VALIDATION %s exit=%s `%s` - %s" % (args.file, args.exit_code, args.command, args.summary))
    print("Validation recorded.")


# Read text lines or [] - Fri Nov 20 17:05:41 CET 2026
def read_lines(path):
    if not path or not os.path.isfile(path):
        return []
    return open(path, encoding="utf-8", errors="replace").read().splitlines(keepends=True)


# report: generate the final remediation report from persisted evidence - Fri Nov 20 17:05:41 CET 2026
def cmd_report(args):
    state = load_state(args)
    p = paths(args)
    fl = state["findings"]
    counts = {s: sum(1 for f in fl if f["status"] == s) for s in ("pending",) + STATUSES}
    partial = counts["pending"] > 0
    o = ["# QSE Remediation Report%s\n" % (" (PARTIAL - pending findings remain)" if partial else ""),
         "Generated: %s\n" % now(), "## 1. Scope\n"]
    m = state["meta"]
    o.append("- Application: %s %s\n- Scan ID: %s (scan time %s)\n- Repository: %s\n- Git HEAD at init: %s\n" % (
        m.get("applicationId"), m.get("applicationVersion"), m.get("scanId"), m.get("scanTime"),
        m.get("repositoryUrl"), state.get("git_head")))
    for n, s in state["sources"].items():
        o.append("- Findings source: `%s` sha256 `%s`\n" % (n, s["sha256"]))
    o.append("\n## 2. Summary\n\n| Status | Count |\n|---|---|\n")
    for k, v in counts.items():
        o.append("| %s | %d |\n" % (k, v))
    o.append("\n## 3. Evidence of identified vulnerabilities (per file)\n")
    for file, items in by_file(state).items():
        o.append("\n### `%s`\n" % file)
        for f in items:
            o.append("\n#### %s - %s (line %s) - **%s**\n" % (f["id"], f["title"], f["line"], f["status"]))
            for v in f["vulnerabilities"]:
                o.append("- %s `%s` [%s]: %s (%s)\n" % (v["id"], v["classification"], v["severity"],
                                                        v["message"], v["doc"]))
            if not f["vulnerabilities"]:
                o.append("- No vulnerability reported (informational artifact)\n")
            o.append("\n<details><summary>Raw finding JSON</summary>\n\n```json\n%s\n```\n</details>\n" %
                     json.dumps(f["raw"], indent=2))
            for n in f["notes"]:
                o.append("- %s %s: %s\n" % (n["time"], n["status"], n["summary"]))
    o.append("\n## 4. Change log\n\n")
    o.append(open(p["changelog"], encoding="utf-8").read().replace("# QSE Remediation Change Log\n", "")
             if os.path.isfile(p["changelog"]) else "_No changes recorded._\n")
    o.append("\n## 5. Before / after comparison\n")
    changed = sorted({f["file"] for f in fl if f["status"] == "applied"})
    for file in changed or []:
        before = read_lines(os.path.join(p["originals"], file))
        after = read_lines(resolve(args, file))
        diff = "".join(difflib.unified_diff(before, after, "a/" + file + " (original)", "b/" + file + " (remediated)"))
        o.append("\n### `%s`\n\n```diff\n%s```\n" % (file, diff or "(no difference)\n"))
        cur = sha256(resolve(args, file))
        last = [f.get("after_sha256") for f in fl if f["file"] == file and f["status"] == "applied"][-1]
        if cur != last:
            o.append("\n> WARNING: file changed after the last recorded remediation (sha256 mismatch).\n")
    if not changed:
        o.append("\n_No files modified._\n")
    o.append("\n## 6. Validation of preserved functionality\n")
    if state["validations"]:
        o.append("\n| Time | File | Command | Exit | Summary |\n|---|---|---|---|---|\n")
        for v in state["validations"]:
            o.append("| %s | %s | `%s` | %s | %s |\n" % (v["time"], v["file"], v["command"], v["exit_code"],
                                                        v["summary"]))
    else:
        o.append("\n_No validation results recorded._\n")
    o.append("\n## 7. Not remediated\n")
    rest = [f for f in fl if f["status"] in ("skipped", "rejected", "deferred", "pending") and f["vulnerabilities"]]
    for f in rest:
        o.append("- %s `%s:%s` %s - %s%s\n" % (f["id"], f["file"], f["line"], f["title"], f["status"],
                                              (": " + f["notes"][-1]["summary"]) if f["notes"] else ""))
    if not rest:
        o.append("\nNone.\n")
    with open(p["report"], "w", encoding="utf-8") as f:
        f.write("".join(o))
    print("Report written: %s" % p["report"])


# CLI wiring - Fri Nov 20 17:05:41 CET 2026
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--result-dir", default="qs_explorer_result")
    ap.add_argument("--workspace", default=".")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init").set_defaults(fn=cmd_init)
    sub.add_parser("status").set_defaults(fn=cmd_status)
    s = sub.add_parser("show")
    s.add_argument("--file", required=True)
    s.add_argument("--context", type=int, default=6)
    s.set_defaults(fn=cmd_show)
    s = sub.add_parser("backup")
    s.add_argument("--file", required=True)
    s.set_defaults(fn=cmd_backup)
    s = sub.add_parser("record")
    s.add_argument("--ids", required=True, help="comma-separated finding ids, e.g. F-001,F-002")
    s.add_argument("--status", required=True, choices=STATUSES)
    s.add_argument("--summary", required=True)
    s.set_defaults(fn=cmd_record)
    s = sub.add_parser("record-validation")
    s.add_argument("--file", required=True)
    s.add_argument("--command", required=True)
    s.add_argument("--exit-code", type=int, required=True)
    s.add_argument("--summary", required=True)
    s.set_defaults(fn=cmd_validation)
    sub.add_parser("report").set_defaults(fn=cmd_report)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
