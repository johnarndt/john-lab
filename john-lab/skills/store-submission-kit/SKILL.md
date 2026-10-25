---
name: store-submission-kit
description: "Use when a user is submitting, resubmitting or answering a rejection for an iOS App Store or Google Play app. Triggers include 'get this app ready for the App Store', 'Apple rejected us', 'Guideline 2.1', 'they want a demo video', 'answer the reviewer', 'make App Store screenshots', 'upload to internal testing', or 'what's left before release'. Builds a per-app submission folder with a checklist, reviewer notes, device recordings, screenshots and draft replies, and tracks each app's status until release."
---

# Store submission kit

App review rejections are rarely about code. They are about missing evidence: a demo account, a recording on a real device, an answer to a specific question. This skill prepares that evidence before the reviewer asks, and answers precisely when they do.

## Per-app folder

```
submissions/<date>/<app>/
  CHECKLIST.md          # every item below, checked with proof
  review-notes.md       # what the reviewer needs: demo login, steps, hardware needs
  reply-drafts/         # one file per reviewer message, drafted for the owner
  recordings/           # screen recordings from a physical device
  screenshots/          # per required device size
  build-check.md        # version, build number, signing, entitlements, privacy manifest
STATUS.md               # one row per app: build, state, last reviewer message, next action
```

## Checklist

- **Build:** version and build numbers bumped; build uploaded and processed; correct build selected for review; signing and entitlements match the features used.
- **Privacy:** privacy policy URL live; data-collection answers match what the app actually sends; permission prompts explain why in plain words.
- **Review notes:** a working demo account (created for review, never the owner's own), exact steps to reach every feature, and what hardware or location a feature needs.
- **Recordings:** when a feature depends on hardware, sensors, purchases or account deletion, record it on a physical device and include it up front.
- **Store page:** screenshots at every required size, showing the real app; title, subtitle and description free of claims the app cannot back; age rating answered.
- **Release mode:** manual or automatic release after approval, chosen by the owner.
- **Android:** internal testing track first; data safety form; target SDK requirement met; upload key stored outside the repo.

## Answering a rejection

1. Quote the guideline and the reviewer's exact question.
2. Answer every part they asked, in their order, one paragraph each. If they ask for an example, give one concrete example per app.
3. Attach the recording or screenshots that prove it.
4. Fix the build if the rejection is right; say plainly what changed.
5. Draft the reply for the owner to send. Do not send it yourself.

## Rules

- The owner signs in to App Store Connect and Play Console, accepts agreements, and presses submit and release.
- Never put signing keys, store credentials or demo passwords in the repo or in chat; store them where the owner keeps secrets.
- Screenshots show the real app. No mocked features.
