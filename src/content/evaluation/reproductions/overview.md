---
title: 跨方法 Benchmark 复现实测总览：结果矩阵、口径与缺口
category: evaluation
kind: roadmap
organization: Embodied AI Map
releaseDate: 2026-09-11
summary: 6 个已公开方法（UnifoLM-VLA、GR00T N1.7、DiT4DiT、Cosmos Policy、OpenHLM、Psi0）在 7 个目标 Benchmark 上的实测记录：42 个组合中 7 格有数字、1 格达到正式规模；给出四档结果口径、空白的真实原因与跨本体适配结论。
tags: [whole-body-humanoid, reproduction, benchmark-matrix, embodiment, action-interface]
draft: false
references:
  - title: LIBERO 官方仓库
    url: https://github.com/Lifelong-Robot-Learning/LIBERO
  - title: SIMPLE 项目页
    url: https://psi-lab.ai/SIMPLE/
  - title: RoboCasa 官方仓库
    url: https://github.com/robocasa/robocasa
  - title: HumanoidBench 项目页
    url: https://humanoid-bench.github.io/
---

## 1. 这份记录回答什么

论文里的成功率是作者在其实验条件下的报告值；本页记录的是**把方法真的部署起来之后**能跑什么、分数多少、口径是什么、哪些组合根本跑不了。所有数字来自评测机实测，均标注完成范围与结果口径；与论文数字的对照写在各自明细页。

## 2. 结果口径：四档工作量，先分类再读数字

| 口径 | 定义 | 本轮的例子 |
|---|---|---|
| 正式规模 | 覆盖官方任务与 trial / seed 规模，千集量级 | UnifoLM-VLA × LIBERO：4 suite × 10 task × 50 trials = 2000 集 |
| 小样本回归 | 多个任务，但每任务仅 1–5 集 | Psi0 × SIMPLE 240 集；GR00T × LIBERO-10；Cosmos Policy 预评测 |
| 单任务闭环 smoke | 1–4 集，只验证“观测 → 策略 → 仿真执行 → 官方判定”链路能通 | DiT4DiT × LIBERO、DiT4DiT × RoboCasa-GR1 |
| 仅推理 smoke | 无环境闭环，只验证权重加载与输出数值 | OpenHLM 一次离线前向推理 |

官方协议规模作为对照：LIBERO 为 40 task × 50 trials × 3 seeds = 6000 集；RoboCasa 为 24 task × 50 trials × 3 seeds = 3600 集。本轮只有 UnifoLM × LIBERO 达到正式规模，其余都低于正式协议，不能当作论文成功率的复现值。

## 3. 方法 × Benchmark 结果矩阵

| 方法 | 本体 | LIBERO | RoboCasa | RoboCasa-GR1 | RoboCasa365 | HumanoidBench | ALOHA（真机） | SIMPLE（G1） | 空白原因 |
|---|---|---|---|---|---|---|---|---|---|
| [UnifoLM-VLA](../unifolm-vla-libero/) | Panda 单臂 | **98.10%** | − | − | − | − | − | − | 官方只发布 LIBERO 权重 |
| [GR00T N1.7](../policy-deployment-records/) | Panda 单臂 | 70% | − | − | − | − | − | − | 缺 RoboCasa-GR1 checkpoint |
| [DiT4DiT](../policy-deployment-records/) | Panda / GR-1 | 1/1 | − | 1/1 | − | − | − | − | 无匹配 checkpoint 的本体无法接入 |
| [Cosmos Policy](../policy-deployment-records/) | PandaMobile 移动单臂 | 40/40 | 4/4 | − | − | − | − | − | 官方只有 LIBERO、RoboCasa、ALOHA 三个入口；ALOHA 需真机 |
| [OpenHLM](../policy-deployment-records/) | G1 全身 | − | − | − | − | − | − | − | 官方无标准入口；G1 RoboCasa 公开代码缺资产 |
| [Psi0](../simple-psi0/)（基线） | G1 全身 | − | − | − | − | − | − | **46.2%** | 官方只发布 SIMPLE 配套权重 |

42 个组合中 7 格有数字（16.7%），其中仅 1 格为正式规模。− 表示未跑，原因写在末列。

## 4. 空白格不是“没测”，是“没有入口”

每个非空格子背后都是一次针对该 Benchmark 的单独适配；空白格由三类缺项造成：

1. **缺入口**：Cosmos Policy 官方只提供 LIBERO、RoboCasa、ALOHA 三个评测入口，HumanoidBench 没有可运行的官方入口；OpenHLM 的评测跑在自建的 G1 benchmark 上，不是标准套件。
2. **缺 checkpoint**：GR00T N1.7 本地只有 `LIBERO_PANDA` 权重，没有与 GR1 本体匹配的 `ROBOCASA_GR1_TABLETOP` checkpoint；RoboCasa 环境部署完成也无法出分。
3. **缺资产**：OpenHLM 公开的 RoboCasa G1 代码经完整审计为 `complete=false`——缺基础包、Arena、G1 模型与控制器配置等上游依赖。

跨本体没有免费通道：**GR-1 的 29 维权重放进 PandaOmron 的 RoboCasa365 直接无效；Panda 的 7 维末端动作喂不了 G1 全身策略。**

## 5. 数据侧发现：评测数据与训练条件不一致会整任务失效

Psi0 × SIMPLE 的复现中，XMovePick（0/15）经逐层排查后定位到两处数据侧缺陷：评测数据的**材质随机化配置**与训练不一致（渲染成黑色镜面桌面）、**指令模板**过期（`bend to pick up` vs 训练实际使用的 `move forward to pick up`）。修复后模型恢复行走输出，但该 checkpoint 仍无法复现 README 公开值——残余差异在“抓取 + 抬升”执行环节。

结论：做跨方法复现时，**先对齐评测数据与 checkpoint 的训练条件，再解释成功率**；否则会把数据配置错误读成模型能力缺陷。完整缺陷清单见 [Psi0 × SIMPLE 复现记录](../simple-psi0/)。

## 6. 跨本体适配结论

部署过这些 Benchmark 之后，问题不在任务难度、也不在成功判定，而在**控制量**这一层：

- **判定与本体解耦**：LIBERO 的 BDDL 符号谓词、RoboCasa-GR1 的“牛奶在炉内 + `door_state ≤ 0.005`”、SIMPLE 的任务自带 `check_success` 都只描述“物体与场景达到什么状态”，与驱动它的是 Panda、GR-1 还是 G1 无关——**官方 evaluator 可以直接沿用**。
- **动作与观测需要重写**：把一个 Benchmark 接入目标本体，要逐一打通六个接口：①资产 ②观测 ③动作映射 ④重置与划分 ⑤成功谓词 ⑥日志。需要重新实现的是 ①–④ 与 ⑥；⑤ 直接复用官方判定。

因此可行路径不是“让所有 Benchmark 统一”，而是：**先定死自己本体的控制量契约与策略输入，再逐个 Benchmark 写适配。**

## 7. 已完成范围与下一步

| # | 事项 | 状态 |
|---|---|---|
| 1 | UnifoLM-VLA × LIBERO 正式规模复现（2000 集，98.10%） | ✅ 完成 |
| 2 | Psi0 × SIMPLE 小样本回归（240 集，46.2%）+ 8 项缺陷修复 | ✅ 完成 |
| 3 | GR00T / DiT4DiT / Cosmos / OpenHLM 部署与 smoke | ✅ 记录在案，未达正式规模 |
| 4 | 把 DiT4DiT / Cosmos 从 smoke 扩到官方规模（LIBERO 7D、RoboCasa 12D 本体已对齐） | 待执行 |
| 5 | RoboCasa-GR1、HumanoidBench、SIMPLE 的全身本体适配 | 待本体与控制量确定后接入 |
| 6 | 工程项：EGL 硬件渲染（OSMesa 是当前吞吐瓶颈）、复用模型服务端避免冷启动 | 待执行 |

明细页：[UnifoLM-VLA × LIBERO](../unifolm-vla-libero/)、[Psi0 × SIMPLE](../simple-psi0/)、[四方法部署记录](../policy-deployment-records/)；结构性依据：[Benchmark 原生机器人本体与控制量图谱](../../guides/robot-action-audit/)。
