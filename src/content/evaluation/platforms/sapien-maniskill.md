---
title: SAPIEN 与 ManiSkill：高速操作评测栈（迁移背景）
category: evaluation
kind: evaluation
organization: SAPIEN / HAOSU Lab
releaseDate: 2023-02-09
summary: 面向 3D 场景理解、机械臂和灵巧操作的仿真与基准栈；可承载自定义人形资产，但现成任务主轴不是双足全身移动操作，故应作为迁移背景而非直接 humanoid benchmark。
tags: [simulation, manipulation, sapien, maniskill, transfer-only]
draft: false
references:
  - title: SAPIEN
    url: https://sapien.ucsd.edu/
  - title: ManiSkill repository
    url: https://github.com/haosulab/ManiSkill
  - title: ManiSkill2 paper
    url: https://arxiv.org/abs/2302.04659
---

## 1. 定位

[SAPIEN](https://sapien.ucsd.edu/) 是用于机器人交互/场景仿真的平台；[ManiSkill](https://github.com/haosulab/ManiSkill) 在其上提供 GPU 并行操作任务、资产和评测工具。其直接优势是机械臂、双臂与灵巧操作的视觉/状态闭环评估，不是现成双足 humanoid 的行走、支撑切换与移动操作基准。[ManiSkill2](https://arxiv.org/abs/2302.04659)

## 2. 统一接口

| 输入 | 输出 | 评测适用性 |
|---|---|---|
| 机器人/物体 URDF、场景、相机、任务 reset/目标 | state/RGB-D/segmentation、接触、reward/done 与关节动作执行结果 | 手—物操作、视觉策略、接触泛化 |
| 自定义 humanoid 全身资产与行动接口 | 需由用户实现的 locomotion/whole-body task | 可以研究，但没有官方全身任务协议 |

## 3. 部署与边界

按[官方仓库](https://github.com/haosulab/ManiSkill)的版本矩阵安装 Python、PyTorch、SAPIEN 和 GPU 依赖；记录 simulator、资产、控制频率和 task config。若把它用于 humanoid，必须自行提供下身控制、落足/跌倒终止、移动操作 success predicate 和 OOD split。仅报 ManiSkill 桌面操作成功率，不能推出全身双足能力。
