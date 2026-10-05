import os
import subprocess
import re
import sys
import time

TARGET_DIR = r"f:\LearningNotes\自进化智能体\02_前沿论文追踪\2026-10-05"
os.makedirs(TARGET_DIR, exist_ok=True)

PAPERS_TO_DOWNLOAD = [
    {
        "id": "2610.02826",
        "title": "Scaling Trajectories for Complex Tasks through Recursive Self-Rewrite",
        "category": "core"
    },
    {
        "id": "2610.03548",
        "title": "Recursive Harness Self-Improvement for Frontier Reasoning Data Synthesis",
        "category": "core"
    },
    {
        "id": "2610.03634",
        "title": "Credit Where It Matters_ Dependency-Aware Policy Optimization for Terminal Agents",
        "category": "core"
    },
    {
        "id": "2610.03476",
        "title": "MobiAgent_ Dual-Loop Recursive Policy Self-Improvement for Long-Horizon Mobile Manipulation",
        "category": "core"
    },
    {
        "id": "2610.02824",
        "title": "MetaRubric_ Learning to Reward for Rubric-Based Reinforcement Learning",
        "category": "core"
    },
    {
        "id": "2610.03185",
        "title": "Gains and Collapse in On-Policy Distillation_ A Reinforcement Learning Perspective",
        "category": "adjacent"
    },
    {
        "id": "2610.03361",
        "title": "Follow the Winners_ Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT",
        "category": "adjacent"
    },
    {
        "id": "2609.36659",
        "title": "On-Policy Parameter Update Direction Underlies Generalization in LLM Post-Training",
        "category": "adjacent"
    },
    {
        "id": "2610.03089",
        "title": "Securing Computer-Use Agents Against Branch Steering Attacks",
        "category": "adjacent"
    },
    {
        "id": "2609.39050",
        "title": "Covert Assistance_ Helpful LLM Agents Evade Oversight in Multi-Agent Systems",
        "category": "adjacent"
    },
    {
        "id": "2610.03153",
        "title": "EvoRiskBench_ An Evolving Benchmark for Runtime Security Risks in Workspace Agents",
        "category": "adjacent"
    }
]

def sanitize_filename(name):
    return re.sub(r'[\/:*?"<>|]', '_', name).strip()

def download_paper(pid, title):
    safe_title = sanitize_filename(title)[:55]
    filename = f"{pid}_{safe_title}.pdf"
    filepath = os.path.join(TARGET_DIR, filename)

    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        print(f"[EXISTS] {filename} ({os.path.getsize(filepath)} bytes)")
        return True, filename

    url = f"https://arxiv.org/pdf/{pid}"
    print(f"[*] Downloading {pid}: {title[:40]}...")
    
    cmd = [
        "curl.exe",
        "-x", "http://127.0.0.1:9674",
        "-s", "-L",
        "--connect-timeout", "15",
        "--max-time", "60",
        "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        url,
        "-o", filepath
    ]
    
    try:
        ret = subprocess.run(cmd, capture_output=True, timeout=70)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
            print(f"[OK] Downloaded: {filename} ({os.path.getsize(filepath)} bytes)")
            return True, filename
        else:
            print(f"[WARN] Failed or file too small: {filename} (size: {os.path.getsize(filepath) if os.path.exists(filepath) else 0})")
            if os.path.exists(filepath):
                os.remove(filepath)
            return False, filename
    except Exception as e:
        print(f"[ERR] Exception downloading {pid}: {e}")
        return False, filename

def main():
    print(f"=== Starting 2026-10-05 Paper Archival ===")
    print(f"Target Directory: {TARGET_DIR}")
    results = {}
    for p in PAPERS_TO_DOWNLOAD:
        success, fn = download_paper(p["id"], p["title"])
        results[p["id"]] = (success, fn)
        time.sleep(1.0)
    
    succeeded = [pid for pid, (succ, _) in results.items() if succ]
    print(f"\nFinished: Successfully downloaded {len(succeeded)} / {len(PAPERS_TO_DOWNLOAD)} papers.")

if __name__ == "__main__":
    main()
