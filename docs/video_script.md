# Project 2 · Two-minute video script: "From a county shortlist to a cited memo in 20 seconds"

**Audience:** Head of Site Selection at a hyperscaler. **Length:** ~2:00 (about 290 words).
**How to record:** play the deck in slideshow mode and screen-record your slides while you read (Cmd + Shift + 5 → Options → Microphone). Pause one beat before your first line and after your last so the clips cut cleanly.
**Optional demo shot:** during slide 4, show the app (`streamlit run app.py`) running the Loudoun / El Paso / Grant request.

| Part | Speaker | Slides | Time |
|---|---|---|---|
| 1 | **Ben** | 1–3 | 0:00–0:30 |
| 2 | **Aditi** | 4–6 | 0:30–1:05 |
| 3 | **Michelle** | 7–8 | 1:05–1:30 |
| 4 | **Eglis** | 9–10 | 1:30–2:00 |

---

## Part 1 · Ben (0:00–0:30)

**Slide 1 · Title** (~5 s)
> "Last time, we showed you which counties to screen. Now we've built the analyst that screens them."

**Slide 2 · The answer** (~12 s)
> "Our agent writes a first-pass site memo in about 20 seconds, for under ten cents. Every number traces back to real data. Without our tools, only a third of the same AI's numbers match."

**Slide 3 · Today's process** (~13 s)
> "Today, an analyst spends about a day per shortlist pulling power prices, grid queues and competing sites from five sources. That's the work we automated."

## Part 2 · Aditi (0:30–1:05)

**Slide 4 · Agentic workflow** (~13 s)
> "Here's how it works. You type a request, like 'compare these three counties.' Claude plans which lookups it needs, calls our tools, and writes the memo using only what those tools return."

**Slide 5 · Tools** (~10 s)
> "It has six tools. Two use our Project 1 model. The others pull grid queues, known data centers, and live power prices from the Energy Department."

**Slide 6 · How we tested it** (~12 s)
> "Then we tried to break it. We ran fourteen requests, including vague county names, a fake county, requests outside the US, and an attempt to trick it into lying."

## Part 3 · Michelle (1:05–1:30)

**Slide 7 · Results** (~12 s)
> "It handled all fourteen correctly. When we told it to claim Maricopa's power costs one cent, it refused and reported the real price. And every figure matched our data."

**Slide 8 · What went wrong** (~13 s)
> "It isn't perfect. It sometimes does its own math, which we can't auto-check, and big requests take many tool calls. Each of these has a clear fix."

## Part 4 · Eglis (1:30–2:00)

**Slide 9 · Impact and adoption** (~15 s)
> "A screen that took a day now takes minutes. And since delay costs over ten thousand dollars per megawatt per day, deciding even one week sooner is worth about seven million dollars on one campus."

**Slide 10 · Recommendation** (~15 s)
> "Our ask: pilot it on your next shortlist, keep an analyst signing off every memo, and give it your own data, like win-loss history, so it gets sharper."

---

**Numbers check:** 100% vs 31%, 14/14, $0.035 mean cost, 17 s median, 7.57¢ Maricopa, $7M = 7 days × $10k/MW/day × 100 MW. All from `eval/results/summary.md` and the deck.
