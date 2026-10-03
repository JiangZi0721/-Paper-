import urllib.request
import json
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from scripts.jev_pipeline.jev_agent import JevTriageAgent

def fetch_url(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    for base in ['https://hf-mirror.com', 'https://huggingface.co']:
        full = base + url
        try:
            req = urllib.request.Request(full, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                if r.status == 200:
                    return json.loads(r.read().decode('utf-8'))
        except Exception:
            pass
    return []

print("[*] Fetching live Daily Papers from Hugging Face...")
p_1002 = fetch_url('/api/daily_papers?date=2026-10-02')
p_home = fetch_url('/api/daily_papers')

seen = {}
for item in p_1002:
    pid = item.get('paper', {}).get('id') or item.get('id')
    if pid and pid not in seen:
        p = item.get('paper', item)
        seen[pid] = {
            'id': pid,
            'title': (p.get('title') or item.get('title') or '').strip(),
            'summary': (p.get('summary') or item.get('summary') or '').strip(),
            'upvotes': p.get('upvotes', 0),
            'authors': [a.get('name') for a in p.get('authors', []) if a.get('name')],
            'org': p.get('organization', {}).get('fullname') or p.get('organization', {}).get('name') or '',
            'github': p.get('githubRepo') or '',
            'publishedAt': p.get('publishedAt', '')[:10],
            'submittedOnDailyAt': p.get('submittedOnDailyAt', '')[:10]
        }

for item in p_home:
    pid = item.get('paper', {}).get('id') or item.get('id')
    if pid and pid not in seen:
        p = item.get('paper', item)
        seen[pid] = {
            'id': pid,
            'title': (p.get('title') or item.get('title') or '').strip(),
            'summary': (p.get('summary') or item.get('summary') or '').strip(),
            'upvotes': p.get('upvotes', 0),
            'authors': [a.get('name') for a in p.get('authors', []) if a.get('name')],
            'org': p.get('organization', {}).get('fullname') or p.get('organization', {}).get('name') or '',
            'github': p.get('githubRepo') or '',
            'publishedAt': p.get('publishedAt', '')[:10],
            'submittedOnDailyAt': p.get('submittedOnDailyAt', '')[:10]
        }

total_pool_count = len(seen)
print(f"[*] Total unique papers in live pool: {total_pool_count}")

# Exclude yesterday's tracked and excluded papers
tracked_yesterday = {
    '2610.02163', # AutoCompact
    '2610.02070', # CMP
    '2609.38349', # MILO
    '2609.37539', # SkillGym
    '2609.37915', # OASIS
    '2609.38854', # LSD
    '2609.36308', # CheatBench
    '2609.39982', # Mid-Harness
    '2610.02179', # Excluded
    '2610.02159'  # Excluded
}

incremental_candidates = {pid: p for pid, p in seen.items() if pid not in tracked_yesterday}
print(f"[*] Incremental candidate pool (excluding yesterday's 8 tracked + 2 excluded): {len(incremental_candidates)} papers")

agent = JevTriageAgent(version="v1.3.1")
triage_results = {
    'core_self_evolving': [],
    'adjacent_inspiration': [],
    'not_recommended': []
}

for pid, paper in incremental_candidates.items():
    decision = agent.evaluate_paper(paper)
    paper['confidence'] = decision['confidence']
    paper['reason'] = decision['reason']
    triage_results[decision['category']].append(paper)

print("\n" + "="*70)
print(f"[AUDIT] JEV PLUS v1.3.1 OBJECTIVE SPECTRUM AUDIT")
print("="*70)
print(f"Total Unique Live Pool:          {total_pool_count} papers")
print(f"Yesterday Tracked / Excluded:    {len(tracked_yesterday)} papers")
print(f"Today Incremental Candidate Pool:{len(incremental_candidates)} papers")
print(f"----------------------------------------------------------------------")
print(f"[CORE] Core Self-Evolving:       {len(triage_results['core_self_evolving'])} papers")
print(f"[ADJ]  Adjacent Inspiration:     {len(triage_results['adjacent_inspiration'])} papers")
print(f"[REJ]  Not Recommended:          {len(triage_results['not_recommended'])} papers")
print("="*70 + "\n")

# Save structured output
with open('scripts/incremental_triage_result.json', 'w', encoding='utf-8') as f:
    json.dump({
        'stats': {
            'total_pool': total_pool_count,
            'tracked_yesterday': len(tracked_yesterday),
            'incremental_candidates': len(incremental_candidates),
            'core_count': len(triage_results['core_self_evolving']),
            'adjacent_count': len(triage_results['adjacent_inspiration']),
            'not_recommended_count': len(triage_results['not_recommended'])
        },
        'core': triage_results['core_self_evolving'],
        'adjacent': triage_results['adjacent_inspiration'],
        'not_recommended': triage_results['not_recommended']
    }, f, ensure_ascii=False, indent=2)

print("--- CORE PAPERS ---")
for i, p in enumerate(triage_results['core_self_evolving'], 1):
    print(f"{i}. [{p['id']}] (upvotes: {p['upvotes']}) -> {p['title']}")
    print(f"   Reason: {p['reason']}")

print("\n--- ADJACENT PAPERS ---")
for i, p in enumerate(triage_results['adjacent_inspiration'], 1):
    print(f"{i}. [{p['id']}] (upvotes: {p['upvotes']}) -> {p['title']}")
    print(f"   Reason: {p['reason']}")

