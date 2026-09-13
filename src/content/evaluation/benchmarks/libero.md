---
title: LIBERO：终身机器人学习与知识迁移 Benchmark
category: evaluation
kind: benchmark
organization: UT Austin LARG / RPL
releaseDate: 2023-06-06
summary: 基于 MuJoCo/robosuite 的桌面操作 Benchmark，用受控分布偏移和长程任务测试声明性知识、程序性知识及其组合的迁移；共 130 个任务，官方代码 MIT、数据集 CC BY 4.0。
tags: [libero, lifelong-learning, manipulation, knowledge-transfer, mujoco, benchmark]
draft: false
references:
  - title: LIBERO 官方仓库
    url: https://github.com/Lifelong-Robot-Learning/LIBERO
  - title: LIBERO 官方文档
    url: https://lifelong-robot-learning.github.io/LIBERO/html/getting_started/overview.html
  - title: LIBERO 数据集说明
    url: https://libero-project.github.io/datasets
---

## 1. 它考什么

LIBERO 不是单纯的模仿学习成功率榜单，而是研究机器人在连续任务中能否把已学知识迁移到新对象、新空间关系、新目标和混合任务。官方仓库把 130 个任务分成四个 suite：Spatial、Object、Goal 与 LIBERO-100；LIBERO-100 再拆为 LIBERO-90（预训练）和 LIBERO-10（下游终身学习测试）。

| Suite | 任务数 | 受控变化/问题 |
|---|---:|---|
| LIBERO-Spatial | 10 | 空间关系变化，考 declarative spatial knowledge |
| LIBERO-Object | 10 | 物体类别变化，考 object knowledge transfer |
| LIBERO-Goal | 10 | 目标/行为变化，考 procedural knowledge |
| LIBERO-90 / LIBERO-10 | 90 / 10 | 混合知识迁移；90 训练、10 下游测试 |

## 2. 输入、动作与数据

官方数据包含 workspace 与 wrist RGB、proprioception、语言任务描述和 PDDL 场景描述；常见控制接口是 7 维连续动作（末端位姿增量 6D + gripper）。策略必须通过 MuJoCo 闭环 rollout 完成任务，离线 demonstration loss 或语言相似度不能替代 success。

## 3. 指标与公平比较

主指标是逐任务/逐 suite 的 episode success rate；终身学习应额外报告任务顺序、每个时间点的 T×T 矩阵、平均成功率（ASR）、后向迁移（BWT）和遗忘（F）。必须固定 suite 版本、task list、机器人/相机、随机种子、每任务 episode 数和是否使用 LIBERO-90 预训练。LIBERO 数据集与 LeRobot 转换版本可能不同，报告中应锁定 dataset revision。

## 4. 与 AlphaBrain 的关系

AlphaBrain 将 LIBERO-Spatial/Object/Goal/Long 作为核心评测与 continual-learning stream；这属于复用官方任务协议。官网展示的 `libero_object 99.0%`、`libero_goal 95.6%`、`libero_spatial 90.6%`、`libero_10 85.4%`（总平均 92.7%）应标为平台自报结果，除非同时提供 checkpoint、commit、seeds、任务级日志，否则不宜与论文 leaderboard 直接合并。

## 5. 局限

LIBERO 主要是固定桌面、单机械臂操作，不能单独证明双足行走、全身平衡或真实部署鲁棒性。将其成绩外推到 humanoid loco-manipulation 前，应在 HumanoidBench/SIMPLE 等目标本体 benchmark 上重新评估。
