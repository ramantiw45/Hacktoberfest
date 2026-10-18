# Week 2 — Side Hustle (Oct 12 → Oct 18, 11:59pm PDT)

**Submission status: draft written, repo committed locally, not yet published.**
Deadline in IST: Mon Oct 19, 12:29 PM.

## What was built

**Udhaar Book** — photograph one page of a shop's handwritten credit notebook
(*khata*); an open-weight lane chain reads the lines, the shopkeeper confirms
them, the balances follow, and each customer gets a WhatsApp reminder **in their
own language** (English / हिंदी / मराठी).

- **Code lives outside this folder**, by design:
  `C:\Users\Raman Tiwari\MyDevelopments\UdhaarBook` (its own git repo, commit
  `52c1d5c`). Nothing heavy belongs inside the Hacktoberfest tree.
- **Prize target:** Best Use of Gemma ($200, featured category) — Gemma 3 27B on
  AI Studio's free tier as the default reader, Gemma 3 4B via Ollama as the
  on-device lane, both selected by env var.
- **Second target, needs a call:** Best Use of Render (a `render.yaml` blueprint
  is committed and deploy-ready; see *Open decisions*).

## Why this qualifies for the theme

Side Hustle = *"build something with open-weight models or open-source AI that
someone would actually pay for."* The paying user is a neighbourhood kirana,
medical or vegetable shop in a tier-2 town: one shared Android phone, a paper
khata, no laptop, and no interest in typing yesterday's entries into an app.
The business case (₹99/month vs. ~₹650/month recovered leakage) is written up in
`draft.md`.

## Open source AI at the core

| Layer | What | Openness |
|---|---|---|
| Reading (default) | `gemma-3-27b-it` via Google AI Studio free tier | open weights |
| Reading (offline) | `gemma3:4b` via Ollama | open weights, on-device |
| Reading (failover) | `qwen/qwen3.8-27b` via Groq free tier | open weights |
| Reading (floor) | built-in deterministic parser | no key, no network |
| OCR (optional) | PP-OCRv5 / PaddleOCR / Tesseract via `requirements-ocr.txt` | open source, CPU only |
| Store | one SQLite file | portable, deletable |

Swapping lanes is one env var: every lane speaks chat-completions. The model is
allowed to soften wording and **never** to produce a figure — amounts come from
the ledger.

## Submission artifacts

- `draft.md` — the DEV post (title, screenshots, why-open paragraph, honest
  limits, prize categories). Placeholders `REPO` / `LIVE` / `SESSION` must be
  filled before publishing.
- Screenshots: `UdhaarBook/docs/screens/*.jpg` (read, confirm, book, ask,
  ask-greyscale, phone).
- Design record: `UdhaarBook/PRODUCT.md`, `.impeccable/surfaces/route-reminders.md`,
  `.impeccable/review/` (captures + detector findings + review packet).
- Tests: `pytest tests/` (4 pipeline tests) and `tools/smoke_http.py`
  (20 HTTP checks, including "a photo upload fails honestly, not with a blank page").

## Honest state (do not upgrade this in the post)

- **No field test and no first user.** `samples/*` are synthetic fixtures; the
  shop in the screenshots (`Suresh Kirana`) is a fixture shop.
- **The photo path is unproven on this machine.** Python 3.14 has no wheels for
  the on-device OCR runtimes, and no model key is set, so an uploaded photo gets
  an honest refusal and a pointer to the sample page. The text path, parsing,
  ledger and reminders are exercised end to end.
- **No live demo URL yet** (Week 1 ran on Render; this one is not deployed).

## Open decisions (need the user)

1. Push `UdhaarBook` to GitHub as a public repo (`ramantiw45/UdhaarBook`?), then
   fill `REPO` in `draft.md` — and the screenshot URLs, which assume
   `raw.githubusercontent.com/<user>/<repo>/main/docs/screens/...`.
2. Deploy to Render from `render.yaml` (needs the account dashboard) — that is
   both the `LIVE` line and the Best Use of Render entry. Set `AI_STUDIO_API_KEY`
   in the dashboard to route the demo through Gemma; without it the demo still
   works on the parser.
3. Save the agent session with DevRelay, which yields `SESSION` for the post.

## Reminders for publishing

- Required tag `#hf26challenge`; the field is 4 tags max
  (`hf26challenge`, `devchallenge`, `gemma`, `hacktoberfest` fits).
- Stage on DEV as a **draft first**, hand over the `edit_url`, publish only on an
  explicit yes. AI disclosure stays `some_ai`.
- Repo must be public before publishing, with LICENSE (MIT, already committed).
