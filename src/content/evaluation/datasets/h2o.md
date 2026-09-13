---
title: H2O：第一人称双手—物体交互数据集
category: evaluation
kind: dataset
organization: KAIST
releaseDate: 2022-03-03
summary: 面向第一人称双手—物体交互的 RGB-D 与 3D 标注数据集，适合训练人形手—物视觉前端和双手操作模块；不含双足运动，属于全身人形系统的迁移数据而非直接评测集。
tags: [whole-body-humanoid, egocentric-vision, bimanual-manipulation, hand-object-interaction, transfer]
draft: false
references:
  - title: H2O project page
    url: https://taeinkwon.com/projects/h2o/
  - title: Paper
    url: https://arxiv.org/abs/2203.01577
  - title: Official code
    url: https://github.com/taeinkwon/h2o
---

## 1. 数据卡与适用范围

[H2O](https://taeinkwon.com/projects/h2o/) 面向第一人称 human two-hand-object interaction（双手—物体交互）。官方项目和代码提供视觉数据、双手姿态、物体姿态及交互动作相关标注，用于观察日常双手操作。它能补齐全身系统的**手—物感知与双手操作前端**，但没有完整双腿、步态、足底接触或移动/换支撑上下文；不能单独作为全身人形评测集。[论文](https://arxiv.org/abs/2203.01577)

| 数据层 | 具体内容 | 合理用途 |
|---|---|---|
| 第一人称视觉 | RGB-D / 多视角交互视觉（以实际 release 为准） | 手/物检测、遮挡感知、视觉条件 policy 输入 |
| 双手状态 | 两只人手的姿态/运动标注 | 机械手关键点或 grasp intent 监督；需 retarget |
| 物体与交互 | 物体姿态、双手—物体交互/动作信息 | 6D object pose、接触阶段、bimanual task state |

## 2. 在仿真与评测链路中怎么用

1. **视觉前端评测**：输入 ego RGB-D，输出左右手状态、物体 6D pose 或交互阶段；按官方划分或按 subject/object/action 分离，报告手/物位姿误差、交互分类、遮挡和未见物体的性能。
2. **机器人映射**：将预测/GT 的物体与手部目标转到目标 humanoid 的相机坐标、手坐标和手部 action space；动作输出必须经 IK、抓取规划或 policy adapter，而非把人体手关节角直接下发。
3. **闭环复评**：在目标 humanoid 仿真环境以预测视觉结果驱动操作，额外报告 grasp/place success、物体掉落、接触力、碰撞、完成时间；若加入下身，再报告移动操作 success 与跌倒率。

## 3. 获取、部署与局限

从[项目页](https://taeinkwon.com/projects/h2o/)按当前数据许可和下载要求取得数据，配合[官方代码](https://github.com/taeinkwon/h2o)复用标注解析。工程中应固定相机内外参、帧同步、深度单位、左右手定义及坐标变换。第一人称数据遮挡严重；人体手部的关节、摩擦和力能力不等于机器人灵巧手，因此成功的手部 pose estimation 也不保证可执行抓取。

## 4. 代表工作怎样训练、怎样测试

原始 **H2O: Two Hands Manipulating Objects** 工作训练视觉模型从 RGB 输入联合预测左右手 3D pose、物体 6D pose 和 interaction class；监督来自每帧手/物 GT 与交互标签。官方 challenge/repository 提供 subject/sequence 划分：subjects 1–2 和 subject 3 的部分序列训练、subject 3 其余序列验证、subject 4 测试。测试比较手部 3D pose、物体 6D pose 与交互识别；其结论是 first-person hand-object perception。若用作 humanoid 训练数据，应以预测/GT 手-物目标训练抓取前端，并在独立 robot episode 测 grasp/place success、掉落和遮挡鲁棒性；不能把 H2O pose error 作为双足全身成绩。
