---
title: 全身人形机器人仿真与评测地图
category: evaluation
kind: roadmap
organization: Embodied AI Map
releaseDate: 2026-09-02
summary: 面向具有双臂双手和双腿双脚、需要在移动或换支撑中操作的全身人形机器人的仿真平台、评测基准与可获取数据集导航。
tags: [whole-body-humanoid, simulation, evaluation, locomanipulation, roadmap, overview]
draft: false
references:
  - title: HumanoidBench
    url: https://humanoid-bench.github.io/
  - title: Isaac Lab humanoid imitation-learning documentation
    url: https://isaac-sim.github.io/IsaacLab/develop/source/overview/imitation-learning/humanoids_imitation.html
  - title: Mimicking-Bench
    url: https://mimicking-bench.github.io/
---

## Overview：这里的“全身”是什么

本文只把**有双臂/手、双腿/脚，且需要站立、行走、改变支撑关系并在移动中操作物体**的系统计为核心对象。单机械臂、轮式移动操作、四足、仅上半身双臂桌面操作可作为迁移数据或软件组件，但不能证明全身人形的 loco-manipulation（移动操作）能力。

本目录把“平台”分成两层：**仿真引擎/训练栈**负责把状态、传感器、动作和物理接起来；**基准**额外固定任务、初始条件、成功判定与汇总规则。不要把“可加载人形 URDF”误报为“已有全身评测基准”。

## 导航

### 仿真与评测平台：部署算法到虚拟 humanoid

| 平台 | 类型与定位 | 直接全身程度 | 入口 |
|---|---|---:|---|
| Isaac Lab / Isaac Sim | GPU 并行仿真、数据生成、训练与闭环评测栈 | 高：已有 G1、H1、Digit、GR1 相关环境，但任务协议可配置 | [条目](../platforms/isaac-lab/) |
| MuJoCo + MJX | 可微/向量化刚体物理底座 | 中：可承载全身任务；需自行定义基准与资产 | [条目](../platforms/mujoco-mjx/) |
| Genesis World | Python 多物理仿真与批量学习平台 | 中：可建人形流程；不是固定全身任务基准 | [条目](../platforms/genesis/) |
| SAPIEN + ManiSkill | 高吞吐操作仿真/基准栈 | 迁移：现成任务以操作为主，非双足全身基准 | [条目](../platforms/sapien-maniskill/) |
| OmniGibson + BEHAVIOR | 家庭场景与长时程交互仿真 | 迁移：场景/任务丰富，原生重点非双足全身控制 | [条目](../platforms/omnigibson-behavior/) |
| InternUtopia（原 GRUtopia） | 城市/社会场景的导航与移动操作栈 | 迁移：高层场景丰富，非专用双足全身基准 | [条目](../platforms/internutopia/) |
| 平台部署审计 | 准入条件、官方硬件需求、安装路径与实验留档 | 只保留可将算法接入虚拟 robot 并运行 rollout 的系统 | [指南](../platforms/deployment-audit/) |

### 控制参考实现：可运行方法，不等同通用仿真平台

| 实现 | 在本地图中的位置 | 入口 |
|---|---|---|
| ASAP / HumanoidVerse | 跨模拟器/真机物理对齐全身技能栈 | [条目](../platforms/asap-humanoidverse/) |
| HOVER | human-to-humanoid 动作重定向、模仿与物理可执行性 | [条目](../platforms/hover/) |
| Humanoid-Gym | humanoid locomotion/sim-to-real 下身控制基础 | [条目](../platforms/humanoid-gym/) |
| UniHCP | 统一多技能/跨本体全身控制方法 | [条目](../platforms/unihcp/) |

### Benchmark：固定任务协议，并与数据集关联

| Benchmark | 直接全身程度 | 核心数据关联 | 入口 |
|---|---:|---|---|
| HumanoidBench | 高：27 个 locomotion + whole-body manipulation 任务 | AMASS/GRAB/OMOMO 可作技能或接触先验；最终按环境 rollout 计分 | [条目](../benchmarks/humanoidbench/) |
| Mimicking-Bench | 高：6 个家庭 humanoid-scene interaction 任务 | 以人类动作与交互几何为核心，适配 AMASS/GRAB/OMOMO/BEHAVE | [条目](../benchmarks/mimicking-bench/) |
| LeVERB-Bench | 高：150+ vision-language WBC 任务（论文报告） | MoCap 重定向与渲染数据；HumanML3D/EgoBody/H2O 可做前端迁移 | [条目](../benchmarks/leverb-bench/) |
| SIMPLE | 高：60 task / 50 scene 候选（项目报告） | Open X/RH20T 作 VLA 预训练，GRAB/BEHAVE/OMOMO 作接触与感知先验 | [条目](../benchmarks/simple/) |
| Benchmark—数据集关联总览 | 明确数据角色、去泄漏和闭环计分 | 连接全部数据集与目标 benchmark | [总览](../benchmarks/overview/) |
| Benchmark 对比指南 | 横向解释任务、数据模态、输入输出与 success predicate | 防止把 data metric 当作 benchmark score | [指南](../benchmarks/comparison-guide/) |
| Benchmark 输入与量化指标手册 | 统一定义 observation、action、success 与安全/效率诊断量 | 用于复现与横向比较 | [手册](../benchmarks/input-metrics-guide/) |

### 数据集

| 数据集 | 主要角色 | 对全身评测的价值 | 入口 |
|---|---|---|---|
| GRAB | 全身抓取 MoCap | 物体接触、手-躯干协同重定向 | [条目](../datasets/grab/) |
| BEHAVE | RGB-D 人-物交互 | 从视觉观测到人/物/接触估计与场景重放 | [条目](../datasets/behave/) |
| OMOMO | 大物体全身操作 | 双手搬运、行走/转身与物体轨迹条件生成 | [条目](../datasets/omomo/) |
| AMASS | 大规模统一 MoCap 档案 | locomotion/姿态先验、retarget 与 motion imitation | [条目](../datasets/amass/) |
| HumanML3D | 语言—3D 人体动作 | 自然语言运动意图与动作生成前评测 | [条目](../datasets/humanml3d/) |
| H2O | 第一人称双手—物体交互 | 手—物视觉与双手操作模块，非双足原生 | [条目](../datasets/h2o/) |
| EgoBody | 自我中心多模态社交动作 | 人形感知、遮挡、第一人称感知评测 | [条目](../datasets/egobody/) |
| RH20T | 人类演示配对的机器人多模态轨迹 | 操作策略预训练/one-shot 转移，非全身人形原生 | [条目](../datasets/rh20t/) |
| Open X-Embodiment | 跨机器人 RLDS 数据联盟 | 通用 VLA 预训练与跨本体对照，非全身人形原生 | [条目](../datasets/open-x-embodiment/) |
| 数据集评测协议 | 数据→重定向→物理闭环的统一口径 | 连接全部数据集与目标 humanoid 任务环境 | [指南](../datasets/evaluation-protocols/) |
| 数据集文件结构与字段 | 原始目录、容器、字段语义与仿真变量映射 | 防止将人体 pose 或异构 arm action 误作 robot command | [指南](../datasets/file-formats/) |

## 宏观路径分类

### 平台：三条路线

1. **任务锁定的全身基准**：HumanoidBench、Mimicking-Bench。优点是任务、随机化、成功条件相对固定，可以横向比较；代价是机器人模型、观测和任务分布受基准约束。
2. **生产级仿真—数据—部署栈**：Isaac Lab/Isaac Sim。重点是 GPU 并行、传感器合成、域随机化、数据集生成、训练/部署闭环；评测可严格但需要研究者自己冻结版本、种子、任务 JSON/配置和统计规则。
3. **物理底座与研究原型栈**：MuJoCo/MJX、Genesis。适合快速搭建控制器、motion imitation、接触/动力学消融；它们本身不提供公平比较所需的完整协议，论文必须公布资产、动作接口和 success predicate。

### 数据：四条路线

1. **运动先验**（AMASS、HumanML3D）：覆盖走、跑、转身和语言意图；通常没有物体动力学，适合低层运动、文本条件动作和 retarget，而非终端任务成功率。
2. **全身人—物几何/接触**（GRAB、BEHAVE、OMOMO）：提供人体、物体和接触或相对运动，可用于把人类参考动作映射到人形、构造接触奖励和测试未见物体；但人体骨架/手与机器人执行器不等价。
3. **视觉/自我中心交互感知**（EgoBody）：强调真实遮挡、多视角 RGB-D、头戴相机、眼动与人体状态；适合 perception-to-control 前端，不能直接替代机器人关节控制数据。
4. **跨本体机器人操作数据**（RH20T、Open X-Embodiment）：含真实机器人动作和多模态观测，适合 VLA/模仿学习预训练；大多是固定底座机械臂或非全身移动操作，报告全身结论前必须在 HumanoidBench/Isaac Lab 等目标本体上再评测。

## 统一评测范式（每个新工作都应交代）

| 层 | 输入必须冻结 | 输出/记录 | 至少报告的量 |
|---|---|---|---|
| 任务 | 任务文本、场景资产版本、初始状态/随机种子、训练/测试划分 | 每回合成功、终止原因、视频 | success rate（均值与种子/置信区间） |
| 感知 | state / RGB-D / tactile 的字段、频率、延迟与噪声 | 观测日志、缺失率 | 按观测模态的消融与 OOD 差值 |
| 控制 | action 含义（关节位置/速度/力矩、base 命令）、频率、动作块长度、限幅 | action、接触力、跌倒/碰撞 | 成功、时间/步数、能耗/平滑度、跌倒率/安全违规 |
| 泛化 | 未见物体、布局、质量/摩擦、地形、指令、机器人参数的拆分 | 每一拆分的逐任务分数 | IID 与每类 OOD 分开，不混成一个平均数 |
| 数据 | 训练数据来源、许可、过滤、human-to-robot retarget 规则 | 样本/轨迹统计、失败样本 | 训练/测试不泄漏；数据量与覆盖度消融 |

## 关联矩阵

平台、数据集、benchmark 和代表工作的证据等级矩阵见[关系矩阵](relationship-matrices/)。矩阵把“官方直接使用/已发表外部使用/仅兼容建议”分别标成 D、E、C，避免把可接入误报为已使用。

## 选择建议

- 想比较一个控制/规划算法：先用 **HumanoidBench**；同时给出状态输入与视觉/触觉输入的差异。
- 想训练具身基础模型或生成合成轨迹：用 **Isaac Lab**，把环境版本、USD/URDF、随机化和 closed-loop 评测脚本一起发布。
- 想验证 human-to-humanoid imitation：用 **Mimicking-Bench**，再以 GRAB/OMOMO/AMASS 明确标注的人类动作为训练或参考来源。
- 只用 AMASS、Open X 或双臂桌面任务的结果只能说明可迁移能力；不能单独写成“全身人形移动操作评测”。
