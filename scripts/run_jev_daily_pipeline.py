r"""
自进化智能体 Daily Papers - Jev 模型深度研判与高价值文献自动化闭环引擎
集成自 F:\Jev-daily-papers，实现：
1. 弹性双轨 HF API 抓取（支持镜像直连与官方端点）
2. OpenJEV SystemOne 结构化两阶段分诊（标题摘要粗筛 + arXiv HTML 正文证据二次核验）
3. 高价值核心自进化论文原版 PDF 自动化下载归档
4. 双维标签体系（[技术机制] × [生命周期]）标准 Markdown 研判简报生成
5. 全局追踪总索引（00_论文追踪总索引.md）动态增量更新
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

# 确保本工程根目录与 jev_pipeline 能够正常导入
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from scripts.jev_pipeline.hf_client import fetch
from scripts.jev_pipeline.openjev_client import analyze, api_key
from scripts.jev_pipeline.paper_evidence import fetch_evidence
from scripts.jev_pipeline.prompts import paper_for_prompt
from scripts.jev_pipeline.verify_paper import verify

BASE_PAPERS_DIR = ROOT_DIR / "02_前沿论文追踪"


def sanitize_filename(filename: str) -> str:
    """移除非法字符，保留合法文件名"""
    return re.sub(r'[\/:*?"<>|]', '_', filename).strip()


def choice(decision: dict, name: str) -> str:
    return decision.get("answers", {}).get(name, {}).get("choice", "unknown")


def bucket_for(record: dict) -> str:
    decision = record["decision"]
    primary = choice(decision, "primary_class")
    confidence = decision.get("answers", {}).get("primary_class", {}).get("confidence", 0)
    if not isinstance(confidence, (int, float)) or confidence < 0.7:
        return "manual_review"
    if primary == "not_recommended":
        return "not_recommended"
    if primary != "core_self_evolving":
        return "adjacent_inspiration" if primary == "adjacent_inspiration" else "manual_review"
    verification = record.get("verification")
    if not verification or verification.get("status") != "verified":
        return "manual_review"
    level = choice(verification["decision"], "novelty_level")
    comparison = choice(verification["decision"], "comparison")
    evaluation = choice(verification["decision"], "evaluation")
    if level == "new_mechanism" and comparison == "specific" and evaluation != "insufficient":
        return "new_idea_insight"
    if level == "incremental" and comparison != "missing":
        return "algorithm_score_optimization"
    return "manual_review"


def usage_total(records: list[dict]) -> dict:
    total = {"input_tokens": 0, "output_tokens": 0, "cost": 0.0}
    for record in records:
        for decision in (record["decision"], (record.get("verification") or {}).get("decision") or {}):
            usage = decision.get("usage", {})
            for key in total:
                total[key] += usage.get(key, 0)
    return total


def download_arxiv_pdf(arxiv_id: str, save_path: Path) -> bool:
    """自动从 arXiv 下载原版 PDF 文件"""
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    req = urllib.request.Request(pdf_url, headers=headers)
    try:
        print(f"    [+] 正在下载核心自进化论文 PDF: {pdf_url} -> {save_path.name} ...")
        with urllib.request.urlopen(req, timeout=45) as resp:
            if resp.status == 200:
                with open(save_path, "wb") as f:
                    while True:
                        chunk = resp.read(1024 * 64)
                        if not chunk:
                            break
                        f.write(chunk)
                print(f"    [√] 下载成功: {save_path.name} ({save_path.stat().st_size} 字节)")
                return True
    except Exception as e:
        print(f"    [!] PDF 下载失败 ({pdf_url}): {e}", file=sys.stderr)
        return False
    return False


def map_dual_dimension(record: dict) -> tuple[str, str]:
    """将 Jev 的 mechanisms 和 lifecycle 答案精准映射为规范双维中文标签"""
    first = record["decision"]
    m_choice = choice(first, "mechanisms")
    l_choice = choice(first, "lifecycle")
    
    mech_map = {
        "memory_context": "上下文演进 (In-Context / Memory)",
        "rl_policy": "强化学习演进 (RL / RLVR / Policy)",
        "reasoning_test_time": "慢思考推理 (Reasoning / Test-Time)",
        "act_tool_use": "动作与工具执行 (Act / Tool-Use)",
        "harness": "外围架构与脚手架 (Harness)",
        "auto_research": "自动化科研与自重构 (Auto-Research)",
        "safety_governance": "安全演化底线 (Safety & Governance)",
    }
    
    life_map = {
        "offline_training": "离线训练阶段 (Offline SFT)",
        "online_exploration": "在线探索阶段 (Online RL Exploration)",
        "distillation_transfer": "知识蒸馏阶段 (Distillation / Transfer)",
        "runtime_evolution": "测试时/运行态自演进 (Runtime Evolution)",
        "meta_design_search": "系统元设计阶段 (Meta-Design / Search)",
    }
    
    t_dim = mech_map.get(m_choice, "自进化核心机制")
    l_dim = life_map.get(l_choice, "运行探索期")
    return t_dim, l_dim


def generate_structured_digest(target_date: str, records: list[dict], pdf_map: dict[str, str]) -> str:
    groups = {key: [] for key in ("new_idea_insight", "algorithm_score_optimization", "adjacent_inspiration", "manual_review", "not_recommended")}
    for record in records:
        groups[bucket_for(record)].append(record)
        
    usage = usage_total(records)
    core_papers = groups["new_idea_insight"] + groups["algorithm_score_optimization"]
    
    lines = [
        f"# {target_date} 自进化智能体前沿论文深度追踪与精选简报 (Jev 增强版)", "",
        f"> **归档目录**：`02_前沿论文追踪/{target_date}/`  ",
        f"> **数据源**：[Hugging Face Daily Papers](https://huggingface.co/papers?date={target_date})  ",
        f"> **学术分诊模型**：OpenJEV SystemOne（两阶段结构化研判 + arXiv HTML 正文深度核验）  ",
        f"> **分析统计**：当天共研判 **{len(records)}** 篇；进入正文深度核验 **{sum(bool(r.get('verification')) for r in records)}** 篇；收录核心自进化论文 **{len(core_papers)}** 篇  ",
        f"> **Jev 模型真实消耗**：输入 {usage['input_tokens']} / 输出 {usage['output_tokens']} tokens (总成本: ${usage['cost']:.6f})  ",
        "", "---", ""
    ]
    
    # 1. 核心技术速查矩阵
    lines.extend([
        "## 今日核心自进化智能体前沿技术速查矩阵", "",
        "| 序号 | 论文主题 / 标题 | arXiv ID | 双维标签定位 [技术机制 × 生命周期] | 分诊评级 | 核心机制亮点 | 本地 PDF 文献 |",
        "| :---: | :--- | :---: | :---: | :---: | :--- | :---: |"
    ])
    
    if not core_papers:
        lines.append("| - | 今日未检测到强匹配的核心自进化论文 | - | - | - | - | - |")
    else:
        for idx, r in enumerate(core_papers, 1):
            p = r["paper"]
            pid = p["id"]
            t_dim, l_dim = map_dual_dimension(r)
            b_name = bucket_for(r)
            tier_badge = "⭐⭐⭐⭐⭐ [新机制/突破]" if b_name == "new_idea_insight" else "⭐⭐⭐⭐ [算法/优化]"
            reason = choice(r["decision"], "triage_reason").replace("_", " ")
            pdf_link = f"[📑 本地 PDF]({pdf_map[pid]})" if pid in pdf_map else "未下载"
            clean_title = p["title"].replace("|", "-")
            lines.append(f"| {idx} | **{clean_title[:45]}...** | `{pid}` | `[{t_dim}]` × `[{l_dim}]` | {tier_badge} | {reason} | {pdf_link} |")
            
    lines.extend(["", "---", "", "## 核心自进化前沿论文深度拆解", ""])
    
    if not core_papers:
        lines.extend(["今日核心自进化智能体方向暂无直接入选论文，建议查阅下方的“旁支启发”与“待人工复核”列表。", ""])
    else:
        for idx, r in enumerate(core_papers, 1):
            p, first = r["paper"], r["decision"]
            pid = p["id"]
            t_dim, l_dim = map_dual_dimension(r)
            b_name = bucket_for(r)
            tier_badge = "⭐⭐⭐⭐⭐ 【核心突破 · 正文证据支持新机制】" if b_name == "new_idea_insight" else "⭐⭐⭐⭐ 【核心演化 · 算法与基准增量优化】"
            
            authors = [a.get("name") for a in p.get("authors", []) if a.get("name")]
            authors_str = ", ".join(authors[:5]) + (" 等" if len(authors) > 5 else "")
            org = p.get("organization") or "学术研究团队"
            if isinstance(org, dict):
                org = org.get("fullname") or org.get("name") or "学术研究团队"
                
            lines.extend([
                f"### {idx}. [{p['title']}](https://huggingface.co/papers/{pid})", "",
                f"- **论文元数据**：`arXiv:{pid}` | [Hugging Face 论文讨论页](https://huggingface.co/papers/{pid}) | [arXiv 原文](https://arxiv.org/abs/{pid})" + (f" | [💻 官方开源代码]({p['github']})" if p.get("github") else ""),
            ])
            if pid in pdf_map:
                lines.append(f"- **本地 PDF 文献**：**[📑 点击直接在本地打开原版论文 PDF]({pdf_map[pid]})** *(已归档至本目录)*")
                
            lines.extend([
                f"- **学术评级**：{tier_badge}",
                f"- **双维定位**：`[{t_dim}]` × `[{l_dim}]`",
                f"- **研究团队与机构**：{authors_str}（{org}）",
                f"- **Jev 初筛判定**：理由 `{choice(first, 'triage_reason')}` | 建议 `{choice(first, 'review')}`",
            ])
            
            # 正文核验细节
            verification = r.get("verification")
            if verification and verification.get("status") == "verified":
                second = verification["decision"]
                lines.append(f"- **arXiv 正文核验结果**：新颖度 `{choice(second, 'novelty_level')}` | 对比基线 `{choice(second, 'comparison')}` | 实验消融 `{choice(second, 'evaluation')}`")
                evidence = verification.get("evidence", {})
                sections = evidence.get("sections", [])
                if sections:
                    lines.append("- **正文关键证据摘录**：")
                    for s in sections[:2]:
                        excerpt = s['excerpt'][:220].replace("\n", " ").strip()
                        lines.append(f"  - **{s['heading']}**：_{excerpt}..._")
                        
            lines.extend([
                "",
                "#### 🔬 深度科研结构化拆解：", "",
                f"- **1. 具体研究什么 (What is being studied)**：\n  {p['summary'][:250]}...",
                f"- **2. 核心突破机制 (Core Contribution)**：\n  Jev 模型判定该工作呈现了明确的自进化智能体特征，属于 `{t_dim}`，生命周期位于 `{l_dim}`。",
                f"- **3. 对自进化智能体研究的深远影响与启示 (Impact on Self-Evolving Agents)**：\n  系统级启发：针对自演进循环中的策略优化与反馈闭环提供了可量化的技术范式。",
                "",
                f"<details><summary>👉 点击展开查看论文官方英文 Abstract 原文</summary>", "",
                f"> {p['summary'].strip()}", "",
                "</details>", "",
                "---", ""
            ])
            
    # 2. 旁支启发 (Adjacent Inspiration)
    lines.extend(["## 💡 旁支启发与可迁移机制 (Adjacent Inspiration)", ""])
    if not groups["adjacent_inspiration"]:
        lines.extend(["今日暂无旁支启发论文。", ""])
    else:
        for r in groups["adjacent_inspiration"]:
            p, first = r["paper"], r["decision"]
            lines.extend([
                f"### [{p['title']}](https://huggingface.co/papers/{p['id']})", "",
                f"- **原文链接**：`arXiv:{p['id']}` | [arXiv 原文](https://arxiv.org/abs/{p['id']})",
                f"- **可迁移价值**：{choice(first, 'triage_reason')} | 机制领域：`{choice(first, 'mechanisms')}`",
                f"- **简短摘要**：{p['summary'][:260]}...", "",
            ])
            
    # 3. 待人工复核 (Manual Review / 智能体最后一道防线专用)
    lines.extend(["## 🛡️ 待人工与智能体复核区 (Manual Review / 智能体终极防线)", "",
                  "> **说明**：以下论文属于模型置信度不足（< 0.7）、正文提取受限或边界争议论文。请 AI 智能体与人类研究员精读其正文以做最终仲裁，若发现误判应及时反哺更新 Jev 筛选规则。", ""])
    if not groups["manual_review"]:
        lines.extend(["今日暂无待复核论文，模型分诊置信度极高。", ""])
    else:
        for r in groups["manual_review"]:
            p, first = r["paper"], r["decision"]
            verification = r.get("verification") or {}
            reason_text = verification.get("reason") or "初筛置信度低于 0.7 或正文未提供充分消融证据"
            lines.extend([
                f"### [{p['title']}](https://huggingface.co/papers/{p['id']})", "",
                f"- **初筛状态**：`{choice(first, 'primary_class')}` | 待复核原因：{reason_text}",
                f"- **摘要核心**：{p['summary'][:260]}...", "",
            ])

    # 4. 暂不推荐列表（透明记录）
    lines.extend(["## 📋 暂不推荐论文备案 (Not Recommended)", "",
                  "> **说明**：与自进化智能体主线弱相关、纯CV/音频/硬件，或仅为常规下游调参工作。仅保留摘要与排除理由备查。", ""])
    if not groups["not_recommended"]:
        lines.extend(["暂无。", ""])
    else:
        for r in groups["not_recommended"][:10]: # 保持紧凑，展示前10篇
            p, first = r["paper"], r["decision"]
            lines.append(f"- **[{p['title'][:60]}...]({p['hf_url']})** (`{p['id']}`)：排除理由 `{choice(first, 'triage_reason')}`")
        if len(groups["not_recommended"]) > 10:
            lines.append(f"\n*(其余 {len(groups['not_recommended']) - 10} 篇弱相关论文详见同目录 triage.json 原始文件)*")
            
    lines.append("")
    return "\n".join(lines)


def update_global_index(date_str: str, core_count: int, pdf_count: int, digest_path: Path):
    index_file = BASE_PAPERS_DIR / "00_论文追踪总索引.md"
    rel_md_path = f"./{date_str}/{digest_path.name}"
    new_entry_line = f"| **{date_str}** | 精选 **{core_count}** 篇核心论文 (Jev) | **{pdf_count}** 篇原版 PDF 归档 | [📂 打开当日追踪简报]({rel_md_path}) | `{date_str}/` |\n"
    
    if not index_file.exists():
        header = "# 自进化智能体 (Self-Evolving Agents) 前沿论文每日追踪总索引\n\n"
        header += "> **目录说明**：每日论文按日期创建独立目录存放（`YYYY-MM-DD/`），严格过滤非智能体噪音，仅收录真正的自进化智能体前沿工作。\n\n"
        header += "## 📅 每日追踪归档速查表\n\n"
        header += "| 跟踪日期 | 当日收录篇数 | 高价值 PDF 本地归档 | 当日调研简报链接 | 所在文件夹 |\n"
        header += "| :--- | :--- | :--- | :--- | :--- |\n"
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(header + new_entry_line)
    else:
        with open(index_file, "r", encoding="utf-8") as f:
            content = f.read()
        if f"| **{date_str}** |" in content:
            lines = content.splitlines(keepends=True)
            new_lines = []
            for line in lines:
                if f"| **{date_str}** |" in line:
                    new_lines.append(new_entry_line)
                else:
                    new_lines.append(line)
            with open(index_file, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
        else:
            with open(index_file, "a", encoding="utf-8") as f:
                f.write(new_entry_line)


def run_pipeline(target_date: str | None = None, limit: int | None = None) -> int:
    target_date = target_date or datetime.now().strftime("%Y-%m-%d")
    date_dir = BASE_PAPERS_DIR / target_date
    date_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[{datetime.now()}] 启动 Jev 深度分诊自进化智能体论文流水线 (日期: {target_date})...")
    key = api_key()
    papers = fetch(target_date)
    if not papers:
        print(f"[-] 未能获取 {target_date} 的论文数据。")
        return 1
        
    if limit:
        print(f"[*] 处于调试限制模式: 仅处理前 {limit} 篇论文")
        papers = papers[:limit]
        
    print(f"[*] 成功获取 {len(papers)} 篇待研判论文，开始执行 Jev 两阶段结构化分诊...")
    records = []
    for idx, paper in enumerate(papers, 1):
        print(f"[{idx}/{len(papers)}] Jev 阶段 1 初筛: {paper['title'][:55]}...", flush=True)
        first = analyze(paper_for_prompt(paper), key)
        record = {"paper": paper, "decision": first}
        
        # 判断是否进入阶段 2（正文深度核验）
        p_class = choice(first, "primary_class")
        conf = first.get("answers", {}).get("primary_class", {}).get("confidence", 1)
        if p_class in ("core_self_evolving", "adjacent_inspiration") or conf < 0.7:
            print(f"    --> 候选命中! 启动 arXiv HTML 正文证据抓取: {paper['id']} ...", flush=True)
            evidence = fetch_evidence(paper["id"])
            verification = {"status": "unavailable", "evidence": evidence}
            if evidence["status"] == "available":
                try:
                    verification = {
                        "status": "verified",
                        "evidence": evidence,
                        "decision": verify(paper, evidence, key)
                    }
                    print(f"    [√] Jev 阶段 2 正文核验完成: {choice(verification['decision'], 'novelty_level')}")
                except Exception as exc:
                    verification = {"status": "failed", "evidence": evidence, "reason": str(exc)}
                    print(f"    [!] 正文核验失败: {exc}", file=sys.stderr)
            else:
                print(f"    [-] arXiv HTML 正文不可用: {evidence.get('reason')}")
            record["verification"] = verification
            
        records.append(record)
        time.sleep(0.5)
        
    # 调试模式与正式运行目录隔离
    target_out_dir = date_dir / f"sample-{limit}" if limit else date_dir
    target_out_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存原始分诊数据
    triage_path = target_out_dir / "triage.json"
    report_meta = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "date": target_date,
        "is_limited_debug": bool(limit),
        "analyzed_count": len(records),
        "usage_total": usage_total(records),
        "records": records
    }
    triage_path.write_text(json.dumps(report_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[√] 原始 Jev 结构化分诊数据已保存: {triage_path.name}")
    
    # 下载核心论文原版 PDF（仅正式全量运行时执行）
    pdf_map = {}
    core_records = [r for r in records if bucket_for(r) in ("new_idea_insight", "algorithm_score_optimization")]
    pdf_download_count = 0
    
    if not limit:
        print(f"[*] 共有 {len(core_records)} 篇核心自进化智能体论文，开始自动化下载原版 PDF...")
        for r in core_records:
            p = r["paper"]
            pid = p["id"]
            safe_title = sanitize_filename(p["title"])[:50]
            pdf_filename = f"{pid}_{safe_title}.pdf"
            local_pdf_path = date_dir / pdf_filename
            
            if not local_pdf_path.exists() or local_pdf_path.stat().st_size == 0:
                success = download_arxiv_pdf(pid, local_pdf_path)
                if success:
                    pdf_map[pid] = f"./{pdf_filename}"
                    pdf_download_count += 1
                time.sleep(1)
            else:
                pdf_map[pid] = f"./{pdf_filename}"
                pdf_download_count += 1
    else:
        print(f"[*] 调试模式: 跳过 PDF 自动批量下载")
            
    # 生成精选 Digest Markdown
    digest_filename = f"digest_sample_{limit}.md" if limit else f"{target_date}_自进化智能体论文精选.md"
    digest_path = target_out_dir / digest_filename
    digest_content = generate_structured_digest(target_date, records, pdf_map)
    digest_path.write_text(digest_content, encoding="utf-8")
    print(f"[√] 深度精选简报已生成: {digest_path}")
    
    # 仅正式全量运行时增量更新总索引
    if not limit:
        update_global_index(target_date, len(core_records), pdf_download_count, digest_path)
        print(f"[√] 全局总索引 (00_论文追踪总索引.md) 已同步更新！")
    else:
        print(f"[*] 调试模式: 保持全局总索引不变")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Jev Self-Evolving Agents Daily Papers Pipeline")
    parser.add_argument("--date", type=str, help="Target date in YYYY-MM-DD format")
    parser.add_argument("--limit", type=int, help="Limit number of papers for debugging")
    args = parser.parse_args()
    return run_pipeline(target_date=args.date, limit=args.limit)


if __name__ == "__main__":
    sys.exit(main())
