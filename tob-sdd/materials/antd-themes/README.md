# antd-themes — Ant Design Pro 方案（B）内置主题包

用途：`DESIGN.md` 附录 B 方案B（ant-design/ant-design-pro v6）的用户可切换主题集。
**默认主题＝shadcn（MUST）**，其余主题供用户运行时自定义切换。

## 文件清单（14）

| 文件 | 说明 |
|---|---|
| `index.ts` | 主题注册表（`usePreviewThemes`）：13 个注册主题 light/dark/**shadcn**/mui/bootstrap/cartoon/illustration/glass/geek/lobe/lark/blossom/v4/serene |
| `shadcnTheme.ts` | **默认主题**：灰黑系 colorPrimary（#262626 族）、borderRadius 8、按钮 #18181b、边框 #e4e4e7（依赖 antd-style＋clsx） |
| `heroTheme.ts` | HeroUI Dashboard 风格（亮/暗双 ThemeConfig）；**未注册进 index**＝可选加挂项，加挂与否 Owner 拍板 |
| 其余 11 个 `*Theme.ts` | 各风格主题（见 index.ts 注册表） |

## 来源与维护约定

- 取自 ant.design 官网主题预览区同一套代码（Owner 于 2026-10-23 提供，原目录 `Downloads/antd-themes/`），**原样照抄未改内容**。
- 消费方式：选 B 的新项目把本目录整体拷入（建议 `src/themes/antd/`），按 `ConfigProviderProps` 展开给 `<ConfigProvider {...props}>`；适配点（import 路径改写、`?raw` 裁剪、antd-style/clsx 依赖取舍）见 `DESIGN.template.md` 附录 B.1「接入形态」。
- 上游改版＝重新照抄并走判例登记（记录来源日期/commit）；本地魔改请改名另立，不覆盖同名文件。
- 动态切换与验收断言（默认 shadcn 生效、切换无残影、不触发重挂载）见 B.1「动态主题」与 B.2 第 3 条。
