---
title: UnifoLM-VLA × LIBERO 正式规模复现：2000 集，98.10%
category: evaluation
kind: evaluation
organization: Embodied AI Map
releaseDate: 2026-09-10
summary: 对 UnifoLM-VLA-Libero 官方 checkpoint 在原始 LIBERO Panda 仿真中按官方协议完成 4 suite × 10 task × 50 trials = 2000 个 episode：总成功率 98.10%，与作者参考值 98.65% 相差 0.55 个百分点；含协议冻结表、失败分布与环境偏差说明。
tags: [libero, vla, reproduction, formal-scale, osmesa]
draft: false
references:
  - title: UnifoLM-VLA 官方仓库
    url: https://github.com/unitreerobotics/unifolm-vla
  - title: UnifoLM-VLA-Libero checkpoint（Hugging Face）
    url: https://huggingface.co/unitreerobotics/UnifoLM-VLA-Libero
  - title: LIBERO 官方仓库
    url: https://github.com/Lifelong-Robot-Learning/LIBERO
---

## 1. 结论

对 **UnifoLM-VLA-Libero** 官方 LIBERO 微调 checkpoint，在原始 LIBERO Panda 仿真中按官方协议评测 **2000 个 episode**：

- 总成功：**1962/2000 = 98.10%**
- 作者原环境参考：98.65%，差值 **−0.55 pt**
- LIBERO-Object 与参考值完全一致；差异集中在 LIBERO-Goal 与 LIBERO-Long 的少数长程 task 上

| Suite | 本次复现 | 成功/试验 | 作者参考 | 差值 |
|---|---|---|---:|---:|
| LIBERO-Spatial | **98.80%** | 494/500 | 99.0% | −0.20 |
| LIBERO-Object | **100.00%** | 500/500 | 100.0% | +0.00 |
| LIBERO-Goal | **98.40%** | 492/500 | 99.4% | −1.00 |
| LIBERO-Long（libero_10） | **95.20%** | 476/500 | 96.2% | −1.00 |
| **平均 / 合计** | **98.10%** | **1962/2000** | 98.65% | **−0.55** |

结论：作者公布的 LIBERO 结果可以在本地完整复现，四 suite 平均仅低 0.55 个百分点。差异落在扩散动作头随机采样与软件渲染栈的正常波动范围内，不需要额外的模型侧解释。

## 2. 评测协议冻结表

| 项目 | 值 |
|---|---|
| 模型 checkpoint | UnifoLM-VLA-Libero 官方权重（`pytorch_model.pt`，约 18 GB） |
| VLM 基座 | UnifoLM-VLM-Base（官方 HF 权重） |
| 归一化统计 | checkpoint 目录 `dataset_statistics.json`（4 个 `libero_*_no_noops` key） |
| 仿真 | LIBERO + robosuite 1.4.1 + MuJoCo 3.3.5，Franka Panda，OSC_POSE 控制器，20 Hz |
| 相机 | `agentview` + `robot0_eye_in_hand`，256×256 |
| 每 task 试验数 | 50（官方协议） |
| 单 episode 最大步数 | spatial 220 / object 280 / goal 300 / libero_10 520（另有 10 步物体稳定预热） |
| 观测历史 | window_size = 2 |
| 动作头 | DiT-L 扩散（flow-matching，4 步去噪），预测 16 步 chunk；执行队列 `deque(maxlen=8)` |
| 动作后处理 | `process_action()`：gripper [0,1]→[−1,1]、二值化、符号翻转（−1 开 / +1 合） |
| 成功判定 | LIBERO/BDDL `_check_success()`（`env.step` 返回的 `done`） |
| 随机性 | 公共 `seed=42`（numpy）；动作扩散采样未固定 torch 种子（与官方脚本一致） |
| 并行方式 | 4 个 suite 各一进程并行（suite 相互独立），单实例显存约 20 GB |
| 渲染后端 | OSMesa 软件渲染（本机 EGL 不可用，见 §4） |

## 3. 失败分布

38 个失败 episode 全部保留了 256×256 回放视频，分布为：Spatial 6 个、Object 0 个、Goal 8 个、Long 24 个。失败集中的 task：

| Suite · Task | 成功/试验 | 说明 |
|---|---|---|
| libero_10 · put the white mug on the plate and put the chocolate pudding to the right of the plate | 41/50（82%） | 全部 9 个失败中最集中的任务；双目标 + 空间关系 |
| libero_10 · put both moka pots on the stove | 45/50（90%） | 需要分别抓取两个物体 |
| LIBERO-Goal · open the top drawer and put the bowl inside | 46/50（92%） | 抽屉开启 + 放入的组合 |
| LIBERO-Goal · put the wine bottle on top of the cabinet | 47/50（94%） | 高位放置 |
| libero_10 · put both the alphabet soup and the tomato sauce in the basket | 47/50（94%） | 双物体长程 |
| libero_10 · put both the cream cheese box and the butter in the basket | 48/50（96%） | 双物体长程 |

其余失败分散在 spatial 的“碗放到盘子”系列与长程任务的单步波动上。失败模式与官方参考的差距同向（Long 与 Goal 更低），没有出现官方表现好而本地整体失效的 task。

## 4. 复现环境与偏差说明（协议未改动）

| # | 偏差 | 处理 | 对结果的影响 |
|---|---|---|---|
| 1 | 本机 NVIDIA EGL 设备栈无法初始化 | 改用 `MUJOCO_GL=osmesa` + `PYOPENGL_PLATFORM=osmesa` 软件渲染；相机、分辨率、控制频率与官方一致 | 只影响单步耗时（约 0.2–0.4 s/步） |
| 2 | 官方脚本将 `LIBERO_CONFIG_PATH` 指向仓库内不存在的目录，会触发交互式配置创建而阻塞 | 使用默认 `~/.libero/config.yaml` | 无 |
| 3 | `robosuite==1.4.1` 的键盘遥操作依赖（pynput→evdev）在本机编译失败 | `--no-deps` 安装并显式补装 `bddl / easydict / gym / cloudpickle / future / numba / python-xlib` | 无（headless 评测不加载该模块） |
| 4 | 官方脚本写失败 episode 视频时未指定编码器，imageio 默认 PyAV 插件会在首个失败 episode 抛异常并中断整个 suite | 补丁：`fps=10, codec="libx264"` | 只影响诊断视频，不影响成功率统计 |
| 5 | 中断后无法从中间 task 续跑 | 新增 `--args.task-start`（默认 0，与官方行为一致） | 无 |
| 6 | — | 4 个 suite 并行执行（suite 之间本无依赖） | 不改变协议 |

仓库内唯一被修改的文件是 `experiments/LIBERO/eval_libero.py`（+4 −1 行，即上述第 4、5 项）；其余全部为新增脚本、日志与报告。

## 5. 耗时与吞吐

| Suite | 评测用时（含模型加载约 4 min） | 平均单 episode |
|---|---|---|
| libero_object | 约 5 h 45 m | 41 s |
| libero_goal | 约 7 h 00 m | 50 s |
| libero_spatial | 约 7 h 15 m | 52 s |
| libero_10 | 约 11 h 45 m | 84 s |

模型单次推理约 0.2 s（每次预测 16 步 chunk）；瓶颈在 OSMesa 软件渲染的 `env.step`。4 suite 并行总墙钟约 11 h 45 m（串行约 32 h）。单实例约占 2 个 CPU 核与约 20 GB 显存（VLM 3B bf16 + DiT-L 动作头）。

## 6. 可复核要点

- 复现口径、逐 suite 明细、失败视频与官方日志已按 episode 归档，统计脚本从日志逐条解析，与视频一一对应。
- 要得到可比较的论文结论，至少锁定：checkpoint、VLM 基座、`unnorm_key`、`max_steps`、`window_size`、动作 chunk 执行长度、渲染后端与 seed；本页 §2 的表格可以直接作为模板。
- 本复现覆盖官方 4 个 suite 的全部 40 个 task，未使用 LIBERO-90 预训练数据；LIBERO 的套件结构见 [LIBERO Benchmark 条目](../../benchmarks/libero/)。
