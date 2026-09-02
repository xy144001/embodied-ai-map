---
title: SMPLOlympics / HumanoidOlympics：物理人形运动与对抗 Benchmark
category: evaluation
kind: benchmark
organization: Carnegie Mellon University / NVIDIA
releaseDate: 2024-06-28
summary: 基于物理仿真的人形运动与竞技环境集合，覆盖高尔夫、标枪、跳高、跨栏、乒乓、网球、击剑、拳击、足球和篮球等；适合评估全身接触、敏捷运动、双人/多人交互与 motion-prior 控制。
tags: [whole-body-humanoid, sports, motion-imitation, physical-simulation, benchmark]
draft: false
references:
  - title: SMPLOlympics project page
    url: https://smplolympics.github.io/SMPLOlympics-Site
  - title: Paper
    url: https://arxiv.org/abs/2407.00187
  - title: Official code
    url: https://github.com/SMPLOlympics/SMPLOlympics
  - title: HumanoidOlympics project page
    url: https://humanoidolympics.github.io/
---

## 1. Benchmark 卡片：考的是“动态全身运动”，不是家务操作

[SMPLOlympics](https://smplolympics.github.io/SMPLOlympics-Site) 是一组 physically simulated sports environments。项目页列出个人项目：高尔夫、标枪、跳高、跳远、跨栏；以及 1v1/2v2 项目：乒乓、网球、击剑、拳击、足球和篮球。后续项目页以 **HumanoidOlympics** 名称继续表述同一“体育环境中的物理人形”路线。[论文](https://arxiv.org/abs/2407.00187)

它与 HumanoidBench/SIMPLE 的差别很明确：前两者主要考日常移动操作；SMPLOlympics 考高速重心切换、接触冲击、身体姿态、道具/球类交互和对手反应。它是**直接全身 humanoid benchmark**，但不以双手搬运家具为主。

## 2. 数据、输入与 action

| 层 | benchmark 提供/需要的内容 | 算法可怎样使用 |
|---|---|---|
| humanoid | 与 SMPL / SMPL-X 人体模型兼容的物理 humanoid；项目页也声明支持 real-world humanoid robot | 把 MoCap/video-derived motion prior 重定向为 policy reference，或直接从 state 学控制 |
| 场地与道具 | 球场、球拍、球、栏架、球门、篮筐、标枪等物理资产 | 形成 task state、碰撞与竞技目标 |
| motion prior | 人类视频/MoCap 可作为运动先验；官方安装要求获取 SMPL/SMPL-X 参数 | imitation / motion prior 训练，而不是唯一的任务标签 |
| observation | robot 自身状态、比赛/道具/对手相关状态；具体字段随 sport env 配置 | state policy；视觉设定必须在具体 env 中另行配置/报告 |
| action | 物理 humanoid 的连续控制动作，具体关节/控制模式取决于所选 humanoid | 输出全身 actuator target，不能直接把 SMPL axis-angle 当 action |

## 3. 量化标准：每个项目的目标函数不同

体育 benchmark 没有一个对所有项目都充分的“单一 success”。必须先固定 sport-specific predicate，再报告动作质量/安全。

| 任务类别 | 可量化主结果 | 具象例子 | 必要诊断 |
|---|---|---|---|
| 距离/高度项目 | 投掷距离、跳跃高度/距离、跨栏完成率/时间 | 标枪是否比基线投得更远；跨栏是否越过全部栏架 | 跌倒、栏架碰撞、足滑、动作能耗 |
| 目标击球项目 | 命中率、回合得分、落点/轨迹误差 | 高尔夫球是否进入目标区域；乒乓是否成功回球 | 球拍—球 contact、身体平衡、违规碰撞 |
| 对抗项目 | 胜率、得分差、有效命中、episode survival | 足球/篮球的进球或得分；击剑/拳击的有效命中 | 对手设置、随机 seed、比赛时长、身体碰撞安全 |
| motion imitation 消融 | reference tracking、动作自然度/稳定性 | 强 motion prior 与简单 reward 是否能得到更人形的动作 | root/hand/foot error、fall、penetration、关节限制 |

报告时把“奖励”与“比赛结果”分开：reward 可用于训练，投掷距离、得分/胜率、完成时间等才是各项目可解释的结果。不同项目量纲不同，不能不加归一化地做总均值。

## 4. 使用方式与代表工作

原始论文用该套环境 benchmark 多种 humanoid control 方法，并分析强 motion prior + 简单 reward 如何产生更自然的体育行为。训练时，方法接收当前 humanoid/环境状态（和可选 motion reference），输出连续全身动作；测试时在未训练的 episode seed、对手行为或比赛初始状态中运行完整回合，按各 sport predicate 计分。

对全身研究的价值：它可补充 HumanoidBench 的“日常任务缺少高速动态运动”问题；但若主张是家务移动操作，仍应同时报告 HumanoidBench/SIMPLE，而不是用体育高分替代物体搬运成功。

## 5. 访问、部署与边界

[官方代码](https://github.com/SMPLOlympics/SMPLOlympics)提供安装说明，要求 PyTorch、Isaac Gym 和需单独申请的 SMPL/SMPL-X body-model 参数。资产和人体模型许可应单独核验。它适合：运动先验、全身动态、竞技多智能体；不适合单独证明视觉语言家务、精细多指抓取或完整 sim-to-real 家居操作。
