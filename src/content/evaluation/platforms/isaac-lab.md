---
title: Isaac Lab / Isaac Sim：面向人形数据生成、训练和闭环评测的 GPU 栈
category: evaluation
kind: evaluation
organization: NVIDIA
releaseDate: 2025-01-01
summary: 基于 Isaac Sim、PhysX 和 Omniverse 的模块化 GPU 并行仿真栈；提供 G1、H1、Digit、GR1 等人形相关环境与 Mimic 数据生成工作流，但评测协议需要研究者显式冻结。
tags: [whole-body-humanoid, isaac-lab, isaac-sim, gpu-simulation, synthetic-data]
draft: false
references:
  - title: Isaac Lab environments
    url: https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html
  - title: Isaac Lab humanoid imitation learning and data generation
    url: https://isaac-sim.github.io/IsaacLab/develop/source/overview/imitation-learning/humanoids_imitation.html
  - title: Isaac Lab Evaluation Tasks
    url: https://github.com/isaac-sim/IsaacLabEvalTasks/
---

## 1. 它解决什么问题

[Isaac Lab](https://isaac-sim.github.io/IsaacLab/main/index.html) 是建立在 Isaac Sim/Omniverse 上的机器人学习框架，不是一张固定排行榜。它提供 manager-based environment、GPU 大规模并行、视觉/深度/接触传感器、USD 资产、随机化、数据采集和训练接口。官方环境列表含 Unitree H1/G1 的平地/崎岖地形 locomotion、Digit 的 `Isaac-Tracking-LocoManip-Digit-v0`，以及 G1 的 pick-and-place locomanipulation 环境；官方 humanoid 文档还给出 GR-1、G1 的 Mimic 生成与训练工作流。[环境目录](https://isaac-sim.github.io/IsaacLab/main/source/overview/environments.html)[人形文档](https://isaac-sim.github.io/IsaacLab/develop/source/overview/imitation-learning/humanoids_imitation.html)

因此它最适合“从资产到闭环评测”的工程链路；若要用于论文横评，研究者必须把 task config、随机化、checkpoint、seed 和 evaluator 一同发布。

## 2. 范式化接口

| 项 | 输入需要准备什么 | 产生什么输出 | 设计/评测注意 |
|---|---|---|---|
| 资产 | 人形 USD/URDF 及关节、碰撞、执行器和驱动参数；场景 USD、物体网格/材质 | PhysX scene、语义标签、可渲染 USD | URDF→USD 后要检查关节轴、惯量、碰撞体和 action ordering |
| 任务 | scene/task config、reward、事件、termination、reset 和 domain randomization | Gymnasium 风格 vectorized env | 任务 ID 同名不代表 randomization 或 success 相同 |
| 观测 | policy state、关节/IMU/接触、RGB/RGB-D/分割、语言或目标位姿；指定频率和延迟 | batched tensor observation 与相机/传感器帧 | 图像与 state 的 timestamp/latency 要对齐；禁止测试用特权 object pose |
| 动作 | joint position/velocity/effort target，或上层 base/hand target + IK/低层 locomotion policy | batched action → PhysX step → next state/reward/done | 分清“全身端到端力矩”与“下身已训练、上身 IK”的能力边界 |
| 数据 | teleoperation / Mimic 轨迹、seed、生成策略和过滤标准 | HDF5 轨迹、图像/状态/动作/标注（具体字段随 workflow） | 数据生成器与 closed-loop evaluator 不能共享测试初始状态 |

官方 Mimic 人形示例将 pick-place demo 进一步和 point-to-point navigation 结合，以生成 G1 locomanipulation 训练数据；同时官方说明下身 locomotion policy 可来自 AGILE、上身操作可分开训练。这是一条可行工程分解，不等于端到端全身策略的同等结果。[人形文档](https://isaac-sim.github.io/IsaacLab/develop/source/overview/imitation-learning/humanoids_imitation.html)

## 3. 推荐的评测协议

1. **固定版本**：记录 Isaac Sim、Isaac Lab、GPU driver、USD/URDF hash、task config 与环境 ID。GPU 物理并行和随机化会使未固定版本的数值难复现。
2. **冻结测试集**：将 scene layout、物体类别/质量/摩擦、目标位置、地形和相机扰动划为 IID 与各类 OOD；训练和测试 seed 分离。
3. **闭环而非 replay**：每个 episode 从传感器重新推理，记录 action 和 success；仅用离线 action MSE 不能证明移动操作完成。
4. **指标**：逐任务 success rate（多 seed）、成功时长/控制步数、跌倒率、碰撞/力阈值违规、能耗或 action jerk；视觉策略另报感知延迟和遮挡 OOD。
5. **分解消融**：分别报告下身预训练、IK、特权目标位姿、Mimic 合成数据和真实数据的贡献，避免把系统工程优势归因为单一模型。

[IsaacLabEvalTasks](https://github.com/isaac-sim/IsaacLabEvalTasks/) 展示了一个可借鉴模式：用预构建的人形（Fourier GR1-T2）工业双臂任务和 closed-loop benchmarking scripts 定量评估 policy；它是人形上身/站立操作实例，不应误标成完整走动全身基准。

## 4. 部署与平台依赖

| 层 | 依赖/方式 | 风险 |
|---|---|---|
| 宿主 | NVIDIA GPU、受支持 NVIDIA 驱动、Linux 是主流开发路径；按 Isaac Sim/Isaac Lab release matrix 配套 Python/OS | Windows/WSL、驱动和 Vulkan/EGL 图形栈常是安装瓶颈；先按官方 release 文档核验 |
| 核心 | Isaac Sim（Omniverse Kit + PhysX）与对应 Isaac Lab release | **不要**将 main 分支 Isaac Lab 任意配到旧 Isaac Sim |
| Python | 通过官方安装方式建立环境，再安装 project tasks/学习算法 | `torch`/CUDA、rl_games/rsl_rl/skrl 等训练包版本需与 release 匹配 |
| headless/规模 | headless 渲染、GPU vectorization、集群调度 | camera/Replicator 会显著增加显存和吞吐压力；报告 env 数与显卡型号 |

## 5. 适用边界

**强项**是视觉合成、场景/资产随机化、并行训练、数据生成与部署链路的统一；**弱项**是“开箱即用的全身排行榜协议”较少。为了可比性，请将代码中所有 task 参数和 evaluator 纳入版本控制；只展示一个 demo 视频或 desktop replay 不构成评测。
