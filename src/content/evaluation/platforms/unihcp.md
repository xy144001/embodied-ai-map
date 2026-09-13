---
title: UniHCP：统一全身 humanoid 控制模型与训练框架
category: evaluation
kind: evaluation
organization: Carnegie Mellon University LeCAR Lab
releaseDate: 2024-07-15
summary: 将物理和行为约束合入统一 humanoid control 模型的研究框架，关注多全身技能与跨 embodiment 泛化；应作为统一控制方法评测页，而非独立标准化基准。
tags: [whole-body-humanoid, unified-control, motion-imitation, cross-embodiment, control-framework]
draft: false
references:
  - title: UniHCP paper
    url: https://arxiv.org/abs/2407.10353
  - title: Official repository
    url: https://github.com/LeCAR-Lab/UniHCP
---

## 1. 定位

[UniHCP](https://arxiv.org/abs/2407.10353)（A Unified Model for Humanoid Control with Physical and Behavioral Constraints）研究如何以统一模型处理多种 humanoid 全身控制技能及不同本体。它属于**方法/训练框架**：评测的核心是跨技能、跨参考动作、跨机器人形态时，控制能否保持物理可行与行为一致；不是带固定场景和统一 task leaderboard 的 standalone benchmark。

## 2. 输入、输出与评测口径

| 输入 | 输出 | 指标 |
|---|---|---|
| robot proprioception、目标/参考运动、物理与行为条件、robot morphology 标识（以代码实现为准） | 全身 joint action/trajectory | tracking、平衡、足滑、关节/力矩限制、跌倒、接触稳定性 |
| 未见技能/未见本体/扰动条件 | 泛化 rollout | 分别报告 seen 与 each OOD split，不能只给总平均 |

若把 UniHCP 接到抓取或移动操作场景，还需额外加 object-level success、掉落、双手接触和安全指标；统一 motion controller 的性能不自动等价于物体操作能力。

## 3. 部署与边界

复现前以[官方仓库](https://github.com/LeCAR-Lab/UniHCP)确认实际开放的 simulator、robot assets、motion datasets 和训练配置。实验报告应锁定动作/形态编码、reference preprocessing、训练数据来源和跨 embodiment split。适合与 HumanoidBench/ASAP/HOVER 对照：前者给任务成功，后两者给物理/人类动作迁移，UniHCP 给统一模型的技能与形态泛化。
