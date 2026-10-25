---
name: verify-release-readiness
description: Review candidate and live release evidence to produce a dated readiness report or deployment receipt, including source identity, required gates, and unresolved proof gaps.
---

# Verify release readiness

Produce read-only evidence of whether a candidate meets the project's release requirements, or whether an already completed rollout serves the intended source and behavior. This skill does not deploy, migrate, rotate secrets, change feature flags, create paid work, or authorize those actions.

## Establish the release contract

Use the project's current instructions, candidate commit or artifact identity, release target, live health or version endpoints, required checks, and supplied deployment receipts. Determine whether this is pre-release readiness or post-release verification. Record the observation time and environment. Never treat a historical runbook's source floor, runtime version, rollback identifier, or command as current without checking it.

Confirm the repository and remote context through available read-only tools. For a candidate release, verify the live source and required release branch are included in the candidate's history when the project's policy requires it. Record dirty files or an unverifiable build identity. A successful test run from a different source cannot establish readiness for the intended artifact.

## Inspect evidence proportionally

- Map required checks to their actual result, source identity, time, and scope. Distinguish focused checks, full suites, skipped cases, pre-existing failures, and missing results. Do not call a suite passing when a known failure is merely considered unrelated.
- For multiple deployed components, verify the project's compatibility rule. Where app and compute must match, compare exact source identities and health for both. Do not impose same-commit deployment on systems whose declared design allows independent releases.
- If data changes are included, compare the candidate migration inventory with the current ledger evidence and identify additions, collisions, partial state, and restore/recovery provisions. Inspect only authorized metadata; do not apply migrations.
- Where in-flight work matters, use authorized aggregate status or supplied evidence to assess the required quiet window. Missing access leaves this gate unverified; it does not imply zero work.
- Compare allowed runtime, configuration and binding metadata before and after when available. Do not retrieve secret values merely to compare metadata. Binding names and types cannot prove that remote secret bytes are identical or that the application used them.
- Check the public behavior relevant to the change. Use safe read-only paths or existing synthetic evidence. A healthy status endpoint does not establish a complete payment, fulfillment or customer workflow. Do not start charges, email, provider inference, or other effects solely to strengthen a receipt.

For an already completed release, verify intended source identities at the actual endpoints, record the observed deployment and runtime metadata, inspect relevant public behavior, and state what is supported by observation versus a provider acknowledgment or saved receipt.

## Deliverable and stopping condition

Return a concise verdict, candidate/live identities, observation time, checks table, preserved-configuration evidence, unresolved gates, and next required action. Link to sanitized evidence where possible. Separate readiness from authorization and observed rollout from untested business outcomes.

Stop when all applicable gates have dispositions or required evidence is inaccessible. Request the specific missing evidence rather than inferring success. If live state changes during the review, mark the earlier observations stale and reread the affected gates; do not repeatedly poll unchanged state or mutate production to resolve ambiguity.

Package status: this Claude skill draft has not been behaviorally tested in Claude. Historical release-verification methods informed it; this package carries no production deployment authority.
