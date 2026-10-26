# DESIGN.md — <项目名> 前端设计规范（ToB 后台 · 多方案候选 · Owner 审批制）

**状态**: Owner 拍板生效后，本文件是 UI 唯一真相源——产出与本文冲突时改代码，不反向放宽本文（AGENTS UI-GATE）。
**方案审批制**: 前端技术与 UI 以**多套候选方案**呈报 Owner 审批、选定一套后生效——候选清单与拍板规则见 §0；§1–§12 为**已选方案的正文**（模板默认＝方案A），方案B 的正文要点见附录 B。
**换皮指引**: 有参考图/品牌色时，§2–§4 的数值全部替换为实际值并重走查；§7/§11 的纪律条款不随换皮变动。

---

## 0. 方案审批（plan 首轮呈报，Owner 选定一套）

### 0.1 候选清单

| 维度 | 方案A：shadcn-admin（satnaing/shadcn-admin） | 方案B（推荐）：Ant Design Pro v6（ant-design/ant-design-pro） |
|---|---|---|
| 组件来源 | shadcn/ui 源码复制进仓（自有可控）＋ shadcn-admin 后台模板 | `antd` 6 库依赖 ＋ ProComponents ＋ Pro 官方脚手架（v6） |
| 底座 | Radix primitives ＋ Tailwind v4 | React 19 / Umi Max 4 / antd 6 / utoopack（构建可选 utoo 或 Umi 常规） |
| 无障碍 | Radix 级 | antd 内建 a11y（官方维护，中文语境成熟） |
| 后台布局壳 | 现成（侧栏/顶栏/⌘K/登录页，§5 直接可用） | 现成且更全：Dashboard（Analysis/Monitor/Workplace）/Form 三式/List 四式/Profile/Result/Exception/Account/登录注册——官方模板块模板（preview.pro.ant.design 实演） |
| 定制方式 | CSS 变量 token ＋ 改 `components/ui` 源码 | ConfigProvider design token ＋ **本包主题资源集（`materials/antd-themes/`，13 主题文件：shadcn【默认】/mui/bootstrap/cartoon/illustration/glass/geek/lobe/lark/blossom/v4/serene/hero，源自 ant.design 官方主题预览区，纯资源无注册表）**；用户可自定义切换主题，默认＝shadcn——结构与接入适配见附录 B |
| CN 网络 | 全链路已验证（npmmirror） | antd 生态国内原生友好：npmmirror/淘宝源齐、文档国内可达、团队中文经验多 |
| 团队实跑经验 | 两个内部 ToB 项目验证，§12 踩坑登记齐 | 本包无实跑经验，接入首季按 spike 对待；但 antd 为国内 ToB 后台事实标准，招人/协作成本最低 |
| AI 工具链 | — | **仓库自带 agent 资产**：根 `AGENTS.md`＋`.agents/skills`（symlink→`.claude/skills`：`antd`、`pro-upgrade` 两技能；antd 技能含 `@ant-design/cli` 七工具 list/info/doc/demo/token/semantic/changelog ＋ MCP server 模式）；官方另有 llms.txt、design.md（google-labs 格式）、MCP——AI 编码前 MUST 读仓库 skills（B.2 第 5 条） |
| 版本成熟度 | shadcn-admin 稳定 | antd 6.6.7 / Pro v6（2026-10 核实，MIT）；v5→v6 迁移期 API 有变，官方带 pro-upgrade 技能承接 |
| 授权成本 | MIT 免费 | MIT 免费（模板/脚手架全开源，无付费墙） |
| 主要风险 | 组件副本的维护成本 | Umi Max 框架绑定（路由/构建随 Umi；纯 Vite＋antd 属另一形态需另拍）＋ 内置 shadcn 主题（官网 neutral 灰阶）与 §2 stone 暖灰有微差需走查（B.1 吻合度条）＋ 主题包 import/依赖适配一次性成本 ＋ 经验空白 |

推荐＝**方案B**：后台壳最全且全免费（无授权门槛）、内置 13 主题资源（shadcn＝默认，用户可切换）、AI 编码资产官方内建（agent skills＋CLI＋MCP 让"禁凭记忆写码"有工具可执行）、国内 ToB 语境协作与招人成本最低。shadcn 黑白灰纪律经内置 shadcn 主题延续，不换血。**方案A 保留为轻量退路**（不想引 Umi 全家桶时用）。两者 UI-GATE 纪律相同。

### 0.2 拍板与落位规则

1. **时机**：plan 首轮技术栈批量问的 UI-GATE 检查环节呈报本表；Owner 未拍板前 §1–§12 保持方案A 默认、**UI-GATE 不解除、前端实现禁止开工**。
2. **落点**：拍板结果写 §0.3；方案选择＝HOW 层——进 DESIGN.md 与 plan Technical Context，MUST NOT 进 spec（AGENTS 落位判据）。
3. **选A**＝正文不动，§0.3 记裁决；**选B**＝按附录 B 重写 §2–§9 与检查清单，重跑 G2'（checklist）后再开工。
4. **中途换方案**＝判例登记（取下一个全局未用号）＋正文整体重写＋G2' 重跑，spec 零改动；禁止口头切换。
5. **新增候选**＝向本包模板追加附录并走一次包评审，不在项目内私加。

### 0.3 拍板记录

| 项 | 值 |
|---|---|
| 已选方案 | 待拍板（推荐候选 B；正文默认＝A，选 B 按附录 B 重写） |
| 拍板日期 / Owner | `<待填>` |
| 重皮依据（参考图/品牌色） | `<待填，无则「沿用默认体系」>` |

---

## 1. 设计定性（方案A · Soft-UI 黑白灰）

**基底**: shadcn/ui（new-york 风格）＋ Tailwind v4 CSS 变量＋ shadcn-admin 布局；所有页面 MUST 经 `@/components/ui` 组件与本文件 token 呈现，禁止页面内私调硬编码色值。

Soft-UI 轻拟物＋扁平：**无硬边框，靠白色卡片＋大圆角＋极柔环境阴影与暖灰背景拉开层次**。留白充足、冷静克制、无高饱和品牌色：主按钮近黑、激活态白卡浮起；仅保留功能语义色（成功绿/失败红/警告琥珀，全部低饱和莫兰迪调）。

## 2. 色彩 token（index.css `:root`，亮色为主；dark 段保留备用不承诺）

| 角色 | 变量 | 色值 | 说明 |
|---|---|---|---|
| 页面背景 | `--background` | `#F5F5F4` | 暖白偏灰（stone-100），侧栏与内容区同色无强分隔 |
| 卡片/面板 | `--card` | `#FFFFFF` | 纯白，靠阴影浮起，**无描边** |
| 主色（主按钮/激活） | `--primary` | `#18181B` | 近黑（zinc-900），白字 |
| 主色前景 | `--primary-foreground` | `#FFFFFF` | |
| 标题文字 | `--foreground` | `#1C1917` | 近黑暖调（stone-900） |
| 正文/次要文字 | `--muted-foreground` | `#78716C` | stone-500；placeholder/表头/分组小标题用 `#A8A29E`(stone-400) |
| 悬浮/选中底色 | `--accent` | `#FFFFFF` | 激活菜单＝白卡浮起（配阴影） |
| 边框/分隔线 | `--border` | `#E7E5E4` | stone-200，1px，仅输入框/表格行/分隔线用 |
| 输入框边 | `--input` | `#E7E5E4` | 同上 |
| 焦点环 | `--ring` | `#18181B` | 聚焦＝近黑 ring/30% |
| 功能-成功 | badge success | 底 `#ECFDF5` 字 `#047857`；状态点 `#84A98C` | 在线/启用/任务成功 |
| 功能-失败 | `--destructive` | `#DC2626`（柔和呈现：底 `#FEF2F2` 字 `#B91C1C`） | 离线/失败/删除 |
| 功能-警告 | badge warning | 底 `#FFFBEB` 字 `#B45309` | 超时/执行中 |
| 侧栏系 | `--sidebar*` | 同背景色系；激活项＝白＋阴影 | 见 §5.1 |

> 红线：**任何页面不得引入蓝/绿/紫等高饱和装饰色**。头像底色允许低饱和多色，文字白色。

## 3. 字体层级（root 16px 不缩放；中文 PingFang SC/思源黑体，西文与数字 Inter/系统等宽）

| 层级 | 字号/字重 | 用途 |
|---|---|---|
| 页面主标题 | 24px / 700 | PageHeader 标题 |
| 卡片/区块标题、按钮 | 15–16px / 600 | CardTitle、主按钮 |
| 正文/表格/菜单项/表单标签 | 14px / 400 | 默认 |
| 表头/标签胶囊/辅助说明/快捷键 | 12–13px / 400，灰色 | TableHead、Badge、muted |
| 分组小标题/Logo 副标/版本号 | 11–12px，`tracking-wider`，stone-400 | SidebarGroupLabel |

行高宽松：正文 1.5–1.7；表格行高 ≥52px。**紧凑＝布局密度，不靠缩字号。**

## 4. 圆角/阴影/边框（Soft-UI 三要素）

| 元素 | 圆角 | 边框 | 阴影 |
|---|---|---|---|
| 大卡片（Card/弹层内容卡） | 16–20px（`rounded-2xl`） | 无 | `0 8px 24px rgba(0,0,0,.05)`（`--shadow-card`） |
| 模态面板（Dialog/命令面板） | 20–24px | 无 | `0 25px 50px -12px rgba(0,0,0,.25), 0 4px 12px rgba(0,0,0,.08)`（`--shadow-float`） |
| 按钮/输入框/下拉 | 10px（`rounded-[10px]`） | 输入框 1px `--input`；主按钮无 | 主按钮 `0 2px 8px rgba(0,0,0,.12)` |
| 搜索框/标签/快捷键标签 | 全圆角胶囊 | 标签无 | 无 |
| 复选框 | 6px | 1px | — |
| 头像/信息图标 | 全圆 | — | — |
| 激活菜单项 | 10px | 无 | `0 2px 8px rgba(0,0,0,.06)`（浮起白卡） |

按钮体系：**主按钮＝近黑底白字**（`--primary`）；次按钮＝无背景文字按钮（带线性图标）；图标按钮＝白底圆角方形＋淡边＋小阴影。禁用态 opacity-50。
悬停指针：所有可点控件 MUST `cursor: pointer`，禁用态维持 default——Tailwind v4 preflight 把 button 默认改 default，须在 `index.css` base 层全局恢复：`button:not(:disabled), [role="button"]:not([aria-disabled="true"]), label[for], select, summary { cursor: pointer }`。

## 5. 布局（shadcn-admin 结构）

### 5.1 侧边栏（宽 16rem，可折叠为图标栏）
- 背景与页面同色，与内容区**无强分隔线**。
- 顶部 Logo 组：深色圆角方块图标（白线性图标）＋产品名 600 ＋副标 11px 灰 `tracking-widest`。
- 导航按业务域分组（分组标题＝灰色小字 `tracking-wider`）。
- 菜单项＝Lucide 线性图标＋文字，高 40–44px；**激活项＝白底圆角卡＋柔阴影＋加粗黑字**；hover＝浅灰。
- 底部版本号灰色小字。

### 5.2 顶栏（高 56–64px，底部 1px 极淡分隔线，白底）
左：折叠按钮（SidebarTrigger）→ 竖分隔线 → 面包屑（上级灰、当前黑 600）。
右：⌘K 搜索胶囊（放大镜＋「搜索菜单」＋键帽标签，点击开命令面板）→ 用户区（圆形头像＝姓名前二字白字深底＋姓名＋角色小字＋下拉箭头；菜单含退出登录）。

### 5.3 命令面板（⌘K，cmdk Dialog）
居中偏上（top≈17%）、max-w 560–640px、`--shadow-float`。三段式：搜索头（放大镜＋placeholder＋`Esc` 键帽）→ 分组列表（行＝圆角图标容器＋主标题 600＋可选次要标签；**选中行＝白底＋细边＋轻影浮起，图标染黑，右侧 `→`**）→ 底部快捷键栏（键帽统一：底 `#F9FAFB` 边 `#E5E7EB` 圆角 6px）。

### 5.4 内容区
外边距 24–32px；页头＝主标题 24px/700＋灰色副标题说明，右侧放页面主操作（**≤3 个**：分段控件/深色主按钮）；卡片内边距 20–24px；控件横向 gap 12–16px；间距按 8 的倍数。

### 5.5 表格（数据卡）
卡片头：状态色点＋标题＋「共 N 条」灰字；右侧刷新/下载方形图标钮。表头灰小字 12–13px；行高 ≥52px；行间极淡分隔线；行 hover 浮白。单元格：复选框列 → 主体列（圆形文字头像/主标识＋次要小字两行）→ 标签列（浅灰胶囊）→ 状态列（色点＋文字）→ 操作列（3–4 个灰色线性图标钮，hover 染黑）。卡片底：左「共 N 条，当前 x–y」＋右「N 条/页」下拉＋翻页（当前页白底高亮）。

### 5.6 登录页（分栏 1:1）
- **左栏（品牌区，lg 以下隐藏）**：底 `#0A0A0A`＋细网格纹理＋径向白/灰光晕。左上 Logo 组；中部大标语 40px/700 白＋副说明 14px `#9CA3AF`；底部毛玻璃特性卡（`rgba(255,255,255,.04)`＋`backdrop-blur(12px)`＋1px 白 8% 边、圆角 16–20px）内 2×2 网格特性。
- **右栏（表单区）**：背景 `--background`；居中白卡 max-w 420px、圆角 24px、`--shadow-card`、内边距 32–40px。卡内：小标签灰 → 标题 30px/700 → 副标 → 字段（标签 13px/500；输入框高 48px 圆角 10px 左侧内嵌灰线性图标；字段间 20–24px）→ 错误态 Alert（destructive 柔和底）→ **全宽近黑主按钮**（高 48px，投影 `0 8px 16px rgba(0,0,0,.15)`）→ 底部灰字帮助文案。

## 6. 图标

统一 **Lucide 线性描边**（stroke 1.5–2px、圆角端点），默认 `#78716C`，激活/深色底内为白，尺寸 16–20px。头像不放图标，放**姓名/对象前两字**文字徽标。箭头用 `›`/`⌄` 细线；快捷键一律键帽样式。

## 7. 动效（克制）

- 过渡只用于 color/background/box-shadow/width（150–200ms ease）。
- 弹层：fade+zoom 进入（radix 默认）；命令面板选中行即时切换无动画延迟。
- **禁止**：弹跳、闪烁、庆祝动画（红线：不庆祝失败、不施压）。加载＝Skeleton（圆角灰块）或「加载中…」灰字；提交按钮 pending 文案变化＋disabled。

## 8. 密度纪律

root 16px 不缩字号；单屏信息不过载（一屏一个主任务区）；ToB 零黑话文案、全中文。表格行高取 ≥52px 上限附近即可，不做 further 放大。

## 9. 落地映射（代码层）

| 设计项 | 实现位置 |
|---|---|
| 色彩/阴影/圆角 token | `frontend/src/index.css`（`:root`＋`@theme inline`＋`--shadow-card/--shadow-float`） |
| 卡片无边框浮起 | `ui/card.tsx`（去 border、rounded-2xl、shadow-card） |
| 按钮/输入框 10px 圆角 | `ui/button.tsx`、`ui/input.tsx` |
| 激活菜单白卡浮起 | `index.css` `[data-sidebar=menu-button][data-active=true]` 覆写 |
| 布局/顶栏/⌘K | `components/layout/app-layout.tsx`＋`command-menu.tsx` |
| 登录页 | `pages/login/index.tsx` |
| 表格卡头/分页样式 | `components/data-table-card.tsx` 或各页 Card 组合 |

> Tailwind v4 自定义 shadow/radius token 必须在 `@theme inline` 注册才生成 utility 类；build 后 grep dist CSS 验证 token 值真实产出——缺失时类名静默无效。

## 10. 移动端适配

- **断点**：<768px（`md` 以下）＝手机形态；≥768px 桌面形态不回退。
- **导航**：窄屏侧栏变 Sheet 抽屉，顶栏汉堡拉出；⌘K 胶囊窄屏隐藏、头像菜单保留。
- **表格卡片化**：窄屏每行转竖排卡片（`MobileRowCard` 或双渲染）：首行＝主标识＋状态 Badge；中部＝关键字段两列 label:value；底部＝操作按钮全宽（触控 ≥40px）。次要字段可省略但不得改变语义。
- **触控**：可点目标 ≥40px 高（`size="sm"` 仅桌面）；筛选条窄屏纵排；分页按钮 `h-10`。
- **弹层**：Dialog 窄屏 `max-w-[calc(100vw-2rem)]`，内容可滚动。
- **验收**：375×667 与 768px 两档走查：无横向滚动条、无触控目标 <40px、表格页出卡片形态。

## 11. 交互行为规则（页面级交互的落点——弹层/抽屉/确认在这章，不在 spec）

> 本章是「点击创建按钮需要给出弹层」这类规则的**正式归属地**（与 `preview/` 原型配合：形态规则写这里，具体页面长什么样由原型呈现）。新增交互规则持续追加，编号递增。

### 11.1 弹层选型

| 场景 | 形态 | 电子商城示例 |
|---|---|---|
| 单实体创建/编辑（字段 ≤8） | 居中 Dialog | 点「创建商品」→ 弹层填名称/类目/价格/库存 |
| 字段多或含表格/详情（>8 字段、多区块） | 右侧抽屉（Sheet）或全屏弹层 | 商品详情弹层含 SKU 表 |
| 高危确认（删除/作废/不可逆） | AlertDialog 阻断式，确认按钮 = destructive 色 | 「下架该商品？已售 X 件不可自动恢复」 |
| 纯信息展示 | toast/行内展开，不占模态 | 保存成功提示 |

判据：**换端后这条还成立吗？** 「操作人 MUST 二次确认才提交」是需求（进 spec 的 FR）；「用 Dialog 还是 Sheet 承载确认」是实现形态（进本章）。弹层改抽屉属 UI 微调；**去掉弹层=去掉确认义务，属需求变化，须先改 spec**。

### 11.2 创建/编辑弹层通用规则

- 触发：页头主操作区按钮（≤3 个主操作，见 §5.4）或表格行操作列；按钮文案＝动词＋对象（「创建商品」不写「新增」）。
- 内容：字段自上而下按填写频率排；枚举/选项类输入 MUST 用下拉 Select，MUST NOT 让用户手输，禁裸 `<select>`；关键词输入框排搜索区最前，筛选下拉依次在后。
- 提交：底部 Footer 操作区；pending 态按钮文案变化（「保存中…」）＋ disabled，禁双提交。
- 关闭：右上角 X 与底部「取消」并存；**表单已填内容非空时关闭 MUST 给丢弃确认**（数据丢失红线）。
- 校验：字段级错误就地显示（destructive 柔和底），不做整屏弹窗报错。

### 11.3 列表↔详情

- 详情入口双通道：主键列做成链接式按钮＋操作列「详情」按钮。
- 列表主列 ≤6（宪法 II），次要信息收「详情」弹层；桌面表格与窄屏卡片**同口径收敛**。
- 未处理/待办行在详情弹层内可直接转入处理动作（少一次跳转）。

### 11.4 加载/进度/反馈（配合宪法 II 高强度关怀）

- 批量/长等待操作 MUST 显示：明确进度、预计耗时、正在发生什么、下一步建议；完成后给平实结果确认（禁庆祝动画）。
- 提交等待 ≥300ms 给 pending 视觉；数据加载给 Skeleton，禁空白页转圈。
- 空状态给一次性、可静音的引导（不拦截）；错误态＝原因 + 可行动作，不甩堆栈。

## 12. UI 组件使用约束（强制，每次写 UI 前必读；来自实际踩坑，持续追加）

### 12.1 Dialog 弹层内容宽度
- DialogContent 内所有 Card MUST 加 `className="w-full"`；所有 Table MUST 外包 `div className="overflow-x-auto"`。
- 宽度用 `max-w-*` 控上限，内容 `w-full` 填满不溢出；多卡片用 `flex flex-col gap-4`。

### 12.2 表格列宽与溢出
- 表格列数 ≤8（超出拆分或展开行）；长文本列（编号/SKU）`font-mono text-xs` + `truncate` 或允许换行；操作列固定 `w-28`/`w-32`；状态列用 Badge 不用纯文字。

### 12.3 响应式断点
- 桌面表格 `hidden md:block`；移动端卡片 `md:hidden`；弹层窄屏 `max-w-[calc(100vw-2rem)]`；按钮窄屏 `h-10`、桌面 `h-9`。

### 12.4 卡片嵌套
- 禁止卡片内再嵌套卡片（用 Separator 分隔区块）；区块标题用 `<p className="mb-3 text-xs font-medium text-muted-foreground">`，不用 CardTitle；弹层内卡片同页面级但 MUST 加 `w-full`。

### 12.5 弹层 Footer 按钮
- `<div className="flex justify-end gap-2 pt-1">`；取消 `variant="outline" size="sm"`；确认 `size="sm"`＋pending「保存中…」+ disabled；关闭统一右下角（DialogContent 自带右上 X）。

### 12.6 空/加载/错误态
- 空数据：`StateHint` 或 `rounded-lg border border-dashed py-8 text-center` 占位；加载：Skeleton；错误：Alert destructive。状态四态（Loading/Progress/Success/Error）与 Empty 为每页必备。

### 12.7 颜色与语义
- 成功/在线 `Badge variant="success"`；失败/离线 `destructive`；警告/进行中 `warning`；中性/未配置 `text-muted-foreground`。**禁止纯文字表状态**，MUST 用 Badge 或色点。

### 12.8 代码/编号字体
- 编号类（SKU/单据号/商品编号）`font-mono text-xs` 或 `text-[13px]`；时间戳 `tabular-nums`；普通文字默认 sans-serif。

---

**检查清单**（每次写 UI 后自检）：
- [ ] Dialog 内 Card 都有 `w-full`？Table 包了 overflow-x-auto？
- [ ] 表格列数 ≤8？长文本有 truncate？
- [ ] 移动端有卡片形态（`md:hidden`）？
- [ ] 状态用 Badge 不是纯文字？编号用 `font-mono`？
- [ ] 弹层 Footer 按钮位置正确？pending 有 disabled？
- [ ] 表单非空时关闭有丢弃确认？
- [ ] 空/加载/错误态有处理？
- [ ] 无高饱和装饰色、无庆祝动画？

---

## 附录 B. 方案B（Ant Design Pro v6）正文要点——Owner 选定 B 后据此重写 §2–§9

> 本附录＝候选方案的呈现要点与接入纪律，非最终正文。选定 B 时：§2–§4 token 表、§5 布局、§6 图标、§7 动效、§9 落地映射 MUST 依此重写并补实际 token 值走查；§10 移动端、§11 交互行为规则、§12 通用纪律（四态、丢弃确认、零黑话、不庆祝、≤6 主列、≤3 主操作、不缩字号）**原样保留**——它们是跨方案铁律，不随换 UI 失效。§12 中 shadcn 专属条目（Dialog `w-full`、`ui/*.tsx` 覆写）随重写替换为 antd 对应踩坑登记（接入初期为空，实跑后追加）。

### B.1 技术事实（2026-10 经 GitHub API / npm registry / 官方文档核实）

- 基线＝`ant-design/ant-design-pro`（v6，MIT，38.9k star）：React 19 / Umi Max 4 / antd 6 / utoopack（可切 Umi 常规构建）；块模板＝Welcome、Dashboard（Analysis/Monitor/Workplace）、Form（基础/分步/高级）、List（搜索×3/表格/基础/卡片）、Profile、Result、Exception、Account、AI Assistant、User（登录/注册）。装包 CN 网络走 npmmirror 即可（antd 生态国内源齐备）。
- 主题三层＝Seed→Map→Alias design token，经 `ConfigProvider theme={{...}}` 下发；`theme.algorithm` 预设 default/dark/compact 算法可组合。
- **内置主题资源（vendored，本包 `materials/antd-themes/`，13 个主题文件，纯资源无注册表）**：源自 ant.design 官方主题预览区（官网 themes 页同一套代码，MIT 生态资产；原 `index.ts` 注册表已删，主题列表/切换器由项目自建）。主题清单：shadcn（**默认，MUST**）、mui、bootstrap、cartoon、illustration、glass、geek、lobe、lark、blossom、v4、serene（12 个 hook 形态＝`use*Theme()` 返回 `ConfigProviderProps`）＋ hero（HeroUI Dashboard 风格，亮/暗双 `ThemeConfig`）；antd 原生 light/dark 基础外观用 `defaultAlgorithm`/`darkAlgorithm` 直接派生，不占文件。
- **接入形态**：所需主题文件拷入项目（建议 `src/themes/antd/`），项目自建主题注册表＋切换器，默认页＝shadcn，按 `ConfigProviderProps` 消费（`<ConfigProvider {...themeProps}>`；hero 用 `<ConfigProvider theme={heroLightTheme}>`）。**依赖适配**：7 个主题（shadcn/mui/bootstrap/cartoon/illustration/glass/geek）依赖 `antd-style`＋`clsx`（mui 另 `@rc-component/util`），接入需加依赖或改写为纯 token/CSS 变量——**取舍记 §0.3**；主题文件零官网路径耦合（`?raw`/useLocale/svg 已随注册表移除），主题名/图标/背景图在切换器侧自备。
- **shadcn 主题与 §2 黑白灰体系吻合度（已核对源码）**：`colorPrimary` 灰黑系（`#262626`＋hover `#404040`/active `#171717`）、`colorPrimaryBg #f5f5f5`、`borderRadius 8`、按钮主色 `#18181b`、边框 `#e4e4e7`——与 §2 `--primary #18181B`/`--border #E7E5E4` 同族但非逐字一致（官网版偏 neutral 灰阶，§2 是 stone 暖灰）。纪律：以 vendored `shadcnTheme.ts` 为默认运行基线；若 Owner 要求像素级贴合 §2，改该文件 token 值并同步本节，MUST NOT 另立第二套 shadcn token 源（防双轨）。
- **动态主题（选型硬要求，MUST）**：用户可自定义切换主题——项目自建主题列表（从 `antd-themes/` 资源挑入，含 hero 亮/暗）＋切换器（设置面板或顶栏入口）＋ `cssVar: true`（运行时 CSS 变量，切换不重编译样式、杜绝半屏残影）＋选择持久 localStorage（可跟随 `prefers-color-scheme` 作初始值，默认仍＝shadcn）。**红线**：组件内 MUST NOT 硬编码色值——一切颜色走 token/主题变量；`theme=undefined↔object` 切换会引发组件重挂载（官方 FAQ），初始即给空对象 `{}` 兜底。
- **AI 编码资产（MUST 使用）**：仓库根 `AGENTS.md`＋`CLAUDE.md` 与 `.agents/skills`（symlink→`.claude/skills`）内两技能——`antd`（触发词＝antd 组件/API/props/token/迁移/版本分析；经 `@ant-design/cli` 提供 `antd_list/info/doc/demo/token/semantic/changelog` 七命令，`--format json`＋`--lang zh`，亦可作 MCP server 暴露 7 tools＋2 prompts）与 `pro-upgrade`（v5→v6 升级承接）。**写 antd/Pro 代码前 MUST 先读这两个 SKILL.md 并优先用 CLI 查当期 API，禁凭记忆写码**（token 名/props 以 CLI 输出为准）。官方层另有 llms.txt、`https://ant.design/design.md`（google-labs design.md 格式，供 AI 设计工具）、MCP server。
- 组件语义钩子＝antd 各组件 `classNames`/`styles` 语义结构（v6 全组件覆盖），局部微调走语义钩子不写全局 CSS 覆写；Pro 布局壳＝`ProLayout`（侧栏/顶栏/水波纹/多 tab）＋ ProTable/ProForm（schema 驱动，字段四列纪律可映射其 columns 定义）。

### B.2 选型必配纪律

1. **§0.3 记拍板后先 spike**：用 Pro 的任一表格页走通「脚手架起站→拷入所需 `antd-themes/` 主题文件并定依赖取舍（antd-style/clsx）→自建主题列表默认页＝shadcn 生效→主题切换器动态换肤无残影→生产构建」五步再全量接入；spike 不达标＝回到 §0 重拍，不得带病推广。
2. **升级锁版**：`antd`/`@ant-design/pro-components` 钉精确版本（v5→v6 API 有 breaking 史），升版走判例登记＋跑仓库 `pro-upgrade` 技能对照清单；`antd-themes/` 若跟进 ant.design 上游改版，同样走判例登记（记录来源 commit/日期）。
3. **动态主题验收进 G2'**：冒烟断言加三条——①默认主题＝shadcn（首屏 `colorPrimary` 为灰黑系非 antd 蓝）；②运行时切换主题后全页无硬编码色残留（getComputedStyle 抽查 token 变量生效、无半屏残影）；③切换不触发整树重挂载（theme 初始给 `{}`）。
4. **视觉铁律不换血**：§8 密度（root 16px、不缩字号、紧凑靠布局）经 `controlHeight`/`size` 与组件 token 实现；antd 默认蓝 `#1677FF` MUST 被 shadcn 默认主题（灰黑系 `colorPrimary`）覆盖——未覆盖＝G2' 不过。用户切换的其他主题（mui/glass/geek 等）允许各自的强调色，但 ToB 生产环境默认展示＝shadcn，切换器入口不抢主操作位（§5.4 主操作 ≤3 纪律）。
5. **AI 会话开场规**：前端实现会话 FIRST READ＝仓库 `AGENTS.md`＋`.agents/skills/antd/SKILL.md`＋本 DESIGN.md §0.3 拍板记录；三件读齐前不落任何 antd 代码（UI-GATE 在方案B 的具体化）。
