#!/usr/bin/env python

import argparse, datetime, json, os, subprocess, requests


def makeGroupsofFive(workstraems):
    groups = [[]]
    i = 0
    group = 0

    for workstream in workstraems:
        for standard in workstream["standards"]:
            shortname = href_to_shortname(standard["href"])
            if i != 0 and i % 5 == 0:
                groups.append([])
                group += 1
            groups[group].append(shortname)
            i += 1

    return groups

def href_to_shortname(href):
    return href[len("https://"):href.index(".")]


def maybeCreatePRs(group):
    for shortname in group:
        os.chdir("../{}".format(shortname))
        maybeCreatePR(shortname)
        os.chdir(".")

def maybeCreatePR(shortname):
    subprocess.run(["git", "checkout", "master"], capture_output=True)
    commits = subprocess.run(["git", "log", "--pretty=oneline", "--abbrev-commit", "--abbrev=8", "--max-count=40"], capture_output=True).stdout
    for commit in commits.split(b"\n"):
        # Remove the leading prefix (see --abbrev=8 above, which cannot be 0, plus a space)
        commitTitle = commit[8+1:]
        if commitTitle.startswith(b"Meta:"):
            continue
        elif commitTitle.startswith(b"Review Draft Publication:"):
            print("{} had no normative commits since the last publication".format(shortname))
            return
        else:
            break

    # We could consider merging
    # https://github.com/whatwg/whatwg.org/blob/master/resources.whatwg.org/build/review.sh and
    # https://github.com/whatwg/html/blob/master/review-draft.sh into this script.
    subprocess.run(["make", "review"])

    # This is straight from MAINTAINERS.md and needs to be kept in sync with that.
    prBody = """A Review Draft for this Workstream will be published shortly, by merging this pull request.

Under the [WHATWG IPR Policy](https://whatwg.org/ipr-policy), Participants may, within 45 days after publication of a Review Draft, exclude certain Essential Patent Claims from the Review Draft Licensing Obligations. See the [IPR Policy](https://whatwg.org/ipr-policy) for details."""

    # TODO: should we expand prBody to include instructions for the maintainer with respect to the
    # subsequent comment and such?
    subprocess.run(["gh", "pr", "create", "--title", "Review Draft Publication: {}".format(datetime.datetime.now().strftime("%B %G")), "--body", prBody])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", metavar="N", type=int, choices=range(1,4), required=True)
    args = parser.parse_args()

    db = json.loads(requests.get("https://github.com/whatwg/sg/raw/master/db.json").text)

    groups = makeGroupsofFive(db["workstreams"])
    # See https://github.com/whatwg/sg/issues/127
    if len(groups) > 6:
        print("Please file an issue against whatwg/sg to discuss a new Review Draft publication policy.")
    if len(groups) > 3:
        print("Please update the calendar (and this script) to account for more groups.")

    maybeCreatePRs(groups[args.group-1])

main()
