# Compatibility and release checks

## Package layout

The installable plugin folder is `plugins/unreasonable-eco`. Repository scripts, CI, marketplace catalogs, and agent discovery documents stay outside that folder. Claude reads `.claude-plugin/plugin.json`, `.mcp.json`, and `skills/`. OpenAI reads portable `plugin.json`, `mcp.json`, and the same `skills/`; `.codex-plugin/plugin.json` remains available for compatible older clients. Each host also has its own repository marketplace catalog. Both catalogs point to that plugin folder, so the skills have one source of truth.

The skill instructions refer to tool names without a host-specific prefix. Hosts may namespace MCP tools differently. Resolve the named operation from the connected Eco server's current tool list and follow its actual input schema.

## Automated checks

`scripts/validate.py` checks JSON parsing, shared identity and versions, MCP transports and endpoint agreement, local paths, four skill front matters and dependency metadata, marketplace sources, README length, license, prohibited system files, and portable filename/size limits. GitHub Actions runs it for pushes and pull requests. This is a focused package validator, not a replacement for either vendor's portal review.

Run `claude plugin validate ./plugins/unreasonable-eco` with an up-to-date Claude Code before release. Claude Code versions older than 2.1.281 may warn about directory listing fields such as `icon` and policy URLs; these fields are intentional. Do not delete them just to silence an older validator.

## Authenticated smoke tests before directory submission

These checks require a dedicated authorized test account and have not been automated in this repository:

1. Install from the repository marketplace in Claude Code and a supported OpenAI client. Confirm all four skills load and OAuth connects to the intended Eco account.
2. Find a known visible person, then search by expertise. Check that the shortlist cites actual profiles and does not invent missing contact details.
3. Review received commitments without a mutation. Draft a follow-up; verify that drafting does not change its status. Explicitly authorize an update on a sample commitment and verify the result.
4. Prepare for an assigned sample program. Check dates, time zones, onboarding state, and links. Test an account with no assigned program.
5. Retrieve a sample fundraising round and draft an introduction. Check the chosen connector and recommendation-specific deck link. Confirm no email is sent and no request is recorded just by drafting.
6. Test an inaccessible profile and a staff-only operation from a non-staff account. Confirm the workflows respect the denial.
7. Check support, privacy, and terms pages are publicly accessible when submitting. Provide reviewer access through the vendor's secure submission form, never through this repository.

GitHub publication makes the source and repository marketplaces public. It does not automatically list the plugin in the Claude or OpenAI public directories, complete their validation, or resolve findings about the hosted MCP server's tools.

## Release

Update the version in all manifests and the Claude marketplace entry. Run validation, package with `python3 scripts/package.py /tmp/unreasonable-eco-VERSION.zip`, and attach that ZIP to a versioned GitHub release. The archive includes only the installable plugin, its user README, license, and assets. It excludes repository discovery docs, marketplace catalogs, Git metadata, CI configuration, and maintainer scripts. Do not commit ZIPs into the plugin folder: Claude's directory scanner holds binary archives for review.

## Official references

- [Claude plugin pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist)
- [Claude plugin manifest](https://code.claude.com/docs/en/plugins-reference)
- [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins)
- [OpenAI skills](https://developers.openai.com/plugins/build/skills)

## Claude asset-reference holds

Version 0.1.8 placed maintenance scripts and discovery documentation inside the plugin folder. Claude's scanner followed their references to manifests and a README containing logo paths, producing six `UNREAD_ASSET_REFERENCED` holds. Version 0.1.9 moves the installable plugin to `plugins/unreasonable-eco`; maintenance scripts and repository discovery docs remain outside it. The plugin itself contains only manifests, MCP configuration, four skills, logo assets, a license, and a user README. No plugin command, hook, script, or setting executes an image. Logo references in manifest listing fields and Markdown images remain intentional.

Select `plugins/unreasonable-eco` as the plugin folder in the Claude portal before re-validating. Local validation does not run Claude's directory policy scanner, so only a fresh portal result can confirm the holds are gone. Listing metadata warnings explicitly marked “No action needed” can remain.
