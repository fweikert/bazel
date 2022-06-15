# Lint as: python3
# pylint: disable=g-direct-third-party-import
# Copyright 2022 The Bazel Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TODO"""
import os
import re

HTML = 0
MD = 0
YAML = 0

_YAML_PATTERN = re.compile(r"((book_|image_)?path: )(/.+)$")

_MD_METADATA_PATTERN = re.compile(r"^((Book|Project): )(/_)")
_MD_LINK_PATTERN = re.compile(r"(\!?\[.*?\]\((https://bazel.build)?)(/.*?)\)")
_HTML_LINK_PATTERN = re.compile(r"((href|src)=[\"'](https://bazel.build)?)/")
# []()
# ![]()
"""YAML

  "book_path: /_book.yaml"
  "project_path: /_project.yaml"
  "path: /foo"
  "image_path: /bar"

  IGNORE:
    /
    /versions/
    /versions/_toc.yaml
MD
  "Project: /_project.yaml", -> NOPE
  "Book: /_book.yaml"
HTML
  <meta name="project_path" value="/_project.yaml">
  <meta name="book_path" value="/_book.yaml">
"""

_DOC_EXTENSIONS = set([".html", ".md", ".yaml"])
_IGNORE_LIST = set(["/", "/versions/", "/versions/_toc.yaml"])


def can_rewrite(path):
  _, ext = os.path.splitext(path)
  return ext in _DOC_EXTENSIONS


def rewrite_links(path, content, version):
  _, ext = os.path.splitext(path)

  # TODO: be careful when rewriting _book.yaml: keep /versions/_toc.yaml and
  # TODO: for every md/html: fix _book.yaml, but not _project.yaml

  for line in ("book_path: /_book.yaml", "project_path: /_project.yaml",
               "path: /foo", "image_path: /bar"):
    print(_YAML_PATTERN.sub(r"\1/versions/foo\3", line))

  for line in ("Project: /_project.yaml", "Book: /_book.yaml"):
    print(_MD_METADATA_PATTERN.sub(r"\1/versions/foo\3", line))

  for line in ("[short link](/foo/bar)",
               "[long link](https://bazel.build/foo/bar)",
               "image ![alt](/foo/bar.jpg)"):
    print(_MD_LINK_PATTERN.sub(r"\1/versions/5.0\3)", line))

  for line in ("<a href=\"/foo/bar\">test</a>",
               "<img src='https://bazel.build/images/foo.jpg'/>"):
    print(_HTML_LINK_PATTERN.sub(r"\1/versions/5.0/", line))

  return content
  substitutions = {".html": [HTML], ".md": [MD, HTML], ".yaml": [YAML, HTML]}
  for current_dir, _, files in os.walk(root_dir):
    for name in files:
      path = os.path.join(current_dir, name)
      _, ext = os.path.splitext(path)
      subs = substitutions.get(ext)
      if not subs:
        continue

      with open(path, "rt") as f:
        old_content = f.read()

      new_content = old_content
      for s in subs:
        new_content = new_content  # TODO sub

      if old_content != new_content:
        with open(path, "wt") as f:
          f.write(new_content)
