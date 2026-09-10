"""Contains fixes for .mdx syntax errors in both generated and narrative docs.

This code is invoked for generated docs via docs2mdx.py, and for narrative docs
(static .mdx files) via create_release_docs.py.

Right now we need to process narrative docs since the 8.x and 9.x release
branches have several syntax errors in their .mdx files.
Once we move to Bazel 10 and beyond, this should no longer be necessary, which will
allow us to move this code into docs2mdx.
"""
import re


def apply(content):
  return content