# 数据集网页更新阶段日志（2026-09-13）

## 阶段一：来源与项目核对
- 已确认用户提供的 `open-source-models-standalone.html` 与项目 `public/datasets/open-source-models-standalone.html` SHA-256 完全一致，无需重复复制。
- 项目数据集区已有本轮调研产物：主目录、Open X-Embodiment 展开表、采集系统、数据格式、Full-body 专题及入口页面改动，均位于 `public/datasets/` 与 `src/content/datasets/`。

## 阶段二：验证
- `npm run validate-content` 通过：Validated 10 content file(s)。
- `npm run build` 未通过，原因是现有 `node_modules` 中 `aria-query`/`axobject-query` 缺少映射文件且存在目录访问限制，属于依赖/环境问题，不是内容校验错误。

## 当前结论与下一步
- 数据集调研汇总已经按项目现有静态网页规则接入；需在具备完整依赖的环境重新安装依赖后复跑构建。

## 阶段三：线上路由修复
- 线上 `/datasets/` 实际命中 Astro 动态分类路由，而非 `public/datasets/index.html`，因此显示空占位页。
- 已修改 `src/pages/[category]/index.astro`：datasets 分类自动跳转到完整静态数据集页 `/datasets/index.html`，其他分类保持原行为。
- 进一步将主页 `src/pages/index.astro` 的数据集入口改为直接链接 `/datasets/index.html`，避免 Astro 分类路由与 `public/datasets/index.html` 冲突；模型架构等入口未改动。
