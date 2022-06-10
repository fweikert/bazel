load("//tools/python:private/defs.bzl", "py_binary", "py_library")

# Requires --config=docs
genrule(
    name = "gen_versioned_docs",
    srcs = [
        "//site/en:docs",
        "//site/en:versions/_toc.yaml",
        "//src/main/java/com/google/devtools/build/lib:reference-docs.zip",
    ],
    cmd = "$(location :create_versioned_docs)" +
          " --version=$$(grep BUILD_SCM_REVISION bazel-out/volatile-status.txt | sed 's/^BUILD_SCM_REVISION //')" +
          " --toc_path=$(location //site/en:versions/_toc.yaml)" +
          " --narrative_docs_path=$(location //site/en:docs)" +
          " --reference_docs_path=$(location //src/main/java/com/google/devtools/build/lib:reference-docs.zip)" +
          " --output_path=$(OUTS)",
    outs = [
      "versioned_docs.zip",
    ],
    tools = [
        ":create_versioned_docs",
    ],
    stamp = 1,
)

py_binary(
    name = "create_versioned_docs",
    srcs = ["create_versioned_docs.py"],
    deps = [
      ":rewriter",
      "//third_party/py/abseil",
    ],
)

py_library(
    name = "rewriter",
    srcs = ["rewriter.py"],
)
