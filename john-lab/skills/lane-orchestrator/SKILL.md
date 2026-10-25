---
name: lane-orchestrator
description: "Use when a user wants several AI coding agents to build one hard change in parallel without stepping on each other. Triggers include 'have a reviewer plan it and agents build it', 'split this across agents', 'use a planner model and builder models', 'spin up parallel lanes', 'get an independent review before merging', or 'coordinate multiple Claude sessions on this repo'. Sets up a strategy review first, file-owned lanes in separate worktrees, append-only status logs, frozen contracts, independent reviewers with reproductions, and an explicit spending rule."
---

# Lane orchestrator

Parallel agents go fast and break things in parallel. This skill is the coordination layer: one planner, a few builders with clear ownership, reviewers who did not write the code, and a root that decides. Everything is a file, so any session can resume after a limit or a crash.

## Roles

- **Strategy reviewer** (the strongest model available): reads the goal and the code, then writes the plan. It does not write production code.
- **Lanes** (builder models): each owns a set of files and a written deliverable.
- **Independent reviewers:** fresh sessions that never saw the lane's reasoning. They get the code and the acceptance criteria, and they write reproductions, not opinions.
- **Root** (you, or the coordinating session): assigns ownership, accepts or overrides the reviewer, integrates and decides on release. Only root merges or deploys.

## Workspace

```
coord/
  plan.md                  # strategy review output
  coordinator-notes.md     # root's timestamped decisions, append-only
  contracts/               # shared interfaces, versioned: contracts.v1.ts, contracts.v2.ts
  acceptance.v1.md         # what "done" means, frozen by hash
  lanes/<lane>-status.md   # each lane's append-only log
  reviews/<lane>-<sha>/review.json + repro scripts
  decisions/<date>-<topic>.json
```

Review JSON: `{ "verdict": "accept|blockers", "findings": [...], "positiveEvidence": [...], "acceptanceLimits": [...], "reviewedSha": "..." }`.

## Flow

1. **Strategy review.** The reviewer writes `plan.md`: architecture, lanes, file ownership per lane, the shared contract to freeze first, and the acceptance criteria.
2. **Freeze the contract.** One lane writes the shared types or interfaces within the first short block of work. Root freezes it. Later changes publish `v2` alongside `v1`; nothing is rewritten in place.
3. **Freeze acceptance.** Record a hash of the acceptance file. Later additions are addenda that may tighten but never relax it.
4. **Run lanes.** Each lane gets its own git worktree and branch, starting from the same commit. It edits only its owned files, logs progress and published interfaces to its status file, commits, and stops at its deliverable.
5. **Independent review.** For each finished lane, a reviewer at the frozen SHA writes findings with reproduction scripts. Blockers go back to the lane as a narrow follow-up with the repro attached.
6. **Integrate.** Root merges accepted lanes into an integration worktree, runs the full suite and the acceptance checks, and records a decision file.
7. **Release** only from a clean integration commit, by root, after the owner approves.

## Spending rule

Write it in `plan.md` and in every lane prompt: which accounts pay for development and which pay for product test runs. A sensible default is to build and review on the subscription, and to spend API credits only on runs of the product itself, capped per run and frozen to a code hash. If a lane hits a usage limit, it stops and preserves its work. It never switches to a paid route to keep going.

## Rules learned the hard way

- **Mocks lie.** Tests that mock the data layer passed while the real path read the wrong field. Reviewers must exercise at least one real path per lane.
- **Shared worktrees collide.** File ownership alone is not enough isolation; give each lane its own worktree.
- **Interrupt with evidence, not new scope.** When root interrupts a lane, the message says what was found and that the original objective stands.
- **The reviewer can be wrong.** Root may override the strategy reviewer and records why. Reject any shortcut that would hide failures, such as skipping work because something looks present.
- **Check the layer.** If repeated fixes do not move the result, ask the reviewer whether the failure lives in a different layer than the one being fixed.
