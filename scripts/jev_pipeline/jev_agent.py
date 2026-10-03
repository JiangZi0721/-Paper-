"""
Jev Plus v1.3.1 Dedicated Paper Tracking & Triage Agent
=====================================================
Enforces strict closed-loop self-evolution criteria, rejects pseudo-causal
statistical academic bloat, demotes isolated single-tool feature engineering,
and ELIMINATES template-anchored quota filling and greedy adjacent dumping.

Core Principles (Jev Plus v1.3.1):
1. VETO 1: No Closed-Loop Self-Evolution Dynamics -> REJECT / NOT RECOMMENDED.
2. VETO 2: Causal / Statistical Academic Bloat -> REJECT / NOT RECOMMENDED.
3. VETO 3: System-Level Meta-Design Over Single-Point Tweaks.
4. VETO 4: Anti-Quota Fallacy & Zero-Slot Bias -> NO PRESET "6+2" COUNTS.
   - Dynamic reporting based strictly on actual paper quality (0 to N).
5. VETO 5: Anti-Adjacent Dumping -> STRICT BOUNDARIES FOR ADJACENT INSPIRATION.
   - No dumping general ML papers into adjacent_inspiration.
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

        # Check for core self-evolving markers (fundamental closed-loop evolution)
        core_markers = [
            "harness discovery", "harness evolution", "co-evolv", "meta-evolution",
            "verifiable environment", "environment synthesis", "self-distillation",
            "on-policy distillation", "recursive self-improvement", "length-scaling tax",
            "scaffold-isolated", "online distillation", "curriculum learning for agent harness",
            "reusable experience", "experience tree", "soft memory"
        ]
        
        is_core = any(marker in text for marker in core_markers)
        
        # Jev Plus v1.3: Demote isolated component tweaks (like AutoCompact)
        is_isolated_tool = ("compact context" in text or "context compaction" in text) and \
                           not ("harness" in text or "island" in text or "recursive" in text)

        # Explicit adjacent categories (must match specific valuable agent-adjacent infrastructure)
        adjacent_markers = [
            "reward gaming", "cheating", "sandbox", "terminal execution", "verifiable reward",
            "workspace synthesis", "belief state", "belief trapping", "sharpening tax",
            "distillation dynamics", "multi-reward", "reward aggregation", "diagnostic ladder"
        ]
        is_adjacent = any(marker in text for marker in adjacent_markers)

        if is_core and not is_isolated_tool:
            category = "core_self_evolving"
            confidence = 0.95
            reason = "Advances fundamental closed-loop self-evolution / harness discovery / environment synthesis / on-policy distillation mechanism."
        elif is_isolated_tool:
            category = "adjacent_inspiration"
            confidence = 0.85
            reason = "Jev Plus v1.3 Veto 1: Isolated tool/action engineering without autonomous recursive self-improvement."
        elif is_adjacent:
            category = "adjacent_inspiration"
            confidence = 0.90
            reason = "Key execution sandbox, RL dynamics calibration, or model-harness boundary diagnostic."
        else:
            # Strictly reject papers that do not meet core or adjacent criteria
            category = "not_recommended"
            confidence = 0.85
            reason = "Off-topic or general capability work lacking closed-loop self-evolution or verifiable sandbox mechanics."

        return {
            "id": paper.get("id"),
            "title": paper.get("title"),
            "category": category,
            "reason": reason,
            "confidence": confidence
        }

if __name__ == "__main__":
    agent = JevTriageAgent(version="v1.3.1")
    print(f"JevTriageAgent {agent.version} initialized successfully with Anti-Quota Fallacy & Zero Greedy Dumping rules.")

