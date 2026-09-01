# 协作规范

三位维护者按目录负责内容，公共组件由全体共同维护。

| 分区 | 目录 | 负责人 |
|---|---|---|
| 灵巧手 | `src/content/dexterous-hand/` | `@starrysky77` |
| 双臂 | `src/content/dual-arm/` | `@xy144001` |
| 全身 | `src/content/humanoid/` | `@SyouSanGin` |

## 工作流

1. 从最新 `main` 创建短期分支，例如 `content/dual-arm-add-aloha`。
2. 只在自己的内容目录添加 Markdown/MDX；不要复制公共页面组件。
3. 本地运行 `npm run check`、`npm run validate-content` 和 `npm run build`。
4. 提交 Pull Request，等待自动检查和至少一位同伴审查。
5. 使用 Squash Merge；合并后删除功能分支。

修改公共组件、Schema、依赖或部署工作流时，应在 PR 中明确说明对三个分区的影响。
