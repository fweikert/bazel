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

"""TODO
"""
import os
import shutil
import sys
import tarfile
import tempfile
import zipfile

from absl import app
from absl import flags

from scripts.docs import rewrite_links
from tools.python.runfiles import runfiles

FLAGS = flags.FLAGS

flags.DEFINE_string("version", None, "Name of the Bazel release. If None, the version will be read from the git branch name.")
flags.DEFINE_string("output_path", None, "Location where the zip'ed documentation should be written to.")


_DOC_EXTENSIONS = set([".html", ".md", ".yaml"])


def extract(archive_path, open_func, output_dir):
  with open_func(archive_path, "r") as archive:
      archive.extractall(output_dir)


def maybe_rewrite(path, version):
  _, ext = os.path.splitext(path)
  if ext not in _DOC_EXTENSIONS:
    return

  with open(path, "rt") as f:
    content = f.read()

  new_content = rewrite_links.rewrite_links(content, ext, version)
  if new_content != content:
    with open(path, "wt") as f:
      f.write(new_content)


def main(unused_argv):
  if not FLAGS.version:
    print("Missing --version flag.", file=sys.stderr)
    exit(1)

  if not FLAGS.output_path:
    print("Missing --output_path flag.", file=sys.stderr)
    exit(1)

  version = FLAGS.version
  output_path = FLAGS.output_path

  r = runfiles.Create()

  tmp_dir = tempfile.mkdtemp()
  version_root = os.path.join(tmp_dir, version)
  os.makedirs(version_root)
  extract(r.Rlocation("io_bazel/site/en/docs.tar"), tarfile.open, version_root)

  extract(r.Rlocation("io_bazel/src/main/java/com/google/devtools/build/lib/reference-docs.zip"), zipfile.ZipFile, version_root)

  with open(r.Rlocation("io_bazel/site/en/versions/_toc.yaml"), "rt") as f:
    toc = f.read()

  # TODO: rewrite TOC
  new_toc = toc

  toc_path = os.path.join(version_root, "_toc.yaml")
  with open(toc_path, "wt") as f:
    f.write(new_toc)

  with zipfile.ZipFile(output_path, "w") as archive:
    for root, _, files in os.walk(tmp_dir):
      for f in files:
        src = os.path.join(root, f)
        # read-only: need to copy file first, or look at zip functions
        # maybe_rewrite(src, version)

        dest = src[len(tmp_dir) + 1:]
        archive.write(src, dest)


if __name__ == "__main__":
  FLAGS(sys.argv)
  app.run(main)
