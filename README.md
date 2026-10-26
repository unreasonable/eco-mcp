# Unreasonable Eco

![Unreasonable Eco](plugins/unreasonable-eco/assets/eco-logo-0.1.2.png)

Connect Claude, ChatGPT, Codex, and other MCP clients to your Unreasonable community. Find people and ventures, follow up on offers of help, prepare for your program, find people from your programs who share your personal interests, and draft fundraising introduction requests using your Eco account's permissions.

This repository contains the plugin configuration and five reusable Agent Skills. The MCP server is hosted by Unreasonable at **https://unreasonable.eco/mcp**; its application source and community data are not included here. An Eco account and authorization are required. Installing the public plugin does not grant access to private community data or staff tools.

## Install in Claude Code

Run these commands in your terminal:

```sh
claude plugin marketplace add unreasonable/eco-mcp
claude plugin install unreasonable-eco@unreasonable
```

Restart your session, open `/mcp`, and connect the Eco server through the browser authorization flow. The marketplace contains one plugin, `unreasonable-eco`. You can invoke a workflow explicitly, for example:

```text
/unreasonable-eco:find-people-who-share-your-interests
```

To test a local checkout without installing it:

```sh
git clone https://github.com/unreasonable/eco-mcp.git
claude --plugin-dir ./eco-mcp/plugins/unreasonable-eco
```

## Install in OpenAI clients

For supported Codex clients, add the repository marketplace:

```sh
codex plugin marketplace add unreasonable/eco-mcp
```

Open the plugin directory in your supported desktop client, choose the **Unreasonable** source, install **Unreasonable Eco**, and connect your Eco account. Marketplace support varies by client; this repository does not imply a public OpenAI Directory listing.

For ChatGPT plugin upload or submission, download the versioned ZIP from [GitHub Releases](https://github.com/unreasonable/eco-mcp/releases). It includes the portable OpenAI manifest, compatibility manifests, five skills, and all logo assets. Use the plugin upload flow available to your account. A custom MCP connection to `https://unreasonable.eco/mcp` provides the tools, but does not by itself install these bundled skills.

In a host with the skills loaded, invoke `$find-the-right-people`, `$follow-up-on-commitments`, `$prepare-for-your-program`, `$find-people-who-share-your-interests`, or `$request-fundraising-introductions`, or describe the task in plain language.

## Included workflows

- [Find the right people](plugins/unreasonable-eco/skills/find-the-right-people/SKILL.md): build a shortlist using profile evidence and explain each person's relevance.
- [Follow up on commitments](plugins/unreasonable-eco/skills/follow-up-on-commitments/SKILL.md): review offers made to you, prioritize follow-ups, and draft messages. Record changes only with your authorization.
- [Prepare for your program](plugins/unreasonable-eco/skills/prepare-for-your-program/SKILL.md): summarize program context, outstanding onboarding, schedule, and useful conversations.
- [Find people who share your interests](plugins/unreasonable-eco/skills/find-people-who-share-your-interests/SKILL.md): find people from your programs who share your personal interests, and rank closer locations higher.
- [Request fundraising introductions](plugins/unreasonable-eco/skills/request-fundraising-introductions/SKILL.md): assess Eco's funder recommendations and draft requests to the returned connectors. Record a request only after you confirm it was sent.

Try “Who in the community could help with water conservation?”, “Who from my programs shares my personal interests?”, or “Draft introduction requests for my current raise.” Available results depend on your account, program assignment, and fundraising access.

## Other agents and MCP clients

Start with [llms.txt](llms.txt), the portable [plugin manifest](plugins/unreasonable-eco/plugin.json), and the five `plugins/unreasonable-eco/skills/*/SKILL.md` files. Agent Skills use Markdown with YAML front matter and can be reused by compatible hosts. OpenAI-specific dependency and display metadata lives in each skill's `agents/openai.yaml`; Claude discovers the same skill instructions from `skills/`.

Connect using Streamable HTTP at `https://unreasonable.eco/mcp`. Use the host's supported OAuth flow and MCP discovery to retrieve the current tools and input schemas. Do not assume these files provide anonymous access, an API key, or a static tool catalog. This package has no local MCP executable and needs no Node or Python runtime to use.

## Data and actions

The plugin sends tool arguments, such as search terms, record IDs, and explicitly requested updates, to the hosted Eco MCP endpoint. Eco returns records visible to the authenticated account; those results are processed by the AI host you choose. OAuth credentials are managed by the host and are not bundled in this repository.

The plugin loads text instructions and connects to Eco. It installs no hooks, background jobs, package launchers, or hidden executable code. Maintainer validation and packaging scripts run only when invoked by a developer. Following returned website, deck, signing, or download links can contact those destinations; the workflows do not automatically fetch them.

Read-only discovery does not change records. Some Eco tools can update records when requested. The skills distinguish drafts, sent requests, follow-ups, and fulfilled commitments; generating an email draft does not send it. They do not automatically contact people, submit forms, sign agreements, or make payments. Staff tool access remains governed by Eco permissions.

## Support and policies

- [Support](https://unreasonable.eco/support)
- [Privacy policy](https://unreasonable.eco/privacy)
- [Terms of service](https://unreasonable.eco/terms)
- [Review walkthrough](https://urg.ai/mcp-review-walkthrough)
- Technical contact: tech@unreasonablegroup.com

## Directory submission

In the Claude submission Source step, select **plugins/unreasonable-eco** as the plugin folder and **main** as the branch (or a version tag). Re-validate after changing the folder or updating the commit. The repository root contains marketplace catalogs, maintainer tooling, and agent discovery documentation; it is not the installable plugin.

## Development and validation

See [compatibility and release checks](docs/compatibility.md). Keep the version, identity, and logo references synchronized across all three manifests. Inside the plugin folder, the portable `mcp.json` uses `streamable-http`; Claude's `.mcp.json` uses `http` for the same transport. Neither file should contain credentials.

```sh
python3 -m pip install PyYAML==6.0.3
python3 scripts/validate.py
claude plugin validate ./plugins/unreasonable-eco
python3 scripts/package.py /tmp/unreasonable-eco.zip
```

## License

The plugin files are [MIT licensed](LICENSE). This license does not grant rights to Unreasonable's trademarks, the hosted Eco service, or community data. Access to Eco remains subject to its terms and your account permissions.
