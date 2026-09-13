---
title: 数据集如何进入全身人形仿真评测：从原始记录到闭环成功
category: evaluation
kind: guidance
organization: Embodied AI Map
releaseDate: 2026-09-02
summary: 将动作、人—物交互、视觉和跨本体机器人数据用于全身 humanoid 仿真时的统一数据划分、重定向、闭环执行与指标协议，并逐一对应本目录数据集。
tags: [whole-body-humanoid, dataset-evaluation, retargeting, simulation, protocol]
draft: false
references:
  - title: GRAB
    url: https://grab.is.tue.mpg.de/
  - title: OMOMO
    url: https://lijiaman.github.io/projects/omomo/
  - title: Open X-Embodiment
    url: https://github.com/google-deepmind/open_x_embodiment
---

## 1. 先区分：数据集评测的不是同一件事

数据集可以评估**表示/预测**，也可以作为仿真中的**参考或训练来源**；后者最终必须评估机器人是否在闭环物理中完成任务。它们不能互相替代：例如 HumanML3D 的 text-to-motion FID 很低，不能说明机器人能拿着箱子走路；RH20T 的机械臂离线动作预测准确，也不能说明双足人形不会跌倒。

| 评测层 | 固定输入 | 模型输出 | 核心量 | 可使用的数据 |
|---|---|---|---|---|
| 数据内预测 | 官方 train/val/test 的视觉、文本、物体状态或历史运动 | 人体/手/物体 pose、contact、动作或文本对齐 | pose/mesh/6D pose error、contact F1、检索/生成分数 | BEHAVE、EgoBody、H2O、HumanML3D、RH20T、Open X |
| 人类动作生成 | 初始人体状态、object geometry/trajectory、语言 | 未来全身运动/手轨迹 | motion FID、R-precision、多样性、foot skating、手—物误差 | HumanML3D、OMOMO、GRAB、AMASS |
| 重定向可执行性 | 人体参考、robot URDF、场景物理、控制器 | robot joint target/torque trajectory | root/hand/foot tracking、足滑、关节/力矩越界、penetration、跌倒 | AMASS、GRAB、OMOMO、BEHAVE |
| 闭环任务 | 仿真传感器、物体/场景、语言目标；禁止测试时注入 GT 人体轨迹 | 实时全身 action | task success、时间、掉落、碰撞、跌倒、能耗/jerk、OOD success | 任意训练集 + HumanoidBench/Isaac Lab/Mimicking-Bench 等任务环境 |

## 2. 数据到仿真的标准转换

1. **冻结 split**：按 sequence/subject/object/scene 划分；绝不按相邻视频帧随机拆分。跨数据预训练时也要把目标 benchmark 的测试对象、场景和任务排除在训练 manifest 外。
2. **时空对齐**：记录原始 fps、坐标系、长度单位、重力方向和相机标定；将人体 root、物体 6D pose、手/脚关键点同步重采样到控制频率。
3. **retarget，而非复制**：以 root 朝向、足接触相位、双手/物体相对位姿为任务约束，求解目标 robot 的关节参考；检查 joint limit、self-collision、速度/力矩和手部自由度。人体 SMPL/SMPL-X 角度不能直接作为机器人命令。
4. **物理重放**：用目标引擎的 collision mesh、质量、质心和摩擦替换纯视觉 mesh；先测 open-loop replay 是否稳定，再测闭环 policy 是否能从扰动中恢复。
5. **训练/测试运行**：每个测试 episode 从真实仿真观测重新推理。human pose、object pose 的 GT 只能作为 oracle 上界，必须与视觉输入结果分表。

## 3. 统一指标与计算口径

| 指标 | 计算/记录方式 | 适用范围 | 常见误用 |
|---|---|---|---|
| Task success rate | `成功 episode 数 / 总 episode 数`；逐任务、逐 IID/OOD split，报告多 seed 均值和方差/置信区间 | 所有闭环任务 | 用 dense reward 或单段 demo 替代 success |
| 运动跟踪 | root/末端 position error、orientation error、joint error；明确是否对齐根坐标 | AMASS/GRAB/OMOMO retarget | 仅看关节 MSE，忽略跌倒和足滑 |
| Contact F1 | 对每帧/每接触对比较 precision/recall/F1；阈值和接触定义公开 | GRAB、BEHAVE、H2O/OMOMO 衍生接触 | 以网格接近代替真实引擎接触而未标注 |
| 物体操作 | object pose error、grasp/hold duration、drop rate、place success | GRAB/BEHAVE/OMOMO/RH20T transfer | 只报手到物体距离，忽略物体是否被稳定控制 |
| 生成指标 | 在固定 published feature extractor、split 与预处理上计算 FID/R-precision/diversity/multimodality | HumanML3D、OMOMO 生成工作 | 跨 feature extractor 或不同 motion normalization 比 FID |
| 安全/物理 | 跌倒、足滑距离、非预期身体碰撞、penetration、joint/torque limit、接触力超阈、能耗/action jerk | 全身仿真 | 只报成功率，不报告危险失败 |

## 4. 各数据集的“正确评测任务”

| 数据集 | 官方/常见数据内任务 | 推荐的仿真后评测 | 必须隔离的 split | 不应声称 |
|---|---|---|---|---|
| GRAB | 全身抓取生成、手—物接触/姿态 | 未见物体上的 robot grasp/hold/place success、contact 与掉落 | subject、object/mesh、action | 真机全身移动操作 |
| BEHAVE | RGB-D 下 human-object tracking/重建 | 预测视觉状态驱动的抓取/搬运闭环，比较 GT-oracle 与 prediction | subject、object、location、sequence | 有机器人 action 标签 |
| OMOMO | object trajectory→全身 motion；未见 object/motion | 物体轨迹跟踪、双手稳定接触、移动搬运 success | object、motion/trajectory | 动作自然即物理可执行 |
| AMASS | motion prior、tracking、扰动恢复 | 低层站立/走跑跟踪、push recovery、足滑/跌倒/力矩 | source corpus、subject、sequence | 物体操作成功 |
| HumanML3D | text→motion 语义/分布评估 | text-conditioned robot motion 再经物理执行 | 官方 ID split、镜像规则 | 操作与接触泛化 |
| H2O | ego hand/object pose、交互识别 | 感知误差下 bimanual grasp/place；若加行走再另报 loco score | subject、object、action/sequence | 双足全身能力 |
| EgoBody | ego/multiview pose、gaze/interaction perception | 带遮挡的 perception-to-control；报告 oracle gap | subject、scene、interaction sequence | 机器人动力学控制 |
| RH20T | 多模态 one-shot manipulation/离线策略 | 迁移至 humanoid 后的 closed-loop task success 与安全 | robot、task、scene/episode | 原生全身 benchmark |
| Open X | cross-embodiment action/skill transfer | pretrain+target fine-tune 对比；目标 humanoid OOD success | source dataset、target robot/task | RLDS 字段天然同动作语义 |

## 5. 最小可复现实验包

每个论文/页面至少发布：数据 URL 与许可、不可变 manifest（样本 ID、split、过滤 hash）、retarget/config 代码、robot/scene asset hash、observation/action schema、控制频率、随机化和 evaluation seeds、逐 episode CSV/视频。只有这样，数据集上的改进才可以被区分为感知/生成改进、retarget 改进或真正的全身闭环控制改进。
