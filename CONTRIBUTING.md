# 协作规范

四位维护者按目录负责内容，公共组件由全体共同维护。

| 分区 | 目录 | 负责人 |
|---|---|---|
| 数据集 | `src/content/datasets/` | `@starrysky77` |
| 模型架构 | `src/content/model-architecture/`、`public/model-architecture/` | `@xy144001` |
| 评测 | `src/content/evaluation/` | `@SyouSanGin` |
| 宏观思想 | `src/content/macro-thinking/` | `@xiaoyazhai` |

## 工作流

1. 从最新 `main` 创建短期分支，例如 `content/models-add-openvla`。
2. 只在自己的内容目录添加 Markdown/MDX；不要复制公共页面组件。
3. 本地运行 `npm run check`、`npm run validate-content` 和 `npm run build`。
4. 提交 Pull Request，等待自动检查通过；各版块负责人可以自行合并自己负责目录的内容。
5. 建议使用 Squash Merge；合并后删除功能分支。

修改公共组件、Schema、依赖或部署工作流时，应在 PR 中明确说明对四个分区的影响，并建议由另一位维护者复核。
