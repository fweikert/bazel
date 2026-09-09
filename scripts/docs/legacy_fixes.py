"""Contains fixes of various legacy .mdx syntax errors.

We only need this module since older Bazel release branches contain
syntax errors in code comments and Markdown docs.
With Bazel 10+ all of them should be fixed, thus makign this file obsolete.
"""
import re


def apply(content):
  return content