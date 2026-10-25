# John Lab

Ten Claude skills taken from the workflows I use to build, ship and market my own products. Each one is a plain `SKILL.md` you can read before installing. Each has an article on [johnarndt.net/skills](https://johnarndt.net/skills) about where it came from.

## Install

In Claude Code:

```
/plugin marketplace add johnarndt/john-lab
/plugin install john-lab@john-lab
```

To use a single skill, copy its folder into `~/.claude/skills/` (personal) or `.claude/skills/` in a repository. In the Claude apps, download a skill's ZIP from [johnarndt.net/skills](https://johnarndt.net/skills) and upload it under Customize → Skills.

## Skills

| Skill | What it does | Article |
|---|---|---|
| [`feature-audit`](john-lab/skills/feature-audit/SKILL.md) | Inventory every user story, test each, fix, retest, all tracked in one CSV. No fixing before testing. | [Read](https://johnarndt.net/skills/feature-audit) |
| [`lane-orchestrator`](john-lab/skills/lane-orchestrator/SKILL.md) | One planner, parallel builders in their own worktrees, reviewers who didn't write the code, and a spending rule. | [Read](https://johnarndt.net/skills/lane-orchestrator) |
| [`safe-cutover`](john-lab/skills/safe-cutover/SKILL.md) | Snapshot DNS, prove parity, cut over behind a health gate with automatic rollback, keep the old host warm. | [Read](https://johnarndt.net/skills/safe-cutover) |
| [`cve-triage`](john-lab/skills/cve-triage/SKILL.md) | Sort advisories into exploitable, mitigated and noise by how the code really uses each package, then patch in batches. | [Read](https://johnarndt.net/skills/cve-triage) |
| [`store-submission-kit`](john-lab/skills/store-submission-kit/SKILL.md) | A per-app folder with reviewer notes, device recordings and precise rejection replies for the App Store and Google Play. | [Read](https://johnarndt.net/skills/store-submission-kit) |
| [`verify-release-readiness`](john-lab/skills/verify-release-readiness/SKILL.md) | Connect the intended source, current live state, required gates, deployed components, and observed behavior in a dated release report. | [Read](https://johnarndt.net/skills/verify-release-readiness) |
| [`recover-document-job`](john-lab/skills/recover-document-job/SKILL.md) | Retrieve the existing result before retrying, then separate replay evidence, source checks, and present spending. | [Read](https://johnarndt.net/skills/recover-document-job) |
| [`writers-room`](john-lab/skills/writers-room/SKILL.md) | A scout, critics, a showrunner, a copywriter and a blind persona panel turn sources into a teleprompter script. | [Read](https://johnarndt.net/skills/writers-room) |
| [`podcast-room`](john-lab/skills/podcast-room/SKILL.md) | Pitchers, a showrunner with a facts ledger, one segment at a time, and a transcript diff on every recording. | [Read](https://johnarndt.net/skills/podcast-room) |
| [`hundred-to-ten`](john-lab/skills/hundred-to-ten/SKILL.md) | Write 100, score them on a rubric, cut 20% a round through a new lens each time, and keep the best 10. | [Read](https://johnarndt.net/skills/hundred-to-ten) |

## Status

Version 0.1.0. These are drafts. The workflows behind them have been run on real products, but the packaged skills are new. Try each one on a small task you can check before relying on it, and please open an issue when one triggers at the wrong time or gets something wrong.

## What these skills do and don't do

- Every skill is instructions only: no hooks, scripts, MCP servers or network calls of their own. They use whatever tools your Claude session already has.
- They don't grant permissions. Skills that touch releases, DNS, app stores or payments stop at a report or draft and leave sign-ins, payments, sends and deploys to you.
- No credentials belong in any skill, and none are included.

## Related

Business-operations skills (feedback inbox, signup alerts, claim audit and more) live in the Soxoa Ops plugin at [johnarndt/soxoa-claude-plugins](https://github.com/johnarndt/soxoa-claude-plugins).

## License

MIT. See [LICENSE](LICENSE).
