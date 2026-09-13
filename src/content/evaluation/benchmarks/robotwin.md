---
title: RoboTwin 2.0：强域随机化双臂操作 Benchmark
category: evaluation
kind: benchmark
organization: RoboTwin Platform
releaseDate: 2025-06-30
summary: 基于 SAPIEN 的双臂操作与数据生成 Benchmark，当前上游包含 50 个任务、clean/randomized 两种设置，用跨视觉域测试评估双臂策略鲁棒性。
tags: [robotwin, bimanual, sapien, domain-randomization, benchmark]
draft: false
references:
  - title: RoboTwin 2.0 官方项目/排行榜
    url: https://robotwin-platform.github.io/leaderboard
  - title: RoboTwin 2.0 评测文档
    url: https://huggingface.co/docs/lerobot/en/robotwin
  - title: RoboTwin 2.0 论文
    url: https://arxiv.org/abs/2506.18088
---

## 1. 任务与环境

RoboTwin 2.0 提供 50 个双臂 manipulation tasks，示例包括堆叠、工具使用、按压、交接、旋钮/开关和搬运。公开配置以 Aloha-AgileX 双臂为主（14 DoF），head/left/right camera 为常见视觉输入，动作是归一化到 `[-1,1]` 的 14 维关节空间控制；仿真后端是 SAPIEN，不是 MuJoCo。

## 2. 官方评测协议

常见设置是每任务 50 条 `demo_clean` 示范、每任务 100 个评测 episode，并区分 clean2clean（easy）和 clean2random（hard）。随机化覆盖 clutter、光照、背景、桌面高度和语言指令。排行榜默认用两种设置的平均值排序；结果必须拆开报告，不可只给一个未说明设置的 success rate。

## 3. AlphaBrain 适配与边界

AlphaBrain 的 RoboTwin 接入应锁定上游任务 tuple、SAPIEN 版本、机器人 embodiment、camera names、action chunk 和 randomization config。双臂成功率能说明 bimanual policy 的操作与视觉泛化，不能直接替代双足 humanoid 的行走、支撑切换、跌倒与全身碰撞评测。排行榜要求公开代码、权重和技术报告，复现时应保存这些版本信息。
