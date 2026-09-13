---
title: LeVERB-Bench：视觉—语言闭环全身控制 Benchmark
category: evaluation
kind: benchmark
organization: University of California, Berkeley
releaseDate: 2025-06-16
summary: 论文提出的 sim-to-real-ready humanoid vision-language WBC benchmark：10 个类别、150+ 闭环任务，以重定向 MoCap、写实 Isaac Sim 渲染和语言指令共同测试视觉语义如何转成全身动力学动作。
tags: [whole-body-humanoid, vision-language-action, closed-loop, sim-to-real, benchmark, synthetic-data]
draft: false
references:
  - title: LeVERB paper
    url: https://arxiv.org/abs/2506.13751
  - title: Paper PDF
    url: https://people.eecs.berkeley.edu/~sastry/pubs/Pdfs%20of%202025/XueLeVERB2025.pdf
  - title: LeVERB-Bench Dataset
    url: https://huggingface.co/datasets/ember-lab-berkeley/LeVERB-Bench-Dataset
---

## 1. Benchmark 卡片：它在考“看懂并动起来”

[LeVERB](https://arxiv.org/abs/2506.13751)论文提出 LeVERB-Bench：10 个类别、150+ humanoid whole-body control 闭环任务。它的关键区分是：策略不能只获得“向前 $x$ 米”或“手到某 pose”的手工 action vocabulary，而要从**视觉观测和语言指令**选择一个可由低层 WBC 执行的全身行为。[论文 PDF](https://people.eecs.berkeley.edu/~sastry/pubs/Pdfs%20of%202025/XueLeVERB2025.pdf)

具象地说，指令可能要求 robot 看到某对象后走向特定区域、绕开障碍、转身或做全身姿态动作；评分要求它在视觉闭环中选对行为且低层动作不失稳。论文报告 LeVERB 方法在简单视觉导航子集为 80.0% success、跨任务总体为 58.5%；这些是**该论文方法与其设定**的结果，不是任何后续方法的默认分数。

## 2. benchmark 带的数据与资产

| 数据/资产层 | 具体内容 | 如何产生 | 用于哪一层 |
|---|---|---|---|
| human motion reference | 人类 MoCap 经 retarget 的运动学全身轨迹 | 将人类动作映射到 humanoid；再在物理中执行/筛选 | 为低层 WBC 和行为 vocabulary 提供可行行为参考 |
| rendered visual data | 第一人称与第三人称视角的写实图像；场景背景、对象属性、相机视角可程序随机化 | Isaac Sim 光线追踪渲染 | 训练/测试 vision-language 高层；测遮挡/外观/视角扰动 |
| language data | 对行为/任务的自然语言指令；论文称可人工或 VLM 标注 | 绑定 task/verb/objective 类别 | 评估指令语义到行为选择 |
| task metadata | `task_name`、`objective_category`、`verb_category`、`task_index` 等字段可在公开 Hugging Face dataset viewer 看到 | 任务标注与索引 | 分类别统计、采样与去泄漏 |
| robot/control data | humanoid proprioception、低层 WBC 需要的 dynamics state、全身 action/rollout | benchmark/simulator 运行时产生 | 把 latent behavior 变成稳定关节级动作 |

论文/第三方数据说明报告 vision-language 数据约 17.1 小时、154 trajectories，language-only 数据约 2.7 小时、460 trajectories；使用者应下载公开数据卡/实际 release 后核验字段和 license，而非假定所有物理资产都随论文无门槛发放。

## 3. 输入 → 输出 → 判分：一条闭环链路

| 层 | 输入 | 输出 | 失败的具体样子 |
|---|---|---|---|
| perception/VL | camera image history + language command | latent verb / behavior code | 选错方向、误解对象、对遮挡敏感 |
| WBC | latent behavior + proprioception | dynamics-level whole-body command | 选对高层意图却跌倒、足滑或超限 |
| environment | action、scene、初始 robot/object state | next observation、contact、termination、task condition | 撞障碍、未达到目标、违反接触/姿态条件 |
| evaluator | 完整 rollout | success/failure、类别汇总、视频/日志 | 不能只以 offline latent classification 计分 |

例如“视觉导航”任务中，policy 先从图像/指令识别应向哪个目标移动，随后 WBC 连续输出稳定步态动作。若高层方向正确但下身失去平衡，或 robot 抵达错误目标，episode 均应失败；因此 success 同时测语义理解和全身物理执行。

## 4. 评测标准与应报告的表格

- **主指标**：每 task / category 的 closed-loop success rate；论文整体结果为 58.5%，基线/消融也应在相同 task set、视觉流、语言模板和 rollout 条件下比较。
- **模态消融**：图像 vs privileged state、带语言 vs 无语言、egocentric vs third-person、是否使用视觉随机化；这些不能混入同一平均值。
- **泛化**：按未见背景/纹理、对象外观、相机位姿、遮挡、指令措辞和初始状态拆分。渲染轨迹相邻帧或同一人类动作的近似增强不能跨 train/test。
- **全身物理诊断**：跌倒、足滑、碰撞、动作/关节/力矩越界、完成时间与物体掉落（任务含对象时）。
- **真机对照**：若主张 sim-to-real，使用同一语言指令、success predicate、相机标定和控制延迟设置，在真机另报 success；不以仿真高分替代真机。

## 5. 外部数据集如何合理接入

- AMASS/其他 MoCap：扩充行为参考，必须与 benchmark test task/trajectory 去重；
- HumanML3D：可预训练语言—动作表示，但没有视觉场景/物体接触标签；
- EgoBody/H2O：可预训练 ego visual front end，不能替代 humanoid WBC action supervision；
- GRAB/OMOMO：可添加接触或物体搬运行为，但应另建 task/success predicate，不能改变原 LeVERB-Bench 分数含义。

## 6. 访问、复现与边界

公开可核验入口包括论文和 [LeVERB-Bench Dataset](https://huggingface.co/datasets/ember-lab-berkeley/LeVERB-Bench-Dataset)。当前资料页不假定完整 simulator/evaluator 代码、资产和所有任务均已在同一 release 开源；复现前应核对 data card、许可证、benchmark runner、Isaac Sim 版本和 humanoid asset。

它最适合回答“视觉/语言条件能否触发正确的全身行为并稳定执行”。对精细手部抓取、长时程多对象家务或通用 sim-to-real，不应单凭这一 benchmark 的分数下结论。
