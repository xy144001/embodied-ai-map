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

为避免把“有论文”“有代码”和“有数据下载”混在一起，目录采用六个互斥的展示分区：

1. **可直接下载数据**：存在可验证的数据卡、Release、云存储、TFDS/RLDS 或官方下载脚本，点击后能拿到实际数据文件。
2. **申请/注册后可获取**：需要注册、签署研究条款、填写申请或登录后才能下载。
3. **部分开放**：只公开预处理子包、示例、镜像或部分模态，原始数据或完整版本受许可限制。
4. **采集系统**：描述如何采集示范（全身遥操作、MoCap、VR、leader-follower、robot-free 等），系统本身不等于数据集。
5. **仿真/Benchmark**：提供环境、任务、资产、评测脚本或可重复 rollout，通常需要在线生成轨迹，不应计入真实机器人训练数据。
6. **代码或论文入口**：目前只能确认论文、代码或项目说明，尚未找到可独立获取的数据包；论文链接不会被当作下载入口。

Open X-Embodiment 应视为一个数据集合并入口，下面的子数据集仍按独立来源记录，不能把 Open X 本身当作单一机器人本体数据集。采集系统、仿真环境、生成器和 benchmark 会保留在资源目录中，但不计入“独立可训练数据集”数量。

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

## 模型数据处理横向对照

当前的 SOTA 工作通常不会只依赖一种数据类别：机器人轨迹提供动作监督，视觉和语言数据提供场景与任务先验，人体视频和仿真数据用于扩展任务与本体覆盖；Full-body 任务还需要保留全身状态、接触和平衡信号。面向真实部署时，失败、恢复和环境变化样本同样重要。下表比较各模型如何组合这些数据并转换为训练监督，以及相关数据是否公开；单一形式的数据集通常不足以覆盖完整训练任务。

| 模型/工作 | 输入数据 | 对齐与转换 | 动作表示 | 训练目标 | 开放状态与本目录对应 |
|---|---|---|---|---|---|
| π₀、π₀.₅、π₀.₇ | 多机器人轨迹、人类视频、网页/视觉语言数据 | 按任务和本体混合；π₀.₅加入物体检测、语义子任务和语言条件 | 连续动作块；FAST 用离散余弦变换压缩高频动作 | 视觉语言预训练 + 语义子任务 + Flow Matching/动作 token | 完整训练混合未公开；对应 `Physical Intelligence π0/π0.5 training mixture` |
| X-VLA | 多来源、多本体机器人轨迹 | 不强行抹平来源差异，为每个数据源配置 soft prompt | Flow Matching 连续动作 | 跨本体联合训练 | 代码/模型公开；未形成独立新数据集 |
| GO-1 | AgiBot World 的多本体真实轨迹，含双臂、灵巧手和视觉触觉 | 统一采集平台 + 人工在环质量检查 | latent action | 大规模行为预训练与可预测规模化 | AgiBot World 已收录，可直接下载 |
| LingBot-VLA 2.0 | 约 5 万小时机器人轨迹 + 1 万小时人类第一视角视频 | 覆盖头、腰、移动底座和灵巧手自由度；增加视频/深度辅助信号 | 全身或多本体动作 | VLA 预训练 + 未来状态预测 | 训练混合未作为独立数据集开放 |
| Qwen-VLA | 机器人操作、人类 ego 视频、仿真轨迹、导航和视觉语言数据 | 用本体文字提示描述机器人和控制约定 | 统一动作与轨迹预测，DiT Flow Matching 解码 | 操作、导航、轨迹预测联合预训练 | 公开模型/代码；完整数据比例未公开 |
| UniFoLM-VLA-0 / UniFoLM-WMA-0 | 机器人操作数据、图文数据、LIBERO 等开放数据 | 按本体和任务配置 LeRobot 数据加载 | 机器人动作与全身动态预测 | 继续预训练 + 动力学/动作学习 | 代码和权重开放；训练混合不完整公开 |
| GR00T N1.7 + SONIC | 真实机器人、人类视频、仿真生成数据 | 转为 GR00T LeRobot v2；每个 episode 使用 MP4 + Parquet，并用 `modality.json` 描述状态/动作切片 | 拼接状态/动作数组，支持相对/绝对动作、归一化和时间采样 | VLA 预训练与本体适配 | GR00T 工具和部分数据开放；对应 GR00T data stack、GR00T X-Embodiment Sim |
| LingBot-VA / LingBot-VA 2.0 | 相机视频片段、语言、机器人动作 | 视频窗口 VAE 编码；动作映射到固定 30 维通道并按 checkpoint 选择通道 | 末端位姿 + 夹爪的动作流 | 视频 latent 与动作流联合去噪 | 代码、模型和部分 LIBERO/RoboTwin 数据流程开放 |
| Motus | 机器人视频、动作和可共享运动信息 | 光流提取像素变化，构建六层数据金字塔 | latent action / delta action | 视频生成、动作预测和世界模型联合训练 | 论文披露方法，完整混合数据未独立发布 |
| DreamZero | 异构机器人视频—动作数据，人类或其他机器人视频示范 | 以未来视频状态作为跨本体中间表征 | 视频条件动作 | 视频与动作联合建模，支持少量本体适配 | 模型论文公开；训练数据主要是混合来源 |
| Fast-WAM / Light-WAM / Faster-WAM | 机器人视频、动作块和 LIBERO/RoboTwin 轨迹 | 视频时间窗口；Light-WAM 在降采样 latent 空间监督未来，Faster-WAM 复用多层未来表征 | 动作块或轻量动作头 | 未来表征监督 + 动作预测 | 主要是模型/训练方法，不新增独立数据集 |
| MotionWAM | 第一视角视频、机器人示范和全身动作 | 三阶段适配：视频动态 → 第一视角 → 目标 humanoid | 统一 motion latent，覆盖腿、躯干、脚和手 | 视频世界模型 + 全身动作预测 | 论文公开；示范数据未单独开放 |
| WholeBodyVLA | 无动作人类 ego 视频 + 人体采集数据 | 人体动作采集、动作迁移与仿真校正 | 全身动作 + LMO 控制器命令 | latent 学习 + loco-manipulation RL | 方法公开；未形成独立大规模数据包 |
| DiT4DiT | 机器人视频与动作轨迹 | 从视频扩散中提取中间去噪特征，不要求重建全部未来帧 | 动作扩散/Flow Matching | 视频和动作双流联合目标 | 代码和模型入口公开；数据规模有限且非独立数据集 |
| ω-0 | 人类/公共视觉运动先验、仿真 replay、真实 humanoid 数据 | 控制器驱动仿真回放，将先验落到目标本体；采集多视角同步数据 | controller-compatible whole-body latent | 未来观测 latent 预测 + 全身动作生成 | `ω-HOME` 是明确的新数据资源，需在主目录单独建卡 |
| Cosmos Policy / Cosmos 3 | 视频、动作、语言、图像、音频和合成数据 | 多模态统一 token 化；Cosmos 3 公开合成数据与评测基准 | 视频/动作联合生成 | 世界模型、视频生成和策略训练 | Cosmos 3 的合成数据与 benchmark 建议补入仿真/生成分区 |
| OpenHLM | 仿真状态、真实 humanoid 观测和动作 | 仿真到真实对齐，按任务生成 rollout | 全身动作 | 生成管线 + Sim2Real | 本目录按“数据生成器”收录，不当作单一数据集 |
| Dexora / Helix 02 | Dexora 真实双臂数据；Figure Helix 内部 humanoid 数据 | 平台内部同步与动作映射，公开细节有限 | 双臂/末端或内部动作 | VLA/通用操作训练 | Dexora 数据可下载；Helix 训练数据为商业内部 |

## 近期模型工作中已确认可公开获取的数据

这一节只统计上表所提到、并且已经找到官方数据入口的数据。**模型开源、论文公开或“使用了公共数据”不等于该模型的完整训练集开源**。因此按两个口径统计：

- **按可独立下载的资源包计数：10 个**。其中 `psi-data` 是同一个 Hugging Face 数据仓库，下面按真实和仿真两个可训练分区展示，但总数只计 1 个仓库。
- **按可训练分区计数：11 个**。`psi-data` 拆成 `real` 和 `simple` 两个分区后，再加上其余 9 个公开数据集/数据包。
- **Psi-Zero 任务粒度：15 个任务子集**，即 9 个真实全身任务 + 6 个 SIMPLE 仿真全身任务；任务子集不是 15 个相互独立的数据集。

| 数据集/分区 | 来源工作 | 可获取内容 | 开放方式 | 训练用途 |
|---|---|---|---|---|
| [Psi-data / real](https://huggingface.co/datasets/USC-PSI-Lab/psi-data) | Psi-Zero | 9 个真实全身遥操作任务，含视频、`data.json`、任务描述和统计文件 | Hugging Face 直接下载；仓库提供原始数据到 LeRobot 的转换脚本 | G1 全身操作、模仿学习和 Ψ₀ 微调 |
| [Psi-data / simple](https://huggingface.co/datasets/USC-PSI-Lab/psi-data) | Psi-Zero | 6 个 SIMPLE 仿真全身 locomotion-manipulation 任务及评测数据 | Hugging Face 直接下载；可在 SIMPLE 中复现 rollout | 全身策略训练、仿真评测和 sim-to-real |
| [AgiBot World Alpha](https://huggingface.co/datasets/agibot-world/AgiBotWorld-Alpha) | GO-1 | 92,214 条真实机器人轨迹（Beta 的精选子集） | Hugging Face 直接下载；配套任务目录和转换工具 | 多本体操作、双臂和视觉触觉策略 |
| [AgiBot World Beta](https://huggingface.co/datasets/agibot-world/AgiBotWorld-Beta) | GO-1 | 1,003,672 条真实机器人轨迹，约 43.8T 数据 | Hugging Face 直接下载；提供 LeRobot 转换和 GO-1 训练代码 | 大规模机器人行为预训练 |
| [DROID](https://droid-dataset.github.io/) | π₀.7、Open X 等 | 跨场景 Franka 真实机器人操作轨迹、视频和语言任务 | 官方入口公开，下载需按数据使用协议申请/确认 | 跨本体操作预训练和行为克隆 |
| [Ego4D](https://ego4d-data.org/) | Qwen-VLA | 大规模第一视角人类活动视频及时间/动作标注 | 公开申请账号并接受许可条款后下载 | 人体视觉先验、语言和动作理解 |
| [EPIC-KITCHENS](https://epic-kitchens.github.io/) | Qwen-VLA | 厨房场景第一视角视频、动作片段和语义标注 | 官方网站提供下载，需遵守数据许可 | 人体操作、物体交互和长时程动作建模 |
| [EgoDex](https://github.com/apple/ml-egodex) | Qwen-VLA、Psi-Zero | Apple Vision Pro 采集的灵巧手/人手第一视角视频与姿态标注，含训练、测试和附加数据 | 官方 GitHub 提供分卷直链下载 | 人体到机器人动作迁移、灵巧操作预训练 |
| [EgoVerse](https://github.com/GaTech-RL2/EgoVerse) | Qwen-VLA | 第一视角人类示范、相机位姿、3D 头部跟踪和语言标注；当前版本约 80k episodes | GitHub 代码公开；数据通过项目云存储/同步脚本获取，需配置访问凭据 | 人类示范到机器人策略迁移 |
| [Humanoid Everyday](https://huggingface.co/datasets/USC-PSI-Lab/humanoid-everyday) | Qwen-VLA、Psi-Zero | Unitree G1/H1 全身示范，覆盖约 260 个任务；RGB、深度、LiDAR、IMU、关节和触觉 | Hugging Face/项目页提供下载与 LeRobot 读取方式 | 全身操作、locomotion-integrated 任务和多模态学习 |
| [Xperience-10M](https://huggingface.co/datasets/ropedia-ai/xperience-10m) | Qwen-VLA 中所称 Xperience | 第一视角 RGB、深度、姿态和动作相关的大规模人类数据 | Hugging Face 提供公开数据卡；按数据卡许可获取 | 人体动作先验、世界模型和跨本体迁移 |

### 开放状态汇总

| 状态 | 数量（按上面的可训练分区口径） | 说明 |
|---|---:|---|
| 可直接下载 | 6 个分区（对应 5 个仓库） | Psi-data（real/simple 两分区）、AgiBot World Alpha/Beta、EgoDex、Humanoid Everyday |
| 公开入口但需申请、配置凭据或接受许可 | 4 | DROID、Ego4D、EPIC-KITCHENS、EgoVerse |
| 公开数据卡/镜像，需按项目许可核对 | 1 | Xperience-10M；下载前应再次确认当前版本和授权范围 |
| **合计** | **11 个可训练分区** | 不包含 π₀.7、GEN-1.5、Skild S1、Gemini Robotics 2、Motus2 的内部训练混合 |

这里的“可公开获取”不表示所有数据都能无条件商用：有些数据需要注册、签署使用协议、配置云端凭据，或仅允许研究用途。目录中的开放状态应以数据集官方页面和当前许可为准，不把模型权重或论文附件重复算作数据集。

这张表的用途是解释“数据如何被加工后才进入模型”，不是重新统计数据集数量。后续核验应优先补充每个模型的原始数据来源、episode 切分规则、时间同步误差、失败样本处理、归一化统计和许可证。

## 数据处理闭环

`采集/生成 → 同步与标定 → 清洗与切分 → 标注 → 质量控制 → 格式统一 → 数据划分 → 训练 → 评测与诊断 → 数据回流`

这是一条持续迭代的闭环，而不是一次性流水线。评测需要定位模型在任务、场景、身体接触、失败状态或传感信息上的缺口，再回到采集、清洗和标注环节补充数据，更新版本后重新训练与评测。

## 使用本条目

完整的交互式目录、Full-body 优先排序、采集系统卡片、仿真资源卡片、数据格式比较和可下载索引，见[具身智能数据集可视化总览](https://xy144001.github.io/embodied-ai-map/datasets/)。

后续新增或修订数据集时，优先补充本目录下的 Markdown 条目，并在 `references` 中提供论文、官方项目页、数据卡或下载入口。对于未公开资源，保留来源和开放状态，但不要将其统计为可直接训练数据。
