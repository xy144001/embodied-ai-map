---
title: AMASS：统一人体动作档案，用于人形运动先验与模仿
category: evaluation
kind: dataset
organization: Max Planck Institute for Intelligent Systems
releaseDate: 2019-06-01
summary: 将多个公开 MoCap 数据源统一为 SMPL/SMPL-H/SMPL-X 参数化人体运动的档案；常用于 humanoid locomotion/motion imitation 的参考动作与姿态先验，不直接提供机器人控制标签。
tags: [whole-body-humanoid, motion-capture, motion-imitation, retargeting, locomotion]
draft: false
references:
  - title: AMASS archive
    url: https://amass.is.tue.mpg.de/
  - title: AMASS paper
    url: https://arxiv.org/abs/1904.03278
  - title: HumanML3D processing repository
    url: https://github.com/EricGuoICT/HumanML3D
---

## 1. 数据卡

[AMASS](https://amass.is.tue.mpg.de/)（Archive of Motion Capture as Surface Shapes）把多个 MoCap 数据集统一成参数化人体 surface/motion 表示。它的价值在于跨来源的全身运动格式统一：root trajectory、body pose、形状与（随子集/模型）手部信息可被处理为 SMPL 系列参数。访问受各原始数据集许可影响，通常需要注册/分别同意条款。[论文](https://arxiv.org/abs/1904.03278)

| 数据 | 包含 | 适用评测 | 不包含 |
|---|---|---|---|
| 人体运动 | 统一的全身 MoCap/SMPL 参数、帧率和来源元数据 | locomotion imitation、motion prior、retarget、扰动恢复 | robot action/torque、真实接触力、通用物体交互标签 |
| 子集多样性 | 日常活动、行走/跑跳、表演/运动等，覆盖随原始 corpus 变化 | 未见运动/subject/source 泛化 | 固定的 humanoid task success protocol |

## 2. 怎样用于仿真评测

1. 在训练/测试 split 前先按原始 corpus、subject、sequence 划分，避免同一 capture session 的片段泄漏。
2. 由 SMPL body points 或关节旋转做 humanoid retarget，明确 root scaling、关节映射、手部忽略/映射规则和 PD/torque controller。
3. 输入可为当前 robot state + future reference frames/phase；输出为全身 joint target 或 torque。
4. 评估应同时报告 tracking（root/关节/关键点误差）、物理可行性（跌倒、足滑、关节/力矩限位、接触）和鲁棒性（外推、推扰、未见轨迹）。只报 pose MSE 无法判断双足稳定性。

AMASS 最常用于“低层人形运动技能”或生成模型的运动质量评估；将其与 GRAB/OMOMO 或 HumanoidBench 组合，才能覆盖物体操作与终端成功。

## 3. 部署与限制

下载后先检查 SMPL/SMPL-X body model 的独立许可和所取 AMASS 子集条款。转换时固定坐标系、单位、fps 和 joint convention；将 source motion、retargeted trajectory 与 robot XML/URDF 一起版本化。AMASS 的人类动作本身没有机器人动力学保证，尤其在手持物、换支撑和高扭矩动作上必须在目标仿真器重放验证。

## 4. 代表工作怎样训练、怎样测试

| 工作 | 训练时怎样用 AMASS | 测试时给什么、看什么 | 这个测试实际证明什么 |
|---|---|---|---|
| [HumanML3D](https://github.com/EricGuoICT/HumanML3D) | 从 AMASS/其他来源动作提取统一 22-joint motion feature，并配对文本描述训练 text-to-motion 模型 | 使用固定 `train/val/test.txt`；输入文本，输出人体 motion；用 motion feature evaluator 计算 FID、R-precision、Diversity、Multimodality | 文本—人体动作生成质量，不是 humanoid 动力学能力 |
| [HuMoR](https://arxiv.org/abs/2009.03329) | 以 AMASS 的 SMPL 关节旋转和 root motion 训练条件 VAE motion prior：由过去身体状态预测下一状态分布/latent | 下游测试输入单目 2D 人体观测，推断完整 3D SMPL motion；报告 MPJPE、PA-MPJPE、加速度和全局轨迹误差 | AMASS motion prior 能帮助人体 3D 恢复平滑/补全；测试集并非 AMASS 本身 |
| Human2Humanoid / HOVER / ASAP 一类 motion-imitation 工作 | 将 SMPL/SMPL-H pose、root translation 重定向为目标 humanoid reference；policy 输入 robot state 与 reference phase/future pose，监督或强化学习得到全身控制 | 对 hold-out motion 或扰动 episode，测 root/末端 tracking、足滑、跌倒、关节/力矩越界及有时的真机完成率 | 人类 motion 是否可在目标 robot 动力学上稳定执行 |

训练/测试必须按原始 corpus、subject 或完整 sequence 划分；把同一录制片段切窗后同时放进 train/test 会让 motion tracking 和生成指标虚高。若最终目标是搬运，还需在 HumanoidBench/SIMPLE 等物理任务中另报 object success。
