---
name: hacktoberfest-submission
description: DEV post submission template, tags, AI disclosure, session embed and pre-publish checks for Hacktoberfest entries. Use when drafting or reviewing the weekly DEV article.
---

# Hacktoberfest Submission (DEV Post)

## Required mechanics
- Publish as DEV post **inside contest window** (Wk1 due Oct 11 11:59pm PDT).
- Include challenge **required tags** from page `full_details` (typically `devchallenge`/`hacktoberfest` + theme/sponsor tags) — max 4 tags, verify via list_tags, never invent.
- English for prize eligibility. List teammates' DEV handles.
- AI disclosure: DevRelay `create_article` defaults `some_ai` — keep it; never `no_ai` for agent-drafted. `fully_autonomous` only if zero human edits.
- Stage as draft first (`published:false`), hand over `edit_url`, publish only on explicit yes.

## Template (adapt per week's Submission Template)
```markdown
# <Title: verb + who it's for>
TL;DR — what it does, who goes outside, open core in 1 line. Live: <url> | Repo: <url> | Video: <url>

## The problem (Touch Grass: screen is longest part today)
## What I built (1 flow, 1 user)
## Why open-source AI (the judging paragraph)
- Model: <name, source, license> | Harness: <name + customization> | Local: <Ollama/... + specs>
- Offline/privacy/cost/swap proof: ...
- Why not closed: ...
## How it works (Mermaid arch + stack)
## Field test (took it outside — photos, what worked/failed)
## Partner category: <e.g. Best Use of Render — what deployed/how>
## Run it yourself (steps, env, test creds)
## Credits (reused code, data, AI help) + DevRelay session
{% agent_session <id_or_slug> %}
```

## DEV formatting
- Mermaid renders natively — keep diagram small. Images with alt text. Code blocks minimal but real (no secrets).
- Ground draft: semantic search DEV for 2-3 related posts, link them.
- Plagiarism: quote + link all non-trivial reuse; AI use doesn't excuse it.

## Pre-publish checks
- [ ] In-window, tags correct, English
- [ ] Live demo opens incognito; repo public + LICENSE + README
- [ ] Why-open + theme mapping present
- [ ] Session embed ID valid, video/GIF loads
- [ ] Teammates listed, credits done, disclosure `some_ai`
