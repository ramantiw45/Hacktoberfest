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

app = FastAPI(title="Foliage Walk Planner")


def get_weather(lat: float, lon: float) -> dict:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max"
        "&timezone=auto&forecast_days=2"
    )
    try:
        r = httpx.get(url, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def llm_plan(location: str, lat: float, lon: float, weather: dict, minutes: int) -> str:
    daily = weather.get("daily", {})
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

    if not HF_TOKEN:
        return (
            f"Mock plan (add HF_TOKEN for live open-weight output, model={MODEL_ID}):\n"
            f"1. Go 9-11am, {tmax}C, rain {rain}%\n"
            "2. 2.5km park loop near you — see map pin\n"
            "3. Look for maples turning edge-first\n"
            "4. Bring water + light layer\n"
            "5. Two hours outside beats two hours scrolling."
        )
    try:
        client = InferenceClient(token=HF_TOKEN)
        out = client.chat_completion(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
        )
        return out.choices[0].message.content.strip()
    except Exception as e:
        return f"Model call failed ({MODEL_ID}): {e}\nFallback: go 9-11am for {minutes} min, bring water."


INDEX_HTML = """<!doctype html><html><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Foliage Walk Planner</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<style>body{font-family:system-ui;margin:0;padding:16px;max-width:800px} #map{height:320px;margin:12px 0} input,button{padding:8px;margin:4px} pre{white-space:pre-wrap;background:#f4f4f4;padding:12px}</style>
</head><body>
<h2>🍂 Foliage Walk Planner</h2>
<p>1 input → 1 walk. Screen is the shortest part.</p>
<label>Place name <input id="loc" value="Prospect Park, Brooklyn"/></label>
<label>Lat <input id="lat" value="40.660" size="7"/></label>
<label>Lon <input id="lon" value="-73.969" size="8"/></label>
<label>Minutes <input id="mins" value="120" size="4"/></label>
<button onclick="plan()">Plan my walk</button>
<div id="map"></div>
<pre id="out">Click Plan…</pre>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
let map=L.map('map').setView([40.66,-73.969],13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'© OpenStreetMap'}).addTo(map);
let pin=L.marker([40.66,-73.969]).addTo(map);
async function plan(){
 const loc=document.getElementById('loc').value, lat=document.getElementById('lat').value,
 lon=document.getElementById('lon').value, mins=document.getElementById('mins').value;
 document.getElementById('out').textContent='Planning…';
 map.setView([+lat,+lon],13); pin.setLatLng([+lat,+lon]);
 const r=await fetch(`/api/plan?location=${encodeURIComponent(loc)}&lat=${lat}&lon=${lon}&minutes=${mins}`);
 const j=await r.json();
 document.getElementById('out').textContent=j.plan+`\\n\\n(model: ${j.model}, weather: ${j.weather_summary})`;
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
    text = llm_plan(location, lat, lon, weather, minutes)
    daily = weather.get("daily", {})
    summary = f"{daily.get('temperature_2m_max',[ '?'])[0]}C max"
    return {
        "plan": text,
        "model": MODEL_ID,
        "model_source": f"https://huggingface.co/{MODEL_ID}",
        "weather_summary": summary,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
