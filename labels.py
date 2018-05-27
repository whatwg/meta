#!/usr/bin/env python

import argparse, collections, json, urllib, urllib2

def get_labels(labels_resource):
    return json.loads(open(labels_resource, "r").read(), object_pairs_hook=collections.OrderedDict)

def clean_labels(labels_resource):
    labels = get_labels(labels_resource)
    labels.sort(key=lambda x: x["name"])
    handle = open(labels_resource, "w")
    handle.write(json.dumps(labels, indent=2, separators=(',', ': ')))
    handle.write("\n")

def create_labels_docs(labels):
    output = """# GitHub Labels

There is currently no WHATWG-wide label policy, except for:

"""
    for label in labels:
        url = "https://github.com/search?q=org%3Awhatwg+label%3A%22" + urllib.quote_plus(label["name"])
        if not "url_exclude_is_open" in label:
            url += "+is%3Aopen"
        output += "* [" + label["name"] + "](" + url + "): " + label["description"]  + "\n"

    output += "\n"
    output += "Using the i18n-* labels results in digest email to [www-international](https://lists.w3.org/Archives/Public/www-international/).\n"

    handle = open("LABELS.md", "w")
    handle.write(output)

def fetch(url, method, token):
    request = urllib2.Request(url)
    request.get_method = lambda: method
    request.add_header("Authorization", b"Basic " + (token + ":x-oauth-basic").encode("base64").replace("\n", ""))
    return urllib2.urlopen(request)

def delete_label(organization, repository, label, token):
    try:
        fetch("https://api.github.com/repos/%s/%s/labels/%s" % (organization, repository, urllib.quote_plus(label)), "DELETE", token)
    except Exception as exc:
        print exc

def adjust_repository_labels(organization, repository, token):
    print organization, repository, token

    delete_label(organization, repository, "bug", token)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--repository")
    parser.add_argument("--token")
    args = parser.parse_args()

    labels_resource = "labels.json"

    if args.update:
        clean_labels(labels_resource)
        create_labels_docs(get_labels(labels_resource))
    elif args.repository and "/" in args.repository and args.token:
        [repository, organization] = args.repository.split("/")
        adjust_repository_labels(repository, organization, args.token)
    else:
        print "Please specify either `--update` or `--repository x/y --token token`"

main()
