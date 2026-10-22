---
name: shadcn-admin-frontend
description: Use when building React+Vite+shadcn/ui admin frontends.
---

# shadcn-admin-frontend

## When to Use

搭建或升级任何 React 管理后台前端；用户提到 shadcn/shadcn-admin/前端骨架/登录页/侧边栏布局；委托子任务搭前端脚手架（把本 skill 的铁律和 CN workaround 写进委托指令）。也适用于 Playwright 前端冒烟、vite dev 联调排障。

ToB 系统前端（React 19 + Vite + TS + Tailwind v4 + shadcn/ui + TanStack Query + react-router-dom），在旧版 macOS、国内镜像网络环境上搭建与升级。

## 铁律（Owner 拍板，违反会被打回）

- 组件必须走官方 shadcn CLI（`npx shadcn add`），禁止手写「等效精简骨架」代替——用户看到手搓组件的直接评价是「毛坯风格」。委托子任务搭前端脚手架时，同样禁止在指令里给「手工搭等效骨架」作为 fallback 选项；应把下方 CN 网络 workaround 写进委托指令，让 CLI 路线成功。
- 布局按 shadcn-admin 结构：可折叠图标侧栏（Sidebar collapsible="icon"，导航分组）＋顶栏（SidebarTrigger＋面包屑＋全局搜索＋用户头像 DropdownMenu）＋卡片式内容区；App 外层包 TooltipProvider＋SidebarProvider＋Toaster(sonner)。
- 品牌与表单控件规范（Owner 拍板，全项目适用）：
  - 登录页与后台内 MUST 体现公司/产品品牌（登录卡品牌区＋侧栏 logo 文案）；用户给图标图片时同轮设为 web favicon（`index.html` 的 icon link，图片放 `public/`），不止贴进页面。用户上传的图片可能扩展名与实际格式不符（名为 `.ico` 实为 PNG）——先读头部字节判定，若是 PNG 则用 PIL 转真多尺寸 ICO（`sizes=[(16,16),(32,32),(48,48),(64,64)]`）并同时保留 PNG，`index.html` 里 `rel=icon`＋`type="image/png"` 的 apple-touch-icon 各指一份；改完 curl 两个路径验 200 与 content-type。
  - 枚举/选项类输入一律用下拉 Select，MUST NOT 让用户手输，禁自由文本框；下拉要有正常 UI 样式（shadcn Select 组件，禁裸 `<select>`，包括弹窗内的）。
  - 大集合值域（时区等）的选项范围先问 Owner，别默认全量：IANA 时区约 400 项，Owner 可能只要「常用基线 ∪ 业务涉及国家对应」（十几项）——值域做成后端选项端点（带 UTC 偏移标注便于选择），前端只消费，将来改范围零前端改动。
  - 所有列表页搜索区统一布局：关键词输入框排最前，筛选下拉依次在后。
  - 筛选下拉的选项来源 MUST 由后端配置驱动（如国家清单来自平台账号配置，经 options 类端点下发），前端 MUST NOT 写死——写死会在新增账号/密钥组后静默缺选项；新筛选维度先配后端选项端点再接前端。
- 配色：仓库有 DESIGN.md（如 specs/*/DESIGN.md）时其 token 是唯一权威——DESIGN.md 由 Owner 拍板产生，冲突时永远改代码不改 DESIGN.md；无 DESIGN.md 才守 ToB 默认（灰白主调＋单一克制强调色）。无论哪套：root 16px、密度靠间距不缩字号、文案全中文零黑话、禁高饱和装饰色，仅保留低饱和功能语义色（成功/失败/警告）。

## CLI 接入流程（CN 网络已验证）

1. 建 `components.json`：style=new-york、css=src/index.css、cssVariables=true、aliases（components/ui/lib/hooks→@/…、utils→@/lib/utils）、iconLibrary=lucide。
2. **根 `tsconfig.json` 必须含 `baseUrl`+`paths`（`@/*`→`./src/*`）**——只在 tsconfig.app.json 有不够，CLI 解析不了别名会把全部组件写进字面量 `./@/` 目录；发现后 `cp "@/components/ui/"*.tsx src/components/ui/` 归位再删目录。
3. `.npmrc` 加 `legacy-peer-deps=true`（registry 已指 npmmirror）——CLI 内部触发的 npm install 会因 zod/react-hook-form 系 peer 冲突整体失败。
4. 本地装 CLI：`npm install -D shadcn --registry=https://registry.npmmirror.com`；`npx --yes shadcn@latest` 现场下载会 ETIMEDOUT。
5. 批量拉取（一次列全，`--overwrite --yes`）：`npx shadcn add button card input label table badge dialog select checkbox dropdown-menu tooltip separator avatar breadcrumb sheet skeleton sonner tabs textarea switch scroll-area sidebar command popover progress alert alert-dialog collapsible radio-group`
6. 验收：`npm run build`（tsc -b）＋ `npm run lint` 0 error 才算完成。

## 坑

- `menu` 不是 registry 组件名（sidebar 家族自带导航），列进 add 会让整批失败——CLI 是整批校验，一个名字错全部不落盘。
- `--overwrite` 会冲掉自定义 badge 变体（success/warning 状态色）——覆盖后 diff 备份补回，业务页在用的变体先 grep 确认。
- 新版 CLI 组件 `import { cn } from "cn"`（独立 npm 包）而非 `@/lib/utils`——两者并存可正常构建，不必统一。
- vite dev server 默认可能只听 IPv6 `[::1]`——`server` 配置加 `host:true`，否则 127.0.0.1 连接被拒，呈现「服务明明起了却连不上」的假象。
- 登录跳转竞态（setToken+navigate 后被守卫弹回登录页）：见 references/spa-auth-guard.md，token 必须进 React state。
- Playwright 在旧版 macOS（13 及以下）不支持新版，钉 `@playwright/test@1.49.1`；下载走 `PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright/`，装 `chromium`。headless 默认跑的 `chromium-headless-shell` 组件在 mac13 常常下不下来（反复报 Executable doesn't exist … headless_shell）——别死磕重试装它，改在 playwright.config 的 `use.launchOptions` 加 `{ channel: "chromium" }`，复用已装的完整 Chromium 新无头模式，直接跑通。
- 后台 terminal 起长驻服务（vite/e2e 后端）时禁止管道接 `head -N`——head 读满即关管道，SIGPIPE 会杀死服务进程；长驻进程用 background=true 裸输出，需要看日志用 process poll。
- execute_code 里 urllib 探测本地端口须 `build_opener(ProxyHandler({}))`——系统代理会拦截 127.0.0.1 并报 ConnectionRefused。
- Tailwind v4 自定义 shadow/radius token（如 shadow-card）必须在 `@theme inline` 注册（`--shadow-card: var(--shadow-card)`）才生成 utility 类；build 后 grep dist CSS 验证 token 值真实产出——缺失时类名静默无效，页面看着「样式没生效」。
- **动态注入第三方地图 SDK 必须带官方 `callback` 参数**：不带 callback 的 loader 内部靠 `document.write` 注入 SDK 本体，而浏览器禁止异步加载的外部脚本 document.write（console `Failed to execute 'write' on 'Document'`）→ 全局对象只剩 loader 建的**空壳** → 构造地图时 `Cannot read properties of undefined (reading 'Map')` → 静默走降级列表，页面看着仍有数据。就绪判定要收紧到具体构造器（`BMapGL?.Map` 而非 `BMapGL`），回调内校验通过才 resolve，否则 reject 让降级路径显式报错。同类 SDK（Google Maps）本就是 callback 模式，两个 loader 要保持同一形态。
- 地图 AK 的鉴权失败由 **SDK 自己弹原生 alert**（百度错误码：240＝APP 服务被禁用、220＝Referer 白名单不匹配、101＝AK 不支持 jsapi、203＝应用类型错、260/261＝未勾选该服务），属凭据侧配置而非代码问题——所以 key MUST 走后端运行时下发端点（`GET /map-config` 一类）而非构建时 `VITE_*` 注入：构建注入需 build-arg、会把 key 固化进 bundle（违背镜像零凭据），且容器构建漏传时**静默不生效**；运行时下发则改 key 无需重建镜像。诊断时先 curl SDK loader URL 看返回体是否含错误码文案，再用浏览器接住 dialog 确认实际码。
- Tailwind v4 preflight 把 `<button>` 默认 cursor 从 pointer 改成 `default`（官方 breaking change）——全站按钮悬停无手型。在 index.css 用 `@layer base { button:not(:disabled), [role="button"]:not([aria-disabled="true"]), label[for], select, summary { cursor: pointer } }` 全局恢复，禁用态维持 default（语义正确）；验证＝Playwright `getComputedStyle(n).cursor` 断言 pointer，别靠肉眼看截图。

## 页面撤销 / 入口合并（导航重构）

用户要求「某功能页并进别页的一个按钮 / 删掉独立页」时，改动面远大于路由本身，按此清单扫：

1. 旧路由保留为重定向（`<Navigate to="/new-path" replace />`），别直接删 Route——旧书签与外链不断。
2. 全仓 grep 旧路由字符串与旧页面名：src（导航数组、⌘K 命令面板、其他页面的空态/引导文案、Link/navigate）与 tests（e2e 的 goto、按钮 name 断言）。导航通常存在两处（sidebar 配置＋命令面板配置），必须都改；删页后跑 lint 清出 unused import（图标等）。
3. 引用被删页面的跨页文案（「先到 X 页…」空态引导）一并改口径指向新入口；新入口按钮遵守触控规范（窄屏 ≥40px，如 `h-10 md:h-9`）。
4. 验收＝build＋tsc＋lint＋Playwright 全绿，另 grep 容器/dist 产物「新文案在、旧文案无」确认部署侧是新版（dev 绿不代表容器镜像已重建）。
5. SDD 仓库还须同步：DESIGN.md（UI 真相源）补入口条款、preview/ 原型（删页、全站 topnav 清扫、PREVIEW.md 映射表＋决策日志）、quickstart 操作文案。入口/布局变更属实现层——FR 语义（如「唯一入口」）不变时 spec 零改动，决策日志注明分流依据。

## 列表收敛与详情弹层（ToB 信息密度反馈）

用户反馈「列表展示的信息过多 / 某些列不用展示 / 要支持查看详情」时：

1. 主表删列向界面铁律回归（主列 ≤6＋勾选/操作列；次要信息收详情），桌面表格与窄屏 MobileRowCard **同口径收敛**——只改桌面会留下移动端信息过载。
2. 完整字段进「详情」弹层：列表接口若已返回全字段（契约核对），这是纯呈现层调整——后端/契约/spec 零改动，PREVIEW.md 决策日志记一笔即可。
3. 详情入口双通道：主键列（编号）做成链接式按钮＋操作列「详情」按钮；未处理/待办行在弹层内可直接转入处理动作（少一次跳转），弹层字段用 `<dl>` 两列 label:value，条件字段（如处理人/时间/备注）仅对应状态展示。
4. 验收用临时 Playwright spec 硬断言，不看截图：thead 列集合（删的列 not.toContain＋保留列 toContain）、详情弹层逐字段 toContain、处理按钮可点转弹层；跑完并入常驻 spec 或删除，别留孤儿断言。

## 参考图改版

用户给应用截图要求「做成这个风格」时，走 references/design-from-screenshots.md：vision_analyze 抽规格 → 立/改 DESIGN.md → token 层→组件层→布局层→页面层顺序落地 → dist CSS 验证。

## e2e 冒烟模式（Playwright 四链路）

前端冒烟需要可控后端：建 `cmd/e2eserver`（与生产入口同构装配，差异四点——数据源换 mock adapter、独立测试库名、SMTP 指向不可达端口=发送必失败可验留痕不真发、seed 测试 admin）；账号经环境变量注入（E2E_EMAIL/E2E_PASSWORD），测试文件里默认值用虚构域名；前端 dev server 经 E2E_BACKEND 环境变量把 /api 代理过去（vite.config 里 `target: process.env.E2E_BACKEND || "http://localhost:8080"`）。
