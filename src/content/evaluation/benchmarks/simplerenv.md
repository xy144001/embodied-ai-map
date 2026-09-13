---
title: SimplerEnv：真实机器人设置的 Real-to-Sim 评测 Benchmark
category: evaluation
kind: benchmark
organization: SIMPLER
releaseDate: 2024-05-01
summary: 基于 SAPIEN/ManiSkill 的真实机器人设置仿真评测环境，通过视觉匹配与变体聚合估计 RT-1、RT-1-X、Octo 等策略在真实部署中的表现与排序相关性。
tags: [simplerenv, real-to-sim, sapien, maniskill, sim2real, benchmark]
draft: false
references:
  - title: SimplerEnv 官方仓库
    url: https://github.com/allenai/SimplerEnv
  - title: SimplerEnv 项目仓库（ManiSkill3 分支说明）
    url: https://github.com/simpler-env/SimplerEnv
---

## 1. 两类评测设置

SimplerEnv 不是通用 humanoid benchmark，而是为 Google Robot、WidowX+Bridge 等真实设置建立可扩展的仿真对照：

- **Visual Matching**：将真实图像外观与仿真背景、机器人和物体纹理对齐。
- **Variant Aggregation**：改变背景、光照、干扰物、桌面纹理等生成多个变体，再平均策略表现。

其代码基于 SAPIEN 与 ManiSkill2，并提供 ManiSkill3 GPU 并行版本。动作示例为末端 xyz/axis-angle 增量加 gripper，具体含义依机器人 URDF 而定。

## 2. 指标与复现

主结果是任务 success 与仿真—真实排序/相关性分析；官方工具可计算 Pearson correlation 与 mean maximum rank violation。必须分别报告 visual-matching、variant-aggregation、仿真和真实结果，不能把 sim success 写成 real success。AlphaBrain 接入时应锁定环境、GPU/渲染后端、相机、控制频率、策略 checkpoint 与 variant seed。

## 3. 边界

SimplerEnv 的价值是 real-to-sim 评估方法和迁移相关性，不是双足全身控制测试。对 AlphaBrain 的结论应限定为“在指定真实机器人设置上的仿真评测可复现”，并在目标 humanoid benchmark/真机协议中另行验证。
