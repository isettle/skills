# Spec Kit Preview 低保真线框套件（项目A 验证过的可复用配方）

生成静态多页线框原型时使用。完整可运行副本在
项目A 仓库的 feature 目录 `preview/`，
新项目直接拷 wireframe.css 过去再写页面。

## 目录结构

```
specs/NNN-slug/preview/
  PREVIEW.md          # 工作流铁律 + 页面↔spec溯源映射表(页面|驱动模块|驱动段落|状态)
                      # + 同步操作规程 + 原型层决策日志(不进spec的决策记这里)
  wireframe.css       # 灰色线框样式，见下
  index.html          # 首页：按 US 分组列出页面卡片(每张带FR编号) + 建议走查路径 + 反馈方式说明
  <page>.html         # 每个 P1 界面一页
  todo.html           # P2/P3 占位页：列驱动段落+计划页面拆解，保证映射完整
```

## wireframe.css 核心（约60行，灰系无设计）

关键 class：
- `.topnav` 深色顶栏：所有页面共用的页间导航 + 右侧 "spec vN 驱动 · 日期" 版本标注
- `.card` / `.card.dashed` 卡片容器；`.row`/`.col` flex 布局
- `.inp` 输入占位，`.inp.locked` 灰底=只读/派生字段（如派生总价、锁定币种）
- `.btn` / `.btn.primary` / `.btn.disabled`（disabled 用 title 属性放"人话原因"，演示 FR 双重拦截/置灰规则）
- `.tag` 溯源小标签（右上角小字，内容如 `FR-013` `US1` `SC-006`）——**每个关键控件必带**
- `.chip` + `.chip.ok/.bad/.warn` 状态胶囊（绿/红/黄）
- `.imgbox` 斜纹灰底占位图（公章预览、上传拖拽区、原件页图）
- `.field-y` 黄底=低可信度/冲突字段；`.frame-hi` 绝对定位橙框=识别位置高亮演示
- `.note` 虚线便签=规则说明；`.trace` 蓝底块=页尾"本页驱动段落"清单（列出全部 FR/US/SC/Edge 引用）

## 页面骨架

```python
def page(title, body):
    return f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="wireframe.css"></head><body>
{nav}<div class="page">{body}</div></body></html>"""
```

每页正文结构：`<h1>标题 + US标签` → `.sub`(场景/虚构示例声明) → 若干 `.card`（每卡 h2 带 FR 标签）
→ `.trace` 驱动段落汇总。**示例数据全虚构**（公司名带"（虚构）"、单号 SO-2026-xxxx），
遵守用户文档规范与零黑话 FR。

## 批量生成助手与残留自检（第二项目 项目B 验证）

- 页面生成用常驻 helper：把 `nav()/page()/trace()/T()`（页骨架+当前页高亮+溯源标签）写成一个 scratch 目录里的 .py 模块，每段生成 execute_code 里 `sys.path.insert` 后 import——比每段内联定义稳（页集合/标签格式单点）。
- **先定跨页共享的虚构数据基线再写页面**：实体行数/关联编号/异常项（如「设备 6 行↔同步计数设备 4+失败1↔预警 4 条↔列表离线 2」）以注释字典形式固定，每页取数都引基线；任何一页重写后必须重算与其对平的其它页计数（计数断链是最容易被用户看出「虚构」的点）。
- **f-string 嵌套引号不展开陷阱**：外层字符串里嵌的 `{T(...)}` 表达式若处在未加 f 前缀的片段中，会以字面量漏进 HTML。批量生成收尾必扫残留：对全部页面 `re.finditer(r"\{[a-zA-Z_][^}]*\}", t)`，命中即 replace 修掉——肉眼几乎看不见。
- 复用他项目 wireframe.css 时，本页新用到的 class 先 grep 确认存在再引用（当前页高亮 `.topnav a.on` 就是拷贝后补写进 css 的）；新状态样式（如未处理整行标红 `tr.red`）追加进 css 并在页面注释其 spec 依据——颜色之外 MUST 并排文字标识（无障碍+零依赖单通道）。
- **多轮迭代改已生成页面：patch 锚点逐字取自磁盘现文，不信会话里的生成字符串**——首稿生成后页面可能已被就地 replace 过（版本标注/计数修正），用记忆中的 f-string 当锚必 no-match；先 `grep 关键字 页面` 拿原文行再 patch，改完跑闭合配平。整页语义变了（列表→预警中心）直接整页重写重生成，不叠补丁。版本号标注（spec vN 驱动）用一次 glob 批量 replace 扫全部页面，重写页自带新标。
- 全 P1 项目可以不建 todo.html，但 PREVIEW.md 要写明 US 覆盖核对结果（spec US 计数 == 映射表覆盖数，无占位缺页）。

## 内容技巧（项目A 验证）

- 用线框直接演示难点交互的"两个状态"：审查页同屏放"有红项→盖章禁用"与"模拟全绿→可盖章"，
  省去 JS；币种锁定用 `.inp.locked` + tag 说明。
- 状态机用 `.statusbar` 一排 `.st`（done/cur/未来态）表达，注明"无回退、人工动作只有 N 个"。
- index.html 必带"建议走查路径"有序列表（按主流程串页），用户按序点即可走完 P1 故事。
- 生成后校验：直接跑 `scripts/check_preview_consistency.py <specs_root> <preview_dir>`
  （打包标签闭合、死链+导航集合一致、FR 引用有定义、spec 重复/泄漏/长行）。
- **差异/代码示例区的转义陷阱**（项目A template-edit 实际踩中）：演示 AI 改稿 diff 时，示例
  HTML 整体转义（`&lt;td&gt;`），但**本页面自己真实存在的包裹标签绝不能连带转义**——
  把真 `</b>` 写成 `&lt;/b&gt;` 会让标签配平检查报 mismatch，肉眼很难发现；写完必跑闭合检查。
- **原型措辞用 spec 原文词，不发明术语**（项目A 实例：spec 写「显著标注」，原型草率写「水印」，
  零虚构双向检查把自造词抓了出来）。评审检查是双向的：spec 元素→原型有落点，原型措辞→spec 有依据。
- **发布结构/汇总块也要与页面演示行数对平**：三向对齐不止列表↔详情——「红项 5/黄项 2/参考 1」
  这类结构化内容示例必须等于同页实际勾选行数（项目A 首稿写了 12/5/8 与左栏 8 行矛盾，自查抓到）。
