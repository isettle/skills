# antd-themes — Ant Design Pro 方案（B）主题资源集

用途：`DESIGN.md` 附录 B 方案B（ant-design/ant-design-pro v6）的**主题资源**。
本目录**只提供主题定义文件，不含注册表/切换器**（原 `index.ts` 注册表已按 Owner 2026-10-23 指令删除）——由项目自行组织主题列表并挂到 `<ConfigProvider>`。
**默认主题＝shadcn（MUST，属 DESIGN 层纪律：项目的主题列表把 shadcn 设为首页）**，其余供用户运行时切换。

## 文件清单（13 个主题资源文件）

| 形态 | 文件 | 导出 | 用法 |
|---|---|---|---|
| hook 返回 `ConfigProviderProps`（12 个） | **shadcnTheme**（默认）、mui、bootstrap、cartoon、illustration、glass、geek、lobe、lark、blossom、v4、serene | `use*Theme()` → `{ theme, wave, app, ... }` | 组件内调 hook：`<ConfigProvider {...props}>` |
| 裸 `ThemeConfig` 成对（1 个） | heroTheme | `heroLightTheme` / `heroDarkTheme` / `heroThemes` | `<ConfigProvider theme={heroLightTheme}>` |

> antd 原生 light/dark 基础外观不占文件＝`theme.defaultAlgorithm` / `theme.darkAlgorithm` 直接派生（原 index.ts 即如此组装）；主题名/图标/背景图/切换器 UI 由项目自备。
> 确切导出名与 props 形状，接入前 MUST 读文件或用 `@ant-design/cli` 核对，禁凭本表记忆写码。

## 依赖（已核实：无官网内部路径耦合）

- 通用：`antd`、`react`；其中 7 个 hook 主题（shadcn/mui/bootstrap/cartoon/illustration/glass/geek）另依赖 `antd-style`＋`clsx`（createStyles 做组件级样式覆写），muiTheme 还用 `@rc-component/util`。
- `?raw` 导入、`useLocale`、`svg-component`（SereneIcon）等 ant.design 官网内部耦合全部随原 `index.ts` 移除，主题文件自身零此类引用。

## 来源与维护约定

- 取自 ant.design 官网主题预览区同一套主题代码（Owner 于 2026-10-23 提供），13 个主题文件**原样照抄未改内容**。
- 消费方式：选 B 的新项目把所需文件拷入（建议 `src/themes/antd/`），自建主题注册表＋切换器，默认页＝shadcn，并开 `cssVar: true`（见 DESIGN 模板 B.1「动态主题」）。
- 上游改版＝重新照抄并走判例登记（记录来源日期/commit）；本地魔改请改名另立，不覆盖同名文件。
- 动态切换与验收断言（默认 shadcn 生效、切换无残影、不触发重挂载）见 `DESIGN.template.md` 附录 B.1「动态主题」与 B.2 第 3 条。
