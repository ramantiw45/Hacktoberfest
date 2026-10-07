"""
Foliage Walk Planner — Week 1 Touch Grass (Python, no local GPU needed).
Open core: open-weight model via Hugging Face Inference API.
Default: Qwen/Qwen2.5-7B-Instruct. Swap via MODEL_ID env (e.g. Llama 3.1).
Maps: Leaflet + OpenStreetMap (no key). Weather: Open-Meteo (no key).
"""
import os
from datetime import datetime

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from huggingface_hub import InferenceClient

load_dotenv()

MODEL_ID = os.getenv("MODEL_ID", "Qwen/Qwen2.5-7B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN", "")
# Inference provider routing. "hf-inference" = Hugging Face's own free serverless
# lane (no credits needed, rate-limited). "featherless-ai" etc. need paid credits.
MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "hf-inference")
# Free hosted lanes for open-weight chat (no GPU needed). Set ONE key to go live.
# Chain order: Groq -> Google AI Studio (Gemma) -> Hugging Face -> mock.
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")  # Meta Llama 3.3 70B, free tier
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemma-3-4b-it")  # Google Gemma 3 4B, free tier

app = FastAPI(title="Foliage Walk Planner")


def get_weather(lat: float, lon: float) -> dict:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        "&timezone=auto&forecast_days=2"
    )
    try:
        r = httpx.get(url, timeout=15, headers={"User-Agent": "foliage-walk-planner/1.0"})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def _chat_openai_compat(base_url: str, api_key: str, model: str, prompt: str) -> str:
    """One POST to any OpenAI-compatible chat endpoint. Raises on failure."""
    r = httpx.post(
        base_url.rstrip("/") + "/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.7,
        },
        timeout=60,
    )
    try:
        r.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise RuntimeError(
            f"{e.response.status_code} from {base_url}: {e.response.text[:200]}"
        ) from e
    return r.json()["choices"][0]["message"]["content"].strip()


def llm_plan(location: str, lat: float, lon: float, weather: dict, minutes: int):
    """Returns (plan_text, served_by, source_url), trying free lanes in order."""
    daily = weather.get("daily", {}) or {}
    tmax = (daily.get("temperature_2m_max") or ["?"])[0]
    tmin = (daily.get("temperature_2m_min") or ["?"])[0]
    rain = (daily.get("precipitation_probability_max") or ["?"])[0]

    prompt = f"""You plan short fall foliage walks that get people outside fast.
Location: {location} ({lat:.3f}, {lon:.3f})
Weather tomorrow: high {tmax}C low {tmin}C rain {rain}%
Time budget: {minutes} minutes.

Reply in 5 short lines:
1. Best 2-hour window
2. 2-3km loop idea (park/trail type, no car needed if possible)
3. Foliage cue to look for
4. What to bring (1 line)
5. One-sentence why this beats scrolling.
Keep screen time minimal, encourage going outside."""

    errors: list[str] = []
    if GROQ_API_KEY:
        try:
            text = _chat_openai_compat(
                "https://api.groq.com/openai/v1", GROQ_API_KEY, GROQ_MODEL, prompt
            )
            return (
                text,
                f"{GROQ_MODEL} (open-weight Llama via Groq free tier)",
                "https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct",
            )
        except Exception as e:
            errors.append(f"Groq: {e}")
    if GEMINI_API_KEY:
        try:
            text = _chat_openai_compat(
                "https://generativelanguage.googleapis.com/v1beta/openai",
                GEMINI_API_KEY,
                GEMINI_MODEL,
                prompt,
            )
            return (
                text,
                f"{GEMINI_MODEL} (open-weight Gemma via AI Studio free tier)",
                "https://ai.google.dev/gemma",
            )
        except Exception as e:
            errors.append(f"Google AI Studio: {e}")
    if HF_TOKEN:
        try:
            client = InferenceClient(provider=MODEL_PROVIDER, token=HF_TOKEN)
            out = client.chat_completion(
                model=MODEL_ID,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.7,
            )
            return (
                out.choices[0].message.content.strip(),
                f"{MODEL_ID} (open-weight via {MODEL_PROVIDER})",
                f"https://huggingface.co/{MODEL_ID}",
            )
        except Exception as e:
            errors.append(f"Hugging Face: {e}")
    if not errors:
        return (
            f"Mock plan (set GROQ_API_KEY for live open-weight output, {GROQ_MODEL}):\n"
            f"1. Go 9-11am, {tmax}C, rain {rain}%\n"
            "2. 2.5km park loop near you — see map pin\n"
            "3. Look for maples turning edge-first\n"
            "4. Bring water + light layer\n"
            "5. Two hours outside beats two hours scrolling.",
            "mock (no model key configured)",
            "https://github.com/ramantiw45/Hacktoberfest",
        )
    detail = "\n".join(f"- {x[:220]}" for x in errors)
    return (
        f"Live models briefly unavailable, tried:\n{detail}\n"
        f"Fallback: go 9-11am for {minutes} min, bring water.",
        "unavailable (all lanes failed)",
        "https://github.com/ramantiw45/Hacktoberfest",
    )


INDEX_HTML = """<!doctype html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<meta name="description" content="Foliage Walk Planner: one input, one autumn walk. The screen is the shortest part."/>
<title>Foliage Walk Planner</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Bitter:wght@500;700&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<style>
:root{
  --paper:#FAF6EC; --card:#FFFDF7; --ink:#232A20; --secondary:#55604E;
  --moss:#2E4B34; --ember:#A9501C; --line:#E7DCC4;
  --shadow:0 14px 34px rgba(46,75,52,.16);
  --radius:14px;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  line-height:1.55;
}
::selection{background:var(--moss); color:#fff}
a{color:var(--moss); text-underline-offset:3px}
:focus-visible{outline:3px solid var(--ember); outline-offset:2px; border-radius:6px}
.wrap{max-width:880px; margin:0 auto; padding:28px 20px 56px}
.site-head{display:flex; gap:16px; align-items:flex-start; margin:8px 0 4px}
.mark{flex:none; width:52px; height:52px; border-radius:16px; background:var(--moss);
  display:grid; place-items:center; box-shadow:var(--shadow)}
h1{
  font-family:Bitter,Georgia,"Times New Roman",serif; font-weight:700;
  font-size:clamp(1.9rem,1.3rem + 2.6vw,2.9rem); letter-spacing:-0.02em;
  line-height:1.08; margin:0; text-wrap:balance;
}
.lede{margin:8px 0 0; color:var(--secondary); max-width:65ch; font-size:1.05rem}
.lede strong{color:var(--ink)}
.grid{display:grid; grid-template-columns:minmax(0,5fr) minmax(0,7fr); gap:20px; margin-top:22px}
@media (max-width:760px){ .grid{grid-template-columns:1fr} }
.panel{background:var(--card); border-radius:var(--radius); box-shadow:var(--shadow); padding:20px}
.panel h2{
  font-family:Bitter,Georgia,serif; font-weight:500; letter-spacing:-0.01em;
  font-size:1.25rem; margin:2px 0 4px;
}
.panel p.hint{margin:0 0 14px; color:var(--secondary); font-size:.95rem; max-width:65ch}
.field{margin:12px 0}
label{display:block; font-weight:600; font-size:.92rem; margin-bottom:6px}
input{
  width:100%; padding:10px 12px; font:inherit; color:var(--ink);
  background:#fff; border:1.5px solid var(--line); border-radius:10px;
}
input::placeholder{color:#8A8471}
input:focus{border-color:var(--moss); outline:3px solid rgba(46,75,52,.25); outline-offset:1px}
.row{display:grid; grid-template-columns:1fr 1fr 1fr; gap:12px}
@media (max-width:480px){ .row{grid-template-columns:1fr} }
button{
  font:inherit; font-weight:700; color:#fff; background:var(--moss);
  border:0; border-radius:999px; padding:12px 22px; margin-top:16px; cursor:pointer;
  transition:transform .18s ease-out, background .18s ease-out;
}
button:hover{background:#24402B; transform:translateY(-1px)}
button:active{transform:translateY(0)}
button:disabled{background:#9AA393; cursor:wait; transform:none}
#map{height:340px; border-radius:var(--radius); box-shadow:var(--shadow); background:#EDE7D3; z-index:0}
@media (max-width:760px){ #map{height:280px} }
.result{
  margin-top:16px; background:var(--card); border-radius:var(--radius);
  box-shadow:var(--shadow); padding:20px; max-width:75ch;
}
.result h2{
  font-family:Bitter,Georgia,serif; font-weight:500; font-size:1.25rem;
  letter-spacing:-0.01em; margin:0 0 6px;
}
.result pre{
  margin:8px 0 0; padding:0; background:none; font:inherit; line-height:1.6;
  white-space:pre-wrap;
}
.meta{margin:14px 0 0; color:var(--secondary); font-size:.88rem; font-variant-numeric:tabular-nums}
.meta b{color:var(--ink)}
.error-text{color:#7C2D12}
footer{margin-top:28px; color:var(--secondary); font-size:.88rem; max-width:75ch}
footer p{margin:6px 0}
.reveal{animation:rise .5s cubic-bezier(.16,1,.3,1) both}
@keyframes rise{from{opacity:0; transform:translateY(10px); filter:blur(3px)}
  to{opacity:1; transform:none; filter:none}}
@media (prefers-reduced-motion:reduce){ .reveal{animation:none} button{transition:none} }
</style>
</head><body><div class="wrap">
<header class="site-head">
  <span class="mark" aria-hidden="true">
    <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#F5EEDC" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 21c-5 0-8-3.5-8-9 0-4 2.5-7.5 8-9 5.5 1.5 8 5 8 9 0 5.5-3 9-8 9Z"/>
      <path d="M12 21V8"/><path d="M12 13l3.2-3.2"/><path d="M12 16l-3.4-3.4"/>
    </svg>
  </span>
  <div>
    <h1>Foliage Walk Planner</h1>
    <p class="lede">One input, one autumn walk. <strong>The screen is the shortest part</strong> — plan in under a minute, then go outside.</p>
  </div>
</header>
<main>
<div class="grid">
  <section class="panel" aria-labelledby="plan-h">
    <h2 id="plan-h">Plan my walk</h2>
    <p class="hint">Pick a place and a time budget. We check the sky and the trees, you handle the walking.</p>
    <div class="field"><label for="loc">Place</label><input id="loc" value="Prospect Park, Brooklyn" autocomplete="off"/></div>
    <div class="row">
      <div class="field"><label for="lat">Latitude</label><input id="lat" value="40.660" inputmode="decimal" autocomplete="off"/></div>
      <div class="field"><label for="lon">Longitude</label><input id="lon" value="-73.969" inputmode="decimal" autocomplete="off"/></div>
      <div class="field"><label for="mins">Minutes</label><input id="mins" value="120" inputmode="numeric" autocomplete="off"/></div>
    </div>
    <button id="go" onclick="plan()">Plan my walk</button>
  </section>
  <div id="map" role="img" aria-label="Map of the walk area. Plan a walk to place a pin."></div>
</div>
<section class="result" aria-live="polite" aria-labelledby="walk-h">
  <h2 id="walk-h">Your walk</h2>
  <pre id="out">Choose a place and press “Plan my walk”. Your route appears here — then close the laptop.</pre>
  <p class="meta" id="meta"></p>
</section>
</main>
<footer>
  <p>Maps © OpenStreetMap contributors · Weather by Open-Meteo · Plan written by an open-weight model.</p>
  <p>Field-test rule: if the plan took longer to read than your walk took to start, we failed. Tell us.</p>
</footer>
</div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
let map=L.map('map').setView([40.66,-73.969],13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'© OpenStreetMap'}).addTo(map);
let pin=L.marker([40.66,-73.969]).addTo(map);
async function plan(){
 const btn=document.getElementById('go'), out=document.getElementById('out'),
       meta=document.getElementById('meta');
 const loc=document.getElementById('loc').value.trim()||'Somewhere green',
       lat=parseFloat(document.getElementById('lat').value),
       lon=parseFloat(document.getElementById('lon').value),
       mins=Math.min(300,Math.max(30,parseInt(document.getElementById('mins').value,10)||120));
 if(!isFinite(lat)||!isFinite(lon)){
   out.innerHTML='<span class="error-text">Those coordinates don’t look right.</span> Latitude runs -90 to 90, longitude -180 to 180 — fix them and try again.';
   meta.textContent=''; return;
 }
 btn.disabled=true; btn.setAttribute('aria-busy','true'); btn.textContent='Reading the sky…';
 out.textContent='Checking weather and foliage for '+loc+'…';
 map.setView([lat,lon],13); pin.setLatLng([lat,lon]);
 try{
   const r=await fetch(`/api/plan?location=${encodeURIComponent(loc)}&lat=${lat}&lon=${lon}&minutes=${mins}`);
   if(!r.ok) throw new Error('server said '+r.status);
   const j=await r.json();
   out.textContent=j.plan;
   meta.innerHTML='';
   meta.append('Model: ',Object.assign(document.createElement('b'),{textContent:j.model}),` · ${j.weather_summary}`);
   const card=out.closest('.result'); card.classList.remove('reveal'); void card.offsetWidth; card.classList.add('reveal');
 }catch(e){
   out.innerHTML='<span class="error-text">Couldn’t reach the planner.</span> Check your connection and press “Plan my walk” again — your place is still filled in.';
   meta.textContent='';
 }finally{ btn.disabled=false; btn.removeAttribute('aria-busy'); btn.textContent='Plan my walk'; }
}
</script></body></html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return INDEX_HTML


@app.get("/api/plan")
def plan(
    location: str = "Prospect Park",
    lat: float = 40.66,
    lon: float = -73.969,
    minutes: int = Query(120, ge=30, le=300),
):
    weather = get_weather(lat, lon)
    text, served_by, source_url = llm_plan(location, lat, lon, weather, minutes)
    daily = weather.get("daily", {}) or {}
    tmax = (daily.get("temperature_2m_max") or ["?"])[0]
    summary = f"{tmax}C max" if tmax != "?" else "weather unavailable"
    return {
        "plan": text,
        "model": served_by,
        "model_source": source_url,
        "weather_summary": summary,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
