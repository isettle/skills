# 参考截图 → DESIGN.md → 落地改版

用户给几张应用截图（登录页/后台/命令面板）要求「以 shadcn-admin 为基底做成这个风格」时的完整流程。

## 1. 截图抽设计规格（vision_analyze）

- 每张图用同一提示模板，要可复现参数不要观感：「详细描述这个界面的设计：布局结构（侧边栏/顶栏/内容区的具体组成）、配色（主色/背景/文字色的具体观感）、字体大小层级、组件样式（卡片/表格/按钮/输入框的圆角、边框、阴影）、间距密度、图标风格。尽量具体，我要复现这个设计。」
- 演示类截图先区分**界面本体 vs 后期叠加层**（播放按钮/字幕/章节角标/设备外框/录屏标注）——叠加层写进 DESIGN.md 的「不实现」清单，防止把视频装饰当 UI 复现。
- 用户的配色指令（如「黑白为主」）**覆盖参考图品牌色**：抽结构与质感（圆角/阴影/层次/密度），色系整体替换；语义色（成功/失败/警告）保留但降饱和。

## 2. 立 DESIGN.md（九节结构）

设计定性 → 色彩 token 表（变量+色值+用途）→ 字体层级表 → 圆角/阴影/边框参数表 → 布局（侧栏/顶栏/命令面板/表格卡/登录页各一小节，含具体尺寸）→ 图标 → 动效（克制，含禁止项：弹跳/闪烁/庆祝）→ 与既有纪律的取舍（显式写明取代哪条旧规则、Owner 何时拍板）→ 落地映射表（设计项→代码文件）。

- 仓库此前若有「DESIGN.md 跳过/豁免」记录，新文档头部加状态行：生效日期＋拍板人＋取代关系——不留两份冲突标准。
- DESIGN.md 入库（specs/<feature>/DESIGN.md），成为验收对照物：页面与 DESIGN.md 不一致时改页面。

## 3. 落地顺序（每层 build 过再下一层）

1. **token 层**：index.css `:root`＋`@theme inline`（色板/阴影档位 shadow-card·float·lift/radius 基准/dark 段）。全局风格覆写用属性选择器，不改组件源码：激活菜单白卡浮起＝`[data-sidebar="menu-button"][data-active="true"]{background:#fff;box-shadow:var(--shadow-lift);font-weight:600}`；命令面板居中偏上＝按 data-slot 选择器改 top/圆角/阴影。
2. **组件层**：直接改 CLI 生成的 ui 组件 className——card 去 border＋rounded-2xl＋shadow-card；button/input 圆角统一 10px（rounded-lg）；badge 补回自定义 success/warning 变体（CLI --overwrite 会冲掉，见 SKILL 坑）。
3. **布局层**：sidebar Logo 区（图标块＋主标＋tracking 副标＋底部版本号）、顶栏（SidebarTrigger＋面包屑＋⌘K 搜索胶囊＋用户头像下拉）、命令面板用 cmdk（CommandDialog 自渲染触发胶囊，触发按钮与面板必须在同一组件内共享 open state）。
4. **页面层**：登录页等结构页重做（分栏品牌墙用内联 style 写网格纹理/径向光晕/毛玻璃——纯 Tailwind 表达不了多层 background-image）；业务页先吃 token 红利，用户看完整体再决定逐页精修。

## 4. 验证

- `npm run build` ✓ ＋ `npm run lint` 0 error。
- **grep dist CSS 验 token 落地**：`--primary:#<值>`、shadow utility 类定义、rounded 类都在编译产物里才算生效——Tailwind v4 自定义 token 没进 `@theme inline` 会静默不生成。
- dev server 硬刷新逐屏对照参考图；色值偏差以 DESIGN.md token 表为准，不以截图取色为准（截图有视频压缩偏色）。
