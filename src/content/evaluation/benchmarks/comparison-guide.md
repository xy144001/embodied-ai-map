---
title: Benchmark 对比：数据类型、判分对象与适用问题
category: evaluation
kind: guidance
organization: Embodied AI Map
releaseDate: 2026-09-02
summary: 用统一矩阵对比核心全身 humanoid benchmark 与 AlphaBrain 适配的操作/长程套件：明确各自的数据、输入输出、成功判定、指标和外部数据集角色，避免把不同本体的分数直接横比。
tags: [whole-body-humanoid, benchmark, comparison, data-modalities, metrics]
draft: false
references:
  - title: HumanoidBench
    url: https://humanoid-bench.github.io/
  - title: Mimicking-Bench
    url: https://mimicking-bench.github.io/
  - title: LeVERB paper
    url: https://arxiv.org/abs/2506.13751
  - title: SIMPLE
    url: https://psi-lab.ai/SIMPLE/
  - title: LIBERO
    url: https://github.com/Lifelong-Robot-Learning/LIBERO
  - title: CALVIN
    url: https://calvin.cs.uni-freiburg.de/
  - title: RoboTwin 2.0
    url: https://robotwin-platform.github.io/leaderboard
  - title: RoboCasa
    url: https://github.com/robocasa/robocasa
  - title: SimplerEnv
    url: https://github.com/allenai/SimplerEnv
  - title: BEHAVIOR-1K
    url: https://github.com/StanfordVL/BEHAVIOR-1K
---

## 1. 四类全身 benchmark 的共同最小单元

四者的最终计分单位都是一个 **closed-loop episode**：给定固定 reset、算法反复读取 observation 并输出 action，物理环境推进直到 success、failure 或 horizon。区别在于每个 benchmark 固定了什么输入模态、任务分布和成功条件。

| Benchmark | 固定任务分布 | benchmark 自带/生成的数据类型 | policy 的典型输入 | policy 输出 | 主判分对象 |
|---|---|---|---|---|---|
| [HumanoidBench](../humanoidbench/) | 12 locomotion + 15 whole-body manipulation | MuJoCo robot/object/scene asset；state、可选头部 RGB、448-taxel tactile、contact/episode log | proprioception；可选视觉/触觉/特权 task state | robot actuator command | 每任务 task success rate |
| [Mimicking-Bench](../mimicking-bench/) | 6 household human-scene tasks | 20K synthetic + 3K real human references、11K object shapes、scene geometry、robot rollout | human reference + robot/scene state；具体视觉依 release | retargeted reference 或全身 control | task success + scene geometry generalization |
| [LeVERB-Bench](../leverb-bench/) | 10 categories、150+ vision-language WBC tasks | retargeted MoCap、ray-traced ego/third-person render、language/task metadata、robot state | image history + language + proprioception | latent behavior + dynamics-level WBC action | vision-language closed-loop success |
| [SIMPLE](../simple/) | 60 loco-manipulation tasks、50 scenes、1K+ objects | scene/object assets、MuJoCo contact state、Isaac Sim visuals、task language/config、planner/VR demonstrations | visual/proprioception + task condition | whole-body action/action chunk | task completion + safety/OOD |
| [LIBERO](../libero/) | 4 个官方 suite、130 tasks（现代接口拆为 5 个 CLI suite） | MuJoCo/robosuite assets、RGB/proprioception、语言与 PDDL、human demonstrations | RGB/proprioception + language | 7D end-effector / robot action（依 adapter） | per-task/suite episode success；终身学习另报 ASR/BWT/F |
| [CALVIN](../calvin/) | 长时程语言 chain（1–5 个连续子任务） | 仿真 Franka、语言指令、可选 RGB/proprioception | image/state + language | 典型 8D joint+gripper action | MTLC/LH-MTLC；按 chain 长度与环境 split 报告 |
| [RoboTwin 2.0](../robotwin/) | 50 双臂任务，clean/randomized | SAPIEN assets、50 demo/task、三路相机与域随机化 | 多视角 RGB + task condition | 14D Aloha-AgileX joint action（版本相关） | clean2clean / clean2random success |
| [RoboCasa / RoboCasa365](../robocasa/) | 厨房 atomic/composite；365-task 扩展 | 程序化厨房、任务/场景生成器、LeRobot mixtures | 视觉/状态 + task condition | 机器人相关 action adapter | seen/unseen 与 per-task success |
| [BEHAVIOR-1K](../behavior-1k/) | 1,000 个家居活动（可按子集运行） | OmniGibson/BEHAVIOR assets、活动定义与多对象状态 | 机器人/场景观测 + activity goal | embodiment-specific action | task predicate success + 长程失败类别 |
| [Habitat-Lab](../habitat-lab/) | PointNav/ObjectNav/Rearrange/social nav | Habitat-Sim scenes、RGB-D、GPS/compass 或 state | RGB-D/state + task goal | base velocity 或 mobile-manipulator action | success、SPL、distance 与安全 |
| [ManiSkill](../maniskill/) | 通用操作、灵巧手、移动操作 | SAPIEN assets、state/RGB-D/segmentation | state/视觉/触觉（依 environment ID） | joint/EE/torque action | per-task success、效率与 sim2real gap |
| [SMPLOlympics](../smplolympics/) | individual sport + 1v1/2v2 sports | SMPL/SMPL-X-compatible humanoid、sports assets、可选 motion prior | humanoid/object/opponent state；具体视觉依 env | whole-body control | sport-specific distance/score/win rate + stability |
| [SPARK](../spark/) | safety in humanoid autonomy/teleoperation | state、nominal command、safety constraints、risk logs | robot/environment state + nominal action | filtered safe action | task performance + constraint violation/intervention/latency |
| [BiGym](../bigym/) | 40 mobile bimanual home tasks（迁移） | human demos、proprioception、RGB、3-view depth | demo + state/visual observation | mobile-base + bimanual action | task success；非双足 humanoid score |
| [MS-HAB](../mshab/) | TidyHouse/PrepareGroceries/SetTable（迁移） | RL/IL demos、state、2×RGB-D | low-level state/visual observation | navigation + manipulation control | subtask/long-horizon success + collision safety |

## 2. 同一“搬运物体”问题在四者里有什么不同

| 问题 | HumanoidBench | Mimicking-Bench | LeVERB-Bench | SIMPLE |
|---|---|---|---|---|
| 你先给模型什么 | 环境状态或相机/触觉 | 一段人类交互参考 + 新对象几何 | 图像 + “做什么”的语言 | 场景视觉 + 任务目标/指令 |
| 真正难点 | 在固定物理任务中不跌倒并达成物体目标 | 人类动作能否迁移到未见几何 | 看懂指令/视觉后选对全身行为 | 走、看、接触、搬运、放置的长链路 |
| 不能只看什么 | reward 或手离物体的距离 | human-motion tracking error | 离线 language/latent accuracy | action prediction loss 或 demo replay |
| 最后要看什么 | object/task predicate + robot 存活 | interaction predicate + physical executability | 指令条件下实际闭环完成 | object/task completion + fall/drop/collision |

## 3. 数据集在 benchmark 中的正确身份

外部 Dataset 不是 benchmark 的“答案文件”。它通常扮演四种角色：

| 数据角色 | 例子 | 进入哪个环节 | 最终不替代什么 |
|---|---|---|---|
| motion prior | AMASS、HumanML3D | train low-level WBC / language-motion representation | target benchmark success |
| contact/interaction prior | GRAB、OMOMO | retarget、hand-object contact、object trajectory condition | robot physical grasp/hold/place |
| visual pretraining | BEHAVE、H2O、EgoBody | object/hand/body pose or ego vision front end | simulator 中实时 perception-to-action |
| cross-embodiment policy pretraining | RH20T、Open X | VLA/action representation pretraining | humanoid action decoding 和目标场景闭环 |

因此正确实验表述应是：**“用 GRAB 预训练接触表示后，在 HumanoidBench 的 `g1-package-v0` 上报告 20 个 evaluation seeds 的 success/fall/drop。”** 而不是“GRAB 的接触 F1 提升，所以 humanoid 搬运能力提升”。

## 4. 选 benchmark 的实用决策

- 要比较低层全身控制、接触、分层 walk/reach skill：选 **HumanoidBench**。
- 要研究 human-to-humanoid、未见家具/物体几何：选 **Mimicking-Bench**。
- 要研究图像 + 语言如何触发稳定 WBC：选 **LeVERB-Bench**。
- 要比较 VLA/WAM、场景级移动操作和数据生成策略：选 **SIMPLE**。

无论选择哪一个，报告都应附 task list、asset version、action adapter、observation fields、evaluation seeds、success predicate 和失败类别；这样“benchmark 分数”才是可复查的科学结果。
