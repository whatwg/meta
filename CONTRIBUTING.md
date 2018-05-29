# Contributor Guidelines

These are the general guidelines for contributing to WHATWG standards.

## Committing

See [COMMITTING.md](COMMITTING.md) for further details.

## Getting started

If this is your first time contributing to the WHATWG standards, check out the global list of [good first issues](https://github.com/search?q=is%3Aopen+label%3A%22good+first+issue%22+user%3Awhatwg&type=Issues) and find one you want to work on. You should comment in the thread to let others know you will be working on the issue. This is a great time to ask any questions that you may have.

Contributions to older issues are always appreciated. If an issue hasn't been updated in a while, you should ask if the issue is still relevant before working on it. If someone else was previously working on an issue, and you want to work on it, it's polite to ask that person if you can work on the issue before taking it.

## Pull requests

Leave the **Allow edits from maintainers** option enabled to allow reviewers to fix trivial issues directly on your branch rather than needing to write review comments asking you make the edits. For more details, see [Improving collaboration with forks](https://github.com/blog/2247-improving-collaboration-with-forks) in the GitHub Blog.

## Building

All WHATWG standards, apart from HTML, have a `Makefile` in their repository to help with building them. You'll need `make` and [`curl`](https://curl.haxx.se/) installed at the minimum; ideally you'll also have a full Bash shell. These prerequisites should be present on most Linux and macOS systems already. For Windows, we recommend [Git Bash](https://gitforwindows.org/) and [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm).

Once you have the prerequisites, you can run `make` in the standard's directory to build the spec; it will appear as a `.html` file in the same directory. This will call out to a web service to build the standard, so be sure you're connected to the internet.

Other Make targets are also available:

* `make deploy` will do a full "deploy" of the standard, including error checking, commit snapshot production, any extra build steps, into a local subdirectory.
* `make local` will do a local build, without calling out to any web services. This requires having [Bikeshed](https://github.com/tabatkins/bikeshed) installed locally.

Due to its large size, the HTML Standard has its own build process, which you can read about in the [html-build repository](https://github.com/whatwg/html-build/blob/master/README.md).

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

## Further principles and guidelines

For any changes please take into account the following principles and guidelines:

* [HTML Design Principles](https://www.w3.org/TR/html-design-principles/) (note that these are applicable outside of HTML too and you are expected to treat them as such)
* [Client-side API Design Principles](https://w3ctag.github.io/design-principles/)
* [WHATWG Working Mode](https://whatwg.org/working-mode)
* [WHATWG FAQ](https://whatwg.org/faq), in particular [Is there a process for removing bad ideas from a standard?](https://whatwg.org/faq#removing-bad-ideas) and [How should I go about proposing new features to WHATWG standards?](https://whatwg.org/faq#adding-new-features)
