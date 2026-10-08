# Field test log — Week 1 Touch Grass

## Before
- Date: 8 Oct 2026, early morning
- Places entered: Virar (19.45510, 72.82513)
- Plan output (verbatim from live app):
  1. 10:00-12:00
  2. 2-3 km loop around Virar Lake promenade (no car needed)
  3. First golden leaves on the banyan trees
  4. Water, a light jacket, and a phone charger
  5. It's a real nature escape that recharges your brain more than scrolling.
- Served by: openai/gpt-oss-20b (open-weight GPT-OSS via Groq free tier)

## Outside
- Places actually walked: the hillside viewpoint above Virar town, then down to Virar Lake.
- Screen time: ~1 minute (one page load, one tap on "Plan my walk").
- Time outside: 1-2 hours.
- Photos: `field-photos/img1.jpeg` (hillside view over the town and the estuary), `img2.jpeg` (city below the viewpoint), `img3.jpeg` (Virar Lake, hazy morning light).

## Honest notes
- Weather shown vs actual: the app said "10:00-12:00" with no weather reading (Open-Meteo returned 429 from Render's shared IP, so the plan fell back to generic advice). The real morning was cooler and clearer than the midday haze in my photos — I went early, the app assumed midday. Off by hours, not by concept.
- What worked: the plan handed me a real destination I would not have chosen myself — the lake promenade — and the "no car needed" line meant I actually walked instead of driving somewhere. The packing line (water, light jacket) was right; I did not carry a charger and my phone died near the end, which is a failure I am choosing to report rather than hide.
- What failed: two things. (1) Weather never rendered for anyone on the deployed app, because Render free tier shares one egress IP across many instances and Open-Meteo rate-limits it. (2) "First golden leaves on the banyan trees" is a New England autumn line, not a Maharashtra one. In mid-October Virar the banyans are still deep green. The prompt is written for fall foliage and I tested it in a place with no fall foliage, so the cue was wrong and I ignored it.
- Would I use it again next weekend: yes, for the destination, not for the foliage talk. The value was "here is a walk you can start in 60 seconds". If the weather call worked, it would have told me early morning beats midday, which is exactly what I chose.

## Theme mapping
Touch Grass, literally: ~1 minute on a screen, 1-2 hours of hill, lake, estuary and birds. The screen was the shortest part by a factor of sixty.
