# Udhaar Book — DEV draft (Week 2: Side Hustle)

> **Before publishing, fill these in** (nothing else in this file is a placeholder):
> - `REPO` = public repo URL for the UdhaarBook code
> - `LIVE` = live demo URL, **or** delete the Live line and keep the honest
>   "run it locally in 60 seconds" line. Do not link a demo that is not up.
> - `SESSION` = the DevRelay agent-session slug, if we save one.
> Screenshots assume images are served from the repo at
> `https://raw.githubusercontent.com/<user>/<repo>/main/docs/screens/...`.

---

# Udhaar Book: photograph the khata, get the udhaar back

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 2: Side Hustle](https://dev.to/challenges/hacktoberfest-week2-2026-10-12)*

TL;DR — Photograph one page of a shop's handwritten credit notebook. An open-weight model reads it (a deterministic parser takes over when there is no key), the shopkeeper confirms every line, the balances follow, and each customer gets a polite WhatsApp reminder **in their own language**. The AI does the reading; the shopkeeper does the deciding. Repo: REPO | Live: LIVE

## What I built

Every kirana, medical and vegetable shop around me runs on a *khata* — a paper notebook where credit gets written in pen, in a hurry, at the counter. *"Ramesh — cheeni 2kg + tel — 340."* Nothing is typed anywhere. When money comes back, it's squeezed into the margin in a different pen, and the running balance lives in the shopkeeper's head until the day it doesn't.

The money isn't lost because customers are dishonest. It's lost because **asking is awkward**. Nobody wants to walk up to a neighbour and say *"aapke ₹140 baaki hain"* — so the shopkeeper waits, the page gets older, and by month end he genuinely isn't sure who owes what any more.

Udhaar Book does three things:

1. **Reads one page of the notebook from a photo.** Local OCR if it's installed, an open-weight model otherwise, a plain deterministic parser if there is no key at all.
2. **Shows every line for confirmation.** Nothing is written to the ledger until a human says it's right.
3. **Turns balances into reminders**, in English, हिंदी or मराठी — with the figure coming from the ledger, never from the model.

## Who would pay for this

This is the part I took seriously, because "Side Hustle" invites you to hand-wave it.

A shop carrying ₹40,000 of udhaar with even 5% quiet leakage loses ₹2,000 every month to money it has already earned. Recovering a third of that is ~₹650 a month. The app costs ₹0 to run: free-tier model lanes, one SQLite file, one Android phone that is already on the counter. Charge ₹99/month and the tool has paid for itself the first time it recovers a single ₹140 line.

The competitor is not another app — it's the pocket of khata apps that want the shopkeeper to **type every entry**. That's the same reason the money gets lost in the first place: the entry never gets made. The only input that already exists in every one of those shops is the photo of a page.

## Demo

| | |
|---|---|
| ![Pick up a page — photo or sample](https://raw.githubusercontent.com/USER/REPO/main/docs/screens/01-read.jpg) | ![Confirm every line before it is written down](https://raw.githubusercontent.com/USER/REPO/main/docs/screens/05-confirm-before-writing.jpg) |
| **Read** — photo the page, or tick "use the sample page" and walk the whole flow with nothing installed. | **Confirm** — every line the reader found, editable, with the raw text one tap away. |
| ![The book: every customer, given / paid / balance](https://raw.githubusercontent.com/USER/REPO/main/docs/screens/02-the-book.jpg) | ![Who to ask: coded names, hue strips, reminder per customer](https://raw.githubusercontent.com/USER/REPO/main/docs/screens/03-who-to-ask.jpg) |
| **The book** — the ledger: what was given, what came back, what is left, per page. | **Who to ask** — the reminder screen. Names stay coded until you tap; the message is already written. |

One page of the sample notebook: 12 transactions, 8 customers, ₹3,210 given, ₹1,000 received, **₹2,210 still out**. Three of those eight have both taken credit and paid some back — that's the state a shop actually lives in, and the one a hand-written margin is worst at tracking.

## Why open matters for what I built

The shop's record of **who owes what, and to whom** is about as private as a small business gets. Names, amounts, neighbourhood relationships. That record should not require an account, a subscription, or an API that reads it.

- **Reading:** `gemma-3-27b-it` (open weights) via Google AI Studio's free tier, `qwen/qwen3.8-27b` on Groq as failover, `gemma3:4b` via Ollama when the shop's own machine can carry it, and a deterministic parser with no key and no network as the floor.
- **Swapping is one env var.** Every lane speaks the same chat-completions shape, so `OLLAMA_BASE_URL` pointed at a local model moves the whole pipeline on-device with zero code changes. Nobody can re-price a shop's own bookkeeping.
- **Cost structure:** at ₹0 per page, the ₹99/month price is a business. Per-token billing turns every read into a cost of goods, and at a ₹99 price point that math gets thin fast.
- **Data shape:** one SQLite file. It can be copied, backed up, deleted, or never uploaded at all. There is no vendor in the middle of a shop's ledger.

The honest asterisk: **the model only writes the sentence, never the number.** The amount in a reminder is read from the ledger; the model gets to soften the wording and nothing else. That rule is in the code, not the prompt.

One more thing, because "runs locally" is the easiest claim in a hackathon post to fake: the repo ships `docs/offline-proof.md`, a five-step test (install the reader, switch the Wi-Fi off *physically*, submit a page) and a table of **what each possible outcome lets you claim** — including the claims you are never allowed to write, like "100% offline" after a hosted lane answered the request. On this machine the honest row is the third one, and that is the row I used.

## How it works

```text
  one photo of a khata page
          │
          ├── local OCR installed?  ──►  text, on this machine (CPU only)
          │
          └── no OCR  ──►  open-weight lane chain
                             gemma3:4b        Ollama, on-device, offline
                             gemma 3 27B      AI Studio, free tier
                             qwen 3.8         Groq, failover
                             deterministic    no key, no network
          │
          ▼
  transaction rows ──► shopkeeper confirms ──► one SQLite file
                                                   │
                                                   ├──► balances per customer
                                                   └──► WhatsApp reminder
                                                        en / हिंदी / मराठी
```

- **Stack:** FastAPI + Jinja2 + SQLite + `httpx`. No model SDKs, so a new lane is a dozen lines and a Python upgrade can't break the app on a Tuesday. Fonts are self-hosted; nothing on any screen makes a third-party request.
- **The reminder is a link, not a send.** `wa.me/?text=...` opens WhatsApp with the message written. Nothing leaves the server, no customer phone numbers are stored, and the shopkeeper still chooses who gets it.

## The decision that took the longest

I am not going to pretend this was an OCR problem. Reading a messy page is the easy half.

The hard half is that **this screen lives on a counter where other people can see it.** The reminder screen is a list of the shop's debtors, and a shopkeeper will not use a tool that flashes a neighbour's name at whoever is standing there.

The screen I designed for is 9pm: shutter half down, one tube light, the shopkeeper alone with the notebook and a phone. That is the one moment the names are safe to show — and the moment the screen has to be worth opening.

So the names are coded: each customer shows as an entry number (their place in the order to ask), a hue strip and an amount, and one tap decodes the row into the name, the plain-language history ("Page 1 · 1 line · last 15/10 · ₹560 given") and the message. The first row is decoded on load, so the screen teaches itself in one look. Decoding is a one-tap act on a 68px row, and Reveal opens all eight when the counter is finally empty.

The screen is built as a catalogue sleeve, not a dashboard: one white hairline per customer, the amount as the only headline, identity as a hue strip and a number until you touch it. That is written down as a design system rather than left as taste.

Two more things I made the design carry its weight on:

- **Nothing is signalled by colour alone.** A filled strip means credit was given; a hollow strip with a line through it means money came back. Strip the colour off and the meaning is still there — which also matters because a shopkeeper will screenshot this and print it.
- **The reminder screen must survive a greyscale print**, so I checked it in greyscale, not just in the browser. It does.

![The reminder screen with colour stripped out](https://raw.githubusercontent.com/USER/REPO/main/docs/screens/03b-who-to-ask-greyscale.jpg)

## What I got wrong

An honest build log, because the flaws are more useful to read than the features.

- **My machine cannot install the OCR layer.** Python 3.14 has no wheels for the usual on-device runtimes yet, so on *this* box the photo path resolves to: no local reader → model lane → and with no key either, a screen that says exactly that and hands you the sample page. The local OCR path is written, documented in `requirements-ocr.txt` and untested here. That is a gap, not a feature, and I've labelled it one in the README.
- **No shopkeeper has used this yet.** No field test, no first user, no one has paid me ₹99. The sample notebook is a fixture I wrote; the shop name in the screenshots is a fixture shop. I would rather say that plainly than dress up a demo as a deployment.
- **Handwriting is genuinely hard, and the honest move is to say so.** [A benchmark of four open-source OCR engines on 5,578 handwritten prescriptions](https://dev.to/kaniel_outis/how-well-can-ocr-read-doctor-handwriting-in-2026-54hn) found the best of them get *one word in three* exactly right. I read that before building and it changed the design: the app does not try to be right, it tries to be **checkable**. Every figure is one tap from the raw text the reader saw, and the ledger never accepts a row nobody confirmed.
- **Devanagari handwriting is the weakest case** for every reader I looked at. The reminder templates are in Marathi and Hindi because the *message* is the part that must feel native, but I am not going to claim the reading is equally strong in all three scripts.

## Also worth reading, if you are building in this space

Three posts that shaped this build:

- **[I Built a Receipt Bookkeeper That Runs AI Fully Offline](https://dev.to/prosperiko/i-built-a-receipt-bookkeeper-that-runs-ai-fully-offline-the-business-math-only-works-because-the-58c5)** — the closest project to this one this week, and the cleanest statement of why the economics only close with open weights. Different user: their freelancer has a wallet of printed receipts; mine has a paper notebook and no laptop.
- **[How Well Can OCR Read Doctor Handwriting in 2026?](https://dev.to/kaniel_outis/how-well-can-ocr-read-doctor-handwriting-in-2026-54hn)** — the 1-in-3-words number above, measured rather than assumed.
- **[Building for the Next Billion Users: Engineering for Emerging Markets](https://dev.to/sunny7899/building-for-the-next-billion-users-engineering-for-emerging-markets-40cp)** — why every screen here is phone-first and why a dead end with no key would have been the real failure.

## Prize categories

**Best Use of Gemma.** Gemma 3 is both the default hosted reader (`gemma-3-27b-it` via AI Studio free tier) and the first choice for the on-device lane (`gemma3:4b` via Ollama). The two Gemma lanes sit at the two ends of the price/privacy trade-off — one free and remote, one free and offline — and both are selected by environment variable, not by code.

<!-- If a live demo exists, add: Best Use of Render — deployed ... . If a .tech domain is used, add it here. Otherwise delete this comment. -->

## Run it yourself

```bash
git clone REPO && cd UdhaarBook
python -m venv .venv && .venv\Scripts\activate     # or source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload                            # http://127.0.0.1:8000
```

**No key needed to judge it.** Tick *use the sample page*, press *Read this page*, and the whole flow runs on the built-in parser: 12 transactions, 8 customers, ₹2,210 outstanding, and a Marathi reminder at the end. Add one free AI Studio key in `.env` and the same flow goes through Gemma; add `OLLAMA_BASE_URL` and it never leaves the machine. `pip install -r requirements-ocr.txt` adds the on-device photo reader where wheels exist.

Tests: `python tests/test_pipeline.py` (4 checks — parsing, money maths, reminders, and the no-key path) and `python tools/smoke_http.py` (20 checks against the running app, including "an uploaded photo fails honestly, with 200, not a blank page"). Neither needs a test framework installed.

## Credits

Built with an AI coding agent in an opencode session over one weekend. The product truth was the human's — the shopkeeper, the counter scene, the rule that names stay coded — and the visual direction was chosen from options the agent dealt and built; the agent wrote the app, the test suite, the design system and this draft, and the human approved each ship decision. FastAPI, Jinja2, SQLite, `httpx`, the self-hosted Rajdhani, Mukta and Spline Sans Mono (all SIL OFL), and the open weights of Gemma 3 and Qwen 3.8. The sample notebook is synthetic and labelled as such in the repo.

**AI disclosure: some_ai.**

<!-- SESSION: replace with the saved agent session once it exists -->
{% agent_session SESSION %}
