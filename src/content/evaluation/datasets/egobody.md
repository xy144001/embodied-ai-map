---
title: EgoBody：第一人称、多视角的人体交互感知数据
category: evaluation
kind: dataset
organization: ETH Zürich / Microsoft Research
releaseDate: 2022-01-01
summary: 真实室内社交交互的自我中心与多视角 RGB-D 数据，含眼动、手/头跟踪、SMPL-X/SMPL 人体状态和 3D 场景；适合全身人形感知前端、遮挡和自我中心观测评测。
tags: [whole-body-humanoid, egocentric-vision, rgbd, perception, smplx]
draft: false
references:
  - title: EgoBody project page
    url: https://sanweiliti.github.io/egobody/egobody.html
  - title: Official code and data access
    url: https://github.com/sanweiliti/EgoBody
  - title: Paper
    url: https://arxiv.org/abs/2112.07642
---

## 1. 数据卡

[EgoBody](https://sanweiliti.github.io/egobody/egobody.html) 采集两个交互者在室内 3D 场景中的真实运动；其中一人戴 HoloLens2，形成自我中心视觉与眼动观测。项目页报告 125 sequences、36 subjects、15 indoor scenes、3–5 台 Azure Kinect 的同步多视角 RGB-D、HoloLens2 RGB、眼动、手/头跟踪与深度，以及 SMPL-X/SMPL 标注。[项目页](https://sanweiliti.github.io/egobody/egobody.html)

| 模态 | 内容 | 可评估能力 |
|---|---|---|
| Ego RGB/深度 | 头戴设备同步视觉 | 人形头部相机下的遮挡、视野限制、相对人/物定位 |
| 第三人称 RGB-D | 多机位同步帧 | 多视角重建、teacher/supervision 与 cross-view 比较 |
| 运动/视线 | 眼动、手/头跟踪、SMPL-X/SMPL body state | gaze-conditioned intention、手/头姿态估计、动作预测 |
| 场景 | 15 个室内 3D 场景 | 视觉域/布局泛化；非机器人可执行任务定义 |

## 2. 怎么用于全身仿真/评测

- **感知前端**：用 ego RGB-D 或多视角 RGB-D 输入，输出人体/手/头/视线、相对关系和（若自建）交互意图；按官方 split 或 subject/scene split，报 3D pose/mesh、手部、gaze 与跨场景误差。
- **感知到控制**：把预测而非 GT 的目标/人体状态送入人形仿真器，测导航/避障/接近/协作任务 success、碰撞率、反应延迟；另给 oracle-state 上界。
- **不能直接做的事**：EgoBody 没有 humanoid joint action、双足动力学、物体操作成功标签。它评测的是感知与社会交互观测，不是全身移动操作控制本身。

## 3. 访问、部署与限制

官方 GitHub 明确要求注册、签署 dataset license 后下载。[注册页](https://egobody.ethz.ch/) 因此它是研究可获取数据，非无需授权的直接镜像。数据量大且有多视角同步/标定；先用官方 loader 验证 frame 对齐、坐标系和许可的 SMPL 资产，再转为训练格式。划分中至少隔离 subject 与 scene，不能把同一 interaction 的相邻帧随机拆分。

## 4. 代表工作怎样训练、怎样测试

原始 **EgoBody** 工作以同步 HoloLens ego RGB 与 Kinect multi-view RGB-D 训练/评估人体 3D pose、shape/mesh 估计；官方发布的 MVSet、EgoSet 和 EgoSet_interactee 都给 train/val/test frame 统计。更具体的下游例子 **EgoHMR** 输入第一人称 RGB、场景点云/相机信息，预测相机坐标下的 SMPL pose、shape 与 global translation；在 EgoBody test split 报 MPJPE、PA-MPJPE、PVE、全局平移误差和 scene collision/一致性量。[EgoHMR](https://arxiv.org/abs/2309.04833) 证明感知前端在未见帧/场景中的人体重建，不证明 robot control；接入 humanoid 时应分别比较 GT-body oracle 和 image-predicted body condition 下的避障/协作/操作 success，并按 subject、scene、完整 interaction sequence 隔离。
