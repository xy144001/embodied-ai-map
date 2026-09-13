---
title: OMOMO：大物体全身操作与对象轨迹条件数据
category: evaluation
kind: dataset
organization: Stanford University
releaseDate: 2023-09-28
summary: 面向大尺寸物体操作的全身人—物运动数据与生成任务，提供物体几何、物体运动和人体运动；适合测试双手接触、全身协调和未见物体泛化。
tags: [whole-body-humanoid, human-object-interaction, locomotion, motion-generation, contact]
draft: false
references:
  - title: OMOMO project page
    url: https://lijiaman.github.io/projects/omomo/
  - title: Paper
    url: https://arxiv.org/abs/2309.16237
  - title: Official code and data instructions
    url: https://github.com/lijiaman/omomo_release
---

## 1. 数据卡

[OMOMO](https://lijiaman.github.io/projects/omomo/)（Object MOtion guided human MOtion synthesis）聚焦人类操作大尺寸物体：官方项目页说明数据含 15 个物体、约 10 小时交互，提供 3D object geometry、object motion 和 human motion。[论文](https://arxiv.org/abs/2309.16237) 的生成问题是“给定对象状态序列，合成全身姿态”，并以手位置作为中间表示以加强手—物接触。

| 数据层 | 含义 | 可映射到机器人评测的量 |
|---|---|---|
| 物体几何 | 3D 物体形状 | 物理引擎 collision mesh、尺度和抓取区域 |
| 物体状态 | 时序 position/orientation | 条件目标、物体轨迹 tracking 与 task completion |
| 人体运动 | 全身姿态序列 | base/脚/躯干/双手的 retarget 参考 |
| 文本（release 提供） | object-motion 数据的文本标注压缩包 | 可做语言条件生成；需核验标注与动作一一对应 |

## 2. 评测范式

论文的生成模型评测包括**未见动作**、**未见物体**和 Blender 设计的对象运动等条件，关注动作自然性、接触与生成质量。将其用于 humanoid 仿真时，建议构造两层结果：

- **人类动作生成层**：输入 object trajectory（可加文本/初始状态/几何），输出 human full-body pose；计算 hand-object position/contact error、foot skating、body penetration、运动分布 FID/多样性（若使用训练好的 feature evaluator）。
- **人到机器人执行层**：将生成/GT 人体序列 retarget 到 humanoid，输入同一物体轨迹或 task goal，输出 robot control；在物理引擎测 object tracking/搬运成功、接触稳定性、双手协同、足滑/跌倒、碰撞和能耗。

不要用“人体序列很好看”替代 robot feasibility。特别是大物体操作中，物体重量、把手形状和机器人手部自由度决定了能否执行。

## 3. 获取与部署

官方 [repository](https://github.com/lijiaman/omomo_release) 提供代码、数据说明、`evaluation_metrics.py` 和 MIT code license。安装/使用时按仓库 requirements 建 Python 环境；数据预处理、人体模型许可和 Blender 可视化是额外依赖。官方 README 还提供文本标注包。先跑一个 sequence 的 object pose + human pose 可视化，再导入 MuJoCo/Isaac Lab 验证坐标、fps、单位和物体 mesh。

## 4. 局限

OMOMO 是**人类—大物体运动**数据，并未直接记录 humanoid actuator action、足底力或真机闭环结果。它比纯 AMASS 更接近全身移动操作，但仍需要有动力学约束的 retarget 和目标机器人环境评估。

## 5. 代表工作怎样训练、怎样测试

原始 **OMOMO** 先训练 object motion → 双手位置的 diffusion stage，再以预测双手和 object motion 为条件训练 full-body motion stage；输入是物体 geometry/状态序列，监督目标是人体全身运动与手—物接触。论文在未见 motion、未见 object、Blender 合成 object trajectory 上测试，量化 Hand JPE、MPJPE、MPVPE、collision percentage、foot-skating（FS）和 contact F1。对 humanoid 的对应做法是：训练/测试沿用 object-disjoint split，把输出 motion retarget 后在 physics 中另测 object tracking/hold、双手接触、跌倒和足滑；原论文的生成指标不是 robot task success。
