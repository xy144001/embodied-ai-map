---
title: Open-Task Benchmark：自动构建能力框架、系统对标与论文清单
category: evaluation
kind: roadmap
organization: Embodied AI Map
releaseDate: 2026-09-20
summary: 把“一句自然语言意图 → 可验证 benchmark”拆成 I1/I2 输入、C1–C4 自动能力与 O1/O2 输出，核对 RoboLab、BenchForge、BenchClaw、GenManip、GIF、AnyTask、FATE 等系统的成熟度与边界；附覆盖矩阵、四条判据路线、本体接入门槛、风险与度量、可复用机制、差异化定位与 41 篇论文清单。
tags: [evaluation, open-vocabulary, automated-benchmark, task-generation, verifier, research-map]
draft: false
references:
  - title: RoboLab 论文
    url: https://arxiv.org/abs/2604.09860
  - title: RoboLab 官方仓库
    url: https://github.com/NVlabs/RoboLab
  - title: Embodied-BenchForge 论文
    url: https://arxiv.org/abs/2609.13082
  - title: GIF 论文
    url: https://arxiv.org/abs/2609.05927
  - title: AnyTask 论文
    url: https://arxiv.org/abs/2512.17853
  - title: FATE 论文
    url: https://arxiv.org/abs/2603.01505
  - title: MolmoSpaces 论文
    url: https://arxiv.org/abs/2602.11337
---

## 1. 问题定义与验收标准

目标问题：用户只给一句任务意图（例如“测试机器人能不能用球杆把高尔夫球打进洞里”），系统能否自动生成**可执行、可验证、可调难度、可直接接入策略评测**的 benchmark。

三种“变化”的难度完全不同：

| 变化 | 内容 | 现状 |
|---|---|---|
| A 外观变化 | 颜色、材质、光照、相机、背景、物体位置 | domain randomization，已成熟 |
| B 结构变化 | 推拉门/折页门/双开门的关节拓扑、运动轴、把手 affordance、碰撞几何、动作路径 | 材质/风格变体已可自动；机构级变体仍靠人工 |
| C 语义变化 | “坐下并观看窗外事件”这类支撑接触 + 姿态稳定 + 视线区域 + 时间窗口 | 现有谓词库基本无法表示 |

合格的 benchmark 需同时满足七项：valid、executable、solvable、non-trivial、verifiable、discriminative、reproducible。两条贯穿全篇的技术立场：

1. **Training Reward ≠ Evaluation Verifier**：训练 reward 高不代表“球进洞”判定成立；判准必须落成 simulator-grounded 的 state / event / temporal 谓词（如 `ball_center ∈ cup_volume ∧ z_ball < z_rim`）。
2. **判据与本体解耦**：成功判定只描述“物体与场景达到什么状态”，与驱动它的是 Panda、GR-1 还是 G1 无关——这也是本目录实测中官方 evaluator 可跨本体复用的原因（见[复现实测总览](../../reproductions/overview/)）。

## 2. 需求拆解：I1/I2 → C1–C4 → O1/O2

| 编号 | 内容 | 例子 |
|---|---|---|
| I1 | 任务需求（自然语言） | “把水杯放到雕像上” / “坐在椅子上观看窗外事件” |
| I2 | 机器人素材 | 本体 URDF + 控制协议约定 |
| C1 | 场景创建·物体 | 根据 task 自动决定用哪些物体 |
| C2 | 场景创建·物体关系 | 自动决定物体之间的空间/接触关系 |
| C3 | 成功判断标准 | 自动给出可执行、可计算的成败判定 |
| C4 | 机器人控制接口 | 让策略能在场景里真的动起来 |
| O1 | 同一 task 多情况成功率 | 木门 80% / 玻璃门 60% / 双开门 45% |
| O2 | 对应回放 | 每个 episode 的视频 |

三个隐藏难点：**I1 开放度极高**（“观看某事件”无法用几何谓词直接表达）；**I2 要求接受外来本体**（URDF 解析、运动学映射、控制协议适配，比“内置多个机器人”难一个量级）；**O1 要求变体生成机制**（木门/玻璃门/双开门），而不是简单域随机化。

### 六项能力成熟度与三个关键判断

| 能力 | 有人做吗 | 最佳实现 | 做到什么程度 |
|---|---|---|---|
| C1 物体 | ✅ 成熟 | RoboLab scenegen、MolmoSpaces、GIF | 已可从自然语言生成桌面场景；RoboLab 物体库 312 个 |
| C2 关系 | ✅ 成熟 | RoboLab 谓词库、GIF 接触几何 | RoboLab 有 13 个空间关系谓词；GIF 归纳出 8 类接触几何 |
| C3 判据 | 🟡 部分成熟 | RoboLab、AnyTask、BenchForge | “谓词库 + LLM 自动选择”已可用；开放语义任务仍脆弱 |
| C4 控制接口 | 🟡 部分 | RoboLab “Bring your own robot” | 支持任意 IsaacLab 兼容本体，但需手写配置类 |
| O1 多情况成功率 | ✅ 有 | RoboLab 敏感性分析、Colosseum V2 | 已能定量回答“哪个因子最强影响成败” |
| O2 回放 | ✅ 有 | RoboLab dashboard | 内置 web dashboard：回放 episode + 跨实验对比 |

1. **没有一项能力完全空白**（4 项成熟、2 项部分）→ 不能靠“填补空白”立论，要靠组合方式 + 易用性差异化。
2. **没有任何系统同时满足 I1 的任意性与 I2 的外部本体要求**：RoboLab 能接任意 IsaacLab 本体但要求会写配置类；BenchForge / BenchClaw 完全不接受外来本体。
3. **最接近的是 RoboLab**：六项覆盖 5 项，是唯一同时具备（自动场景 + 自动判据 + 多本体 + 变体归因 + 回放）的单一系统。

## 3. 领域工作地图

```text
                     Natural Language / User Intent
                                │
        ┌───────────────────────┼────────────────────────┐
        ▼                       ▼                        ▼
  场景 / 资产生成          任务生成                  Reward 生成
  Holodeck, ReGen,        GenSim, RoboGen,          Eureka,
  ClutterGen, STABLE      GenSim2, GenManip          Text2Reward
        │                       │                        │
        └───────────┬───────────┴────────────┬───────────┘
                    ▼                        ▼
           任务规范与验证              Benchmark 自动化
       BDDL, CodeBotler/RoboEval,   RoboLab, Isaac Lab-Arena,
       RTSF                         BenchClaw, BenchForge, A2Eval
                    │                        │
                    └───────────┬────────────┘
                                ▼
                     评测基础设施
        Inspect Robots / WorldEvals, XPolicyLab, RoboDojo
```

2023–2024 重点在“自动生成环境/任务/reward，用于训练”；2025 扩展到复杂任务与 goal conditions；2026 开始直接研究“自动 benchmark 构建 / agentic benchmark authoring”。**当前瓶颈集中在验证、任务本体扩展、度量有效性与难度校准。**

## 4. 系统对标与逐项机制

### 4.1 六项能力覆盖矩阵

| 系统 | C1 物体 | C2 关系 | C3 判据 | C4 控制接口 | O1 变体成功率 | O2 回放 |
|---|---|---|---|---|---|---|
| **RoboLab** | ✅ | ✅ 13 谓词 | ✅ 谓词库+LLM | 🟡 任意 IsaacLab 本体（需写配置） | ✅ SBI 敏感性 | ✅ dashboard |
| BenchForge | 🟡 固定 pool | 🟡 PDDL 语义 | ✅ 可执行 verifier | 🟡 AI2-THOR 原语 | ✅ 220×28 | ✅ 评测报告 |
| BenchClaw | 🟡 复用 | ✅ 语义层 | ✅ scoring protocol | ❌ 明确不做 | 🟡 | 🟡 |
| MolmoSpaces | ✅ | ✅ | ✅ LLM atomic checks | 🟡 内置双接口 | ✅ 2k×4 | ✅ |
| GIF | ✅ | ✅ 8 类 | 🟡 人工定义 | 🟡 | ✅ 24×5 | 🟡 |
| AnyTask | ✅ | 🟡 | ✅ check_success() | ✅ skill API | 🟡 | 🟡 |
| FATE | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | — |
| STABLE | ✅ | — | — | — | — | — |
| TabletopGen | ✅ | 🟡 | 🟡 | 🟡 | 🟡 | — |
| **目标形态** | 自动 | 自动（几何级） | 自动 | **用户自带 URDF** | 多情况 + 归因 | 回放 |

读法：没有任何一行全绿；**RoboLab 是绿格最多的一行**，且唯一同时具备变体归因与回放 dashboard。

构建闭环方向另可参考：**BenchForge** 用 artifact 依赖图 + artifact-specific contract + 6 种修复算子（只重跑受影响子图）把构建做成可维护流程，Interactive track 达 220 任务 × 28 个 AI2-THOR 场景（GPT-5.5 83.18% / 人类 97.73%），但限于单模拟器离散原语且无开源；**BenchClaw** 以三 agent + 预定义 skill DAG 做过程质控，原文明确不做闭环机器人控制；**GenManip** 用 task-oriented scene graph 显式组织 goal conditions（200-task），语义扩展受已有 relation/skill 表示限制；**A2Eval** 从已有 benchmark 池策展评测套件，不生成新任务语义。

### 4.2 C1 场景创建：四代谱系与三级校验

| 代际 | 代表 | 做法 |
|---|---|---|
| 一代：程序化生成 | ProcTHOR | 规则驱动，场景图 + 模板；语义贫乏 |
| 二代：数据驱动资产 | RoboCasa、BEHAVIOR-1K | 人工建模资产库 + 规则布局 |
| 三代：LLM 生成 | RoboLab、MolmoSpaces、STABLE、TabletopGen | LLM 出计划 → 几何求解 → 物理校验 |
| 四代：生成式 3D | EmbodiedGen、Seed3D、MetaScenes | 图像/文本直接生成仿真就绪资产 |

RoboLab 三级校验（可直接复用）：LLM 生成结构化场景计划（物体目录 + 尺寸 + 主题）→ 空间求解器把关系谓词编译成合法位姿（按依赖顺序，先支撑面后其上物体）→ Isaac Sim 重力前向仿真 300 步校验稳定性（最大位移 > 0.02 m 即视为不稳定）→ 错误文本反馈重新规划。关键分工：**LLM 只做语义规划，几何与物理由确定性求解器/仿真器校验**，避免 LLM 直接输出坐标。

其他可借鉴：ClutterGen（物理合规的杂乱场景）、AgentWorld（布局 + 语义标注 + 移动操作）、ForeRobo（3D 目标驱动的海量仿真数据）。RoboLab 物体库构成（312 个）：vomp 196 / hope 27 / hot3d 25 / ycb 22 / handal 19 / objaverse 10 / fruits 9 / basic 4。

### 4.3 C2 物体关系：两套互补范式

**谓词库 + 求解（RoboLab）**：13 个空间关系谓词（`left_of`/`right_of`、`in_front_of`/`behind`、`above`/`below`/`below_top`/`on_bottom`、`on_center`、`next_to`、`between`、`at`、`objects_in_line`）+ 6 个容纳/放置谓词（`in_container`、`on_top`、`enclosed`、`inside`、`outside_of`、`outside_of_and_on_surface`）；参考系可选（robot / world），通用参数统一（`logical` = all/any/choose K、`require_contact_with`、`require_gripper_detached`、`tolerance`）。优点：精确、可参数化、可求解。

**从数据归纳（GIF）**：从 Ego4D 约 60 万条人—物交互按**几何接触模式**聚类出 8 类：Containment 容纳、Capping 加盖、Resting 静置、Leaning 倚靠、Hooking 悬挂、Slotting 插入槽位、Spanning 跨越、Pegging 销接。优点：覆盖真实人类行为分布；局限：粒度粗、难参数化。

选用：两者结合——GIF 路线产出关系分类，RoboLab 路线产出可执行谓词。方法论要点：必须按几何接触模式聚类，否则“放到/放在/置于”会被当成三种不同关系。

### 4.4 C3 成功判据：四条技术路线

| 路线 | 代表 | 判据载体 | 自动性 | 主要弱点 |
|---|---|---|---|---|
| A. VLM 直接查询/打分 | SuccessVQA、T²-VLM | VQA / 分数 | 中（多需微调） | 复述脆弱、in-the-wild 失败 |
| B. 概率/价值探针（免训练） | TOPReward、GVL、RoboCLIP | token 概率 / 价值 / 相似度 | 高 | 需 logits 访问；进展标定 |
| C. LLM 生成代码/参数 | Eureka、Text2Reward、LARG、AnyTask | 可执行代码 | 高 | 需仿真在环；成功率 ≠ 指令对齐 |
| D. 训练专用判别器 | Eval-Actions、RoboReward | 分类器 / 评估器 | 低（需标注） | 人工标注成本、闭集 |

RoboLab 的实现是当前最完整的工程解：LLM 被喂入场景物体目录、任务范例、完整谓词库、能力轴模板与难度约束 → 生成任务代码 → 语法/资产校验 → 失败精炼；禁止引用不存在的物体，从**受控词表**选词因而天然可校验、可复现。AnyTask 则先生成 `check_success()`，再让 `reset / compose_state / reward_function / scripted_policy` 围绕它保持一致（作者报告可运行率最高 96%）。

### 4.5 C4 控制接口：离“上传 URDF 即用”还有多远

| 系统 | 支持本体 | 外部 URDF | 门槛 |
|---|---|---|---|
| RoboLab | 任意 IsaacLab 兼容机器人 | 🟡 部分 | 需手写 Python 配置类：`ArticulationCfg`、`ee_recorder_bodies`、`table_fixture`、`root_z_above_ground`、动作/观测/夹爪配置 |
| MolmoSpaces | 内置（joint + pose 双接口） | ❌ | 不可换 |
| BenchForge | AI2-THOR 离散原语 | ❌ | 不可换 |
| BenchClaw | 无控制接口 | ❌ | — |
| RoboCasa / ManiSkill / LIBERO / BEHAVIOR-1K | 固定（Franka、R1 等） | ❌ | 不可换 |

RoboLab 官方 NOTE 写明“创建新机器人与在 IsaacLab 中创建完全相同”——**这正是机会所在：把“接入新本体”从写代码做成上传向导。** 内置本体可作输出形态参考：DROID / Franka Panda 并列提供 joint position、absolute EE IK、relative EE IK 三种动作空间（8 / 8 / 7 维），Kinova Gen3 提供 joint position。

参考技术：跨本体动作空间（Unify Robot Actions in Camera Frame 2511.17001、One-Policy-Fits-All 2603.14522、Universal Actions 2501.10105、Unified Hand Action Space 2607.03570）；URDF/机构处理（URDFormer 2405.11656、URDF-Anything 2511.00940、SPARK 2512.01629、LLM-Guided Robot Ontology from URDF 2606.17073）。推荐路线：URDF 解析（关节类型/限位/连杆树）→ 统一动作空间映射（末端位姿/相机系）→ 仿真器 IK → 并列输出 joint + pose 双接口 → 控制协议适配层。

### 4.6 O1 变体生成：四代演进

| 代际 | 代表 | 机制 | 局限 |
|---|---|---|---|
| 一代：固定任务集 | LIBERO、ManiSkill2 | 预设任务 + 固定场景 | 无变体概念 |
| 二代：域随机化 | ManiSkill3、RoboCasa | 随机化位姿/光照/材质 | 随机但不解释“为什么” |
| 三代：语义变体 | GIF、MolmoSpaces | 保持任务关系，改材质/颜色/子风格 | 变体轴人工指定 |
| 四代：因子敏感性归因 | RoboLab SBI+MNPE、Colosseum V2 | 定量回答“哪个因子最强影响成败” | 需大量 rollout |

GIF 三级展开：8 类接触几何 → 每类 3 个代表任务 → 每任务 5 个语义变体 = 24 × 5 = 120 场景。RoboLab：θ = (θ_cont, θ_disc)，用 MNPE 近似后验 p(θ|x)，把输出从“成功率是多少”升级为“**材质/相机/光照/位姿中哪个因素最强影响成败**”；变化向量 ξ = (camera, light, background, pose)。语言变体：每任务三档指令（default / vague / specific），是应对复述脆弱性的现成方案。

### 4.7 O2 回放与自动化评测

RoboLab 内置自包含 web dashboard（浏览场景/任务、回放 episode、跨实验对比、env_cfg.json 可复现回合）；BenchForge 在 Evaluation Reporting 阶段产出评测报告；AutoEval（2503.24278）提供集群式任务队列 + 自动成功检测 + 自动场景重置，可 7×24 无人值守；ManiSkill3 的 GPU 并行渲染是回放基础设施。RoboLab 的 server-client 架构（模型独立 server + 轻量 client）让任何策略后端都能接入——与“用户自带机器人素材”的思路同构。

## 5. 风险与度量

| # | 风险 | 证据 |
|---|---|---|
| 1 | **复述脆弱性**：语义等价改写会让同一轨迹的成功判定翻转，不能靠模型规模缓解 | ROBORMBENCH：2,390 条轨迹 / 21,673 条复述 |
| 2 | **成功 ≠ 遵从指令**：只看成功率做反馈，策略会“达成目标但不听指令” | RDA |
| 3 | **负例瓶颈**：真实语料以成功样本为主，判据假阳性偏高 | RoboReward；无单一 VLM 全任务最优 |
| 4 | **长时程平坦**：单 prompt 的 VLM reward 在轨迹大部分区域近乎平坦 | RMTL |
| 5 | **生成场景物理不可行** | FATE：无审计端到端可行率仅 12.6% |
| 6 | **成本转移**：自动化把成本转移到验证与治理，而非消除成本 | 自动构建综述（CAAR 分级） |

自动构建系统自身也需要被度量：Executability（能 reset/run 的比例）、Semantic Correctness（专家 rubric）、**Verifier Precision/Recall**（对人工标注 trace）、Oracle Solvability、Non-triviality（random/no-op 策略成功率应接近 0）、Calibration Quality（难度调进目标区间如 P(success) ∈ [0.2, 0.8]）、Policy Discrimination（跨策略方差 / IRT）、Human Effort Reduction、Reproducibility。

难度校准的正确做法是 **evaluation-in-the-loop**：calibration 策略集先跑出难度分布 → 冻结 benchmark → 在 held-out 策略与 seed 上评测；calibration 与 test 必须分离，否则 benchmark 会过拟合参赛模型。

## 6. 可复用机制与 Benchmark IR

| # | 机制 | 出处 | 用途 |
|---|---|---|---|
| 1 | 谓词库 + LLM 选词组合（受控词表，非自由生成） | RoboLab | 判据可校验、可复现 |
| 2 | LLM 只做语义规划，几何由求解器校验、物理由仿真校验，失败反馈重生成 | RoboLab | 避免 LLM 直接输出坐标 |
| 3 | `check_success()` 先生成，其余四函数围绕它保持一致 | AnyTask | 判据与场景/奖励一致 |
| 4 | 可行性审计（静态四项检查 + 动态执行检查）+ 主动修复 | FATE | 生成场景物理可行 |
| 5 | 接触几何分类 → 任务模板 → 语义变体，三级展开 | GIF | “同一任务换物体/材质”一等公民化 |
| 6 | 每任务多档语言指令（default / vague / specific） | RoboLab | 应对复述脆弱性 |
| 7 | server-client 策略架构（模型独立 server） | RoboLab / 本目录实测 | 任何策略后端可接入评测 |
| 8 | 集群式任务队列 + 自动成功检测 + 自动场景重置 | AutoEval | 7×24 无人值守评测 |
| 9 | artifact 依赖图 + 局部修复（只重跑受影响子图） | BenchForge | 失败恢复的工程范式 |
| 10 | 结构化中间表示（Benchmark IR）替代自由生成 Python | FactorSim、RTSF | 任务本体可扩展、可静态校验 |

最小 Benchmark IR 字段骨架：`capability / embodiment_requirements / assets / initial_state_distribution / semantic_operators（state、event/contact、temporal）/ success（temporal formula）/ failure / metrics / validation 步骤 / calibration 参数`。核心不是格式本身，而是它**允许任务本体被扩展**，而不是假设所有 predicate 事先写好。

## 7. 差异化定位与实施顺序

三条护城河（按可信度排序）：

1. **本体接入的易用性**：把“会写 IsaacLab 配置类”降到“上传 URDF + 声明控制协议”。这是易用性差异化而非能力空白，需靠第二、三条加固。
2. **RoboLab 明确未覆盖的场景类型**（论文自述）：可形变物体（cloth / cables / bags）、接触密集/力控任务、桌面级以外的房间级布局。
3. **判据的鲁棒性与可审计性**：复述不变性、指令对齐度作为一等指标；判据独立验证、不做自评估；记录 provenance（哪个 LLM、什么 prompt、什么版本）。

建议输出形态（成功率之外）：变体成功率 + 因子敏感性归因 + 复述稳定性（“5 种表述下判据一致性 92%”）+ 指令对齐度 + 每 episode 回放与可复现配置。

实施顺序：① 判据地基（受控谓词词表）→ ② 场景可靠性（三级校验 + FATE 式审计）→ ③ 本体接入（URDF → 统一动作空间 → 双接口）→ ④ 变体与归因 → ⑤ 输出层（成功率 + 归因 + 复述稳定性 + 对齐度 + 回放）。

## 8. 论文清单（41 篇 + 补充引用）

> 汇总日期 2026-09-18；论文编号经 arXiv API 逐一验证。

### A 类 · 基准自动构建 / 任务生成（10 篇）

| 编号 | 论文 | arXiv | 日期 |
|---|---|---|---|
| A01 | Embodied-BenchForge: A Closed-Loop Agentic Workflow for Embodied Benchmark Construction | 2609.13082 | 2026-09-11 |
| A02 | Embodied-BenchClaw: An Autonomous Multi-Agent System for Embodied Spatial Intelligence Benchmark Construction | 2606.11909 | 2026-06-10 |
| A03 | Intelligent Automation for Embodied Benchmark Construction: Pipelines, Embodiments, Simulators, and Trends | 2606.12207 | 2026-06-10 |
| A04 | GIF: Agentic Generation of Interactive and Functional Object Compositions for Robot Learning | 2609.05927 | 2026-09-05 |
| A05 | AnyTask: an Automated Task and Data Generation Framework for Advancing Sim-to-Real Policy Learning | 2512.17853 | 2025-12-19 |
| A06 | FATE: Closed-Loop Feasibility-Aware Task Generation with Active Repair for Physically Grounded Robotic Curricula | 2603.01505 | 2026-03-02 |
| A07 | MolmoSpaces: A Large-Scale Open Ecosystem for Robot Navigation and Manipulation | 2602.11337 | 2026-02-11 |
| A08 | TabletopGen: Tabletop Scene Generation and Interactive Simulation for Robotic Manipulation | 2512.01204 | 2025-12-01 |
| A09 | STABLE: Simulation-Ready Tabletop Layout Generation via a Semantics-Physics Dual System | 2605.16137 | 2026-05-15 |
| A10 | RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies（NVIDIA） | 2604.09860 | 2026-04-10 |

### B 类 · 自动成功判据 / Auto-Reward（9 篇）

| 编号 | 论文 | arXiv | 日期 | 判据范式 |
|---|---|---|---|---|
| B01 | Vision-Language Models as Success Detectors | 2303.07280 | 2023-03-13 | VLM VQA |
| B02 | Improving Robot Success Detection using Static Object Data | 1904.01650 | 2019-04-02 | 训练分类器 |
| B03 | Eval-Actions: Fine-Grained Execution Quality Evaluation for Robotic Manipulation | 2601.18723 | 2026-01-26 | 多模态评估器 |
| B04 | TOPReward: Token Probabilities as Hidden Zero-Shot Rewards for Robotics | 2602.19313 | 2026-02-22 | Token 概率探针 |
| B05 | Self-Refined Large Language Model as Automated Reward Function Designer for DRL in Robotics | 2309.06687 | 2023-09-13 | 可执行 reward code |
| B06 | LARG: Language-based Automatic Reward and Goal Generation | 2306.10985 | 2023-06-19 | 可执行 reward+goal |
| B07 | Learning Reward for Robot Skills Using Large Language Models via Self-Alignment | 2405.07162 | 2024-05-12 | LLM 提议 + 自对齐 |
| B08 | RoboCLIP: One Demonstration is Enough to Learn Robot Policies | 2310.07899 | 2023-10-11 | VLM 相似度 |
| B09 | Vision Language Models are In-Context Value Learners | 2411.04549 | 2024-11-07 | 轨迹价值函数 |

### C 类 · 场景 / 资产生成（9 篇）

| 编号 | 论文 | arXiv | 日期 |
|---|---|---|---|
| C01 | URDFormer: A Pipeline for Constructing Articulated Simulation Environments from Real-World Images | 2405.11656 | 2024-05-19 |
| C02 | ClutterGen: A Cluttered Scene Generator for Robot Learning | 2407.05425 | 2024-07-07 |
| C03 | AgentWorld: An Interactive Simulation Platform for Scene Construction and Mobile Robotic Manipulation | 2508.07770 | 2025-08-11 |
| C04 | EmbodiedGen: Towards a Generative 3D World Engine for Embodied Intelligence | 2506.10600 | 2025-06-12 |
| C05 | FetchMan: Learning Visual Humanoid Loco-Manipulation Policies from Simulated Experiences | 2608.17027 | 2026-08-17 |
| C06 | MetaScenes: Towards Automated Replica Creation for Real-world 3D Scans | 2505.02388 | 2025-05-05 |
| C07 | MarketGen: A Scalable Simulation Platform with Auto-Generated Embodied Supermarket Environments | 2511.21161 | 2025-11-26 |
| C08 | ForeRobo: Unlocking Infinite Simulation Data for 3D Goal-driven Robotic Manipulation | 2511.04381 | 2025-11-06 |
| C09 | Seed3D 1.0: From Images to High-Fidelity Simulation-Ready 3D Assets | 2510.19944 | 2025-10-22 |

### D 类 · 评测基准套件与元批判（13 篇）

| 编号 | 论文 | arXiv | 日期 |
|---|---|---|---|
| D01 | RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots | 2406.02523 | 2024-06-04 |
| D02 | BEHAVIOR-1K: A Human-Centered, Embodied AI Benchmark with 1,000 Everyday Activities | 2403.09227 | 2024-03-14 |
| D03 | RoboDojo: A Unified Sim-and-Real Benchmark for Generalist Robot Manipulation Policies | 2607.04434 | 2026-07-05 |
| D04 | What Are We Actually Benchmarking in Robot Manipulation? | 2606.04233 | 2026-06-02 |
| D05 | Colosseum V2: Benchmarking Generalization for Vision-Language-Action Models | 2605.27759 | 2026-05-26 |
| D06 | ManiSkill3: GPU Parallelized Robotics Simulation and Rendering | 2410.00425 | 2024-10-01 |
| D07 | ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills | 2302.04659 | 2023-02-09 |
| D08 | LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning | 2306.03310 | 2023-06-05 |
| D09 | ProcTHOR: Large-Scale Embodied AI Using Procedural Generation | 2206.06994 | 2022-06-14 |
| D10 | Mini-BEHAVIOR: A Procedurally Generated Benchmark for Long-horizon Decision-Making | 2310.01824 | 2023-10-03 |
| D11 | CleanUpBench: Embodied Sweeping and Grasping Benchmark | 2508.05543 | 2025-08-07 |
| D12 | Embodied Agent Interface: Benchmarking LLMs for Embodied Decision Making | 2410.07166 | 2024-10-09 |
| D13 | FMB: a Functional Manipulation Benchmark for Generalizable Robotic Learning | 2401.08553 | 2024-01-16 |

### 补充引用（正文提及）

| 论文 | arXiv | 用途 |
|---|---|---|
| ROBORMBENCH: Same Trajectory, Contradictory Rewards | 2609.05401 | 复述脆弱性基准 |
| RoboReward: General-Purpose Vision-Language Reward Models for Robotics | 2601.00675 | 负例瓶颈诊断 |
| AutoEval: Autonomous Evaluation of Generalist Robot Policies | 2503.24278 | 7×24 无人值守评测 |
| Eureka: Human-Level Reward Design via Coding LLMs | 2310.12931 | reward-code 路线 |
| Text2Reward: Reward Shaping with Language Models for RL | 2309.11489 | data-free 可执行 reward 代码 |
| RDA: Reward Design Agent for RL | 2606.01672 | 成功 ≠ 遵从指令 |
| RMTL | 2606.26175 | 长时程平坦问题 |
| Unify Robot Actions in Camera Frame | 2511.17001 | 跨本体统一动作空间 |
| One-Policy-Fits-All: Geometry-Aware Action Latents | 2603.14522 | 几何感知动作隐空间 |
| Universal Actions for Enhanced Embodied Foundation Models | 2501.10105 | 通用动作表示 |
| Cross-Embodiment via a Unified Hand Action Space | 2607.03570 | 统一手部动作空间 |
| URDF-Anything | 2511.00940 | 关节物体 URDF 构建 |
| SPARK: Sim-ready Part-level Articulated Reconstruction | 2512.01629 | 仿真就绪关节重建 |
| Extracting Semantics: LLM-Guided Automatic Population of Robot Ontology from URDF | 2606.17073 | 从 URDF 自动提取本体语义 |

## 9. 调研方法与可信度说明

- **检索方式**：arXiv API（须 HTTPS + curl 传输，HTTP 返回 406），8 组主题查询、约 350 条结果，全部使用一手元数据。
- **全文核验**：RoboLab / BenchForge / BenchClaw / 综述 / GIF / AnyTask / FATE / MolmoSpaces 等获取 HTML 全文（含附录）逐段核对；RoboLab 同时核对 GitHub 仓库（README、`docs/robots.md`、taskgen/scenegen skills、`references/conditionals.md`）。
- **已知局限**：未获取全部论文全文，个别边界为合理推断（正文已标注）；会议录用状态以 arXiv comment 字段为准；检索盲区——初期仅用关键词检索曾遗漏 RoboLab（标题措辞为 high-fidelity simulation benchmark / task generalist policies），教训是须补充“已知系统名”的定向核查；“LARM / Language Model Rewards”经多轮检索无法在 arXiv 核实，不建议引用。
- 本目录所在环境的 arXiv 索引已推进至 2026 年 9 月，26xx 号段论文均经 API 逐一验证。

## 10. 与本目录的关系

1. **接入现有 Benchmark 仍以人工适配为主**：自动构建系统的判据都建立在受控谓词库或固定动作语义之上；把方法落到 LIBERO/RoboCasa/SIMPLE 上，当前路径仍是“定死本体控制量契约 → 逐个 Benchmark 写适配”（依据见[复现实测总览](../../reproductions/overview/)与[本体与控制量图谱](../../guides/robot-action-audit/)）。
2. **开放词汇物理语义是全身人形评测的下一个缺口**：现有系统能组合 `Pick/Place/Open/Close`，但不能自动发明 `Strike`、`Scoop`、`Roll-through-gate` 这类接触/动力学 operator；本目录的全身任务也全部使用预定义任务集。
3. **最确定的两条复用**：判据与本体解耦（官方 evaluator 可直接沿用）；server-client 架构与结果登记 schema（本目录[四档结果口径](../../reproductions/overview/)即按此实践）。
