---
name: recover-document-job
description: Recover an interrupted document-processing job from saved state and distinguish a replay from new processing, duplicate work, or an unresolved outcome.
---

# Recover a document job

Use this when a document extraction or conversion appears interrupted and a prior request may already exist. Do not restart a job merely because its client timed out.

## Establish the identity

Collect the service, existing job or request identifier, source identity, intended schema or conversion settings, and the last observed status. Use a source hash or service-held attachment identity when available; a filename alone may be ambiguous. Keep secrets and source-document contents out of operational logs.

Separate a job ID, historical provider request ID, and client idempotency key. They serve different purposes. Use the service's documented key and replay behavior; do not manufacture a replacement key or infer retry safety from a successful HTTP response.

## Inspect before retrying

Prefer status and result reads through available authorized tools. Classify the existing request as completed, running, failed, absent, or unknown. If completed, retrieve its saved result. If running, follow the documented status mechanism. If absent or failed, determine whether an authorized retry can reuse the original identity. A missing read permission or unavailable status endpoint leaves the outcome unknown.

Replaying an existing completed request is appropriate only when the service documents it as retrieval without a new operation. If replay may start new processing, consume credits, or duplicate a write, require authorization for that action unless already granted. A new source, schema, or processing configuration is a new request unless the service explicitly supports updating the existing one.

## Verify the recovered result

Match source identity and schema/settings to the intended job. Record returned extraction/job identity and replay markers. Check required fields and validation warnings, and compare material extracted values to the original source when accessible. A valid schema or confidence score alone does not establish correctness. If the source is unavailable, say the result was recovered but source review is pending.

Treat saved credits, model names, processing duration, and historical request IDs as metadata about the prior execution. To establish a new debit or fresh provider work, use current transaction or execution evidence. Without it, classify new spending as unknown; never infer a new charge from a saved credits-used field.

## Return a recovery receipt

Include the existing job identity, observed status, identity match, recovered artifact location, validation/source-review findings, whether the response is a saved replay or fresh execution, and the evidence for any debit classification. Record unknowns next to their consequences. Give the next safe action for unresolved cases.

Stop when the saved result is recovered and checked, or when an access/identity/side-effect uncertainty prevents a safe continuation. Do not loop through retries with new keys. Recovery does not authorize emailing, posting, purchasing, or approving the extracted data.
