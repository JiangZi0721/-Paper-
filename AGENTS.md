# 自进化智能体工作区永久 Agent 规范 (Workspace AGENTS.md)

本文件是当前工作区（`f:\LearningNotes\自进化智能体`）的全局最高执行准则，适用于本工作区的所有会话、所有子智能体（Agents）及自动化脚本。

---

## 🚨 核心漏洞防范铁律：彻底杜绝“伪配额制”与“模板偏置漏洞” (Anti-Quota Fallacy & Zero-Slot Bias)

针对此前会话中反复出现的“每次基本固定输出 6 篇核心 + 2~3 篇旁支”的恶性认知惯性，所有 Agent 在处理文献追踪、科研分诊与报告生成时，必须绝对恪守以下三条铁律：

### 1. 绝对零配额铁律 (Zero Quota-Filling / Absolute Dynamic Count)
- **严禁心理锚定**：严禁受历史索引中“精选 6 篇核心 + 2 篇关键前沿”模板的先验误导，绝对禁止潜意识中以“凑齐 6 篇”为目标进行筛选；
- **纯动态事实驱动**：当天抓取的论文池中，有几篇真正符合底层闭环自进化，就客观收录几篇（可以有 1 篇、5 篇、12 篇，也可以是 0 篇）；
- **严禁削足适履**：
  - 绝对禁止为了凑齐卡槽把单点微调工具补丁（如 AutoCompact）或经院统计包装（如 CMP）硬抬为“核心”；
  - 绝对禁止为了控制篇幅而强行压制、隐瞒或折叠已经通过严苛筛选的真实前沿突破。

### 2. 严禁大容积默认兜底 (No Greedy Default Fall-through / Anti-Adjacent Dumping)
- **严禁无脑归入相邻**：严禁在分类代码或推理时，将未被黑名单剔除的普通论文无脑划入 `adjacent_inspiration`；
- **精细化多级漏斗**：
  - 凡是缺乏环境交互闭环、无自演化更新准则、无确定性 Verifier 的常规单轮问答、纯文本微调、普通多模态视频/图像模型、常规具身遥操作或经院统计计量包装，一律无情判定为 `not_recommended`；
  - `adjacent_inspiration` 仅限具备直接技术启发的外围关键基座（如真实可执行安全沙盒、奖励作弊评估基准、模型边界动作验证）。

### 3. 全景客观事实账本 (Objective Spectrum Integrity)
- 每次汇报前必须首先交代当前真实数据池底数（总候选篇数、初筛淘汰篇数、核心突破篇数、紧密周边篇数），保持学术透明。

---

## ⚔️ Jev Plus v1.3 三大一票否决铁律 (Three Absolute Veto Rules)

1. **Veto 1: 无闭环演进动力学，一票否决 (No Closed-Loop Evolution, Reject)**
   - 严禁收录“单纯给 Agent 加了个新工具/新动作做单次微调”的常规工程补丁（如 AutoCompact 类微调，缺少递归自演化闭环，顶多算局部组件）；
   - 核心自进化必须具备系统级递归闭环（Recursive Self-Improvement / Co-Evolution / Harness Auto-Evolution / Environment Synthesis）。
2. **Veto 2: 经院派因果/统计学学术灌水硬排除 (Causal/Statistical Academic Bloat Exclusion)**
   - 坚决一票否决一切打着 Causal/Counterfactual/Econometric 旗号、实质仅是外挂式静态概率采样与纯数学包装（如 CMP 类的 Hájek IPW 检索插槽轮播）的经院派灌水论文。样本复杂度荒谬、落地需数万轮对话且无法泛化者直接 `not_recommended`。
3. **Veto 3: 系统级元设计压倒单点微观调优 (System-Level Meta-Design)**
   - 聚焦脚手架代码自演化（如 MILO）、实例自适应动态打补丁（如 Turbo Harness）、训练课程双闭环共演（如 ActiveSaddler）、知识文献驱动进化（如 ScholarEvolve）与认知解构机制（如 OASIS 拆解特权鸿沟、LSD 对冲长度税、On-Policy vs Off-Policy 解耦）。

---

## 📝 笔记与知识库增量写入铁律 (Strict Incremental Append & Zero-Shrinkage)
1. **彻底放弃全量覆写**：严禁使用全量覆盖模式替换已有笔记，必须采用物理末尾增量追加；
2. **绝对禁止删除与压缩历史内容**：严禁对用户手写笔记、推导细节、代码示例进行精简或吞并，100% 保持只读与原样留存；
3. **以深度、定性、机理解构优先**：杜绝无意义的分数堆砌，彻底穿透数学机理与系统本质。
