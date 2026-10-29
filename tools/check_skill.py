#!/usr/bin/env python3
"""Static checker for UGREEN Uliya skill folders.

Usage: check_skill.py <skill_dir>
Output: one `ERROR|WARN CODE file:line message` per finding, then a summary.
Exit status is 1 when any error was reported.
"""
import re
import sys
from pathlib import Path

MAX_FILE = 1 << 20
MAX_TOTAL = 10 << 20
MAX_FILES = 100
MAX_BODY_LINES = 500
STATUSES = ("completed", "failed", "cancelled", "waiting_user", "waiting_approval")
AGENTS = {"media-agent", "security-monitor-agent", "file-agent",
          "document-agent", "knowledge-agent", "photo-agent"}
CLI_OWNER = {
    "ug-music": "media-agent", "ug-video": "media-agent",
    "ug-surveillance": "security-monitor-agent",
    "ug-filesystem": "file-agent", "ug-filemgr": "file-agent", "file-workflow": "file-agent",
    "ug-document": "document-agent", "ug-knowledge": "knowledge-agent", "ug-photo": "photo-agent",
}
H1 = r"^# +(?:%s) *$"
REQUIRED = [
    ("Goal", H1 % "Goal|目标"),
    ("Required input", H1 % "Required input|必需输入"),
    ("Workflow or Orchestration", H1 % "Workflow|Orchestration|专家编排"),
    ("Completion and failure or Failure handling",
     H1 % "Completion and failure|Failure handling|完成与失败"),
]
EVIDENCE_H1 = re.compile(H1 % "Generation-time capability evidence|生成期能力依据", re.M | re.I)
EVIDENCE_LINE = re.compile(r"^\s*-\s+`([\w-]+)`\s+→\s+`([\w-]+)`\s*$")
ASCII_EVIDENCE = re.compile(r"^\s*-\s+`?[\w-]+`?\s+->\s+`?[\w-]+`?\s*$")
NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
TRIGGER = re.compile(r"\bwhen\b|use when|当用户|用户(?:说|问|要|需要|希望|提到)|适用于", re.I)
LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)\s]*)?\)")
DELEGATE = re.compile(r"delegate --\S.*")
PLACEHOLDER = re.compile(r"<[^>\n]{1,80}>|the previous path|该路径|上一步的?(?:路径|目录|结果)")
FORBIDDEN_SUFFIXES = {".sh", ".py", ".js", ".mjs", ".ts", ".rb", ".exe", ".bat", ".ps1", ".bin",
                      ".so", ".dll", ".jar", ".zip", ".tar", ".gz", ".7z", ".json", ".yaml",
                      ".yml", ".toml", ".xml", ".ini", ".env"}

LINE_RULES = [
    ("SECURITY_CREDENTIAL", re.compile(
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----|\b(?:password|passwd|token|api[_-]?key|secret)\s*[:=]\s*[\"'][^\"'\n]+[\"']", re.I),
     "credential literal", False),
    ("SECURITY_DOWNLOAD", re.compile(r"\b(?:curl|wget)\b", re.I), "remote download tool", False),
    ("SECURITY_CODE_FENCE", re.compile(
        r"^\s*```\s*(?:bash|sh|shell|zsh|python|py|js|javascript|node|ts|typescript|powershell|ruby|perl|php|go)\b", re.I),
     "runtime code fence", False),
    ("SECURITY_FILE_API", re.compile(
        r"\b(?:readFile|writeFile|unlink|fs\.\w+|open\s*\(|fetch\s*\(|axios)|\b(?:cp|mv|rm|cat)\s+\S", re.I),
     "direct file or network API", True),
    ("SECURITY_NAS_PATH", re.compile(r"(?:^|[\s\"'`(])/(?:nas|mnt|volume\d*)(?:/|\b)", re.I),
     "literal NAS path outside a delegate line", True),
    ("SECURITY_BYPASS", re.compile(
        r"\b(?:bypass|skip|disable|ignore)\b[^\n]{0,40}\b(?:approval|permission|audit|gateway)\b|绕过|跳过审批", re.I),
     "approval bypass wording", False),
    ("SECURITY_INTERNAL_NAME", re.compile(
        r"\bug-ai\b|\bHERMES\b|\bexpert[-_ ]?id\b|\bcorrelation[-_ ]?id\b", re.I),
     "internal platform name", False),
    ("RUNTIME_COMPACT_PROFILE", re.compile(r"\bcompact[-\s]profile\b|compact-(?:main|unified)-agent", re.I),
     "compact profile is unsupported", False),
    ("RUNTIME_HOME_PATH", re.compile(r"/home/(?![<{$])[\w.-]+"), "hardcoded home directory", False),
    ("SKILL_PLACEHOLDER", re.compile(r"\b(?:TODO|TBD)\b"), "unfinished placeholder", False),
]
CLI_INVOKE = re.compile(r"\bcli\.invoke\b")
CLI_INVOKE_NEGATED = re.compile(r"(?:do not|don't|never|must not|without|不)[^\n]{0,40}cli\.invoke", re.I)


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, code, file, line, msg):
        self.items.append((level, code, file, line, msg))

    def error(self, *a):
        self.add("ERROR", *a)

    def warn(self, *a):
        self.add("WARN", *a)

    @property
    def errors(self):
        return sum(i[0] == "ERROR" for i in self.items)


def parse_frontmatter(text, rep):
    m = re.match(r"---\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.S)
    if not m:
        rep.error("FRONTMATTER_MISSING", "SKILL.md", 1, "file must start with a --- frontmatter block")
        return {}, text
    fields = {}
    for offset, raw in enumerate(m.group(1).splitlines(), start=2):
        key, sep, value = raw.partition(":")
        key, value = key.strip(), value.strip()
        if not sep or key not in ("name", "description") or key in fields or not value:
            rep.error("FRONTMATTER_INVALID", "SKILL.md", offset,
                      "only single-line, non-empty name and description are allowed")
            continue
        if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        fields[key] = (value, offset)
    for key in ("name", "description"):
        if key not in fields:
            rep.error("FRONTMATTER_INVALID", "SKILL.md", 1, f"missing {key}")
    return fields, text[m.end():]


def hidden(path, root):
    return any(part.startswith(".") for part in path.relative_to(root).parts)


def check_layout(root, rep):
    texts, total = {}, 0
    for entry in sorted(root.iterdir()):
        if entry.name.startswith("."):
            continue
        if entry.name not in ("SKILL.md", "references"):
            rep.error("PACKAGE_FILE_NOT_ALLOWED", entry.name, 0, "only SKILL.md and references/ may exist at the root")
    files = [p for p in sorted(root.rglob("*")) if (p.is_file() or p.is_symlink()) and not hidden(p, root)]
    if len(files) > MAX_FILES:
        rep.error("PACKAGE_TOO_MANY_FILES", ".", 0, f"{len(files)} files exceeds {MAX_FILES}")
    for path in files:
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            rep.error("PACKAGE_SYMLINK", rel, 0, "symbolic links are not allowed")
            continue
        size = path.stat().st_size
        total += size
        if size > MAX_FILE:
            rep.error("PACKAGE_FILE_TOO_LARGE", rel, 0, f"{size} bytes exceeds 1 MiB")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES or path.stat().st_mode & 0o111:
            rep.error("PACKAGE_FORBIDDEN_TYPE", rel, 0, "scripts, binaries, manifests and archives are not allowed")
        elif rel != "SKILL.md" and not (rel.startswith("references/") and path.suffix == ".md"):
            rep.error("PACKAGE_FILE_NOT_ALLOWED", rel, 0, "only .md files under references/ are allowed")
        elif path.suffix == ".md":
            try:
                texts[rel] = path.read_bytes().decode("utf-8")
            except UnicodeDecodeError:
                rep.error("PACKAGE_NOT_UTF8", rel, 0, "file is not valid UTF-8")
    if total > MAX_TOTAL:
        rep.error("PACKAGE_TOO_LARGE", ".", 0, f"{total} bytes exceeds 10 MiB")
    return texts


def check_frontmatter(root, fields, rep):
    if "name" in fields:
        name, line = fields["name"]
        if not 2 <= len(name) <= 64:
            rep.error("NAME_LENGTH", "SKILL.md", line, f"name has {len(name)} characters, need 2-64")
        if not NAME_RE.fullmatch(name):
            rep.error("NAME_INVALID", "SKILL.md", line, "name must be lowercase alphanumeric words joined by single hyphens")
        elif name != root.name:
            rep.error("NAME_DIR_MISMATCH", "SKILL.md", line, f"name {name!r} differs from directory {root.name!r}")
    if "description" in fields:
        desc, line = fields["description"]
        if len(desc) > 1024:
            rep.error("DESCRIPTION_LENGTH", "SKILL.md", line, f"description has {len(desc)} characters, max 1024")
        if not TRIGGER.search(desc):
            rep.warn("DESCRIPTION_NO_TRIGGER", "SKILL.md", line, "description should say when to use the skill")


def check_headings(body, rep):
    for label, pattern in REQUIRED:
        if not re.search(pattern, body, re.M | re.I):
            rep.error("HEADING_MISSING", "SKILL.md", 1, f"missing required heading: # {label}")
    if not EVIDENCE_H1.search(body):
        rep.error("HEADING_MISSING", "SKILL.md", 1, "missing required heading: # Generation-time capability evidence")


def evidence_agents(text, rep):
    agents, seen, inside = set(), set(), False
    for n, line in enumerate(text.splitlines(), 1):
        if line.startswith("# "):
            inside = bool(EVIDENCE_H1.match(line))
        if not inside:
            continue
        if ASCII_EVIDENCE.match(line):
            rep.error("EVIDENCE_ASCII_ARROW", "SKILL.md", n, "use the Unicode arrow → in evidence lines")
        m = EVIDENCE_LINE.match(line)
        if not m:
            continue
        cli, agent = m.groups()
        if cli in seen:
            rep.error("EVIDENCE_DUPLICATE", "SKILL.md", n, f"{cli} listed twice")
        elif cli not in CLI_OWNER:
            rep.error("EVIDENCE_UNKNOWN_CLI", "SKILL.md", n, f"{cli} is not a known CLI")
        elif CLI_OWNER[cli] != agent:
            rep.error("EVIDENCE_OWNER_MISMATCH", "SKILL.md", n, f"{cli} belongs to {CLI_OWNER[cli]}, not {agent}")
        else:
            agents.add(agent)
        seen.add(cli)
    return agents


def check_delegates(file, text, rep):
    targets = []
    for n, line in enumerate(text.splitlines(), 1):
        m = DELEGATE.search(line)
        if not m:
            continue
        cmd = m.group(0).rstrip("`")
        tgt = re.findall(r"--target(?:\s+(\S+))?", cmd)
        ins = re.findall(r"--instruction(?:\s+('(?:[^']|'\"'\"')*'))?", cmd)
        extra = re.findall(r"\s--(?!target\b|instruction\b)[\w-]+", cmd)
        if len(tgt) != 1 or len(ins) != 1 or extra:
            rep.error("DELEGATE_FORMAT", file, n, "need exactly one --target and one --instruction, no other flags")
            continue
        if not ins[0] or ins[0] == "''":
            rep.error("DELEGATE_FORMAT", file, n, "--instruction must be a non-empty single-quoted string")
            continue
        rest = cmd[cmd.index(ins[0]) + len(ins[0]):].strip(" `.,;)") if ins[0] in cmd else ""
        if rest or re.search(r"\s(?:\||>|<|&&|;)\s|\$\(", cmd.replace(ins[0], "")):
            rep.error("DELEGATE_FORMAT", file, n, "no pipes, redirects, chaining or text after the quoted instruction")
        if tgt[0] not in AGENTS:
            rep.error("DELEGATE_TARGET", file, n, f"{tgt[0] or '(none)'} is not a registered agent")
        else:
            targets.append((tgt[0], n))
        if PLACEHOLDER.search(ins[0]):
            rep.warn("DELEGATE_UNRESOLVED_VALUE", file, n, "instruction contains an unresolved placeholder")
    return targets


def check_security(file, text, rep):
    for n, line in enumerate(text.splitlines(), 1):
        in_delegate = "delegate --" in line
        for code, pattern, msg, skip_delegate in LINE_RULES:
            if (not (skip_delegate and in_delegate)) and pattern.search(line):
                rep.error(code, file, n, msg)
        if CLI_INVOKE.search(line) and not CLI_INVOKE_NEGATED.search(line):
            rep.error("RUNTIME_CLI_INVOKE", file, n, "cli.invoke may only appear negated")


def check_skill_md(root, texts, rep):
    text = texts["SKILL.md"]
    fields, body = parse_frontmatter(text, rep)
    check_frontmatter(root, fields, rep)
    check_headings(body, rep)
    if len(body.splitlines()) > MAX_BODY_LINES:
        rep.warn("BODY_TOO_LONG", "SKILL.md", 1, f"body exceeds {MAX_BODY_LINES} lines")
    linked = set()
    for target in LINK.findall(text):
        if target.startswith("references/"):
            linked.add(target)
            if target not in texts:
                rep.error("LINK_BROKEN", "SKILL.md", 1, f"linked file does not exist: {target}")
    for rel in texts:
        if rel != "SKILL.md" and rel not in linked:
            rep.error("REFERENCE_UNLINKED", rel, 0, "not linked directly from SKILL.md")

    all_targets = []
    for file, content in texts.items():
        all_targets += check_delegates(file, content, rep)
    evidenced = evidence_agents(text, rep)
    for agent, n in all_targets:
        if agent not in evidenced:
            rep.error("EVIDENCE_MISSING", "SKILL.md", n, f"no evidence line maps a CLI to {agent}")
    corpus = "\n".join(texts.values())
    missing = [s for s in STATUSES if s not in corpus]
    if missing:
        rep.error("STATUS_TOKENS_MISSING", "SKILL.md", 1, "missing status tokens: " + ", ".join(missing))
    if not all_targets:
        rep.warn("NO_DELEGATION", "SKILL.md", 1, "no delegate command found")
    if re.search(r"\b(?:search|find|scan|list|query)\b|查询|搜索", corpus, re.I) and not re.search(
            r"no results?|zero matches|empty (?:result|list)|无结果|空结果|没有找到", corpus, re.I):
        rep.warn("EMPTY_RESULT_UNHANDLED", "SKILL.md", 1, "query steps need explicit empty-result handling")
    if len(all_targets) > 1 and not re.search(r"upstream|downstream|real result|上一步|真实", corpus, re.I):
        rep.warn("RESULT_PASSING_UNSTATED", "SKILL.md", 1, "say that steps pass real upstream results downstream")


def check(root):
    rep = Report()
    if not root.is_dir():
        rep.error("TARGET_INVALID", str(root), 0, "not a directory")
        return rep
    texts = check_layout(root, rep)
    if "SKILL.md" not in texts:
        rep.error("SKILL_MD_MISSING", "SKILL.md", 0, "SKILL.md is required")
    else:
        check_skill_md(root, texts, rep)
    for file, content in texts.items():
        check_security(file, content, rep)
    return rep


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    rep = check(Path(argv[1]).resolve())
    for level, code, file, line, msg in rep.items:
        print(f"{level} {code} {file}:{line} {msg}")
    print(f"{rep.errors} errors, {len(rep.items) - rep.errors} warnings")
    return 1 if rep.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
