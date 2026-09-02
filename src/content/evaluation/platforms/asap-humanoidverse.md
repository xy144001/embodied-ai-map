---
title: ASAP / HumanoidVerse：跨模拟器与真机物理对齐的全身技能栈
category: evaluation
kind: evaluation
organization: Carnegie Mellon University LeCAR Lab
releaseDate: 2025-02-03
summary: 面向 agile humanoid whole-body skills 的 sim-to-real 物理对齐框架，建立在 HumanoidVerse 多模拟器学习框架与 Human2Humanoid 动作跟踪之上；适合跨仿真器/真机一致性验证，不是固定多任务排行榜。
tags: [whole-body-humanoid, sim-to-real, physics-alignment, humanoidverse, motion-tracking]
draft: false
references:
  - title: ASAP repository
    url: https://github.com/LeCAR-Lab/ASAP
  - title: ASAP paper
    url: https://arxiv.org/abs/2502.01143
---

## 1. 定位

[ASAP](https://github.com/LeCAR-Lab/ASAP)（Aligning Simulation and Real-World Physics for Learning Agile Humanoid Whole-Body Skills）是 RSS 2025 的开源 sim-to-real 系统，目标是让全身人形技能的仿真物理更贴近真实硬件。官方 repository 标明它构建于 **HumanoidVerse**（多模拟器 humanoid 学习框架）和 Human2Humanoid（全身动作跟踪）之上，并以 MIT license 发布代码。[论文](https://arxiv.org/abs/2502.01143)

它应当被理解为“验证全身技能是否跨 physics backend/真机仍成立”的评测栈，而不是 HumanoidBench 那类统一任务数量、场景和排行榜的 benchmark。

## 2. 接口

| 输入 | 输出 | 应记录的比较 |
|---|---|---|
| 参考全身动作、robot model、物理参数与观测/控制设定 | 低层全身 policy、仿真/真机 rollout | reference tracking、稳定性、动作延迟和接触差异 |
| 模拟器配置与对齐策略 | 不同 simulator 的同策略轨迹 | joint/root/foot/hand trajectory deviation、接触事件一致性 |
| 真实硬件系统辨识/传感记录（若做 sim-to-real） | 真机执行日志 | sim→real success、跌倒、torque/thermal/limit 违规、安全恢复 |

## 3. 评测范式

1. **同一任务、跨后端**：冻结 robot asset、动作接口、控制频率、目标运动和扰动；分别在训练 simulator、第二 simulator 与真机运行。
2. **不是只测 imitation error**：报告 root/关键末端 tracking 之外的跌倒、足滑、接触事件、关节/力矩限制和任务成功。
3. **对齐消融**：比较未对齐物理、参数对齐、观测/actuation delay 模型、domain randomization；否则无法归因 sim-to-real 提升。
4. **移动操作扩展**：若加入物体，须单独固定物体质量/摩擦/碰撞与 grasp success；纯运动 tracking 不证明 loco-manipulation。

## 4. 部署与边界

官方代码含 `humanoidverse/`、`sim2real/`、scripts 和 setup；按仓库的 release/README 创建 Python 环境，并锁定目标 simulator 与机器人资源。该项目的长处是物理对齐和全身技能迁移；它未替代面向多家庭/移动操作任务的标准化 benchmark。最佳组合是：在 HumanoidBench/LeVERB-Bench 取得任务分数，再以 ASAP 式跨后端/真机实验验证可信度。
