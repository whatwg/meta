# Contributor Guidelines

These are the general guidelines for contributing to WHATWG standards.

## Committing

See [COMMITTING.md](COMMITTING.md) for further details.

## Pull requests

Leave the **Allow edits from maintainers** option enabled to allow reviewers to fix trivial issues directly on your branch rather than needing to write review comments asking you make the edits. For more details, see [Improving collaboration with forks](https://github.com/blog/2247-improving-collaboration-with-forks) in the GitHub Blog.

## Tests

For normative changes, a corresponding [web-platform-tests](https://github.com/w3c/web-platform-tests) pull request (PR) is needed. The author and reviewer can be different from the PR for the standard. If current behavior is unclear, writing tests first can help inform the discussion. Typically, both PRs will be merged at the same time.

To be clear, a test PR with changes that conflict with the standard cannot land before the corresponding standard is changed.

If testing is not practical, please explain why and if appropriate [file an issue](https://github.com/w3c/web-platform-tests/issues/new) to follow up later.

## Investigation

Often in the course of discussing a potential change, issue with a standard, or browser bug, it's useful to investigate the behavior in question in a variety of rendering engines and provide data back to the discussion. The best way to do this is to host a small test case and report the results in various engines.

For simple cases (not involving multiple files), sites like [Live DOM Viewer](https://software.hixie.ch/utilities/js/live-dom-viewer/) or [JSBin](https://jsbin.com/) are recommended. For cases involving multiple files, you'll likely need to use your own hosting, for example using [GitHub Pages](https://pages.github.com/). Or you could skip straight to working on web-platform-tests, as discussed above.

Attempt to make your test cases produce clearly-differentiable results regarding the different outcomes you're investigating. You can then report the results back to the issue thread using the following Markdown syntax as a starting point:

```markdown
| Test case                               | EdgeHTML | Blink | Gecko | WebKit |
|-----------------------------------------|----------|-------|-------|--------|
| Test case description 1                 |          |       |       |        |
| Test case description 2                 |          |       |       |        |
| Test case description 3                 |          |       |       |        |
```

If there are additional interesting engine variations you are testing, for example older versions or engines not in the list, feel free to add more columns. If you can't test certain engines, leave a question mark in that cell, and others on the thread can help fill them in.

For examples of this kind of investigation in action, see [whatwg/html issue #775](https://github.com/whatwg/html/issues/775#issuecomment-190796607) or [whatwg/html issue #1087](https://github.com/whatwg/html/issues/1087#issue-150128324).
