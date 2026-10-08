---
title: Benchmark 原生机器人本体与控制量图谱
category: evaluation
kind: guidance
organization: Embodied AI Map
releaseDate: 2026-09-09
summary: 逐条锁定本目录 17 个 Benchmark 条目（不含 AlphaBrain 编排层）的原生机器人型号、策略输出的控制量与动作语义，给出跨 Benchmark 适配必须保存的 6 个字段，并用本轮实测的五种动作向量印证“维数相同不等于物理量相同”。
tags: [whole-body-humanoid, benchmark, embodiment, action-space, control-interface]
draft: false
references:
  - title: LIBERO 官方仓库
    url: https://github.com/Lifelong-Robot-Learning/LIBERO
  - title: HumanoidBench 项目页
    url: https://humanoid-bench.github.io/
  - title: SIMPLE 项目页
    url: https://psi-lab.ai/SIMPLE/
  - title: RoboCasa 官方仓库
    url: https://github.com/robocasa/robocasa
  - title: RoboTwin 官方仓库
    url: https://github.com/RoboTwin-Platform/RoboTwin
  - title: LeVERB 论文
    url: https://arxiv.org/abs/2506.13751
---

## 1. 这张表解决什么问题

“7 维动作”在不同 Benchmark 里是不同的物理量：LIBERO 的 7 维是**末端位姿增量**，CALVIN 的 7 维是**相对末端动作**，而 H1 + 双 Shadow Hand 的全身动作是 **61 维**、RoboCasa-GR1 的 GR-1 是 **29 维**。按维数对齐接口一定错位——接口的真正内容是**每一维的物理语义**。

本页逐条锁定每个 Benchmark 的原生机器人型号与策略控制量。“原生支持”只指官方任务、配置、资产或论文明确出现的本体；底层仿真器理论上能导入的模型不计入。

| 口径 | 含义 | 示例 |
|---|---|---|
| 已锁定 | 官方 runner / 论文 / 仓库配置给出型号与动作维数、关节顺序 | HumanoidBench H1 61D、Mimicking-Bench 19D |
| 官方配置 | 型号由官方提供，动作维数随 robot / controller 配置拼接 | BEHAVIOR-1K、ManiSkill、Habitat-Lab |
| 变体 | 官方扩展或多 embodiment，动作空间按变体单列 | RoboCasa-GR1 29D、RoboTwin 的 ARX / Franka profile |
| 未锁定 | 公开资料没有可独立复核的统一动作向量 | LeVERB-Bench（高层 latent + WBC 解码） |

AlphaBrain Platform 不属于本表：它是 LIBERO、CALVIN、RoboTwin、RoboCasa365、SimplerEnv、BEHAVIOR-1K 等套件的编排/适配层，机器人和 action space 继承目标套件，不构成独立的本体标准。

## 2. 17 个 Benchmark 条目的原生本体与控制量

表中 RoboCasa-GR1 为官方扩展变体行，不计入 17 个条目。

| Benchmark | 原生本体 | 策略控制量 | 控制器 / 频率 | 适配状态 |
|---|---|---|---|---|
| [HumanoidBench](../../benchmarks/humanoidbench/) | H1 + 双 Shadow Hand（主实验）；仓库另有 H1 原生手、H1 + Robotiq 2F-85、G1 三指手、Digit | 61D 连续动作＝H1 身体 19 + 每手 21；position target 或 torque | MuJoCo / MJX，50 Hz | 已锁定 |
| [Mimicking-Bench](../../benchmarks/mimicking-bench/) | Unitree H1（19 关节） | 19D；position / velocity / torque 三种控制语义 | Isaac Gym，50 Hz | 已锁定 |
| [SMPLOlympics](../../benchmarks/smplolympics/) | SMPL / SMPL-X 参数化物理人形（非量产型号） | PD joint-position target；latent 变体输出 embedding 再由低层策略解码 | Isaac Gym，30 Hz | 已锁定（参数化本体） |
| [LeVERB-Bench](../../benchmarks/leverb-bench/) | Unitree G1 | 高层 latent behavior → dynamics-level WBC 解码为关节量；统一动作维数未公开 | Isaac Sim 渲染 + WBC | 未锁定 |
| [SIMPLE](../../benchmarks/simple/) | G1 + Inspire 灵巧手；框架另支持 Franka / ALOHA / 轮式机器人 | 无统一维数：decoupled WBC 与 SONIC WBC 两条控制链 | MuJoCo 3.3 + Isaac Sim 4.5 | 随控制链变化 |
| [BiGym](../../benchmarks/bigym/) | H1 上身 + Robotiq 2F-85；浮动基座移动 | joint position 或 torque；floating-base 另有 pelvis x / y / yaw | MuJoCo | 随配置变化 |
| [LIBERO](../../benchmarks/libero/) | Franka Panda 单臂 + 平行夹爪 | 7D 末端增量＝Δpos 3 + Δrot 3 + gripper 1 | robosuite / MuJoCo，20 Hz | 已锁定 |
| [LIBERO-plus](../../benchmarks/libero-plus/) | Franka Panda（仅扰动初始状态，不换型号） | 继承 LIBERO 的 7D 末端增量 | robosuite / MuJoCo | 已锁定 |
| [CALVIN](../../benchmarks/calvin/) | Franka Panda 单臂 | 7D 相对末端动作（与 LIBERO 的 7D 语义不同） | PyBullet 内置控制器 | 已锁定 |
| [RoboTwin 2.0](../../benchmarks/robotwin/) | AgileX ALOHA 双臂；官方 profile 另含双 ARX X5、双 Franka | 14D 双臂关节（每臂 7，含夹爪通道），归一化 [-1,1] | SAPIEN | 已锁定（主榜）+ 可选 profile |
| [RoboCasa / RoboCasa365](../../benchmarks/robocasa/) | PandaOmron（Panda 臂 + Omron 底盘，旧名 PandaMobile） | 12D＝base motion 4 + control-mode 1 + EE 位姿 6 + gripper 1 | robosuite + MuJoCo，20 Hz | 已锁定（365 默认） |
| RoboCasa-GR1（官方扩展） | Fourier GR-1 双臂 + 灵巧手 + 腰部 | 29D 关节级动作（DiT4DiT 权重实测） | robosuite-GR1 | 变体，按 embodiment 单列 |
| [BEHAVIOR-1K](../../benchmarks/behavior-1k/) | R1Pro（2026 Challenge 默认）；另 Fetch / TIAGo / Stretch / R1 | 底盘 + 头 + 躯干 + 单双臂 + 夹爪按所选机器人拼接；无跨本体统一维数 | OmniGibson → Isaac Sim / PhysX | 随配置变化 |
| [Habitat-Lab](../../benchmarks/habitat-lab/) | Fetch / Franka / Stretch 2 / Spot；Habitat 3 另有 humanoid agent | PointNav 离散 move / turn 或底盘速度；Rearrange 组合 base + arm + gripper | Habitat-Sim | 随 task 配置 |
| [ManiSkill](../../benchmarks/maniskill/) | Panda / Fetch / WidowX / xArm / UR10e / SO-100 / Allegro / G1 / H1 / Go2 等 | 关节、速度、末端、力矩多控制模式；维数从 `env.action_space` 读取 | SAPIEN（GPU 并行） | 随配置变化 |
| [MS-HAB](../../benchmarks/mshab/) | Fetch 移动操作体 | 13D normalized delta-pos＝底盘 2 + 躯干 3 + 臂 7 + 夹爪 1 | ManiSkill 3 / SAPIEN | 已锁定（基线） |
| [SimplerEnv](../../benchmarks/simplerenv/) | Google Robot / WidowX 250s + Bridge | 7D 末端＝Δxyz 3 + axis-angle 3 + gripper 1；IK + Ruckig 转关节目标 | SAPIEN / ManiSkill2_real2sim | 已锁定 |
| [SPARK](../../benchmarks/spark/) | Unitree G1（论文重点）；另 AgiBot G1、R1 Lite、iiwa 14、Kinova Gen3 | nominal action → filtered safe action；一阶 velocity 或二阶 acceleration / force | MuJoCo / Isaac Sim | 随 robot dynamic config |

按本体类别统计：6 个双足/物理人形、7 个机械臂/移动操作/双臂、4 个平台型 Benchmark 栈；平台栈的动作维数随环境配置变化。

## 3. 跨 Benchmark 适配必须保存的 6 个字段

| 字段 | 具体记录 | 不记录会发生什么 |
|---|---|---|
| robot model | 厂商 + 型号 + 手/夹爪 + fixed / mobile / floating-base 变体 | 把 G1、H1、Panda 的结果误当成同一难度 |
| action semantics | 关节绝对/增量位置、速度、力矩，或末端位姿、底盘速度、高层 latent | 维数相同但物理意义不同 |
| action order | 每一维对应哪个关节/末端/夹爪；是否含终止位 | adapter 接对 shape 却驱动错关节 |
| controller | PD / IK / OSC / WBC，增益、限幅、归一化范围 | 把高层目标误称为电机命令 |
| timing | policy Hz、physics Hz、action repeat、chunk 长度、延迟 | 同一动作在不同时间尺度下不可比 |
| scope | 官方默认、官方可选、论文演示、第三方适配 | 把“仿真器兼容”夸成“Benchmark 原生支持” |

## 4. 本轮实测出现的五种动作向量

把已公开方法部署到这些 Benchmark 后，实际处理过的动作向量如下（详见[方法部署记录](../../reproductions/policy-deployment-records/)）：

| 本体（来源） | 维数 | 逐维拆解 | 执行方式 |
|---|---:|---|---|
| Franka Panda（LIBERO） | 7 | Δx, Δy, Δz, Δroll, Δpitch, Δyaw, gripper | 末端增量 → OSC 转关节 |
| PandaOmron（RoboCasa / 365） | 12 | base 4 + mode 1 + EE-pos 3 + EE-rot 3 + gripper 1 | 底盘 + 末端混合，20 Hz |
| Fourier GR-1 双臂（RoboCasa-GR1） | 29 | 双臂关节 + 灵巧手 + 腰部 | 关节级，需匹配 embodiment |
| Unitree G1 全身（OpenHLM） | 34 | 一次预测 50 步 × 每步 34 维 | 全身策略，输出动作序列 |
| H1 + 双 Shadow Hand（HumanoidBench） | 61 | 身体 19 + 左手 21 + 右手 21 | 关节位置或力矩，50 Hz |

实测结论直接：**本体对得上，官方 evaluator 就能直接沿用**（任务判定与机器人本体解耦）；**本体对不上，连一行可解释的成功率都产不出来**。GR-1 的 29 维权重放进 PandaOmron 的 RoboCasa365 直接无效；Panda 的 7 维末端动作喂不了 G1 全身策略。

## 5. 使用方式

- 选一个 Benchmark 做横向比较前，先读它的“控制量”一列，确认自己的策略输出与官方 action 契约一致，或者明确写成“第三方适配实验”。
- 报告里至少附上第 3 节的 6 个字段；转移评测的边界说明见[Benchmark 对比指南](../comparison-guide/)与[输入与量化指标手册](../input-metrics-guide/)。
- 要复现本页口径：以各官方仓库当前 release 的 robot config、env ID 与 action space 为准，逐条从代码读回维数与关节顺序，不从论文数字推断。
