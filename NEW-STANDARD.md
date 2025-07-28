# New Standard Checklist

When adding a new WHATWG standard, here is a checklist that needs to be considered. When coordination is required with the SG or an administrator of the WHATWG GitHub, the step is prefixed with SG/admin.

1. Identify a shortname that is used for the spec.whatwg.org subdomain and repository (for tooling it is important that these are named identically).
   1. SG/admin: ensure the subdomain works and is configured:
      1. Update and deploy https://github.com/whatwg/misc-server.
      1. Configure the new A record on the DigitalOcean control panel. 
   1. SG/admin: ensure there is a repository under the whatwg GitHub organization.
      1. Give PR Preview access to the new repository (through organization settings).
      1. Run [`labels.py`](./labels.py) with appropriate `--repository` and `--token` parameters to create appropriate labels for the new repository.
      1. Fill in "Edit repository details" on the frontpage of the repository (button next to About).
      1. Add branch protection for the default branch.
      1. Add the editors to the repository with Role: Write.
      1. Add @whatbot to the repository with Role: Write so it can perform participant agreement checks.
      1. Add the @whatwg/triage team to the repository with Role: Triage.
      1. Add the @whatwg/editors-all-specs team to the repository with Role: Write.
      1. Configure a [participate webhook](https://github.com/whatwg/participate.whatwg.org?tab=readme-ov-file#setting-up-the-github-webhook).
      1. Disable "Wikis", "Discussions", and "Allow merge commits". Enable "Automatically delete head branches".
1. Create an SVG logo in the right shade of green (i.e., WHATWG green) and add it to https://github.com/whatwg/whatwg.org/tree/main/resources.whatwg.org.
1. SG/admin: create a Twitter account.
   1. SG/admin: use https://github.com/whatwg/whattweetbot-keys to get the relevant keys.
1. Add the standard to https://github.com/whatwg/sg/blob/main/db.json and ensure the relevant details are filled in. (In case a new Workstream is needed an issue will have to be filed with the SG first for review.)
1. SG/admin: run https://github.com/whatwg/spec-factory.
1. SG/admin: set up the participation check
   1. Follow the steps [documented in the participate.whatwg.org repo](https://github.com/whatwg/participate.whatwg.org/blob/main/README.md#setting-up-the-github-webhook)
   1. Use the DigitalOcean control panel to redeploy the participate app (so that it picks up the new `db.json`).
   1. If you need to manually re-trigger any participation checks, use `https://github.com/whatwg/<spec-name>/settings/hooks` to redeliver the `pull_request.opened` hook.

You should be all set. When in doubt reach out to the Steering Group.
