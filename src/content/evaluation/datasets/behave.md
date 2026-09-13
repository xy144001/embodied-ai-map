---
title: BEHAVE：多视角 RGB-D 全身人—物交互数据集
category: evaluation
kind: dataset
organization: MPI-INF / University of Tübingen
releaseDate: 2022-04-14
summary: 在自然环境中采集的全身人—物交互 RGB-D 数据，带多视角帧、SMPL 人体拟合、物体拟合和接触标注；适合视觉感知、交互重建和仿真场景重放。
tags: [whole-body-humanoid, rgbd, human-object-interaction, perception, contact]
draft: false
references:
  - title: BEHAVE project page
    url: https://virtualhumans.mpi-inf.mpg.de/behave/
  - title: Paper
    url: https://arxiv.org/abs/2204.06950
  - title: Official code and access utilities
    url: https://github.com/xiexh20/behave-dataset
---

## 1. 数据卡

[BEHAVE](https://virtualhumans.mpi-inf.mpg.de/behave/) 是面向自然环境 full-body human-object interaction 的多视角 RGB-D 数据集。论文报告约 15k 帧、5 个地点、8 位受试者与 20 个常见物体；公开的内容包括多视角 RGB-D、对应 3D SMPL 与 object fits，以及接触标注。[论文](https://arxiv.org/abs/2204.06950)[官方代码](https://github.com/xiexh20/behave-dataset)

| 数据类型 | 具体内容 | 在全身人形评测中的角色 |
|---|---|---|
| 视觉 | 多相机 RGB-D 时间帧 | 测试遮挡、深度、跨视角的人/物感知 |
| 人体 | 逐帧 SMPL 拟合 | 估计人体姿态后提供 retarget 参考 |
| 物体 | 物体 3D 拟合/pose | 重放对象运动、目标条件、构造 sim asset |
| 接触 | 人体—物体接触标注 | contact prediction、接触奖励或失败诊断 |
| 场景 | 5 个真实地点与日常对象交互 | 环境变化与视觉背景泛化 |

## 2. 现有评测怎样使用

原始工作针对 human-object joint tracking：输入多视角 RGB-D，输出人体与物体的 3D 参数化状态，并以重建/跟踪误差和接触质量评价。对于 humanoid 研究，应拆成两个阶段：

1. **视觉前端**：训练 split 输入 RGB-D，预测 human pose、object pose、接触；评估 3D pose/mesh 误差、object pose 误差、接触 precision/recall，以及未见地点/物体的退化。
2. **机器人后端**：将已估计或 GT 的物体轨迹与接触序列 retarget 到目标 humanoid，在 MuJoCo/Isaac Lab 闭环执行；评估 object-level success、碰撞/穿透、跌倒、手部接触持续时间和完成时间。

禁止把 GT SMPL/object pose 结果与 RGB-D 输入结果混在同一表中；前者是 oracle state control，后者包含 perception error。

## 3. 部署/格式与划分

使用[官方 repository](https://github.com/xiexh20/behave-dataset)的依赖、数据读取和 contact computation 工具。由于 RGB-D 体积、深度相机标定和 SMPL 许可是常见障碍，首先运行一个 sequence 的 loading/visualization，再批量预处理。按 subject、object、location 或 interaction sequence 划训练/测试，且不要把相邻帧随机分到两侧——那会造成严重时间泄漏。

## 4. 边界

BEHAVE 是人类交互视觉数据，不含机器人关节动作、力矩或真实 robot success 标签。它最适合量化“从视觉看到交互”的可靠性，不能单独作为全身机器人移动操作能力的结论。

## 5. 代表工作怎样训练、怎样测试

**CHORE** 是具象训练/测试例子：训练时输入一张 RGB human-object image，监督模型学习人体/物体连续隐式距离场与 correspondence，随后恢复 SMPL 人体、物体 mesh 和相对 6D pose；测试时输入一张 held-out RGB 图像，报告人体顶点误差、物体 rotation/translation error、Chamfer distance 与 contact/penetration 量。[CHORE](https://arxiv.org/abs/2204.01645) 证明单图人—物 3D 重建，不证明机器人能抓取。后续 **VisTracker** 将输入收缩为单 RGB 视频，仍用 BEHAVE packed GT 的 test split 评估重建。迁到 humanoid 时应把“预测的 human/object state”而非 GT 喂给 policy，并另做同一 episode 的 oracle-vs-prediction closed-loop 对比：抓取/搬运 success、碰撞、掉落、跌倒；随机拆帧不允许，因为同一 sequence 会泄漏物体扫描、背景和相邻姿态。
