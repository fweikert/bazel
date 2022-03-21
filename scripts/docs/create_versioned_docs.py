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
import sys
import zipfile

from absl import app
from absl import flags

from tools.python.runfiles import runfiles

FLAGS = flags.FLAGS

flags.DEFINE_string("output_dir", None, "Directory where the documentation should be written to.")
flags.DEFINE_string("version", None, "Name of the Bazel release. If None, the version will be read from the git branch name.")


def main(unused_argv):
  r = runfiles.Create()

  get_path = lambda f : r.Rlocation("io_bazel/src/main/java/com/google/devtools/build/lib/{}".format(f))

  with open(get_path("command-line-reference.html"), "r") as f:
    ref = f.readlines()
  with zipfile.ZipFile(get_path("build-encyclopedia.zip"), "r") as archive:
    print(archive.namelist())
  with zipfile.ZipFile(get_path("skylark-library.zip"), "r") as archive:
    print(archive.namelist())
  #  x = FLAGS.output_dir
  #  y = FLAGS.version


if __name__ == "__main__":
  FLAGS(sys.argv)
  app.run(main)
