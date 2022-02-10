import os
import re
import sys


_TEMPLATE = """
<div style="background-color: #EFCBCB; color: #AE2B2B;  border: 1px solid #AE2B2B; border-radius: 5px; border-left: 10px solid #AE2B2B; padding: 0.5em;">
<b>IMPORTANT:</b> The Bazel docs have moved! Please update your bookmark to <a href="https://bazel.build/{0}" style="color: #0000EE;">https://bazel.build/{0}</a>
<p/>
You can <a href="DS_BLOG_URL" style="color: #0000EE;">read about</a> the migration, and let us <a href="https://forms.gle/onkAkr2ZwBmcbWXj7" style="color: #0000EE;">know what you think</a>.
</div>
"""

_DOC_EXTENSIONS = set(['.html', '.md'])

_PATTERN = re.compile(r'^---$', re.MULTILINE)

_MAPPING = {
  'bazel-overview.md': 'start/bazel-intro',
  'bazel-vision.md': 'start/bazel-vision',
  'getting-started.md': 'start/getting-started',
  'install.md': 'install',
  'install-redhat.md': 'install/redhat',
  'install-os-x.md': 'install/os-x',
  'install-suse.md': 'install/suse',
  'install-ubuntu.md': 'install/ubuntu',
  'install-windows.md': 'install/windows',
  'install-compile-source.md': 'install/compile-source',
  'install-bazelisk.md': 'install/bazelisk',
  'completion.md': 'install/completion',
  'ide.md': 'install/ide',
  'migrate-maven.md': 'migrate/maven',
  'migrate-xcode.md': 'migrate/xcode',
  'migrate-cocoapods.md': 'migrate/cocoapods',
  'tutorial/cpp.md': 'tutorials/cpp',
  'cpp-use-cases.md': 'tutorials/cpp-use-cases',
  'tutorial/java.md': 'tutorials/java',
  'tutorial/android-app.md': 'tutorials/android-app',
  'tutorial/ios-app.md': 'tutorials/ios-app',
  'versions/main/tutorial/cc-toolchain-config.md': 'tutorials/cc-toolchain-config',
  'build-ref.html': 'concepts/build-ref',
  'versions/main/build-ref.md#labels': 'concepts/labels',
  'versions/main/build-ref.md#name': 'concepts/labels',
  'versions/main/build-ref.md#BUILD_files': 'concepts/build-files',
  'versions/main/build-ref.md#dependencies': 'concepts/dependencies',
  'external.md': 'docs/external',
  'bzlmod.md': 'docs/bzlmod',
  'configurable-attributes.md': 'docs/configurable-attributes',
  'platforms-intro.md': 'concepts/platform-intro',
  'visibility.md': 'concepts/visibility',
  'hermeticity.md': 'concepts/hermeticity',
  'versioning.md': 'release/versioning',
  'releases.md': 'release',
  'backward-compatibility.md': 'release/backward-compatibility',
  'updating-bazel.md': 'versions/updating-bazel',
  'guide.md': 'docs/build',
  'memory-saving-mode.md': 'docs/memory-saving-mode',
  'windows.md': 'docs/windows',
  'best-practices.md': 'docs/best-practices',
  'skylark/tutorial-sharing-variables.md': 'rules/tutorial-sharing-variables',
  'query-how-to.html': 'docs/query-how-to',
  'query.html': 'reference/query',
  'cquery.html': 'docs/cquery',
  'aquery.html': 'docs/aquery',
  'remote-execution.md': 'docs/remote-execution',
  'remote-execution-rules.md': 'docs/remote-execution-rules',
  'remote-execution-ci.md': 'docs/remote-execution-ci ',
  'dynamic-execution.md': 'docs/dynamic-execution',
  'remote-execution-sandbox.md': 'docs/remote-execution-sandbox',
  'workspace-log.md': 'docs/workspace-log',
  'remote-execution-caching-debug.md': 'docs/remote-execution-caching-debug',
  'remote-caching.md': 'docs/remote-caching',
  'remote-caching-debug.md': 'docs/remote-caching-debug',
  'user-manual.html': 'docs/user-manual',
  'be/overview.md': 'reference/build-encyclopedia',
  'test-encyclopedia.html': 'reference/test-encyclopedia',
  'skylark/build-style.md': 'rules/build-style',
  'build-event-protocol.md': 'docs/build-event-protocol',
  'bep-examples.md': 'docs/bep-examples',
  'bep-glossary.md': 'docs/bep-glossary',
  'output_directories.md': 'docs/output_directories',
  'platforms.md': 'docs/platforms',
  'exec-groups.md': 'reference/exec-groups',
  'toolchains.md': 'docs/toolchains',
  'skylark/concepts.md': 'rules/concepts',
  'skylark/language.md': 'rules/language',
  'skylark/bzl-style.md': 'rules/bzl-style',
  'skylark/macros.md': 'rules/macros',
  'skylark/rules.md': 'rules/rules',
  'skylark/depsets.md': 'rules/depsets',
  'skylark/aspects.md': 'rules/aspects',
  'skylark/repository_rules.md': 'rules/repository_rules',
  'skylark/config.md': 'rules/config',
  'rules.md': 'rules',
  'skylark/rules-tutorial.md': 'rules/rules-tutorial',
  'skylark/windows_tips.md': 'rules/windows_tips',
  'rule-challenges.md': 'docs/rule-challenges',
  'skylark/tutorial-creating-a-macro.md': 'rules/tutorial-creating-a-macro',
  'skylark/tutorial-custom-verbs.md': 'rules/tutorial-custom-verbs',
  'skylark/testing.md': 'rules/testing',
  'skylark/performance.md': 'rules/performance',
  'skylark/deploying.md': 'rules/deploying',
  'persistent-workers.md': 'docs/persistent-workers',
  'multiplex-worker.md': 'docs/multiplex-worker',
  'creating-workers.md': 'docs/creating-workers',
  'contributing.md': 'contribute',
  'governance.md': 'contribute/contribution-policy',
  'recommended-rules.md': 'contribute/recommended-rules',
  'support.md': 'contribute/support',
  'https://bazel.build/help.md': 'help',
  'basics/getting_started.md': 'contribute/getting-started',
  'basics/patching.md': 'contribute/patch-acceptance',
  'designs/index.md': 'contribute/design-documents',
  'basics/release-notes.md': 'contribute/release-notes',
  'naming.md': 'contribute/naming',
  'maintaining/breaking-changes-guide.md': 'contribute/breaking-changes',
  'maintaining/maintainers-guide.md': 'contribute/maintainers-guide',
  'maintaining/windows-chocolatey-maintenance.md': 'contribute/windows-chocolatey-maintenance',
  'maintaining/windows-scoop-maintenance.md': 'contribute/windows-scoop-maintenance',
  'https://bazel.build/basics/docs-style.md': 'contribute/docs-style-guide',
  'experts.md': 'community/experts',
  'tutorial/cc-toolchain-config.md': 'tutorials/cc-toolchain-config',
  'toolchain_resolution_implementation.md': 'docs/toolchain_resolution_implementation',
  'bazel-and-javascript.md': 'docs/bazel-and-javascript',
  'sandboxing.md': 'docs/sandboxing',
  'android-build-performance.md': 'docs/android-build-performance',
  'glossary.md': 'reference/glossary',
  'bazel-and-apple.md': 'docs/bazel-and-apple',
  'android-instrumentation-test.md': 'docs/android-instrumentation-test',
  'cc-toolchain-config-reference.md': 'docs/cc-toolchain-config-reference',
  'mobile-install.md': 'docs/mobile-install',
  'bazel-and-android.md': 'docs/bazel-and-android',
  'integrating-with-rules-cc.md': 'docs/integrating-with-rules-cc',
  'android-ndk.md': 'docs/android-ndk',
  'bazel-and-java.md': 'docs/bazel-and-java',
  'bazel-and-cpp.md': 'docs/bazel-and-cpp',
  'bazel-container.md': 'docs/bazel-container',
  'skylark/index.md': 'rules/index',
  'skylark/faq.md': 'rules/faq',
  'skylark/errors/read-only-variable.md': 'rules/errors/read-only-variable',
  'coverage.md': 'docs/coverage',
}

def main():
  docs_dir = os.path.join(os.getcwd(), 'site/docs')
  for root, dirs, files in os.walk(docs_dir):
    for f in files:
      _, ext = os.path.splitext(f)
      if ext not in _DOC_EXTENSIONS:
        continue

      full_path = os.path.join(root, f)
      rel_path = os.path.relpath(full_path, docs_dir)
      destination = _MAPPING.get(rel_path)
      if not destination:
        print('Failed to find destination for {}'.format(rel_path), file=sys.stderr)
        continue

      callout = _TEMPLATE.format(destination)

      with open(full_path, 'rt') as f:
        content = f.read()

      parts = _PATTERN.split(content, maxsplit=2)
      if len(parts) != 3:
        print('Failed to parse {}'.format(rel_path), file=sys.stderr)
        continue

      new_content = ''.join([parts[0], '---', parts[1], '---\n', callout, parts[2]])
      with open(full_path, 'wt') as f:
        f.write(new_content)


if __name__ == '__main__':
    sys.exit(main())
