"""
Jev Plus v1.3 Dedicated Paper Tracking & Triage Agent
=====================================================
Enforces strict closed-loop self-evolution criteria, rejects pseudo-causal
statistical academic bloat, and demotes isolated single-tool feature engineering.

Core Principles (Jev Plus v1.3):
1. VETO 1: No Closed-Loop Self-Evolution Dynamics -> REJECT / NOT RECOMMENDED.
   - Demotes isolated tool engineering (e.g., adding a compact() action) without
     recursive self-improvement or meta-harness evolution.
2. VETO 2: Causal / Statistical Academic Bloat -> REJECT / NOT RECOMMENDED.
   - Rejects econometric/biostatistical papers dressing basic heuristic exploration
     (like epsilon-greedy slot rotation) in 40+ pages of SCM / IPW with intractable
     sample complexity (e.g., Causal Memory Policy / CMP).
3. VETO 3: System-Level Meta-Design Over Single-Point Tweaks.
   - Prioritizes macro-structural harness code evolution (e.g., MILO), dynamic playbook
     patching (Turbo Harness), literature-driven lifelong evolution (ScholarEvolve),
     and verifiable synthetic sandbox generation (SkillGym, PhantomEnvironments).
"""

import sys
import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

from .prompts import SYSTEM_PROMPT, paper_for_prompt

class JevTriageAgent:
    """
    Autonomous Jev Plus v1.3 Agent for evaluating and classifying frontier AI papers.
    """
    def __init__(self, version: str = "v1.3"):
        self.version = version
        self.system_prompt = SYSTEM_PROMPT

    def pre_filter_hard_exclusions(self, paper: Dict[str, Any]) -> Optional[str]:
        """
        Stage 1: Fast regex-based hard negative filter.
        Returns exclusion reason if filtered, None if passed.
        """
        title = paper.get("title", "").lower()
        summary = paper.get("summary", "").lower()
        text = f"{title} {summary}"

        # 1. Pure vision / video / image generation diffusion
        if any(kw in text for kw in [
            "text-to-video", "video generation", "diffusion model", "image synthesis",
            "gaussian splatting", "text-to-image", "super-resolution", "point cloud"
        ]):
            return "Pure computer vision / diffusion generation (off_topic)"

        # 2. Pure speech / audio
        if any(kw in text for kw in [
            "speech recognition", "text-to-speech", "audio synthesis", "voice conversion"
        ]):
            return "Pure speech / audio generation (off_topic)"

        # 3. Traditional document OCR / layout parsing
        if any(kw in text for kw in [
            "document parsing", "ocr", "layout analysis", "table recognition"
        ]):
            return "Traditional document parsing / OCR (off_topic)"

        # 4. Jev Plus v1.3: Statistical / Econometric Causal Bloat
        if ("inverse propensity weighting" in text or "hájek" in text or "positivity violation" in text) and \
           ("retrieval" in text or "memory" in text) and not ("recursive" in text or "harness" in text or "co-evolution" in text):
            return "Jev Plus v1.3 Veto 2: Causal/statistical academic bloat without closed-loop evolution"

        return None

    def evaluate_paper(self, paper: Dict[str, Any]) -> Dict[str, Any]:
        """
        Stage 2 & 3: Deep evaluation against Jev Plus v1.3 criteria.
        """
        exclusion = self.pre_filter_hard_exclusions(paper)
        if exclusion:
            return {
                "id": paper.get("id"),
                "title": paper.get("title"),
                "category": "not_recommended",
                "reason": exclusion,
                "confidence": 0.99
            }

        title = paper.get("title", "").lower()
        summary = paper.get("summary", "").lower()
        text = f"{title} {summary}"

        # Check for core self-evolving markers
        core_markers = [
            "harness discovery", "harness evolution", "co-evolv", "meta-evolution",
            "verifiable environment", "environment synthesis", "self-distillation",
            "on-policy distillation", "recursive self-improvement", "length-scaling tax",
            "scaffold-isolated", "online distillation"
        ]
        
        is_core = any(marker in text for marker in core_markers)
        
        # Jev Plus v1.3: Demote isolated component tweaks (like AutoCompact)
        is_isolated_tool = ("compact context" in text or "context compaction" in text) and \
                           not ("harness" in text or "island" in text or "recursive" in text)

        if is_core and not is_isolated_tool:
            category = "core_self_evolving"
            confidence = 0.95
            reason = "Advances fundamental closed-loop self-evolution / harness discovery / environment synthesis mechanism."
        elif is_isolated_tool:
            category = "adjacent_inspiration"
            confidence = 0.85
            reason = "Jev Plus v1.3 Veto 1: Isolated tool/action engineering without autonomous recursive self-improvement."
        elif "reward gaming" in text or "cheating" in text or "sandbox" in text:
            category = "adjacent_inspiration"
            confidence = 0.90
            reason = "Key safety / reward gaming benchmark for self-evolving agent reinforcement learning."
        else:
            category = "adjacent_inspiration"
            confidence = 0.70
            reason = "Related adjacent exploration or domain tooling."

        return {
            "id": paper.get("id"),
            "title": paper.get("title"),
            "category": category,
            "reason": reason,
            "confidence": confidence
        }

if __name__ == "__main__":
    agent = JevTriageAgent()
    print(f"JevTriageAgent {agent.version} initialized successfully.")
