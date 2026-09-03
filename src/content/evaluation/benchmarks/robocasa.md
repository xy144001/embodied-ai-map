---
title: RoboCasa / RoboCasa365：厨房与日常家务操作 Benchmark
category: evaluation
kind: benchmark
organization: RoboCasa
releaseDate: 2026-02-18
summary: 面向家庭厨房场景的程序化仿真操作 Benchmark；RoboCasa365 将任务扩展到 365 个日常任务与大规模厨房场景，并区分 atomic/composite、seen/unseen 评测。
tags: [robocasa, robocasa365, household, kitchen, long-horizon, benchmark]
draft: false
references:
  - title: RoboCasa 官方仓库
    url: https://github.com/robocasa/robocasa
  - title: RoboCasa365 AlphaBrain 适配说明
    url: https://github.com/AlphaBrainGroup/AlphaBrain/blob/main/benchmarks/Robocasa365/README.md
---

## 1. 评测对象

RoboCasa 关注厨房/家庭场景中的抓取、放置、开关与组合操作；RoboCasa365 在公开说明中覆盖 365 个任务、2500+ procedurally generated kitchen scenes，并提供 atomic 与 composite task collection。它更适合衡量场景多样性、长时程家务与跨任务泛化，不应和 LIBERO 的固定桌面 10-task suite 混为同一难度尺度。

## 2. RoboCasa365 协议

AlphaBrain 的公开适配通过 policy server 与 RoboCasa365 simulation client 的 WebSocket 通信完成；配置支持 `atomic_seen`、`composite_seen`、`composite_unseen` 等 task set，常见默认是每任务 50 episodes、16-step action chunk。报告必须写明任务集合、场景生成版本、机器人/相机、episode 数和是否 target-only。

## 3. 指标与复现

主指标是每任务 success rate 及 seen/unseen 聚合；建议另报子任务完成率、掉落、碰撞、超时和失败原因。AlphaBrain README 中的 RoboCasa365 数字（例如 Atomic-Seen、Composite-Seen/Unseen 的平均成功率）属于平台/基线表，只有在锁定 checkpoint、任务清单和 evaluator 后才可复核。RoboCasa365 依赖其官方环境与数据许可证，安装版本应单独记录。

## 4. 与全身人形的边界

默认 RoboCasa/RoboCasa365 本体是 Panda/移动操作平台。迁移到双足人形时需新增下身 controller、支撑与跌倒 predicate、foot slip 和全身碰撞日志；厨房任务成功本身不等于 humanoid loco-manipulation 成功。
