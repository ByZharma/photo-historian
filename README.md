# Photo Historian

Date an old photograph from the evidence in it.

Upload a scan of an old photo. Claude reads the clues a historian checks (clothing, hairstyles, architecture, vehicles, signage, the photographic process, the print and its mount), says what date range each clue points to and why, and then gives an overall range that fits all of them. You also get the historical context for that time and place, concrete leads for archival research, and a note on what could make the estimate wrong.

**Live demo:** https://claude.ai/artifact/6FNFW97rbNfmzxvw1HjaFd (runs on claude.ai; each viewer's photos are analyzed on their own Claude account)

## Why

I'm a photographer and a history student. Old photos are historical sources, but most family and archive prints have no date. Dating them by hand means cross-checking fashion, architecture and photographic technology, and that takes experience. Photo Historian does a first pass and, more importantly, shows its reasoning so you can check it.

## How it works

- A single static page (`index.html`): no server, no build step.
- The page sends the image and a structured prompt to Claude through the claude.ai artifact runtime (`claude.use("sample")` with images), on the viewer's own Claude account. No API key is stored anywhere.
- The prompt makes Claude list the evidence **before** the date and keep the range consistent with every clue, widening it when the evidence is weak. This prevents the confident single-year guesses a model makes when you just ask "what year is this?".
- The answer comes back as JSON and is shown as an archive catalog card, with a timeline of photographic processes (daguerreotype → albumen → gelatin silver → colour → instant → digital) and the estimated range marked on it.
- The answer can be in English, Russian or Kazakh.

## The hard part

Getting the model to explain how it dated a photo instead of guessing a year. The fix was an evidence-first output schema: every clue has to name the range it points to, and the final range must agree with all of them.

## Limits

- It estimates, it doesn't prove. Reprints from old negatives, retouching and modern scans can make the material younger than the scene.
- It reads only what is visible. Writing on the back of a print, studio stamps and family knowledge are worth more than any model, so add them in the notes field.

Built with [Claude Code](https://claude.com/claude-code).
