---
name: product-workspace-playbook
description: Apply a product workspace's standing rules when choosing feedback-driven work, running paid product tests, preparing public writing, or shipping a change. Use when an owner wants an agent to carry a product task from intake through verification while respecting local spending and release rules.
---

# Product Workspace Playbook

Read the current workspace instructions and the affected repository's guidance. Identify the product, what the owner asked you to do, and which of the steps below apply. Use current local policy and live evidence for environment-specific decisions. This playbook grants no authorization to spend, deploy, publish, or contact anyone.

## Use customer feedback to choose work

- When asked what to work on, read the feedback inbox's portfolio-wide open list, then the relevant product's open list and issue records. Before changing a product or its UX, check its issue records for related reports. Distinguish repeated requests from individual reports and use them to inform the owner's decision.
- Treat feedback as evidence. Start implementation when the owner selects the issue or the requested work clearly covers it. Log newly supplied feedback through the workspace's intake mechanism, retaining the speaker's words verbatim and their attribution.
- After fixing a tracked issue, add a fix note to its source issue with the branch and commit. Mark it planned while awaiting release. Mark it shipped with the verified live commit after checking production. Preserve original quotes and let the inbox regenerate its own indexes.

## Check spending before choosing tools

- Identify the purpose of each paid call and confirm the workspace authorizes that use. Permission to run product inference or test actual product results covers those calls. Coding, code review, development planning, and strategy require their own permitted route. Apply the same boundary to delegated agents and external CLIs.
- If development is restricted to subscription access and that access runs out, preserve the work and report the limit. Obtain separate authorization for any credit purchase or top-up.
- For accuracy-sensitive product tests, define the scope, source evidence and acceptance measures before comparing workflows. Prefer the model or workflow that materially improves accuracy or overall efficiency within the authorized budget. Preserve earlier benchmark results and report omissions, false positives, unresolved scope, conflicts, reproducibility, observed latency, and cost.
- For a plan takeoff, read the complete plan and check every relevant trade and quantity against source pages. Report symbol-level results at their measured scope. If the project sets a whole-job target, calculate it across the declared scope. Report automated delivery cost separately from development and human review.

## Use the right publishing guides

For LinkedIn strategy, profile edits, drafts, calendars, engagement, or performance reviews, read the workspace's standing guide for the relevant personal or product account. For personal writing, also read the owner's voice guide and prompt when provided. Apply current instructions to the requested deliverable and keep draft preparation within the authorized scope.

## Verify releases against production

1. Start from the project's designated base branch and fetch the remote. Read the current live source identity from health, version metadata, or authoritative deployment evidence. Confirm the candidate contains both the required base and the actual live source, including security fixes. For Git, use `git merge-base --is-ancestor "$live_sha" HEAD` with the verified live SHA.
2. Run the project's required quality gates. Check the live migration ledger when changing schema, preserve configuration and secret bindings, and follow documented requirements for coordinated components, idle-state checks, and operator-only steps. Use binding metadata and avoid exposing secret values.
3. Confirm authorization for the actual release and any applicable notice or rollout prerequisites. Recheck live source and other change-sensitive gates immediately before deployment. If another release landed, integrate it and rerun affected checks before proceeding.
4. Verify the intended version, runtime, component identities, and affected behavior in production. Record the deployed source, gate results, and unresolved checks in the release record. When work stops at preparation or review, report the candidate and the checks still needed. Update the source feedback issue only with the status the evidence supports.
