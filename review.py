#!/usr/bin/env python

import argparse, datetime, json, os, subprocess, requests


def is_third_monday(d):
    return d.weekday() == 0 and 15 <= d.day <= 21

def find_third_monday(d, days=1, limit=10):
    i = 0
    while not is_third_monday(d):
        d = d + datetime.timedelta(days=days)
        i += 1
        if i > limit:
            return None
    return i * days

def days_from_third_monday(d):
    if d.day < 15:
        return find_third_monday(d)
    elif d.day > 21:
        return find_third_monday(d, -1)
    else:
        forward = find_third_monday(d)
        if not forward:
            return find_third_monday(d, -1)
        return forward

def find_shortnames(workstreams, month):
    shortnames = []

    for workstream in workstreams:
        for standard in workstream["standards"]:
            if month not in standard["review_draft_schedule"]:
                continue
            shortnames.append(href_to_shortname(standard["href"]))

    return shortnames

def href_to_shortname(href):
    return href[len("https://"):href.index(".")]

def maybe_create_prs(shortnames):
    for shortname in shortnames:
        os.chdir("../{}".format(shortname))
        maybe_create_pr(shortname)
        os.chdir(".")

def maybe_create_pr(shortname):
    subprocess.run(["git", "checkout", "master"], capture_output=True)
    commits = subprocess.run(["git", "log", "--format=%s", "--max-count=40"], capture_output=True).stdout
    for subject in commits.split(b"\n"):
        if subject.startswith(b"Meta:"):
            continue
        elif subject.startswith(b"Review Draft Publication:"):
            print("{} had no non-Meta commits since the last publication".format(shortname))
            return
        else:
            break

    today = datetime.datetime.today()
    nice_month = today.strftime("%B %Y")
    path_month = today.strftime("%Y-%m")

    # We should consider merging
    # https://github.com/whatwg/whatwg.org/blob/master/resources.whatwg.org/build/review.sh and
    # https://github.com/whatwg/html/blob/master/review-draft.sh into this script.
    subprocess.run(["make", "review"])

    # This is straight from MAINTAINERS.md and needs to be kept in sync with that.
    pr_body = """The [{} Review Draft](https://{}.spec.whatwg.org/review-drafts/{}) for this Workstream will be published shortly after merging this pull request.

Under the [WHATWG IPR Policy](https://whatwg.org/ipr-policy), Participants may, within 45 days after publication of a Review Draft, exclude certain Essential Patent Claims from the Review Draft Licensing Obligations. See the [IPR Policy](https://whatwg.org/ipr-policy) for details.""".format(nice_month, shortname, path_month)

    subprocess.run(["gh", "pr", "create", "--title", "Review Draft Publication: {}".format(nice_month), "--body", pr_body])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", dest="force", action="store_true")
    args = parser.parse_args()

    today = datetime.datetime.today()
    ideal_publication_diff = days_from_third_monday(today)

    if ideal_publication_diff == 0:
        print("Right on, today is the day!")

    if not args.force:
        if ideal_publication_diff == None:
            print("Publication is at least ten days away. Better wait. Use --force to ignore.")
            exit(1)
        elif ideal_publication_diff > 3:
            print("It's still more than 3 days before publication. Use --force to ignore.")
            exit(1)
        elif ideal_publication_diff < -3:
            print("It's 3 days after publication, hopefully you already published. Use --force to ignore.")
            exit(1)

    db = json.loads(requests.get("https://github.com/whatwg/sg/raw/master/db.json").text)
    shortnames = find_shortnames(db["workstreams"], today.month)

    if len(shortnames) == 0:
        print("Looks like there's nothing to be published this month.")
        exit(1)

    maybe_create_prs(shortnames)

main()
