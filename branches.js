'use strict';

const Ajv = require('ajv');
const Octokit = require('@octokit/rest');

async function main() {
    if (!process.env.GITHUB_TOKEN) {
        throw new Error('GITHUB_TOKEN environment variable must be set');
    }

    const ajv = new Ajv();

    function enabledObject(shouldBeEnabled) {
        return {
            type: 'object',
            properties: {
                enabled: {
                    const: shouldBeEnabled
                }
            },
            required: ['enabled']
        }
    }

    const validate = ajv.compile({
        type: 'object',
        properties: {
            required_pull_request_reviews: {
                type: 'object',
                properties: {
                    required_approving_review_count: {
                        type: 'integer',
                        minimum: 1
                    }
                },
                required: ['required_approving_review_count']
            },
            required_linear_history: enabledObject(true),
            enforce_admins: enabledObject(true),
            allow_force_pushes: enabledObject(false),
            allow_deletions: enabledObject(false),
        },
        required: [
            'required_pull_request_reviews',
            'required_linear_history',
            'enforce_admins',
            'allow_force_pushes',
            'allow_deletions',
        ]
    });

    const octokit = new Octokit({
        auth: process.env.GITHUB_TOKEN,
        previews: ['luke-cage'],
    });

    const repos = (await octokit.repos.listForOrg({
        org: 'whatwg',
        per_page: 100,
    })).data.filter((r) => !r.archived && !r.private);
    repos.sort((r1, r2) => r1.name.localeCompare(r2.name));

    for (const repo of repos) {
        const options = {
            owner: 'whatwg',
            repo: repo.name,
            branch: repo.default_branch,
        };
        let rule;
        try {
            rule = (await octokit.repos.getBranchProtection(options)).data;
        } catch {
            rule = null;
        }

        const valid = validate(rule);
        if (valid) {
            console.log(repo.name, 'OK')
        } else {
            console.log(repo.name, 'FAIL');
            for (const error of validate.errors) {
                console.error(`\trule${error.dataPath}: ${error.message}`);
            }
        }
    }
}

main().catch((reason) => {
    console.error(reason);
    process.exit(1);
});
