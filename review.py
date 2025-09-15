#!/usr/bin/env python
#
# See https://github.com/whatwg/meta/blob/main/MAINTAINERS.md#review-drafts for some notes on how to
# run this.

import argparse, datetime, json, os, subprocess, requests, glob, re


def print_header(string):
    print()
    print(f"\x1b[1m{string}\x1b[0m")
    print()

def fetch_json(url):
    return json.loads(requests.get(url).text)

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

def find_shortnames(workstreams, month=None):
    shortnames = []

    for workstream in workstreams:
        for standard in workstream["standards"]:
            if month and month not in standard["review_draft_schedule"]:
                continue
            shortnames.append(href_to_shortname(standard["href"]))

    return shortnames

def href_to_shortname(href):
    return href[len("https://"):href.index(".")]

def replace_rd_pointer(shortname, contents, path_month):
    if shortname != "html":
        return re.sub(
            "Text Macro: LATESTRD [0-9]+-[0-9]+",
            f"Text Macro: LATESTRD {path_month}",
            contents
        )

    return re.sub(
        "<a href=\"/review-drafts/[0-9]+-[0-9]+/\">",
        f"<a href=\"/review-drafts/{path_month}/\">",
        contents
    )

def add_date_to_rd(shortname, contents, today):
    if shortname != "html":
        metadata_date = today.strftime("%Y-%m-%d")
        return contents.replace(
            "Group: WHATWG",
            f"Group: WHATWG\nStatus: RD\nDate: {metadata_date}"
        )

    title_date = today.strftime("%B %Y")
    contents = contents.replace(
        "<title w-nodev>HTML Standard</title>",
        f"<title w-nodev>HTML Standard Review Draft {title_date}</title>"
    )

    # This intentionally removes the <span class="pubdate"> since otherwise Wattsi would put in the build date.
    pubdate = today.strftime("%d %B %Y")
    contents = contents.replace(
        '<p w-nohtml w-nosnap id="living-standard">Review Draft &mdash; Published <span class="pubdate">[DATE: 01 Jan 1901]</span></p>',
        f'<p w-nohtml w-nosnap id="living-standard">Review Draft &mdash; Published {pubdate}</p>'
    )

    return contents

def create_pr(shortname, today):
    nice_month = today.strftime("%B %Y")
    path_month = today.strftime("%Y-%m")

    # This is straight from MAINTAINERS.md and needs to be kept in sync with that.
    pr_body = f"""The [{nice_month} Review Draft](https://{shortname}.spec.whatwg.org/review-drafts/{path_month}/) for this Workstream will be published shortly after merging this pull request.

Under the [WHATWG IPR Policy](https://whatwg.org/ipr-policy), Participants may, within 45 days after publication of a Review Draft, exclude certain Essential Patent Claims from the Review Draft Licensing Obligations. See the [IPR Policy](https://whatwg.org/ipr-policy) for details."""

    subprocess.run(["gh", "pr", "create", "--title", f"Review Draft Publication: {nice_month}", "--body", pr_body])

def maybe_create_branch(shortname, today):
    subprocess.run(["git", "checkout", "main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    subprocess.run(["git", "pull"], stdout=subprocess.DEVNULL, check=True)
    commits = subprocess.run(["git", "log", "--format=%s", "--max-count=40"], capture_output=True, check=True).stdout
    for subject in commits.split(b"\n"):
        if subject.startswith(b"Meta:"):
            continue
        elif subject.startswith(b"Review Draft Publication:"):
            print_header(f"{shortname} had no non-Meta commits since the last publication")
            return False
        else:
            print_header(f"Processing {shortname}")
            break

    nice_month = today.strftime("%B %Y")
    path_month = today.strftime("%Y-%m")

    subprocess.run(["git", "branch", "-D", f"review-draft-{path_month}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "checkout", "-B", f"review-draft-{path_month}"], check=True)

    input_file = "source" if shortname == "html" else glob.glob("*.bs")[0]

    with open(input_file, "r", encoding="utf-8", newline="\n") as file:
        contents = file.read()
    contents = replace_rd_pointer(shortname, contents, path_month)
    with open(input_file, "w", encoding="utf-8", newline="\n") as file:
        file.write(contents)

    print("\nUpdated Living Standard to Point to the new Review Draft.")
    print("Please verify that only one lined changed:")
    subprocess.run(["git", "--no-pager", "diff"])

    os.makedirs("review-drafts", exist_ok=True)
    review_draft_contents = add_date_to_rd(shortname, contents, today)

    file_extension = "wattsi" if shortname == "html" else "bs"
    review_draft_file = f"review-drafts/{path_month}.{file_extension}"
    with open(review_draft_file, "w", encoding="utf-8", newline="\n") as file:
        file.write(review_draft_contents)

    print(f"\nCreated Review Draft at {review_draft_file}")
    print(f"Please verify that only two lines changed relative to {input_file}:")
    subprocess.run(["git", "--no-pager", "diff", "--no-index", input_file, review_draft_file])

    print()

    subprocess.run(["git", "add", input_file], stdout=subprocess.DEVNULL, check=True)
    subprocess.run(["git", "add", "review-drafts/*"], stdout=subprocess.DEVNULL, check=True)
    subprocess.run(["git", "commit", "-m", f"Review Draft Publication: {nice_month}"], stdout=subprocess.DEVNULL, check=True)

    return True

def regenerate_rd(shortname, today):
    print_header(f"Regenerating Review Draft for {shortname}")

    path_month = today.strftime("%Y-%m")
    input_file = "source" if shortname == "html" else glob.glob("*.bs")[0]

    with open(input_file, "r", encoding="utf-8", newline="\n") as file:
        contents = file.read()

    review_draft_contents = add_date_to_rd(shortname, contents, today)

    file_extension = "wattsi" if shortname == "html" else "bs"
    review_draft_file = f"review-drafts/{path_month}.{file_extension}"
    with open(review_draft_file, "w", encoding="utf-8", newline="\n") as file:
        file.write(review_draft_contents)

    subprocess.run(["git", "add", input_file], stdout=subprocess.DEVNULL, check=True)
    subprocess.run(["git", "add", review_draft_file], stdout=subprocess.DEVNULL, check=True)
    subprocess.run(["git", "commit", "--amend", "--no-edit"], stdout=subprocess.DEVNULL, check=True)

    print(f"\nRegenerated Review Draft at {review_draft_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("shortnames", nargs="*", help="Optional spec shortnames to create. If omitted, will use this month's per db.json.")
    parser.add_argument("-f", "--force", action="store_true", help="bypass date checks")
    parser.add_argument("-p", "--pr", action="store_true", help="create pull requests in addition to branches")
    parser.add_argument("--regenerate", action="store_true", help="regenerate the review draft without creating a new branch")
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

    shortnames = args.shortnames
    if not shortnames:
        db = fetch_json("https://github.com/whatwg/sg/raw/main/db.json")
        shortnames = find_shortnames(db["workstreams"], today.month)

    if len(shortnames) == 0:
        print("Looks like there's nothing to be published this month.")
        exit(1)

    for shortname in shortnames:
        os.chdir(f"../{shortname}")
        if args.regenerate:
            regenerate_rd(shortname, today)
        else:
            branch_created = maybe_create_branch(shortname, today)
            if (branch_created and args.pr):
                create_pr(shortname, today)
        os.chdir("..")

if __name__ == "__main__":
    main()
