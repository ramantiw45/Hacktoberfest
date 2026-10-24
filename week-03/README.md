# Week 3 — Slow and Steady (Oct 19 → Oct 25, 11:59pm PDT)

**Submission status: PUBLISHED 24 Oct 2026, 22:48 IST** — article id 4911464,
<https://dev.to/ramantiw45/sloth-ledger-the-model-has-an-opinion-the-ledger-has-the-numbers-22gc>
— with tags `devchallenge` `hf26challenge` `tigerdata` `opensource`, and it
appears in the `hf26challenge` feed. Live demo:
<https://sloth-ledger.onrender.com> (Render free plan, backed by Tiger Cloud).
Repo public at <https://github.com/ramantiw45/SlothLedger>.

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
- **Prize targets:** Best Use of Tiger Data ($100) and Best Use of Render ($200).
  Tiger: hypertable for reclaimed minutes, continuous aggregate for the panel
  that reads them, compression policy, least-privilege `sloth_app` role.
  Render: free web service built from `render.yaml`, deployed and verified live.
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
- **Public demo is shared and disposable.** Render free plan sleeps after 15
  minutes (first request takes a few seconds); writes are capped at 8 per
  visitor per 10 minutes and the page says `public demo · shared ledger`.
  Ledger data survives restarts because it lives in Tiger, not on Render.
- **Free-tier API.** The Groq lane may rate-limit under a judge's hand; the rules
  floor answers instead, with the lane name printed on every card.

## Artifacts

- `draft.md` — the published DEV post, mirrored from
  <https://dev.to/ramantiw45/sloth-ledger-the-model-has-an-opinion-the-ledger-has-the-numbers-22gc>
  (id 4911464).
- Repo: `docs/desktop.png`, `docs/mobile.png`, `docs/live.png` — captures from
  the shipping build and the Render deployment, served from the public repo so
  the post's images resolve.
- Deploy: `render.yaml` (blueprint, `sync: false` secrets, health check),
  `docs/deploy.md` (step-by-step), `requirements.txt` (only `pg8000`).
  Render service `srv-dbee9h0n74is73eev8hg`, region Singapore, free plan.
- Design record: `SlothLedger/PRODUCT.md`, `DESIGN.md`,
  `.impeccable/surface-brief-ledger.md`, `.impeccable/review/` (captures +
  detector output).
- Tests: `python tests/test_ledger.py` → 11 tests OK;
  `python tools/smoke_http.py` → 15 checks passed against a live server on the
  Tiger lane.
- Live verification: `/healthz` → `store=postgres`,
  `lanes=[rules, api:qwen/qwen3.8-27b]`; live POST judged by the model lane;
  test rows removed afterwards (8 chores / 4 runs / 43m remain).

## Publish checklist

- [x] In contest window (published 24 Oct, before the Sun Oct 25 12:29 PM IST
      deadline)
- [x] Repo public, MIT, README + screenshots
- [x] Tags verified to exist (`tigerdata` is live on Week 3 entries)
- [x] Deployed on Render free plan; `/healthz` and a live write verified
- [x] DEV post created and published (id 4911464) with live URL, Render
      section, live image
- [x] Published 24 Oct 2026, 22:48 IST — id 4911464, appears in the
      `hf26challenge` feed
- [x] Published article id + URL recorded above

**Submission complete.** One entry for Week 3; winners are announced the week of
Oct 26. No further action is required for the entry itself.
