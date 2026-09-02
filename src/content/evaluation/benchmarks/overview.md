---
title: 全身人形 Benchmark：任务协议与数据集关联地图
category: evaluation
kind: roadmap
organization: Embodied AI Map
releaseDate: 2026-09-02
summary: 区分仿真平台与 benchmark，并把 HumanoidBench、Mimicking-Bench、LeVERB-Bench、SIMPLE 的任务协议连接到 AMASS、GRAB、BEHAVE、OMOMO、HumanML3D 等可获取数据集。
tags: [whole-body-humanoid, benchmark, datasets, evaluation-protocol, locomanipulation]
draft: false
references:
  - title: HumanoidBench
    url: https://humanoid-bench.github.io/
  - title: Mimicking-Bench
    url: https://mimicking-bench.github.io/
  - title: LeVERB paper
    url: https://arxiv.org/abs/2506.13751
  - title: SIMPLE
    url: https://psi-lab.ai/SIMPLE/
---

## 1. Benchmark 与平台、数据集的边界

- **仿真与评测平台**回答“算法如何部署到虚拟机器人上”：它提供 physics、robot asset、传感器、action interface、reset 和 rollout，例如 MuJoCo、Isaac Lab、Genesis。
- **数据集**回答“模型从哪些记录中学习/被离线检验”：它提供人体动作、视觉、物体、接触或真实机器人轨迹，例如 GRAB、BEHAVE、AMASS。
- **Benchmark**回答“不同方法如何公平比较”：它固定任务、初始状态分布、训练/测试划分、success predicate、episode budget 和汇总指标。它可以使用数据集作为动作先验、视觉训练源或任务生成来源，但 benchmark 的最终分数必须来自固定 closed-loop rollout。

## 2. 全身人形 benchmark 与数据集的关联

| Benchmark | 固定的评测问题 | 可关联的数据集 | 数据如何进入 benchmark | 最终应报告 |
|---|---|---|---|---|
| [HumanoidBench](../humanoidbench/) | 27 个 locomotion 与 whole-body manipulation 仿真任务 | AMASS、GRAB、OMOMO | 用于预训练 walk/reach/motion imitation skill，或构造人类动作/接触先验；官方 benchmark 任务本身以 MuJoCo 环境为准 | 逐任务 success、return、完成时间、跌倒/接触安全、IID/OOD |
| [Mimicking-Bench](../mimicking-bench/) | 人类动作到 humanoid-scene interaction 的 6 个家庭任务 | AMASS、GRAB、OMOMO、BEHAVE | 人类动作/交互几何是核心参考；通过 retarget 和 scene interaction generation 形成训练数据 | scene/generalization success、tracking、接触、penetration、跌倒 |
| [LeVERB-Bench](../leverb-bench/) | vision-language humanoid WBC 的 150+ 闭环任务（论文报告） | AMASS/其他人类 MoCap、HumanML3D、EgoBody/H2O（感知迁移） | 重定向 MoCap 与 Isaac Sim 渲染构成视觉—语言训练源；视觉数据可做前端预训练，不能替换闭环评测 | 指令条件 success、视觉 OOD、跌倒/碰撞、oracle-vs-vision gap |
| [SIMPLE](../simple/) | 60 个全身移动操作任务、50 个室内场景（项目报告） | Open X、RH20T、GRAB、BEHAVE、OMOMO | Open X/RH20T 用于 VLA 上游预训练；人—物数据用于 retarget/接触或感知；目标 task 不得泄漏到预训练 | VLA/WAM closed-loop success、对象/场景/指令 OOD、掉落/跌倒/安全 |

## 3. 数据集—benchmark 的合规连接流程

1. **先定 benchmark**：选择 robot、任务、场景与 evaluation split；这一层决定最终 claim 的范围。
2. **再选数据集角色**：标为 motion prior、human-object contact prior、视觉前端或 cross-embodiment pretraining；一个数据集可承担多角色，但必须分别做消融。
3. **建立不可变 manifest**：列出数据集版本、许可、sequence ID、subject/object/scene、过滤规则和 split；明确 benchmark test asset/文本/场景没有进入训练。
4. **重定向与物理校验**：人体数据经过 coordinate/scale alignment、IK、joint/torque limit、碰撞体和物体惯量配置后，先评估可执行性，再投入 policy training。
5. **闭环计分**：测试时由仿真传感器实时驱动 policy；GT human/object state 只能作为 oracle 上界，不能混入正式 vision score。

详细的输入、输出、指标和泄漏审计见[数据集评测协议](../../datasets/evaluation-protocols/)。

## 4. 最小 benchmark 报告表

| 字段 | 必须公开 |
|---|---|
| 任务协议 | 环境/asset commit、robot/hand 型号、success predicate、horizon、evaluation seeds |
| 数据关联 | 每个数据集的版本、许可、用途、样本量、split 与与 benchmark test 的去重规则 |
| 输入输出 | 观测字段/频率/延迟、action 意义/频率/chunk、是否使用 privileged state 或预训练低层 skill |
| 结果 | 每任务 IID/OOD success、平均/方差、完成时间、跌倒/足滑/碰撞/掉落/力矩或接触违规 |
| 复现 | retarget/config、evaluator、episode CSV、视频和失败类型 |

结论只能按最窄链路表述：例如“Open X 预训练 + GRAB 接触先验在 SIMPLE 的指定 humanoid task 上提升 OOD success”，不能缩写成“Open X 证明了全身 humanoid 能力”。
