# WHATWG committer guidelines

## Branches

Branches are transient and their names must be detailed enough to avoid confusion. Choose short and descriptive names. Using hyphens to separate words is encouraged _(but not required)_.

```bash
# good
$ git checkout -b descriptive-name-relative-to-feature
```

```bash
# bad - too vague and malformatted
$ git checkout -b fix_paragraph-header
```

Identifiers from corresponding Github issues are great candidates for use in branch names. For example, when working on an issue:

```bash
$ git checkout -b issue-15
```

## Committing

Each change needs to result in a single commit on the master branch, with no merge commits. The green squash and merge button is OK to use, but be sure to tidy up the commit message per [guidelines for writing good commit messages](https://github.com/erlang/otp/wiki/Writing-good-commit-messages).

Prefix the summary line with "Editorial: " if the change is just to fix formatting, typos, or is a refactoring that does not change how the standard is understood. Note that bug fixes or clarifications are not editorial, even if they only affect non-normative text.

Prefix the summary line with "Meta: " for changes that do not directly affect the text of the standard, but instead the ecosystem around it, such as spec tooling or contributor documentation.

## Conventions

Write a title and message that will allow your future self to understand the intent of change without looking at the diff. This will not only benefit the author but also the reviewer and will better allow intent expression versus implementation details.

## Example

From: http://git-scm.com/book/ch5-2.html

```
Provide a short summary of changes
 [line intentionally left blank]
More detailed explanatory text, if necessary.  Wrap it to about 72
characters or so.  In some contexts, the first line is treated as the
subject of an email and the rest of the text as the body.  The blank
line separating the summary from the body is critical (unless you omit
the body entirely); tools like rebase can get confused if you run the
two together.

Further paragraphs come after blank lines.

  - Bullet points are okay, too

  - Typically a hyphen or asterisk is used for the bullet, preceded by a
    single space, with blank lines in between, but conventions vary here
```
