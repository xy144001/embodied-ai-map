---
title: LIBERO-plus：VLA 鲁棒性与零样本泛化 Benchmark
category: evaluation
kind: benchmark
organization: LIBERO-plus project
releaseDate: 2024-06-01
summary: 在 LIBERO 任务上施加相机、机器人、语言、光照等多维扰动，评估视觉语言动作模型是否真正泛化而非记忆固定渲染与指令模板。
tags: [libero-plus, robustness, zero-shot, vla, benchmark]
draft: false
references:
  - title: LIBERO-plus 官方仓库
    url: https://github.com/sylvestf/LIBERO-plus
  - title: LIBERO 官方仓库
    url: https://github.com/Lifelong-Robot-Learning/LIBERO
---

## 1. 评测问题

LIBERO-plus 保留 LIBERO 的任务语义与基本评测方式，同时对观测和语言条件做系统扰动，用于诊断模型对视觉域、机器人 embodiment、语言表达和环境变化的鲁棒性。它的核心结论是 zero-shot robustness，而不是在扰动数据上重新训练后的 in-distribution success。

## 2. 结果应如何报告

至少拆分原始 LIBERO baseline 与各扰动维度的 success rate，并给出扰动强度、任务 suite、是否使用 target fine-tuning、随机种子和聚合方式。不要把七个维度简单平均后省略维度级结果；应同时报告 worst-group 或各组置信区间，才能看出模型是否被某一类扰动击穿。

## 3. AlphaBrain 适配边界

AlphaBrain 官网将 LIBERO-plus 列入全面基准套件，仓库 README 将其描述为 robustness 分支。平台结果只有在公开扰动配置、checkpoint、commit 与 episode 日志后才可与 LIBERO-plus 官方/社区结果比较；普通 LIBERO 高分不能推断 LIBERO-plus 鲁棒性。该套件仍以桌面操作为主，不覆盖全身人形的跌倒、脚底接触或长时行走。
