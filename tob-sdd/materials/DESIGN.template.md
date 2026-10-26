# DESIGN.md — <项目名> 前端设计规范（ToB 后台 · 多方案候选 · Owner 审批制）

**状态**: Owner 拍板生效后，本文件是 UI 唯一真相源——产出与本文冲突时改代码，不反向放宽本文（AGENTS UI-GATE）。
**方案审批制**: 前端技术与 UI 以**多套候选方案**呈报 Owner 审批、选定一套后生效——候选清单与拍板规则见 §0；§1–§12 为**已选方案的正文**（模板默认＝方案A），方案B 的正文要点见附录 B。
**上游原样定调（Owner 2026-10-23 拍板，A/B 同律）**: 两套方案都**不手抄 UI 参数表**——上游仓库代码内的前端技术架构与 UI 设计是什么样子，就原样使用什么；本文件只做「指向真相源」＋「裁剪/例外登记」，不做数值复刻（防手抄漂移成第二真相源）。方案A 指针见 §1–§9；方案B 指针与扩展白名单见附录 B。**唯一允许的项目级自定义＝主题层**；其余改动一律走官方支持的插件/扩展点，禁 fork 魔改上游源码。

---

## 0. 方案审批（plan 首轮呈报，Owner 选定一套）

### 0.1 候选清单

| 维度 | 方案A：shadcn-admin（satnaing/shadcn-admin，上游原样） | 方案B（推荐）：Ant Design Pro v6（ant-design/ant-design-pro） |
|---|---|---|
| 组件来源 | shadcn/ui 源码复制进仓（自有可控）＋ shadcn-admin 后台模板 | `antd` 6 库依赖 ＋ ProComponents ＋ Pro 官方脚手架（v6） |
| 底座 | Radix primitives ＋ Tailwind v4 | React 19 / Umi Max 4 / antd 6 / utoopack（构建可选 utoo 或 Umi 常规） |
| 无障碍 | Radix 级 | antd 内建 a11y（官方维护，中文语境成熟） |
| 后台布局壳 | 现成即用（inset 侧栏/顶栏/⌘K/登录页两形态/暗黑模式，上游自带） | 上游自带全套后台页结构（Dashboard/Form/List/Profile/Result/Exception/Account/登录注册，实演 preview.pro.ant.design）；**结构细节以上游当期代码为准，本表不复刻** |
| 定制方式 | **上游代码＝视觉真相源**；换皮唯一入口＝`src/styles/theme.css` token 值；不改 `components/ui` 源码 | **同左：架构与 UI 代码设计认上游仓库本身**；允许的改动只有两类——①**主题自定义**（本包 `materials/antd-themes/` 13 主题资源＋自建切换器＋`cssVar`，默认＝shadcn，用户可切换）②**官方支持的插件/扩展点形态**（ConfigProvider token 体系、组件 `classNames/styles` 语义钩子、ProComponents schema 扩展、Umi Max 官方插件）；**禁 fork 魔改 antd/Pro 内部源码**——逐项见附录 B |
| CN 网络 | 上游 `index.html` 外联 Google Fonts（Inter/Manrope），内网不可达——按 §3 系统栈替代（唯一允许的视觉偏离，retrofit 配方有做法） | antd 生态国内原生友好：npmmirror/淘宝源齐、文档国内可达、团队中文经验多 |
| 团队实跑经验 | 两个内部 ToB 项目实跑；**注意：旧实跑是黑白灰重皮版——工程结论（§12、retrofit 配方的 pnpm/路由/构建/托管坑）仍适用，视觉结论（slate→stone、无边框大圆角、行高 ≥52px 等复刻条款）随 2026-10-23「原样」指令作废** | 本包无实跑经验，接入首季按 spike 对待；但 antd 为国内 ToB 后台事实标准，招人/协作成本最低 |
| AI 工具链 | — | **上游仓库自带 agent 资产**：根 `AGENTS.md`＋`.agents/skills`（symlink→`.claude/skills`：`antd`、`pro-upgrade` 两技能；antd 技能含 `@ant-design/cli` 七工具 list/info/doc/demo/token/semantic/changelog ＋ MCP server 模式）；官方另有 llms.txt、design.md（google-labs 格式）、MCP——AI 编码前 MUST 读上游 skills（B.3 第 6 条） |
| 版本成熟度 | shadcn-admin 稳定（接入时钉 commit 记 §0.3，见 §1） | ant-design-pro v6，MIT；接入时同样钉上游 commit 记 §0.3；v5→v6 迁移由仓库自带 `pro-upgrade` 技能承接 |
| 授权成本 | MIT 免费 | MIT 免费（模板/脚手架全开源，无付费墙） |
| 主要风险 | 组件副本的维护成本；上游 slate 冷灰＋高饱和 chart 色板＋社交登录残留＝接受上游默认（裁剪清单见 §9） | 扩展面受官方机制约束（B.2 白名单两类之外的改动一律判例拍板，禁私改上游；复杂定制先核实扩展点可达）＋ 主题资源依赖适配一次性成本 ＋ 经验空白 |

推荐＝**方案B**：后台壳最全且全免费（无授权门槛）、内置 13 主题资源（shadcn＝默认，用户可切换）、AI 编码资产官方内建（agent skills＋CLI＋MCP 让"禁凭记忆写码"有工具可执行）、国内 ToB 语境协作与招人成本最低。**方案A 保留为轻量退路**（不想引 Umi 全家桶时用；视觉＝上游原样）。两者 UI-GATE 纪律相同。

### 0.2 拍板与落位规则

1. **时机**：plan 首轮技术栈批量问的 UI-GATE 检查环节呈报本表；Owner 未拍板前 §1–§12 保持方案A 默认、**UI-GATE 不解除、前端实现禁止开工**。
2. **落点**：拍板结果写 §0.3；方案选择＝HOW 层——进 DESIGN.md 与 plan Technical Context，MUST NOT 进 spec（AGENTS 落位判据）。
3. **选A**＝正文不动（上游即真相源），§0.3 记裁决＋钉版 SHA；**选B**＝正文 §1–§9 的真相源指针整体换成 ant-design-pro 上游（形态见附录 B.1），主题层按 B.2 落地，重跑 G2'（checklist）后再开工。
4. **中途换方案**＝判例登记（取下一个全局未用号）＋正文整体重写＋G2' 重跑，spec 零改动；禁止口头切换。
5. **新增候选**＝向本包模板追加附录并走一次包评审，不在项目内私加。

### 0.3 拍板记录

| 项 | 值 |
|---|---|
| 已选方案 | 待拍板（推荐候选 B；正文默认＝A＝上游原样） |
| 拍板日期 / Owner | `<待填>` |
| 上游版本锚点（选 A 时） | `<待填：commit SHA / clone 日期>` |
| 换皮依据（参考图/品牌色，可选） | `<待填，默认＝上游原样不换皮>` |

---

## 1. 设计定性（方案A ＝ satnaing/shadcn-admin 上游原样）

**真相源**：上游仓库代码本身。落库＝`git clone --depth 1`，并把 **commit SHA 记入 §0.3 与 plan**——此后该项目视觉＝该快照；上游演进不追改本文件。

关键源文件指针（只引路径不复刻值；值以仓内当期文件为准，路径与形态 2026-10 已实拉核实）：

| 设计项 | 上游真相源 |
|---|---|
| 色彩/圆角 token | `src/styles/theme.css`——`:root`＋`.dark` 双套（slate 系 oklch、`--primary` 近黑、`--destructive` 饱和红、`--chart-1..5` 高饱和色板、`--sidebar*` 八件套、`--radius: 0.625rem`） |
| 全局样式/字体注册/圆角派生 | `src/styles/index.css`——`@theme inline` 注册 `--font-inter/--font-manrope`＋`--radius-sm/md/lg/xl`（由 `--radius` ±px 派生）；`no-scrollbar`/`faded-bottom` 工具类；button `cursor:pointer` 修复上游已自带 |
| 组件 | `src/components/ui/*`（new-york 风格源码在仓，直接改即用）——Card 带 border＋`rounded-xl`＋`shadow-sm`；Button `rounded-md`、default `h-9`/sm `h-8`/lg `h-10`/icon `size-9`；Badge `rounded-md text-xs`、variant＝default/secondary/destructive/outline |
| 布局壳 | `components/layout/*`＋`ui/sidebar.tsx`——SidebarProvider 默认 `variant=inset`＋`collapsible=icon`、侧栏 `--sidebar-width: 16rem`；Header `h-16`＋内层 `p-4`（fixed 时 backdrop-blur）；Main `px-4 py-6`、非 fluid 时容器查询 `max-w-7xl` 居中 |
| 命令面板 | `components/command-menu.tsx`（CommandDialog；数据源复用 `layout/data/sidebar-data.ts` navGroups，改菜单即同步） |
| 登录页 | `features/auth/sign-in/index.tsx`（单列小卡）与 `sign-in-2.tsx`（左 `bg-muted` 展示图＋右表单）两形态上游自带 |
| 暗黑模式 | `context/theme-provider.tsx`——`defaultTheme='system'`，light/dark/system 三态跟随 OS，顶栏 ModeToggle 入口自带。**上游原样＝暗色可用；旧「dark 保留备用不承诺」条款作废** |

**保留纪律（不因「原样」放松）**：所有页面 MUST 经 `@/components/ui` 组件与 CSS 变量 token 呈现，MUST NOT 新增上游 token 体系外的硬编码色值。

**换皮唯一入口**：§0.3「换皮依据」有值时只改 `theme.css` 的 `:root/.dark` 变量值（衍生需要时同步 `@theme inline`），组件源码不动——组件全走变量，改值即全局生效。

## 2. 色彩

真相源＝`theme.css`（§1 指针表）。上游默认＝slate 冷灰中性系、主按钮近黑、chart 五色板高饱和。**本文件不复刻色值**；Owner 选 A 即接受该默认，旧黑白灰 stone 复刻表作废。确需语义色扩展（如状态绿/琥珀）＝在 `theme.css` 加变量＋登记 §0.3，禁页面私加、禁 inline style。

## 3. 字体

上游真相源＝`index.css` `@theme inline`（Inter 正文／Manrope 标题，`index.html` 外联 Google Fonts）＋各组件类名字重层级。**唯一允许的视觉偏离＝内网字体替代**：删 `index.html` 的 preconnect/fonts `<link>`（及 og/twitter 外链图），`--font-inter/--font-manrope` 改指系统字体栈（`-apple-system…PingFang SC/Microsoft YaHei`）——只换字体名注册，不改层级结构。做法见本包 `spec-kit-sdd/references/shadcn-admin-tob-retrofit.md` §5。root 16px 不缩字（即 Tailwind 默认）。

## 4. 圆角/阴影/边框

真相源＝`theme.css --radius` 派生链＋各 `ui/*.tsx` 类名。上游默认：Card `rounded-xl border shadow-sm`（有边框）、Button/Badge `rounded-md`。旧「无边框大圆角 Soft-UI 三要素」复刻表随「原样」指令作废，不再逐组件覆写。

## 5. 布局

上游默认即用（§1 指针表：inset 侧栏、Header h-16、Main px-4 py-6＋max-w-7xl）。**保留的行为纪律（跨方案铁律，不依赖具体皮）**：每屏主操作 ≤3、一屏一个主决策点、低频/高危动作收 `⋯` 下拉——在业务页遵守，不改上游壳。

## 6. 图标

上游自带 lucide-react 即用；键帽＝上游 `Kbd` 组件。旧「头像二字徽标/箭头字符」自定义条款作废。

## 7. 动效（克制）

上游 `tw-animate-css`＋Collapsible slide（300ms）即用。**禁止追加**：弹跳、闪烁、庆祝动画（红线：不庆祝失败、不施压）。加载＝Skeleton 或「加载中…」灰字；提交按钮 pending 文案变化＋disabled。

## 8. 密度

上游默认即密度（Button h-9、Main py-6 等）。跨方案铁律保留：root 16px 不缩字号、紧凑＝布局密度不靠缩字、单屏信息不过载、ToB 零黑话全中文。旧「表格行高 ≥52px／`--spacing:0.22rem` 全局收紧」降为**项目级可选项**（做法在 retrofit 配方 §5），需 §0.3 登记后才启用，不是方案A 默认。

## 9. 落地动作（代码层，方案A）

| 动作 | 位置 | 性质 |
|---|---|---|
| 钉版落库 | `git clone --depth 1`＋SHA 记 §0.3/plan | 前置 |
| 删 demo/clerk | `routes/clerk`、`_authenticated/{chats,apps,tasks,users,help-center}`、对应 `features/*`、`@clerk/react`＋`clerk-logo`（清单与 grep 清零断言＝retrofit 配方 §1） | 裁剪，非改 UI |
| 删社交登录按钮/外链 | `features/auth/sign-in/components/user-auth-form.tsx`（Facebook/GitHub 品牌色按钮）、Sign Up/terms 外链文案（内网无外部协议页） | 裁剪＋红线清理 |
| 业务菜单 | `components/layout/data/sidebar-data.ts`（navGroups 业务化＋中文标题；teams 留一个）——命令面板同源自动跟变 | 扩展 |
| 首页指向 | 删 demo dashboard，redirect 到业务首屏 | 扩展 |
| 字体内网替代 | §3 | 唯一视觉例外 |
| 换皮（可选） | `theme.css` `:root/.dark` 值 | §1 唯一入口 |

> Tailwind v4 自定义 token 须 `@theme inline` 注册才生成 utility；改 `theme.css` 后 build 完 grep dist CSS 验证值真实产出——类名静默无效是已踩坑（retrofit 配方）。

## 10. 移动端适配

上游自带响应式即用：窄屏侧栏自动转 Sheet、sign-in-2 左栏 `max-lg:hidden`、移动端输入控件 `font-size:16px` 防聚焦缩放（index.css 自带）。**项目侧补充纪律（跨方案铁律）**：窄屏表格转竖排卡片（次要字段可省不改语义）；可点目标 ≥40px（上游 `size=sm` 仅桌面用）；弹层窄屏 `max-w-[calc(100vw-2rem)]`；375×667 与 768px 两档走查：无横向滚动条、表格页出卡片形态。

## 11. 交互行为规则（页面级交互的落点——弹层/抽屉/确认在这章，不在 spec）

> 本章是「点击创建按钮需要给出弹层」这类规则的**正式归属地**（与 `preview/` 原型配合：形态规则写这里，具体页面长什么样由原型呈现）。新增交互规则持续追加，编号递增。跨方案保留，不随上游/原样调整。

### 11.1 弹层选型

| 场景 | 形态 | 电子商城示例 |
|---|---|---|
| 单实体创建/编辑（字段 ≤8） | 居中 Dialog | 点「创建商品」→ 弹层填名称/类目/价格/库存 |
| 字段多或含表格/详情（>8 字段、多区块） | 右侧抽屉（Sheet）或全屏弹层 | 商品详情弹层含 SKU 表 |
| 高危确认（删除/作废/不可逆） | AlertDialog 阻断式，确认按钮 = destructive 色 | 「下架该商品？已售 X 件不可自动恢复」 |
| 纯信息展示 | toast/行内展开，不占模态 | 保存成功提示 |

判据：**换端后这条还成立吗？** 「操作人 MUST 二次确认才提交」是需求（进 spec 的 FR）；「用 Dialog 还是 Sheet 承载确认」是实现形态（进本章）。弹层改抽屉属 UI 微调；**去掉弹层=去掉确认义务，属需求变化，须先改 spec**。

### 11.2 创建/编辑弹层通用规则

- 触发：页头主操作区按钮（≤3 个主操作，见 §5）或表格行操作列；按钮文案＝动词＋对象（「创建商品」不写「新增」）。
- 内容：字段自上而下按填写频率排；枚举/选项类输入 MUST 用下拉 Select，MUST NOT 让用户手输，禁裸 `<select>`；关键词输入框排搜索区最前，筛选下拉依次在后。
- 提交：底部 Footer 操作区；pending 态按钮文案变化（「保存中…」）＋ disabled，禁双提交。
- 关闭：右上角 X 与底部「取消」并存；**表单已填内容非空时关闭 MUST 给丢弃确认**（数据丢失红线）。
- 校验：字段级错误就地显示（就地红字/Alert），不做整屏弹窗报错。

### 11.3 列表↔详情

- 详情入口双通道：主键列做成链接式按钮＋操作列「详情」按钮。
- 列表主列 ≤6（宪法 II），次要信息收「详情」弹层；桌面表格与窄屏卡片**同口径收敛**。
- 未处理/待办行在详情弹层内可直接转入处理动作（少一次跳转）。

### 11.4 加载/进度/反馈（配合宪法 II 高强度关怀）

- 批量/长等待操作 MUST 显示：明确进度、预计耗时、正在发生什么、下一步建议；完成后给平实结果确认（禁庆祝动画）。
- 提交等待 ≥300ms 给 pending 视觉；数据加载给 Skeleton，禁空白页转圈。
- 空状态给一次性、可静音的引导（不拦截）；错误态＝原因 + 可行动作，不甩堆栈。

## 12. UI 组件使用约束（强制，每次写 UI 前必读；来自实际踩坑，持续追加）

> 本章全部＝行为/约束类经验，不依赖黑白灰皮，「原样」指令后仍有效；仅 12.7 涉 variant 需按上游基线理解。

### 12.1 Dialog 弹层内容宽度
- DialogContent 内所有 Card MUST 加 `className="w-full"`；所有 Table MUST 外包 `div className="overflow-x-auto"`。
- 宽度用 `max-w-*` 控上限，内容 `w-full` 填满不溢出；多卡片用 `flex flex-col gap-4`。

### 12.2 表格列宽与溢出
- 表格列数 ≤8（超出拆分或展开行）；长文本列（编号/SKU）`font-mono text-xs` + `truncate` 或允许换行；操作列固定 `w-28`/`w-32`；状态列用 Badge 不用纯文字。

### 12.3 响应式断点
- 桌面表格 `hidden md:block`；移动端卡片 `md:hidden`；弹层窄屏 `max-w-[calc(100vw-2rem)]`；按钮窄屏 `h-10`、桌面用上游默认 `h-9`。

### 12.4 卡片嵌套
- 禁止卡片内再嵌套卡片（用 Separator 分隔区块）；区块标题用 `<p className="mb-3 text-xs font-medium text-muted-foreground">`，不用 CardTitle；弹层内卡片同页面级但 MUST 加 `w-full`。

### 12.5 弹层 Footer 按钮
- `<div className="flex justify-end gap-2 pt-1">`；取消 `variant="outline" size="sm"`；确认 `size="sm"`＋pending「保存中…」+ disabled；关闭统一右下角（DialogContent 自带右上 X）。

### 12.6 空/加载/错误态
- 空数据：`StateHint` 或 `rounded-lg border border-dashed py-8 text-center` 占位；加载：Skeleton；错误：Alert destructive。状态四态（Loading/Progress/Success/Error）与 Empty 为每页必备。

### 12.7 颜色与语义
- 上游 Badge 仅 default/secondary/destructive/outline 四变体。**成功/警告语义 variant＝项目扩展项**：需要时按 `badgeVariants` 模式在 `ui/badge.tsx` 追加（颜色值走 `theme.css` 新变量＋登记 §0.3），禁页面内拼 inline style。失败/离线用 `destructive`；中性用 `secondary`/`outline`＋`text-muted-foreground`。**禁止纯文字表状态**，MUST 用 Badge 或色点。

### 12.8 代码/编号字体
- 编号类（SKU/单据号/商品编号）`font-mono text-xs` 或 `text-[13px]`；时间戳 `tabular-nums`；普通文字默认 sans-serif。

---

**检查清单**（每次写 UI 后自检，方案A）：
- [ ] 改动是否只落在 `theme.css`（换皮）与 §9 裁剪/扩展清单内？
- [ ] §0.3 已记钉版 SHA？有无新增上游 token 体系外的硬编码色值？
- [ ] Dialog 内 Card 都有 `w-full`？Table 包了 overflow-x-auto？
- [ ] 表格列数 ≤8？长文本有 truncate？状态用 Badge 不是纯文字？
- [ ] 移动端有卡片形态（`md:hidden`）？
- [ ] 弹层 Footer 按钮位置正确？pending 有 disabled？表单非空关闭有丢弃确认？
- [ ] 空/加载/错误态有处理？无庆祝动画？
- [ ] demo 路由/clerk/社交按钮已 grep 清零（断言见 §9）？

---

## 附录 B. 方案B（Ant Design Pro v6）——上游原样制：指针、主题扩展与插件白名单

**定调（与方案A 同律）**: 前端技术架构与 UI 代码设计**全部认上游仓库 `ant-design/ant-design-pro` 本身**——本附录不手抄参数，只做真相源指针＋主题自定义层＋官方插件扩展白名单。选定 B 后正文 §1–§9 按本附录指针表改写为 B 的真相源指向；§10–§12 跨方案铁律原样保留。

**真相源与钉版**：落库＝`git clone --depth 1`＋**commit SHA 记 §0.3 与 plan**（模板期快照＝v6.0.3，2026-10 实测 master）；此后该项目架构/视觉＝该快照，上游演进不追改本文件。

### B.1 真相源指针表（只引路径，值以仓内当期文件为准）

| 设计项 | 上游真相源 |
|---|---|
| 技术栈与构建 | `package.json`（React 19、`antd ^6.6.7`、`@ant-design/pro-components ^3.1.14-2`、`@umijs/max ^4.7.27`、`antd-style`）＋ `config/config.ts`（Umi Max 配置；`max dev`/`max build` 即上游脚本，**Umi Max＝上游锁定框架，选型即接受它，不存在"纯 Vite＋antd"形态**——要换那是判例级改案） |
| 路由与页面 | `config/routes.ts`＋`src/pages/*`（dashboard〔analysis/monitor/workplace〕/ form〔basic/step/advanced〕/ list〔table-list 等〕/ profile / result / exception / account / chatbot / user〔登录注册〕——全部上游自带，实演 preview.pro.ant.design） |
| 布局壳 | `src/app.tsx`（`layout` 运行时配置＝ProLayout 入口：侧栏/顶栏/水印/多 tab）＋ ProLayout/ProTable/ProForm（`@ant-design/pro-components`） |
| 组件与视觉 | `antd` 6 当期 API（主题三层 Seed→Map→Alias token、`theme.algorithm` default/dark/compact、组件 `classNames/styles` 语义钩子）——**写码前用 `@ant-design/cli` 查当期 props/token，禁凭记忆** |
| 内置能力 | Umi Max 官方插件即上游已启用的形态：`locale`（i18n）、`request`、`mock`、`access`、`@umijs/max-plugin-openapi`（devDep 实配）——启用同类能力＝在 `config.ts` 的 plugins 里加官方插件 |

### B.2 自定义边界（白名单＝两类，其余全禁）

**① 主题层＝唯一允许的项目级自定义（选型硬要求，MUST）**：用户可自定义切换主题——
- 主题资源＝本包 vendored `materials/antd-themes/`（13 主题文件：shadcn【**默认，MUST**】/mui/bootstrap/cartoon/illustration/glass/geek/lobe/lark/blossom/v4/serene ＋ hero 亮/暗双 `ThemeConfig`；源自 ant.design 官方主题预览区照抄，纯资源无注册表）；antd 原生 light/dark 用 `defaultAlgorithm`/`darkAlgorithm` 派生。
- 接入：拷所需文件入项目（建议 `src/themes/antd/`），**项目自建主题列表＋切换器**，默认页＝shadcn，`cssVar: true`（运行时 CSS 变量，切换不重编译、杜绝半屏残影），选择持久 localStorage（初始值可跟随 `prefers-color-scheme`，默认仍 shadcn）。
- 依赖适配：7 个 hook 主题依赖 `antd-style`＋`clsx`（mui 另 `@rc-component/util`）——上游 package.json 本就含 `antd-style`，`clsx` 若缺则补依赖；主题名/图标/背景图切换器侧自备。
- 红线：组件内 MUST NOT 硬编码色值，一切颜色走 token/主题变量；`theme=undefined↔object` 切换引发重挂载（官方 FAQ），初始即给 `{}`。
- 与方案A 的关系：本包 shadcn 主题文件（`#262626` 族）与 shadcn-admin 上游（slate 冷灰）**同族不同源**——选 A 认 A 的上游、选 B 认 `shadcnTheme.ts`，互不对齐，各守各的单一真相源。

**② 官方支持的插件/扩展点＝其余一切改动的唯一通道**：Umi Max 插件体系（`config.ts` plugins，对齐上游已用形态）；ConfigProvider `theme` token 定制；组件 `classNames`/`styles` 语义结构；ProComponents schema/props 扩展；locale/request/mock/access 官方内置件开关。

**禁**：fork/patch-package 魔改 `antd` 或 `pro-components` 内部源码；绕过 token 体系的全局 CSS 覆写；抄上游 `src/pages` demo 页进业务后养分叉（业务页自建，引用上游组件）。扩展点不够用时＝停下交 Owner 判例拍板，不私改上游。

### B.3 选型必配纪律

1. **§0.3 记拍板＋钉 SHA 后先 spike**：走通「clone 上游起站（`npm install` 走 npmmirror）→ 不删默认页直接浏览确认上游形态 → 拷主题文件定依赖取舍 → 自建主题列表默认页＝shadcn 生效 → 切换器动态换肤无残影 → `max build` 生产构建」六步再全量接入；spike 不达标＝回到 §0 重拍，不得带病推广。
2. **升级锁版**：`antd`/`@ant-design/pro-components`/`@umijs/max` 按上游 package.json 钉住，升版走判例登记＋跑上游 `pro-upgrade` 技能对照清单；`antd-themes/` 若跟进 ant.design 上游改版，同样判例登记（记录来源日期/commit）。
3. **动态主题验收进 G2'**：冒烟断言三条——①默认主题＝shadcn（首屏 `colorPrimary` 为灰黑系 `#262626` 族、非 antd 蓝 `#1677FF`）；②运行时切换后全页无硬编码色残留（getComputedStyle 抽查 token 变量生效、无半屏残影）；③切换不触发整树重挂载（theme 初始 `{}`）。
4. **白名单审计进 G2'**：diff 审查断言——`node_modules` 外零 `antd`/`pro-components` 源码级 patch；全局 CSS 覆写 antd 类名＝0；新依赖须属主题适配或官方插件。
5. **跨方案铁律不换血**：§8 密度（root 16px、不缩字号、紧凑靠布局）经 `controlHeight`/`size` 组件 token 实现；antd 默认蓝 MUST 被默认 shadcn 主题覆盖——未覆盖＝G2' 不过。用户切换其他主题（mui/glass/geek 等）允许各自强调色，但 ToB 生产默认展示＝shadcn，切换器入口不抢主操作位（§5 主操作 ≤3）。
6. **AI 会话开场规**：前端实现会话 FIRST READ＝上游仓库 `AGENTS.md`＋`.agents/skills`（`antd`：经 `@ant-design/cli` 七命令 `list/info/doc/demo/token/semantic/changelog`，`--format json --lang zh`，可作 MCP server；`pro-upgrade`：升级承接）＋官方 llms.txt/`ant.design/design.md`＋本 DESIGN.md §0.3 拍板记录；读齐前不落任何 antd/Pro 代码（UI-GATE 在方案B 的具体化）。
