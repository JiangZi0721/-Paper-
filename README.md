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
- **调度机制**：Windows 任务计划程序已配置为每天上午 **10:00**（本机时区）自动执行 `SelfEvolvingAgents-DailyPapers`。
- **结构化拆解维度**：
  1. 具体研究什么（Research Objective）
  2. 解决了什么核心痛点（Problems & Pain Points）
  3. 提出的新技术 / 新架构 / 新理念（Novel Contribution）
  4. 对自进化智能体研究的深远影响与启示（Impact on Self-Evolving Agents）
  5. 官方 ArXiv / Hugging Face 链接及开源代码库

---

## 🚀 常用手动指令

若需要随时手动触发最新前沿论文同步与分析，可在根目录执行：
```powershell
python scripts/fetch_hf_papers.py
```
该脚本会自动去重，仅更新当日最新解析，同时完整保留所有历史日期的追踪记录。

## ⏰ 每日自动化配置

### 执行内容

每日 10:00 运行 `scripts/fetch_hf_papers.py`，完成以下流程：

1. 请求 Hugging Face Daily Papers API；
2. 按黑名单、Agent 主体和自进化特征词进行严格筛选；
3. 生成 `02_前沿论文追踪/YYYY-MM-DD/` 下的当日 Digest；
4. 从 arXiv 下载筛选论文 PDF；
5. 增量更新 `02_前沿论文追踪/00_论文追踪总索引.md`。

### Windows 任务计划程序

- **任务名**：`SelfEvolvingAgents-DailyPapers`
- **触发时间**：每天 `10:00`
- **执行解释器**：`E:\Anaconda\python.exe`
- **执行脚本**：`F:\LearningNotes\自进化智能体\scripts\fetch_hf_papers.py`
- **工作目录**：`F:\LearningNotes\自进化智能体`
- **启动策略**：错过计划时间后，系统可在下次可用时启动；单次最长运行 2 小时。

### 常用核验与手动控制

```powershell
# 查看任务状态（需要有权访问任务计划程序）
Get-ScheduledTask -TaskName 'SelfEvolvingAgents-DailyPapers'
Get-ScheduledTaskInfo -TaskName 'SelfEvolvingAgents-DailyPapers'

# 立即运行一次
Start-ScheduledTask -TaskName 'SelfEvolvingAgents-DailyPapers'

# 删除自动化任务
Unregister-ScheduledTask -TaskName 'SelfEvolvingAgents-DailyPapers' -Confirm:$false
```

### 配置过程中发现的问题与处理

- 用户给出的交接文档路径并不存在；实际文件是根目录下的 `00_DAILY_PAPERS_AGENT_HANDOVER.md`，已按真实文件读取。
- 原 README 记录的是每天 20:00，和本次要求冲突；已改为每天 10:00，避免文档与系统配置不一致。
- 当前 Codex 沙箱普通权限无法写入 Windows 任务计划程序；通过一次管理员授权完成任务注册。若任务被系统策略禁用，需要在 Windows“任务计划程序”中检查该任务的“历史记录”和“上次运行结果”。
