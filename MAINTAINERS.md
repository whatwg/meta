# Maintainer Guidelines

These are the general guidelines for maintaining WHATWG standards. Mostly boring infrastructure stuff.

## Handling pull requests

Rules for title/message must be satisfied before pull request (PR) is reviewed. See [COMMITTING.md](COMMITTING.md) for further details.

For normative changes, ask for a [web-platform-tests](https://github.com/w3c/web-platform-tests) PR if testing is practical and not overly burdensome. Aim to merge both PRs at the same time. If one PR is approved but the other needs more work, add the `do not merge yet` label or, in web-platform-tests, the `status:needs-spec-decision` label.

If a follow-up issue is filed in the web-platform-tests repository, add the `type:untestable` or `type:missing-coverage` label, and any other appropriate labels, e.g., `html` for the HTML Standard.

Furthermore, for changes affecting one or more implementations, ensure implementation bugs are filed:

* [Chromium](https://crbug.com/new)
* [Gecko](https://bugzilla.mozilla.org/enter_bug.cgi?product=Core&component=DOM)
* [WebKit](https://bugs.webkit.org/enter_bug.cgi?product=WebKit&component=HTML%20DOM)
* [Deno](https://github.com/denoland/deno/issues/new) [^1]
* [Node.js](https://github.com/nodejs/node/issues/new) [^1]
* [webidl2.js](https://github.com/w3c/webidl2.js/issues/new) [^2]
* [widlparser](https://github.com/plinss/widlparser/issues/new) [^2]

[^1]: Only for specifications that these projects implement. This is listed in the pull request template for each WHATWG specification.
[^2]: Only for Web IDL. You might consider pinging [wpt](https://github.com/web-platform-tests/wpt) and [Bikeshed](https://github.com/tabatkins/bikeshed) as well.

And for changes affecting [MDN web docs](https://developer.mozilla.org/), such as the introduction of new features, ensure an [MDN web docs issue](https://github.com/mdn/content/issues/new/choose) is filed (or alternatively a pull request). Ideally the `impacts documentation` label is also used and the `@whatwg/documentation` team is made aware. The team might also be able to assist, though the responsibility lies with the maintainer.

### Merging pull requests

Use the green button on the PR page in the GitHub Web UI:

* Rebase and merge: please ensure each individual commit makes sense on its own and contains the relevant information.
* Squash and merge: remember to delete the PR reference the commit title and clean up the commit body.

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

## Review Drafts

Per the [Workstream Policy](https://whatwg.org/workstream-policy#review-drafts), editors are expected to publish a Review Draft every six months.

To accomplish this the `review.py` script is used (see below), this:

1. Finds which drafts are scheduled to be published the current month as per [db.json](https://github.com/whatwg/sg/blob/main/db.json).
1. Creates a Review Draft source file and updates the Living Standard source file to point to the newly-latest review draft.
1. Creates a pull request for the changes. The pull request body will be:
   ```markdown
   A MONTH YEAR Review Draft (linked) for this Workstream will be published shortly after merging this pull request.

   Under the [WHATWG IPR Policy](https://whatwg.org/ipr-policy), Participants may, within 45 days after publication of a Review Draft, exclude certain Essential Patent Claims from the Review Draft Licensing Obligations. See the [IPR Policy](https://whatwg.org/ipr-policy) for details.
   ```

The editor or deputy editor will then review all is in order and merge it.

### `review.py`

In order to run `python review.py` successfully your environment has to meet these requirements:

* You need to have the relevant Python packages installed, in particular [`requests`](https://pypi.org/project/requests/).
* You need to have the `git` command line utility installed.
* You need to have the [`gh` command line utility](https://cli.github.com/) installed.
* The repositories of the WHATWG standards are supposed to be in parallel directories of the directory you run the script in (presumably `meta`), named after the shortname of the respective standard. E.g., it expects that the git checkout of the Fetch standard is at `../fetch`.
