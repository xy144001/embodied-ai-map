---
title: Humanoid-Gym：人形 locomotion 与 sim-to-real 训练框架
category: evaluation
kind: evaluation
organization: RobotEra
releaseDate: 2024-04-08
summary: 基于 NVIDIA Isaac Gym 的人形强化学习训练框架，面向 locomotion、扰动鲁棒性与零样本 sim-to-real；可作为全身下肢控制基础，但不应混同于全身移动操作 benchmark。
tags: [whole-body-humanoid, locomotion, isaac-gym, sim-to-real, control-framework]
draft: false
references:
  - title: Humanoid-Gym repository
    url: https://github.com/roboterax/humanoid-gym
  - title: Project page
    url: https://sites.google.com/view/humanoid-gym/
  - title: Paper
    url: https://arxiv.org/abs/2404.05695
---

## 1. 定位

[Humanoid-Gym](https://github.com/roboterax/humanoid-gym) 是在 NVIDIA Isaac Gym 上训练 humanoid locomotion 的开源强化学习框架，论文/项目强调 zero-shot sim-to-real transfer，并包含面向 Unitree H1 等机器人训练和部署的资源。它直接涉及双足人形的稳定、行走和扰动恢复，但当前核心不是手—物交互或完整移动操作任务集。[项目页](https://sites.google.com/view/humanoid-gym/)

## 2. 输入—输出与指标

| 输入 | 输出 | 推荐报告 |
|---|---|---|
| joint state、IMU/base 状态、命令速度、历史观测和随机扰动 | lower-body/全身关节 action、rollout | command tracking error、速度、跌倒率、push recovery、足滑、torque/能耗 |
| sim 参数随机化、地形、外力 | 多环境训练/测试结果 | IID 与摩擦、质量、延迟、地形 OOD 分开报告 |
| 接上上身/手部策略时的 hand/base 目标 | 分层执行轨迹 | 单列上身 policy、IK 和下身 controller，避免归因混淆 |

## 3. 部署与边界

使用 Isaac Gym、Python、GPU 与仓库指定的 RL 依赖；历史 Isaac Gym 版本与新 Isaac Lab 不可想当然混装。对全身移动操作研究，它适合作为下身基础技能/对照：后续仍需在 HumanoidBench、Isaac Lab 或 SIMPLE 等环境中加入物体、双手、足部支撑和 task success 评测。仅有 locomotion 指标时，结论必须限制为 locomotion/sim-to-real，而不是全身操作。
