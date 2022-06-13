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

from scripts.docs import rewriter

FLAGS = flags.FLAGS

flags.DEFINE_string("version", None, "Name of the Bazel release.")
flags.DEFINE_string("toc_path", None, "Path to the _toc.yaml file that contains the table of contents for the versions menu.")
flags.DEFINE_string("narrative_docs_path", None, "Path of the archive (zip or tar) that contains the narrative documentation.")
flags.DEFINE_string("reference_docs_path", None, "Path of the archive (zip or tar) that contains the reference documentation.")
flags.DEFINE_string("output_path", None, "Location where the zip'ed documentation should be written to.")

_ARCHIVE_FUNCTIONS = {".tar": tarfile.open, ".zip": zipfile.ZipFile}


def try_extract(flag_name, archive_path, output_dir):
  if not archive_path:
    raise ValueError("Missing --{} flag".format(flag_name))

  _, ext = os.path.splitext(archive_path)
  open_func = _ARCHIVE_FUNCTIONS.get(ext)
  if not open_func:
    raise open_func("Flag --{}: Invalid file extension '{}'. Allowed: {}", flag_name, ext, _ARCHIVE_FUNCTIONS.keys.join(", "))

  with open_func(archive_path, "r") as archive:
      archive.extractall(output_dir)


def get_versioned_content(path, version):
  with open(path, "rt") as f:
    content = f.read()

  return rewriter.rewrite_links(path, content, version)


def update_table_of_contents(input_path, output_path):
  if not input_path or not input_path.endswith("_toc.yaml"):
    print("{}".format, input_path, file=sys.stderr)
    exit(1)

  with open(input_path, "rt") as f:
    toc = f.read()

  # TODO: rewrite TOC
  new_toc = toc

  with open(output_path, "wt") as f:
    f.write(new_toc)


def main(unused_argv):
  if not FLAGS.version:
    print("Missing --version flag.", file=sys.stderr)
    exit(1)

  if not FLAGS.output_path:
    print("Missing --output_path flag.", file=sys.stderr)
    exit(1)

  version = FLAGS.version
  output_path = FLAGS.output_path

  tmp_dir = tempfile.mkdtemp()
  toc_dest_path = os.path.join(tmp_dir, "_toc.yaml")
  shutil.copyfile(FLAGS.toc_path, toc_dest_path)

  version_root = os.path.join(tmp_dir, version)
  os.makedirs(version_root)
  try_extract("narrative_docs_path", FLAGS.narrative_docs_path, version_root)
  try_extract("reference_docs_path", FLAGS.reference_docs_path, version_root)

  with zipfile.ZipFile(output_path, "w") as archive:
    for root, _, files in os.walk(tmp_dir):
      for f in files:
        src = os.path.join(root, f)
        dest = src[len(tmp_dir) + 1:]

        if rewriter.can_rewrite(src):
          archive.writestr(dest, get_versioned_content(src, version))
        else:
          archive.write(src, dest)


if __name__ == "__main__":
  FLAGS(sys.argv)
  app.run(main)
