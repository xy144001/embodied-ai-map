---
title: MuJoCo 与 MJX：全身控制基准的物理底座
category: evaluation
kind: evaluation
organization: Google DeepMind
releaseDate: 2025-01-01
summary: MuJoCo 提供接触刚体动力学与 Python API，MJX 以 JAX/XLA 形式提供向量化并行计算；两者可承载 humanoid loco-manipulation，但任务、资产和评测协议需要上层项目定义。
tags: [whole-body-humanoid, mujoco, mjx, jax, physics-simulation]
draft: false
references:
  - title: MuJoCo Python documentation
    url: https://mujoco.readthedocs.io/en/stable/python.html
  - title: MuJoCo XLA (MJX) documentation
    url: https://mujoco.readthedocs.io/en/stable/mjx.html
  - title: MuJoCo repository
    url: https://github.com/google-deepmind/mujoco
---

## 1. 定位

[MuJoCo](https://github.com/google-deepmind/mujoco) 是可编程物理引擎；[MJX](https://mujoco.readthedocs.io/en/stable/mjx.html) 是其 JAX API/后端，用于把大量环境批量放到加速器上运行。HumanoidBench 等全身基准以它为底座，但“MuJoCo 能跑 humanoid”并不意味着“MuJoCo 自带全身移动操作评测”。

## 2. 输入—输出

| 层 | 输入 | 输出 |
|---|---|---|
| 模型 | MJCF/XML：body、joint、actuator、sensor、碰撞几何、材质、初始 keyframe | `MjModel`（编译后的质量、几何、接触和 actuator 定义） |
| 状态 | qpos、qvel、act、控制 `ctrl`、外力、时间 | `MjData`：下一状态、传感器读数、接触对/力、动力学中间量 |
| 任务层（自建） | reset 分布、观测选择、reward、termination、success predicate、随机种子 | Gym 风格 `(obs, reward, terminated, truncated, info)` 或训练框架张量 |
| MJX | `mjx.put_model` 后的模型和批量 state/action | JAX arrays，可 `jit`/`vmap`/编译；再由上层计算 reward/指标 |

人形控制常把 qpos/qvel、IMU、足/手接触、目标相对位姿作为输入，并输出全身 actuator control。必须在文档写清 actuator 是 torque、position servo 还是 PD target；同样的“30/50 维 action”在不同 XML 中可能完全不同。

## 3. 评测如何搭建

1. 使用版本化 MJCF/mesh/texture，固定 timestep、substep、solver、接触摩擦和 actuator gain。
2. 为每个任务写显式 `success(state)`，不要只拿 reward 大小做成功率。
3. 记录 state/action/contacts/终止原因；按任务计算 success、时间、跌倒率、碰撞/接触违规、能耗或 action jerk。
4. 对随机化（质量、摩擦、延迟、外力、目标/物体初始位姿）定义 train/test seed 与 OOD split；MJX 的批量吞吐不能替代独立 evaluation episodes。
5. 若从 MJX 训练而在经典 MuJoCo 回放或部署，验证两条执行路径的控制解释和数值差异。

## 4. 部署

- 官方 Python binding 的基础安装是 `pip install mujoco`；文档称 wheel 随包携带 MuJoCo library。
- MJX 安装为 `pip install mujoco-mjx`，可选 Warp extra；它依赖主 `mujoco` 做模型编译/可视化。[MJX 文档](https://mujoco.readthedocs.io/en/stable/mjx.html)
- CPU 足以调试 XML/task；大规模 PPO/motion imitation 通常需匹配 JAX 与 CUDA 的 GPU 环境。将 Python、mujoco、mujoco-mjx、jax/jaxlib、CUDA、GPU 型号记录进实验元数据。

## 5. 边界

MuJoCo/MJX 的优势是轻量、可复现的控制研究与高吞吐；局限是视觉逼真度、真实传感器建模、复杂场景资产与 sim-to-real 仍由上层工程负责。选它做全身论文实验时，最好同时采用 HumanoidBench 这类固定协议，或公开完整 task package。
