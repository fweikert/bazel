load("//tools/python:private/defs.bzl", "py_binary", "py_library")

py_binary(
    name = "create_versioned_docs",
    srcs = ["create_versioned_docs.py"],
    data = ["//src/main/java/com/google/devtools/build/lib:generated_docs"],
    deps=["//tools/python/runfiles",        "//third_party/py/abseil",],
)
