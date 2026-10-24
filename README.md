# Hacktoberfest 2026 — build it, then write it down

My record of the **DEV Open-Source AI Challenge** (MLH + DEV, presented by
DigitalOcean). No PR counting this year: each round is a new project with
open-source AI at its core, plus a DEV post that explains why open innovation
matters for what was built.

[Challenge hub](https://dev.to/challenges) ·
[#hf26challenge](https://dev.to/t/hf26challenge) ·
[Hacktoberfest](https://hacktoberfest.com) ·
[Promos](https://hacktoberfest.com/my/promos)

## Season at a glance

| Week | Theme | Window | Project | Code | DEV post |
|---|---|---|---|---|---|
| — | Build for a Friend | Oct 02-05 | not entered | — | — |
| 1 | Touch Grass | Oct 05-11 | Foliage Walk Planner | [week-01-touch-grass](https://github.com/ramantiw45/Hacktoberfest/tree/main/week-01-touch-grass) | [I planned a walk in 60 seconds…](https://dev.to/ramantiw45/i-planned-a-walk-in-60-seconds-then-walked-for-two-hours-open-weight-ai-no-gpu-248o) |
| 2 | Side Hustle | Oct 12-18 | Udhaar Book | [UdhaarBook](https://github.com/ramantiw45/UdhaarBook) | [Photograph the khata, get the udhaar back](https://dev.to/ramantiw45/udhaar-book-photograph-the-khata-get-the-udhaar-back-5bej) |
| 3 | Slow and Steady | Oct 19-25 | Sloth Ledger | [SlothLedger](https://github.com/ramantiw45/SlothLedger) | [The model has an opinion, the ledger has the numbers](https://dev.to/ramantiw45/sloth-ledger-the-model-has-an-opinion-the-ledger-has-the-numbers-22gc) |
| 4 | TBD — drops Oct 26 | Oct 26-31 | — | — | upcoming |

Weeks 1-3 are published inside their windows. Week 4 is the last round.

## How an entry works

- One **new project per challenge**, started inside that week's window. Prior
  open-source work can be credited, not reused as the entry.
- At least one of these has to be what makes it work: an **open-weight model**,
  an **open-source agent harness**, or **local inference**. The post explains why
  that choice matters, not just which model was called.
- Publish on DEV before the deadline with the required **#hf26challenge** tag
  (plus `devchallenge`; four tags maximum).
- Writing quality is weighted most heavily, then relevance to the prompt and
  theme, creativity, technical execution, and partner use.
- Partner categories are separate prizes. Across the season the builds used
  Gemma, Tiger Data, and Render; each post names what actually ran.

## What is in here

| Path | What it holds |
|---|---|
| `skills/` | Rules, FAQ, tool notes, playbook, and the submission checklist to load before weekly work |
| `week-XX/` | That week's record: published post mirror (`draft.md`), field-test notes, captures |
| `week-01-touch-grass/` | Week 1 app, which lives in this repo |
| `AGENTS.md` | Standing instructions for agents working in this folder |

Weeks 2 and 3 keep their code in separate public repos (`UdhaarBook`,
`SlothLedger`) so each app can be cloned, tested, and deployed on its own.
Weeks 1-3 each have a published DEV post linked in the table above.

## Honest notes

- Demo corpora are synthetic and labelled in each repo; no real customer's or
  user's data is shown.
- Live demos are free-tier Render services and may sleep on the first request;
  the posts say so where it matters.
- Posts are snapshots. A shared demo ledger can move after publication, and the
  post says which figures are the build snapshot.

## Prizes, briefly

Each week awards one overall prize ($250 + DEV++ membership + winner badge) and
one winner per partner category ($200 each). Free partner credits are claimed at
[hacktoberfest.com/my/promos](https://hacktoberfest.com/my/promos), and three
virtual stickers earn a mailed sticker pack. No pull requests, no labels.

Agents: read `AGENTS.md` and the relevant `skills/` file before any weekly work.
