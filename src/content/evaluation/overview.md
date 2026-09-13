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
  - title: AlphaBrain Platform
    url: https://www.alphabrain-platform.com/
---

## Overview：这里的“全身”是什么

本文只把**有双臂/手、双腿/脚，且需要站立、行走、改变支撑关系并在移动中操作物体**的系统计为核心对象。单机械臂、轮式移动操作、四足、仅上半身双臂桌面操作可作为迁移数据或软件组件，但不能证明全身人形的 loco-manipulation（移动操作）能力。

本目录把“平台”分成两层：**仿真引擎/训练栈**负责把状态、传感器、动作和物理接起来；**基准**额外固定任务、初始条件、成功判定与汇总规则。不要把“可加载人形 URDF”误报为“已有全身评测基准”。

## 先看结论：Benchmark 不是一条排行榜

对第一次接触具身智能的人，可以先用下面三问定位一个 benchmark：

1. **它测哪条能力轴？** 是走路/平衡、手—物接触、语言长程规划、视觉鲁棒性，还是安全约束？
2. **它的 robot 是否真的需要双足全身？** 桌面双臂或 Franka 的高分，不能直接外推到双足移动操作。
3. **它的数字来自哪里？** 只有锁定任务版本、split、seed、checkpoint 和 evaluator 的 closed-loop rollout 才是可复核的 benchmark score；平台网页自报或论文摘要数字应单独标注。

| 能力轴 | 首选入口 | 适合回答的问题 | 不应据此宣称 |
|---|---|---|---|
| 全身 locomotion + 接触 | [HumanoidBench](../benchmarks/humanoidbench/)、[SMPLOlympics](../benchmarks/smplolympics/) | 机器人能否走、转身、保持平衡并完成接触任务？ | 已具备通用家务或语言泛化 |
| 人类动作重定向与场景交互 | [Mimicking-Bench](../benchmarks/mimicking-bench/)、[LeVERB-Bench](../benchmarks/leverb-bench/) | 人类动作/语言能否转成可执行的全身行为？ | 真实世界成功率或大规模家务覆盖 |
| VLA 桌面/双臂操作 | [LIBERO](../benchmarks/libero/)、[CALVIN](../benchmarks/calvin/)、[RoboTwin](../benchmarks/robotwin/) | 语言条件操作、长程 chain、双臂泛化是否提升？ | 双足平衡、足底接触和跌倒鲁棒性 |
| 家庭场景规模与 sim-to-real | [RoboCasa](../benchmarks/robocasa/)、[BEHAVIOR-1K](../benchmarks/behavior-1k/)、[SimplerEnv](../benchmarks/simplerenv/)、[SIMPLE](../benchmarks/simple/) | 多对象、未见场景或仿真—现实排序是否可靠？ | 只跑一个子集就覆盖全部任务，或把仿真分数当真机分数 |
| 安全与约束 | [SPARK](../benchmarks/spark/) | 完成任务时是否违反安全约束、碰撞或跌倒？ | 低违规率等于高任务泛化 |

这些轴可以组合成一份评测包，但分数必须按 benchmark 分开报告；不存在一个“总分”能替代能力拆解。

## 各评测方面的主流代表

下面按“要回答的研究问题”归纳主流 benchmark。每一类的分数只在同一协议内可比，跨类只能作为能力画像的不同切片。

| 评测方面 | 主流代表 | 主要测量内容 | 读者应记住的边界 |
|---|---|---|---|
| **下肢运动与全身控制** | [HumanoidBench](../benchmarks/humanoidbench/)、[HumanoidOlympics](../benchmarks/smplolympics/)、Isaac Lab humanoid tasks | 行走、平衡、动态接触、全身动作控制 | locomotion 成功不等于会抓取、搬运或理解语言；Isaac Lab 自定义任务不是天然排行榜 |
| **人类动作重定向与交互** | [Mimicking-Bench](../benchmarks/mimicking-bench/)、[LeVERB-Bench](../benchmarks/leverb-bench/)、HOVER | MoCap→robot retarget、手—物接触、视觉/语言触发全身动作 | tracking/penetration 等离线或几何指标，不能替代真实 task success |
| **桌面操作与终身学习** | [LIBERO](../benchmarks/libero/)、[LIBERO-plus](../benchmarks/libero-plus/)、[Meta-World](https://github.com/Farama-Foundation/Metaworld) | 多任务抓取放置、语言条件操作、持续学习与 zero-shot 鲁棒性 | 以固定机械臂为主，不能直接证明双足稳定性或移动操作 |
| **长程语言—动作链** | [CALVIN](../benchmarks/calvin/)、[RoboCasa/RoboCasa365](../benchmarks/robocasa/)、[BEHAVIOR-1K](../benchmarks/behavior-1k/) | 多阶段子任务、语言指令、家庭物体状态变化 | 必须报告 chain/task completion；单步成功率会掩盖长程失败 |
| **双臂与视觉泛化** | [RoboTwin 2.0](../benchmarks/robotwin/)、[BiGym](../benchmarks/bigym/) | 双臂协同、clean→random、移动双臂家庭任务 | 多数是轮式或固定底座，本体动作空间与 humanoid 不同 |
| **导航与空间理解** | [Habitat-Lab](../benchmarks/habitat-lab/)、Habitat 3.0、ObjectNav/PointNav | 目标导航、重排、社会导航、SPL 与路径效率 | 导航指标不能替代接触操控；RGB-D、GPS/compass、oracle state 必须分轨 |
| **家庭规模与真实—仿真一致性** | [BEHAVIOR-1K](../benchmarks/behavior-1k/)、[RoboCasa365](../benchmarks/robocasa/)、[SimplerEnv](../benchmarks/simplerenv/)、SIMPLE | 多对象家务、未见场景、sim-to-real 排序相关性 | 子集结果不能写成全量覆盖；仿真 success 不是现实成功率 |
| **通用操作与高吞吐训练** | [ManiSkill](../benchmarks/maniskill/)、SAPIEN/ManiSkill-HAB | GPU 并行数据采集、跨机器人操作、real2sim/sim2real | 框架可自定义任务；必须锁定 environment ID、资产和 evaluator 才能复现 |
| **安全与约束** | [SPARK](../benchmarks/spark/)、安全控制/遥操作 benchmark | 约束违规、碰撞、跌倒、干预延迟与任务性能权衡 | 安全低违规率不等于任务泛化；应与 success、效率一起报告 |

### 最小阅读顺序

若只想快速建立全局认识：先读 **HumanoidBench**（全身核心）、再读 **LIBERO/CALVIN**（操作与语言链）、**Habitat-Lab**（导航）、**BEHAVIOR-1K/SIMPLE**（家庭规模），最后用 **SPARK** 补安全轴。这样能覆盖“走—看—拿—做—长期执行—安全”六个互补方面。

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
| LIBERO | 中：130 个终身学习操作任务（4 个官方 suite；现代接口拆为 5 个 CLI suite） | 官方 MuJoCo/robosuite 任务与 human demonstrations；非全身 humanoid | [条目](../benchmarks/libero/) |
| LIBERO-plus | 中：LIBERO 多维鲁棒性扰动 | 相机、机器人、语言、光照等 zero-shot 诊断；非新的全身任务集 | [条目](../benchmarks/libero-plus/) |
| CALVIN | 中：语言条件长时程操作 chain | 仿真 Franka、语言与多模态观测；按 MTLC/LH-MTLC 计分 | [条目](../benchmarks/calvin/) |
| RoboTwin 2.0 | 中：50 个双臂操作任务 | SAPIEN、Aloha-AgileX、clean/randomized；非双足全身 | [条目](../benchmarks/robotwin/) |
| RoboCasa / RoboCasa365 | 中：厨房 atomic/composite；365-task 扩展 | 程序化家庭场景与任务生成；按 seen/unseen 分开 | [条目](../benchmarks/robocasa/) |
| SimplerEnv | 迁移评测环境：real-to-sim | 视觉匹配、变体聚合与 sim-real 排序相关性；不是独立 humanoid 榜单 | [条目](../benchmarks/simplerenv/) |
| BEHAVIOR-1K | 中：1,000 个家居活动（实际可按子集运行） | OmniGibson/BEHAVIOR 家庭资产与活动 predicate；非默认双足全身 | [条目](../benchmarks/behavior-1k/) |
| Habitat-Lab | 迁移：PointNav/ObjectNav/Rearrange/社会导航 | Habitat-Sim 场景、RGB-D 与导航 episode；双足需自建接口 | [条目](../benchmarks/habitat-lab/) |
| ManiSkill | 迁移：高吞吐通用操作与跨本体任务 | SAPIEN 资产、GPU 并行 state/RGB-D；任务可自定义 | [条目](../benchmarks/maniskill/) |
| Mimicking-Bench | 高：6 个家庭 humanoid-scene interaction 任务 | 以人类动作与交互几何为核心，适配 AMASS/GRAB/OMOMO/BEHAVE | [条目](../benchmarks/mimicking-bench/) |
| LeVERB-Bench | 高：150+ vision-language WBC 任务（论文报告） | MoCap 重定向与渲染数据；HumanML3D/EgoBody/H2O 可做前端迁移 | [条目](../benchmarks/leverb-bench/) |
| SIMPLE | 高：60 task / 50 scene 候选（项目报告） | Open X/RH20T 作 VLA 预训练，GRAB/BEHAVE/OMOMO 作接触与感知先验 | [条目](../benchmarks/simple/) |
| SMPLOlympics / HumanoidOlympics | 高：全身体育、对抗与动态接触 | SMPL/SMPL-X motion prior 可用于运动技能；项目结果仍按 sport-specific score 计分 | [条目](../benchmarks/smplolympics/) |
| SPARK | 高：humanoid autonomy/teleoperation 安全控制 | 以 task performance 与 safety constraint log 联合计分 | [条目](../benchmarks/spark/) |
| BiGym | 迁移：移动双臂家庭操作，默认非双足 humanoid | 人类 demonstrations 可作上游操作数据；不能替代双足全身测试 | [条目](../benchmarks/bigym/) |
| ManiSkill-HAB（MS-HAB） | 迁移：家居重排与低层全身控制，默认非双足 humanoid | RL/IL demos 与长时程 task graph 可迁移；需重写足部评测 | [条目](../benchmarks/mshab/) |
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

仿真技术栈到具体 benchmark 的选择、原生/适配边界与迁移接口见[仿真方法—Benchmark 适配地图](simulator-benchmark-map/)。

## 选择建议

- 想比较一个控制/规划算法：先用 **HumanoidBench**；同时给出状态输入与视觉/触觉输入的差异。
- 想训练具身基础模型或生成合成轨迹：用 **Isaac Lab**，把环境版本、USD/URDF、随机化和 closed-loop 评测脚本一起发布。
- 想验证 human-to-humanoid imitation：用 **Mimicking-Bench**，再以 GRAB/OMOMO/AMASS 明确标注的人类动作为训练或参考来源。
- 只用 AMASS、Open X 或双臂桌面任务的结果只能说明可迁移能力；不能单独写成“全身人形移动操作评测”。
