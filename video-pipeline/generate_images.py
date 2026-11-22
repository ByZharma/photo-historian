"""Generate one image per line of project/scenes.txt with the free Pollinations API.

No API key needed. Already generated images are skipped, so a re-run continues
where the previous one stopped.
"""
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
SCENES = ROOT / "project" / "scenes.txt"
STYLE = ROOT / "project" / "style.txt"
OUT = ROOT / "output" / "images"

WIDTH = os.environ.get("IMG_WIDTH", "1920")
HEIGHT = os.environ.get("IMG_HEIGHT", "1080")
MODEL = os.environ.get("IMG_MODEL", "flux")
DELAY = float(os.environ.get("IMG_DELAY", "20"))  # pause between requests (free tier is rate limited)
RETRIES = 6


def read_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    return [l.strip() for l in path.read_text(encoding="utf-8").splitlines()
            if l.strip() and not l.strip().startswith("#")]


def fetch(prompt: str, seed: int) -> bytes:
    url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(prompt) + "?" + urllib.parse.urlencode(
        {"width": WIDTH, "height": HEIGHT, "model": MODEL, "seed": seed, "nologo": "true", "enhance": "false"})
    req = urllib.request.Request(url, headers={"User-Agent": "video-pipeline/1.0"})
    with urllib.request.urlopen(req, timeout=300) as r:
        data = r.read()
        if not r.headers.get("Content-Type", "").startswith("image/"):
            raise RuntimeError(f"not an image: {data[:200]!r}")
        return data


def main() -> int:
    scenes = read_lines(SCENES)
    style = " ".join(read_lines(STYLE))
    if not scenes:
        print(f"No scenes in {SCENES}")
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    failed = []
    for i, scene in enumerate(scenes, 1):
        target = OUT / f"{i:03d}.jpg"
        if target.exists():
            continue
        prompt = f"{scene}. {style}".strip()
        for attempt in range(1, RETRIES + 1):
            try:
                target.write_bytes(fetch(prompt, seed=i))
                print(f"[{i}/{len(scenes)}] ok")
                break
            except Exception as e:  # rate limit / timeout: wait longer and retry
                wait = DELAY * attempt * 2
                print(f"[{i}/{len(scenes)}] attempt {attempt} failed: {e}; waiting {wait:.0f}s")
                time.sleep(wait)
        else:
            failed.append(i)
        time.sleep(DELAY)
    if failed:
        print("Failed scenes:", failed, "- run the workflow again to retry only these.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
