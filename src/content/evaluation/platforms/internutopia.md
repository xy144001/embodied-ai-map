---
title: InternUtopia（原 GRUtopia）：城市场景中的具身导航与移动操作平台
category: evaluation
kind: evaluation
organization: OpenRobotLab / InternRobotics
releaseDate: 2024-07-15
summary: 提供大规模交互场景、社会导航和移动操作基准的通用具身仿真平台；可作为 humanoid 高层场景/任务评测背景，但当前基准并非专为双足全身人形定义。
tags: [simulation, mobile-manipulation, navigation, grutopia, internutopia, transfer-only]
draft: false
references:
  - title: InternUtopia repository
    url: https://github.com/InternRobotics/InternUtopia
  - title: GRUtopia paper
    url: https://arxiv.org/abs/2407.10943
  - title: PyPI package and benchmark documentation
    url: https://pypi.org/project/grutopia/
---

## 1. 定位

[InternUtopia](https://github.com/InternRobotics/InternUtopia) 是 GRUtopia 的后续项目名称。其 README/PyPI 文档列出 GRBench，包括 object loco-navigation、social loco-navigation 与 loco-manipulation benchmark；论文描述 GRScenes 含 100k 可交互、细粒度标注场景，并可组合为城市级环境。[论文](https://arxiv.org/abs/2407.10943)

对全身 humanoid 的价值是：提供更大规模的场景、任务语言/交互对象和移动操作高层评估压力。其限制也必须明确：基准所支持的“mobile manipulation robot”不自动等价于有双脚支撑转换与全身手—腿协调的 humanoid。

## 2. 接口与评测

| 输入 | 输出 | 对全身扩展所需补充 |
|---|---|---|
| 场景/语义资产、任务目标、agent 传感器、导航/操作 action | 轨迹、任务进度、导航/交互成功、场景状态 | humanoid URDF/USD、足底接触、下身控制与跌倒终止 |
| 生成的 benchmark episode/config | benchmark score、rollout/log | 双足 locomotion 与 manipulation 的统一 action adapter |

原生可报告的量包括目标到达、social navigation 和移动操作成功；若换成 humanoid，应增加跌倒、足滑、接触/碰撞、关节/力矩限制和操作成功，且证明任务在“行走+操作”而非“固定底座/轮式底盘”上完成。

## 3. 部署与边界

官方文档提供 Linux 源码安装、PyPI 包和 benchmark baseline 路径；大型场景与仿真/渲染依赖应按当前 release 的安装矩阵核验。它适合用来增加场景/任务分布，不能作为 HumanoidBench 的替代或直接排名依据；更严谨的流程是把 GRBench 场景迁入目标 humanoid control stack，再公开对应的全身任务协议。
