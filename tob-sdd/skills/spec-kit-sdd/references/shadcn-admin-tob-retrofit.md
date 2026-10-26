# shadcn-admin 模板改造配方（ToB 内网项目，项目A 2026-09-29 验证）

把 https://github.com/satnaing/shadcn-admin 落成内网 ToB 前端（FastAPI 单进程托管、无 nginx）的完整步骤与坑。React 19 + Vite + TanStack Router/Query/Table + Tailwind v4 + shadcn/ui + pnpm。

## 1. 落库与裁剪

```bash
git clone --depth 1 https://github.com/satnaing/shadcn-admin.git frontend
rm -rf frontend/.git
```

- 删 demo：`src/routes/clerk`、`src/routes/_authenticated/{chats,apps,tasks,users,help-center}`、对应 `src/features/*`、`src/features/dashboard`（首页改 redirect 到业务首屏）。
- `package.json` 去掉 `@clerk/react`；删 `src/assets/clerk-logo.tsx` 等残留引用（grep `@clerk|clerk-logo` 清零）。
- `(auth)` 路由可保留（未启用登录时不碍事）；首期内网无认证＝`_authenticated` layout 本身不拦截，无需旁路代码。
- 侧栏改 `src/components/layout/data/sidebar-data.ts`（业务菜单+中文标题；teams 留一个即可）。
- 模板上游杂物（`frontend/.github/`、CHANGELOG、netlify.toml）入库无害，介意就删。

## 2. pnpm 安装坑

- 国内：`npm i -g pnpm --registry=https://registry.npmmirror.com`，`pnpm install --registry=…`。
- `ERR_PNPM_IGNORED_BUILDS`（esbuild 等 postinstall 被拦）→ package.json 加：
  ```json
  "pnpm": { "onlyBuiltDependencies": ["esbuild"] }
  ```
- `pnpm-lock.yaml` 建议 gitignore（团队未统一 pnpm 前避免锁文件噪音；统一后再入库）。

## 3. 路由生成顺序（tsc 报错的假象）

TanStack Router 的 `routeTree.gen.ts` 由 **vite 插件在构建时**生成；`pnpm build` = `tsc -b && vite build`，新加路由文件后 tsc 先跑 → 报 `TS2345 '/_authenticated/xxx' not assignable to keyof FileRoutesByPath`。
**解法：先单跑 `pnpm exec vite build` 重生 routeTree，再 `pnpm build`。** 不是代码错。

## 4. 对接 FastAPI 托管（无 nginx）

```ts
// vite.config.ts
server: { port: 5173, proxy: { '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true } } },
build: { outDir: '../backend/app/static', emptyOutDir: true },
```

FastAPI 侧：`app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"))`（注意双层路径坑）+ catch-all 回 index.html；**catch-all 与 API router 的注册顺序**：API include_router 全部在 catch-all 之前。

## 5. 视觉落地（2026-10-23 Owner 拍板改「上游原样制」后修订）

历史教训保留：用户说"紧凑/小巧"时先确认是**字号还是密度**，默认解读为布局密度，字号保持正常可读（root 16px 不缩字仍是铁律）。

- ~~紧凑三 token（`--spacing:0.22rem`／`line-height:1.45`／`--radius:0.375rem`）＋控件 `h-8/h-7`＋表格行高 ≥52px~~——**Owner 2026-10-23 拍板全部删除**：密度纯用上游默认，不再全局收紧；换皮唯一入口＝`theme.css` 变量（见 DESIGN §1/§4）。
- **字体＝离线下载入仓自托管（Owner 定案，取代旧「降级系统栈」案）**：下载 Inter/Manrope 的 woff2 存进项目（建议 `src/styles/fonts/` ＋ `@font-face` 本地声明，family 名沿用 `--font-inter/--font-manrope` 注册值——组件类名零改动、观感＝上游）。获取：`rsms.me/inter` 官方发布包，或 `@fontsource-variable/inter`＋`@fontsource/manrope`（npmmirror 可达）取包内字体文件入库。同步删 `index.html` 的 Google Fonts `<link>`/preconnect 及 og/twitter 外链图。
- 配色不动（模板默认 slate 中性色已符合），彩色只留语义：destructive=危险、amber 边框=提醒、Badge variant outline/secondary 区分状态。
- **Tailwind v4 preflight 把 button 默认 cursor 改成 `default`**（v3 是 pointer，官方 breaking change）：全站按钮悬停不变手型，用户会当 bug 报（"鼠标停留没变样式"）。修复＝index.css 全局恢复，不逐按钮加 className：
  ```css
  @layer base {
    button:not(:disabled),
    [role="button"]:not([aria-disabled="true"]),
    label[for], select, summary { cursor: pointer; }
  }
  ```
  禁用态维持 default（语义正确）。把「可点控件悬停＝pointer、禁用＝default」写进项目 DESIGN.md 防回退。**2026-10 复核：上游 `index.css` 已自带此修复（base 层 `cursor: pointer`），新项目先核对再决定是否自加，别重复打补丁。**
- **冒烟断言**：`fontSize === '16px'`（防缩字回退）+ 关键按钮 `getComputedStyle(el).cursor === 'pointer'`（防 preflight 回退）。~~行高比 ≤1.5 断言~~ 随 2026-10-23 收紧条款删除作废。批量调字号层级时用占位符三步替换避免连锁命中（`text-xs→@@X@@` 先全部占位再统一落新值）。

## 6. shadcn DOM 的 E2E 选择器对照（Playwright，从 Element Plus 迁移时全换）

| 目标 | Element Plus 旧 | shadcn 新 |
|---|---|---|
| 确认对话框 | `.el-message-box` | `[role='alertdialog']` |
| 对话框校验错误保持打开 | 天然不关 | `AlertDialogAction` 的 onClick 收 event，**必须 `e.preventDefault()`** 才不关闭（否则空提交直接关框，断言永远看不到错误文案） |
| toast | `.el-message--success` | `li[data-sonner-toast]`（has_text 过滤） |
| radio 选中态 | `.el-radio.is-checked` | `[role='radio'][data-state='checked']` |
| checkbox | `.el-checkbox` | `label` 内 `[role='checkbox']`（click checkbox 本体） |
| 表格行 | `.el-table__row` | `table tbody tr` |
| Collapsible 分组头 | — | button 文本含计数后缀如「订单详情 API（20）+」→ 用 `page.locator("button", has_text="订单详情 API")`，**别加 `[role='button']` 属性过滤**（原生 button 无此属性，匹配 0 个超时） |
| 抽屉/Sheet 内容 | `.el-drawer` | `[data-slot='sheet-content']` 或按标题文本定位 |
| 输入框值断言 | eval input values | 同（`eval_on_selector_all("input", …map(e=>e.value))`）——受控 Input 的 value 不在 innerText 里 |
| `has_text` 定位陷阱 | — | `locator("div", has_text="已选字段").last` 会匹配到**标题 div 自身**（文本最短的包含者）导致断言取错元素 → 改断言计数（`已选字段（1）`）或用更精确的 class/结构定位 |

## 7. 排障顺序（本 session 两次假失败）

1. E2E 突然连片失败（JSONDecodeError/连接超时）→ **先 `curl /api/v1/health`**：外部 MySQL（如阿里云 RDS 共享实例）有间歇性分钟级超时，恢复后原样重跑即绿——不是前端/测试代码问题。
2. 页面白屏 → 浏览器 console 看 404 资源 → `curl -w "%{http_code}"` 探 assets URL → 挂载路径 or 产物缺失。
3. tsc 报路由类型错 → 先跑 vite build 重生 routeTree（见 §3）。
4. 构建产物没更新 → 确认 `emptyOutDir` 生效、FastAPI static 目录与 outDir 一致。
5. 全站按钮悬停无手型 → Tailwind v4 preflight cursor 变更（见 §5），全局 base 层修复。

## 8. 预览窗口尺寸规范（2026-09-29 用户拍板，长期 ToB 规则）

用户原话：「凡是涉及到 html、其它文件预览的视觉设计，都需要保证预览窗口尺寸必须半屏以上的大窗口，不能太小。」适用所有预览型 UI（模板 mock 预览、合同预览、批红 PDF 预览、发布结构预览…），跨模块长期有效。

**硬指标**：预览窗口宽 ≥ 50vw、高 ≥ 55vh，禁小窗。编辑态旁挂预览（三栏工作台右栏那种）给足高度（`min-h-[55vh]`）并额外提供「放大预览」按钮 → 近全屏 Dialog（`w-[92vw] max-h-[92vh]`，内容区 `min-h-[75vh]`）。

**⚠ shadcn Dialog 宽度覆盖坑（实测踩中，靠尺寸断言才抓到）**：`DialogContent` 内置 `sm:max-w-lg`，在 ≥640px 视口会**覆盖**你写的 `max-w-[92vw]`——首次部署后实测宽度只有 **40%**（约 32rem），不是 92vw。修：宽度类必须**同时**给 `sm:` 变体提权：
```
className='flex max-h-[92vh] w-[92vw] max-w-[92vw] sm:max-w-[92vw] flex-col'
```
只写 `max-w-[92vw]` 无效。Sheet（抽屉）不受此坑影响（无内置 sm:max-w），但同理给 `sm:max-w-[95vw]` 保险。

**判定边界**：「预览窗口」指展示渲染内容（HTML/PDF/JSON 结构）的窗口；**操作表单对话框不算**（如翻译表批量导入=填数据+确认冲突，维持 `max-w-2xl` 合理）。判据=窗口主体是「看内容」还是「填/确认」，后者不放大。拿不准时向用户点破判定（【待复核】）而非默默决定。**详情展示弹层**（列表收敛后看全属性）介于两者之间：只读详情用 `max-w-2xl` 级别即可，不必按预览窗口放大——它不是渲染文件内容。

**冒烟尺寸断言（防双向回退，加进 spa_smoke）**：真实建一个样本 → 打开预览 → `dlg.bounding_box()` 除以 `window.innerWidth/innerHeight`，断言宽 ≥0.5、高 ≥0.5：
```python
box = page.locator("[role='dialog']").first.bounding_box()
vw, vh = page.evaluate("window.innerWidth"), page.evaluate("window.innerHeight")
assert box["width"]/vw >= 0.5 and box["height"]/vh >= 0.5
```
样本数据放 `finally` 软删（`DELETE FROM tpl_file WHERE id=:i` + 对应 audit_log 行），避免每次冒烟堆积。清单发布预览这类「库空就测不了」的断言写成条件式（`if pub_btn.count(): … else: 跳过`），别因前置数据缺失把冒烟卡死超时。
