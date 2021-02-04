When adding a new WHATWG standard, these are the things that need to be done:

1. Identify a shortname that is used for the spec.whatwg.org subdomain and repository (for tooling it is important that these are named identically).
   1. Ensure the subdomain works and is configured: https://github.com/whatwg/misc-server.
   1. Ensure there is repository.
1. Create a logo and add it to https://github.com/whatwg/whatwg.org/tree/main/resources.whatwg.org.
1. Create a Twitter account.
   1. Use https://github.com/whatwg/whattweetbot-keys to get the relevant keys. (The Steering Group will help with this.)
1. Add it to https://github.com/whatwg/sg/blob/main/db.json and ensure the relevant details are filled in. (In case there's a new Workstream more updates will be needed.)
1. Run https://github.com/whatwg/spec-factory.
1. Run `labels.py`.
1. You should be all set. When in doubt reach out to the Steering Group.
