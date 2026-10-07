---
name: hacktoberfest-tools
description: Allowed open-weight models, frameworks, local-inference runtimes, deploy targets and free credits for Hacktoberfest 2026. Use when choosing a stack or proving open-source-AI-at-core.
---

# Hacktoberfest Tools (Allowed Stack)

Rule: open pieces must be **what makes the project work**, not decoration.

## 1. Open-weight models (pick 1 as core)
- Llama 3.x, Mistral/Mixtral, Qwen 2.5, Gemma 2/3, Phi-3/4, Falcon, OLMo, DeepSeek-distills, Whisper (STT), Piper/Bark (TTS), Stable Diffusion (image), YOLOv8 (vision).
- State exact model + weights source + license (e.g. `meta-llama/Meta-Llama-3.1-8B-Instruct`, Llama Community License).
- Swappable-model design scores: abstract behind interface, document how to swap.

## 2. Local inference (proves privacy/offline/cost story)
- **Ollama** (easiest: `ollama run llama3.1`), llama.cpp, vLLM, Ollama + Open WebUI, HuggingFace Transformers, LM Studio.
- Demo angle: runs on laptop, no internet, no data leaves device — record a photo/video offline.
- Always note RAM/VRAM needs + quantized variant used (Q4/Q5).

## 3. Open-source agent harness / framework
- LangChain/LangGraph, LlamaIndex, CrewAI, AutoGen, Haystack, OpenClaw, Semantic Kernel (OSS), Flowise/Langflow (low-code agents).
- Judges want: tools the agent can call, memory, guardrails you customized — show the graph/code.

## 4. Data + supporting OSS
- pgai + Ollama + Postgres, SQLite/DuckDB, Chroma/Qdrant (self-hosted), Leaflet/OpenStreetMap (maps — no Google key), FastAPI, Next.js, SvelteKit, Tailwind.
- Bird/weather/trail data: eBird API, Open-Meteo, GBIF, local CSV.

## 5. Deploy + partner categories (target ≥1 for $200 pool)
- **Render** = known featured category (Best Use of Render, $200). Use Render Blueprint + free tier.
- Others rotate among the 16 partners — read current challenge `full_details`/page, pick the one your stack already fits. Claim credits first: Tinker, Render, Backboard, ElevenLabs at hacktoberfest.com/my/promos.
- Keep deploy free-tier-safe; provide live URL + test creds if login needed.

## 6. Writing/evidence toolchain
- DevRelay: save agent session → embed in DEV post (optional, helps judging).
- Mermaid diagrams render natively on DEV — include architecture diagram.
- LICENSE file (MIT/Apache-2.0), README with setup, env vars, demo video/GIF.

## Anti-patterns
- Closed-API-only (pure GPT-4/Claude/Gemini API with no open model/harness) = fails core requirement.
- Paywalled deploy judges can't open. Missing LICENSE. No offline/privacy/cost argument.
