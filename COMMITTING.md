# Committer Guidelines


## General

Each change needs to result in a single commit on the master branch, with no merge commits. The green squash and merge button is OK to use, but be sure to tidy up the commit message per the below guidelines. In particular, if you use the squash functionality, delete the parenthetical pull request number that GitHub adds.

## Commit messages

(Derived from the [erlang/otp wiki](https://github.com/erlang/otp/wiki/Writing-good-commit-messages).)

### Purpose

Great commit messages serve at least three important purposes:

* To help pull requests reviewers understand what is being changed.
* To make it easy and pleasant to review the history of the repository.
* To help future maintainers find out why a particular change was made.

As such, you should write a commit message that will allow your future self to understand the intent of change without looking at the diff. This will not only benefit reviewers, but also other maintainers. Your commit message should express intent without delving into implementation details.

For more on this topic, see ["On commit messages"](https://who-t.blogspot.com/2009/12/on-commit-messages.html).

### Structure and conventions

Commit messages consist of a single title line, a blank line, and then a more detailed change description. The description (and preceding blank line) may be omitted for simple fixes.

All lines should be at most 72 characters, to make them easier to view in GitHub and other tools. Single "words" are an exception to this convention (e.g., URLs). Some sources recommend restricting the title line to 50 characters, but we do not enforce this.

The title must be written in imperative mode, as if commanding someone. This means using verb conjugations such as "fix"/"add"/"change" instead of "fixed"/"added"/"changed" or "fixing"/"adding"/"changing". We are less consistent with the description, but often use present tense (e.g., "This change adds…").

Title lines must not end in a period; they are titles, not sentences.

Be sure to reference related GitHub issues within pull requests so they are appropriately cross-linked by GitHub. Use "closes" or "fixes" as appropriate to [automatically close issues](https://help.github.com/articles/closing-issues-using-keywords/).

Avoid using Markdown-style code markup (i.e., backticks) unless necessary for disambiguation.

### Title prefixes

Prefix the title line with **"Editorial: "** if the change is just to fix formatting, typos, or is a refactoring that does not change how the standard is understood. Note that bug fixes or clarifications are not editorial, even if they only affect non-normative text.

Prefix the title line with **"Meta: "** for changes that do not directly affect the text of the standard, but instead the ecosystem around it, such as spec tooling or contributor documentation.

In general, most commits do not have a prefix.

### Example

```
Editorial: Fix formatting and typo

Fixes #35, fixes #38, fixes #21

This is descriptive text providing details further explaining the title above. There is no restriction to the line length of this commit summary.

Do remember to insert a single blank line between multiple paragraphs within the commit summary.
```
