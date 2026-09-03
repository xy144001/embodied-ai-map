---
title: SPARK：humanoid 安全控制与遥操作 Benchmark
category: evaluation
kind: benchmark
organization: Carnegie Mellon University Intelligent Control Lab
releaseDate: 2025-02-05
summary: 面向 humanoid autonomy 与 teleoperation 的安全控制 benchmark/toolkit；通过可配置安全准则、不同任务/环境/机器人模型的仿真对比，测试性能与安全约束之间的权衡，并支持 Unitree G1 等硬件部署路径。
tags: [whole-body-humanoid, safety, teleoperation, safe-control, benchmark]
draft: false
references:
  - title: SPARK project page
    url: https://intelligent-control-lab.github.io/spark/
  - title: Paper
    url: https://arxiv.org/abs/2502.03132
  - title: Official code
    url: https://github.com/intelligent-control-lab/spark
---

## 1. Benchmark 卡片：它考“完成任务时是否安全”

[SPARK](https://intelligent-control-lab.github.io/spark/)（Safe Protective and Assistive Robot Kit）不是以日常任务覆盖度为主的 benchmark，而是将**安全约束—任务性能权衡**变成可复现比较对象。官方项目页/论文说明它含多种 humanoid-safe control 仿真任务、可配置安全准则和灵敏度，并支持将合成的安全控制器快速部署到真实硬件，包括 Unitree G1。

它适合回答：在 robot autonomy 或 teleoperation 中，安全过滤器/CBF/优化控制是否能减少碰撞、越界或危险接近，同时尽可能保持任务完成。它不能替代 HumanoidBench 对长时程移动操作、或 SMPLOlympics 对体育动态能力的覆盖。

## 2. 输入、输出与任务数据

| 层 | 输入 | 输出 | 具象含义 |
|---|---|---|---|
| robot/scene state | humanoid 关节/末端状态、环境对象/障碍、人或操作者意图（按模块） | safety monitor 的风险量 | 判断“手是否将撞到人/墙”“关节是否接近限位” |
| nominal command | autonomy policy 或 teleoperator 给出的原始 control | safe controller 的修正前 command | 比较安全层是否过度改变原任务动作 |
| safety specification | 距离、速度、碰撞、关节/工作空间等可配置约束与 sensitivity | 可行集/约束违规判定 | 同一移动动作可设为宽松或严格安全距离 |
| safety controller | nominal action + state + constraints | filtered/safe robot action、rollout、constraint log | 在接近危险时减速、投影或替代原动作 |

## 3. 量化指标：必须同时报安全和性能

| 指标 | 定义方式 | 为什么必须与另一类指标一起报 |
|---|---|---|
| task success / task progress | 完成目标的 episode 比例或任务进度 | 只降低动作幅度可很安全但完全不工作 |
| constraint violation | 碰撞、最小距离/速度/关节限位等约束被违反的次数、比例或累计量；阈值必须公开 | 只报 success 会掩盖危险完成方式 |
| intervention magnitude | safe action 与 nominal action 的差，例如 $\|a_{safe}-a_{nominal}\|$ 或投影次数 | 量化安全层对操作者/策略的侵入程度 |
| minimum clearance / risk margin | episode 内最小人—robot/robot—obstacle 距离或 barrier margin | 区分“未撞上”与“长期危险贴近” |
| computation latency | safety filter 单步耗时、控制频率下能否实时运行 | 安全算法若超过实时预算，真机不可部署 |

推荐结果图应绘制 Pareto 曲线：横轴任务 success/progress，纵轴 violation rate 或 clearance，而不是只公布某一个 safety weight 下的最好分数。

## 4. 代表使用与边界

SPARK 的原始工作以模块化 safe-control 算法在仿真 humanoid autonomy/teleoperation 场景中比较，并提供向 Unitree G1/外部传感器（如 Apple Vision Pro、motion capture）的部署路径。训练或调参时可对不同 safety criterion/sensitivity、任务环境和 nominal controller 扫描；测试时固定 task seed 与 nominal command，比较“无安全层”对“安全层”的 success、violation、intervention 和 latency。

它是全身人形研究的**安全轴 benchmark**：与 HumanoidBench/SIMPLE 一起用时，可将后者的 task policy 作为 nominal controller，再用 SPARK 协议追加安全指标；不能把 SPARK 的安全低违规率解释为已经具备移动操作泛化。

## 5. 访问与部署

官方 [repository](https://github.com/intelligent-control-lab/spark)提供可配置 toolkit、仿真 benchmark 和示例；安装时按所选 backend/robot task 固定版本。真实 G1 部署前应先复现相同 safety constraints、控制频率和 sensor latency；仿真中没有违反约束不自动保证真实接触/感知同样安全。
