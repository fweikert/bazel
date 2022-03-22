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

from tools.python.runfiles import runfiles

FLAGS = flags.FLAGS

flags.DEFINE_string("version", None, "Name of the Bazel release. If None, the version will be read from the git branch name.")
flags.DEFINE_string("output_path", None, "Location where the zip'ed documentation should be written to.")


def extract(archive_path, open_func, output_dir):
  os.makedirs(output_dir)
  with open_func(archive_path, "r") as archive:
      archive.extractall(output_dir)


def main(unused_argv):
  if not FLAGS.version:
    print("Missing --version flag.", file=sys.stderr)
    exit(1)

  if not FLAGS.output_path:
    print("Missing --output_path flag.", file=sys.stderr)
    exit(1)

  r = runfiles.Create()
  gen_path = lambda f : r.Rlocation("io_bazel/src/main/java/com/google/devtools/build/lib/{}".format(f))

  tmp_dir = tempfile.mkdtemp()
  version_root = os.path.join(tmp_dir, FLAGS.version)
  extract(r.Rlocation("io_bazel/site/en/docs.tar"), tarfile.open, version_root)

  clr_dir = os.path.join(version_root, "reference")
  shutil.copy(gen_path("command-line-reference.html"), clr_dir)

  be_root = os.path.join(version_root, "reference", "be")
  extract(gen_path("build-encyclopedia.zip"), zipfile.ZipFile, be_root)

  starlark_root = os.path.join(version_root, "rules", "lib")
  extract(gen_path("skylark-library.zip"), zipfile.ZipFile, starlark_root)

  repo_root = os.path.join(starlark_root, "repo")
  extract(r.Rlocation("io_bazel/tools/build_defs/repo/doc.tar"), tarfile.open, repo_root)

  # TODO: rewrite links
  # TODO: write version file

  with zipfile.ZipFile(FLAGS.output_path, "w") as archive:
    for root, _, files in os.walk(tmp_dir):
      for f in files:
        src = os.path.join(root, f)
        dest = src[len(tmp_dir) + 1:]
        archive.write(src, dest)


if __name__ == "__main__":
  FLAGS(sys.argv)
  app.run(main)
