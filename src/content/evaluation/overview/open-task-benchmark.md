---
title: Open-Task Benchmark：自动构建能力框架、逐项对标与论文清单
category: evaluation
kind: roadmap
organization: Embodied AI Map
releaseDate: 2026-09-18
summary: 把“用户给一句任务需求 → 系统自动产出可执行评测”拆成 I1/I2 输入、C1–C4 自动能力与 O1/O2 输出，逐项对照文献的实现程度、两套物体关系范式、四条成功判据路线与本体接入门槛；附端到端系统对标、差异化定位、实施顺序与 41 篇论文清单。
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

## 1. 需求拆解：把“自动做评测”写成可核对的清单

### 1.1 系统输入

| 编号 | 输入 | 例子 |
|---|---|---|
| I1 | 任务需求（自然语言） | “把水杯放到雕像上” / “开门” / “坐在椅子上观看窗外事件” |
| I2 | 机器人素材 | 本体 URDF + 控制协议约定 |

### 1.2 需要自动完成的四项能力

| 编号 | 能力 | 具体含义 |
|---|---|---|
| C1 | 场景创建·物体 | 根据 task 自动决定用哪些物体 |
| C2 | 场景创建·物体关系 | 自动决定物体之间的空间/接触关系（“杯子在雕像上”） |
| C3 | 成功判断标准 | 自动给出可执行、可计算的成败判定 |
| C4 | 机器人控制接口 | 让策略能在这个场景里真的动起来 |

### 1.3 系统输出

| 编号 | 输出 | 例子 |
|---|---|---|
| O1 | 同一 task 在多种情况下的成功率 | 木门 80% / 玻璃门 60% / 双开门 45% |
| O2 | 对应回放 | 每个 episode 的视频 |

### 1.4 三个隐藏难点（决定调研重点）

1. **I1 的开放程度极高**：“坐在椅子上观看窗外事件”不是传统操作任务，成功语义模糊，无法用几何谓词直接表达。
2. **I2 要求系统接受外来本体**：URDF 解析、运动学映射、控制协议适配，比“内置多个机器人”难一个量级。
3. **O1 要求“同一 task 的多种情况”**：需要变体生成机制（木门/玻璃门/双开门），而不是简单域随机化。

## 2. 六项能力成熟度与三个关键判断

| 能力 | 有人做吗 | 最佳实现 | 做到什么程度 |
|---|---|---|---|
| C1 物体 | ✅ 成熟 | RoboLab scenegen、MolmoSpaces、GIF | 已可从自然语言生成桌面场景；RoboLab 物体库 312 个 |
| C2 关系 | ✅ 成熟 | RoboLab 谓词库、GIF 接触几何 | RoboLab 有 13 个空间关系谓词；GIF 归纳出 8 类接触几何 |
| C3 判据 | 🟡 部分成熟 | RoboLab、AnyTask、BenchForge | “谓词库 + LLM 自动选择”已可用；开放语义任务仍脆弱 |
| C4 控制接口 | 🟡 部分 | RoboLab “Bring your own robot” | 支持任意 IsaacLab 兼容本体，但需手写配置类 |
| O1 多情况成功率 | ✅ 有 | RoboLab 敏感性分析、Colosseum V2 | 已能定量回答“哪个因子最强影响成败” |
| O2 回放 | ✅ 有 | RoboLab dashboard | 内置 web dashboard：回放 episode + 跨实验对比 |

三个关键判断：

1. **没有一项能力完全空白**（4 项成熟、2 项部分）→ 不能靠“填补空白”立论，要靠组合方式 + 易用性差异化。
2. **没有任何系统同时满足 I1 的任意性与 I2 的外部本体要求**：RoboLab 具备接任意 IsaacLab 本体的能力，但要求会写配置类；BenchForge / BenchClaw 完全不接受外来本体；也没有系统把“观看某事件”这类开放语义与 C3 的自动判据打通。
3. **最接近的是 RoboLab**：六项能力覆盖 5 项，是唯一同时具备（自动场景 + 自动判据 + 多本体 + 变体敏感性分析 + 回放）的单一系统。

## 3. 逐项调研

### 3.1 C1 场景创建（物体）：四代方法谱系

| 代际 | 代表 | 做法 |
|---|---|---|
| 一代：程序化生成 | ProcTHOR | 规则驱动，场景图 + 模板；可无限生成但语义贫乏 |
| 二代：数据驱动资产 | RoboCasa、BEHAVIOR-1K | 人工建模资产库 + 规则布局 |
| 三代：LLM 生成 | RoboLab、MolmoSpaces、STABLE、TabletopGen | LLM 出场景计划 → 几何求解 → 物理校验 |
| 四代：生成式 3D | EmbodiedGen、Seed3D、MetaScenes | 图像/文本直接生成仿真就绪资产 |

**RoboLab 的三级场景校验（可直接复用）**：① LLM 生成结构化场景计划（输入：物体目录（名称 + bounding box 尺寸）+ 主题）→ ② 空间求解器把关系谓词转成合法位姿（按依赖顺序：先放支撑面，再放其上的物体）→ ③ Isaac Sim 重力前向仿真 300 步做物理稳定性校验（最大位移 > 0.02 m 即视为不稳定）→ ④ 生成文本错误描述反馈给 LLM 重新规划。关键分工是 **LLM 只负责语义规划，几何与物理由确定性求解器/仿真器校验**，避免 LLM 直接输出坐标不可靠。

RoboLab 物体库构成（312 个）：vomp 196 / hope 27 / hot3d 25 / ycb 22 / handal 19 / objaverse 10 / fruits_veggies 9 / basic 4。

其他可借鉴：ClutterGen（物理合规的杂乱场景）、AgentWorld（布局生成 + 语义标注 + 移动操作一体化）、ForeRobo（3D 目标驱动的海量仿真数据）。

### 3.2 C2 物体关系：两套互补范式

**范式甲：谓词库 + 求解（RoboLab 路线）**——13 个空间关系谓词：`object_left_of` / `object_right_of`、`object_in_front_of` / `object_behind`、`object_above` / `object_below` / `object_below_top` / `object_on_bottom`、`object_on_center`、`object_next_to`、`object_between`、`object_at`、`objects_in_line`；另有容纳与放置类 6 个：`object_in_container`、`object_on_top`、`object_enclosed`、`object_inside`、`object_outside_of`、`object_outside_of_and_on_surface`。两个设计点：参考系可选（`robot` 自我中心 / `world` 世界坐标，mirrored 可翻转 XY）；通用参数统一（`logical` = all/any/choose K、`require_contact_with`、`require_gripper_detached`、`tolerance`）。

**范式乙：从数据归纳（GIF 路线）**——从 Ego4D 约 60 万条手—物交互中，用 LLM 按**几何接触模式**（而非语言表层）聚类出 8 类：Containment 容纳、Capping 加盖、Resting 静置、Leaning 倚靠、Hooking 悬挂、Slotting 插入槽位、Spanning 跨越、Pegging 销接。

| 维度 | RoboLab 谓词库 | GIF 接触几何 |
|---|---|---|
| 来源 | 人工设计 + LLM 选择 | 从真实数据归纳 |
| 数量 | 13 空间 + 6 容纳 + 其他 | 8 类 |
| 优点 | 精确、可参数化、可求解 | 覆盖真实人类行为分布 |
| 缺点 | 覆盖面受人工设计限制 | 类别粒度粗，难参数化 |
| 选用 | 两者结合：GIF 路线产出关系分类，RoboLab 路线产出可执行谓词 |  |

方法论要点：必须按几何接触模式聚类，否则“放到/放在/置于”会被当成三种不同关系，导致关系体系冗余。

### 3.3 C3 成功判据：四条技术路线（全链路最难的一环）

| 路线 | 代表 | 判据载体 | 自动性 | 主要弱点 |
|---|---|---|---|---|
| A. VLM 直接查询/打分 | SuccessVQA、T²-VLM | VQA / 分数 | 中（多需微调） | 复述脆弱、in-the-wild 失败 |
| B. 概率/价值探针（免训练） | TOPReward、GVL、RoboCLIP | token 概率 / 价值 / 相似度 | 高 | 需 logits 访问；进展标定 |
| C. LLM 生成代码/参数 | Eureka、Text2Reward、LARG、AnyTask | 可执行代码 | 高 | 需仿真在环；成功率 ≠ 指令对齐 |
| D. 训练专用判别器 | Eval-Actions、RoboReward | 分类器 / 评估器 | 低（需标注） | 人工标注成本、闭集 |

**RoboLab 的实现（当前最完整的工程解）**：LLM 被喂入①场景物体目录 + 元数据 ②任务范例 ③完整谓词库 ④能力轴语言模板 ⑤难度与物理可行性约束 → 生成任务代码 → 语法校验 → 资产校验 → 失败则精炼；同时禁止引用场景中不存在的物体，并注入已生成任务防重复。判据从**受控词表**中选择组合，因此天然可校验、可复现。

**AnyTask 的 check_success() 路线**：先生成 `check_success()`（定义任务目标条件），再用它指导 `reset()`、`compose_state()`、`reward_function()`、`scripted_policy()` 四个函数保持一致；作者报告可运行率最高 96%（o3-mini + 改进 prompt）。

必须正视的四个风险（完整清单见[自动 Benchmark 构建](../automated-benchmark-construction/)）：复述脆弱性（ROBORMBENCH：2,390 条轨迹 / 21,673 条复述，语义等价改写会让同一轨迹的成功判定翻转）；负例瓶颈（RoboReward）；长时程平坦（RMTL）；成功 ≠ 听指令（RDA）。对应指标建议：任务成功率、进展相关性 SRCC、成功检测准确率、**复述稳定性**、**指令对齐度**、分阶段进展校准。

### 3.4 C4 控制接口：离“上传 URDF 即用”还有多远

| 系统 | 支持本体 | 是否接受外部 URDF | 门槛 |
|---|---|---|---|
| RoboLab | 任意 IsaacLab 兼容机器人 | 🟡 部分 | 需按 IsaacLab 规范手写 Python 配置类 |
| MolmoSpaces | 内置（joint + pose 双接口） | ❌ | 不可换 |
| BenchForge | AI2-THOR 离散原语 | ❌ | 不可换 |
| BenchClaw | 无控制接口 | ❌ | — |
| RoboCasa / ManiSkill / LIBERO | 固定（Franka 等） | ❌ | 不可换 |
| BEHAVIOR-1K | 固定（R1 + 移动底盘） | ❌ | 不可换 |

**RoboLab 的 bring-your-own-robot 门槛**（接入新本体需要）：用 IsaacLab 的 `ArticulationCfg` 定义机器人；声明 `ee_recorder_bodies`（端到端位姿记录通道，缺失直接报 ValueError）；声明 `table_fixture`（桌面夹具归属机器人而非场景）；处理 `root_z_above_ground`（地面站立高度）；定义动作配置、本体感觉观测与接触夹爪 prim 路径。官方 NOTE 写明“创建新机器人与在 IsaacLab 中创建完全相同”——**这正是机会所在：把“接入新本体”从写代码做成上传向导。**

RoboLab 内置本体与动作空间（可作统一接口的输出形态参考）：

| 机器人 | 动作空间 | 维度 |
|---|---|---|
| DROID（Franka + Robotiq 2F-85，默认） | joint position / absolute EE IK / relative EE IK | 8 / 8 / 7 |
| Franka Panda | joint position / absolute EE IK / relative EE IK | 8 / 8 / 7 |
| Kinova Gen3（+ Robotiq 2F-85） | joint position | — |

设计要点：同一机器人**并列提供多种动作空间**，让不同抽象层级的策略都能对接。

跨本体技术参考：Unify Robot Actions in Camera Frame（2511.17001）、One-Policy-Fits-All（2603.14522）、Universal Actions for Embodied Foundation Models（2501.10105）、Cross-Embodiment Unified Hand Action Space（2607.03570）。URDF/机构处理参考：URDFormer（2405.11656）、URDF-Anything（2511.00940）、SPARK（2512.01629）、LLM-Guided Robot Ontology from URDF（2606.17073）。

建议技术路线：用户 URDF → 解析运动学链（关节类型/限位/连杆树）→ 映射统一动作空间（末端位姿 / 相机系）→ 仿真器 IK 求解 → 并列输出 joint + pose 双接口 → 控制协议适配层（用户声明 ROS topic / API 约定）。

### 3.5 O1 变体生成：四代演进

| 代际 | 代表 | 机制 | 局限 |
|---|---|---|---|
| 一代：固定任务集 | LIBERO、ManiSkill2 | 预设任务 + 固定场景 | 无变体概念 |
| 二代：域随机化 | ManiSkill3、RoboCasa | 随机化物体位姿/光照/材质 | 随机但不解释“为什么” |
| 三代：语义变体 | GIF、MolmoSpaces | 保持任务关系不变，改材质/颜色/子风格 | 变体轴是人工指定 |
| 四代：因子敏感性归因 | RoboLab SBI+MNPE、Colosseum V2 | 定量回答“哪个因子最强影响成败” | 需大量 rollout |

**GIF 的三级展开**（与“木门/玻璃门/双开门”逐字对应）：60 万条真实交互归纳 8 类接触几何 → 每类选 3 个代表任务 → 每任务实例化 5 个语义变体 → 24 × 5 = 120 个 benchmark 场景；评测指标为 Object Matching / Relationship Matching / Collision Rate（GIF 碰撞率 < 1%）。

**RoboLab 的敏感性分析**：θ = (θ_cont, θ_disc) 为环境参数，数据集 D = {(θ_i, x_i)}（x_i 为任务成功等观测），用 MNPE 训练神经密度估计器近似后验 p(θ|x)，结论从“成功率是多少”升级为“**材质/相机/光照/位姿中哪个因素最强影响成败**”；变化向量 ξ = (camera, light, background, pose)，另有三组消融（固定场景变指令具体度 / 固定指令变场景复杂度 / 固定场景变任务）。

**RoboLab 的语言变体**：每任务三档指令（default / vague / specific），是应对复述脆弱性的现成方案。

### 3.6 O2 回放与自动化评测

| 系统 | 回放能力 |
|---|---|
| RoboLab | 内置自包含 web dashboard：浏览场景/任务、回放 episode 视频、跨实验对比；记录 env_cfg.json 可复现回合 |
| BenchForge | Evaluation Reporting 阶段产出评测报告；IE-Track 记录 746 个实例化 action expression |
| AutoEval（2503.24278） | 集群式任务队列 + 自动成功检测 + 自动场景重置，7×24 无人值守；与人工真值高度一致 |
| ManiSkill3 | GPU 并行渲染，为大规模回放提供基础设施 |

RoboLab 的 server-client 架构值得注意：模型作为独立 server 运行，评测端是轻量 inference client——任何策略后端都能接入，与“用户自带机器人素材”的思路同构。

## 4. 端到端系统对标

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

## 5. 差异化定位与实施顺序

三条护城河（按可信度排序）：

1. **本体接入的易用性**：把 RoboLab 要求的“会写 IsaacLab 配置类”降到“上传 URDF + 声明控制协议”。这是易用性差异化而非能力空白，需要靠第二、三条加固。
2. **RoboLab 明确未覆盖的场景类型**（论文自述）：可形变物体（cloth / cables / bags）、需要精确力控与柔顺交互的接触密集任务、桌面级以外的房间级与多房间布局。
3. **判据的鲁棒性与可审计性**：把复述不变性、指令对齐度作为一等指标；判据独立验证、不做自评估；记录 provenance（哪个 LLM、什么 prompt、什么版本）。

建议的输出形态（在成功率之外）：各变体成功率 + **因子敏感性归因**（“材质是影响成功率的最强因子，相机位姿次之”）+ **复述稳定性**（“同一任务 5 种表述下判据一致性 92%”）+ **指令对齐度** + 每 episode 回放与可复现配置。

实施顺序：

1. **判据地基**：参考 RoboLab 的谓词库设计，建受控谓词词表（可参考其 `robolab-taskgen/references/conditionals.md`）；
2. **场景可靠性**：接入三级校验（几何求解 + 物理稳定性仿真 + 反馈重生成），同时参考 FATE 的静态四项检查（可达性/可供性/物理合理性/形态兼容性）；
3. **本体接入（差异化）**：URDF 解析 → 统一动作空间映射 → joint + pose 双接口输出；
4. **变体与归因**：语义变体轴（材质/几何/关系/拓扑）+ SBI 因子归因；
5. **输出层**：成功率 + 归因 + 复述稳定性 + 对齐度 + 回放 dashboard。

## 6. 论文清单（41 篇 + 补充引用）

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
| D03 | RoboDojo: A Unified Sim-and-Real Benchmark for Comprehensive Evaluation of Generalist Robot Manipulation Policies | 2607.04434 | 2026-07-05 |
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

## 7. 调研方法与可信度说明

- **检索方式**：arXiv API（须 HTTPS + curl 传输，HTTP 返回 406），8 组主题查询、约 350 条结果，全部使用一手元数据。
- **全文核验**：RoboLab / BenchForge / BenchClaw / 综述 / GIF / AnyTask / FATE / MolmoSpaces 等获取 HTML 全文（含附录）逐段核对；RoboLab 的核查同时使用论文与 GitHub 仓库（README、`docs/robots.md`、taskgen/scenegen skills、`references/conditionals.md`）。
- **已知局限**：未获取全部论文的全文，个别边界为合理推断（正文已标注）；会议录用状态以 arXiv comment 字段为准；检索盲区——初期仅用关键词检索曾遗漏 RoboLab（标题措辞为 high-fidelity simulation benchmark / task generalist policies），教训是须补充“已知系统名”的定向核查；用户提到的 “LARM / Language Model Rewards” 经多轮检索无法在 arXiv 核实，不建议引用。
- 本目录所在环境的 arXiv 索引已推进至 2026 年 9 月，26xx 号段论文均经 API 逐一验证。
