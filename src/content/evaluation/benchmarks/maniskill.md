---
title: ManiSkill：高吞吐通用操作 Benchmark 与仿真框架
category: evaluation
kind: benchmark
organization: ManiSkill
releaseDate: 2026-09-02
summary: 基于 SAPIEN 的 GPU 并行机器人操作框架与 benchmark，覆盖单臂、灵巧手、移动操作和部分 humanoid 任务；同时提供 real2sim、sim2real 与 RL/IL/VLA 基线。
tags: [maniskill, sapien, manipulation, gpu-simulation, benchmark]
draft: false
references:
  - title: ManiSkill 官方仓库
    url: https://github.com/haosulab/ManiSkill
  - title: ManiSkill 文档
    url: https://maniskill.readthedocs.io/
---

## 1. 定位

ManiSkill 同时是 SAPIEN 仿真框架和操作 benchmark 集合。官方环境覆盖桌面操作、清洁/绘图、灵巧操作、移动操作及不同机器人本体，并支持 GPU 并行采集 RGB-D、分割和状态数据。因此它适合做**高吞吐算法比较与跨本体操作消融**，但不能把任意自定义 task 当成官方统一排行榜。

## 2. 评测协议

| 维度 | 必须固定 | 推荐报告 |
|---|---|---|
| 任务 | environment ID、资产/场景版本、成功 predicate | 每任务 success、失败原因 |
| 观测 | state、RGB-D、segmentation、触觉及延迟 | 观测模态消融与 sim2real gap |
| 动作 | 关节位置/速度/力矩或末端增量、频率、chunk | action limit、控制频率、平滑度 |
| 泛化 | 物体、材质、布局、质量/摩擦与机器人 split | seen/unseen、IID/OOD 分开 |
| 执行 | GPU 并行数、episode horizon、seed | wall-clock throughput 与成功率分开 |

## 3. 与双足全身 benchmark 的关系

ManiSkill 的 humanoid 或移动操作环境可以作为全身控制的适配底座；但只有在公开 robot asset、接触模型、跌倒/足滑 predicate 和 evaluator 后，结果才具有全身 benchmark 的可比性。默认操作任务的成功率应归入“操作迁移诊断”，不能直接替代 HumanoidBench、SIMPLE 等全身任务。
