---
title: RH20T：人类演示配对的多模态机器人操作数据
category: evaluation
kind: dataset
organization: Shanghai Jiao Tong University
releaseDate: 2023-07-02
summary: 覆盖多种机器人、任务和场景的配对人类演示—机器人接触操作数据，包含视觉、力、音频和动作；适合 one-shot/跨模态操作策略，但不是全身人形移动操作原生数据。
tags: [robot-learning, multimodal, human-demonstration, manipulation, transfer]
draft: false
references:
  - title: RH20T project page
    url: https://rh20t.github.io/
  - title: RH20T API
    url: https://github.com/rh20t/rh20t_api
  - title: Paper
    url: https://arxiv.org/abs/2307.00595
---

## 1. 数据卡与适用边界

[RH20T](https://rh20t.github.io/) 是为 one-shot robot skill learning 构建的配对 `<Human Demonstration, Robot Manipulation>` 数据。项目页将其描述为多机器人、多模态、多任务数据；社区/项目材料报告十余万级机器人 episodes、相应人类 demonstrations、5000 万以上 frames、140+ tasks。官方 API 说明 RGB-D 以 MP4 存储，并提供抽帧/scene loader 工具。[项目页](https://rh20t.github.io/)[API](https://github.com/rh20t/rh20t_api)

| 模态 | 内容 | 在 humanoid 项目中的合理位置 |
|---|---|---|
| 人类演示 | 对应任务的人类 demonstration 视频 | 从人类示范抽取高层任务/视觉先验 |
| 机器人观测 | 多视角 RGB-D、场景/相机数据 | VLA 或 perception-policy 预训练 |
| 接触模态 | 力、音频 | contact-rich manipulation 的辅助监督 |
| 机器人动作 | robot manipulation trajectory/action | policy learning 与 offline evaluation |

它的核心本体是操作机器人，不保证双腿、换支撑或走动。因此只能作为**迁移/预训练数据**；在其上获得的离线成功或 imitation 分数不能作为全身 humanoid 结论。

## 2. 怎样纳入严谨评测

1. 用 RH20T 的 human/robot paired episodes 训练视觉、任务识别或操作 action head；保留官方任务/robot/scene split 或按 episode 严格隔离。
2. 离线评估可报 action prediction、视觉/力/音频消融、one-shot skill success；须在同一 robot/task protocol 中比较。
3. 将模型迁移到 humanoid 时，重新定义 action adapter（手臂、手、base、下身）、场景观测和安全约束；最终用 HumanoidBench 或 Isaac Lab 的移动操作 closed-loop success、跌倒/碰撞等指标再测。
4. 人类 demonstration video 不能直接当 robot action label；需要明确视觉表征、retarget、对齐或 policy conditioning 方法。

## 3. 获取与部署

按[官方 API](https://github.com/rh20t/rh20t_api)下载和解码数据；其 README 明确说明 RGB-D 的 MP4→原始图像转换工具。存储、视频解码和多视角时间同步是工程成本；把 camera intrinsics/extrinsics、frame sampling、force/audio sampling rate 记录在 preprocessing manifest。使用前核验数据下载协议与各子集许可。

## 4. 限制

RH20T 的优势是现实机器人多模态接触数据；不足是机器人形态和任务主要不覆盖全身双足移动操作。适合作为“数据金字塔”的迁移层，而不应替代目标 humanoid 仿真评测。

## 5. 代表工作怎样训练、怎样测试

RH20T 原论文的 one-shot 学习设置把 paired human demonstration 与机器人 RGB-D、force、audio、action 序列用于训练多模态 skill representation / policy；测试时给一段新任务的人类演示和当前 robot 感知，输出目标机器人操作轨迹。数据收集时包含成功/失败与人工质量等级，论文以真实操作完成/质量来评价多技能 one-shot transfer。具象下游例子 **RoboMM** 使用多机器人演示训练视觉—语言—动作模型：输入多视角 RGB、语言、robot state 与相机标定，预测末端执行器动作/夹爪控制；在 held-out sequence 或真机当前观测下输出下一步 action，以离线动作误差及真实任务 success 测试。[RoboMM](https://arxiv.org/abs/2402.10807) 仍是机械臂操作测试。迁移到 humanoid 时，训练阶段可保留 human-video 与多模态表征，但必须在目标 humanoid 上重新定义 action、task split 和 closed-loop success；不能沿用 arm trajectory 误差宣布全身移动操作成功。
