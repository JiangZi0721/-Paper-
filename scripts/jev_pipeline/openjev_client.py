from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


API_URL = "https://api.openjev.sh/v1/systemone"


def analyze(paper: dict, api_key: str) -> dict:
    payload = {
        "model": "openjev",
        "state": {"source": "Hugging Face Daily Papers", "paper": paper},
        "questions": {
            "primary_class": {
                "type": "choice",
                "instructions": "Classify the paper for self-evolving-agent research. Choose core_self_evolving for a direct self-improvement loop, adjacent_inspiration for a non-core paper with a concrete transferable mechanism, or not_recommended for weak relevance or insufficient evidence.",
                "criteria": {
                    "core_self_evolving": "Directly studies an agent that improves its policy, memory, skills, tools, harness, data, or parameters from feedback",
                    "adjacent_inspiration": "Not mainly self-evolving agents but offers a concrete transferable mechanism or evaluation lesson",
                    "not_recommended": "Weak relevance, insufficient evidence, or routine incremental work for this research track"
                }
            },
            "value_tier": {
                "type": "choice",
                "instructions": "Identify the strongest value signal. Use new_idea_insight for a new problem framing, mechanism, system boundary, or generalizable insight; algorithm_score_optimization for mainly algorithm, training, prompt, data, or benchmark optimization; adjacent_inspiration for useful non-core inspiration; routine_or_unclear when the abstract does not support a stronger claim.",
                "criteria": {
                    "new_idea_insight": "A new framing, mechanism, system boundary, or generalizable insight",
                    "algorithm_score_optimization": "Mostly incremental algorithmic, training, prompt, data, or benchmark optimization",
                    "adjacent_inspiration": "Useful transferable inspiration, but not a direct core contribution",
                    "routine_or_unclear": "Routine, weakly evidenced, or unclear from the abstract"
                }
            },
            "triage_reason": {
                "type": "choice",
                "instructions": "Choose the main reason supporting the triage decision, especially when not recommending the paper.",
                "criteria": {
                    "direct_self_evolution_loop": "Feedback changes the agent, memory, skills, tools, harness, data, or policy",
                    "new_system_boundary": "New system boundary or problem framing for agent evolution",
                    "transferable_mechanism": "Concrete mechanism adaptable to self-evolving agents",
                    "incremental_optimization": "Main contribution is an incremental algorithm, recipe, prompt, or implementation",
                    "benchmark_score_focus": "Evidence mainly emphasizes scores without a new transferable mechanism",
                    "weak_or_insufficient_evidence": "Abstract lacks evidence for a stronger inclusion",
                    "off_topic": "Outside the current research scope"
                }
            },
            "mechanisms": {
                "type": "choice",
                "instructions": "Choose the primary technical mechanism.",
                "criteria": {
                    "memory_context": "Memory, context, experience, or prompt evolution",
                    "rl_policy": "RL, RLVR, policy optimization, or distillation",
                    "reasoning_test_time": "Search, reflection, verification, or test-time compute",
                    "act_tool_use": "Tools, skills, action execution, or environment interaction",
                    "harness": "Agent harness, orchestration, runtime, or architecture",
                    "auto_research": "Automated research, self-reconstruction, or model/harness co-evolution",
                    "safety_governance": "Safety, auditability, alignment, or governance",
                    "none_clear": "No clear match"
                }
            },
            "lifecycle": {
                "type": "choice",
                "instructions": "Choose the central lifecycle phase.",
                "criteria": {
                    "offline_training": "Offline SFT or behavior cloning",
                    "online_exploration": "Online environment interaction or RL",
                    "distillation_transfer": "Teacher-student transfer or distillation",
                    "runtime_evolution": "Inference-time memory, skill, or runtime adaptation",
                    "meta_design_search": "System design search or architecture evolution",
                    "none_clear": "No clear phase"
                }
            },
            "evidence_quality": {
                "type": "score",
                "instructions": "How strong is the abstract-level evidence for the classification and value claim?",
                "criteria": ["Insufficient", "Weak", "Moderate", "Strong", "Very strong"]
            },
            "transferable_insight": {
                "type": "noul",
                "instructions": "Does the paper provide a concrete transferable insight for self-evolving agents?",
                "criteria": {
                    "true": "A specific mechanism, evaluation principle, or design lesson can be transferred",
                    "false": "No concrete transferable lesson is supported by the abstract"
                }
            },
            "novelty": {
                "type": "noul",
                "instructions": "Does the abstract support a genuinely new idea or insight rather than only incremental optimization?",
                "criteria": {
                    "true": "A new framing, mechanism, boundary, or generalizable insight is supported",
                    "false": "The contribution appears incremental, score-driven, or insufficiently evidenced"
                }
            },
            "review": {
                "type": "choice",
                "instructions": "What should the human reviewer do next?",
                "criteria": {
                    "read_first": "Read soon including method and ablations",
                    "read_if_time": "Keep for secondary reading",
                    "inspect_abstract_only": "Record the lesson but do not prioritize full reading",
                    "skip_for_now": "Do not prioritize for this track"
                }
            },
        },
    }
    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "HF-Daily-Papers-Self-Evolving-Triage/1.0"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"OpenJEV HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"OpenJEV network error: {exc.reason}") from exc


def api_key() -> str:
    key = os.environ.get("JEV_API_KEY") or os.environ.get("OPENJEV_API_KEY")
    if not key:
        raise RuntimeError("JEV_API_KEY or OPENJEV_API_KEY is not set.")
    return key

