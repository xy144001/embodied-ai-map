---
title: Open X-Embodiment：跨本体机器人学习数据联盟
category: evaluation
kind: dataset
organization: Google DeepMind and collaborators
releaseDate: 2023-10-01
summary: 以 RLDS 统一多机构真实机器人轨迹的数据与工具集合，用于跨本体视觉—语言—动作预训练及转移评测；覆盖广但原生重心是机器人操作，不是全身双足移动操作。
tags: [robot-learning, cross-embodiment, rlds, vla, transfer-learning]
draft: false
references:
  - title: Official Open X-Embodiment repository
    url: https://github.com/google-deepmind/open_x_embodiment
  - title: Project page and RT-X evaluation
    url: https://robotics-transformer-x.github.io/
  - title: Open X-Embodiment paper
    url: https://arxiv.org/abs/2310.08864
---

## 1. 数据卡

[Open X-Embodiment](https://github.com/google-deepmind/open_x_embodiment) 目标是把多机构开源机器人数据统一为便于下游消费的格式。官方 repository 指出每个数据集由 episode 序列组成，采用 [RLDS](https://github.com/google-research/rlds) episode format，并提供贡献数据集的 spreadsheet/citation；软件为 Apache-2.0，其他材料为 CC-BY 4.0，但**原始子数据集可能仍有各自的使用条件**，应逐一核验。[官方仓库](https://github.com/google-deepmind/open_x_embodiment)

| 层 | 内容 | 如何用于 humanoid |
|---|---|---|
| episode | step 序列、observation、action、任务语义（字段随来源数据集不同） | 建立跨数据统一 loader 与 modality/action adapter |
| 本体 | 多实验室、多种真实机器人与操作任务 | 预训练视觉、语言—动作表征；不能假定 action space 可直接共享 |
| 评测 | RT-X 项目对多机构真实机器人/新技能做 transfer evaluation | 作为上游 VLA 泛化证据；须再做目标 humanoid closed-loop 测试 |
| 许可 | 代码 Apache-2.0、材料 CC-BY 4.0、来源数据逐项确认 | 创建数据 manifest，记录每个 dataset 的可用范围 |

## 2. 在评测中如何正确使用

### 数据选择与输入

选取的子数据集、机器人、相机、语言字段、动作 representation、时间对齐和 action normalization 必须显式列出。不要把“RLDS 格式一致”误解为“各机器人动作语义一致”：一个数据集的 Cartesian delta、夹爪开合与另一个的 joint command 不可直接拼接。

### 输出和指标

- **离线预训练/验证**：动作/trajectory prediction、语言—视觉条件的行为预测、held-out robot/task/domain 的 success 或 task-specific score。
- **目标 humanoid 测试**：将模型输出映射到机器人上肢/手/base/下肢控制接口，在固定仿真场景闭环执行；报告 HumanoidBench/Isaac Lab 上逐任务 success、跌倒、碰撞、时长和 OOD split。
- **数据比例消融**：比较 only-target、Open X pretrain + target finetune、不同 source mixture；否则不能区分跨本体 transfer 与目标数据量效果。

## 3. 部署与限制

官方 repo 提供转换和使用工具；Python/TensorFlow/RLDS/数据存储的具体版本以所选 release README 为准。工程上先读取一条 episode，打印 schema、camera tensor、action dtype/shape、timestamp 和 task string，再构建 batch pipeline。原始数据规模大、异构且许可不同，建议对每个子集生成 immutable manifest（URL、version、license、fields、preprocess hash）。

Open X 的本体跨度是优势，也是全身评测的边界：它大多支持通用操作预训练而非双足移动中操作。文中若将它称为“humanoid dataset”，必须明确指出这只是预训练迁移意义，而非全身人形原生 benchmark。

## 4. 代表工作怎样训练、怎样测试

**RT-1-X / RT-2-X** 是官方代表协议：将多个来源 RLDS episode 的 observation/action 先 canonicalize，再在多机器人数据上训练同一视觉—语言—动作策略；论文的 RT-X 实验实际选用 9 种 manipulator 训练，并在真实机器人、目标环境和 emergent-skill 任务上与“仅用该目标数据训练”的模型比较 success。它测试的是跨本体正迁移与新技能泛化。用于 humanoid 时应复制这一对照：`target humanoid only` 对比 `Open X pretrain + target finetune`，随后在 HumanoidBench/SIMPLE 的固定 test episodes 报 success、fall/drop 和 OOD；RLDS action 不可未经 adapter 直接输出给 humanoid。
