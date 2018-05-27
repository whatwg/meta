#!/usr/bin/env python

import argparse, collections, json, urllib

def clean_labels(labels_resource, labels):
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    labels_resource = "labels.json"
    labels = json.loads(open(labels_resource, "r").read(), object_pairs_hook=collections.OrderedDict)

    if args.update:
        clean_labels(labels_resource, labels)
        create_labels_docs(labels)

main()
