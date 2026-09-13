---
title: 具身数据格式与处理闭环
category: datasets
kind: guidance
organization: 具身机器人技术地图数据集组
releaseDate: 2026-09-02
summary: 区分文件容器、语义规范、时序同步和 Full-body 专用字段，并说明从采集到评测的数据闭环。
tags: [data-format, rlds, lerobot, synchronization, lifecycle]
draft: false
references:
  - title: RLDS
    url: https://github.com/google-research/rlds
  - title: LeRobot Dataset v3
    url: https://huggingface.co/docs/lerobot/lerobot-dataset-v3
  - title: MCAP
    url: https://mcap.dev/
  - title: robomimic datasets
    url: https://robomimic.github.io/docs/datasets/overview.html
---

## 容器与规范不是一回事

| 层级 | 例子 | 作用 |
|---|---|---|
| 文件容器 | HDF5、Zarr、Parquet、TFRecord、WebDataset | 保存数组、视频和分片 |
| 原始日志 | ROS bag、MCAP | 按时间保存相机、关节、IMU、力传感器话题 |
| 语义规范 | RLDS/TFDS、Open X-Embodiment、LeRobot | 统一 episode、step、observation、action 等字段 |

![RLDS 官方 Episode、Step、Observation、Action、Reward 数据组织结构图](/embodied-ai-map/datasets/images/formats/rlds.png)

图示来源：[RLDS 官方 README 的 Dataset Format](https://github.com/google-research/rlds/blob/master/README.md#dataset-format)。它展示了数据集、episode、step 以及 observation/action/reward 等字段之间的层级关系。

## Full-body 同步要求

人形机器人可能同时记录视觉约 30 Hz、关节约 500 Hz、力/触觉约 1 kHz。必须保存硬件时间戳、时钟来源、同步误差和缺帧策略；简单把所有信号降到同一频率，可能丢失落脚冲击、失衡、接触变化和恢复触发信号。

## 最低字段

- 时间戳、采样频率和 episode 边界；
- observation、可执行 action 和控制模式；
- 机器人、关节、坐标系和传感器标定；
- 任务结果、来源、版本、许可和已知限制。

Full-body 还应保存根部姿态、IMU、全身关节、足底接触、手物接触、负载、安全中止、失衡和恢复原因。

## 数据处理闭环

`采集/生成 → 同步与标定 → 清洗与切分 → 标注 → 质量控制 → 格式统一 → 数据划分 → 训练 → 评测与诊断 → 数据回流`

评测结果需要反向定位任务、场景、失败状态、身体接触或传感信息缺口，再补采数据或重新清洗标注，形成可追踪的数据版本。
