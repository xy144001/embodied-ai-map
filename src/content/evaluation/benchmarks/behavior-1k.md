---
title: BEHAVIOR-1K：面向人类日常活动的大规模家居 Benchmark
category: evaluation
kind: benchmark
organization: Stanford Vision and Learning Lab
releaseDate: 2024-03-14
summary: 基于现实人类需求调查选择 1,000 个家居活动的综合仿真 Benchmark，覆盖清洁、烹饪、整理等长时程、多对象行为，并提供训练与评测基础设施。
tags: [behavior-1k, household, long-horizon, omnigibson, benchmark]
draft: false
references:
  - title: BEHAVIOR-1K 官方仓库
    url: https://github.com/StanfordVL/BEHAVIOR-1K
  - title: BEHAVIOR 官方网站
    url: https://behavior.stanford.edu/
  - title: BEHAVIOR-1K 论文
    url: https://arxiv.org/abs/2403.09227
  - title: 2026 Challenge evaluation rules
    url: https://github.com/StanfordVL/BEHAVIOR-1K/blob/main/docs/challenge/evaluation.md
---

## 1. Benchmark 定位

BEHAVIOR-1K 以真实人类时间使用调查和偏好研究为任务来源，目标是评估 agent 在 1,000 个 everyday household activities 中的长期行为组合能力。任务通常涉及多个对象、状态变化与子目标，难度和资源开销都高于固定桌面操作套件。

## 2. 评测记录

应按官方版本、任务子集、场景/物体资产、agent embodiment、episode horizon 和许可证记录结果。2026 challenge 规则要求锁定 `v3.9.1`，使用 RGB+depth+proprioception，排名分数是 100 个任务的 BDDL predicate 部分成功平均值，并另报模拟时间、导航距离和末端位移等效率量。若仅运行 AlphaBrain 可访问的子集，必须明确“BEHAVIOR-1K subset”，不能宣称覆盖 1,000 任务。

## 3. AlphaBrain 与全身人形边界

AlphaBrain 将 BEHAVIOR-1K 列为评测适配方向，但平台支持不等于仓库已经提供完整、可复核的全量结果。默认 BEHAVIOR/OmniGibson 机器人和控制接口也不等价于双足 humanoid；迁移时需公开 embodiment、动作适配、支撑/跌倒规则和目标任务清单，并重新运行 closed-loop evaluator。
