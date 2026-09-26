from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

DEFAULT_ENDPOINT = os.environ.get("HF_ENDPOINT", "https://hf-mirror.com").rstrip("/")
CANDIDATE_ENDPOINTS = list(dict.fromkeys([
    DEFAULT_ENDPOINT,
    "https://hf-mirror.com",
    "https://huggingface.co"
]))
USER_AGENT = "HF-Daily-Papers-Self-Evolving-Triage/1.0"


def fetch(date: str | None = None) -> list[dict]:
    query = f"?date={date}" if date else ""
    errors = []
    
    for base in CANDIDATE_ENDPOINTS:
        url = f"{base}/api/daily_papers{query}"
        try:
            data = _fetch_python(url)
            if isinstance(data, list) and data:
                return [normalize(item) for item in data]
        except RuntimeError as python_error:
            errors.append(f"{base} (python): {python_error}")
            if sys.platform == "win32":
                try:
                    data = _fetch_windows(url)
                    if isinstance(data, list) and data:
                        return [normalize(item) for item in data]
                except RuntimeError as win_error:
                    errors.append(f"{base} (windows): {win_error}")
                    
    raise RuntimeError(f"Hugging Face fetch failed across all endpoints: {'; '.join(errors)}")


def _fetch_python(url: str) -> object:
    # 针对 hf-mirror 明确绕过本地代理，避免代理拦截导致 SSL 握手异常
    if "hf-mirror.com" in url:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    else:
        opener = urllib.request.build_opener()
        
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with opener.open(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}") from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(f"Python network error: {exc}") from exc


def _fetch_windows(url: str) -> object:
    command = [
        "powershell.exe", "-NoProfile", "-NonInteractive", "-Command",
        "$ProgressPreference='SilentlyContinue'; "
        f"$r=Invoke-WebRequest -UseBasicParsing -Uri '{url}' "
        f"-Headers @{{'User-Agent'='{USER_AGENT}'}} -TimeoutSec 30; "
        "[Console]::OutputEncoding=[Text.Encoding]::UTF8; [Console]::Out.Write($r.Content)",
    ]
    try:
        completed = subprocess.run(command, capture_output=True, timeout=40, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise RuntimeError(f"PowerShell execution failed: {exc}") from exc
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.decode("utf-8", errors="replace").strip() or "unknown PowerShell error")
    try:
        return json.loads(completed.stdout.decode("utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"PowerShell returned invalid JSON: {exc}") from exc


def normalize(item: dict) -> dict:
    paper = item.get("paper") or {}
    paper_id = paper.get("id") or item.get("id") or ""
    return {
        "id": paper_id,
        "title": (paper.get("title") or item.get("title") or "").strip(),
        "summary": (paper.get("summary") or item.get("summary") or "").strip(),
        "authors": paper.get("authors") or item.get("authors") or [],
        "organization": paper.get("organization") or item.get("organization"),
        "upvotes": paper.get("upvotes", item.get("upvotes", 0)),
        "github": paper.get("githubRepo") or item.get("githubRepo"),
        "hf_url": f"https://huggingface.co/papers/{paper_id}",
        "arxiv_url": f"https://arxiv.org/abs/{paper_id}" if paper_id else None,
        "published_at": item.get("publishedAt") or paper.get("publishedAt"),
    }

