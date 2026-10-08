---
title: 方法部署记录：GR00T N1.7、DiT4DiT、Cosmos Policy 与 OpenHLM
category: evaluation
kind: evaluation
organization: Embodied AI Map
releaseDate: 2026-09-11
summary: 四个方法在 LIBERO、RoboCasa、RoboCasa-GR1、HumanoidBench 等目标上的部署、闭环 smoke 与回归结果，以及每个未跑通组合的具体缺项：缺 checkpoint、缺资产、本体不匹配或需要真机。
tags: [evaluation, deployment, gr00t, dit4dit, cosmos-policy, openhlm, server-client]
draft: false
references:
  - title: GR00T 官方仓库
    url: https://github.com/NVIDIA/Isaac-GR00T
  - title: LIBERO 官方仓库
    url: https://github.com/Lifelong-Robot-Learning/LIBERO
  - title: RoboCasa 官方仓库
    url: https://github.com/robocasa/robocasa
  - title: RoboCasa-GR1 tabletop 扩展
    url: https://github.com/robocasa/robocasa-gr1-tabletop-tasks
  - title: Cosmos Policy 项目页
    url: https://research.nvidia.com/labs/dir/cosmos-policy/
---

## 1. 统一口径与评测链路

**状态定义**（跨方法共用，与[结果矩阵](../overview/)的四档口径对应）：

- **环境 smoke**：只验证环境能注册、`reset`、`step`，不代表策略会完成任务。
- **闭环 smoke**：真实策略 + 真实模拟器 + 官方成功判定，完整运行一个 episode。
- **1 episode/task 回归**：每任务固定 seed 跑一集，检查部署覆盖和明显退化；样本数不足以代表论文结果。
- **正式统计**：每任务多 episode / seed，报告均值与波动，并固定最大步数、action chunk、渲染方式和 checkpoint。

**评测链路**（所有方法共用同一结构）：

```text
Benchmark 环境 reset/step
   ↓ 相机图像、机器人状态、语言指令
本机策略客户端
   ↓ socket
GPU 模型服务端（独立 conda 环境）
   ↓ 动作 chunk
Benchmark 环境执行并检查官方 success condition
   ↓
日志、成功标记、可选 MP4
```

模型服务端与仿真客户端分环境、经本机 socket 通信，隔离两套互相冲突的依赖（如 GR00T 与新版本 MuJoCo 栈）。评测机为 8×RTX 4090 共享工作站；无 EGL 权限时统一使用 OSMesa 软件渲染，渲染成为主要速度瓶颈。

## 2. GR00T N1.7

| 项目 | 内容 |
|---|---|
| checkpoint | GR00T-N1.7-LIBERO（`libero_10`），embodiment tag `LIBERO_PANDA` |
| 已完成 | `libero_10` 全部 10 个任务 × 1 episode/task 回归 |
| 参数 | seed 0；最大 720 步；action chunk 8；单环境；OSMesa |
| 结果 | **7/10 = 70%**；全部 episode 平均长度 400.1 步，成功 episode 平均 263.0 步 |

逐任务结果（3 个失败均为 `libero_10` 中的双目标/多目标长程任务）：

| 任务（简写） | 成功 | 长度 |
|---|:---:|---:|
| LIVING_ROOM_SCENE2：alphabet soup + tomato sauce → basket | ✅ | 276 |
| LIVING_ROOM_SCENE2：cream cheese box + butter → basket | ✅ | 233 |
| KITCHEN_SCENE3：开炉灶并放 moka pot | ✅ | 264 |
| KITCHEN_SCENE4：黑碗入下层抽屉并关闭 | ✅ | 254 |
| LIVING_ROOM_SCENE5：两个杯子分放左右盘 | ❌ | 720 |
| STUDY_SCENE1：书放进 caddy 后格 | ✅ | 159 |
| LIVING_ROOM_SCENE6：杯子放盘 + 布丁放盘右侧 | ❌ | 720 |
| LIVING_ROOM_SCENE1：alphabet soup + cream cheese box → basket | ❌ | 720 |
| KITCHEN_SCENE8：两个 moka pot 放炉灶 | ✅ | 382 |
| KITCHEN_SCENE6：杯子入微波炉并关门 | ✅ | 273 |

70% 是**固定 seed 的部署回归值**，不是 GR00T 论文成功率的复现值；当前 checkpoint 只对应 `libero_10`，不能据此补跑其余三个 LIBERO suite。

RoboCasa-GR1：环境部署完成且可独立运行，但没有与 GR1 本体匹配的 `ROBOCASA_GR1_TABLETOP` checkpoint，因此没有可归属 GR00T 的 rollout 或成功率；现有 Panda checkpoint 的观测/动作定义与 GR1 双臂 29 维接口不一致，不能直接套用。

## 3. DiT4DiT

| 项目 | 内容 |
|---|---|
| Cosmos 基座 | Cosmos-Predict2.5-2B（本地路径引用，避免运行时重复下载） |
| LIBERO checkpoint | `dit4dit_libero` |
| RoboCasa-GR1 checkpoint | `dit4dit_robocasa_gr1`（约 21.3 GiB，GR1 双臂 + Fourier 手 + 腰部，29 维动作） |

已完成：

- **LIBERO 闭环 smoke**：`put_both_the_alphabet_soup_and_the_tomato_sauce_in_the_basket` 1/1 成功（官方成功条件判定）。
- **RoboCasa-GR1 部署验证**：源码与约 8.7 GiB 资产安装完成，共注册 197 个 Gym 环境 ID；`PnPCanToDrawerClose` 完成 reset smoke。
- **RoboCasa-GR1 闭环 smoke**：`PnPMilkToMicrowaveClose`，seed 7，最大 720 步，action chunk 12，1/1 成功。该任务官方成功条件同时要求牛奶盒在微波炉内且 `door_state ≤ 0.005`；视频与文件名中的 `success1` 标记一致。
- 接口修复：视频 wrapper 在清理阶段对不存在文件重命名的问题已加 `.exists()` 检查；模型侧接口改为直接读取数据集统计信息，避免客户端为读取统计量而导入整套 GPU 依赖。

RoboCasa365 边界：当前 DiT4DiT RoboCasa checkpoint 面向 GR1 的 29 维动作，而 RoboCasa365 本地版本默认 PandaOmron，本体、控制器、观测字段和任务初始化均不匹配。两条合规路径：①取得 PandaOmron 的 checkpoint 与归一化统计；②编写并验证 GR1 → PandaOmron 的观测/动作适配器，并把结果标为**自定义迁移实验**，而不是原 checkpoint 的标准 Benchmark 结果。

## 4. Cosmos Policy

| 项目 | 内容 |
|---|---|
| 已接入入口 | 官方提供 LIBERO、RoboCasa、ALOHA 三个评测入口 |
| LIBERO | 4 个 suite × 10 task × 1 trial = **40/40 成功**；每 episode 保存普通 rollout 与 future-image 两种视频 |
| RoboCasa | `TurnOffMicrowave`（PandaMobile，seed 195）：单集验证 1/1 + 3 集预评测 3/3，episode 长度 264 / 264 / 355 / 371 |
| 推理 smoke | checkpoint 加载 `missing_keys=[]`；输出 `(32, 7)`（32 步 × 7 维动作）；峰值显存 7.978 GiB |

已证明的链路：观测输入 → Cosmos 策略推理 → action chunk → 仿真执行 → 官方成功判定 → 日志/视频保存。未达正式规模：RoboCasa 官方目标为 24 task × 50 trials × 3 seeds = 3600 集，本地只覆盖 1 个任务；LIBERO 官方规模为 40 task × 50 trials × 3 seeds = 6000 集，本地每任务仅 1 trial 单 seed。ALOHA 面向真实双臂机器人，需要硬件；HumanoidBench 官方没有可直接运行的入口，需要机器人、观测、动作与 checkpoint 适配。

## 5. OpenHLM

| 项目 | 内容 |
|---|---|
| 面向本体 | Unitree G1 全身 humanoid（动作同时覆盖上肢与身体控制） |
| 已完成 | 官方 checkpoint 加载 + 一次离线前向推理 smoke：输出 `(50, 34)`（50 步 × 34 维），数值全部 finite，范围约 [−0.5090, 1.0124]；峰值显存 7.121 GiB |
| RoboCasa G1 审计 | 公开代码缺 7 类上游依赖，`complete=false`：`robocasa.models` 基础包、`GroundArena` / `FactoryArena` / `LabArena`、`MJCFObject`、G1 robot 与 gripper 模型、G1 wrapper 默认控制器配置、RoboCasa macro setup 脚本 |
| 未完成 | 真实 G1 任务（需硬件与低层控制/安全部署）；标准 RoboCasa / LIBERO / HumanoidBench 入口（无官方适配） |

对 OpenHLM 的可行路径只有两条：取得官方完整 RoboCasa G1 依赖与评测脚本以复现官方条件；或者自行把 G1 模型、全身控制器和任务资产接入现有 RoboCasa——后者属于新适配工作，应标为自定义实验。

## 6. 结果总表与速度

| 方法 | Benchmark | checkpoint 匹配 | 已完成范围 | 当前结果 | 统计等级 |
|---|---|:---:|---|---|---|
| GR00T | LIBERO-10 | 是 | 10 task × 1 episode | 7/10 | 1 episode/task 回归 |
| GR00T | RoboCasa-GR1 | 否 | 环境已部署 | 无 | checkpoint 阻塞 |
| DiT4DiT | LIBERO | 是 | 1 task × 1 episode | 1/1 | 闭环 smoke |
| DiT4DiT | RoboCasa-GR1 | 是 | 环境验证 + 1 task × 1 episode | 1/1 | 闭环 smoke |
| DiT4DiT | RoboCasa365 | 否 | 未开始 | 无 | 本体/动作不匹配 |
| Cosmos Policy | LIBERO | 是 | 40 episodes | 40/40 | 小样本回归 |
| Cosmos Policy | RoboCasa | 是 | 1 task × 4 episodes | 4/4 | 小样本回归 |
| OpenHLM | —（官方自建 G1 benchmark） | — | 1 次离线推理 | 输出 (50, 34) | 仅推理 smoke |

速度量级：GR00T + LIBERO 单 episode 约 2 分钟；DiT4DiT + RoboCasa-GR1 单 episode 约 4 分钟；DiT4DiT checkpoint 冷启动每服务进程 5–6 分钟（服务复用后不再重复支付）。DiT4DiT 24 tasks × 1 episode 估计 1.5–2.5 小时；LIBERO 4 suite 共 40 tasks × 1 episode 估计 1.5–2 小时。实测中 GPU 利用率约 19% 的时段，等待主要发生在 CPU 模拟与 OSMesa 渲染，不在 MP4 编码。

## 7. 结论

四个方法都只是“部分 Benchmark 上的成功案例”，而这个“部分”由方法自身的本体决定：**每多一个本体，就多写一份接口**。可复用的部分是成功判定（官方 evaluator 与本体无关），需要按 Benchmark 重写的是观测与动作映射。下一步的接口契约与优先级见[复现实测总览](../overview/)；各 Benchmark 的原生本体与动作语义见[本体与控制量图谱](../../guides/robot-action-audit/)。
