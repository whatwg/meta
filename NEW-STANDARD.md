# New Standard Checklist

When adding a new WHATWG standard, here is a checklist that needs to be considered. When coordination is required with the SG or an administrator of the WHATWG GitHub, the step is prefixed with SG/admin.

1. Identify a shortname that is used for the spec.whatwg.org subdomain and repository (for tooling it is important that these are named identically).
   1. SG/admin: ensure the subdomain works and is configured: https://github.com/whatwg/misc-server.
   1. SG/admin: ensure there is a repository under the whatwg GitHub organization.
      1. Give PR Preview access to the new repository.
      1. Ensure @whatbot has write access to the repository so it can perform participant agreement checks.
      1. Run [`labels.py`](./labels.py) with appropriate `--repository` and `--token` parameters to create appropriate labels for the new repository.
      1. Fill in "Edit repository details" on the frontpage of the repository (button next to About).
      1. Add branch protection for the default branch.
      1. Ensure editors have write access.
      1. Disable "Wikis" and "Allow merge commits". Enable "Automatically delete head branches".
1. Create an SVG logo in the right shade of green (i.e., WHATWG green) and add it to https://github.com/whatwg/whatwg.org/tree/main/resources.whatwg.org.
1. SG/admin: create a Twitter account.
   1. SG/admin: use https://github.com/whatwg/whattweetbot-keys to get the relevant keys.
1. Add the standard to https://github.com/whatwg/sg/blob/main/db.json and ensure the relevant details are filled in. (In case a new Workstream is needed an issue will have to be filed with the SG first for review.)
1. SG/admin: run https://github.com/whatwg/spec-factory.

You should be all set. When in doubt reach out to the Steering Group.
