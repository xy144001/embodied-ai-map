---
title: 数据集文件结构与字段目录：从磁盘文件到仿真变量
category: evaluation
kind: guidance
organization: Embodied AI Map
releaseDate: 2026-09-02
summary: 汇总本目录九个数据集的官方发布格式、目录/字段语义、哪些字段可转成虚拟 humanoid 的观测或参考，且明确人体姿态文件不是机器人关节命令。
tags: [whole-body-humanoid, dataset-schema, file-format, retargeting, simulation]
draft: false
references:
  - title: BEHAVE official data repository
    url: https://github.com/xiexh20/behave-dataset
  - title: AMASS archive and tools
    url: https://amass.is.tue.mpg.de/
  - title: HumanML3D official repository
    url: https://github.com/EricGuoICT/HumanML3D
  - title: RH20T API
    url: https://github.com/rh20t/rh20t_api
  - title: Open X-Embodiment
    url: https://github.com/google-deepmind/open_x_embodiment
---

## 1. 读文件前的三条规则

1. `pose`、`trans`、SMPL/SMPL-X 参数描述的是**人类参数化身体**；它们不是“机器人关节 A 的角度”。转成 humanoid action 前必须做骨架映射、根坐标/尺度对齐、IK、限位与动力学控制。
2. 文件结构会随 release/subset 变化。下面仅把官方项目页、官方 loader/README 明确给出的结构当作“发布格式”；下游论文的缓存 `.npy/.pt` 是其预处理，不是原始数据标准。
3. `RGB-D`、`mp4`、`HDF5`、`RLDS` 等容器不保证字段完全一致；加载器应先打印一个 episode/sequence 的 schema、shape、单位、时间戳和坐标系，再批量转换。

## 2. 逐数据集文件结构与字段

### GRAB：人体—物体 MoCap（需注册下载）

- **发布组织**：官方数据提供以 sequence 为单位的参数化全身/手/脸与 object motion；配套 [GRAB code](https://github.com/otaheri/GRAB) 用 SMPL-X、物体 mesh 和 sequence 参数读取/可视化。
- **核心内容**：每帧人体全身 pose、shape、global translation/orientation、手部/脸部参数，及物体 6D pose；可由人体与物体网格算接触/距离。官方项目描述为 10 subjects × 51 objects 的全身抓取。
- **仿真转换**：`SMPL-X pose/trans` → robot root/手/脚目标；`object mesh + 6D pose` → collision mesh、质量/摩擦和目标物体轨迹；接触由引擎重算并与 mesh-derived contact 分开存。
- **常见下游使用**：GrabNet 以对象形状为条件生成手抓取；human-to-humanoid 工作把它作为全身接触/末端参考，而非直接关节控制标签。

### BEHAVE：多视角 RGB-D 人—物交互

官方 [loader README](https://github.com/xiexh20/behave-dataset) 指定解压后核心目录：

```text
BEHAVE/
├── calibs/                 # 每个采集地点的 Kinect intrinsics/extrinsics
├── objects/                # 20 个物体的 3D scan / mesh / texture
├── sequences/              # 每段交互 sequence
│   └── <sequence>/
│       ├── t*/             # 时间帧：各相机 color/depth 等原始观测
│       ├── smpl_fit_all.npz    # 人体 SMPL 拟合序列（发布/下游 loader 使用）
│       └── object_fit_all.npz  # 刚体 object pose 拟合序列
└── split.json              # 发布的 train/test sequence 划分（以实际版本为准）
```

`calibs` 将像素/深度转进世界坐标；`objects` 给视觉 mesh 与物理碰撞体来源；`smpl_fit_all.npz` 是人体参数轨迹，`object_fit_all.npz` 是物体刚体姿态序列。现有工作从 RGB-D 估计人/物 mesh/pose 或 contact；仿真里应分别测**视觉估计误差**和“估计状态驱动后”的 grasp/carry success，不能用 GT fit 混入视觉结果。

### OMOMO：对象运动条件的全身操作

官方 [release](https://github.com/lijiaman/omomo_release) 发放数据、训练脚本、文本标注压缩包和 `evaluation_metrics.py`。每条样本的语义单元是：**object geometry + object motion sequence + full-body human motion sequence**；论文说明覆盖 15 个对象、约 10 小时交互。实际下载目录/序列文件名以该 release 的数据说明为准，不能假定为公开统一 NPZ schema。

仿真读取时至少抽取 `(T, 3/6D) object trajectory`、人体 root/关节/hand/foot 序列、对象 mesh 与 fps；输出 robot reference 或 policy action，并报告 hand-object relative pose/contact、object tracking/hold、足滑/跌倒。OMOMO 原工作以 object motion → human motion 评估未见 object/motion 的生成质量；物理可执行性是后续 humanoid 实验新增的一层。

### AMASS：统一人体 MoCap NPZ

AMASS 官方工具说明单个数据文件含控制**性别、pose、shape、global rotation、translation、soft-tissue dynamics**的参数。典型 MoSh++ archive 以 `.npz` 存储：

```text
<AMASS-subset>/<subject>/<sequence>_poses.npz
  gender        # 人体模型性别标签
  betas         # shape coefficients
  poses         # 每帧 SMPL+H/SMPL-X pose parameters（含 global + articulated body/hand）
  trans         # 每帧 root translation
  mocap_framerate
  dmpls         # 软组织动态参数（若该 release 含有）
```

键/维度可能随 SMPL、SMPL-H、SMPL-X 版本变化，loader 必须读取实际 key；`poses[:, i]` 仍是**人体**轴角参数。Human2Humanoid、HOVER、ASAP 等运动模仿管线会把它重定向为 robot reference，再从 tracking、足滑、跌倒、扰动恢复与 sim-to-real 评价。

### HumanML3D：语言—3D motion 的预处理发布包

官方 [repository](https://github.com/EricGuoICT/HumanML3D) 明确给出目录：

```text
HumanML3D/
├── new_joints/          # 每条 motion 的 3D joint position 序列
├── new_joint_vecs/      # rotation-invariant / rotation feature vectors
├── texts/               # 每条 motion 的一个或多个自然语言描述
├── Mean.npy, Std.npy    # feature normalization
├── train.txt, val.txt, test.txt
└── animations/          # 可视化视频（发布包中提供）
```

`new_joints/<id>.npy` 是 22-joint 人体 3D 坐标序列；`new_joint_vecs/<id>.npy` 是模型输入特征；`texts/<id>.txt` 保存描述及时间片段信息（具体行格式以 repo parser 为准）。T2M/扩散工作用官方 split 计算 FID、R-precision、diversity/multimodality；把生成 motion 放入 humanoid 时还必须测 retarget 后的物理可行性。

### H2O：第一人称双手—物体交互

官方 [project/code](https://github.com/taeinkwon/h2o)发布视觉与标注读取工具。样本由同步的 ego/multi-view 图像/深度、左右手 3D pose/mesh 参数、object pose 与交互动作构成；具体 folder name、标注 JSON/NPZ key 以下载版 README 为准。模型常以 RGB-D 输入预测双手/物体 pose 或交互类别；这类输出可变成 humanoid 双手抓取目标，但没有下肢 trajectory、足部 contact 或 robot torque。

### EgoBody：自我中心和多视角人体交互

官方 [EgoBody repo](https://github.com/sanweiliti/EgoBody)列出 MVSet/EgoSet/EgoSet_interactee，并报告：Azure Kinect 同步第三人称 RGB-D、HoloLens2 ego RGB、eye gaze、hand/head tracking、深度、SMPL-X/SMPL 标注以及 train/val/test frame 统计。典型访问按 scene/sequence/frame 存多视角 image/depth、camera calibration 和人体参数；具体压缩包路径需注册下载后按 release index 读取。

现有工作用它进行 ego/multiview 3D pose、shape/mesh 和交互感知评估；仿真里应把预测的人/头/手/视线状态视作 observation 前端，和 GT-oracle 对照，再在 robot task 上测 collision、reaction delay 和 success。

### RH20T：真实机器人多模态 episode

官方 [API](https://github.com/rh20t/rh20t_api)说明：

```text
RH20T/
├── configs/configs.json     # 各 robot configuration；API 的必需元数据
├── <scene/episode>/         # 视觉、传感器与动作的时间序列
│   ├── *.mp4                # RGB-D 存储容器；extract.py 可还原原始帧
│   ├── camera/calibration   # 内外参/坐标变换（随实际 release 组织）
│   └── robot/force/audio/action time series
└── human demonstration video
```

官方项目说明每 episode 含 visual、force、audio、action 及对应 human demo，机器人平台含 arm、F/T sensor、gripper、in-hand/global RGB-D cameras 和 microphones。loader 会按 timestamp 对齐/插值。下游 one-shot/multimodal policy 用这些真实 action/感知训练；迁移到 humanoid 时必须重新定义 action adapter，RH20T arm action 绝非 humanoid 全身关节命令。

### Open X-Embodiment：RLDS 跨本体 episode

官方 [README](https://github.com/google-deepmind/open_x_embodiment)规定每个贡献数据集是 RLDS episode 序列：

```text
Dataset (TFDS/RLDS)
└── episode
    └── steps[]
        ├── observation      # RGB/RGB-D/state 等；字段随 source dataset 不同
        ├── action           # source robot action；语义/shape 随本体不同
        ├── reward / discount（若 source 提供）
        ├── is_first / is_last / is_terminal
        └── language/task metadata（若 source 提供）
```

RLDS 统一的是 episode/step 组织，不统一每个 source 的 action physical meaning。RT-1-X/RT-2-X 等工作先为各数据源 canonicalize observation/action，再训练跨本体策略；把它转到 humanoid benchmark 时要显式写出 source action normalization、目标 robot decoder 和 target-only finetune，随后闭环测 target success。

## 3. 把“字段”变成虚拟 humanoid 输入输出

| 原始字段例子 | 可作为 | 不能直接作为 |
|---|---|---|
| AMASS/GRAB `poses`, `trans` | motion reference、root/末端目标 | robot actuator command |
| BEHAVE `color/depth`, camera calibration | vision observation、world-frame state estimation | 已完成的 robot manipulation label |
| `object_fit_all.npz` / OMOMO object trajectory | object goal/condition、物理重放参考 | 稳定 grasp 的证明 |
| RH20T `action` | source-arm policy supervision | 不同 humanoid 的全身 action |
| Open X RLDS `steps.action` | cross-embodiment pretraining source | 可直接拼接的同语义动作 |

最终实体是 `virtual_robot.observe() → algorithm.act() → simulator.step()`；所有人类/异构机器人字段必须在这个接口之前通过可版本化转换器。
