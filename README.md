# 自进化智能体 (Self-Evolving Agents) 科研知识库与前沿追踪

欢迎进入**自进化智能体（Self-Evolving / Self-Improving Agents）**系统化研究知识库。本工作区专为智能体自我强化、长程规划、自主探索与在策略蒸馏等核心课题构建，分为两大独立体系：**学习笔记系统**（用于学术跟进与概念梳理）与**论文追踪系统**（用于每日科研论文调研与拆解）。

---

## 📁 目录架构说明

```plaintext
f:\LearningNotes\自进化智能体\
├── 01_学习笔记\
│   ├── 00_学习笔记总索引与知识图谱.md          # 学习笔记总索引与知识图谱导航（矩阵化分类与直达链接）
│   ├── 01_理论基石与分类规范\                  # 模块一：核心定义、3层循环、5代历史、5大流派、双维分类规范
│   │   └── 自进化智能体全景概览与双维分类体系.md
│   ├── 02_外围架构与Harness演进\               # 模块二：Agent Harness、SoL-Pi、宽深漏斗、4大机制、安全短路
│   │   └── SoL-Pi与Agent_Harness自演化深度精读.md
│   ├── 03_强化学习与特权蒸馏\                  # 模块三：稀疏奖励、RetireOPD、一阶梯度冲突数学证明、自适应退休
│   │   └── RetireOPD与在策略自适应蒸馏深度精读.md
│   ├── 04_环境交互与因果探索\                  # 模块四：ActObs环境观测建模、前驱基石(FireAct/AgentTuning/SWE-gym)
│   │   └── ActObs与环境观测联合建模深度精读.md
│   ├── 05_专题思辨与认知沉淀\                  # 模块五：外置记忆管理、遗忘曲线、自造工具与代码执行核心答疑
│   │   └── 外置记忆管理与自造工具核心认知答疑.md
│   └── 自进化智能体初学_系统化学习笔记.md      # 历史全集归档（严格增量保存，含全量推导与问答）
├── 02_前沿论文追踪\
│   ├── 00_论文追踪总索引.md                  # 论文总索引表：按日期记录收录篇数、PDF归档数与快速跳转链接
│   ├── 2026-09-18\                         # 按日期独立归档文件夹
│   │   ├── 2026-09-18_自进化智能体论文精选.md # 当日深度结构化科研调研报告（遵循双维标签规范）
│   │   ├── 2609.20784_RetireOPD_...pdf     # 核心高价值论文原版 PDF 文献
│   │   ├── 2609.20715_Dont_Mask_...pdf     # 核心高价值论文原版 PDF 文献
│   │   └── ...                             # 其他高价值文献原版 PDF
│   └── YYYY-MM-DD\                         # 未来每日自动生成对应日期的专属独立目录
├── scripts\
│   └── fetch_hf_papers.py                  # 自动化论文抓取、双维标签化研判与 PDF 自动归档引擎（Python 3.12+）
├── 00_DAILY_PAPERS_AGENT_HANDOVER.md       # 【核心交接文档】Daily Papers 定时追踪系统智能体交付与执行全景规范
└── README.md                               # 仓库总览与使用规范文档
```

---

## 📌 两大模块职责划分

### 1. 学习笔记系统 (`01_学习笔记/`)
- **定位**：用于跟进组会、自学、导师研讨、公式推导与技术细节答疑。
- **模块化结构**：按核心研究维度解耦为 5 个独立专栏主题，避免单文件过度膨胀，各专题独立维护、交叉索引。
- **分类标签规范**：全面落实 `[技术机制分类 (上下文/RL/Reasoning/Act/Harness/Auto-Research)]` × `[生命周期阶段 (离线训练/在线探索/知识蒸馏/测试应用/系统元设计)]` 双维正交标签标准。
- **维护准则 (Strict Incremental Append)**：
  - 严格遵循**增量追加与历史零删改**原则；
  - 所有数学公式、一阶梯度动力学证明、微观数值与代码示例 100% 完整留存；
  - 顶部自动增量维护 `Changelog` 与 `目录 (TOC)`。

### 2. 论文追踪系统 (`02_前沿论文追踪/`)
- **定位**：用于承担日常学术文献精读与调研工作。
- **数据源**：[Hugging Face Daily Papers](https://huggingface.co/papers)
- **调度机制**：当前未启用自动调度；`SelfEvolvingAgents-DailyPapers` 已于 2026-09-22 删除。
- **结构化拆解维度**：
  1. 具体研究什么（Research Objective）
  2. 解决了什么核心痛点（Problems & Pain Points）
  3. 提出的新技术 / 新架构 / 新理念（Novel Contribution）
  4. 对自进化智能体研究的深远影响与启示（Impact on Self-Evolving Agents）
  5. 官方 ArXiv / Hugging Face 链接及开源代码库

---

## 🚀 常用手动指令

### 1. 深度 Jev 智能分诊模式（推荐，两阶段研判 + 正文核验）：
```powershell
python scripts/run_jev_daily_pipeline.py
# 或指定日期与调试数量
python scripts/run_jev_daily_pipeline.py --date 2026-09-25
```

### 2. 纯基线正则初筛模式（零外部模型依赖，纯本地运算）：
```powershell
python scripts/fetch_hf_papers.py
```

### 3. 一键在“纯基线”与“Jev 增强”之间切换：
```powershell
# 一键移除 Jev 隔离至纯基线:
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/rollback_to_no_jev.ps1

# 一键重新启用 Jev:
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/enable_jev.ps1
```

## ⏰ 自动化状态

论文追踪目前只支持手动执行，自动化任务已取消。手动运行流程、过滤规则和归档规范见 [00_DAILY_PAPERS_AGENT_HANDOVER.md](./00_DAILY_PAPERS_AGENT_HANDOVER.md) 与无 Jev 纯基线手册 [00_BASELINE_NO_JEV_HANDOVER.md](./00_BASELINE_NO_JEV_HANDOVER.md)。
