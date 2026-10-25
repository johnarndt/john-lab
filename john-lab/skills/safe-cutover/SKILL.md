---
name: safe-cutover
description: "Use when a user wants to move a live site or app to a new host, change its DNS, or ship a risky release without downtime. Triggers include 'migrate from Vercel to Cloudflare', 'move my site to a new host', 'switch DNS', 'cut over to the new server', 'deploy this safely', 'can we roll back if it breaks', or 'make the deploy refuse a dirty tree'. Snapshots DNS and config first, proves parity on staging, cuts over with a scripted health gate and automatic rollback, and keeps the old host warm until the owner retires it."
---

# Safe cutover

Most outages during a migration come from one of three things: a record nobody snapshotted, a secret that did not come across, or a scheduled job that runs in two places or in none. This skill makes each of those a checked step.

## Phases

**P0 · Stabilize.** The current host must be healthy before you move anything. Fix it there first.

**P1 · Build for the new host** on its own branch. Do not change behavior; this is a platform move.

**P2 · Prove parity on staging.** A script requests every important URL on both live and staging and compares status codes, redirects, page titles, canonical links and structured data. The target is zero differences. Also confirm sessions issued by the old host still work on the new one, so nobody is logged out.

**P3 · Cut over**, scripted, in this order:

1. Snapshot DNS: every record in the zone, plus routes and scheduled jobs on both hosts, to a timestamped JSON file with owner-only permissions. Never overwrite a snapshot.
2. Preflight, and refuse to continue unless every check passes:
   - the live commit is contained in the branch being deployed (re-merge it right before cutover; live may have moved today);
   - every required secret resolves on the new host;
   - a signed webhook test returns 200 and a bad signature returns 400;
   - the parity check shows zero differences.
3. Disable scheduled jobs on the old host.
4. Point DNS at the new host. Leave mail records (MX, SPF, DKIM, DMARC) untouched.
5. Poll the health endpoint until it reports the new platform at the expected commit. If it does not within the timeout, restore the snapshot automatically.
6. Enable scheduled jobs on the new host, then confirm each one actually fires.
7. Freeze builds on the old host. Take a second snapshot.

**P4 · Decommission**, only with the owner's approval, after a waiting period (default 7 days).

## Guarded release (for every deploy afterwards)

The deploy command refuses a dirty working tree, a commit other than HEAD, or a commit that does not contain the recorded live commit. After deploying it checks the version endpoint and build header for the new commit, then rechecks every sitemap URL for a 200. Record the result in `RELEASE_STATE.md`.

## Rules learned the hard way

- **Scheduled jobs are the silent failure.** After one cutover the new host's cron never fired. Add a freshness check that alerts when a job has not run on time, and keep the old host's jobs available to switch back on.
- **Some secrets cannot be read back** from the old host. Plan a deliberate rotation, or a temporary bridge that accepts both old and new sessions, before cutover day.
- **Caches may ignore the hostname.** Add an explicit www-to-apex (or reverse) redirect rule rather than trusting the cache.
- **Owner does the dashboard clicks; the agent runs the commands and the checks.** DNS changes on a production zone get the owner's go-ahead each time.
