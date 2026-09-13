---
title: HumanML3D：语言条件 3D 人体运动数据集
category: evaluation
kind: dataset
organization: Tsinghua University / Simon Fraser University
releaseDate: 2022-06-01
summary: 基于 AMASS 与 HumanAct12 构建的语言—3D 人体动作数据集，含 14,616 段运动和 44,970 条文本描述；适合语言到运动、运动质量与语义一致性的前置评测。
tags: [whole-body-humanoid, language-conditioned-motion, human-motion, amass, evaluation]
draft: false
references:
  - title: Official HumanML3D repository
    url: https://github.com/EricGuoICT/HumanML3D
  - title: HumanML3D paper
    url: https://arxiv.org/abs/2212.00596
---

## 1. 数据卡

[HumanML3D](https://github.com/EricGuoICT/HumanML3D) 将 HumanAct12 和 AMASS 的 3D 人体动作配上自然语言描述。官方仓库报告 14,616 段 motion、44,970 条 descriptions、28.59 小时运动，覆盖日常动作、体育、杂技和舞蹈；并提供 train/val/test 列表、joint positions、rotation-invariant features、文本和归一化统计。[仓库](https://github.com/EricGuoICT/HumanML3D)

| 类型 | 内容 | 机器人用途 |
|---|---|---|
| 运动 | 22-joint 表示/3D joint positions 与特征 | 语言意图→全身参考运动、motion prior |
| 文本 | 一段运动对应一条或多条自然语言描述 | instruction-conditioned motion 和语义匹配 |
| 划分 | 官方 train/val/test ID 文件 | 复用官方 split 评估生成模型 |
| 扩增 | 左右镜像并同步替换方位词 | 必须在报告中说明是否使用，避免与原序列跨 split 泄漏 |

## 2. 当前如何评测，怎样连接全身人形

语言到动作模型通常输入 text，输出固定长度/变长人体运动；常用生成质量、文本—动作检索/匹配、diversity 和 multimodality 指标，依赖指定的 motion/text feature evaluator。复现实验必须复用同一预处理、官方 split 和 feature extractor；不同 feature space 的 FID/R-precision 不可直接比较。

对 humanoid：把输出人体动作 retarget 成 robot reference，再用物理控制器执行。最终应报告两层分数：

1. **HumanML3D 层**：文本语义一致性、动作分布质量、多样性；
2. **机器人层**：指令对应的动作/位移是否完成、跟踪误差、跌倒率、足滑、碰撞和力矩限制。

HumanML3D 大多不含物体、场景、手部精细操作或 contact force；它可支持“走到/转向/摆臂”等语言运动前端，不能单独评估移动中抓取、放置或换支撑操作。

## 3. 获取与部署

按官方仓库的数据构建与许可说明下载；由于上游 AMASS 子集有独立许可，不能假定所有数据无条件再分发。预处理时固定 fps、22-joint convention、文本清洗版本和 mean/std；把测试 ID 文件与训练日志共同保存。

## 4. 代表工作怎样训练、怎样测试

HumanML3D 的 T2M baseline/MDM、MotionDiffuse、T2M-GPT 等工作都按官方 ID split 训练：输入 text embedding，目标为归一化后的 22-joint motion feature sequence；测试时对 `test.txt` 的 caption 采样 motion，再以公开的 text-motion feature extractor 算 FID、R-precision、Diversity 和 Multimodality。它们测的是“生成动作的分布、文本一致性和多样性”。接到 humanoid 时，应把同一生成动作 retarget 后再在仿真测 tracking、足滑、跌倒和指令对应位移；HumanML3D 的高 R-precision 本身不包含对象、手接触或稳定抓取。
