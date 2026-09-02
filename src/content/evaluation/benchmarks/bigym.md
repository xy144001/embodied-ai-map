---
title: BiGym：演示驱动的移动双臂操作 Benchmark（迁移参考）
category: evaluation
kind: benchmark
organization: University of Edinburgh / University of Bristol
releaseDate: 2024-07-10
summary: 公开的移动双臂操作 benchmark 与 learning environment，包含 40 个家庭任务、人类演示以及 proprioception、RGB 和三视角 depth 观测；适合评估移动双臂策略，但默认机器人不是双足全身 humanoid。
tags: [mobile-manipulation, bimanual, demonstrations, benchmark, transfer-only]
draft: false
references:
  - title: BiGym project page
    url: https://chernyadev.github.io/bigym/
  - title: BiGym paper
    url: https://arxiv.org/abs/2407.07788
  - title: Official code
    url: https://github.com/NeuracoreAI/bigym
---

## 1. 为什么纳入，但不标作直接全身 benchmark

[BiGym](https://chernyadev.github.io/bigym/) 有 40 个家庭环境任务，从目标到达延伸到厨房清洁；它提供 human-collected demonstrations，并支持 proprioception、RGB 和来自 3 个 camera views 的 depth。[论文](https://arxiv.org/abs/2407.07788) 这使它成为研究“移动平台 + 双臂 + 演示驱动操作”的可靠参考。但它的默认移动本体/任务不等价于有双足足部接触、支撑切换和 humanoid 全身控制，因此本页将其标为**迁移参考**。

## 2. 输入—输出与量化指标

| 层 | 输入 | 输出 | 典型评测 |
|---|---|---|---|
| observation | proprioceptive state、RGB、3-view depth、演示轨迹 | policy observation | state/vision 模态消融 |
| demonstration | 每任务人类采集的行为示范 | action/skill condition | demonstration 数量与泛化消融 |
| action | 移动基座与双臂/末端控制（具体 task/action space 依环境） | rollout | 不能直接当 humanoid joint action |
| task | 家庭场景、物体和目标 predicate | success/failure episode | 从 reach 到 kitchen cleaning 的任务 success |

原论文用 imitation learning 与 demo-driven reinforcement learning 方法在这些任务上进行 benchmark；主指标应为 task success rate，并按任务/观测模态/演示数量报告。若迁移到 humanoid，必须新增 fall、foot slip、whole-body collision、object drop 和支撑切换成功率。

## 3. 与全身人形 benchmark 的连接

BiGym 的演示和家庭任务可以作为高层操作/场景数据来源；转换到 HumanoidBench/SIMPLE 时需重建 humanoid asset、下身 controller、手部自由度、相机位姿和 success predicate。BiGym 的移动双臂成功只能证明该 benchmark 本体上的 mobile bi-manual policy 能力，不能直接证明双足全身 loco-manipulation。

## 4. 访问与部署

官方 [GitHub](https://github.com/NeuracoreAI/bigym) 提供 Python 环境与 benchmark 代码，仓库标注 Apache-2.0。按 release 安装后先跑单任务 demo，再记录 observation/action shape、camera、演示 split、seed 与每任务 success；大规模场景或视频评测时另记录 GPU/渲染配置。
