---
title: ManiSkill-HAB（MS-HAB）：家居重排与全身控制 Benchmark（迁移参考）
category: evaluation
kind: benchmark
organization: UC San Diego / HAOSU Lab
releaseDate: 2024-12-18
summary: 基于 ManiSkill3 的开源 home-scale low-level manipulation benchmark，复现 Home Assistant Benchmark 的长时程家居重排任务，并提供低层控制、GPU 并行、RL/IL baseline 与轨迹数据生成；默认本体非双足 humanoid，故作为迁移参考。
tags: [home-rearrangement, whole-body-control, maniskill, imitation-learning, benchmark, transfer-only]
draft: false
references:
  - title: MS-HAB project page
    url: https://arth-shukla.github.io/mshab
  - title: Paper
    url: https://arxiv.org/abs/2412.13211
  - title: Official code
    url: https://github.com/arth-shukla/mshab
---

## 1. 定位

[MS-HAB](https://arth-shukla.github.io/mshab)（ManiSkill-HAB）将 Home Assistant Benchmark 的家居重排任务落到支持 realistic low-level control 的 GPU 并行环境。官方项目页列出长时程任务 **TidyHouse、PrepareGroceries、SetTable**，并将它们拆成 Pick、Place、Open、Close 等技能；训练/评估可以使用 RL、IL 及规则过滤后的 demonstrations。

它与全身 humanoid 的关联在于：技能链需要同步 manipulation 和 navigation，项目页称其 baseline 使用 whole-body control（同时控制 manipulation 与 navigation）。不过其默认 robot 不是双足 humanoid，所以不能将 MS-HAB 分数并入 HumanoidBench/SIMPLE 的全身榜单。

## 2. 输入、输出与量化指标

| 项 | 具体内容 | 测试时量化什么 |
|---|---|---|
| observation | 低层 robot state、场景物体状态、2 路 $128\times128$ RGB-D（论文描述的环境设置） | state/visual policy 的 task/subtask success |
| action | navigation 与 manipulation 的低层 control | 是否在物理接触下完成 pick/place/open/close，而非 magical grasp |
| task | TidyHouse、PrepareGroceries、SetTable 及其子任务/目标对象 | 子技能 success、长时程任务成功、碰撞/安全条件 |
| demonstrations | 从 RL policy 采样并经行为/安全条件过滤的 trajectory | IL 与 RL 的 data efficiency / task success |

论文明确给出 Pick success 的一个例子：达到目标条件且累积 robot collision 小于指定阈值（原配置为 5000 N）；这说明 success predicate 可同时要求任务完成与安全。报告应分别列 Pick/Place/Open/Close 的 success，再列三项长时程任务完成率，避免让一个长任务 0% 掩盖已可用的低层技能。

## 3. 如何为 humanoid 使用它

MS-HAB 最适合作为“家庭场景、长时程 task graph、低层接触操作与 demo filtering”的迁移基准。若换成双足 humanoid，必须新增：足部接触、fall termination、foot slip、下身 action、支撑切换与上身—下身协调；重写之后的结果应命名为 `MS-HAB-inspired humanoid protocol`，不能称原 MS-HAB 成绩。

## 4. 访问与部署

官方仓库给出 conda Python ≥3.9、ManiSkill3 `mshab` branch、asset/data 下载及训练/评估脚本。项目页报告 GPU 并行在机器人与动态对象交互、渲染两路 $128\times128$ RGB-D 时可达 4300+ samples/s；这属于所述配置下的吞吐，不是所有硬件的保证。复现需锁定 ManiSkill branch、asset bundle、control mode、demo filter 和 success/safety阈值。
