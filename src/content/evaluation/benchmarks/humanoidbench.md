---
title: HumanoidBench：面向全身移动操作的 MuJoCo Benchmark
category: evaluation
kind: benchmark
organization: UC Berkeley / RAI
releaseDate: 2024-03-15
summary: 一个可本地安装的 MuJoCo humanoid benchmark：12 个 locomotion 与 15 个 whole-body manipulation 任务，配有 state、头部视觉和全身触觉观测选择，以及基于任务完成的闭环成功率评测。
tags: [whole-body-humanoid, mujoco, locomotion, manipulation, benchmark, tactile]
draft: false
references:
  - title: Project page
    url: https://humanoid-bench.github.io/
  - title: Paper (RSS 2024)
    url: https://roboticsproceedings.org/rss20/p061.pdf
  - title: Official code
    url: https://github.com/carlosferrazza/humanoid-bench
---

## 1. Benchmark 卡片：它到底在考什么

[HumanoidBench](https://humanoid-bench.github.io/) 将“一个人形控制算法是否好”具体化为 **27 个固定 MuJoCo episode family**：12 个 locomotion 任务与 15 个 whole-body manipulation 任务。[论文](https://roboticsproceedings.org/rss20/p061.pdf)的典型题目不是单臂桌面 pick-place，而是让双足 humanoid 同时解决平衡、落足、躯干姿态、手部接触和物体目标。

| 任务簇 | 具体例子 | 成功需要协调什么 | 仅看什么会误判 |
|---|---|---|---|
| locomotion | walk、run、hurdle、crawl、maze、stair、slide、pole | root 速度/路径、足接触、平衡与避障 | 只看关节 tracking，可能已经跌倒或未到目标 |
| 静态/短程操作 | reach、push、cabinet、door、cube、insert | 手到目标、物体位姿、全身稳定 | 只看末端距离，可能未真正开门/插入 |
| 长时程移动操作 | truck/package、bookshelf、basketball、window、kitchen、room | 行走 + 伸手/双手操作 + 接触序列 + 任务分解 | 只报 dense reward，不能说明最终任务完成 |
| 姿态与稳定 | stand、sit、balance、powerlift | 支撑关系、重心、接触安全 | 只报存活步数，可能偏离目标姿态 |

## 2. 它随 benchmark 带来什么“数据”

HumanoidBench 的主要数据不是离线 demonstration archive，而是**每个 reset 后在线生成的仿真 episode**。官方环境/资产和任务代码决定下列字段；算法可选择其中部分作为 observation。

| 数据层 | 具体字段或资产 | 形状/物理含义 | 如何用于算法 |
|---|---|---|---|
| robot asset | H1/G1 humanoid XML、手部末端（实验可用 H1+双 Shadow Hand，仓库也有三指手/夹爪任务族） | link、joint、actuator、collision geometry、joint limit | 定义 action order、动力学、接触与可用自由度 |
| proprioception | joint angle、joint velocity、actuator/robot state | 当前机器人内部状态；不含“人类动作标签” | 状态 policy 的输入；须列出字段与归一化 |
| task state | 与任务相关的 object pose、velocity、goal/target state | 多数属于仿真器可直接给出的 privileged state | 适合作为 oracle/control 上界；不能与视觉闭环混表 |
| vision | 头部布置的两路 egocentric camera RGB | robot 第一视角图像；受遮挡、相机位姿和渲染影响 | vision policy 的图像输入；需记录分辨率、帧率和延迟 |
| tactile | 全身 MuJoCo tactile grid：论文描述共 448 个 taxels，每个给 3D contact force；手部更高分辨率 | 接触位置/力的离散化读数 | 接触感知或安全约束；报告 force clip/阈值与模态消融 |
| episode log | action、reward、termination、contact、state trajectory、视频（由 evaluator 导出） | 一次闭环执行记录 | 诊断掉落、跌倒、卡死、误碰撞和任务失败 |

**关键边界**：`qpos/qvel/object pose` 是 MuJoCo 在时刻 $t$ 的观测，不是 benchmark 提供的正确 action；policy 的输出仍是按当前 robot XML 定义的连续 actuator control。不同 hand/robot 的 action dimension 和语义不同，不能直接平均比较。

## 3. 输入 → 输出 → 判分：一个具体 episode

以 `g1-door-v0` 为例：reset 将 G1、门、把手和目标初始关系放入场景；算法读取关节状态、可选头部相机和任务状态；它每个 control step 输出 G1 各 actuator 的连续命令。环境推进接触物理后返回新的观测、reward、终止标志和 task info。**最终应问的不是“手是否接近把手”，而是门是否达到任务定义的打开状态，机器人是否仍可站立且 episode 未非法终止。**

| 接口 | 调用方给什么 | 环境回什么 | 必须冻结 |
|---|---|---|---|
| `reset` | env ID、seed、task config | initial observation / simulator state | robot+hand XML、物体/场景版本、随机化分布 |
| `act` | 连续 actuator action；可来自 PPO、SAC、MPC 或分层 policy | next observation、reward、`terminated/truncated`、info | action interpretation、限幅、control Hz、action repeat |
| `evaluate` | checkpoint、evaluation seeds、episode count | per-task success/failure、return、trajectory、video | success predicate、horizon、聚合统计方式 |

## 4. 官方基准怎样给分

- **主指标：task success rate**。每任务分别统计“满足该任务成功 predicate 的 episode 数 / 评估 episode 数”；长时程任务的 dense reward 只能辅助训练，不可替代成功率。[论文](https://roboticsproceedings.org/rss20/p061.pdf)
- **结果拆分**：至少分 locomotion、manipulation、whole-body/long-horizon 三组，并保留逐任务列。一个 `average return` 可以掩盖某些任务 0% success。
- **训练预算要写清**：论文对不同方法使用不同训练范式/预算；复现时须记录 environment steps、wall-clock、seed、低层预训练技能和高层训练算法，不能把有预训练 walk/reach 的 hierarchical policy 与裸端到端 policy 当作同一输入条件。
- **安全与可解释日志**：除 success/return，导出跌倒或提前终止、物体掉落、接触力、完成步数和失败视频。尤其触觉实验应给有/无 tactile、force 阈值和接触传感布局消融。

## 5. 评测时的数据集如何关联

HumanoidBench 本身的 test score来自实时 MuJoCo rollout；AMASS、GRAB、OMOMO 等外部数据集可用于训练 low-level motion skill、human-contact prior 或 retarget，但它们**不改变 benchmark 的官方 success 定义**。报告应分别列：数据集版本/样本 split、retarget 方法、是否预训练，以及最终 HumanoidBench test seeds。详见[Benchmark—数据集关联总览](../overview/)。

## 6. 可运行性与最小复现

官方 [repository](https://github.com/carlosferrazza/humanoid-bench)提供环境、assets、MJX、PPO/SAC/TD-MPC2/Dreamer 入口。README 建议 Python 3.11、`pip install -e .`，并按算法选择 requirements；MJX GPU 路径使用与 CUDA 匹配的 JAX，CPU 路径可做 smoke test。

最小实验：选一个环境 ID → 固定 seed 和 state observation → 跑随机/已存 policy 确认 reset/step/action shape → 记录一条 trajectory → 再做多 seed 训练和独立 evaluation。最终表格要同时给 environment ID、robot/hand、observation fields、action type、control Hz、训练步数、success 与失败类型。

## 7. 结论边界

HumanoidBench 证明的是“在该 robot asset、MuJoCo 接触参数、任务初始分布和 evaluator 下”的全身控制能力。它不单独证明真实硬件鲁棒性、开放世界视觉或自然语言泛化；这些要以真机、视觉域随机化或 LeVERB/SIMPLE 等不同协议补充。
