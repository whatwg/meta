#!/usr/bin/env python

import argparse, collections, json, re, urllib, urllib2

def get_labels(labels_resource):
    return json.loads(open(labels_resource, "r").read(), object_pairs_hook=collections.OrderedDict)

def remove_markdown_links(input):
    return re.sub(r"\[(.+)\]\(.+\)", r"\1", input)

def lint_labels(labels):
    for label in labels:
        if "name" not in label:
            print "A label needs a name"
        elif "description" not in label:
            print "A label (" + label["name"] + ") needs a description"
        elif len(remove_markdown_links(label["description"])) > 100:
            print "GitHub will likely complain about the length of your label (" + label["name"] + ")'s description."
        elif "color" not in label:
            print "A label (" + label["name"] + ") needs a color"
        elif "url_exclude_is_open" in label and label["url_exclude_is_open"] != True:
            print "A label (" + label["name"] + ")'s url_exclude_is_open needs to be set to true if present."

def clean_labels(labels_resource):
    labels = get_labels(labels_resource)
    lint_labels(labels)
    labels.sort(key=lambda x: x["name"])
    handle = open(labels_resource, "w")
    handle.write(json.dumps(labels, indent=2, separators=(',', ': ')))
    handle.write("\n")

def create_labels_docs(labels):
    output = """<!-- Please do not edit this file directly. It is generated by labels.py -->

# GitHub Labels

These are labels used by all [WHATWG standards](https://spec.whatwg.org/):

"""
    for label in labels:
        url = "https://github.com/search?q=org%3Awhatwg+label%3A%22" + urllib.quote_plus(label["name"]) + "%22"
        if not "url_exclude_is_open" in label:
            url += "+is%3Aopen"
        output += "* [" + label["name"] + "](" + url + "): " + label["description"]  + "\n"

    output += "\n"
    output += "Using the i18n-* labels results in digest email to [www-international](https://lists.w3.org/Archives/Public/www-international/).\n"

    handle = open("LABELS.md", "w")
    handle.write(output)

def fetch(token, url, method, body=None):
    request = urllib2.Request(url, body)
    request.get_method = lambda: method
    request.add_header("Authorization", b"Basic " + (token + ":x-oauth-basic").encode("base64").replace("\n", ""))
    request.add_header("Accept", b"application/vnd.github.symmetra-preview+json")
    return urllib2.urlopen(request)

def label_name_url(common_url, label_name):
    # Note: this uses quote() instead of quote_plus() as spaces need to become %20 here
    return common_url + "/" + urllib.quote(label_name)

def error(type, label_name, exc):
    print type + " label: " + label_name + "; error " + str(exc)

def delete_label(common_url, token, label_name):
    try:
        fetch(token, label_name_url(common_url, label_name), "DELETE")
    except urllib2.HTTPError as exc:
        if exc.code != 404:
            error("Deleting", label_name, exc)

def update_label(common_url, token, label):
    # Note: this reraises the error so the caller can branch.
    body = json.dumps(label)
    fetch(token, label_name_url(common_url, label["name"]), "PATCH", body)

def add_label(common_url, token, label):
    body = json.dumps(label)
    try:
        fetch(token, common_url, "POST", body)
    except Exception as exc:
        error("Adding", label_name, exc)

def adjust_repository_labels(organization, repository, token, labels_resource):
    common_url = "https://api.github.com/repos/%s/%s/labels" % (organization, repository)

    # Delete default GitHub labels except for "good first issue"
    for label_name in ("bug", "duplicate", "enhancement", "help wanted", "invalid", "question", "wontfix"):
        delete_label(common_url, token, label_name)

    # Update and add labels
    labels = get_labels(labels_resource)
    lint_labels(labels)
    for label in labels:
        label["description"] = remove_markdown_links(label["description"])
        if "url_exclude_is_open" in label:
            del label["url_exclude_is_open"]
        try:
            update_label(common_url, token, label)
        except urllib2.HTTPError as exc:
            if exc.code == 404:
                add_label(common_url, token, label)
            else:
                error("Updating", label_name, exc)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--repository")
    parser.add_argument("--all-whatwg-standards", action="store_true")
    parser.add_argument("--token")
    args = parser.parse_args()

    labels_resource = "labels.json"

    if args.update:
        clean_labels(labels_resource)
        create_labels_docs(get_labels(labels_resource))
    elif args.repository and "/" in args.repository and args.token:
        [organization, repository] = args.repository.split("/")
        adjust_repository_labels(organization, repository, args.token, labels_resource)
    elif args.all_whatwg_standards and args.token:
        # It would be slightly neater to instead pull the repositories from a JSON resource so this
        # script would remain WHATWG-agnostic, but we don't have a good JSON resource for this so
        # far.
        for repository in ("compat", "console", "dom", "encoding", "fetch", "fullscreen", "html",
                           "infra", "mimesniff", "notifications", "quirks", "storage", "streams",
                           "url", "xhr"):
            # Give a little bit of output as otherwise it's hard to tell what's going on
            print "About to process", repository
            adjust_repository_labels("whatwg", repository, args.token, labels_resource)
    else:
        print "Please invoke as one of:\n\n" + \
              "./labels.py --update\n" + \
              "./labels.py --repository <x/y> --token <token>\n" + \
              "./labels.py --all-whatwg-standards --token <token>"

main()
