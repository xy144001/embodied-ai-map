---
title: GRAB：全身抓取与接触重定向数据集
category: evaluation
kind: dataset
organization: Max Planck Institute / TU Eindhoven
releaseDate: 2020-08-25
summary: 10 名受试者与 51 个日常物体交互的全身 3D grasp 数据，包含人体/脸/手姿态、物体姿态和从网格计算的接触，适合 human-to-humanoid 接触与动作先验研究。
tags: [whole-body-humanoid, human-object-interaction, mocap, contact, retargeting]
draft: false
references:
  - title: GRAB project and dataset access
    url: https://grab.is.tue.mpg.de/
  - title: GRAB paper
    url: https://arxiv.org/abs/2008.11200
  - title: Official GRAB code
    url: https://github.com/otaheri/GRAB
---

## 1. 数据定位与可获得性

[GRAB](https://grab.is.tue.mpg.de/)（GRasping Actions with Bodies）是**全身人—物抓取**数据：10 位受试者与 51 个不同形状/大小的日常物体交互。官方介绍明确给出全身形状与姿态序列（含脸和手）、3D 物体姿态，以及由网格推导的 body-object contact。[论文](https://arxiv.org/abs/2008.11200) 数据与代码面向 research purposes，下载页要求登录/同意条款；因此它是可申请获得的研究数据，不应标成无条件 public-domain。

## 2. 统一数据卡

| 维度 | 内容 | 对全身人形的用途 |
|---|---|---|
| 主体 | SMPL-X 风格全身 shape/pose，含手和脸；MoCap 原始标记拟合 | 作为全身姿态参考；需重定向到机器人关节/手 |
| 物体 | 51 个物体的 3D 几何与逐帧 6D pose | 构造物体相对运动、抓取/放置目标和仿真碰撞体 |
| 交互 | 人体—物体表面距离/接触可由拟合网格计算 | 接触奖励、接触时序、手/躯干协同诊断 |
| 覆盖 | 10 subjects、日常 whole-body grasp 行为 | 有全身性但规模有限；不等同家庭长时程移动任务 |
| 获取/许可 | 官方站点注册下载，官方代码辅助读取 | 下载前核验当前 license；不可将受限资产直接再发布 |

## 3. 在仿真/评测中怎样用

### 输入准备

1. 选定 subject/object/action split；将 SMPL-X 全身姿态、物体 mesh 和 pose 统一到仿真世界坐标。
2. 对人形机器人做 retarget：匹配 root 朝向、脚接触相位、双手末端轨迹、物体相对位姿；不要直接复制人体关节角。
3. 将物体 mesh 转换为目标引擎格式，校验尺度、重心、碰撞体与摩擦；GRAB 的几何接触不自动等价于仿真接触。

### 训练与评测输出

- **motion imitation**：输出 robot joint/control trajectory；测 root/hand/foot 位置误差、姿态误差、接触一致率、足滑、跌倒/关节限位和任务完成。
- **grasp/interaction generation**：输入对象几何、初始人/机器人状态或 object trajectory，输出手/全身姿态和接触；测物体成功抓取/稳定保持、接触 precision/recall、penetration、物体—手相对误差和多样性。
- **泛化**：按未见 subject、物体或物体类别划分；训练/测试不能让同一物体 mesh 的近重复序列泄漏。

GRAB 原论文使用它训练 GrabNet，展示对未见物体形状的手抓取生成；这证明的是 human grasp representation 的泛化，不是 humanoid 真机成功率。[论文](https://arxiv.org/abs/2008.11200)

## 4. 限制

人体与机器人在手指、质量、力矩、足底和接触模型上有根本差异。GRAB 适合作为**参考动作/接触先验**或 retarget 评测数据；最终需在目标 robot 的物理仿真中闭环执行，并报告 object success 与安全指标。

## 5. 代表工作怎样训练、怎样测试

GRAB 原论文的 **GrabNet** 是最直接的例子：训练时输入物体 3D shape 和条件变量，目标是生成与物体接触的左右手抓取；测试时在 held-out object shapes 上生成抓取，并比较手部/顶点位置误差、接触质量与多样性。这个测试证明对**未见物体形状的手抓取生成**，不证明双足 humanoid 已能搬运。用于全身 robot 时，常见训练是以 GRAB 的 body/hand/object 序列作 retarget/contact prior；测试应把 held-out object sequence 重放到目标引擎，报告 grasp/hold/place success、掉落、接触持续率、穿透、足滑与跌倒，并按 subject/object/action 分离 train/test。
