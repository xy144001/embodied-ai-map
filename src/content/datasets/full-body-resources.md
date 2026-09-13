---
title: Full-body 机器人数据与资源
category: datasets
kind: dataset
organization: 具身机器人技术地图数据集组
releaseDate: 2026-09-02
summary: 梳理真正涉及全身协调、移动—操作和平衡—接触耦合的机器人数据、人类上游动作和仿真资源。
tags: [full-body, humanoid, whole-body, loco-manipulation]
draft: false
references:
  - title: H2O
    url: https://human2humanoid.com/
  - title: HumanoidBench
    url: https://humanoid-bench.github.io/
  - title: TWIST
    url: https://github.com/Qinwen Hu/TWIST
---

## Full-body 的判定边界

Full-body 不是“机器人长得像人”，而是 episode 中是否实际控制腿、躯干、双臂或双手，并且任务是否包含移动—操作、平衡—接触或负载转移耦合。

| 层级 | 判定标准 | 代表资源 |
|---|---|---|
| 核心层 | 腿、躯干和臂手协同，或任务明确要求双足平衡与操作联合 | H2O、TWIST、HumanPlus、HOMIE、HumanoidBench |
| 扩展层 | humanoid 或高自由度双臂，但下肢没有持续参与 | RoboMIND、AgiBot World、Open-TeleVision |
| 对照层 | 移动机械臂、四足带臂等相邻形态 | Mobile ALOHA、RoboCasa、BEHAVIOR-1K |

## 重点数据内容

- **全身示范与运动先验**：人体姿态、根部状态、全身关节、足底接触、机器人参考动作。
- **真实机器人轨迹**：视觉、机器人本体状态、动作、任务结果和安全终止信息。
- **仿真 rollout**：任务状态、接触、物体位姿、渲染观测、动作和 termination。
- **人体上游数据**：MoCap、人体视频、人—物接触和语言动作描述，需要 retarget 后才能训练机器人策略。

## Full-body 特有缺口

真实长时程任务、足底接触、根部状态、负载转移、多接触、跌倒和恢复样本仍然稀缺。人体动作与机器人动作之间存在骨骼比例、关节范围和接触条件差异，不能把人体姿态直接当成机器人 action。

## 推荐使用方式

先保留原始人体动作和机器人 retarget 结果，再保存接触与修正信息；训练时区分运动先验、低层跟踪策略和高层任务策略；评测时分别报告 locomotion、操作、全身组合任务和失败恢复。
