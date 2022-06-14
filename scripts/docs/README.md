bazel build //scripts/docs:gen_release_docs --config=docs

bazel build //scripts/docs:gen_new_toc_ --config=docs

bazel test --test_output=streamed //scripts/docs:rewriter_test