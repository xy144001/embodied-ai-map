---
title: Psi0 × SIMPLE 复现：DR 分级结果与数据一致性缺陷
category: evaluation
kind: evaluation
organization: Embodied AI Map
releaseDate: 2026-09-11
summary: Psi0 checkpoint（step 40000）在 SIMPLE 的 16 个可测任务 × 3 个 DR 级别 × 5 集上完成 240 集闭环：总成功率 46.2%，与 README 可比的 29 个级别为 48.3% vs 75.9%；同时定位并修复 8 项数据/代码/环境缺陷。
tags: [simple, g1, whole-body-humanoid, reproduction, domain-randomization, data-consistency]
draft: false
references:
  - title: SIMPLE 项目页
    url: https://psi-lab.ai/SIMPLE/
  - title: SIMPLE 官方仓库
    url: https://github.com/physical-superintelligence-lab/SIMPLE
  - title: SIMPLE 论文
    url: https://arxiv.org/abs/2606.08278
---

## 1. 结论

在完整跑完的 48 个数据集上（唯一未完成的 `LocomotionPickBetweenTables` dr-level-2 按约定排除）：

- **总体正确率：111/240 = 46.2%**（成功集数 / 已评测集数）
- 与 README 公开值可比的 29 个级别：**本地 70/145 = 48.3%　vs　README 220/290 = 75.9%**
- 分组：操作类 Teleop 70/135 = 52%；MP 系（AMO 行走 + 操作）27/60 = 45%；行走类 12/40 = 30%；sonic 2/5（发布文档注明官方实测 0/5）
- 四个异常任务（XMovePick 0/15、HugContainer 0/15、XMoveBendPickMP 1/15、Variant5MP 0/15）合计仅 1/60；剔除后其余任务为 110/180 = 61%
- 过程中发现并修复 8 项数据/代码/环境缺陷，其中 3 项直接恢复了 3 个任务的正常评测

评测管线本身经逐层验证工作正常（§4），失败可归因于两类因素：**评测数据/配置与 checkpoint 训练条件不一致**，以及 **checkpoint 自身能力**。

## 2. 评测协议

| 项目 | 说明 |
|---|---|
| 协议 | 16 个可测任务 × 3 个 DR 级别（dr-level-0/1/2）× 5 集 + sonic 5 集 |
| DR 级别定义（README） | L0 视觉 & 干扰物随机化；L1 增加极端光照；L2 再增加目标物体初始位姿扰动 |
| 推理服务 | 每任务一个专用 checkpoint 服务（ckpt step 40000，RTC=train 模式，action-exec-horizon=24） |
| 编排 | 3 条并行评测车道（每车道串行跑多个任务、每任务换服务）+ 2 条旁路修复链；支持断点续跑 |
| 结果口径 | 每集二值成功（任务自带 `check_success`）；统计文件 `eval_stats.txt` / `summary.json`；每集含相机视频 |
| 数据校验 | 25 个评测 zip（sha256 = LFS oid）、18 个训练 zip、22 个 checkpoint 逐字节校验通过 |

范围说明：仓库 25 个 G1Wholebody 任务 = 16 个可测（数据 + checkpoint 齐备）+ 1 个 sonic（独立管线）+ 8 个无 checkpoint 发布（未纳入）。

## 3. 分组结果（vs README 公开值）

README 列为该任务 L0|L1|L2 各级别 10 集公开值；“—”表示未公开。

### 操作类 Teleop

| 任务 | L0 | L1 | L2 | 合计 | README |
|---|---|---|---|---|---|
| CloseDoorTeleop | 4/5 | 4/5 | 4/5 | **12/15（80%）** | 10 \| 10 \| 10 |
| HandoverTeleop | 3/5 | 4/5 | 1/5 | **8/15（53%）** | 7 \| 7 \| 10 |
| OpenFaucetTeleop | 2/5 | 2/5 | 1/5 | **5/15（33%）** | 3 \| 3 \| 4 |
| OpenOvenTeleop | 3/5 | 3/5 | 1/5 | **7/15（47%）** | 7 \| 5 \| 4 |
| OpenTrashCanTeleop | 3/5 | 3/5 | 2/5 | **8/15（53%）** | — |
| PushOfficeChairTeleop | 5/5 | 4/5 | 2/5 | **11/15（73%）** | — |
| BendHandoverTeleop | 3/5 | 4/5 | 5/5 | **12/15（80%）** | — |
| BendPickTeleop | 2/5 | 2/5 | 3/5 | **7/15（47%）** | — |
| PickAndPlaceAndHugContainerTeleop | 0/5 | 0/5 | 0/5 | **0/15（0%）** | 7 \| 6 \| 3 |
| **小计** | | | | **70/135 = 52%** | |

### MP 系（AMO 行走 + 操作）

| 任务 | L0 | L1 | L2 | 合计 | README |
|---|---|---|---|---|---|
| BendPickMP | 5/5 | 5/5 | 4/5 | **14/15（93%）** | 10 \| 10 \| 10 |
| TabletopGraspMP | 5/5 | 5/5 | 2/5 | **12/15（80%）** | 10 \| 10 \| 8 |
| XMoveBendPickMP | 0/5 | 0/5 | 1/5 | **1/15（7%）** | — |
| LocomotionPickBetweenTablesVariant5MP | 0/5 | 0/5 | 0/5 | **0/15（0%）** | — |
| **小计** | | | | **27/60 = 45%** | |

### 行走类与 sonic

| 任务 | L0 | L1 | L2 | 合计 | README |
|---|---|---|---|---|---|
| XMovePickTeleop | 0/5 | 0/5 | 0/5 | **0/15（0%）** | 10 \| 10 \| 6 |
| XMoveBendPickTeleop | 4/5 | 2/5 | 3/5 | **9/15（60%）** | 10 \| 9 \| 9 |
| LocomotionPickBetweenTablesTeleop | 2/5 | 1/5 | —（未完成） | **3/10（30%）** | 7 \| 5 \| 6 |
| XMoveBendCarryBoxSonic | 2/5 | — | — | **2/5（40%）** | 发布文档注明官方实测 0/5 |

**总计：111/240 = 46.2%。**

读法：原地操作任务的管线健康度最好，主要变量是 checkpoint 在各 DR 级别下的鲁棒性；MP 金标准任务（BendPickMP、TabletopGraspMP）复现良好；行走类任务分化明显（从 0% 到接近公开值），指示问题不在“行走功能整体失效”，而在逐任务的数据/权重一致性。

## 4. 异常案例与缺陷

### 4.1 XMovePick 0/15：数据与训练条件不一致的完整案例

症状：README 公开 10|10|6 的 checkpoint 本地 15 集全败；视频显示机器人整集站在桌边几乎不动（“不尝试”而非“尝试失败”）。

逐层排查（全部有实证）：

| 层 | 手段 | 结论 |
|---|---|---|
| 模型 checkpoint | 离线回放：训练帧 + 状态直连推理服务 | ✅ 正常（行走窗口输出 vx 0.43/0.49，录制值 0.44/0.50，逐块吻合） |
| 服务 / RTC / 预处理 | 同上 + 服务端日志 | ✅ 正常 |
| 状态构造 | 客户端公式 vs 训练数据逐项数值比对 | ✅ 完全一致 |
| 执行链 | 实时调试打印 WBC 消费值 | ✅ WBC 收到并传递指令 |
| **输入图像** | **严格 A/B：同一状态换图像** | ❌ **决定性变量**：训练图像 → 行走 0.43；评测图像 → 空转 0.001 |

数据侧根因（已修复 2 处）：

1. **材质 DR 不一致**：训练数据 99/99 集 `material=null`，评测数据为金属度 0.95–0.99 的 `SET(4)` → 评测时桌子渲染成黑色镜面，视觉完全 OOD。修复：评测数据 `material→null`。
2. **指令模板过期**：评测数据用 `"bend to pick up the { }"`，训练实际为 `"move forward to pick up the { }"`（代码类已在 commit 099ffc5 修正，但 HF 数据未同步）。修复：3 级 × 10 集全部对齐。

修复后：材质对齐后模型恢复行走指令输出（峰值 0.43 m/s），视频中机器人开始靠近、弯腰、伸手抓箱——**但从“不动”变成“抓而不起”，依然 0/15**。

结论：该 checkpoint 的评测数据与训练条件存在明确不一致（已定位并修复可见项，足以解释“行为异常”）；**即使完全对齐训练条件，本地仍无法复现 README 的 10|10|6**。残余差异在“抓取 + 抬升”执行环节，建议后续做 shadow-replay（同帧对比模型输出）或换低负载机器复验。

### 4.2 其余异常

- **HugContainer 0/15**：训练/评测的材质与指令一致；视频显示部分阶段可执行（能接近、接触物体），失败发生在多阶段流程的后段（“pick → hug container → walk → place”中的行走/放置环节），待做逐阶段分析。
- **XMoveBendPickMP 1/15、Variant5MP 0/15**：两者本地无训练数据可比对，异常待独立排查；Variant5MP 的评测在补齐 `max_episode_steps` 后才可正常运行（§4.3 第 5 项）。

### 4.3 本次发现并修复的缺陷清单

| # | 缺陷 | 类别 | 影响 | 修复 |
|---|---|---|---|---|
| 1 | XMovePick 评测数据指令模板过期 | 数据 | L0–L2 指令 OOD | 3×10 集模板对齐训练 |
| 2 | XMovePick 材质 DR 不一致 | 数据 | 评测渲染黑色镜面桌面，策略拒绝行动 | 评测数据 `material→null` |
| 3 | OpenFaucet 指令模板过期 | 数据 | 潜在指令 OOD | 3×10 集对齐训练 |
| 4 | XMoveBendPickTeleop 任务 uid 遗留命名（`g1_sonic_*` vs 数据集 `g1_wholebody_*`） | 代码 | 3 个级别全部 0 集退出（AssertionError） | 模块 uid 对齐数据集 |
| 5 | Variant5MP 缺 `max_episode_steps` | 代码 | episode 无上限（实测 3 h 45 m / 25632 步不终止） | 补 `"max_episode_steps": 1200` |
| 6 | 3 个任务模块在当前版本缺失（XMoveBendPickMP / XMoveBendPickTeleop / Variant5MP） | 代码 | 数据 + checkpoint 齐备但无法评测 | 从 git `8e5fe20` 恢复模块并注册 |
| 7 | EGL/NVIDIA 驱动栈版本错配（内核 570.124.06 / 用户态 570.211.01） | 环境 | 容器内 GPU 渲染无法初始化 | 内置同版本库 + `LD_LIBRARY_PATH` 覆盖 |
| 8 | 评测目录权限 / 服务 TLS 挂起 / 缓存重建慢 | 环境 | 冒烟失败、服务启动挂起、每容器约 10 min 重建缓存 | root 建目录 + chown；离线环境变量；持久化缓存卷 |

为支撑本轮评测构建了编排工具链：任务服务生命周期管理 + 断点续跑（orchestrate.py）、三车道编排与实时仪表盘、跨入口视频路径统一、全量数据完整性校验（评测 25 zip / 训练 18 zip / checkpoint 22 项逐字节校验）。

## 5. 口径与建议

1. 本页数字是**小样本回归**（每任务 × 每 DR 级别 5 集），不是官方规模复现值；裸成功率跨任务差异大，报告时必须带 DR 级别拆分与逐任务表。
2. 数据侧建议：XMovePick / OpenFaucet 的评测数据存在与训练不一致的模板与材质配置，建议上游同步修正；其余任务数据未发现同类问题。
3. 高并发负载使单集耗时 15–45 分钟，对超时敏感任务可能不利；争议结果应在低负载机器上复验。
4. 未覆盖对象：另有 8 个任务（BendPickAndPlaceMP / BendPickAndPlaceOnSofaMP / BendPickAndPlaceTeleop / PickAndBendPlaceMP / PickNPlaceMP / TabletopHandoverMP / XMoveAndHandoverMP / XMoveAndPickMP）无公开 checkpoint，待发布权重后补测。

SIMPLE 的任务结构、双模拟器设计与数据资产见 [SIMPLE Benchmark 条目](../../benchmarks/simple/)；运行时与扩展方式见 [SIMPLE 运行时与扩展指南](../../guides/simple-runtime-guide/)。
