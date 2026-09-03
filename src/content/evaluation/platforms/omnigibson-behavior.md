---
title: OmniGibson 与 BEHAVIOR：家庭长时程交互仿真（迁移背景）
category: evaluation
kind: evaluation
organization: Stanford Vision and Learning Lab
releaseDate: 2024-02-26
summary: 面向具身家庭活动、真实感场景资产和长时程交互的仿真平台与任务生态；对家居场景和操作任务有价值，但原生任务重点不是全身双足 humanoid 移动操作。
tags: [simulation, household, omnigibson, behavior, transfer-only]
draft: false
references:
  - title: BEHAVIOR project
    url: https://behavior.stanford.edu/
  - title: OmniGibson
    url: https://behavior.stanford.edu/omnigibson/
  - title: OmniGibson repository
    url: https://github.com/StanfordVL/OmniGibson
  - title: BEHAVIOR-1K paper
    url: https://arxiv.org/abs/2402.16784
---

## 1. 定位

[OmniGibson](https://github.com/StanfordVL/OmniGibson) 与 [BEHAVIOR](https://behavior.stanford.edu/) 提供家庭场景、物体交互、活动定义与具身仿真任务生态。它们对于“人形未来要在什么样的家庭环境中工作”很有参考价值：可以给出多房间、物体状态变化和长时程活动的场景压力；但它们不是以双腿支撑、行走和全身协调为默认评测目标。[BEHAVIOR-1K](https://arxiv.org/abs/2402.16784)

## 2. 接口与使用方式

| 输入 | 输出 | 对 humanoid 的含义 |
|---|---|---|
| 场景/对象资产、任务初始状态、机器人模型、RGB-D/分割/本体观测 | 物理状态、传感器帧、任务进度/成功、交互事件 | 能作为高层任务与场景层；下身控制需额外加入 |
| 行动（通常是操控/导航接口） | object state transitions 与 episode result | 需明确是否真的使用双足人形，而非移动底盘/机械臂代理 |

## 3. 部署与边界

遵循[OmniGibson 官方仓库](https://github.com/StanfordVL/OmniGibson)的安装说明和资产获取流程；它通常涉及 Python、NVIDIA GPU/渲染、物理引擎及大型场景资产。自定义 humanoid 后，必须重新验证关节/碰撞、足底接触、开门/搬运时的稳定性，且分别报告 lower-body stability 与 object-level task success。不能用 BEHAVIOR 的家庭任务完成率替代全身移动操作基准成绩。
