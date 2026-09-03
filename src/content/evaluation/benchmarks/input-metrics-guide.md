---
title: Benchmark 输入与量化指标手册
category: evaluation
kind: guidance
organization: Embodied AI Map
releaseDate: 2026-09-02
summary: 对 HumanoidBench、Mimicking-Bench、LeVERB-Bench 与 SIMPLE 的 policy input、action output、主评分、推荐物理诊断量和统计聚合方式做统一定义，避免将离线 data metric 与闭环 benchmark score 混淆。
tags: [whole-body-humanoid, benchmark, inputs, metrics, evaluation-protocol]
draft: false
references:
  - title: HumanoidBench paper
    url: https://roboticsproceedings.org/rss20/p061.pdf
  - title: Mimicking-Bench paper
    url: https://arxiv.org/abs/2412.17730
  - title: LeVERB paper
    url: https://arxiv.org/abs/2506.13751
  - title: SIMPLE paper
    url: https://arxiv.org/abs/2606.08278
  - title: LIBERO official repository
    url: https://github.com/Lifelong-Robot-Learning/LIBERO
  - title: CALVIN official repository
    url: https://github.com/mees/calvin
  - title: RoboTwin 2.0 evaluation documentation
    url: https://huggingface.co/docs/lerobot/en/robotwin
  - title: SimplerEnv official repository
    url: https://github.com/allenai/SimplerEnv
  - title: BEHAVIOR-1K official repository
    url: https://github.com/StanfordVL/BEHAVIOR-1K
---

## 1. 先统一符号：一个 benchmark episode 是什么

第 $i$ 条 evaluation episode 从固定 reset state $s_0^{(i)}$ 开始。策略在每个控制时刻接收观测 $o_t$，输出 action $a_t$，物理环境推进到 $s_{t+1}$；直到成功、失败或最大时长 $H$。最终任务分数不是训练 loss，而是 evaluator 对完整轨迹 $	au_i$ 的判定。

$$
\mathrm{SuccessRate}=\frac{1}{N}\sum_{i=1}^{N}\mathbb{1}[\mathrm{predicate}(\tau_i)=\mathrm{true}]
$$

其中 `predicate` 必须由 benchmark/task 明确实现，例如“箱子被抬起且机器人未跌倒”，而不是“reward 超过某个未公开阈值”。

## 2. 输入/输出总表

| Benchmark | 必须或可选输入 | 输入中最容易被误用的字段 | 输出 action | 不能混淆的对照 |
|---|---|---|---|---|
| [HumanoidBench](../humanoidbench/) | 必须：robot proprioception、任务条件；可选：task-relevant object state、头部双相机 RGB、448-taxel tactile | object pose 是 privileged state；RGB 与 tactile 的频率、延迟和分辨率会改变难度 | 当前 robot XML actuator 对应的连续 control | state oracle、vision、vision+tactile 三套结果分表 |
| [Mimicking-Bench](../mimicking-bench/) | human reference motion、scene/object geometry、robot state；视觉字段以发布 runner 为准 | human motion 是参考，不是 robot joint command；未见 object mesh 不可用于训练 | retargeted reference 或 position/velocity/torque 型全身 control | 仅 retarget、tracking policy、scene-aware generation+tracking 分开 |
| [LeVERB-Bench](../leverb-bench/) | image history、language instruction、robot proprioception；task metadata 可含 objective/verb category | 图片/语言属于高层输入；真值 state 只能作 oracle | 高层 latent behavior + 低层 dynamics-level WBC action | image vs state、with/without language、不同 camera view 分开 |
| [SIMPLE](../simple/) | Isaac Sim visual stream、MuJoCo state/proprioception、task language/config；可选 demonstration context | 必须检查 render state 与 physics state 同步；不允许用 object GT 偷看 | whole-body action 或 action chunk，经 AMO/SONIC/adapter 落到 controller | state policy、vision policy、VLA/WAM、不同 data source 分开 |

### 2.1 每次论文都应把 input 写成字段表

| 字段 | 需要报告的具体信息 | 示例 |
|---|---|---|
| proprioception | joint/root/IMU/contact 是否包含、shape、归一化、历史帧数 | `qpos,qvel,base angular velocity`，不包含 object GT |
| visual | camera name、RGB/RGB-D/segmentation、resolution、FPS、delay、randomization | head RGB 2 views，$128\times128$，10 Hz，2-step delay |
| tactile | taxel 数、每个 taxel 内容、clip/normalize、采样频率 | 448×3 contact force，按 $	au_f$ clip |
| language/task | 原始文本、模板数量、tokenizer、是否有目标类别/pose oracle | “把红箱子搬到门边”；不输入目标 6D pose |
| human reference | pose representation、fps、future window、retarget mapping | SMPL-X root+hands，30 Hz，未来 20 帧 |
| action | control mode、维数、关节顺序、Hz、chunk、clip | joint-position target，$d_a=...$，50 Hz，chunk=4 |

没有这些字段，两个“success rate”并不具有可比性。

## 3. 主量化指标：核心全身 benchmark 各如何读数

| Benchmark | 官方/核心主指标 | 应如何汇总 | 具体例子 |
|---|---|---|---|
| HumanoidBench | 每任务 task success rate；论文同时报告 return | 按 27 task 列 success，再分别平均 locomotion / manipulation；不要只报总 return | `g1-door-v0`：门达到 task 定义开度且 robot 未提前失败才记 1 |
| Mimicking-Bench | 每个 household task 的 completion/success，重点是 seen vs unseen geometry | 六任务逐项列出，并把 training shape 与未见 chair/bed/box shape 分开 | `lift box`：箱体满足抬起条件、全身动作物理可执行，不是 hand tracking 小就得分 |
| LeVERB-Bench | vision-language closed-loop success；论文报告 10 categories / 150+ tasks 的分类/总体成功 | task 与 category success 分开；image/state、with/without language 分开 | 论文报告 LeVERB 总体 58.5%、简单视觉导航 80.0%；只能在同一设定下比较 |
| SIMPLE | per-task closed-loop task completion，论文强调大规模 policy benchmark 与 sim-real correlation | 60 task 逐项，另按 scene/object/instruction OOD 聚合 | 搬运：走到正确对象、稳定持物并到达目标，且无 fall/drop/非法终止 |
| LIBERO | per-task/suite episode success；终身学习可加 T×T 的 ASR/BWT/F | Spatial/Object/Goal/LIBERO-90/LIBERO-10 分开，明确 dataset revision 与预训练 | 不把 demonstration loss 或语言相似度当最终分数 |
| CALVIN | MTLC 与 LH-MTLC（连续 chain 完成长度） | 按 1–5 子任务、环境 split、sensor suite 分开 | 单步 success 不能替代 chain-level 结果 |
| RoboTwin 2.0 | clean2clean 与 clean2random success | 50 tasks 逐项，并分别聚合 easy/hard | 不混淆 14D action adapter 与其他机器人版本 |
| RoboCasa / RoboCasa365 | per-task success 与 seen/unseen 聚合 | atomic/composite、任务集和场景生成版本分开 | 子集结果不能写成全量 365-task 结果 |
| SimplerEnv | success + sim/real rank correlation（如 Pearson、MMRV） | visual matching、variant aggregation、仿真/真实分别报告 | 仿真成功率不是现实机器人成功率 |
| BEHAVIOR-1K | activity success predicate | 任务子集、场景/物体版本、长程失败类型分开 | 运行 subset 不能宣称覆盖 1,000 活动 |
| Habitat-Lab | success、SPL（导航）或 rearrangement task success | PointNav/ObjectNav/Rearrange/social nav 分开；RGB-D 与 oracle state 分开 | 导航 SPL 不能替代操作或双足全身成功 |
| ManiSkill | per-task success、return/效率；部分环境支持 real2sim 对照 | environment ID、robot、资产版本、并行规模和 observation track 分开 | 自定义任务结果不能冒充官方统一榜单 |

### 3.1 success 之外的量：必须标成“诊断”而非偷换主结论

| 量化指标 | 定义/单位 | 适合回答什么 | 不足以单独证明什么 |
|---|---|---|---|
| episode return $R=\sum_t r_t$ | reward 累加，无单位且依 reward scale | 训练是否收敛、reward shaping 是否工作 | 不同 task/method 的真实任务完成能力 |
| completion time / steps | 成功 episode 的控制步数或秒数；失败样本如何处理须说明 | 成功后谁更快 | 未成功时的能力，或安全性 |
| fall rate | $\#\mathrm{fall}/N$；须公开 fall threshold/termination | 双足稳定性 | 手部操作质量 |
| foot slip | 支撑脚接触期间的切向位移/速度积分，m 或 m/s | 行走/站立是否真实稳定 | 物体是否被正确操作 |
| drop rate | 已抓取后物体掉落的 episode 比例 | carry/hold 稳定性 | 是否拿到正确对象或完成最终放置 |
| collision / contact violation | 非允许 link/contact 或超过力阈的次数/比例 | 安全/场景交互质量 | 高层语义是否正确 |
| tracking error | root/hand/foot position error（m）、orientation error（rad/deg） | retarget 和 WBC 跟踪 | 完成实际家具/物体任务 |
| action jerk / energy proxy | $\|a_t-a_{t-1}\|$ 或力矩/功的明确公式 | 平滑、控制代价 | 任务成功；不同 action mode 下不可直接比 |

## 4. Benchmark 专属指标模板

### HumanoidBench

```text
每个 task: N_eval, success rate, return(mean±std), episode length,
fall/termination count, object-drop count（若有）, contact-force violation；
另列 observation = state / RGB / RGB+tactile、robot+hand、action mode、training steps、seeds。
```

其 tactile 版还应报告 taxel force 如何聚合/clip；视觉版还应报告 camera 参数。否则“多模态更好”的结论无法归因。

### Mimicking-Bench

```text
每个 task × geometry split: success rate, tracking error, contact consistency,
penetration, fall rate, foot slip；
另列 human reference source = synthetic/real、retarget method、scene/object split、control mode。
```

核心指标是 **新场景几何下的 task success**。只给 human-reference 的 MPJPE，说明的是拟合，不是 interaction generalization。

### LeVERB-Bench

```text
task/category success; overall success;
image-vs-state gap; with-language-vs-no-language gap;
visual OOD / language paraphrase / camera-view OOD success;
fall, collision, joint/torque-limit violation, completion time。
```

将论文中的 `58.5% overall` 复现时，必须同时报告 task subset、camera stream、language annotation version、WBC checkpoint 和 rollout count；缺少其中任何一项都不应称为同一数字。

### SIMPLE

```text
task success × {IID, object-OOD, scene-OOD, layout-OOD, instruction-OOD};
fall, foot slip, drop, invalid collision, force/joint-limit violation;
completion time, action jerk/energy proxy;
visual/state policy, VLA/WAM architecture, action chunk, controller, data source。
```

SIMPLE 的 MuJoCo physics 与 Isaac Sim rendering 同步错误会污染所有视觉指标；建议先以相同 rollout 抽查 object/root pose 差，再评价 VLA/WAM。

## 5. 统计、随机种子与不确定性

- 报 `N_eval`、evaluation seed 列表和 $\hat p \pm$ 置信区间或多训练 seed 均值/标准差；不可只展示最佳 checkpoint 一次运行。
- 对失败 episode，completion time、energy、tracking error 是丢弃、截断还是记为 horizon，必须写明。
- OOD 分数不要与 IID 混平均；object、scene、instruction、camera、physics 参数分别是不同泛化问题。
- 若输入包含 external dataset pretraining，主表旁报告 `no-pretrain / dataset-pretrain / target-finetune` 消融，否则 benchmark 提升无法归因。

这张手册与[Benchmark 对比指南](../comparison-guide/)配套使用：前者规定“怎么把数字写清楚”，后者解释“这些 benchmark 分别在考什么”。
