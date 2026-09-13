---
title: Habitat-Lab：导航、重排与社会交互 Benchmark 栈
category: evaluation
kind: benchmark
organization: Meta AI
releaseDate: 2026-09-02
summary: 基于 Habitat-Sim 的模块化 embodied benchmark 栈，覆盖 PointNav、ObjectNav、ImageNav、Rearrange 与 Habitat 3.0 社会导航等任务；任务配置与 benchmark 配置分离，结果必须锁定场景、episode split 和传感器。
tags: [habitat, navigation, rearrangement, social-navigation, benchmark]
draft: false
references:
  - title: Habitat-Lab 官方仓库
    url: https://github.com/facebookresearch/habitat-lab
  - title: Habitat-Lab benchmark 配置说明
    url: https://github.com/facebookresearch/habitat-lab/blob/main/habitat-lab/habitat/config/README.md
---

## 1. 它在测什么

Habitat-Lab 更像一套可组合的 benchmark/训练框架，而不是单一排行榜。PointNav 测到目标点的导航，ObjectNav 测寻找目标类别，Rearrange 测在室内场景中移动并操作物体，Habitat 3.0 还提供多智能体社会导航等配置。官方代码把 task specification 与 benchmark config 分开，便于复用传感器、动作和数据集。

## 2. 输入、输出与主指标

| 任务族 | 典型输入 | action | 主指标 | 关键边界 |
|---|---|---|---|---|
| PointNav / ObjectNav | RGB、深度、里程计或 oracle state | base linear/angular velocity | success、SPL、distance | 导航成功不等于物体操作成功 |
| ImageNav | 目标图像、RGB-D、位姿估计 | base motion | success、SPL | 需要明确目标图像是否见过 |
| Rearrange | RGB-D、关节/底盘状态、物体观测 | base + arm/gripper | task success、SPL/效率 | 默认 agent 多为移动操作体，双足接口需自建 |
| Habitat 3.0 social nav | 多视角深度、humanoid detector 等 | base velocity | follow/social success 与安全约束 | 社会导航不能替代全身接触操控 |

## 3. 如何用于人形研究

它适合补足全身 benchmark 中较弱的**室内空间理解、长距离导航和社会交互**轴。若迁移到双足 humanoid，报告必须额外记录足底接触、跌倒终止、碰撞和全身 action adapter；只改 robot asset 而保留原有导航 success，最多能说明导航迁移。

复现时锁定 Habitat-Lab/Habitat-Sim commit、场景数据版本、episode JSON、传感器分辨率与噪声、动作频率、seed 和 SPL 计算实现。RGB-D 与 oracle state 应分开成独立 track。
