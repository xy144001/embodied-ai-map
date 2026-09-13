---
title: 重点数据集与入手路径
category: datasets
kind: dataset
organization: 具身机器人技术地图数据集组
releaseDate: 2026-09-04
summary: 从全身 humanoid、规模化真实轨迹和人类第一视角迁移三条线，整理重点公开数据集的获取条件、下载步骤和首轮实验建议。
tags: [datasets, acquisition, full-body, humanoid, open-data, VLA]
draft: false
references:
  - title: Psi-Zero / psi-data
    url: https://github.com/physical-superintelligence-lab/Psi0
  - title: AgiBot World Alpha
    url: https://huggingface.co/datasets/agibot-world/AgiBotWorld-Alpha
  - title: AgiBot World Beta
    url: https://huggingface.co/datasets/agibot-world/AgiBotWorld-Beta
  - title: Humanoid Everyday
    url: https://github.com/physical-superintelligence-lab/Humanoid-Everyday
  - title: DROID
    url: https://droid-dataset.github.io/droid/the-droid-dataset
  - title: EgoDex
    url: https://github.com/apple/ml-egodex
  - title: EgoVerse
    url: https://github.com/GaTech-RL2/EgoVerse
---

## 这组数据为什么值得先入手

这不是“所有数据集”的重新罗列，而是面向后续模型与数据生成实验的最小优先集：

- **全身 humanoid**：Psi-Zero / psi-data、Humanoid Everyday，先解决全身状态、动作和多模态同步。
- **规模化真实轨迹**：AgiBot World、DROID，用来扩大任务和本体覆盖，验证 VLA 的规模效应。
- **人类上游迁移**：EgoDex、EgoVerse，提供第一视角、人体姿态和任务语义，但必须经过 retarget，不能直接当机器人 action。

## 公开状态与获取入口

| 资源 | 主要内容 | 当前获取方式 | 体量与注意事项 | 建议用途 |
|---|---|---|---|---|
| [Psi-data / real](https://huggingface.co/datasets/USC-PSI-Lab/psi-data) | 9 个真实全身任务；视觉、人体/机器人状态和动作 | Hugging Face 公开下载；按任务 ZIP 获取 | 仓库整体约 418 GB，先下载单个任务验证流程 | 全身模仿学习、动作块与时间戳检查 |
| [Psi-data / simple](https://huggingface.co/datasets/USC-PSI-Lab/psi-data) | 6 个 SIMPLE 仿真全身任务及评测数据 | 同一 Hugging Face 仓库公开下载 | 需安装 SIMPLE / IsaacSim；可先跑单个任务 | Sim2Real、失败轨迹与域随机化 |
| [AgiBot World Alpha](https://huggingface.co/datasets/agibot-world/AgiBotWorld-Alpha) | 100,000+ 轨迹、100 台机器人、100+ 场景 | Hugging Face；可完整 Git LFS 或 sparse-checkout | CC BY-NC-SA 4.0；完整下载前先取约 7 GB sample | VLA 预训练、跨本体和多任务覆盖 |
| [AgiBot World Beta](https://huggingface.co/datasets/agibot-world/AgiBotWorld-Beta) | 1M+ 轨迹、约 2,976 小时、217 任务/87 技能 | Hugging Face gated dataset；登录并同意社区许可后下载 | 需要提交联系方式并接受许可；WebDataset Tar，规模很大 | 大规模预训练与 WebDataset 流式读取 |
| [Humanoid Everyday](https://github.com/physical-superintelligence-lab/Humanoid-Everyday) | Unitree G1/H1；约 260 任务；RGB、深度、LiDAR、IMU、关节、触觉 | 官方任务表逐任务下载；也有 LeRobot 与 lite 版本 | 原始约 500 GB，完整 LeRobot 版本约 1 TB；30 Hz | 多模态同步、全身 loco-manipulation |
| [DROID](https://droid-dataset.github.io/droid/the-droid-dataset) | 76k 轨迹、约 350 小时、跨 564 场景的真实操作 | Google Cloud Bucket；RLDS 约 1.7 TB，提供 100 episode 调试包 | raw 版本 5.6–8.7 TB；官方说明 raw 桶曾暂缺部分 episode | 规模化采集、RLDS loader、跨场景泛化 |
| [EgoDex](https://github.com/apple/ml-egodex) | 829 小时 30 Hz 第一视角视频、3D 手/头/上身姿态、语言标注 | Apple CDN 直接下载；test 约 16 GB，训练集分 5 个约 300 GB 分片 | CC BY-NC-ND；先下载 test，再选择 basic_pick_place | 人类动作先验、视觉表征和 retarget |
| [EgoVerse](https://github.com/GaTech-RL2/EgoVerse) | 第一视角人类活动、Aria/手部数据、Zarr/语言标注 | GitHub 代码公开；数据通过项目脚本和云存储凭据同步 | 不要把密钥写入仓库；数据版本更新后需刷新 episode hash | 人类上游迁移、动作先验和跨 embodiment |

> **开放不等于无条件下载**：AgiBot Beta 需要登录和社区许可；EgoDex 有非商业/禁止派生限制；DROID 和 EgoVerse 需要大容量云下载或凭据；Humanoid Everyday 通过任务表分发。许可、版本和数据卡应在下载当天再次核对。

## 第一轮入手步骤

### 0. 先准备环境与磁盘

1. 预留至少 **2 TB 可用空间**：先做小样本验证，不要一开始下载 DROID raw、EgoDex 全训练集或 Humanoid Everyday 完整 LeRobot 版本。
2. 准备 Python 3.10/3.11、Git LFS、`huggingface_hub`、解压工具和校验工具；训练阶段再按各项目 README 建独立虚拟环境。
3. 建议统一目录：

```text
data/
  raw/{psi,agibot,humanoid_everyday,droid,egodex,egoverse}/
  processed/lerobot/
  manifests/
  checksums/
```

### 1. 先跑最小可行样本

按下面顺序，不依赖昂贵 GPU：

1. **Psi-data / real**：下载一个任务 ZIP，解压后确认 `episode_*/data.json`、图像帧、动作字段和时间戳。
2. **AgiBot Alpha sample**：先拿 sample 或单个 task，确认 WebDataset/脚本能读出 observation、action 和 task_info。
3. **Humanoid Everyday 单任务**：从任务表下载一个 ZIP，用官方 `Dataloader` 读取 RGB、深度和 LiDAR。
4. **DROID 100 episodes**：先用 RLDS 调试包跑 Colab/loader，再决定是否拉取完整桶。
5. **EgoDex test**：用最小 test ZIP 检查 MP4 与 HDF5 是否按帧对齐。
6. **EgoVerse 小筛选**：先配置项目凭据并同步一个 filter，不下载全量。

### 2. 各资源的最短下载路径

#### Psi-data / real 与 simple

```bash
pip install -U huggingface_hub
hf auth login

# 真实全身任务（示例）
hf download USC-PSI-Lab/psi-data \
  real/Pick_bottle_and_turn_and_pour_into_cup.zip \
  --local-dir data/raw/psi --repo-type dataset
unzip data/raw/psi/real/Pick_bottle_and_turn_and_pour_into_cup.zip -d data/raw/psi/real

# SIMPLE 仿真任务（示例）
hf download USC-PSI-Lab/psi-data \
  simple/G1WholebodyXMovePickTeleop-v0.zip \
  --local-dir data/raw/psi --repo-type dataset
```

然后按 [Psi0 README](https://github.com/physical-superintelligence-lab/Psi0) 配置 `PSI_HOME`、`HF_TOKEN`，先做数据可视化，再运行对应的 fine-tune 或 SIMPLE evaluation 脚本。

#### AgiBot World Alpha / Beta

```bash
git lfs install

# Alpha：先拉样本或单任务
git clone https://huggingface.co/datasets/agibot-world/AgiBotWorld-Alpha

# Beta：先登录 Hugging Face 并在网页同意 gated community license，
# 再按官方卡片或 sparse-checkout 选择 observations / task_info。
```

Alpha 的官方脚本可把任务转换为 LeRobot；Beta 采用 WebDataset Tar，建议先写一个流式读取器，不要把全部视频一次性解压到内存。

#### Humanoid Everyday

```bash
git clone https://github.com/physical-superintelligence-lab/Humanoid-Everyday
cd Humanoid-Everyday
pip install -e .
```

从官方 task spreadsheet 下载一个任务 ZIP 后，用：

```python
from humanoid_everyday import Dataloader
ds = Dataloader("/path/to/task.zip")
print(len(ds))
ds.display_image(0, 1)
ds.display_depth_point_cloud(0, 1)
ds.display_lidar_point_cloud(0, 1)
```

确认 `data.json`、RGB、depth、LiDAR、IMU 和关节流的时间关系后，再使用仓库内 `scripts/he2lerobot.py` 转换。

#### DROID

先用官方 100 episode 调试包：

```bash
gsutil -m cp -r gs://gresearch/robotics/droid_100 data/raw/droid
```

确认 RLDS loader 能读取 `language_instruction`、`observation`、`action`、`is_first/is_last` 后，再按需要选择完整 RLDS（约 1.7 TB）或 raw 视频版本。raw 桶的完整性应以下载当天官方说明为准。

#### EgoDex

先下载最小 test 集：

```bash
curl "https://ml-site.cdn-apple.com/datasets/egodex/test.zip" -o data/raw/egodex/test.zip
unzip data/raw/egodex/test.zip -d data/raw/egodex/test
```

检查每个任务目录中的配对 `N.hdf5` / `N.mp4`，验证 HDF5 中第 `i` 帧姿态对应视频第 `i` 帧，再决定是否下载训练分片。

#### EgoVerse

```bash
git clone https://github.com/GaTech-RL2/EgoVerse.git
cd EgoVerse
uv venv emimic --python 3.11
source emimic/bin/activate
uv pip install -r requirements.txt
uv pip install -e .
```

按官方 README 配置**自己的**云存储凭据和访问脚本，使用 `sync_s3.py --filters <filter>` 拉取一个小筛选；不要复制、提交或在聊天中暴露任何密钥。下载后可用 `latent_inspector.py` 或 `zarr_data_viz.ipynb` 检查 episode、动作叠加和语言标注。

## 下载后的统一验收清单

每个资源先生成一份 manifest，再进入训练：

- episode 数、帧数、时长、磁盘大小和下载版本；
- observation / action / reward / termination / language 字段是否齐全；
- 相机、关节、IMU、触觉等多速率流的时间戳是否可对齐；
- 坐标系、关节顺序、单位、控制频率和本体标定是否记录；
- 成功、失败、截断和安全终止是否可区分；
- 许可证、数据用途限制、署名要求和是否允许再分发；
- 转换前后抽样可视化，保留原始文件和转换日志。

建议统一输出 `manifests/<dataset>-<version>.json`，并把每次转换脚本、命令行和校验结果一并保存。

## 我们的推荐起步顺序

**Psi-data / real → Humanoid Everyday 单任务 → AgiBot Alpha sample → DROID 100 → EgoDex test → AgiBot Beta / DROID 全量 → EgoVerse 筛选。**

这个顺序先验证全身数据链路和多模态同步，再逐步增加规模；只有在字段、时间戳和许可检查通过后，才进入大规模预训练或仿真数据生成。
