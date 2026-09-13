---
title: 具身机器人数据采集系统
category: datasets
kind: guidance
organization: 具身机器人技术地图数据集组
releaseDate: 2026-09-02
summary: 比较全身遥操作、视觉人体、leader-follower、VR/手柄、robot-free 和多模态工作站如何产生可训练数据。
tags: [data-collection, teleoperation, humanoid, robot-learning]
draft: false
references:
  - title: OmniH2O
    url: https://omni.human2humanoid.com/
  - title: HumanPlus
    url: https://humanoid-ai.github.io/
  - title: DROID
    url: https://droid-dataset.github.io/
  - title: UMI
    url: https://umi-gripper.github.io/
---

## 采集范式

| 范式 | 代表系统 | 主要产出 | 适用边界 |
|---|---|---|---|
| 全身遥操作 | H2O、OmniH2O、HumanPlus、TWIST、HOMIE | humanoid 全身参考动作和任务示范 | 映射链较长，需要处理平衡和接触 |
| 沉浸式视觉遥操作 | Open-TeleVision、AnyTeleop | 上身、双臂和手部动作 | 跨本体强，但 retarget 误差需要标定 |
| Leader-follower | ALOHA、GELLO | 目标机器人关节监督 | 精度高，跨本体能力有限 |
| VR/手柄多站点 | BridgeData、DROID | 多场景真实机器人轨迹 | 吞吐量和场景覆盖较好 |
| Robot-free 手持设备 | UMI | 机器人不到场时的环境示范 | 需要可行性修复和动作映射 |
| 多模态接触工作站 | RH20T | 视觉、关节、力/触觉和物体交互 | 标定和同步复杂 |

## 一套系统需要记录什么

机器人和传感器型号、相机内外参、关节定义、控制模式、硬件时间戳、同步误差、控制频率、记录频率、通信延迟、标定版本、操作者和安全中止原因都应成为元数据。

## 系统与数据集的关系

采集系统本身不是数据集。需要另外记录它实际生成了哪些数据包、数据是否开放、是否提供 loader、动作是否可以直接用于策略监督，以及哪些字段只在论文中描述。

引用量和仓库关注度只能作为影响力代理，不能直接解释真实用户人数或数据质量。
