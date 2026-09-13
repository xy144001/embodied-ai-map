---
title: 仿真平台部署审计：准入条件、硬件与复现计划
category: evaluation
kind: guidance
organization: Embodied AI Map
releaseDate: 2026-09-02
summary: 为“把算法部署到虚拟 humanoid 并运行闭环实验”设定平台准入标准，列出官方可访问入口、资源等级、安装路径和复现实验记录要求；研究方法仓库不作为通用仿真平台混入。
tags: [whole-body-humanoid, simulation-platform, deployment, hardware, reproducibility]
draft: false
references:
  - title: Isaac Lab local installation
    url: https://isaac-sim.github.io/IsaacLab/main/source/setup/installation/index.html
  - title: Isaac Sim system requirements
    url: https://docs.isaacsim.omniverse.nvidia.com/latest/installation/requirements.html
  - title: Genesis World installation
    url: https://genesis-world.readthedocs.io/en/latest/user_guide/overview/installation.html
  - title: ManiSkill installation
    url: https://maniskill.readthedocs.io/en/latest/user_guide/getting_started/installation.html
  - title: InternUtopia installation
    url: https://internrobotics.github.io/user_guide/internutopia/get_started/installation.html
---

## 1. 什么才算本目录的“仿真平台”

只有同时满足以下条件，才列为平台：

1. 有官方可访问的代码/文档和安装入口；
2. 能载入或定义 robot asset、场景与传感器；
3. 能把外部算法接到 observation → action 的闭环，并推进物理时间得到 rollout；
4. 能记录 state/contact/reward/termination 或等价实验结果。

因此，HumanoidBench、Mimicking-Bench、LeVERB-Bench、SIMPLE 放在 **Benchmark**：它们固定了任务与计分协议。ASAP、HOVER、Humanoid-Gym、UniHCP 保留为平台区的**可运行控制参考实现**：能作为虚拟人形上的训练/执行起点，但不是通用仿真引擎，也不是统一 benchmark。平台是否“支持 humanoid”还取决于用户提供的 URDF/USD/MJCF、手部与足部控制接口；不能由软件名称推断。

## 2. 官方资源需求：如何读表

`官方最小` 只写官方文档明确给出的值；没有明确 CPU/RAM/Storage 数字时写“未规定”，不伪造配置。`建议实验机`是为了全身视觉闭环的保守工程规划，不是发布方承诺。渲染、并行环境数、相机数量、mesh 规模和训练算法会显著改变资源占用。

| 平台 | 官方最小/明确要求 | 适合的 humanoid 实验 | 入口 |
|---|---|---|---|
| Isaac Lab / Isaac Sim | Ubuntu 22.04 或 Windows 11；≥32 GB RAM、≥16 GB VRAM；Isaac Sim 文档列 50 GB SSD 最小、RTX 4080 最小级别 | 大规模并行、RGB-D/分割、USD 场景、G1/H1/Digit 相关任务 | [部署页](../isaac-lab/) |
| MuJoCo + MJX | `pip install mujoco`/`mujoco-mjx`；官方未给统一 RAM/Storage/CPU 数字 | 状态控制、接触、JAX 批量 motion imitation/低层技能 | [部署页](../mujoco-mjx/) |
| Genesis World | Python 3.10–3.13；Linux/macOS/Windows；CPU、CUDA 和非 CUDA GPU 均支持；官方未给统一资源数字 | 多物理/传感器原型、可自定义 humanoid | [部署页](../genesis/) |
| SAPIEN + ManiSkill | state-only 不额外要求 GPU；GPU 渲染需 Vulkan；官方未给统一 RAM/Storage 数字 | 高吞吐视觉/状态操作；全身任务需自定义 | [部署页](../sapien-maniskill/) |
| OmniGibson + BEHAVIOR | 依赖 Omniverse/Isaac Sim；按对应 release 的 NVIDIA RTX 要求核验 | 家庭场景与长时程交互；全身下身控制需自建 | [部署页](../omnigibson-behavior/) |
| InternUtopia | Ubuntu 20.04/22.04、≥32 GB RAM、RTX 2070+（需 RT cores）、driver 535.216.01+；绑定 Isaac Sim 4.5.0 | 大场景、social navigation、mobile manipulation；humanoid 需核验 asset/action | [部署页](../internutopia/) |

## 3. 可行部署方案

### A. 视觉全身移动操作（首选 Isaac Lab）

- **设备规划**：Linux RTX 工作站，至少官方 32 GB RAM / 16 GB VRAM / 50 GB SSD；实际含多相机、Replicator 或大量环境时规划 64 GB RAM、24 GB+ VRAM、500 GB SSD，后者是工程建议。
- **官方路径**：先按 Isaac Sim 版本矩阵安装 NVIDIA driver 与 Isaac Sim，再按 Isaac Lab 的 local/pip 安装页建立 Python 环境、安装匹配的 CUDA PyTorch 和 Isaac Lab；运行官方环境 smoke test 后才导入 humanoid asset。
- **实验接入**：封装 policy 的 `reset(obs)` / `act(obs)`；冻结 USD/URDF、sensor config、action adapter、control Hz、seed；导出 episode CSV、视频、contact/termination 日志。

### B. 状态控制与低层技能（MuJoCo/MJX）

- **设备规划**：CPU 能运行单环境调试；MJX 批量训练使用与 JAX wheel 匹配的 GPU。官方未公布统一最低硬件，应以模型大小、batch 和 JAX backend 做 profiling。
- **官方路径**：安装 `mujoco`；需要 JAX 批量执行时安装 `mujoco-mjx`，再选匹配 CPU/CUDA 的 JAX。使用 versioned MJCF 载入 robot，先验证 actuator 与 qpos/qvel mapping。
- **实验接入**：把 policy action 写入 `ctrl` 或明确的上层 adapter；记录 actuator type、timestep/substep、solver、friction、控制频率。不要把 MJX 中的 tensor shape 当作自动正确的机器人 action 含义。

### C. 跨平台原型/自定义物理（Genesis World、ManiSkill）

- **Genesis**：官方安装是先安装符合系统/CUDA 的 PyTorch，再 `pip install genesis-world`；以 `gs.init()` 初始化 backend。先用 CPU 单场景确认 asset/单位/接触，再迁到 CUDA。
- **ManiSkill**：官方基本安装为 `pip install --upgrade mani_skill torch`；state simulation 可不依赖 GPU，GPU rendering 要 Vulkan。先跑官方 quickstart，再自建 humanoid scene/action adapter；默认 manipulation task 不构成双足测试。

### D. 大规模场景（InternUtopia / OmniGibson）

- 先锁定其对应 Isaac Sim release，而不是使用“最新 Isaac Sim”；InternUtopia 2.2 文档明确绑定 Isaac Sim 4.5.0。
- 优先 Linux source/PyPI 安装做 GUI smoke test；无显示器/集群则按官方 Docker + NVIDIA Container Toolkit 路径。
- 先运行一条官方 benchmark episode，确认 RTX rendering、asset download 和 camera；再替换为 humanoid。没有足接触、跌倒终止和全身 action adapter 时，只能称为场景/高层任务实验。

## 4. 每次部署必须留档

`platform/release + GPU/driver + OS + Python + simulator backend + robot asset hash + scene asset hash + observation/action schema + control Hz + seed + train/eval split + evaluator commit`。缺任一项，跨机器或跨论文的结果都可能不可比较。
