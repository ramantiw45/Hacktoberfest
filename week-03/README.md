# Week 3 — Slow and Steady (Oct 19 → Oct 25, 11:59pm PDT)

**Submission status: DRAFTED — DEV draft id 4911464, not yet published.** Post
draft is `draft.md`; the staged article is
<https://dev.to/ramantiw45/sloth-ledger-the-model-has-an-opinion-the-ledger-has-the-numbers-36nf-temp-slug-9697672/edit>.
It publishes only on an explicit yes.

Deadline in IST: **Sun Oct 25, 12:29 PM** (`2026-10-25T06:59:00Z`).

## What was built

**Sloth Ledger** — describe a chore in plain English; an open-weight model
decides whether to automate it, hand it to a human, or ignore it forever. When
an automation actually runs, the reclaimed minutes are booked into a Tiger Cloud
hypertable, and the dashboard answers one question with evidence: *how much time
did this actually save me?*

- **Code lives outside this folder**, by design:
  `C:\Users\Raman Tiwari\MyDevelopments\SlothLedger`, public at
  <https://github.com/ramantiw45/SlothLedger> (`main`, MIT).
- **Prize target:** Best Use of Tiger Data ($100 partner category) — hypertable
  for reclaimed minutes, continuous aggregate for the panel that reads them,
  compression policy, and a least-privilege `sloth_app` role.
- Tags planned: `devchallenge`, `hf26challenge`, `tigerdata`, `opensource`.

## Why this qualifies for the theme

Slow and Steady is about rewarding laziness. Most entries automate a chore.
Sloth Ledger automates the chore **and then does the accounting**, including the
chores it refused to automate. The "still on you" line is allowed to grow, which
is the opposite of a productivity dashboard.

## Open source AI at the core

| Layer | What | Openness |
|---|---|---|
| Judgement (demo) | `qwen/qwen3.8-27b` via Groq's OpenAI-compatible API | open weights |
| Judgement (floor) | deterministic rules in `sloth/model.py` | no key, no network |
| Judgement (swap) | any OpenAI-compatible endpoint, including a local server | one env var |
| Store (demo) | Tiger Cloud / TimescaleDB | hypertable + CAGG |
| Store (default) | one SQLite file | portable, deletable |

The model may judge, never compute: countable chores are priced by
`count × per-item seconds`, measured chores use the human's number, and totals
come from SQL. In the demo, the model proposed 20 minutes for 40 receipts; the
ledger booked 13 and printed the sum on the card.

**No local inference is used.** This machine could not run a local model; an
Ollama install was started and then removed at the user's request. The app keeps
a local-server path (any compatible base URL), but the demo evidence is the
hosted open-weight lane, and the post says so.

## Honest state (do not upgrade this in the post)

- **Synthetic demo corpus.** The eight chores in `tools/seed_demo.py` are a
  labelled fictional freelancer week, not the user's measurements.
- **No multi-user, no auth, no edit/delete.** Single-user local tool.
- **No public deployment.** Runs from `python app.py` on localhost; the post
  links the repo and does not pretend there is a live demo.
- **Free-tier API.** The Groq lane may rate-limit under a judge's hand; the rules
  floor answers instead, with the lane name printed on every card.

## Artifacts

- `draft.md` — the DEV post draft (not yet published).
- Repo: `docs/desktop.png`, `docs/mobile.png` — captures from the shipping build,
  served from the public repo so the post's images resolve.
- Design record: `SlothLedger/PRODUCT.md`, `DESIGN.md`,
  `.impeccable/surface-brief-ledger.md`, `.impeccable/review/` (captures +
  detector output).
- Tests: `python tests/test_ledger.py` → 11 tests OK;
  `python tools/smoke_http.py` → 15 checks passed against a live server on the
  Tiger lane.

## Publish checklist

- [x] In contest window (drafted Oct 25, before 12:29 PM IST)
- [x] Repo public, MIT, README + screenshots
- [x] Tags verified to exist (`tigerdata` is live on Week 3 entries)
- [ ] DEV draft created, then published on explicit yes
- [ ] Add the published article id + URL here after publishing
