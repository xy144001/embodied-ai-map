---
title: CALVIN：语言条件长时程操作 Benchmark
category: evaluation
kind: benchmark
organization: University of Freiburg
releaseDate: 2022-06-30
summary: 基于仿真 Franka 的语言—视觉长时程连续控制 Benchmark，按连续完成的子任务数评价策略能否组合语言指令并保持状态。
tags: [calvin, language-conditioned, long-horizon, manipulation, benchmark]
draft: false
references:
  - title: CALVIN 官方网站
    url: https://calvin.cs.uni-freiburg.de/
  - title: CALVIN 官方仓库
    url: https://github.com/mees/calvin
---

## 1. 任务协议

CALVIN（Composing Actions from Language and Vision）要求 agent 从 onboard sensors 读取观测，仅凭连续自然语言指令完成一串操作。LH-MTLC（Long-Horizon Multi-Task Language Control）在每条 chain 开始前将机器人 reset 到中性姿态，避免初始位姿偏差；官方提供不同训练/测试环境组合（如 D→D）和 1–5 条指令的链。

## 2. 输入、动作与指标

可选 sensor suite 包括静态 RGB、gripper RGB 与本体状态（具体字段随 CALVIN 配置而定）；典型 joint action 为 **8 维**（7 个关节位置 + 1 个 gripper action）。主指标是 multi-task language-conditioned success（MTLC）以及长时程平均完成链长（LH-MTLC），应同时报告 1、2、3、4、5 子任务的成功率、环境 split、语言输入方式和 chain 数。

## 3. AlphaBrain 适配注意

AlphaBrain 的 CALVIN 适配应被记录为对外部 simulator/evaluator 的接口接入：policy server 输出动作，CALVIN 环境负责语言切换、状态推进与 success。不能将单步 MTLC、离线动作误差或单一 chain 长度写成与官方 LH-MTLC 等价；须锁定 CALVIN commit、sensor suite、环境 D/A/B/C split、reset 规则和每条 chain 的随机种子。官方代码为 MIT 许可。

## 4. 边界

CALVIN 是固定机械臂的仿真长程操作，不包含双足支撑、跌倒或全身碰撞指标；对全身人形结论只能作为语言长程规划迁移证据。
