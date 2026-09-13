---
title: HOVER：人类动作驱动的人形全身运动控制框架
category: evaluation
kind: evaluation
organization: Carnegie Mellon University LeCAR Lab
releaseDate: 2024-11-15
summary: 面向 human-to-humanoid whole-body control 的开源研究框架，重点在从人类运动学习接触丰富的全身技能与稳定执行；适合动作重定向/模仿及 sim-to-real 评测，不是通用双手移动操作排行榜。
tags: [whole-body-humanoid, human-to-humanoid, motion-imitation, sim-to-real, control-framework]
draft: false
references:
  - title: HOVER project page
    url: https://hover-lab.github.io/
  - title: Official repository
    url: https://github.com/LeCAR-Lab/HOVER
  - title: Paper
    url: https://arxiv.org/abs/2411.10488
---

## 1. 定位

[HOVER](https://hover-lab.github.io/) 是 human-to-humanoid whole-body control 研究框架：将人类全身运动转为具备双臂、双腿和足部接触的人形机器人可执行技能。它的直接价值是建立“人类动作先验 → robot retarget → 物理闭环稳定性”的评测链，而非提供像 HumanoidBench 那样固定的多任务移动操作排行榜。[官方代码](https://github.com/LeCAR-Lab/HOVER)

## 2. 输入、输出与评测

| 输入 | 输出 | 应评估什么 |
|---|---|---|
| 人类全身运动、目标 humanoid 资产、关节映射与控制器 | robot joint target/控制动作及仿真 rollout | root/手/脚 tracking、跌倒、足滑、joint/torque limits、接触一致性 |
| 扰动、初始姿态、物理参数 | 闭环恢复轨迹 | push/参数扰动下的恢复成功率与稳定性 |
| 若接入物体任务：物体几何/pose 与接触目标 | 全身移动操作 rollout | 另报 grasp/hold/place success、掉落、物体碰撞；不可从纯 motion tracking 推断 |

## 3. 部署与边界

按[官方仓库](https://github.com/LeCAR-Lab/HOVER)锁定训练代码、simulator、robot asset 与 motion-data 依赖。复现时应公开人体数据版本、retarget 配置、控制频率和 test sequence；按 subject/sequence 拆分以避免同一动作片段泄漏。HOVER 适合补足 AMASS/GRAB/OMOMO 到 humanoid 执行的低层验证，但并非原生的长时程双手物体操作 benchmark。
