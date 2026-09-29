from __future__ import annotations

import json
import urllib.error
import urllib.request

from scripts.jev_pipeline.openjev_client import API_URL


QUESTIONS = {
    "novelty_level": {
        "type": "choice",
        "instructions": "Using ONLY the supplied paper excerpts, classify the contribution to self-evolving agents. Distinguish foundational evolution mechanisms (environment synthesis, program verification, non-symmetric credit, self-revision scoping) from vertical application wrappers (robot deployments of standard prompt-reflection/coding) or ML training infra. Do not infer priority from benchmark gains alone.",
        "criteria": {
            "new_mechanism": "A clearly described new self-evolution mechanism, verifiable learning principle, or environment co-evolution framing with evidence",
            "incremental": "A useful but mainly incremental algorithm, engineering deployment on robot hardware without new evolution theory, or infra patch",
            "uncertain": "Available excerpts do not establish novelty"
        }
    },
    "comparison": {
        "type": "choice",
        "instructions": "Do the excerpts compare this work to prior approaches with a substantive methodological distinction?",
        "criteria": {
            "specific": "Specific distinction from prior work is stated",
            "generic": "Only generic novelty claims or scores",
            "missing": "No usable comparison in excerpts"
        }
    },
    "evaluation": {
        "type": "choice",
        "instructions": "What level of evaluation evidence is present in the excerpts?",
        "criteria": {
            "cross_domain_or_ablation": "Ablation or cross-domain evidence is explicitly present",
            "benchmark_only": "Only benchmark comparisons are shown",
            "insufficient": "No meaningful evaluation evidence in excerpts"
        }
    },
}


def verify(paper: dict, evidence: dict, api_key: str) -> dict:
    payload = {
        "model": "openjev",
        "state": {
            "title": paper["title"],
            "abstract": paper["summary"],
            "excerpts": evidence["sections"]
        },
        "questions": QUESTIONS
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"OpenJEV verification HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"OpenJEV verification network error: {exc.reason}") from exc

