---
title: 自动 Benchmark 构建与开放词汇评测：相关工作与可复用机制
category: evaluation
kind: roadmap
organization: Embodied AI Map
releaseDate: 2026-09-20
summary: 按“自然语言意图 → 可验证 benchmark”链路梳理场景生成、任务生成、reward、任务规范、benchmark 自动化与评测基础设施六条线，重点核对 RoboLab、Isaac Lab-Arena、BenchForge、BenchClaw、GenManip、GIF、AnyTask、FATE 的覆盖与边界，给出可复用机制与风险清单。
tags: [evaluation, automated-benchmark, open-vocabulary, verifier, research-map]
draft: false
references:
  - title: RoboLab 论文
    url: https://arxiv.org/abs/2604.09860
  - title: RoboLab 官方仓库
    url: https://github.com/NVlabs/RoboLab
  - title: Embodied-BenchForge 论文
    url: https://arxiv.org/abs/2609.13082
  - title: Embodied-BenchClaw 论文
    url: https://arxiv.org/abs/2606.11909
  - title: Isaac Lab-Arena agentic environment generation
    url: https://isaac-sim.github.io/IsaacLab-Arena/release/0.3.0/pages/concepts/agentic_environment_generation/index.html
  - title: GENMANIP 论文
    url: https://openaccess.thecvf.com/content/CVPR2025/html/Gao_GENMANIP_LLM-driven_Simulation_for_Generalizable_Instruction-Following_Manipulation_CVPR_2025_paper.html
  - title: AnyTask 论文
    url: https://arxiv.org/abs/2512.17853
  - title: 自动构建综述
    url: https://arxiv.org/abs/2606.12207
---

## 1. 问题定义与验收标准

目标问题：用户只给一句任务意图（例如“测试机器人能不能用球杆把高尔夫球打进洞里”），系统能否自动生成**可执行、可验证、可调难度、可直接接入策略评测**的 benchmark。

先区分三种“变化”，它们的难度完全不同：

| 变化 | 内容 | 现状 |
|---|---|---|
| A 外观变化 | 颜色、材质、光照、相机、背景、物体位置 | domain randomization，已成熟 |
| B 结构变化 | 推拉门/折页门/双开门的关节拓扑、运动轴、把手 affordance、碰撞几何、动作路径 | 部分系统能做材质/风格变体，机构级变体仍靠人工 |
| C 语义变化 | “坐下并观看窗外事件”这类支撑接触 + 姿态稳定 + 视线区域 + 时间窗口的组合语义 | 现有谓词库基本无法表示 |

一个合格的 benchmark 要同时满足七项：valid（语义对得上要测的能力）、executable、solvable（存在可成功轨迹）、non-trivial（初始状态不是成功状态、随机策略不能完成）、verifiable（成功判定不误判）、discriminative（不同能力策略能拉开差距）、reproducible（版本/seed/资产可复现）。

两条贯穿全篇的技术立场：

1. **Training Reward ≠ Evaluation Verifier**：`r = −‖p_ball − p_hole‖ + λv` 这类训练 reward 很高，不代表“球进洞”的判定成立；判准必须落成 simulator-grounded 的 state / event / temporal 谓词（例如 `ball_center ∈ cup_volume ∧ z_ball < z_rim`）。
2. **Judge 与本体解耦**：成功判定只描述“物体与场景达到什么状态”，与驱动它的是 Panda、GR-1 还是 G1 无关——这也是本目录实测中官方 evaluator 可以跨本体复用的原因（见 §7）。

## 2. 六条线的工作地图

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

时间线：2023–2024 重点是“自动生成环境/任务/reward，用于训练”；2025 扩展到复杂任务、goal conditions 与大规模 demonstrations；2026 开始直接研究“自动 benchmark 构建/agentic benchmark authoring”。**目前的瓶颈集中在验证、任务本体扩展、度量有效性与难度校准。**

## 3. 重点系统核对

| 系统 | 定位 | 关键机制 | 规模 / 结果 | 边界 |
|---|---|---|---|---|
| **RoboLab**（NVIDIA，RSS 2026） | 最完整的同构系统：自然语言 → 场景 → 任务 → 判据 → 回放 | 场景计划 + 几何求解 + 物理校验三级生成；13 个空间关系谓词 + 6 个容纳/放置谓词 + LLM 选择；server-client 策略接口；SBI + MNPE 敏感性归因；每任务三档语言指令 | 312 个物体资产；RoboLab-120（120 个任务，visual / relational / procedural 三能力轴 × 三档难度）；π0.5 成功率 31.9%（论文 Table I，对应旧版 80 任务） | 判据仍受现有 predicate library 限制；rigid-body tabletop scenes，论文自述 deformable 与 contact-rich 不足；接入新本体要按 Isaac Lab 规范手写配置类 |
| **Embodied-BenchForge**（2026-09） | benchmark 构建闭环最完整 | artifact dependency graph + artifact-specific contract；前向合成 + 后向验证/修复（6 种修复算子，仅重跑受影响子图）；可执行 terminal-state verifier | Interactive track：220 任务 × 28 个 AI2-THOR 场景；GPT-5.5 83.18% / 人类 97.73%；Skill 复用率 91.6% | 仅 AI2-THOR 单模拟器；离散动作原语，无连续控制/自定义 URDF；无代码开源 |
| **Embodied-BenchClaw** | 同团队前作，三 agent + 五阶段流水线 | 预定义 stage-wise skill DAG（LLM 不自由生成 workflow）；过程验证 + 受影响子图修复 | 主要面向图像/多视角/simulator-state 的空间评测 | 原文明确：不做闭环机器人控制、触觉、力反馈 |
| **GENMANIP**（CVPR 2025） | 任务语义结构化最直接 | task-oriented scene graph 组织 instruction、objects、states/relations、goal conditions、demonstrations | 200-task benchmark | 语义扩展受已有 relation/skill 表示限制；保留 human-in-the-loop 修正 |
| **GIF**（2026-09） | 结构性变体最有启发 | 按**几何接触模式**（非语言表层）从 60 万条 Ego4D 人—物交互聚类出 8 类接触几何；每类 3 任务 × 5 语义变体 | 24 任务 × 5 变体 = 120 场景；碰撞率 < 1% | 变体是材质/风格级；成功判据与外部机器人接口不是主贡献 |
| **AnyTask**（2025-12） | 判据生成接口最适合复用 | 先生成 `check_success()`，再用它指导 `reset / compose_state / reward_function / scripted_policy` 四个函数保持一致 | 作者报告可运行率最高 96%（o3-mini + 改进 prompt） | 依赖已有 simulator API 与资产；代码可运行 ≠ 语义对齐 |
| **FATE**（2026-03） | 可行性审计 | 静态可达性/可供性/物理合理性/形态兼容性检查 + 主动修复 | 论文报告：无审计的端到端可行率仅 12.6% | 面向课程生成，不含评测协议 |
| **Isaac Lab-Arena 0.3** | 环境生成基建 | 自然语言 → EnvGraphSpec → 资产选择 → 空间关系求解 → 合法布局 | 模块化 scene/objects/embodiment/task/variations | agentic 生成当前限于标注 `@agent_ready` 的既有任务类型 |
| **MolmoSpaces**（2026-02） | 大规模开放场景生态 | LLM atomic checks；内置 joint + pose 双接口 | 2k scenes × 4 变体 | 本体不可替换 |
| **A2Eval**（2026-02） | 评测套件自动策展 | 从已有 benchmark 池自动挑选代表性 evaluation suite | — | 面向已有 benchmark 的筛选，不生成新任务语义 |

尚无任何系统同时满足：①接受极端开放的自然语言语义；②接受用户自带本体（上传 URDF 即用）；③自动产出可验证的 state/event/temporal 判据。RoboLab 覆盖 6 项能力中的 5 项，是组合上最接近的单一系统；BenchForge 的 artifact 验证闭环补齐了“构建后如何保证质量”；**开放词汇物理语义（strike / scoop / roll / hammer 等新 operator 的自动合成）仍然空缺。**

逐项能力对标（C1–C4 / O1–O2 需求清单、六项能力成熟度、端到端系统打分与 41 篇论文清单）见 [Open-Task Benchmark 能力框架与逐项对标](../open-task-benchmark/)。

## 4. 六个对照维度

核对每一篇工作时，按六问追踪：

| # | 维度 | 问题 | 现状最好的实现 |
|---|---|---|---|
| 1 | 语言 → 任务 | 能否从一句话得到可执行的任务定义 | RoboLab taskgen、GenManip、BenchForge |
| 2 | 物体 / 机构 | 是否生成或检索不同物体、关节结构与 affordance | GIF、MolmoSpaces、EmbodiedGen/Seed3D |
| 3 | 合理场景 | 是否检查碰撞、可达、稳定与 embodiment compatibility | RoboLab 三级校验、FATE 审计、STABLE |
| 4 | 结构性变体 | 换材质，还是改拓扑与运动约束 | GIF（语义变体）、RoboLab ξ=(camera, light, background, pose) |
| 5 | 成功程序 | 是否产出 state / event / temporal verifier | RoboLab 谓词组合、AnyTask check_success-first、BDDL |
| 6 | 闭环执行 | 是否真正跑 rollout、反例测试、诊断与修复 | RoboLab、BenchForge、AutoEval 集群队列 |

## 5. 风险与度量

| # | 风险 | 证据 |
|---|---|---|
| 1 | **复述脆弱性**：语义等价改写会让同一轨迹的成功判定翻转，且不能靠模型规模缓解 | ROBORMBENCH：2,390 条轨迹 + 21,673 条复述 |
| 2 | **成功 ≠ 遵从指令**：只看成功率做反馈，策略会“达成目标但不听指令” | RDA |
| 3 | **负例瓶颈**：真实语料以成功样本为主，判据假阳性偏高 | RoboReward；无单一 VLM 全任务最优 |
| 4 | **长时程平坦**：单 prompt 的 VLM reward 在轨迹大部分区域近乎平坦 | RMTL |
| 5 | **生成场景物理不可行** | FATE：无审计端到端可行率 12.6% |
| 6 | **成本转移**：自动化不消除成本，而是把成本转移到验证与治理 | 自动构建综述（CAAR 分级） |

自动构建系统自身也需要被度量。可用的指标组：**Executability**（能 reset/run 的比例）、**Semantic Correctness**（专家 rubric）、**Verifier Precision/Recall**（对人工标注 trace）、**Oracle Solvability**、**Non-triviality**（random/no-op 策略成功率应接近 0）、**Calibration Quality**（把难度调进目标区间，如 P(success) ∈ [0.2, 0.8]）、**Policy Discrimination**（跨策略方差 / IRT 区分度）、**Human Effort Reduction**（人工时间/LOC/debug 次数）、**Reproducibility**（跨机器/时间/adapter 的 evaluator 行为一致）。

难度校准的正确做法是 **evaluation-in-the-loop**：calibration 策略集先跑出难度分布 → 冻结 benchmark → 在 held-out 策略与 seed 上评测；calibration 与 test 必须分离，否则 benchmark 会过拟合到参赛模型。

## 6. 可复用机制清单

| # | 机制 | 出处 | 用途 |
|---|---|---|---|
| 1 | 谓词库 + LLM 选词组合（受控词表，非自由生成） | RoboLab | 判据可校验、可复现 |
| 2 | LLM 只做语义规划，几何由求解器校验，物理由仿真校验，失败反馈重生成 | RoboLab | 避免 LLM 直接输出坐标 |
| 3 | `check_success()` 先生成，其余四函数围绕它保持一致 | AnyTask | 判据与场景/奖励一致 |
| 4 | 可行性审计（静态四项检查 + 动态执行检查）+ 主动修复 | FATE | 生成场景物理可行 |
| 5 | 接触几何分类 → 任务模板 → 语义变体，三级展开 | GIF | “同一任务换物体/材质”的一等公民化 |
| 6 | 每任务多档语言指令（default / vague / specific） | RoboLab | 应对复述脆弱性 |
| 7 | server-client 策略架构（模型独立 server） | RoboLab / 本目录实测（见[方法部署记录](../../reproductions/policy-deployment-records/)） | 任何策略后端可接入评测 |
| 8 | 集群式任务队列 + 自动成功检测 + 自动场景重置 | AutoEval | 7×24 无人值守评测 |
| 9 | artifact 依赖图 + 局部修复（只重跑受影响子图） | BenchForge | 失败恢复的工程范式 |
| 10 | 结构化中间表示（Benchmark IR）替代自由生成 Python | FactorSim、RTSF | 任务本体可扩展、可静态校验 |

**最小 Benchmark IR** 的字段骨架（调研给出的提案，可直接作为设计参考）：`capability / embodiment_requirements / assets / initial_state_distribution / semantic_operators（state、event/contact、temporal）/ success（temporal formula）/ failure / metrics / validation 步骤 / calibration 参数`。核心不是格式本身，而是它**允许任务本体被扩展**，而不是假设所有 predicate 事先写好。

## 7. 与本仓库评测地图的关系

1. **接入现有 Benchmark 的工作仍然以人工适配为主**：自动构建系统的判据都建立在某个受控谓词库或固定动作语义之上；把方法落到 LIBERO/RoboCasa/SIMPLE 上，当前路径仍是“定死本体控制量契约 → 逐个 Benchmark 写适配”（依据见[复现实测总览](../../reproductions/overview/)与[本体与控制量图谱](../../guides/robot-action-audit/)）。
2. **开放词汇物理语义是全身人形评测的下一个缺口**：现有系统能组合 `Pick/Place/Open/Close`，但不能自动发明 `Strike`、`Scoop`、`Roll-through-gate` 这类接触/动力学 operator 并同步生成可执行的物理判据；本目录的全身任务（HumanoidBench、SIMPLE、Mimicking-Bench 等）也全部使用预定义任务集。
3. **可复用的最确定的两条**：判据与本体解耦（官方 evaluator 可直接沿用）；server-client 架构与结果登记 schema（本目录的[四档结果口径](../../reproductions/overview/)就是按此实践）。

研究侧如果要推进一步，建议的动作是：先把 RoboLab / Isaac Lab-Arena / BenchForge 的 task representation 与 verifier API 拆到代码级，确认它们能否新增一种此前不存在的动态交互 operator；再在 Isaac Lab 中手工实现 Strike / Hammer / Puck 三类任务，反推哪些代码与物理判据可以由 agent 自动生成。
