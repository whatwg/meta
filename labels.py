import json, urllib

labels = json.loads(open("labels.json", "r").read())

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
