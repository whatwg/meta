# WHATWG maintainer guidelines

These are the general guidelines for maintaining WHATWG standards. Mostly boring infrastructure stuff.

## Handling pull requests

Each change needs to result in a single commit on the master branch, with no merge commits. The green squash and merge button is OK to use, but be sure to tidy up the commit message per [guidelines for writing good commit messages](https://github.com/erlang/otp/wiki/Writing-good-commit-messages).

Prefix the summary line with "Editorial: " if the change is just to fix formatting, typos, or is a refactoring that does not change how the standard is understood. Note that bug fixes or clarifications are not editorial, even if they only affect non-normative text.

Prefix the summary line with "Meta: " for changes that do not directly affect the text of the standard, but instead the ecosystem around it, such as spec tooling or contributor documentation.

For normative changes, ask for a [web-platform-tests](https://github.com/w3c/web-platform-tests) PR if testing is practical and not overly burdensome. Aim to merge both PRs at the same time. If one PR is approved but the other needs more work, add the `do not merge yet` label or, in web-platform-tests, the `status:needs-spec-decision` label.

If a follow-up issue is filed in the web-platform-tests repository, add the `type:untestable` or `type:missing-coverage` label, and any other appropriate labels, e.g. `html` for the HTML Standard.

### Checking out pull requests from forks

Pull requests from external contributors come from branches in their forks. You can check out those external branches in order to review and test the commits in those pull requests, and to be able to push changes to them on your own (e.g., fixes for typos)—rather than needing to write review comments asking the PR contributor to make the edits.

To checkout a PR branch, note the user it's coming from and the branch they used in their fork. For example, for user `estark37` with branch `example-fix` on the `html` repository, you would do

```bash
git remote add estark37 https://github.com/estark37/html.git
git fetch estark37
git checkout -b estark37-example-fix estark37/example-fix
```

You can then push to the `estark37-example-fix` branch and it will update the `example-fix` branch in `estark37`'s fork, and thus will update the pull request.

#### Git config tweak

It's recommended that you also make the following change to your `git` configuration:

```bash
git config push.default upstream
```

If you make that change, then whenever you're in a local PR branch and want to push changes back to the corresponding external branches, you can just run `git push` with no arguments (rather than also needing to specify the remote name and branch name as arguments). Otherwise, you need to also specify the remote name and branch name each time you push.

If you want to enable that same ability for all your project clones, also specify the `--global` option: `git config --global push.default upstream`.

#### Helper script

You can add the following helper script to your `.bash_profile` or similar to make the process above slightly simpler:

```bash
checkout-pr() {
  local REPO=`basename $(git config remote.origin.url | cut -d: -f2-)`
  local REMOTE_URL=https://github.com/$1/$REPO
  if [ "`git config remote.origin.url | cut -d: -f1`" == "git@github.com" ]; then
      REMOTE_URL="git@github.com:$1/$REPO"
  fi
  git remote add $1 $REMOTE_URL 2> /dev/null
  git fetch $1
  git checkout -b $1-$2 $1/$2
}
```

You can then use it as

```bash
checkout-pr estark37 example-fix
```

### Merging pull requests into master

Just use the normal green button in the pull-request page in the GitHub Web UI, but first ensure the commit message follows [the guidelines](https://github.com/erlang/otp/wiki/Writing-good-commit-messages).

#### Merging to master from the command line

Regardless of whether a pull request comes from a contributor (in which case the branch is from a different remote repository and you've already used the **Checking out pull requests from forks** steps above to fetch the branch) or from other editors or members of the WHATWG GitHub organization (in which case the branch is in the main repository), the steps for cleanly merging it to master are the same:

```bash
git checkout BRANCH_NAME
git rebase master
... build and review the spec ...
git push --force
git checkout master
git merge BRANCH_NAME --ff-only
```

This checks out the PR's commits, rebases them on `master`, then fast-forwards `master` to include them.

The `git push --force` line here ensures that the original branch gets updated to sit on top of `master` as well. This ensures GitHub can automatically figure out that the commits were merged, and thus automatically close the pull request with a nice purple "merged" status. So at this point you can do a `git push origin master` to push the changes, and GitHub will close the PR and mark it as merged.
