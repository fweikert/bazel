import re


# {: .external}, {:.devsite-disable-click-to-copy}
_TAG_RE = re.compile(r"\s*\{:\s?.\S+\}")
_DISABLE_FINDING_RE = re.compile(r"\{# disableFinding\([^)]+\) #\}")
# {:#foo} and {: #foo } -> {#foo}
_KEYWORDS_RE = re.compile(r"^keywords: .+$", re.MULTILINE)
# https://github.com/bazelbuild/bazel/commit/6ec6d867843d274fa4555eb635ebafc60259b88e
_BAD_TITLE_RE = re.compile(r"^---\n\n## title: (.+)\n\n", re.MULTILINE)
_PRE_BLOCK_RE = re.compile("^\s*</?pre>$", re.MULTILINE)
# {{ '<var>' }} / {{ "</sub>" }} or any variations thereof
_DOUBLE_BRACKET_RE = re.compile(r"\{\{ ['\"](</?\w+>)['\"] \}\}")
_ANCHOR_RE = re.compile(r"\{:\s?(#[\S+]+)\s?\}")
_HEADING_RE = re.compile(r"^# (.+)$", re.MULTILINE)
_HTML_LINK_RE = re.compile(r"\]\(([^)]+)\.html")
_TITLE_RE = re.compile(r"^title: '", re.MULTILINE)
_ANGLE_BRACKET_LINK_RE = re.compile(r"<(https?://[^>]+)>")
_HTML_STYLE_PATTERN = re.compile(r"^</?style>", re.MULTILINE)
_MD_FRONT_MATTER_PATTERN = re.compile(r"^---", re.MULTILINE)


def fix(content):
  no_tags = _TAG_RE.sub("", content)
  no_disable_findings = _DISABLE_FINDING_RE.sub("", no_tags)
  no_keywords = _KEYWORDS_RE.sub("", no_disable_findings)
  fixed_title = _BAD_TITLE_RE.sub(r"---\ntitle: \1\n---\n\n", no_keywords)
  no_pre_blocks = _PRE_BLOCK_RE.sub("```", fixed_title)
  no_double_brackets = _DOUBLE_BRACKET_RE.sub(r"\1", no_pre_blocks)
  fixed_anchors = _ANCHOR_RE.sub(r"{\1}", no_double_brackets)
  no_html_links = _HTML_LINK_RE.sub(_fix_link, fixed_anchors)
  no_angle_links = _ANGLE_BRACKET_LINK_RE.sub(r"\1", no_html_links)
  no_double_empty_lines = no_angle_links.replace("\n\n\n", "\n\n")
  no_trailing_whitespaces = _remove_trailing_whitespaces(no_double_empty_lines)
  fixed_headings = (
      no_trailing_whitespaces
      if _TITLE_RE.search(no_trailing_whitespaces)
      else _HEADING_RE.sub(_fix_title_heading, no_trailing_whitespaces, count=1)
  )
  front_matter_first = _remove_anything_before_front_matter(fixed_headings)
  return _remove_style_sections(front_matter_first)


def _fix_link(m):
  raw = m.group(1)
  # Only keep .html extension for external links.
  if raw.startswith("http://") or raw.startswith("https://"):
    return m.group(0)

  return f"]({raw}"


def _remove_trailing_whitespaces(content):
  lines = (l.rstrip() for l in content.split("\n"))
  return "\n".join(lines)


def _fix_title_heading(m):
  title = m.group(1).replace("'", "\\'")
  return f"---\ntitle: '{title}'\n---"


def _remove_anything_before_front_matter(content):
  if content.startswith("---\n"):
    return content

  parts = _MD_FRONT_MATTER_PATTERN.split(content, maxsplit=1)
  if len(parts) == 1:
    # Technically this only affects files that we need for the old site,
    # so the better solution would be to stop generating them.
    return parts[0]

  return f"---{parts[1]}"


def _remove_style_sections(content):
  m = _HTML_STYLE_PATTERN.search(content)
  if not m:
    return content

  parts = _HTML_STYLE_PATTERN.split(content)
  return f"{parts[0]}{parts[2].lstrip()}"
