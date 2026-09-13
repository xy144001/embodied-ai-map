---
title: Mimicking-Bench：人类参考驱动的 humanoid 场景交互 Benchmark
category: evaluation
kind: benchmark
organization: Tsinghua University / Galbot / Shanghai AI Laboratory
releaseDate: 2024-12-24
summary: 以“人类动作参考能否变成不同场景中可执行的 humanoid 技能”为核心的 6 项家庭交互 benchmark；提供 20K 合成和 3K 真实人类交互参考，覆盖 11K 对象形状。
tags: [whole-body-humanoid, human-to-humanoid, imitation-learning, scene-interaction, benchmark, retargeting]
draft: false
references:
  - title: Project page
    url: https://mimicking-bench.github.io/
  - title: Paper
    url: https://arxiv.org/abs/2412.17730
---

## 1. Benchmark 卡片：它把什么问题固定下来

[Mimicking-Bench](https://mimicking-bench.github.io/) 不是一般“让机器人完成一个物体任务”的基准，而是固定问题：**从人类与场景交互的动作参考出发，能否让 humanoid 在未见几何/布局中仍完成同类身体—场景交互？** 官方项目页报告 6 个家庭全身任务、11K 个对象形状、20K synthetic + 3K real-world human interaction skill references。[项目页](https://mimicking-bench.github.io/)

| 六类任务 | 成功动作的具象含义 | 主要接触关系 | 为什么是全身任务 |
|---|---|---|---|
| sit on chair | 臀部落到椅座、身体稳定而非悬空 | 足—地、臀/背—椅 | 需要走近、转身、屈膝、改变支撑 |
| sit on sofa | 在不同宽度/高度沙发上稳定坐下 | 足—地、臀/背—沙发 | 场景几何变化影响落座姿态 |
| lie on bed | 身体躺到床面并保持姿态 | 足/躯干—床 | 不是单一末端目标，涉及大范围 body contact |
| lie on sofa | 在沙发上躺下 | 躯干/腿—软家具几何 | 接触面积与姿态约束更复杂 |
| touch points near object | 身体/手到达物体附近指定点 | 足—地、手/身体—目标邻域 | 测未见对象几何下的到达与碰撞规避 |
| lift box | 走近、抓住、抬起箱子且维持平衡 | 足—地、双手—箱、箱—环境 | 把双手操作与全身支撑/重心变化合在一起 |

## 2. benchmark 随附的数据类型

它比 HumanoidBench 更像“benchmark + human reference data package”。每个能力样本可概念化为 **human reference + scene/object geometry + target humanoid rollout**，而不是只给一个 reward function。

| 数据层 | 官方明确的内容 | 用途 | 不能误读为 |
|---|---|---|---|
| human skill references | 20K 合成交互参考 + 3K 真实人类交互参考 | retarget、motion tracking、imitation-learning 的训练/输入 | 机器人 torque/action label |
| object/scene geometry | 11K 多样对象形状及家庭交互场景 | scene-aware interaction generation、未见几何泛化 | 每个对象都已有机器人可行抓取 |
| human body motion | 全身动作与交互关系；具体发布表示/文件以代码 release 为准 | root/hand/foot/body contact target | 目标 humanoid 的同构关节角 |
| robot state/action | humanoid proprioception、控制器输出和物理 rollout（由 benchmark pipeline 产生） | 闭环执行、tracking/physical metrics | 与 human reference 自动一一对应 |
| task annotation | 任务类别、目标对象/接触或姿态条件、训练/测试几何关系 | 成功 predicate 与 scene split | 仅凭文本即可判分 |

## 3. 输入 → 输出 → 判分：以“搬箱子”为例

1. 输入是一段人类 lift-box 参考、箱子 mesh/初始 pose、目标 humanoid 的初始状态，以及训练/测试场景配置。
2. 方法可以先将人类动作 retarget 成 robot reference，再训练 tracking/imitation policy；也可以生成 scene-aware reference，再输出全身控制。
3. 每个 control step，policy 从 robot state（可能加视觉/scene observation）输出 position/velocity/torque 型控制；模拟器计算接触和下一状态。
4. 判分至少包含：箱子是否被抬起/保持、robot 是否稳定、目标身体/接触关系是否达到，而不是“reference joint MSE 小”。

| 评测层 | 输入 | 输出 | 应报告的量 |
|---|---|---|---|
| retarget | human motion + target robot morphology | robot reference trajectory | body/hand/foot target error、joint-limit violation、self-collision |
| tracking | robot state + robot reference | control action / rollout | tracking error、foot slip、fall rate、contact timing |
| task execution | robot state + scene/object + task condition | success/failure trajectory | 每个任务 success、object/pose condition、episode duration |
| geometry generalization | 未见 chair/sofa/bed/box shape 或布局 | 同一技能的 rollout | seen vs unseen geometry success，不合并成单一均值 |

## 4. 评价标准：什么算“做对了”

论文强调两类互补信号：

- **kinematic/interaction correctness**：关键 body part 是否达到相对物体的目标几何关系，例如坐下时骨盆/躯干相对座面的姿态，触点任务中身体部位是否到达指定邻域；lift-box 中手与箱子的相对关系。
- **physical executability**：机器人是否保持平衡、没有无效穿透/明显碰撞，且在物理引擎中完成物体或姿态任务。对坐/躺任务，纯 motion tracking 好看但身体没有实际支持也不应视为成功。

每个新方法应逐项给六任务的 success，并分 **seen geometry**、**unseen geometry/scene**。另外报告 reference tracking、接触一致性、penetration、跌倒和足滑，明确这些是诊断量而非 success 的替代。

## 5. 它和外部数据集的关系

Mimicking-Bench 内部已有 human reference 资产；AMASS/GRAB/OMOMO/BEHAVE 可作为额外 motion/contact/scene 数据，但必须在 manifest 中标注来源和作用：

- AMASS：补充不含物体的 locomotion/姿态先验；
- GRAB、OMOMO：补充手—物/大物体交互参考；
- BEHAVE：补充 RGB-D 人—物感知前端。

这些外部数据不应包含 benchmark test 的对象/场景/动作近重复；更不能覆盖基准的未见 geometry split。详见[数据集—Benchmark 关联页](../overview/)。

## 6. 复现与访问状态

论文/项目页明确给出任务、参考数据规模和 benchmark pipeline，但它不是通用物理引擎。运行前必须从作者实际发布的代码/asset 指引核实：物理引擎、humanoid model、scene mesh、reference format、split 文件、许可证和 evaluator。最小复现记录应含：reference 数据版本、synthetic/real 比例、object geometry split、retarget 参数、控制频率、episode seed 与每项 success predicate。

## 7. 结论边界

它适合回答“人类动作数据能否迁移到新场景几何中的 humanoid 全身交互”。它不直接覆盖长时程开放家庭任务、自然语言理解或细粒度多指操作；这些需要与 HumanoidBench、LeVERB-Bench 或 SIMPLE 的不同协议组合报告。
