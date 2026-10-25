---
name: feature-audit
description: "Use when a user wants to know whether their app actually works, end to end, before a launch or after a lot of AI-written changes. Triggers include 'audit my app', 'test every feature', 'is anything broken', 'QA this product', 'find the bugs before launch', 'feature audit', or 'make a test tracker'. Runs four phases with a CSV tracker: inventory every user story from the code, test each one, fix what failed, retest. Writes a dated ledger per phase and never fixes before the testing phase is done."
---

# Feature audit

"Is my app broken?" has no answer. "Does each of these 175 user stories pass?" does. This skill turns the first question into the second, in four phases, with a tracker that says exactly what was tested, what failed, what got fixed and what is still blocked.

## Tracker

`qa/FEATURE_TRACKER.csv` in the repo:

```
ID,Area,Priority,Feature,Role,User Story,Expected Behaviour,Code Ref,Test How,P1_Documented,P2_Test_Result,P3_Fix,P4_Retest,Notes
```

| Column | Values |
|---|---|
| Priority | P0 (money, auth, data loss), P1 (core flow), P2 (everything else) |
| P2_Test_Result | `PASS`, `PARTIAL`, `FAIL`, `BLOCKED-ENV` + a dated note |
| P3_Fix | `FIXED`, `NO-FIX-NEEDED`, `DEFERRED-ENV`, `DEFERRED-OWNER`, `WONTFIX` + commit |
| P4_Retest | `PASS`, `BLOCKED-ENV`, `N/A` |

Each phase also writes `qa/P<n>_<NAME>_<date>.md`: inventory, errors, fixes, retest.

## Phases

**P1 · Inventory.** Read the code, not the marketing. Routes, API handlers, background jobs, emails, webhooks, admin screens, settings, billing states, permission checks. One row per user story: "As a <role>, I can <action> so that <outcome>", with the expected behavior, the file it lives in, and how to test it. Include the unhappy paths: wrong password, expired link, card declined, another tenant's ID in the URL.

**P2 · Test.** Run each story through the real interface or API on a local or staging build and record the result with evidence. No code changes in this phase, even for obvious bugs. Write them down. A `PARTIAL` says what part failed.

**P3 · Fix.** Fix the `FAIL` and `PARTIAL` rows in priority order, one commit per fix or per tight group, each referenced in the tracker. Anything that needs the owner (a dashboard setting, a decision, a real payment) is `DEFERRED-OWNER` and goes on the owner's action list.

**P4 · Retest.** Rerun every fixed row and every row that shares code with a fix. Update the tracker. Summarize: total stories, first-pass passes, fixed, deferred, blocked.

## Safety rules

- Before P2, the existing test suite must pass. Record the baseline.
- No real sends to customers or prospects. No live payments; use the payment provider's test mode. No production feature-flag flips. Cap any paid third-party API calls and state the cap.
- One audit per repo at a time. Two sessions editing the same repo will collide.
- Commit fixes as you go. Uncommitted fixes get lost between sessions.

## Rules learned the hard way

- **Deployed is not proven.** After fixes ship, check the live site's behavior and its deployed commit. Notes that say "deployed" have been wrong for weeks at a time because the live site was serving a different branch.
- **Cross-tenant checks are P0.** Swap one account's IDs into another account's requests for every read and write endpoint. These are the bugs that matter most and the ones people skip.
- **After any credential rotation, retest login, database and webhooks.** A rotated secret that never reached the app fails silently.
