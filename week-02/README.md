# Week 2 — Side Hustle (Oct 12 → Oct 18, 11:59pm PDT)

**Submission status: draft written, repo public at
<https://github.com/ramantiw45/UdhaarBook>, deploy guide committed, not yet
deployed or published.**
Deadline in IST: Mon Oct 19, 12:29 PM.

## What was built

**Udhaar Book** — photograph one page of a shop's handwritten credit notebook
(*khata*); an open-weight lane chain reads the lines, the shopkeeper confirms
them, the balances follow, and each customer gets a WhatsApp reminder **in their
own language** (English / हिंदी / मराठी).

- **Code lives outside this folder**, by design:
  `C:\Users\Raman Tiwari\MyDevelopments\UdhaarBook`, its own repo, now public at
  <https://github.com/ramantiw45/UdhaarBook> (`main`; `3c56eff` = finish-review
  fixes, `d3d276d` = deploy guide). Nothing heavy belongs inside the
  Hacktoberfest tree.
- **Prize target:** Best Use of Gemma ($200, featured category) — Gemma 4 26B A4B
  on AI Studio's free tier as the default reader, Gemma 3 4B via Ollama as the
  on-device lane, both selected by env var.
- **Second target, needs a call:** Best Use of Render. The `render.yaml` blueprint
  is deploy-ready and `UdhaarBook/docs/deploy.md` is the step-by-step; it needs
  the Render account (see *Open decisions*).

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
| Reading (default) | `gemma-4-26b-a4b-it` via Google AI Studio free tier | open weights |
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
  limits, prize categories). `REPO` and all five screenshot URLs are filled with
  the public repo; `LIVE` waits on the deploy, `SESSION` is optional.
- Screenshots: `UdhaarBook/docs/screens/*.jpg` (read, confirm, book, ask,
  ask-greyscale, phone).
- Design record: `UdhaarBook/PRODUCT.md`, `.impeccable/surface-brief-reminders.md`,
  `DESIGN.md` + `.impeccable/design.json` (the written system, reconciled to the
  shipped build), and `.impeccable/review/` (captures + detector findings +
  review packet, revision 2).
- Tests: `python tests/test_pipeline.py` (4 pipeline tests) and
  `python tools/smoke_http.py` (20 HTTP checks, including "a photo upload fails
  honestly, not with a blank page"). Neither needs a test framework installed.

## Honest state (do not upgrade this in the post)

- **No field test and no first user.** `samples/*` are synthetic fixtures; the
  shop in the screenshots (`Suresh Kirana`) is a fixture shop.
- **The photo path is unproven on this machine.** Python 3.14 has no wheels for
  the on-device OCR runtimes, and no model key is set, so an uploaded photo gets
  an honest answer (nothing here can read it, use the sample) rather than a
  crash or a blank table. The text path, parsing, ledger and reminders are
  exercised end to end.
- **No live demo URL yet.** Deploy instructions are committed
  (`UdhaarBook/docs/deploy.md`); the Render account and the AI Studio key are the
  user's to create. Until then the post links the repo only — no dead demo link.

## Revision 2 — after the finish review

The finish reviewer returned *fix* with eight material findings. All eight are
closed in `UdhaarBook` commit `3c56eff`, and every capture plus the review packet
was regenerated from that build:

1. Footer and read screen name what actually read the page (parser vs OCR vs
   model lane); the confirm screen no longer implies a model saw the image.
2. The plot band is capped at 118px with one dashed aggregate hairline past
   eighteen dues (proved on a throwaway 25-customer database).
3. Collapsed decode panels are `inert` — 18 tab stops at rest, not 32.
4. Copy is the one solid full-width action in a row; WhatsApp is a quiet 44px
   text link beneath it.
5. The identity device commits: 6px strip at rest, 10×44px on the decoded row,
   the entry number stepping to 15px there.
6. The "2 lines" filler is gone; at rest a row is entry number, mark, amount, and
   the page number moved into the opened row's lineage.
7. Seed `d2007df6` is recorded in `options-bolder.json`.
8. `DESIGN.md` + `.impeccable/design.json` now describe the shipped build; the
   detector's design-system advisories fell from 27 to zero.

Also fixed: `GET /read` returns 303 to `/` instead of raw JSON, and dead code is
gone (`--track`, `static/reminders.js`). Detector state: no errors, no
`text-occlusion`; the remaining warnings are the identity strip (`side-tab` ×4),
a white-ground static-scan contrast false positive, and the em-dash advisory.

## Revision 3 — the Gemma 4 route (deploy-day fix)

The first live read failed with `ai-studio: 404 Not Found` on
`/v1beta/openai/chat/completions`, next to `groq: 429`. Two separate facts:

1. **Gemma 3 was retired from the Gemini API in 2026.** AI Studio now serves
   only `gemma-4-31b-it` and `gemma-4-26b-a4b-it`, and Gemma 4 is **not** on the
   OpenAI-compatible route at all — only on the native `generateContent` route.
   Renaming the model alone would still have 404'd.
2. Groq's 429 was its free-tier rate limit, not a code fault. With the Gemma
   lane answering, it drops off the demo path.

The AI Studio lane now carries a small native-protocol adapter
(`_gemini_payload` / `_gemini_call` in `udhaar/llm.py`): system prompt becomes
`systemInstruction`, inline base64 images become `inline_data`, and the reply is
read from `candidates[0].content.parts`. Ollama and Groq keep the OpenAI shape.
The old `/openai` base URL in existing `.env` files is normalised
automatically, and the default model is `gemma-4-26b-a4b-it` — the fast MoE
variant; `gemma-4-31b-it` is one env var away for heavier pages. The 31B dense
model was the first pick, but it has a reported 500-error rate on the free tier;
the 26B-A4B is faster and steadier under a judge's hand, and a single retry on a
5xx covers the rest (429 is a quota answer, so it is never retried).

Proof: `tests/test_pipeline.py` is now **5 checks** — the new one asserts the
native body, the `/openai` normalisation and the Gemma 4 default —
and `tools/smoke_http.py` is still **20 PASS**. The hosted lane itself awaits
the key in the Render dashboard; that is the one thing this machine cannot
prove.

## Open decisions (need the user)

1. ~~Push `UdhaarBook` as a public repo~~ — **done**: public at
   <https://github.com/ramantiw45/UdhaarBook>, `main` is the default branch, and
   every screenshot URL in `draft.md` resolves from it.
2. **Deploy to Render** from the blueprint, following
   `UdhaarBook/docs/deploy.md`: create the free AI Studio key, paste it as
   `AI_STUDIO_API_KEY`, then `GET /healthz` should list
   `["ai-studio","deterministic"]`. That deploy is both the `LIVE` line and the
   Best Use of Render entry. Without a key the demo still works on the parser.
3. **Publish the DEV post** (`draft.md`) as a draft first; fill `LIVE` only if the
   deploy is healthy. Required tag `#hf26challenge`.
4. Optional: save the agent session with DevRelay for `SESSION`.

## Reminders for publishing

- Required tag `#hf26challenge`; the field is 4 tags max
  (`hf26challenge`, `devchallenge`, `gemma`, `hacktoberfest` fits).
- Stage on DEV as a **draft first**, hand over the `edit_url`, publish only on an
  explicit yes. AI disclosure stays `some_ai`.
- Repo is public with LICENSE (MIT). Do not link the demo until `/healthz` is
  green.
