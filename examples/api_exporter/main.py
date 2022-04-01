import sys

from tools.python.runfiles import runfiles
from src.main.protobuf import builtin_pb2


def main(argv=None):
    r = runfiles.Create()
    path = r.Rlocation("io_bazel/src/main/java/com/google/devtools/build/lib/builtin.pb")
    with open(path, "rb") as f:
        content = f.read()

    proto = builtin_pb2.Builtins.FromString(content)
    # Do something with proto. See https://github.com/bazelbuild/bazel/blob/master/src/main/protobuf/builtin.proto for fields
    print(proto)


if __name__ == "__main__":
    sys.exit(main())