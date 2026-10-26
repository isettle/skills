# Changelog

本包所有值得注意的变更都记录在此。
格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

发布约定：发版时把 `[Unreleased]` 归入新版本号段落 → 提交 → 打附注 tag（`git tag -a vX.Y.Z -m "..."`）→ `git push origin vX.Y.Z` → 远端 `git ls-remote --tags origin` 验证。

## [Unreleased]

（暂无）

## [0.1] - 2026-10-23

首个发布版（tag `v0.1` @ commit `1d0b89f`）。ToB SDD（spec-kit）开发流程团队共享包定稿。

### Added

- **materials/ 治理物料模板层**（与 agent 无关，任何项目可拷用）：
  - `AGENTS.template.md`：仓库根 AGENTS.md 母版（填 §P 项目参数表）
  - `constitution.template.md`：`.specify/memory/constitution.md` 母版
  - `DESIGN.template.md`：UI-GATE 真相源母版（§0 多方案审批制）
  - `intent.template.md`：流程最前端入口物料（GI 门禁）
  - `spec-kit物料落位与回写规则.md`：内容归属判据＋原型回写三分类
  - `antd-themes/`：方案B 主题资源集（13 个 antd 6 主题文件，源自 ant.design 官方主题预览区照抄，纯资源无注册表，默认选用＝shadcn）
- **skills/ AI 代理技能层**：`spec-kit-sdd`（全流程执行经验）、`sdd-speckit-research`（spec-kit 官方结构事实）、`grill-me`（GI 拷问执行体）、`shadcn-admin-frontend`（前端搭建配方）、`domain-modeling`（vendored，mattpocock/skills，GLOSSARY/ADR 落纸）
- **流程与门禁定稿**：`intent.md(GI) → constitution → specify → preview(G1) → clarify(G0') → plan → checklist(G2') → (analyze) → tasks → implement(G2 六件套 + UI-GATE) → converge(G3)`；**DG diff 审批门禁**——`data-model.md` 与 `contracts/api.md` 首版落笔及后续任何修改均先呈改动表获批才落笔，首轮不豁免（Owner 2026-10-23 拍板收紧）
- **前端方案审批制**（A/B 同律＝上游原样制：架构与 UI 认上游仓库本身，clone 钉 commit SHA，DESIGN 只做真相源指针不手抄参数，禁 fork 魔改上游）：
  - 方案A：`satnaing/shadcn-admin`（轻量退路）；换皮唯一入口＝`theme.css` 变量
  - 方案B（推荐）：`ant-design/ant-design-pro` v6；自定义白名单两类＝①主题层（antd-themes 资源＋自建切换器＋cssVar，默认 shadcn，用户可动态切换）②官方插件/扩展点（Umi Max plugins、ConfigProvider token、classNames/styles、ProComponents schema）
- **跨方案行为铁律**（Owner 2026-10-23 追认定稿，凌驾任一上游默认）：表格主列 ≤6、每屏主操作 ≤4、Loading/Progress/Success/Error 四态＋Empty、表单非空关闭丢弃确认、禁庆祝动画、root 16px 不缩字号、ToB 零黑话全中文
- **字体方案**：离线下载 woff2 入仓自托管（`@font-face`，family 名沿用上游注册值＝观感不降级），取代"降级系统字体栈"；删 Google Fonts 外链
- 入库红线与工具：脱敏扫描 `scripts/sanitize_scan.py`（零命中方可提交）；拷问执行体定稿＝`grill-me`＋`domain-modeling`（上游 grill-with-docs/grilling 组合已移除）

### Removed

- 旧「表格行高 ≥52px／`--spacing:0.22rem`／`line-height:1.45`／`--radius:0.375rem`」全局收紧条款（2026-10-23 拍板删除，密度纯用上游默认）
- Soft-UI 黑白灰手抄参数表（stone 色值/无边框大圆角/激活白卡浮起等复刻条款，随「上游原样制」作废——方案A 认 shadcn-admin 上游，方案B 认 `shadcnTheme.ts`，各守各的单一真相源）

### Known open items（非阻塞，团队试用后定）

- G0'（clarify）与 G2'（checklist）两道加强门禁的去留反馈收集
- 方案B 无实跑经验：接入首季按 spike 对待（DESIGN 附录 B.3）

<!-- 链接区 -->
[0.1]: https://github.com/isettle/skills/releases/tag/v0.1
