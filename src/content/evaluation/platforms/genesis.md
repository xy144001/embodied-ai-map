---
title: Genesis World：用于全身仿真原型的统一多物理平台
category: evaluation
kind: evaluation
organization: Genesis-Embodied-AI
releaseDate: 2024-12-01
summary: Apache-2.0 的 Python 机器人与具身学习仿真平台，组合多物理求解、渲染与跨平台编译；可构建 humanoid 训练/评测环境，但没有预先冻结的全身移动操作榜单。
tags: [whole-body-humanoid, genesis, simulation, physics, synthetic-data]
draft: false
references:
  - title: Genesis World repository
    url: https://github.com/Genesis-Embodied-AI/genesis-world
  - title: Genesis World documentation
    url: https://genesis-world.readthedocs.io/
---

## 1. 定位

[Genesis World](https://github.com/Genesis-Embodied-AI/genesis-world) 是开源（Apache-2.0）通用机器人/具身 AI 仿真平台。其文档将系统描述为统一多物理引擎、Nyx 渲染器和跨平台编译器之上的 Python 接口。[官方文档](https://genesis-world.readthedocs.io/) 适合作为构建 humanoid 物理、传感器、随机化和批量训练原型的底座；它不是像 HumanoidBench 那样已定义完成的全身基准。

## 2. 输入—输出

| 项 | 输入 | 输出 |
|---|---|---|
| 场景 | Python scene 配置、机器人/物体资产、刚体/可变形/流体等求解器选择、碰撞/材质参数 | 编译后的 scene、实体句柄与物理状态 |
| 人形 | URDF/MJCF 等资产（按版本支持为准）、关节/执行器控制和初始状态 | 关节状态、root state、link pose、接触与传感器信息 |
| 观测 | state、相机图像/深度/分割及自定义传感器，定义采样频率 | numpy/torch 风格批量张量或渲染帧（具体 API 以 release 为准） |
| 动作 | joint target/PD/力矩或任务空间控制，由用户定义 policy adapter | 下一仿真状态、接触、task reward/终止（若任务层实现） |

## 3. 如何把它变成可评测平台

Genesis 不替你决定“拿什么比”。建立全身移动操作任务时应将以下内容随仓库发布：

- robot asset 与 conversion script、执行器/PD 参数、control Hz；
- 场景和物体资产、物理 solver 配置、render/sensor 配置；
- train/test 的对象、布局、质量/摩擦、地形与扰动种子；
- `success predicate`、失败/安全终止、evaluator，以及逐任务 success/time/fall/collision 指标。

建议先把一个 task 在单环境下与已知动作回放对齐，再扩大 batch；并将 GPU 型号、driver、Genesis commit 写入结果表头。快速并行只降低实验成本，不会自动提高评测可信度。

## 4. 部署与依赖

官方 repository 含 `pyproject.toml`、examples、tests 和文档；优先按目标 release 的官方 installation instructions 安装，不要把 README 的 main 分支命令当作历史版本的保证。Python ≥3.10 是其文档构建示例的环境下限。复杂渲染和 GPU 加速依赖显卡驱动/图形后端；集群 headless 运行先用一个最小 scene 验证 renderer 和 physics。

## 5. 适用边界

适合：需要同时探索接触动力学、传感器合成、资产导入和训练吞吐的早期系统研究。限制：全身 humanoid 任务、真实机器人 asset fidelity、指标与基准切分由使用者决定；结论应写为“在公开的 Genesis task package 上”，不要泛化为“跨平台 humanoid 基准性能”。
