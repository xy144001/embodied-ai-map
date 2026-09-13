---
title: 仿真环境与具身数据生成
category: datasets
kind: benchmark
organization: 具身机器人技术地图数据集组
releaseDate: 2026-09-02
summary: 说明仿真任务库、轨迹生成器和 Sim2Real 桥接如何产生可重复的具身数据。
tags: [simulation, synthesis, sim2real, benchmark, humanoid]
draft: false
references:
  - title: HumanoidBench
    url: https://humanoid-bench.github.io/
  - title: ManiSkill
    url: https://maniskill.readthedocs.io/
  - title: RoboCasa
    url: https://robocasa.ai/
  - title: MimicGen
    url: https://mimicgen.github.io/
---

## 三类仿真资源

### 仿真任务库

HumanoidBench、ManiSkill、RoboCasa 和 BEHAVIOR-1K 提供环境、资产、任务定义、reset/step 接口和评测脚本。它们通常在线生成 rollout，而不是提供固定的专家轨迹压缩包。

### 数据生成器

MimicGen、RoboTwin、X-Humanoid 和类似管线可以从少量示范、人体动作或场景资产合成状态—动作序列。统计时应记录生成 episode、场景、任务和资产数量，不能和真实采集小时数混在一起。

### Sim2Real 桥接

重点记录坐标系、动力学随机化、接触模型、执行器延迟、控制频率和传感器噪声。仿真可以扩展场景、预训练策略和构造失败样本，但不能替代真实硬件噪声、碰撞风险和安全事件。

## 与模型工作的边界
