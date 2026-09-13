---
title: AlphaBrain Platform：统一 VLA 评测套件与 Benchmark 适配
category: evaluation
kind: benchmark
organization: AlphaBrain Group
releaseDate: 2026-09-02
summary: AlphaBrain Platform 将多种具身策略接入同一套 policy-server 与仿真客户端流程，覆盖 LIBERO、LIBERO-plus、CALVIN、RoboTwin、RoboCasa、RoboCasa365、SimplerEnv 与 BEHAVIOR-1K；它是评测编排/适配层，不是替代这些 benchmark 官方任务协议的新 benchmark。
tags: [vla, benchmark-suite, libero, robocasa, robotwin, calvin, long-horizon, continual-learning]
draft: false
references:
  - title: AlphaBrain Platform 官网
    url: https://www.alphabrain-platform.com/
  - title: AlphaBrain GitHub 仓库
    url: https://github.com/AlphaBrainGroup/AlphaBrain
  - title: AlphaBrain 文档
    url: https://alphabraingroup.github.io/AlphaBrain/
---

## 1. 定位：Benchmark 编排层，而非第九个任务集

[AlphaBrain Platform 官网](https://www.alphabrain-platform.com/)把自己定位为覆盖数据、训练、架构、测试与部署的一站式具身模型平台，并宣称“8 大主流 Benchmark 全覆盖”。开源仓库的 benchmark 表和目录提供了更具体的可复查边界：平台复用各 benchmark 的任务、资产、reset、success predicate 与许可证；AlphaBrain 负责 policy 训练/服务、配置管理和结果聚合。因此在调研地图中应把它记为 **benchmark suite / evaluation harness**，不能把“平台支持”写成在所有套件上已有可比 SOTA 结果。

## 2. 覆盖矩阵（按仓库当前公开目录）

| 套件 | 平台中承担的角色 | 原生主要考察 | 复现时必须冻结 |
|---|---|---|---|
| LIBERO Spatial / Object / Goal / Long | 核心回归与持续学习 stream | 语言条件下的桌面操作、空间/物体/目标与长程组合 | suite、task list、机器人/相机、episode seeds、每任务 success |
| LIBERO-plus | 鲁棒性分支 | 约 7 个扰动维度的零样本泛化（相机、机器人、光照、语言等） | 扰动分支与强度、是否 zero-shot、聚合规则 |
| CALVIN | 长时程语言—动作链评测 | 多阶段子任务连续完成长度 | chain split、初始状态、语言指令、平均完成链长 |
| RoboTwin | 双臂操作与域随机化 | 多任务双臂抓取/装配及视觉泛化 | 版本、任务/场景 split、随机化、动作 chunk |
| RoboCasa / RoboCasa365 | 厨房与日常操作 | 场景多样性、atomic/composite 任务及长时程家务 | task set（atomic/composite seen/unseen）、场景生成版本、每任务 episode 数 |
| SimplerEnv | 仿真到真实相关性参考 | 已配对的视觉操作环境与策略迁移 | 环境版本、相机/控制频率、sim/real protocol，不混报两者分数 |
| BEHAVIOR-1K | 大规模家居任务适配 | 长时程、多对象、面向人类需求的行为 | 任务许可、场景/物体版本、评测子集与资源限制 |

> 官网将 LIBERO 的四个 suite 与其余套件合计描述为“8 大 Benchmark”；仓库 README 当前还列出 RoboCasa365，并注明 CALVIN、RoboTwin、SimplerEnv、BEHAVIOR-1K 等适配方向。发布结果时应以锁定的仓库 commit 和实际可运行目录为准。

## 3. 输入、输出与主指标

AlphaBrain 的评测入口通常是两个进程：AlphaBrain 环境中的 **policy server** 提供动作，目标仿真环境作为 **simulation client** 推进 episode（RoboCasa365 的公开说明明确采用 WebSocket 通信）。策略输入必须按目标套件的 observation schema 提供，输出则按目标机器人 action space 与 action-chunk 约定解码；不能因共享 server API 就认为不同套件的动作语义相同。

主结果建议逐任务报告 `success rate`（或套件官方等价指标），同时给出均值、95% 置信区间/种子范围和失败类别。对于 AlphaBrain 的持续学习实验，仓库提供从 T×T 评测矩阵计算 **ASR（平均成功率）、BWT（后向迁移）与 F（遗忘）** 的脚本；这些是跨任务学习指标，不能替代 LIBERO 等套件的逐 episode success。

## 4. 官网展示结果的证据等级

官网展示一组 2000 episodes 的 LIBERO 汇总（`libero_object 99.0%`、`libero_goal 95.6%`、`libero_spatial 90.6%`、`libero_10 85.4%`、总平均 `92.7%`），并展示 Backprop 与 R-STDP 的训练步数/成功率对比。它们可作为 **平台自报结果**，但页面没有同时给出完整 checkpoint、commit、任务级 seeds、置信区间、机器人/相机配置和 evaluator 日志；因此调研表应标注“reported by platform”，不能直接与严格锁定协议的论文 leaderboard 横向合并。

## 5. 与全身 humanoid Benchmark 的边界

AlphaBrain 当前公开、可直接核验的仓库目录主要集中在 LIBERO 与 RoboCasa365；官网额外宣称支持 CALVIN、RoboTwin、SimplerEnv、BEHAVIOR-1K 等方向。除非目标套件的 runner、配置、资产和 evaluator 在同一 commit 中可运行，否则应标注为“平台宣称支持/待复核”，而非“已完成 benchmark 复现”。这些 VLA 操作套件默认本体也多为 Panda/移动双臂，与 HumanoidBench、Mimicking-Bench 的双足全身 locomotion-manipulation 目标不同。若把 AlphaBrain policy 迁移到全身人形，应额外公开 humanoid asset、下身/全身 action adapter、站立与跌倒 predicate、foot-contact/碰撞日志，并在目标 humanoid benchmark 上重新 closed-loop 评测。

## 6. 最小复现清单

1. 锁定 AlphaBrain 仓库 commit、配置文件、基础模型与 LoRA/full-parameter 模式。
2. 为每个套件记录官方版本、许可证/ gated 资源、task split、场景生成器、机器人与相机配置。
3. 保存每 episode 的 seed、success/failure reason、完成步数、视频和汇总 CSV；持续学习另保存完整 T×T 矩阵。
4. 将 `no-pretrain`、外部数据预训练、target-only fine-tune 分开做消融，避免把数据来源收益写成 benchmark 本体收益。
