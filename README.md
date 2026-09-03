# 具身机器人技术地图

一个由四位维护者共同建设的静态知识网站，分为数据集、模型架构、评测和宏观思想四个并列分区。项目使用 Astro 生成纯静态页面，并通过 GitHub Actions 自动校验和部署到 GitHub Pages。

## 分工

- 数据集：`@starrysky77`
- 模型架构：`@xy144001`
- 评测：`@SyouSanGin`
- 宏观思想：`@xiaoyazhai`

数据集版块当前收录 64 个数据集、benchmark、采集系统与数据管线，支持按 Full-body 层级、数据来源和证据等级筛选，并包含采集系统、数据格式与任务覆盖专题。

模型架构版块当前收录 π₀.₅、X‑VLA 0.9B、LingBot‑VLA 2.0 6B、Light‑WAM 和 LingBot‑VA。

## 本地运行

```bash
npm install
npm run dev
```

提交前运行：

```bash
npm run validate-content
npm run build
```

详细协作方式见 [CONTRIBUTING.md](CONTRIBUTING.md)。
