from __future__ import annotations

import urllib.error
import urllib.request

from bs4 import BeautifulSoup

SECTIONS = (
    "introduction", "related work", "background", "method", "approach",
    "framework", "experiment", "evaluation", "ablation", "limitation",
    "discussion", "conclusion"
)
MAX_CHARS_PER_SECTION = 2200


def fetch_evidence(paper_id: str) -> dict:
    url = f"https://arxiv.org/html/{paper_id}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) JevDailyPapers/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            soup = BeautifulSoup(response.read(), "html.parser")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return {"status": "unavailable", "url": url, "reason": str(exc), "sections": []}

    sections = []
    for heading in soup.select("h2.ltx_title_section, h3.ltx_title_subsection, h4.ltx_title_subsubsection"):
        title = heading.get_text(" ", strip=True)
        if not any(word in title.lower() for word in SECTIONS):
            continue
        text = " ".join(p.get_text(" ", strip=True) for p in heading.parent.select(":scope > div p"))
        if text:
            sections.append({"heading": title, "excerpt": text[:MAX_CHARS_PER_SECTION]})
            
    if not sections:
        return {"status": "unavailable", "url": url, "reason": "No relevant sections in arXiv HTML", "sections": []}
    return {"status": "available", "url": url, "sections": sections[:12]}

