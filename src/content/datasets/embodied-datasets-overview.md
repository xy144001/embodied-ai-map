---
title: 具身智能数据集全景与 Full-body 专题
category: datasets
kind: roadmap
organization: 具身机器人技术地图数据集组
releaseDate: 2026-09-02
summary: 按数据资源、采集系统、仿真生成、数据格式、规模口径和任务覆盖整理 2022—2026 年具身智能数据，并单独梳理 Full-body 机器人相关资源。
tags: [datasets, embodied-ai, full-body, humanoid, data-collection, simulation]
draft: false
references:
  - title: 具身智能数据集可视化总览
    url: https://xy144001.github.io/embodied-ai-map/datasets/
  - title: Open X-Embodiment
    url: https://robotics-transformer-x.github.io/
  - title: LeRobot 数据集格式
    url: https://huggingface.co/docs/lerobot/lerobot-dataset-v3
  - title: RLDS
    url: https://github.com/google-research/rlds
---

## 调研范围

本条目覆盖 2022-01-01 至 2026-09-01 发布或持续维护的具身智能数据资源。时间窗外的经典资源只用于解释数据格式、采集范式和研究演进。资源按谱系去重，不把同一项目的论文、代码、数据包和 benchmark 重复计数。

数据资源分为五类：真实机器人训练数据、人类示范与动作上游数据、仿真与合成数据、benchmark/任务库，以及论文或商业系统中提到但尚未独立公开的数据。Open X-Embodiment 应视为一个数据集合并入口，下面的子数据集仍按独立来源记录，不能把 Open X 本身当作单一机器人本体数据集。

## 负责人四个问题

### 1. 有哪些具身数据集

当前重点资源包括：Open X-Embodiment 及其子数据集、RT-1、RT-2、BridgeData、DROID、ALOHA、Mobile ALOHA、RoboMIND、AgiBot World、RH20T、CALVIN、LIBERO、RoboCasa、BEHAVIOR-1K、HumanoidBench、H2O、TWIST、HumanPlus、Motion-X、AMASS、GRAB、PROX、RoboTwin 和各类人体动作、运动先验资源。

目录还保留未独立开放或仅在论文中描述的资源，但会明确标记“可直接下载”“需申请/注册”“部分开放/分散获取”“仅代码/论文”“商业/内部”和“开放状态待核验”。论文、项目页、数据卡和下载入口之间是否形成交叉证据，也单独记录，避免把“论文提到”误写成“数据已开源”。

### 2. 数据通过什么采集系统获得

真实示范主要来自以下采集范式：

- 全身遥操作：H2O/OmniH2O、HumanPlus、TWIST、HOMIE 等，用人体姿态、动捕或外骨骼驱动 humanoid。
- 沉浸式视觉遥操作：Open-TeleVision、AnyTeleop 等，用头显、手部跟踪和主动视觉采集上身或双臂动作。
- Leader-follower：ALOHA、GELLO 等，用结构相近的 leader 设备直接产生目标关节监督。
- VR、手柄和多站点工作站：BridgeData、DROID 等，适合跨场景采集机械臂轨迹。
- Robot-free 手持设备：UMI 等，先在机器人不到场时采集环境示范，再做可行性修复和动作映射。
- 多模态接触工作站：RH20T 等，同时记录相机、关节、力/触觉和物体交互。

采集系统本身不等于数据集。系统卡需要说明：硬件组成、控制与记录频率、时间同步、标定方式、人体到机器人映射、数据是否公开，以及由该系统实际产出了哪些数据资源。引用量和仓库关注度只能作为影响力代理，不能直接等同于真实用户人数。

### 3. 数据采用什么格式和组织方式

需要区分文件容器与语义规范：

- 文件容器：HDF5、Zarr、Parquet、TFRecord、ROS bag、MCAP、视频文件和 WebDataset Tar 分片。
- 组织规范：RLDS/TFDS、Open X-Embodiment、LeRobot 等，描述 episode、step、observation、action、reward、termination 和语言指令。
- 机器人元数据：关节定义、坐标系、相机内外参、URDF/MJCF、控制模式、固件和标定版本。
- 动作表示：关节位置/速度/力矩、末端位姿、增量动作或高层技能；转换时必须记录原始表示和目标表示。

人形机器人尤其需要保存硬件时间戳、时钟来源、同步误差和缺帧策略。视觉通常约 30 Hz，关节约 500 Hz，力/触觉可能达到 1 kHz；简单降采样可能丢失落脚冲击、失衡、接触变化和恢复触发信号。电子皮肤、足底压力、麦克风和语音指令也应记录采样率、坐标系、校准状态及与 episode 的时间关系。

### 4. 数据规模多大、覆盖哪些任务

规模不使用单一“轨迹数”比较，而是分别记录小时数、episode、帧数、磁盘体积、机器人和操作者数量、场景、物体、任务、技能、语言指令，以及成功/失败比例。真实采集、人体上游、仿真 rollout 和生成轨迹必须分开统计。

任务覆盖统一归入：locomotion 与导航；抓取、放置和基础操作；双臂协作；移动操作与 loco-manipulation；工具使用与接触丰富操作；全身搬运、推拉、开门和环境交互；人机协作；跌倒、扰动、失败恢复和安全行为；长时程组合任务。

## Full-body 边界与重点

Full-body 不是由机器人外形决定，而是由 episode 中实际受控的身体部分和任务耦合决定：

- 核心层：腿、躯干、双臂或双手协同，或任务显式要求移动—操作、平衡—接触耦合。代表包括 H2O、TWIST、HumanPlus、HOMIE、HumanoidBench 等。
- 扩展层：平台是 humanoid 或高自由度双臂，但公开任务主要由躯干、双臂和手完成，下肢没有持续参与。代表包括部分 RoboMIND、AgiBot World、Open-TeleVision 资源。
- 对照层：移动机械臂、四足带臂或其他相邻形态，可验证数据组织、任务泛化和 loco-manipulation，但不能直接证明双足平衡能力。代表包括 Mobile ALOHA、RoboCasa、BEHAVIOR-1K、GrandTour 等。

Full-body 数据的主要缺口是：真实长时程任务较少，locomotion 与 manipulation 常被分开记录，足底接触、根部状态、负载转移、多接触、跌倒和恢复样本不足。人体动作数据需要 retarget 后才能成为机器人监督，必须同时保存原始人体动作、机器人参考动作、接触信息和修正结果。

## 仿真与合成数据

仿真资源应独立于真实采集系统记录，主要包括三类：

1. 仿真任务库：提供 MuJoCo、Isaac、PyBullet 等环境、资产、任务定义和评测脚本，可在线生成可重复 rollout。代表包括 HumanoidBench、ManiSkill、RoboCasa 和 BEHAVIOR-1K。
2. 数据生成器：从少量示范、人体动作或场景资产合成状态—动作序列。代表包括 MimicGen、RoboTwin、X-Humanoid 和 GR00T X-Embodiment Sim。
3. Sim2Real 桥接：围绕坐标系、动力学随机化、接触模型和控制频率，评估仿真策略迁移到真实本体时的差异。

跨架构持续学习、类脑 VLA、RL Token、CosmosPolicy 等属于模型或训练方法；它们可以调用仿真环境，但本身不应作为仿真数据集条目计数。只有其中公开的环境、任务库、生成器或可复用数据管线才进入数据资源目录。

## 最低字段与建议标准

### 所有可训练 episode 的最低字段

- 时间戳、采样频率和 episode 边界；
- observation、可执行 action 和控制模式；
- 机器人本体、关节定义、坐标系和传感器标定；
- 任务结果、数据来源、版本、许可和已知限制。

### 提升研究价值的增强字段

- 语言指令、任务阶段、技能和物体身份；
- 失败原因、人工干预、扰动和恢复过程；
- 力、触觉、接触、操作者、固件和标定质量；
- 未见物体、未见场景和跨本体测试划分。

### Full-body 专用字段

- 根部姿态、IMU、全身关节和质心代理；
- 足底接触、手物接触、负载和环境支撑；
- 躯干、髋、膝、踝与双臂的协调关系；
- 安全中止、失衡、跌倒、恢复触发条件和恢复结果。

这些字段是从现有数据集反复出现的实际需求中提炼出的建议标准，不代表现有数据集已经全部满足。语言、触觉、音频等模态也不是所有任务的统一必需项，是否必需取决于任务和学习目标。

## 数据处理闭环

`采集/生成 → 同步与标定 → 清洗与切分 → 标注 → 质量控制 → 格式统一 → 数据划分 → 训练 → 评测与诊断 → 数据回流`

这是一条持续迭代的闭环，而不是一次性流水线。评测需要定位模型在任务、场景、身体接触、失败状态或传感信息上的缺口，再回到采集、清洗和标注环节补充数据，更新版本后重新训练与评测。

## 使用本条目

完整的交互式目录、Full-body 优先排序、采集系统卡片、仿真资源卡片、数据格式比较和可下载索引，见[具身智能数据集可视化总览](https://xy144001.github.io/embodied-ai-map/datasets/)。

后续新增或修订数据集时，优先补充本目录下的 Markdown 条目，并在 `references` 中提供论文、官方项目页、数据卡或下载入口。对于未公开资源，保留来源和开放状态，但不要将其统计为可直接训练数据。
