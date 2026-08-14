import re


def _fix_pre(m):
    prefix, content, suffix = m.groups()
    parts = [prefix]
    if prefix.strip():
        parts.append("\n")

    parts.append("```\n")
    parts.append(content.strip())
    parts.append("\n```")

    if suffix.strip():
        parts.append("\n")

    parts.append(suffix)
    return "".join(parts)


def _fix_link(m):
    raw = m.group(1)
    # Only keep .html extension for external links.
    if raw.startswith("http://") or raw.startswith("https://"):
        return m.group(0)

    return f"]({raw}"


def _fix_td_linebreaks(m):
  lb = "\n" if "\n" in m.group(1) else ""
  return f"<td>{lb}{m.group(1).strip()}{lb}</td>"


# {: .external}, {:.devsite-disable-click-to-copy}
_TAG_SUB = ("", re.compile(r"\s*\{:\s?.\S+\}"))
_DISABLE_FINDING_SUB = ("", re.compile(r"\{# disableFinding\([^)]+\) #\}"))
# {:#foo} and {: #foo } -> {#foo}
_KEYWORDS_SUB = ("", re.compile(r"^keywords: .+$", re.MULTILINE))
# https://github.com/bazelbuild/bazel/commit/6ec6d867843d274fa4555eb635ebafc60259b88e
_BAD_TITLE_SUB = (
    r"---\ntitle: \1\n---\n\n",
    re.compile(r"^---\n\n## title: (.+)\n\n", re.MULTILINE),
)
_PRE_BLOCK_SUB = (
    _fix_pre,
    re.compile(r"^(.*?)(?:<pre>)(.*?)(?:</pre>)(.*?)$", re.DOTALL | re.MULTILINE),
)
# {{ '<var>' }} / {{ "</sub>" }} or any variations thereof
_DOUBLE_BRACKET_SUB = (r"\1", re.compile(r"\{\{ ['\"](</?\w+>)['\"] \}\}"))
_HTML_COMMENT_SUB = (r"{/* \1 */}", re.compile(r"<!--(.*?)-->", re.DOTALL))
_ANCHOR_SUB = (r"{\1}", re.compile(r"\{:\s?(#[\S+]+)\s?\}"))
_HTML_LINK_SUB = (_fix_link, re.compile(r"\]\(([^)]+)\.html"))
_ANGLE_BRACKET_LINK_SUB = (r"\1", re.compile(r"<(https?://[^>]+)>"))
# {# some comment #} -> {/* some comment */}
_BAD_COMMENT_SUB = (r"\1{/*\2*/}\3", re.compile(r"^(.*?)\{#(.*?)#\}(.*)$", re.MULTILINE))
_SELF_CLOSING_TAG_SUB = (r"<\1\2/>", re.compile(r"<(img|hr|col|br)([^>]*?)(/?)>"))
_BAD_LINEBREAK_TD_SUB = (_fix_td_linebreaks, re.compile(r"<td>(.*?)</td>", re.DOTALL))

_SUBS = [
    _TAG_SUB,
    _DISABLE_FINDING_SUB,
    _KEYWORDS_SUB,
    _BAD_TITLE_SUB,
    _PRE_BLOCK_SUB,
    _DOUBLE_BRACKET_SUB,
    _HTML_COMMENT_SUB,
    _ANCHOR_SUB,
    _HTML_LINK_SUB,
    _ANGLE_BRACKET_LINK_SUB,
    _BAD_COMMENT_SUB,
    _SELF_CLOSING_TAG_SUB,
    _BAD_LINEBREAK_TD_SUB,
]


_TITLE_RE = re.compile(r"^title: '", re.MULTILINE)
_HEADING_RE = re.compile(r"^# (.+)$", re.MULTILINE)
_HTML_STYLE_RE = re.compile(r"^</?style>", re.MULTILINE)
_MD_FRONT_MATTER_RE = re.compile(r"^---", re.MULTILINE)


def fix(content):
    for sub, pattern in _SUBS:
        content = pattern.sub(sub, content)

    no_trailing_whitespaces = _remove_trailing_whitespaces(content)
    fixed_headings = (
        no_trailing_whitespaces
        if _TITLE_RE.search(no_trailing_whitespaces)
        else _HEADING_RE.sub(_fix_title_heading, no_trailing_whitespaces, count=1)
    )
    front_matter_first = _remove_anything_before_front_matter(fixed_headings)
    return _remove_style_sections(front_matter_first)


def _remove_trailing_whitespaces(content):
    lines = (l.rstrip() for l in content.split("\n"))
    return "\n".join(lines)


def _fix_title_heading(m):
    title = m.group(1).replace("'", "\\'")
    return f"---\ntitle: '{title}'\n---"


def _remove_anything_before_front_matter(content):
    if content.startswith("---\n"):
        return content

    parts = _MD_FRONT_MATTER_RE.split(content, maxsplit=1)
    if len(parts) == 1:
        # Technically this only affects files that we need for the old site,
        # so the better solution would be to stop generating them.
        return parts[0]

    return f"---{parts[1]}"


def _remove_style_sections(content):
    m = _HTML_STYLE_RE.search(content)
    if not m:
        return content

    parts = _HTML_STYLE_RE.split(content)
    return f"{parts[0]}{parts[2].lstrip()}"
