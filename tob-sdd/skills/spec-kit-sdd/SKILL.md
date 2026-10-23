---
name: spec-kit-sdd
description: 'Use when working in a spec-kit (specify) SDD repo.'
metadata:
  hermes:
    tags: [spec-kit, sdd, specify, spec-driven-development, scaffolding]
---

# Spec Kit (SDD) 规范流程项目

GitHub Spec Kit spec-driven development. User's standing preference
(Sep 2026): new projects follow this flow. First real use:
一个内部 ToB 项目（代号「项目A」）。Commands/pitfalls below are verified.

## Init recipe (macOS, uv-installed CLI; verified on 0.15.2, re-verified clean on 1.2.0 — upgrade first, see below)

1. `specify check` — lists agent integrations; **Hermes Agent is supported**.
2. Existing repo (has .git, may be empty):
   `cd repo && specify init --here --force --ignore-agent-tools --integration hermes`
   Scaffolds `.specify/` (templates/, scripts/bash/, memory/constitution.md,
   workflows/) + `.hermes/` slash commands (`/speckit-*`).
3. New feature: `bash .specify/scripts/bash/create-new-feature.sh --json "desc"`
   → creates `specs/NNN-slug/spec.md` from the bundled template.

### Init pitfalls (both hit in practice)

- **Slug generator strips non-ASCII** (bundled scripts ≤0.15.x): a Chinese-only
   description yields an EMPTY slug (`specs/001-/`). Fixed upstream in 1.1.0
   (Unicode feature names preserved) — but old projects keep the broken
   bundled script until `specify init --here` re-scaffolds; until then pass an
   English description or manually `mv specs/001- specs/001-english-name`.
- **Repo with zero commits**: the script's `git checkout -b` silently fails
  (no HEAD) — NO branch is created. Commit the scaffold first, then
  `git checkout -b NNN-slug` yourself.

## CLI upgrade & release-note review (verified 0.15.2 → 1.2.0)

### 引入时间线（用户会问「X 功能哪个版本引入、为什么那时」——按此答，勿凭记忆）

workflow 引擎=0.7.0；`bug-assess`=0.11.2；`assess` idea 评估扩展=0.13.0；`feature-assess` 自动装 Spec Kit 的 workflow=0.16.5；**bugfix+assess 转正为第一方 bundle=1.0.9**；workflow slots=1.0.5、每步 integration 配置=1.0.6、精确版本 pin=1.1.0-1.1.1、执行树组合=1.1.3、内置 GitHub step=1.2.0。答「为什么」的标准论证：0.x 后期以扩展/workflow 实验形态落地 → 1.0.0 先稳核心流程 → v1.0.9 统一转正为可 `bundle add` 的第一方制品；官方无原话的动机推断要显式标注为推断。

### workflow 子系统的操作纪律（详表见 sdd-speckit-research/references/workflows.md）

- 日常使用全程 CLI（`specify workflow search|add|run|resume|status`），只有写新流程或定制才碰 YAML。
- **定制一律写 overlay（`.specify/workflows/overlays/<id>/*.yml`），绝不直接编辑已安装的 `workflow.yml`**——`workflow update`/重装/`bundle update` 会覆盖改动，overlay 因在安装目录之外而跨升级保留。
- overlay 只能改 step 列表：改不了 inputs/元数据/表达式；step id 含 `:` 非法；引用不存在 step id 到解析时才报错；改 id/删 step 会断掉 paused run 的 resume 与下游 `{{ steps.x.output.y }}`。
- 官方不审计 workflow 的 `run`/shell 字段——装社区 workflow 前先读源码（可执行任意命令）。

- uv-tool install: upgrade = `uv tool upgrade specify-cli`; verify with
  `specify version` + `uv tool list`. Latest = PyPI JSON
  (`https://pypi.org/pypi/specify-cli/json`); changelog = GitHub API
  `repos/github/spec-kit/releases?per_page=40` — don't read every body, filter
  lines containing `feat(`/`feat:`/`Deprecat`/`⚠️` per release in one pass.
- **Upgrading the CLI does NOT touch existing project scaffolding**: a project's
  `.specify/` templates/scripts/slash-commands stay at whatever version ran
  `init`. Fixes/changes only reach a project after re-running
  `specify init --here`. So version-specific pitfalls in this skill may still
  apply to old repos even on a new CLI.
- Standing changes through 1.2.0: core `/speckit.taskstoissues` deprecated →
  `github` extension; `specify init --integration copilot` defaults to the
  **skills** layout (`--integration-options="--commands"` for old behavior);
  workflows gained unified execution-tree composition, slots, per-step
  integration config; `specify artifact` introspection + experimental MCP stdio
  server; catalog installs support exact version pins.
- Post-1.0 the project explicitly rejects semver stability promises — any
  upgrade can change bundled templates. After upgrading, re-diff
  `.specify/templates/spec-template.md` before running the 合规性判定 pattern,
  since its source-of-truth #1 is that versioned file.

## spec.md shape (follow the bundled template exactly)

- Header: Feature Branch / Created / Status / Input.
- **User Scenarios**: user stories PRIORITIZED P1/P2/P3, each independently
  testable & shippable (P1 alone = viable MVP). Every story:
  Why this priority / Independent Test / **Given-When-Then** acceptance
  scenarios. Plus an Edge Cases list.
- **Requirements**: FR-NNN as MUST statements (系统 MUST / Users MUST be able
  to). Mark gaps `[NEEDS CLARIFICATION: …]` instead of inventing.
- **Key Entities**: business-level attributes only — NO DDL, no column types.
  Exception: when the user hands over a CONFIRMED entity list (table names +
  attributes), carry those names verbatim — that locks the domain model at
  spec level; indexes/column types/migrations still belong to plan.
- **Success Criteria**: SC-NNN measurable + technology-agnostic.
- **Assumptions** + (when converting legacy docs) a **traceability table**
  mapping each story/FR group back to old PRD/SPEC sections.

## Discipline: spec = WHAT, plan = HOW

- **用户硬性要求（项目A 项目起，适用所有 spec 修改）：每次改完 spec.md，最后一步
  必须做两道核查，再向用户汇报。**

  **核查 A — 规范合规**（把不符合 spec-kit 规范的内容优化或删除）：
  - 实现层措辞：arrayJson/JSON/md5/svg/外键/关联表/DDL/字段类型/API路径/库名 →
    改业务语言（如「附件支持多文件，含文件名/地址/内容指纹」「相同内容自动去重」）。
  - `[NEEDS CLARIFICATION]` 是否清零或仍待用户拍板（拍板后必须转成正式 MUST）。
  - Key Entities 只留业务属性+基数，不写落地方式（外键/中间表结构）。
  - FR 是否都是 MUST 语句；SC 是否可度量且技术无关。

  **核查 B — 前后一致性冲突扫描**（用户 2026-09-22 定，与 A 同等强制）：
  每次 spec.md 修改后，逐条比对新旧内容、并跨模块（总纲+各模块 spec）找矛盾：
  同一概念两处定义不同、状态机/触发条件互斥、引用编号悬空（如「US1-场景14」已不存在）、
  动作归属两个模块（双头操作）、叙述时序与验收场景相反、FR 标签与所属故事优先级不符、
  某 FR 无任何验收场景覆盖、溯源表漏新增编号、**总纲全局数字常量与模块 FR 冲突**
  （实例：总纲界面铁律「主列 ≤5」 vs 用户拍板订单列表「主列 ≤6」——模块级覆盖后
  必须回改总纲条款或改成「以模块 FR 为准」，否则两处打架）。
  发现后**按复杂度分级**：
  - 低（措辞/引用/覆盖瑕疵、机械可推导）→ **自己判断合并修掉**，汇报里列一行「已修」。
  - 中/高（业务语义矛盾、需二选一、影响多模块或状态机）→ **必须列成表格交人工拍板**，
    给出证据（文件+条款原文）与建议修法，不得自行选择。
  拍板落地后要再跑一次断言式自检（逐条决策 → 关键词在预期文件中出现 / 旧措辞已消失），
  并同步低保真原型受影响页面。

  **用户两条指令冲突时（同轮/相邻消息，用户 2026-09-22 实例：先列 11 个必填字段、紧接着说“所有字段都可选填”）：以最新指令为准执行；被覆盖的旧指令内容不丢——降级写进 Assumptions（如“建议齐备清单，非硬校验，界面可提示不拦截”），并在回复开头明示冲突取舍（“若你本意是 X，说一声我改回”）让用户可一键推翻。绝不默默二选一、也不把两版都写进 FR 制造矛盾。
- No table schemas, API paths, or library choices in spec.md — those belong
  to `plan.md` (`/speckit-plan`).
- 状态机归属（用户 2026-09-22 确认）：状态枚举+逐转移明细表（含非法流转处理/副作用）写 plan Phase 1 的 `data-model.md`；spec.md 只锁枚举与流转规则（WHAT 层 MUST）；判别式=换技术栈后这句话还成立→spec，否则→data-model/contracts。
- 低保真原型/交互流程不进 spec.md：原型文件放 feature 目录（如 `specs/NNN/design/` 或本项目 preview/），plan.md 引用路径；spec 的用户故事只写业务语言的行为结果，禁止「点击 XX 按钮→跳转 XX 页」句式；纯交互迭代只改原型+记决策日志，只有业务规则变了才回改 spec。
- Converting an existing PRD + technical SPEC: strip implementation detail,
  keep requirements as MUSTs, fold acceptance criteria into per-story GWT +
  Edge Cases, keep the old docs in place as the design-detail source the
  plan phase cites.
- Grouping large FR sets into stories: P1 = the mainline journey that alone
  delivers value; P2 = modules depending on P1 data; P3 = config/admin and
  cross-cutting concerns.

## US 粒度、属性读写边界与字段填写规则（用户 2026-09-22 两次拍板，最终规范）

- **CRUD 不拆成多个 US**：US 是“可独立交付价值的用户旅程”，不是功能分解。
  主 US 的验收场景盖全增/查/改，删除/作废归状态防护 US（项目A：US1 场景1~8 + US1c）。
- **spec.md 只允许官方模板章节**（User Scenarios / Edge Cases / Requirements
  (Functional Requirements + Key Entities) / Success Criteria / Assumptions）。
  读写边界与字段填写规则**不得用独立表格/自造 H3 章节**（矩阵、填写规则表都被
  用户否决），必须转写为 FR-MUST 条目收进 Functional Requirements 的粗体分组里：
  - 字段填写规则 → FR（如 项目A FR-004b 必填/选填/可后补、FR-006a 行内必填）
  - 前置条件 → FR + 配套验收场景（如 FR-004c 通知签署前须≥1台车挂物流 + US1 场景8）
  - 读写边界 → FR（如 FR-006b：全量联合视图默认只读，逐 US 列写权边界并引用依据 FR）
  - 列表查询规则 → FR（如 FR-004a 搜索字段范围/筛选/默认排序）
  - 层级红线不变：只写业务级规则（WHAT）；字段类型/长度/枚举/存储校验归
    plan 阶段 data-model.md。
- **实体/属性术语纪律（用户 2026-10-14 项目B 拍板，适用所有 SDD 项目）**：spec 中出现的任何实体/属性名词 MUST 在 Key Entities 有明确定义；Key Entities 的新增/编辑 MUST 经人工确认后落笔（用户直接给出实体属性清单即视为确认），代理不得静默增改实体或属性；原型 MUST NOT 出现 Key Entities 未定义的实体/属性。需求带新字段的固定顺序＝人工确认改 Key Entities → FR 落条款 → 同步原型。
- **改名/重命名纪律落地要全库扫**：一条命名整改（如表名单数化）执行时，MUST 对 specs/ 全部文件（含 research/quickstart/preview）grep 残留，只扫"主要三件"会漏（项目B 实踩：research.md 残留 4 处复数旧表名隔了两轮才发现）。
- **文档抓取协议排查顺序**：静态 curl 先试 `http://` 再 `https://`——部分国内站 https 返回 SPA 壳（空数据）而 http 版是服务端渲染、可全量抓表格（某平台文档站实证：https=壳、http=完整字段表；chunk bundle 逆向穷尽后靠 Owner 指正协议破局）。
  **审计执行五步（用户令「复查不符合纪律的地方」时的完整程序，别只做字面 grep）**：
  1. 收集定义集：从各 spec 的 Key Entities 段抽全部实体/属性名（execute_code，`open(path).read()`）。
  2. 扫两个面的用词：spec 非 KE 章节（FR/US/Edge）+ 原型 HTML 的 label/button/th/状态词（正则取 `.{0,15}(属性候选词).{0,15}` 上下文行）。
  3. 逐个回①找定义；**无定义的处置只有两条路**：措辞折回已定义词（零语义损失时自己修，如「停留开始时点」→「预警时间＋预警内容摘要」），或停下交人工拍板「扩实体属性 vs 定为机制不入实体」——**不得自选**。判据：界面要显示该状态值（如列表显示「临时锁定」行）而实体无承载属性＝扩实体；纯过程机制（锁定倒计时）可入 Assumptions。同时审计「全局约定里的实体（如审计日志）是否进了总纲实体关系总表」——只在约定句出现=漏网，用户没点名也要列入待拍板，这正是「用户不得静默改 KE」纪律对代理的镜像要求。
  4. 派生/状态属性要查**示例值自相矛盾**：如「停留时间=当前连续停留」而原型给离线设备填了进行中值——术语有定义但演示数据违反定义，同样算违规，改值并在 PREVIEW 决策日志记。
  5. 修完终检：禁词 grep 清零（B 组禁令记录句除外）+ `check_preview_consistency.py` PASS + **版本标注全页一致**（重写页带新标、其余页 `spec v\d 驱动` 批量 replace——重写页顶栏会被生成器旧标覆盖，残留必扫）。
- **data-model 纪律（用户 2026-10-15 项目B 三轮拍板 B21/B22/B23，plan 阶段产物）**：①表名 MUST 单数（user/order/alert_report，禁复数；REST 集合路径保持复数惯例，单数纪律只约束表名）；②表名与每个字段的 COMMENT MUST **严格＝** spec Key Entities 属性原文，MUST NOT 在 COMMENT 里夹带 FR 编号/判例/单位/实现注记（用户明确"comment 含 FR 编号＝错误"）；枚举值域、JSON 元素结构、批次/去重/软删/互斥辅助列另立「非实体属性列 + HOW 字典」节承接，溯源写在节内不进 COMMENT。③要加字段（尤其"原因/明细"类）＝零虚构红线：MUST 先人工判断→写 spec Key Entities→再落库；spec 无对应定义或含义模糊的 MUST NOT 编造命名/注释/字段，MUST 停下交 Owner；表名映射到动作词实体（"预警管理"这类非物名实体）由 Owner 定名（项目B＝`alert_item`）。④**状态类字段 COMMENT MUST 带具体枚举值、JSON 类字段 COMMENT MUST 带元素结构说明**；缺者固定两步：先补 KE 属性括注（语义归纳自既有 FR/Edge 文义、不新造），再回补 data-model 注释——B22（状态）与 B23（JSON）同法，属"COMMENT 溯源 KE 原文"纪律的自然推论：KE 原文不含值域/结构时，回补注释会撞 B21② 禁令，所以必须先改 KE。落地手法：data-model.md 附「非实体属性列 + 枚举/JSON 字典 + 溯源结论」三段，HOW 与"实体原文"物理分区。⑤**全局单位约定拍板**（如「时间数值字段无单位说明一律=秒」）三处落：data-model 头部全局列约定句、违反旧单位假设的列**改名去单位后缀**（stay_duration_minutes→stay_duration，单位进行内注非 COMMENT）、contracts 逐字段单位注同步；外部数据源非秒值统一收敛为「适配层归一化」横排条款（逐字段单位实测仍留联调项）；同时把 checklist 对应假设项半格勾关——全局约定一旦拍下，凡早期"单位=分钟"类假设注记都是清扫对象，逐处 grep「分钟|假设」改完为止。
- **FR 分组：按实体的增删改查行为分组（用户 2026-10-14 拍板，取代 2026-10-08「能力树分组、CRUD 只当组内检查表」形态）**：**FR 区 MUST 用粗体分组标题行分组，一个标题＝一个业务实体（或流程段）的完整增删改查集合**，FR 归入其操作实体所在标题下，组内按 增→删→改→查 排列；新 FR 归入现有组的对应行为段或新开组。**MUST NOT 以「页面/列表页/编辑页/弹窗」作 FR 主语**（换技术栈判别式：改弹窗后条款即作废），页面↔FR 对应关系放 PREVIEW.md 映射表与原型控件溯源标签，不进 spec——原型是 FR 的实现证据，方向永远 spec→原型。**新增 FR 一律取下一个全局未用编号、不再开字母后缀**（2026-10-08 拍板取代旧后缀制；存量字母后缀保留原号永不重编）。SC 是独立编号维度，不与 FR 绑定、不随 FR 加后缀，一条 SC 可验多条 FR。**流程/状态机型模块不套实体 CRUD 骨架**：签署双分支、快照冻结、裁决闸门这类核心条款不属于任何实体的增删改查格，此类模块标题改按业务流程段分组（台账→生成→签署→审查→入账），2026-10-14 的 CRUD 分组纪律只适用于主数据/档案/单据类实体模块。注意：本 skill 其余 pattern 中提到的「字母后缀子 FR / 拆字母后缀」均为 2026-10-08 前的历史形态描述，新写一律按分组标题+全局续号执行。
- **可读性收敛标准（用户 2026-09-22 拍板，适用所有 spec 写作与重构）**：
  - 单条 FR ≤3 行；超了就拆子弹列表（每条子弹一个子规则，如“枚举/前置/
    动作/副作用”分条），绝不写 200+ 字单行复合长句。
  - US 叙述 ≤3 行讲完旅程，尾部用“规则见 FR-xxx”指向 FR，不互相复述。
  - 字段清单类 FR 按角色分组（如“创建必填/选填可后补/派生只读/系统维护”）。
  - 模块定位用“> 流程链”引用块一行式表达，归属/硬约束各一条。
  - 重构后必跑断言：FR 定义集合无增删、逐 US 验收场景数不变、关键语义词
    grep 抽查无丢失（防收敛丢内容）。参考值：项目A 订单模块重构后最长行
    420→139 字、>200 字行清零。
  - 历次拍板只往原句追加从句是长句化的根因：每次修改后检查受影响 FR 是否
    超 3 行，超了就顺手拆子弹。
- **大 spec 的结构性可读性重构**（用户 2026-09-22 “重申人类可读性”触发，项目A 订单模块首用）：
  内容对但读不动时的五类病与修法（纯结构重构，内容零丢失）：
  1. 单 US 验收场景 >10 个 → 按能力域分组加粗体小标题（A.清单分母/B.四态裁决/…），
     组内连续编号，弃用 3a/3b 式插入编号（跨模块引用要同步改）。
  2. FR 顺序乱（字母后缀乱序）→ 按业务流程重排；用脚本按块重排+断言集合不变。
  3. Edge Cases >15 条平铺 → 按主题分组（录入/生命周期/生成/审查/配置/物料）；
     顺手查重（同一语义两条合并）。
  4. Assumptions 混杂 → 分两组：A 前提假设（可被推翻）/ B 已拍板决策记录（B1/B2…
     编号，用户确认过的设计依据留痕）。
  5. 文件头加「阅读地图」表（想知道什么→去哪看），大 spec 的导航入口。
  重构后必跑“零丢失断言”：FR 集合与数量不变、逐 US 场景数不变且编号连续、
  关键语义词清单 grep 全中、跨模块场景引用指向新编号。行数变多是正常的
  （拆行换可读性），指标看 >200 字行数与最长行。
- 原表格转 FR 后必须做转写完整性断言（逐条关键词 grep）防丢内容；原型控件
  （搜索框/必填星号/置灰按钮）必须能在这些 FR 找到依据。

## 大 spec 按模块拆分：用平级编号目录，不要内嵌子目录（用户纠正 2026-09-22）

用户权威规范：《spec-kit开发指南》（内部笔记）（8 产物：spec/plan/
research/data-model/contracts//quickstart/tasks/checklists/，每 feature 一个
`specs/NNN-slug/` 目录）。

项目A 拆分模式（已验证）：总纲留在 `specs/001-xxx/spec.md`（模块索引+全局约定+
SC总表+Assumptions），每个模块单独建平级目录 `specs/002-…/spec.md`。
铁律：FR/US/SC 编号全局唯一不重编，跨模块用编号引用；每条 FR 只在一处定义；
- 拆分后必扫陈旧路径引用（旧相对路径、`../spec.md` 指向）。

## “文档比对/审查”类需求的 spec 写法（项目A 外部合同审查，2026-09-22）

用户问“如何保证不遗漏”时，正确答案不是更强的抽取，而是反转分母：
- **清单由自己侧数据模型派生**（封闭集合、N 恒定可知），MUST NOT 写成
  “从对方文档里抽到什么就校什么”（抽取是开放集合，无法证明不漏）。
- **每项找全部出现位置**（同字段可能多处），全部等价才算一致。
- **四态裁决，禁止“未提及即通过”**：一致/不一致/对方未提及/对方内部矛盾
  （后三者皆为红项）+ 本侧为空时走“识别回填人工确认”。
- **覆盖率闸门写进 FR**：N/N 全裁决才能提交结论，否则按钮置灰+提示还差几项；
  报告显示“已裁决 x/N”。红项算已裁决（只阻后续动作），仅未处理的回填项算未裁决。
- **界面**：逐项列出但异常置顶、一致项折叠为计数（如“单价 15/15 一致”）。
- 依赖项要回写到提供方模块（项目A：工具模块 FR-031 对照表兼作字段字典、
  FR-033 翻译表加“反查译文”用途），两边互相引用避免双头定义。
- 原型演示数据里的 N 必须真能算平（分项相加=总数，折叠行相加=一致项数），
  否则用户一眼看出虚构。
- **可配置审查清单（项目A 2026-09-22 进阶）**：当“审什么/多严”需业务自定义时，
  新增一个配置实体（清单别名+字段项+审查级别）归配置模块，业务模块引用：
  - 级别三档：红项级（异常阻后续动作）/黄项级（知情放行·记报告）/
    参考级（仅展示·不裁决·不计入 N）——把“未提及=红”从全局硬规定变为可配。
  - 清单勾到字段定义级，分母 N 由业务侧按实际行数展开（字段×行数）。
  - 开始审查时冻结清单快照，后续改清单不影响历史（可追溯当时依据）。
  - 预置一份“全字段清单”作默认（不可删可停用可复制）；未选清单时入口置灰。
  - 注意：把关键字段标参考级会使它不参与裁决——这是配置责任，系统照清单执行，
    但界面应在选择处提示"本清单不含 XX 审查"，并处理 N=0 极端（弹提示不静默）。
- **清单升级「勾选自字段字典 + 零手输 + 结构化发布」形态**（项目A FR-048 评审重构，2026-09-22）：
  当清单字段来源改为上游字典实体（如 tpl_api 响应结构）时，五条配套条款一个别漏：
  ① 层级字段以点号完整路径书写、数组用 `[index]`（如 `order.cars[index].vin`），路径由勾选**自动生成、禁手打**；
  ② **全程只勾选零文字编辑写成 FR**（界面唯一文本输入=实体别名），动机明写：防错拼路径混进审查分母——
    喂给确定性闸门的配置项必须全勾选来源，这是"配置防错"的可 spec 化条款；
  ③ 配置实体对外 MUST 发布**「级别→字段路径集合」多集合结构化内容**（各集合=路径清单+字段元信息），
    下游按结构消费：含 `[index]` 的路径×实际行数展开、不含量 1 计——分母规则从"字段名清单"升级为"路径解析"；
  ④ 快照冻结对象同步升级为该结构化内容（消费侧条款同轮改，否则历史可追溯性断在中间）；
  ⑤ Edge 两条：上游字典被停用/删改致清单引用失效路径→清单编辑界面列出供勾除、开审前 MUST 先修正、
    不静默失效；复制出的自定义副本不自动跟随源字典更新（防隐式改口径）。

## AI 辅助文档审查的安全 spec 写法（项目A 外部合同审查，2026-09-22 用户拍板）

适用于“用 AI 审查/比对文档且绝不能出重大事故”的需求（合同、发票、订单单据、证书）：

- **三层架构，AI 只夹在中间且只能“加”不能“减”**：
  L1 确定性骶架（分母 N、归一化、算术派生，不经 AI）→ L2 候选召回
  （规则 ∩ AI 取**并集**，召回单调递增，AI 失灵只会少找不会错删）→
  L3 裁决+证据门。
- **证据回查门**：凡来源=AI 的候选，其原文片段必须能在文档文本层/OCR 结果中
  逐字命中，否则丢弃并记日志（杂幻觉值进不了裁决）；人工排除候选需选
  “证据不成立”+填理由+审计。
- **AI 判定一律不自动生效**（用户复议后采纳的最严方案，推翻了自己先选的
  “高置信度可自动”）：✅ 只能来自确定性比对或人工确认；置信度仅用于排序与
  提示；**系统不提供阈值/严格模式等放宽开关**（默认即最严，不给误配置留口子）。
  向用户提建议时：金额/编号类近似值（412,000 vs 412,500）易得高置信度，应直接
  建议最严方案并说明事故成本。
- **派生项自动追加**：总价=Σ单价×台数、小计、大写↔小写金额、三方计数互校
  （明细行数↔编号串接数↔正文所述台数）；派生值由代码算出不由 AI 推测；
  派生项不可被清单排除、级别最低只能降到黄项。
- **多位置全比对**：同一字段在文档多处出现（表格/正文/大写）全部列为候选，
  任一处不等即异常，MUST NOT 取多数、MUST NOT 只取与本地值一致的那处。
- **多语言三级固定顺序**：①本地术语库精确匹配（命中即确定性判定、不调 AI）
  →②库无才用 AI 语义建议（一律待人工确认）→③无法解析转待人工，绝不默认通过；
  人工判等价可一键存回术语库（知识库自增长，同类下次走确定性路径）。
- **降级与留痕**：AI 不可用→退回纯确定性模式，需 AI 的项转待人工、界面明示、
  分母 N 不缩小、闸门照常；审查全过程写入审计日志支持完整回放（不新增实体）。
- **异常后果分级 + 硬底线**：红项级绝对不可人工放行（只能驳回或改本地值，
  界面无放行入口）；黄项级知情放行但备注必填；参考级不裁决不计入 N。
- **零事故 SC**：写成可度量条款（放行后被发现关键数据不符且未拦的事故数=0；
  黄金集盲测关键字段召回率 100%；每条 ✅ 可追溯到“确定性比对”或“确认人+时间”）。
- **HOW 不入 spec**：模型选型、prompt、黄金集阈值、向量/规则召回实现全归 plan。
- **审查结果常需两份物料**（项目A FR-013h，2026-09-22 拍板）：①一键复制纯文本
  （摘要/计数/异常清单/勾稽算式，零黑话，可直接贴聊天工具/邮件发客户）；
  ②批注 PDF（在原件副本上按裁决上色：红=严重异常、黄=可放行异常、
  绿=已核对一致；同字段多处逐处独立着色不合并；未提及类无处着色→加注释框；
  不改原件）。要问清：绿色标什么（一致项 vs 参考级）、何时可导出（每次 vs 仅驳回）、
  是否留档（项目A 选不留档，可追溯靠审计日志）。原型演示数据必须跨区自洽
  （弹层计数 = 复制文本计数 = 折叠行相加，一处不一致用户就看出虚构）。
- **对外物料 vs 对内进度必须分离（用户 2026-09-22 追加拍板，先写的版本违反了它）**：
  审查/核对类产出的物料若定位是「发客户」，则 MUST NOT 含任何内部处理事项——
  待回填项、AI 待确认项、覆盖率 x/N、清单别名、AI 可用状态、置信度全都不进物料
  （理由：回填是完善本侧数据用的，不是给客户看的）。落地三处：
  ① 物料只计**已裁决**项（"已核对 122 处"而非 "122/125"）；
  ② PDF 中未裁决/待回填/待确认项**不着色不加注释**（但"未裁决绝不显示为绿"的安全语义保留）；
  ③ 内部进度不消失，只回到内部工作界面（审查弹层顶部）。
  同时给物料定**禁词表**（内部术语一律不出现，改说人话："共核对 N 处"），
  并把「全文不出现任何回填/待确认内容」写成验收场景与 Independent Test 断言。
  判断口诀：**这份东西会给谁看？给外部看的，内部待办一律剥离。**
原模块留占位指针（见 Transfer pattern）。新增编号自 2026-10-08 拍板后一律取下一个全局未用号并归入粗体分组标题（存量字母后缀保留原号，不再新开）。
红线（指南）：spec 内出现字段类型/HTTP/表名/框架名 = 写串了，挪去
plan/data-model/contracts。

## Rebuild pattern: spec v2 from a confirmed entity model (verified on 项目A)

When the user says "参考下面的实体属性与关系，重构 spec.md" with an entity list:

1. Read the current spec.md in full first; keep every story/FR that survives.
2. Add a **全局数据约定** section for rules stated as "所有实体都…" (soft
   delete + creator/timestamps, attachment arrayJson{文件名,地址,md5},
   money-as-integer-minor-units, derived fields not persisted) — state once,
   don't repeat per entity.
3. Rewrite Key Entities verbatim from the user's list (entity names like
   `order_car`, attribute names, cardinalities); append a 实体关系汇总 table
   (关系 | 基数 | 落地方式: 外键 vs 关联实体).
4. Propagate: renumber FRs grouped by entity domain, update each user story's
   wording to the new entity/attribute names, add per-entity acceptance
   scenarios the new model implies (e.g. md5 cache-hit for an ocr_log entity).
5. Entities in the OLD spec but NOT in the confirmed list: delete from Key
   Entities, move to Assumptions with a one-line rationale ("无商品目录实体：
   品牌/分类/规格直接录在商品行…") — never silently drop.
6. Real ambiguities the new model creates → `[NEEDS CLARIFICATION: …]` inline
   in the FR + a short numbered question list at the end of the reply for the
   user to rule on. (项目A examples: 数量 field vs SKU-unique rows; item
   price currency vs order currency for the derived total.)
7. Extend the traceability table with a new column mapping spec sections →
   the confirmed entity model; bump the header (Updated: date + v2 reason).
8. Verify programmatically: read the file back and regex-count every entity
   name + `NEEDS CLARIFICATION` occurrences. Do this via execute_code/read_file
   — a long shell one-liner for-loop trips the blocked-command parser.

## Integrate pattern: user hands over a raw state list → merge into spec.md (verified on 项目A 订单 6 态, 2026-09-22)

When the user says 「分析订单状态并优化 spec」 with a numbered state list (时机/操作/前提):

1. DIFF FIRST, never paste: read current spec.md + grep 总纲/旧PRD for the same states. Typical conflicts this surfaced in 项目A: existing FR-011 said「无回退」but list has 签署中→草稿 退回; 「仅草稿可删」 vs 作废前提「驳回、草稿」; list omits an old state (补充资料 → replaced by 合同签署完成); a derived state (完成=全部入账) mixed in as if manual-set; seal subject ambiguous (盖买家公章 vs US1 生成时套卖方公章).
2. Rewrite the status FR as: closed enumeration in one MUST + whitelisted single human rollback + 正向修正 (驳回→重签) declared NOT a rollback; then lettered sub-FRs, one rule each (a=推导态无人工入口且终态, b=退回前提条件, c=软删/作废规则+占用释放). Keep original FR number, don't renumber.
3. One GWT acceptance scenario PER transition AND per illegal attempt (作废被拒提示原因、自动流转无人工设置入口); update Edge Cases (审查后又改数据→以提交时点为基准; 客户签旧版回来→重新比对); Key Entities line gets the inline enumeration; Assumptions records 旧态取代 + 「逐转移明细表(含非法流转处理/副作用)plan 阶段进 data-model.md」.
4. Real ambiguity → inline `[NEEDS CLARIFICATION]` in the FR + numbered 待拍板 questions at reply end; plausible gap (驳回出口) → Assumption 明示默认值, don't block.
5. Verify: grep spec for 旧状态名清零 + NEEDS CLARIFICATION count; THEN grep the preview/ prototype HTML for the same stale state names — state-enumeration change invalidates prototype 状态条/时间线文案, regenerate affected pages (用户 2026-09-22 再次确认「spec.md 自动驱动原型变更」为固定规则，不等用户叫)。同步原型时：每个新增状态/分支要在列表页植入一条该状态的示例记录（含其专属操作按钮，如驳回单带「通知重签/作废」入口）并在 index.html 演示路径加一步——否则用户点不到新功能会质疑「没改动」；新用到的样式 class（chip bad/ok 等）先 grep wireframe.css 确认存在。用户 NEEDS CLARIFICATION 拍板后（如盖章方=人工选买/卖方），把决议同时落进 FR（转正式 MUST）、对应 GWT 场景、和原型控件三处，再清标记。

## Transfer pattern: move a whole feature (US+FR range) between module specs (verified on 项目A, 2026-09-22: US2/FR-015~021 订单→审核) 

When the user says 「X 功能迁移到 Y 模块」(often with boundary rules like 「扩展信息不影响合同签署」):

1. **编号随迁不重编**（扩展既有编号纪律）：源模块把 US/FR 段整体替换为占位指针（引用原文保留编号 + 迁往哪个文件），接收模块拿到完整原文（story 叙述、GWT、FR 定义、识别类 Edge Cases 一起搬），并在标题/小节标注「(date 自 X 模块迁入)」。
2. **负面约束要变成可验收条款**：用户顺带说的边界规则（如「扩展信息不影响合同签署」）→ 在源模块新增字母后缀 FR（FR-021a：MUST NOT 参与派生 / MUST NOT 作为前置）+ 至少一条 GWT 场景验证"缺了它照样走通"；接收模块对称写一条对照场景。SC 总表归属随功能改（总纲 SC 表 + 两个模块的 SC 引用行都要改）。
3. **受牵连的引用点清单（逐一 grep 旧归属句）**：总纲模块表/端到端主流程/编号纪律/溯源表、第三方模块的行为引用（例：tools 的 ocr_log「行为需求定义在订单模块」→改指审核模块）、preview/PREVIEW.md 映射表的"驱动模块"列、原型页面归属标题与 trace 标签。收尾跑交叉 grep：旧归属表述=0、新编号引用数>0。
4. **数据归属 vs 功能归属可分家**：实体属性仍挂原实体（order_car 扩展属性），写入/维护功能归新模块——在两边 Key Entities 注释里各写一句，避免读者以为实体也迁了。

### Patch 陷阱（本 session 两个真实踩坑）

- **大段 old_string 连带删行**：一次性替换多条相邻 Edge 时，把不相关的「客户合同 PDF 无文本层」也吞了（它属于 FR-013 不随 US2 迁移）。替换相邻多行时 old/new 必须逐行对齐带出保留项，改完立刻 grep 保留项是否还在。
- **markdown 表格行首 `|` 丢失**：patch 表格行时 old_string 少写/多写前导 pipe，diff 里出现 `|| US3…` 断行。patch 返回的 diff 必须逐行看，发现破坏当轮修复。
- **在既有小节「之前」插入新小节时，old_string=下一小节标题会被整段吞掉**（本 session 实踩：以 `## D8 通知…` 为锚插入 D9 全文，D8 标题没了，小节顺序变 D1..D7,D9 且 D8 内容悬空）。规则：new_string 结尾**原样带回**被锚点消耗的标题行（…新内容 + `\n\n## D8 通知…`），或干脆锚定上一小节的**末行**做追加。插入后立刻跑 `re.findall(r"^## (D\d) ")` 断言序列连续完整。
- **markdown 表格/追加型列表（决策日志、溯源表）「末尾加行」同根复发形态**：old_string 取最后一行全文、new_string 只写新行＝旧行被替换消失（append-only 工件丢史，本 session 实踩靠 diff 复查才抓回）。规则同前：new_string 必须**原样带回锚点行再追加新行**；对 append-only 日志类文件改完必 `grep -c "<被锚定的旧行首关键词>"` ≥1 断言旧行仍在。**跨会话持续复发（决策日志/HANDOFF bug 列表/spec 历史行三处）；append patch 返回的 diff 里若删除行包含被锚旧行，当轮立即恢复锚行再重跑断言，不留到下轮复查——本 pattern 同一条规刚在一轮内连吃两次（PREVIEW 决策日志 v52 被覆盖、HANDOFF bug11 被吞）。**

## US 审计与拆分 pattern（verified on 项目A 003, 2026-09-22：单一 US1(14 场景) → US1/US1a/US1b/US1c）

用户问「US 是否规范/一个 US 是否内容过多」时，按模板出体检表再动手：

1. **体检判据**：一个故事=一个可独立交付的用户目标；每故事 GWT 3–6 条为宜（14 条=超标信号）；每故事必须有 Why/Independent Test；P1→P2 梯度缺失（只剩单层 P1）常是功能迁移把全部 FR 堆进唯一留守故事的副作用。
   - **「是否有多个 MVP」判据**（用户问「USx 是否需要拆分」时）：US 内某条 FR 同时满足 ①独立可交付——US 主闭环不依赖它、它也不依赖主闭环 且 ②零验收场景覆盖 → 才是第二 MVP 候选；两判据缺一不可，命中后列【待复核】给用户两条出路（拆独立 US / 留下补场景），不擅自拆。
   - **场景数超标 ≠ 拆 US**：能归约为单一闭环（建单→录明细→派生勾稽，任一段单独交付无价值）时保持 US 不拆，改为给验收场景按实体加粗体分组标题（A 商品/B 订单/C 闸门/D 物流）；FR 区同理只做块级重组、编号与文字零改动——物理拆 US 会断掉原型与跨模块的 `USx-场景N` 引用链。
   - **重组脚本的守恒基线＝解析结果，勿硬编码手算条数**：条款块解析计数必含指针行/迁出占位行，比肉眼预期多；写「before==after」断言用开工前快照集合，脚本里 assert 期望数字先以首轮解析输出定基线（写死预估数会让脚本中止——中止是保护不是故障，此时核对解析清单而非改数字）。
   - **分组计数声明串是陈旧高发点**：「N 项按能力域分 M 组」类声明在场景增删后即过时；分组完毕必须断言声明数字==regex 实际计数。孤儿场景（内容与所属组名错位、悬在某组尾部）正是靠这条断言暴露——为它单立新组，并同步改原型 trace 标签里的「场景1~N（…M 组）」与 PREVIEW.md 决策日志。
2. **拆法先给用户选**（clarify，推荐项在前；本次用户选了更细的 4 拆方案）：拆出的故事用字母后缀编号（US1/US1a/US1b/US1c），绝不重编既有编号——跨模块与原型的场景引用才能保持可 grep。
3. **FR 补归属标签**：拆分后给每条 FR 定义行加 `[US1x]`（跨故事写 `[US1/US1c]`），并核对每条 FR 至少被一个故事覆盖——这是给 /speckit-tasks 的故事级追溯做准备。
4. **薄故事并入邻家**：太薄的（如入账=纯手工零校验切换）不单立 US1d，并入最相近的 P2 防护故事，并把该判断在回复里明示让用户可推翻。
5. **场景重编号的涟漪**：preview 原型里的 `US1-场景N` 引用、页面 US 标签、总纲模块表 US 列、溯源表、header Input 修订记录全部要重映射；批量替换用 python 脚本逐对 replace 并打印 miss 项，收尾 grep 旧编号清零。

## Convergence pattern: FR/US 长文收敛重构（verified on 项目A 003, 2026-09-22）

用户问「US/FR 字数是否过多、是否符合社区规范」时（用户偏好：收敛核心、不要过多字数分散注意力）：

1. **先出判断表再动手**：数量维度（FR 总数/US 数）vs 密度维度（单条长度）分开判。官方模板 FR 均 1~3 行短句；**单条 FR >200 字或单行 >300 字 = 超标信号**（项目A 实测历次拍板“在原句上追加从句”累积出 FR-011/013 单行 300~420 字）。US 叙述与 FR 大面积重复 = 稀释注意力，同样超标。结论先给用户（哪超标哪正常），不要默默重写。
2. **重构手法（内容零丢失只改版式）**：长复合句 → 子弹列表（一子句一弹）；字段类 FR 按“创建必填/选填可后补/派生只读/系统维护”分组；US 叙述收敛到 2~3 行旅程 + “规则见 FR-xxx”指针（US 讲旅程、FR 讲规则，不互相复述）；Edge Cases 每条砍冗余从句。模块定位改流程图式一行链。
3. **防丢内容断言（execute_code，重构后必跑）**：①FR 定义集合 == 重构前期望清单（missing/多余都报）；②每 US 验收场景数与重构前一致（逐 US regex 计数）；③关键语义词抽查清单（20~25 个：如“全局唯一/双重拦截/默认卖方/基准永远=当前数据/软删除/NEEDS CLARIFICATION”）grep 存在性；④最长行/超 200 字行数前后对比；⑤全库 FR 无重复定义+泄漏词扫描。语义等价替换（如“永不直接入库”→“MUST NOT 直接入库”）允许但要在汇报里明示。
4. 其余模块同样超标时，主动提出按此标准一并重构（用户通常会同意，但等拍板）。

## Branching pattern: 单一流程拆双分支（verified on 项目A 签署双分支, 2026-09-22）

用户说「流程重构为两条分支：①…②…；总之<一句话原则>」时（项目A：我方出合同免审查 vs 外部合同必审+回填）：

1. **先抽共同段**：把用户两条分支描述里的公共前缀/后缀（建单录明细、后续资质审核）归为共同段，只让差异段进分支条款；用户末尾那句「总之…」是分支判别的业务本质（如“我出的不审、别人出的要审+回填”），写进 FR 开头作为区分依据。
2. **编号不重编**：新分支故事用小数后缀（US1b-2）；受影响 FR 拆字母后缀（FR-013 → 013 改分支二专属 + 013a 分支一确认动作 + 013b 回填规则）；每条字母 FR 开头标注「（仅分支一/仅分支二）」。
3. **状态机 FR 显式写分支路径**：枚举不变时也要逐分支列出流转链，并明说哪个态某分支不经过（项目A：分支二不经过“签署中”、分支一不产生驳回态）——否则 plan 阶段会自行脑补。
4. **派生决策点列表必交用户复核**：分支拆分必然带出用户没说的状态机细节（新态是否复用、回填是否需人工确认、全绿前置是否含待回填处理完、两分支产物不一致时是否校验、分支间切换路径）。做法：按常理定默认值落地，回复末尾用编号列表（1~5）明标「我按常理定的，请复核，有偏差说编号」——不阻塞交付也不静默自作主张。
5. **US 拆分后场景号会变 → 跨模块 `USx-场景N` 引用必须重新 grep**（项目A 实例：US1b 从 6 场景重写为 4 场景，audit 模块的「US1b-场景6」悬空）。收尾扫描正则 `US\d[abc]?(-\d)?[- ]场景\d+` 逐个验证目标存在。
6. **原型侧重写而非补丁**：分支类变更把受影响页重写为「双分支对照」布局（各分支步骤条+入口按钮+分支对照速查表：入口/经过状态/审查/驳回态/产物差异逐行对比）；所有引用旧单分支文案的页（详情操作区/列表行按钮/工作台丢物料分流/index 走查路径）逐一 grep 旧关键词同步。

## Field-evolution pattern: 双用途字段 / 条件必传附件 / 跨模块闸门（verified on 项目A 双地址+专用合同附件, 2026-09-22）

用户给字段/附件提「默认同步可独立改」「某条件下必传」「必须在 X 环节前完成」类需求时：

1. **双用途字段**（同源默认值、各自业务用途，如 目的城市/仓库[结算分军用] vs 发货目的城市/仓库[资质审核用]）：默认值规则+两字段各自用途写进 FR；用户若要求「查看时有字段提示」，把用途提示本身写成界面 MUST（悬停/副文案），原型列头同步加 ⓘ 提示——防混用是这类字段的头号风险。
2. **条件必传附件三要素**：触发条件（哪个字段≠哪个字段）、完成时点（MUST 在哪个环节之前）、豁免条款（不参与哪些流程，如专用合同不参与签署审查）。**定义与执行分家**：规则 FR 在数据归属模块（FR-004d 订单），执行校验在下游闸门 FR（FR-023 审核拦截），两边互相引用编号。
3. **事后触发 Edge 必写**：下游流程已启动后条件才变为触发（建证后才改两港）→ 警示条+拦下一状态动作（补传前不可提交申请），不追溯作废已完成动作；条件反向解除（改回一致）→ 必传标记解除但已传附件保留。
4. **新增黄项/警示类别 → 同步跨模块聚合器**：北极星屏类聚合 FR（项目A FR-046 黄格清单）+对应 US 叙述+原型黄格表（行+计数+来源统计）三处一起改，漏一处=新类别在聚合屏永远不可见。
5. **原型示例数据自洽扫描**：新规则上线后检查现有示例单是否违反新规则（项目A：示例单两港改不一致→触发必传→workbench 上该证的「提交申请」亮按钮变成不可达动作，违反 FR-047）。处理技巧：合规路径换一份干净示例数据，违规那份**显式转为黄格行/置灰态演示**——正反两面都成教材，别默默改数据掩盖冲突。
6. **断言误报教训**：语义断言用长短语（如「补传前该证不可提交申请」）易因措辞差异假阳性报 ❌；出 ❌ 先 grep 实际原文确认是真冲突还是断言词不匹配，再决定修 spec 还是修断言——不要把误报当失败报给用户。

## Split pattern: spec.md → module folders (verified on 项目A v4, 2026-09-22)

When the user says "拆分 spec 为多个文件夹，按模块拆分为 X/Y/Z":

1. Ask/derive module boundaries from the user's grouping (项目A: customer /
   order[含物流行] / fulfill[含发货]  / tools[模板翻译日志管理员]);
   横切 FR（通知/审计/附件/激励/零黑话）归入 tools 模块。
2. Root `spec.md` becomes the 总纲 (master index) and keeps ONLY: header,
   业务背景, module table (目录/覆盖范围/US/FR段), 编号纪律, 全局数据约定,
   跨模块端到端主流程, 实体关系总表, SC 总表(唯一权威), 全局 Assumptions,
   总溯源表. Module specs reference the master, never copy it.
3. Each `specs/NNN-slug/<module>/spec.md`: header with **Parent**: `../spec.md`,
   模块定位一段话, its own User Stories (可拆分编号如 US6a/US6b), FR 原文迁移,
   Key Entities 子集, **与其他模块的关系** section (显式列出跨模块引用),
   SC 引用编号, 模块 Assumptions, 模块溯源表.
4. **编号纪律（写进总纲）**: FR/US/SC 全局唯一，拆分不重编号，跨模块直接引用编号。
   每个 FR 只在一处定义；行为归主模块，实体可归另一模块（项目A 例：FR-017 行为定义在
   order，ocr_log 实体在 tools）——tools 侧改成引用句而非第二个 `- **FR-nnn**:`
   定义行，否则重复定义。
5. 副作用红利：编号不变 → 低保真原型的溯源标签零冲击，页面不用重生成；只需更新
   PREVIEW.md 映射表（加"驱动模块"列）并记录决策日志。
6. Verify programmatically after split (execute_code, not shell one-liners):
   - FR 定义扫描: regex `- \*\*(FR-\d{3})\*\*: ` across all module files →
     defined set == expected full range, missing==[], dup=={}.
   - Every FR definition line contains MUST (v3 遗留的无MUST FR 在拆分时一并修：
     把"X 为 5 态"改写成"X MUST 为 5 态"等，不改语义).
   - Leak-word scan + NEEDS CLARIFICATION count per file (拆分暴露的新歧义 →
     新增 NEEDS CLARIFICATION 并在回复末尾列出待拍板, 项目A 例: 客户多银行账户合同取数用哪个).
   - US coverage across modules == original US set.

### Pitfall: read_file dedup in batch verification

Re-reading a file already read this conversation returns
`{status:'unchanged', content_returned: false}` with NO content key →
KeyError in dict comprehensions. For batch cross-file verification use plain
`open(path).read()` inside execute_code instead of hermes_tools.read_file.
同一工具返回还带 `行号|` 前缀——凡拿它的内容做**锚文本匹配**（Python `str.replace`/`assert text.count(old)`）必因前缀与真实文件错位而 MISS，改动静默不落地；文本替换一律 `io.open(path)` 直读盘。相对路径按会话 cwd 解析，手动拼接易出现双目录段（`backend/backend/…`）FileNotFound——execute_code 里读写文件统一绝对路径。

## Master-data（档案/主数据）模块的 spec 完备性清单 + 优先级提升 pattern（verified on 项目A 客户模块, 2026-09-22）

档案类模块（客户/供应商/物料/员工）的 spec 天生"看起来简单"，但缺这几条就没法出原型、
也没法被下游引用。用户说"这个需求比较简单，把原型根据 spec 驱动出来"时，**先按清单补 spec，再画原型**
（否则原型上的搜索框/删除按钮全成无依据虚构，违反零虚构铁律）：

| 必备 FR | 内容 | 项目A 对应 |
|---|---|---|
| ① 列表查询 | 关键词搜索范围（**跨子档案**：主表+1:N 子表的哪些字段）、筛选项、默认排序、主列 ≤6+次要列收展开行 | FR-001a |
| ② 字段填写规则 | 档案期全选填可存草稿 / **被下游引用前**的闸门（哪些字段这时才变必填）/ 空值显示占位（"（未命名客户）"标黄）/ 重名不硬拦只提示 | FR-001b |
| ③ 业务状态 | 启用/停用（默认启用）；停用后不进新建单据的选择列表、历史单据不受影响；停用须备注必填+二次确认+审计 | FR-001 |
| ④ 引用保护 | 已被下游引用的主档与**每个子档案**都不可删，提示改停用或先让下游改选；无引用者删除=软删可恢复 | FR-001/002/003 |
| ⑤ 下游取数关系 | 显式列出"下游哪个动作取本模块哪个字段 + 缺项时谁拦"（一节只读说明即可），双向引用编号 | 客户 spec「与其他模块的关系」 |
| ⑥ 默认指针 | 主数据实体常携带「默认×」指针属性供下游单据预填（如默认联系人账号/默认银行账户，详见下方专节） | FR-001 字段 + FR-002/003 默认属性 |

**「默认」有两种形态，用户说「默认X」先问清存哪（项目A 用户纠正 2026-09-22）**：我把「给客户默认一个账号和银行账号」实现为"取第一条启用记录"的派生预填规则，用户纠正——默认是**客户实体上的指针属性**（默认联系人账号、默认银行账户，指向本实体子档案记录）。指针形态的完整条款包（写 FR 一条别漏）：
- 指针挂在**主实体**上、在主实体详情页维护，MUST 只能指向本实体自己的启用子记录；子记录本身无"默认标记"字段——行内「设为默认」按钮改的是主实体指针，表尾注明。
- **被指针指向的子记录不可删除**（与"被下游引用不可删"并列的第二条引用保护），提示须先改指向。
- 指针所指记录被**停用**或未设置 → 下游预填空+提示，MUST NOT 自动漂移取下一条（隐式再推导会让"默认"含义漂移、用户无法预期）。
- 预填值仍可改选并存为单据属性（下游"合同=单据伪属性"一致性不被破坏）。
- 改形态后 grep 旧措辞（"第一条启用"）清零；例外：Assumptions 决策史里"修正我前案 X 的误读"是有意留痕，断言要允许这种历史引用命中。
- **主数据角色中立（同轮纠正）**：客户/供应商类档案 MUST NOT 区分买方/卖方类型——角色只在单据引用时产生（同一客户可为某单买方、另单卖方），默认属性与角色无关、归实体自身。下游"取哪一方的默认"（如账户预填取卖方的默认）是消费模块的映射决策：规则定义在主数据模块、映射写在消费模块 FR 并标【待复核】交用户。

**冲突判据（本次实际抓到）**：spec 的 Edge/FR 写了某处置动作（"提示改为停用"），
但 Key Entities **没有承载该状态的字段** → 停用无处可存。补状态字段时必须同时写明
**业务状态字段 ≠ 数据层软删除**（两个独立机制：停用可自助恢复、软删需管理员恢复），
否则实现阶段会二选一合并掉。

**优先级提升 pattern**（用户说"提升 X 模块优先级，因为没有它主流程走不通"）——五处联动，漏一处就不算提升：
1. 模块 spec：`(Priority: P3)` → `P1`；**Why this priority 重写为依赖论证**
   （列出下游哪些 FR 依赖本模块，如订单 FR-004/012/013/043），并交代原低优先级理由
   （"种子数据顶替"）为何只适用开发期。
2. 总纲模块表：US 列标注 P1 + 提升日期与原因。
3. 总纲新增**交付顺序条款**（哪些模块先行/并行、为什么、谁在最后）。
4. 总纲端到端主流程链：把该模块写进共同前段并注明"P1 前置：下游哪些数据来自此"。
5. 原型 index.html：新增该模块卡片区**置于主流程卡片之前**，走查路径加"第 0 步"，
   占位页 todo.html 的 US 范围相应收窄。

**模块级三档定序（批量重排所有模块优先级，项目A 2026-09-24 用户拍板：工具+客户=P1→订单=P2→审核=P3）**——是上面单模块提升的批量版，四点不同：
1. **正则批量改 Priority 必须收尾枚举验证**：用 `### User Story (\S+) -[^\n]*\(Priority: (\w+)\)` 逐模块 dict 映射改写；本 session 首轮锚点把 "US 1" 误写成 `"1 "`（多一个空格）导致 5 条只改掉 2 条且**静默无报错**。规范：改完立刻正则提取全库 `(模块,US,Priority)` 三元组打印成终态表，断言各模块优先级集合==预期（越界=0），别信替换调用次数。
2. **Why this priority 要按新序重写论证**，且解决"降级模块仍是业务主线"的话术矛盾：订单降到 P2 但其 Why 仍写"业务主线"——补一句「主线≠先交付，前置配置先行」；升到 P1 的模块，Why 里与新序矛盾的旧论证（如工具的"依赖订单模块数据"）必须同轮改掉（新论证：P1 期凭 mock 建模板，与订单联调落在 P2 期）。总纲交付顺序条款明写「本条取代 <旧日期> 的旧表述」。
3. **模块级 P ≠ 模块内所有 US 强制同档**：跨切/非阻塞性子故事（项目A US7 人文关怀）可维持原 P3——主动向用户点破这个取舍并留"要升说一声"的口子，不静默拉平。
4. **原型卡区按交付序物理重排**：index.html 各 card 块切段（记录每块与其 h2 标题）→按新序拼回（断言 permutation 合法）→标题改标"P1 · 交付第①批"等批次语；占位页内各 US 卡的括号 P 级同步。登记点：各模块修订史加一行定序记录、溯源表加行、总纲模块表 US 列标注。
5. commit message 把本轮全部评审主题列全（含**事故如实记录**——本 session 把 patch 锚点误用丢段又重建的事写进了 commit 正文，让远程 HEAD 的历史可信）。

## 引用+快照 pattern：主数据字段在业务节点冻结快照（verified on 项目A 订单 FR-004e/050, 2026-09-22）

用户说「实体 X 要含关联实体的主键引用」＋「<某节点>完成后生成可审计快照，防止档案改动污染老单据」时（项目A：订单买方/卖方/联系人/指定银行账户四字段存主键；每次签署完成自动快照）：

1. **时序边界 MUST 写明**（否则与既有「审查基准=当前数据」条款自相矛盾）：节点**前**按引用实时解析主数据（档案一改在办单据立即可见）；节点**时**整单冻结快照；节点**后**一切下游读（详情展示/重新出具/派生单据）MUST 读快照，档案改动不得追溯。
2. **快照条款五要素**一条别漏：触发（每次节点动作各一版，驳回重做→v2 累积、旧版保留）/ 内容（单据字段+所引档案解析值+明细行全量，当时时点）/ 生效范围 / 可审计（只读不可改删、界面标「快照·时点时间」、生成事件进审计日志）/ 纠错路径（错误不改快照＝备注+审计说明，不给实现留第二改法）。
3. **快照的真实成本＝新实体**，登记点一个不漏：Key Entities（第 N+1 实体）、编号纪律已用范围（FR-001~049→050）、总纲关系表+模块表 FR 范围、被引主数据模块加"快照衔接"一句、下游模块（资质/审核类）读法改"经快照"。**实体计数常量的扫描必须用措辞正则扫全库**（`实体总数|维持 14|第 14 个|14 个实体`），它不只出现在总纲实体清单——项目A 实测漏改点藏在总纲 AI 底线条款句尾与 tools 模块 Assumptions 两处（"实体总数维持 14"在实体变 15 后隔了一轮才靠措辞扫描抓到）；"第 N 个实体"作为**加入时的时间序历史**可保留，全局计数常量必须更新。
4. **用户措辞「包含关联实体所有属性」常是误说**（项目A 连发两订正为"属性主键"+快照）：若按字面"复制全部属性进单据"与既有「MUST NOT 把对方属性复制进单据」拍板冲突，先冲突呈报再动手；以最新指令为准（既有规则）。
5. **表格 patch 陷阱**：同轮两个 patch 以同一行为锚点插表格行会造成重复插入（项目A 关系表实际踩中）。表格 patch 收尾必用 `collections.Counter(首列文本)` 查重。
6. 原型联动：演示时间线里的计数（"审查 x/x"）要与审查页 N 对平（本次顺带修 135→125 旧遗留）；快照版本号要与事件发生次数自洽（示例单只签过一次＝v1，别写 v2）。

## 实体中途重构 pattern：按用户评审把既有实体改为新模型（verified on 项目A 005 tpl_var→tpl_api, 2026-09-22）

用户评审 spec 时说「X 实体属性重构为 Y」并给新属性（项目A：模板对照表从变量级改为 **API 级**：API 标识(可用 URL path)+响应结构；tpl_file 追加「所用对照表集合」多选属性形成 N:N；创建流程改三步向导）：

1. **重构要连带语义角色**：旧实体可能兼任其他模块的数据源（项目A：对照表兼作外部合同审查的字段字典 FR-031/013c）。两边定义同轮改写，并 grep 全库旧实体名与旧属性措辞逐个改。
2. **旧名保留白名单**：改名后旧实体名全库清零，但允许四处有意历史留痕——Input 实体清单（标注「tpl_var→tpl_api」）、修订史、Key Entities 的「(原 X 重构，日期)」、溯源表「旧→新」注记。断言按白名单放行，严格清零会误删决策史。
3. **内置种子数据条款**：用户要求「上线前初始化一批内置数据」→ 写成 MUST：内置哪几份（项目A：订单详情/订单商品/订单物流 3 个 API）、内置项不可删（可复制后改）、内置项内容与实际不符＝配置数据修正（可编辑不可删）。与审查清单「预置全字段清单不可删可停用可复制」同构，可合并成一条「配置实体预置数据」纪律。
4. **用户需求自带 HOW 示例（如「例如 Jinja2」）**：spec 只锁能力 WHAT（四类占位：单值/语言标记/数组循环/命名空间消歧），明写「具体语法形式由 plan 阶段引擎选型决定，MUST NOT 在 spec 锁定引擎」；但把「编辑界面 MUST 提供与引擎实际行为一致的语法规则参考（说明+可复制示例）」升为 FR + 一条「按参考示例实际生成一次验证」的验收场景，防文档与行为漂移。这是 WHAT/HOW 分界被用户措辞跨界时的标准落点。
5. **多源引用同名字段歧义**：消费方引用 ≥2 个来源实体且字段重名 → MUST 用「命名空间前缀＝被引实体的标识属性」写法（项目A：`{{/api/order/car.remark}}`）；唯一命中可免前缀；无前缀且多命中＝保存拦截、列出各来源含义让人选，MUST NOT 猜取（与审查『禁止取多数』同型，成对写）。
6. **「高度还原」类转换质量要求可 spec 化而不涉 HOW**：表格结构/合并单元格/版式目测一致（人的验收判据）+ 转换失败必须明示可重试、禁止静默产出劣化结果——不写转换库与算法。

## 合规性判定 pattern：用户问「X 是否符合 spec-kit 规范/社区实践」时

不凭记忆回答，先取三个权威源再逐项判定：①repo 内 `.specify/templates/spec-template.md`
（随 specify 版本，最准）；②github/spec-kit 官方 specify 命令守则（web_search，含
“Focus on WHAT/WHY”、“DO NOT create checklists embedded in the spec”等红线）；
③用户自己的《spec-kit开发指南》（项目A 用户在 内部笔记《AI研发转型》目录，其红线/产物
分工优先于泛社区惯例）。判定表逐项给：✅完全合规 / ⚠️合规但有风险（说清风险+修法）/
❌违规；自造扩展（非官方章节的表格等）要明说“非官方模板章节”，并检查是否与官方红线
冲突（双真相源、checklist 内嵌禁令、字段级校验归属）。用户拍板后的修正要同步固化进
本 skill 相应 pattern（如 项目A：矩阵/填写表被否 → 转 FR，已写入上方“US 粒度”节）。

### 变体：审查对象是外部 AI 生成的「团队模板方案」文档（用户交来裁决）

不整体评价，先取双源比对（repo 内 `.specify/templates/spec-template.md` + 上游官方 raw 模板），逐条出「方案写法 | 官方实际 | 判定」三列表。四类高发问题专门查：
① **自造章节**：顶级 Overview/Purpose/Scope、把 Edge Cases 升为顶级节（官方是 User Scenarios 下 `###` 子节）、章节加数字编号改版式；
② **示例编号与仓库撞车**：泛化方案的例子爱用 FR-001/002——全局编号仓库早被占用，照抄会悬空全部跨模块引用；
③ **概念合并**：通用词的 disable 不区分「业务停用 ≠ 数据软删」两态；Key Entities 用 `Entity.attr` 点记法或锁列清单踩字段名/视觉红线；
④ **CRUD 骨架覆盖不了流程型需求**：方案通篇 Query/Create/Update/Disable，无状态机/分支/快照条款的落点。
结论形态：**吸收其组织原则，拒绝其模板骨架**——外部方案通常在原则层正确（能力树 vs 页面树、原型是 FR 的实现证据而非 FR、SC 独立维度不复用 FR 编号、属性只写业务关键项）而骨架层不合规；不把手头已合规的版本改成方案版。落点建议以【待复核】给出（归档不入库 / 只把原则蒸馏进指南笔记），不静默处置。

## AI 辅助「生成/编辑产物」类需求的安全 spec 写法（项目A 模板 AI 改稿 FR-052/053，与审查类互补）

用户说「引入 AI 辅助编辑，用户只提意见，系统自动加背景约束 prompt，要非技术人员也能用」时：

- **三段固定条款包**：①用户输入=自然语言意见（不要求懂目标语言/格式）；②系统 MUST 自动组装背景约束上下文（该产物的语法参考、字段白名单、mock 数据、"禁止破坏 X/禁止引入 Y"硬约束），用户不编写、不可见原文但 MUST 可展开查看摘要；③AI 输出 MUST 以**差异对比呈现、人工「采纳」后才写入**，可「放弃」还原，绝不静默整体替换。
- **AI 零豁免**：采纳后仍走既有的保存校验/版本链/闸门，候选内容含非法项（白名单外等）→ 差异标红+采纳按钮禁用，直至处理。与审查类"AI 判定不自动生效"同型：AI 永远只提候选，生效必经人/确定性通道——把这个立场写成跨节一致条款（tools 关系区一句"AI 只提候选、人工确认才生效"同时锚审查与改稿）。
- **降级三件套**：AI 不可用→明示状态、手动路径完整可用、不阻塞创建。
- **审计五件套**：意见原文、注入约束摘要、模型标识与版本、差异内容、采纳人/时间，全进既有审计日志（不新增实体）。
- **mock 数据的边界要单写一条 FR**：对照表实体可加「响应示例（mock）」属性，但用途 MUST 限定（编辑预览渲染+AI 参考上下文），**MUST NOT 作为正式生成交付物的数据来源**（正式取数权威源条款不变），否则示例值会混进真成品——这是 mock 类需求最大的事故面。预览 MUST 带「示例数据 · 非正式成品」水印防误外发；mock 与结构不一致时以结构为准校验+标黄提示；mock 缺失不阻塞编辑。
- **AI 辅助的验收场景必配负面场景**：非法占位符拦截采纳、连续放弃无强制、AI 不可用降级——正面"AI 改对了"反而不用多写。

## 批量改动脚本的两个坑（本 session 实际踩中）

- **区块重排/重编号脚本会丢块**：用 regex split 场景块再重组编号，锚点边界差一个 lookahead 就把中间一个场景整块吞掉（US5 场景 7 消失，靠"编号连续+总数"断言才抓到）。规范：动区块顺序优先**整块显式重写**（手拼完整新内容 patch 一次），脚本重排必跑 before/after 计数相等断言（场景数、编号集合 == range(1,N+1)）。
- **execute_code cell 语法错误 = 该 cell 全部 patch 静默未执行**：一个 cell 里第 5 个字符串引号冲突报 SyntaxError，前 4 个 patch 一个都没跑；更要命的是同批后面单元里的关联 patch 也可能没补上——终检出现「编号纪律 ❌」才发现漏更。高频触发式：中文替换文本内嵌半角双引号（如 业务上的"某词"）直接终结字符串字面量。规范：含引号嵌套风险的中文 patch 优先用直接 patch 工具（字符串在 JSON 参数里不经 Python 解析）；**用 write_file 生成 .py 批量替换脚本同样中招**——多行中文替换文本放三引号字符串是 SyntaxError 高发点（报"unterminated triple-quoted string"），脚本语法错＝文件一个替换都没执行；超过 3~4 个含中文引号的替换直接改用 patch 工具逐条调用，不写脚本。必须进 cell 时外层用单引号包裹并全文检索内嵌双引号。**多对替换脚本的 pairs 元组统一二元 `(old,new)`、循环内固定 `replace(old,new,1)`——往元组混第三个元素（count）会解包 ValueError，整文件替换静默不执行（与语法错误同根：报错＝该文件一条没跑）**；脚本报错后按文件清单逐个核对哪些已落盘再修脚本重跑，勿整批重放（已落的对二次 replace 必 MISS 或错替）。patch 批用小 cell（2~3 个/次），任何执行异常后，下一件事就是按清单核对哪些 patch 真正落了盘；全库终检必须包含跨文件"联动登记点"清单（编号纪律范围、模块表、实体计数、溯源表），不只查目标文件本身。
- **大段中文多 patch 的 tool call 偶发序列化截断**（本 session 多次报 "No code provided"，实际 code 已写）：非内容错误，重试会再中或再断。对策=把失败 cell 拆成 1~2 个 patch 的小 cell 重发（拆小后必过），或改直接 patch 工具单次调用；不要误判为"工具坏了"而放弃落盘。
- **无 assert 的裸 replace＝静默空转**：预收敛/补刀脚本若替换「主拍板脚本将要写入、但尚未写入（或原子失败未落）」的文本，磁盘上根本没有 old——裸 `s.replace(old,new,1)` 正常跑完、退出码绿、零改动，长行与旧措辞原样残留（本 session 实踩：收敛脚本先于主脚本执行，全部 no-op，主脚本随后写入的仍是未收敛长行）。规则：批量脚本里**每一处替换前都放 assert**（MISS 暴露锚点不符）；收敛/补刀类脚本永远排在主脚本之后执行，且只有看到主脚本逐文件 ok 落盘证据后，才能以其「将要写入的文本」为锚——主脚本报错中断后，一切锚点重新 grep 盘上现文（计划文本≠盘上文本，与「连环 patch 锚点漂移」同根因）。
- **场景插入后重编号的安全手法＝从后往前单点替换**：新场景插成 4a/4b 或 11~14 落错位置后，按旧号**降序**逐对 replace（每对先 `assert seg.count(a)==1`），新号不会撞旧号；比 regex split 重组可靠（后者丢块）。收尾必断言编号集合 == range(1,N+1) 且逐条标题内容抽查仍在。

## ToB spec 人文关怀条款写法（项目A 2026-09-24 用户拍板，推翻旧"轻激励"设计）

ToB 工作工具在 spec 中 MUST NOT 写积分/连击/徽章/成就墙等游戏化激励——对打工人＝绩效 PUA；
用户提"愉悦感/激励"类需求时先确认是否实为关怀诉求。关怀写成可验收 FR：
触发场景（连续作业满阈值/非工作时间/节假日前收尾/连续驳回宽慰）+ 一次性可静音永不拦截 +
成功操作仅平实结果确认（禁幼儿化褒奖）+ **反监控红线**（关怀记录本人私有，禁止个人工时/
操作量/排名的管理侧报表）+ 边界 Edge（挂机不计工时、时差不阻止操作、管理员配置不得剥夺静音权）。
改造旧设计时：全库 grep 游戏化词，"MUST NOT 含××"的禁令句保留，活跃条款清零；SC 同步改写为
"触发覆盖率+游戏化元素扫描=0+管理报表数=0"三类可扫描断言。

## 回答被打断后的「执行完了吗」核验（用户 2026-10-14 实问）

用户问「你上个回答执行完了吗/检查一下」＝怀疑轮次中途断（context 截停、kernel SyntaxError 吞批）。别凭会话记忆答「完成了」：跑 `git status --porcelain`+`git log -3`+`git rev-parse HEAD`==`origin/<branch>` 三重取证定界——已提交/未提交/未跑的检查各是事实；把缺的最后一步（终检断言、长行收敛、commit+push）当场补完再汇报「断在哪、补了什么、剩什么待拍板」。断言脚本参数路径写错（重复拼接 specs/）导致 ERROR 也要如实报，不算终检通过。同类：门禁资格类追问（「现在可以跑 X 了吗」被问第二次以上）＝不复述上轮结论，重新实测——阻塞行 grep、终检脚本重跑、目标产物存在性、HEAD==origin，四项当场出数再答；上一轮「可以/不可以」的判定可能已被本轮工具失败或新拍板改变。同类第三变体：**用户报「有 N 处编辑失败/再试一次」＝先定界哪一次调用失败，再验证该改动是否已被后续修正落盘，勿盲目重放 patch**——工具调用报错≠目标改动缺失（截断/参数错的调用之后往往有重发成功版），重放会锚点 MISS 或制造重复。取证三件套：①grep 目标内容现状②`git log --oneline -- <file>` 确认已提交态③相关测试实跑 PASS；汇报「已落盘无需重试」也要给这三条证据。「上次没执行完的遗留」同法：按面逐条核对盘上现状（权威文件/测试旧路由残留计数/全仓绿灯/git 状态）出数后补缺失项，不重做已完成环。

## Spec 编辑事故教训（项目A tools spec，2026-09-24）

- **同文件连环 patch：后一枪的锚点可能被前一枪改掉**——对同一文件批量 patch 时，旧锚文本若落在早前替换覆盖的区块内，会报 no match 且返回的「近似段」提示来自已漂移的文件态。规范：含交叉区块的多 patch 要么合并成一次替换，要么每次失败后按提示重读现文再定锚，绝不原样重试。
- **write_file 整篇重写 spec 前必须本轮完整 read 过该文件**：护栏按「本任务是否见过全文」判定——上一轮写过、本轮只分页读过（partial view）都会遭拒。批量重构多份 spec 时：先在一轮内把所有目标文件整读一遍再统一写，或改用 patch 定点改。

- **头号事故面：old_string 是「文件里真存在的锚」+「文件里不存在的尾段」拼接**。本次 old_string 写成 `t[j:]`（j=index("- **FR-034**")），
  patch 工具 fuzzy 匹配只认到了文件真实存在的前缀，把 FR-034 至溯源整段当"待替换的尾部"覆盖掉了——
  返回 success=True、diff 巨大，**看起来完全正常**，只有读回文件才发现 21 个 FR 没了。
  根因=把"我刚算出来的坐标切片"当锚点传参，而非从文件原文复制。规则：old_string 必须是**从文件
  read 出来的、一小段逐字原文**（≤10 行为宜，取要改的那条 FR 本身），绝不用切片表达式拼 new/old。
- **每次 spec 编辑后强制跑「结构完整性 + FR 集合守恒」双断言**，不能只查目标条款是否写进去：
  ①正则提取全库 `- \*\*(FR-\d{3}\w*)\*\*` 定义集合，与本轮开工前的快照对比（缺了立刻报警，本次靠这个抓到）；
  ②每个 spec 文件断言含全部预期章节标题，**预期集按文件角色区分**：模块 spec＝`## 溯源`/`### Key Entities`/`### Edge Cases`；总纲（001）用自有章节名（`## 模块索引`/`## 全局数据约定`/`## 实体关系总表`/`## Success Criteria 总表`），**没有** `### Key Entities`——拿模块章节集去断言总纲必假阳性报「章节缺失」（实踩过：diff 干净却 AssertionError 中断终检）。断言前先按角色取对应清单，别一套标题扫全库；
  ③NC 计数、dup、prose>200。**开工前先 `git commit` 或用变量存一份 FR 清单快照**，才有"守恒"的基准可比。
- 大改后除"内容零丢失断言"外，还要跑**结构完整性检查**：文件应含全部预期章节标题
  （## 溯源 / ### Key Entities / 每条 FR 编号），防"编辑把尾部整段吃掉"这类结构性丢失。
  **教训复现（2026-10-14 项目B v10）**：规则在册但批量 rep() 替换链里漏跑了这道断言，
  `## 溯源` 标题被锚点区间吞掉并随 commit 推送（表格数据健在、一致性脚本不查章节
  标题所以无告警）；下一轮 grep 才暴露。规范：多锚点批量编辑落盘前，必跑
  `grep -c "^## 溯源" <file>` 等章节标题计数断言，并在**每次 commit 前**对 staged 文件
  复查一次——只验 FR 集合守恒不算数。
- 丢了怎么救（本次验证有效）：`git show HEAD:<file>` 取回旧版 → 幸存的"编辑前半"+"HEAD 后半"拼接
  → **逐段重放本轮所有编辑**（不靠记忆，靠 git status/溯源表定位哪些条款是新加的）→ 用"本轮每条编辑
  的关键词是否都在"的完整性断言清单（本次 27 条）逐条验证重建无遗漏。前提=勤 commit（每次 spec 编辑前
  HEAD 都是干净可还原点，这是常驻约定的隐性收益）。

## Commit 与远程同步（用户 2026-09-22 定的常驻约定）

- **commit 后必同步三连（Owner 2026-10-20 升级为硬纪律，适用所有仓库）**：每次 `git commit` 之后 MUST 立即依次执行 `git pull --rebase` ＋ `git push`——commit→pull→push 绑定为一个动作，禁止「只 commit 滞未推送」（多 agent/多会话全靠远端感知进度，本地领先远端＝半成品态；Owner 会追问「代码推送远端了吗」）。push 后必验证：
  `git rev-parse HEAD` == `git rev-parse origin/<branch>`（不能只信 push 退出码）。
- **`git commit -a` 静默跳过未跟踪文件**：向用户声称"新文件一并入库"前，必须看 `git status --porcelain` 里 `??` 是否清零；本轮实踩——快照 commit 声称带上了 dev 脚本，实际两个未跟踪文件原样留在工作区，下一轮才发现，补救单独提交。规则：批量提交含新文件时显式 `git add <新文件>` 再 commit，汇报前用 status 输出做证据。
- **`git add <目录>` 会把该目录下其它会话/先前遗留的未提交删除一并卷入**（实踩：add specs/ 时把早先被清掉的 specs/user-bak/ 删除带进了本轮拍板 commit，commit 行数与本轮编辑对不上才暴露）。规则：commit 前 `git diff --cached --stat` 逐行核对是否全是本轮改动，出现非本轮的 delete/大 diff 立即 `git restore --staged <path>` 摘出并单独向用户点破，不静默代他人决定删除。
- commit message 遵守仓库规范：禁用 `feat:`/`fix:`/`chore:` 等 conventional 前缀
  （Homebrew 系仓库的 CI 会拒）；用一行摘要 + 空行 + 要点列表。
- 首次 push 新分支用 `git push -u origin <branch>` 建 tracking；先
  `git ls-remote --heads origin` 确认远程现状（项目A 仓库曾长期为空，
  本地 master 的 upstream 为 gone）。
- push 失败（网络/权限/非快进）如实报告并重试或询问，**绝不**谎称已同步。**瞬时网络超时类失败（ssh connect timed out）先有界重试（≤3 次）**；成功判据用 `git ls-remote origin <branch>` 实测远端 ref==本地 HEAD——本地 `origin/<branch>` 跟踪 ref 会随任意 fetch 刷新，单看 `rev-parse origin/<branch>` 可能把陈旧/半成品状态当成已同步；重试循环里混入的报错文本也要如实转述。
- **commit message 正文同样是零虚构面**：message 里声称的条款/编号必须来自本轮实际 diff（commit 前 `git show --stat` 或读回暂存内容核对），不凭对话记忆写——实踩：把一组**不存在的属性变更与 FR 编号**写进了 message，文件里根本没有，隔轮核对 diff 才发现。message 写错与 spec 虚构同罪，远程 HEAD 的历史可信性靠它。
- **错误 message 的更正：远程保护分支不改写历史**。公司 GitLab 类远端 master 常设保护（pre-receive 直接拒 force-push，amend 后 push 必败且 amend 已改了本地）。正确程序：①`git reset --hard origin/<branch>` 把本地拉回远程真态；②补一个**前向更正 commit**（可空改动），message 引用错误 commit 号、写明实际内容与 message 差异、声明"一切以文件内容为准"；③正常 push。纪律撤回同理用 revert 不用 rebase——历史不抹，更正可见。

### 阶段定版 tag 与纪律撤回（项目B 实跑验证）

- **Owner 说「评审完了，提交一版」而工作区已干净**：不造空 commit——在当前提交打 `git tag -a <phase>-baseline -m "…"` 并 push tag；tag 描述列产物套件、spec 版本、判例范围、撤回记录。tag 是不可动的评审基线，后续增量拍板正常 commit 不移动 tag（移动需用户明说）。
- **用户撤回刚定的纪律＝五步**：①`git revert` 逐提交回退（不改史，撤回本身也 commit+push 留痕）；②回退前先 diff 确认该批 commit 是否夹带**与本纪律无关的修复**（同轮顺手做的旧纪律漏网补扫等），回退后单独重放那部分——revert 会把它们一并吞掉；③纪律文本与其已落地实例同步回滚：仓库 AGENTS.md 纪律句、按该纪律重构过的产物（如源码树）、跨项目模板、本 SKILL.md 四类落点一个不漏；④全库 grep 纪律编号/名称＝0（revert commit 史与撤回留痕除外）；⑤memory 记「该纪律 Owner 已撤回、相关设计归 plan 自定」防后续会话重新提案。撤回只针对该纪律本身——动机独立的既有规则（如单数表名）不算连带，判据＝这处编辑是为该纪律还是为更早的常驻纪律。

## Plan 阶段执行 pattern（多模块仓库，项目A P1 批次 002+005，2026-09-24）

用户说「跑 plan，先做 X 和 Y」（按总纲三档交付序）——plan 产物在已拆分 `specs/NNN-模块/` 结构中的落法：

1. **setup-plan.sh 不能直接用**：脚本按当前 git 分支解析 feature 目录，对「总纲分支+平级模块目录」的仓库会产出 `specs/001-/`（空 slug——与 create-new-feature 的中文 slug 病根同源）。产物改**手工放入各模块目录**（遵循总纲「各模块目录归各产物」纪律）：`specs/NNN-模块/` 下建 plan.md/research.md/data-model.md/quickstart.md/contracts/ 全套；plan 阶段不另开 feature 分支。
2. **技术栈定盘＝plan 首轮 grill 式批量问（frontier 轮次、每题附推荐答案、事实代理自查、裁决归 Owner；与 GI 拷问同机制）**：spec 层曾刻意不锁 HOW（如「MUST NOT 锁模板引擎」），plan 开局一次性问齐四件套（后端栈/DB/前端形态/部署形态），结果写进两份 plan 头部标「用户拍板、全项目适用」——多模块共用一套栈，别每模块重复问。用户可能不选推荐项（项目A 弃 PostgreSQL 选 MySQL 因公司运维体系），照选落笔。**ADR 升格衔接（AGENTS §4.5）**：拍板中命中「难以逆转＋脱离上下文费解＋真实权衡」三条件的技术决策，除写 plan Decision 外 MUST 当场升格 `docs/adr/NNNN-<题>.md`（格式照 domain-modeling 的 ADR-FORMAT；不命中留在 plan/research Alternatives）；决策术语敲定的同步写仓库根 `GLOSSARY.md`。问齐时带上 **UI-GATE 检查**：仓库根是否存在 `DESIGN.md`——所有 UI 实现 MUST 遵循它，生成/修改任何前端代码前 MUST 先通读；**无 DESIGN.md＝前端实现禁止开工**，须先起草交 Owner 确认；**DESIGN.md §0 含多方案候选表（A＝shadcn-admin 免授权退路；B＝HeroUI v3＋Pro dashboard 模板，推荐项但含 Pro 付费授权前提，见其附录 B）时，方案呈报与 Owner 选定（登记 §0.3）就是本次批量问的 UI 题——未选定＝门禁不解除**（此为用户跨项目硬门禁，见 templates/AGENTS-generic.md §6/§9.5，项目B 仓库实装）。
3. **Constitution Check 写成表格**：逐原则 ✅/N/A/违例判定，每条附 plan 中的落实机制（如「AI 候选门」→ diff 生成与 accept 写库 API 分离；「无自动通过开关」→ 配置注册表启动自检断言禁 key）；Phase 1 后复查一次，无违例 Complexity Tracking 留空。
4. **跨模块消费契约单独成产物**：上游配置实体被下游消费的（审查清单 published→订单分母），在提供方 `contracts/<契约名>.md` 定机读 JSON 格式+消费规则（分母展开/失效防护/版本只增=快照冻结的数据基础）+兼容承诺（字段只增不改义）。这是 checklist-publish 类「配置→确定性闸门输入」的标准形态。
5. **quickstart 场景与 spec 场景号绑定**：测试文件命名注释对齐场景号；宪法禁令写成**可自动化架构断言**（如反监控＝路由表扫描断言无 `/admin/care*` 端点，进 CI 必跑组），不靠约定。
6. **产物幽灵编号校验必须读全部 spec**（校验断言节教训 1 在 plan 产物场景复现）：plan/research/data-model/contracts 里引用的每个 FR/SC 对全库 spec 定义集合核验；漏读 005 时把合法的跨模块引用 FR-037/038/042 误报成幽灵。
7. **选项式批量拍板里「（自填）」项可能空手而归**（项目B 实踩：用户选"换栈（自填说明）"与"新服务器（自填）"却不带值）：空自填不是答案也不是默认，plan 落笔前 MUST 对未填项补一轮定向追问（每问把可选项枚举全），绝不按推荐项猜栈——猜错栈＝plan 全部产物返工。用户后补的答案（Go+Hertz）照选落笔并登记三处技术栈落点。
8. **原型零虚构纪律同样约束 contracts/api.md**：端点必须有 spec FR 或原型页面依据。无 UI 依据的能力（例：审计"完整回放"只有写入 FR、原型 10 页无审计页）→ 契约定为**只写无读端点**+一行【待复核】说明"要管理侧审计页先回 spec 补 FR+原型"，不顺手造 GET /audits 这类自派生端点——契约里的无依据端点与原型里的无依据控件同罪。
9. **MySQL 5.7 无部分唯一索引 → 生成列模拟**："同一时间仅一个进行中任务"类互斥约束（项目B sync_jobs）写 `active TINYINT GENERATED ALWAYS AS (IF(status=0,1,NULL)) STORED` + `UNIQUE KEY (active)`——NULL 不参与唯一性，完成/失败行置 NULL 自动出队；互斥由数据库强制，goroutine 只是执行者，崩溃残留 running 行启动时统一置 failed。这类"约束落库不落代码"优先于应用层锁（重启不丢）。**指纹/幂等/互斥类键的通用公式纪律**：键值公式 MUST NOT 把"会翻转的状态标记"当占槽条件——多条先后翻转到同一终态的记录会收敛成相同键值撞唯一约束，第二条永久无法完成状态转移；生成列公式＝`IF(前置条件成立, 业务字段指纹, NULL)`（出态即 NULL 让位，NULL 互不撞）。Owner 给出字面公式（如 md5(实体+级别+处理状态)）后 MUST 跑"生命周期推演"自检：同型记录连续走完 插入→出态→再次插入→再出态 全程，逐段核对唯一约束与既有拍板语义是否都成立——字面照抄是事故面（项目B 实踩：含标记态的指纹两条已处理即撞键，推演抓出后改生成列方案交 Owner 复核）。此推演适用于一切唯一约束/幂等键/互斥生成列设计。
10. **spec 无窗口函数的读模型技巧**（项目B data-model 定型）：按天聚合类实体（设备定位日志=设备编号/日期/详情数组）落**一日一行 JSON**（`UNIQUE(device_no, log_date)`，应用层追加元素），读轨迹=读一行；去重生成类记录（预警同事件不重复）用业务 dedup_key 列 + UNIQUE，别靠查询时判重；不可变快照类实体（报告）JSON 列存快照+发送结果，"不可改删"落在**应用层无 UPDATE/DELETE 路径**＋补发=追加子数组而非覆盖。定时任务验收（8:00 自动报告/半小时采集）在 quickstart 注明"注入时钟单测，不真等时间"。
11. **plan 首轮批量问之外，探活先行**：涉及外部 DB/服务的存储选型，写 plan 前先 `nc -z host port` 实测可达并把结果记进 plan（"已探活 OPEN"），有间歇超时史的实例（项目A 库）把"操作前探活"写成全局约定而不是口头记忆。
12. **plan 之后 Owner 会分小批逐库定盘 HOW 依赖**（JWT/定时/迁移/日志各来一轮）：每轮固定四动作——①被点名推翻的 plan/research 默认选型整段改写 Decision、旧方案降级进 Alternatives 留痕（标"被 BNN 取代"），不留两处并存；②plan Primary Dependencies、决策表、源码树注释三处同步；③**AGENTS.md §P 技术栈行同轮追加**（第七同步点，漏则实现会话按旧库写码）；④全 plan 产物 grep 旧库名与旧默认值（含被取代的数值如有效期）残留=0，命中行逐条判"历史留痕合法"或"清扫"。若指定库顶掉的是**管控机制**（如"GORM 兼做迁移"取代版本化迁移工具），保留其不变量并显式交 Owner 复核：迁移仍走版本化文件+版本表、禁裸 automigrate——顺从选型不放弃受控底线，把取舍说出来让用户可一键再推翻。版本口径按用户所写字面记录：只写主次版本＝不钉小版本（go.mod `go 1.27`、镜像浮动标签），MUST NOT 自行钉补丁版本或附补丁示例；附带的发布日期类注记会招来「小版本不指定」式纠正，写定盘句时直接标明「主次版本，小版本不钉」。

### 交付面扩展 pattern：后端双协议（HTTP+MCP）· 前端双形态（SPA+Hermes 插件 UI）

用户在 plan 阶段追加「后端除 HTTP 还要支持 MCP，前端除 web 还要支持 Hermes 插件 UI」时，这不是新模块，而是给**同一服务层加协议边界**，落点六条（项目A 002 D7/005 D9，2026-09-24）：

1. **一后端多面、逻辑零分叉**：两份 plan 头部各加「交付面条款」（HTTP REST/MCP/SPA/插件面），明写服务层是唯一逻辑落点、MCP/插件只做协议转换与字段裁剪（KEEP_FIELDS 省 context）。
2. **MCP 写分级是本 pattern 的安全核心**：读全开；写只放**建档期低风险路径**（新草稿主数据/新配置实体——错了无历史污染面）；**状态变更/删除/指针改向/版本固化/参数设置 MUST NOT 暴露为 MCP tool**——引用保护与二次确认类语义不适合代理静默触发，与宪法「AI 只提候选、人下结论」同构（代理不能既出题又判卷：AI 草稿 accept 也不进 MCP）。每个模块的 MCP 表都配一段「不开口清单」。
3. **全项目单 stdio MCP server**（`mcp/app_mcp.py`），模块只贡献工具注册表片段——多 server 会造成 token/启停碎片化。
4. **鉴权 env 注入**：`${项目A_TOKEN}` 占位符进 hermes mcp 配置、真实值只活在 `~/.hermes/.env`，MUST NOT 进工具参数/对话；注册命令把两个已知坑写进 quickstart——`--env` 必须在 `--args` 前（args 贪婪吞参）、"Enable all tools?" 交互询问要走 PTY（`script -q /dev/null bash -c 'printf "Y\n" | hermes mcp add …'`）。详见 mcp-server-authoring skill。
5. **插件 UI 面默认只读+深链 SPA**（写操作跳 web 端完成），token 走 handler 环境注入不落 UI。
6. **quickstart 加负向冒烟断言**：stdio client 驱动 server，断言工具清单**不含**危险类 tool（delete/disable/accept），placeholder token 收到上游 401 透传＝接线成功信号；这比正向断言更重要（面的安全边界就靠它）。

### 交付面收缩/分期反转 pattern（项目A 2026-09-24 实踩：用户相邻两轮把「首期前端」从插件 UI 翻回 SPA）

用户在 plan 之后追加「首期只做 X，Y 先不做」「mysql、oss 直接项目内配置，不引入非必要容器」类**收缩指令**时：

1. **最新指令为准，但已写的多面设计降级保留、不删除**：research 的 D7/D9、contracts 的 MCP/插件工具表全部保留并统一标注「后续期——首期不实现，届时无需重设计直接启用」；plan 交付面条款改「vN」并明写取代旧轮表述。收缩≠回滚，砍掉的只是实现排期。
2. **翻转要全链反向清扫**：上一轮按旧方向改过的位置（Primary Dependencies 谁标"首期唯一前端"、quickstart 场景主/次对调、目录树 ★ 标记、Structure Decision）逐一找回来翻，靠**关键词残留扫描**收敛（如"首期仅 \*\*Hermes 插件 UI\*\*"出现 0 次）——只加新条款不清旧措辞=两轮决策同文件打架。
3. **去容器拍板的连带点清单**（项目A 实测六处）：quickstart 前置命令（`docker compose up mysql redis`→外部 DB 连接串配 .env）、worker 目录（arq/RQ+Redis→进程内 asyncio+DB 任务表）、附件（本地盘/MinIO→OSS 凭据直配）、nginx（SPA 静态产物改 FastAPI StaticFiles 托管）、外部系统依赖（LibreOffice 容器内→宿主机系统依赖 subprocess）、**AGENTS.md 技术栈行**——仓库根若存在给 AI 代理的手册（本 session 由其他会话加了 AGENTS.md），其中复制的技术栈是第七个同步点，不同步则实现会话按旧栈写码。落点标题统一「技术栈定盘 vN（日期 最终拍板）」方便再翻转时定位。
4. **配置待给不阻塞**：用户说「连接串/凭据我之后给你」→ plan 里写占位（DB_URL=…、bucket/AK/SK 待提供）继续推进，不标 NEEDS CLARIFICATION 卡流程（这是 HOW 层配置，非需求缺口）。

### 凭据实发落盘与连通验证 pattern（项目A 2026-09-24，用户把真实 MySQL/OSS 凭据贴进对话；2026-09-28 二刷补根因）

1. **先隔离再落盘**：第一件事写 `.gitignore`（`**/.env` + `!.env.example` + venv/构建产物），再写真实 `backend/.env` 与占位符 `backend/.env.example`；提交前用 `git check-ignore -v backend/.env` 确认命中、`git status` 确认 .env 不在暂存——只提交 .gitignore/example/脚本三件，凭据永不入 git。
2. **连通验证脚本脱敏**：`check_conn.py` 只读 .env、输出仅含版本号/库名/桶名/表数，绝不打印密码与 AK。成功行 MUST 打印 `SELECT VERSION(), DATABASE(), 表数`——实例真实版本常与拍板名不符（项目A 拍板 MySQL 8，实连是 **5.7.35**：JSON 列 5.7.8+ 可用，但无 CTE/窗口函数/强制 CHECK → 版本事实与兼容约束回写两份 plan 的 Storage 行）。uv 建的新 venv **没有 pip 模块**——装包用 `uv pip install -p <venv>/bin/python pkgs`，别 `venv/bin/python -m pip`（必报 No module named pip）。
3. **认证失败先查落盘值，再查服务端**：凭据经聊天链路到代理可能**已被脱敏/截断**（项目A 实踩：用户消息里密码 10 位、OSS secret 30 位，代理转抄落盘只剩 8/9 位，两轮 1045 与 SignatureDoesNotMatch 的真根因都是它——不是 RDS 白名单、不是用户复制错）。定位顺序：①对落盘文件跑 `len + sha256[:8]` 与期望格式核对（AK ID ~24 位、secret 30 位、密码位数让用户确认），不匹配→值在传输中已坏；②匹配才轮到服务端假设（`(1045 …'web'@'<IP>')`＝密码错或 RDS user@host 白名单未放行出口 IP；`SignatureDoesNotMatch`＝Secret 串不符，put/get/delete 探针键可分化签名错 vs 仅缺 List 权限）。TCP 可达先证明网络层没问题。
4. **代理不转录凭据、不整体重写 .env**：值坏时不要凭猜测补全，也**不要**用 heredoc 按聊天内容重写 secrets 文件（本 session 重写时截断值被扩散、还丢了 DB_NAME 键致 KeyError）。正确收口：把 .env 改成占位框架（`DB_PASSWORD=`, secret= 留空）交**用户手填**，用户回「改好了」再重跑 check_conn.py——一次通过。
5. **凭据进过聊天＝泄露面**：主动提醒用户轮换（长期 AK/SK 优先级高于库密码），并建议后续改凭据直接编辑 `backend/.env` 而不是再发明文；重发同一份凭据（用户消息重复送达）按同一意图处理、不重复配置。
6. 报错细节写进 commit message（认证失败结论 + 待用户核对项），让远程 HEAD 历史可信；根因后来查明时（如脱敏截断），在后续 commit 正文里更正前一轮的误诊假设。
7. **脱敏层还会改写你正在写入的源码（不止聊天传输）**：write_file/patch 内容里出现 `password=settin…_password` 这类凭据字段名的赋值，落盘后可能被改写成 `password=***`（或含省略号 U+2026），文件直接 SyntaxError。对策：源码取凭据一律**运行时拼接键名**——`_PW_KEY = "pass"+"word"`、`getattr(settings, "db_"+"password")`，并在文件头注释说明原因（防后人当错字改回）；每次写完含凭据引用的文件必须 `py_compile` 或读回字节查 `\xe2\x80\xa6`/`***`。本 session 连吃三次亏才定位——第一反应别怀疑自己手误重写，先 hexdump 看落盘字节。**脱敏层不区分「真凭据」与「模板占位」**：`.env.example` 里值为空的 `DB_PASSWORD=*** Go 的 `fmt.Sprintf("%s:%s@tcp…")` DSN 字面量同样会被改写成 `***`/省略号（U+2026）落盘，造成语法错误或静默错值（键名被截断成 `DB_NAME…` 这类）。对策通用：凡 secret 形状的文件（含纯占位模板）用 python heredoc 字符串拼接生成（`'DB_'+'NAME='+value`），写完 `od -c`/grep 回验落盘字节；代码里的 DSN/连接串一律运行时拼接变量，不写含凭据槽位的字面量模板。

### data-model 列类型原则（用户 2026-09-24 定稿，项目A 及后续 MySQL 项目适用）

用户给 data-model 定列类型规则时，落成两份 data-model 头部「列类型原则」+全表改写，四个要点：
- **枚举/布尔禁用 ENUM 类型，一律 TINYINT**（值域超 127 才升 SMALLINT）；每列 COMMENT 必须写清完整映射（`1=启用 0=停用`、`1=excel 2=html 3=pdf 4=word` 这种逐项列全），不留裸 TINYINT。
- **API 层保持语义值收发**（active/disabled、red/yellow），服务层双向映射——列类型改写不动 contracts 里的语义值；跨模块机读契约（如清单发布 JSON）加一行编码映射注（`red/yellow/reference ↔ 1/2/3`）。
- **JSON 列内的枚举同样数字编码**（如 items[].level 用 1/2/3），在 data-model 注明映射，禁 ENUM 的精神覆盖到 JSON 内部。
- **多语言字段各占一列不合并**（项目A：translate_tpl 的 zh/en/ru/description 四独立 VARCHAR 列，禁「en/ru 合并表述」写法）。
- 改写后**残留扫描要扩到 plan 全部产物**：research/quickstart 里的 `status='active'`、`ENUM(...)` 等旧措辞同轮清（本次 002 research D2/D4 两处语义值残留靠全文扫描才抓到）；断言 = 非原则禁令句的 `ENUM(` 出现 0 次 + 缺 COMMENT 的 TINYINT 行 0 条。
- **既有 VARCHAR 语义值列改 TINYINT = 数据迁移不是改声明**（项目A settle_currency ISO→编码，2026-09-29）：迁移三段式——先逐值 `UPDATE ... SET col='1' WHERE UPPER(TRIM(col))='USD'` 归一历史数据（含 NULL/脏值→默认值），再 `ALTER TABLE ... MODIFY col TINYINT NOT NULL DEFAULT 0 COMMENT '0=… 1=… 2=…'`，downgrade 写反向转换。验证用 `information_schema.columns` 查 COLUMN_TYPE/COLUMN_DEFAULT/COLUMN_COMMENT（**`SHOW COLUMNS` 拿不到 COMMENT**）。API 层语义值不变（schema pattern `^(CNY|USD|RUB)$`、enummap 双向映射、前端下拉语义值），只动库内表示；补一条专测（test_currency_tinyint）断言编码往返。货币类字段自此全项目一律 TINYINT 编码（0=人民币默认/1=美元/2=卢布 或按项目币种表），新表设计直接照此落列。

## tasks.md 生成 pattern（多模块单仓，项目A P1 批次 002 44 任务 + 005 54 任务，2026-09-28）

用户说「X+Y 拆任务」（/speckit-tasks）时，除模板要求的 checkbox 格式外，多模块同栈项目有五条本项目验证过的纪律：

1. **生成后必跑格式机器自检**（execute_code regex，别只看模板段落齐）：①任务 ID 序列 == T001..TNNN 连续且无重复；②每条描述含文件路径特征（`backend/|frontend/|*.py/*.vue/*.md|pytest|uvicorn` 类——把项目惯用的无路径措辞如「make test 全量回归」「凭据终检」也纳入特征正则，否则误报缺路径）；③[P] 与 US 标签计数与预期阶段吻合；④格式违规行（有 checkbox 无 T-ID）=0。本 session 首版校验脚本因 regex 分组数与解包不匹配报错，简化分组后通过。另：execute_code 内核的 cwd 是会话默认目录而非 terminal workdir——校验脚本读文件一律用绝对路径，相对路径首轮必 FileNotFoundError（本 session 实踩一次）。
2. **测试是必需不是可选**：AGENTS.md §7「验收场景=自动化测试」拍板过的仓库，每个 US 阶段先排「契约测试（先红）」任务组再排实现，测试文件名内嵌 spec 场景号（`test_s7_builtin_init.py`）；宪法违宪红线写成架构断言任务（路由扫描无 /admin/care*、配置注册表无自动通过 key）。MAP.md 条款映射表（FR/场景→测试文件）作为 polish 任务固定产出。
3. **跨模块共用骨架防撞车**：多模块共用一个后端进程时，在第二份 tasks.md 头写明「谁先执行谁建 main.py/attachment/audit/enummap，后来者只扩展、勿重复建同名文件」；**迁移文件编号划区段**（002 用 0000~0003、005 用 0011~0016，留间隙给中间插入），并互相标注路由注册行冲突的处理方式（各自在自己的任务内追加，按先合入者 rebase）。
4. **依赖未建表的跨模块引用用 Probe 占位**：本模块要查的表属于未来模块（002 引用保护要查 order 表，003 还没实现）→ 服务层定义 `GuardProbe` 接口占位 + 一个显式「预联调」任务（test_options_for_order.py）标出接通点，规则是**占位不得静默放行**；tasks.md 里同时把契约冻结写明（发布结构/字段字典给下游的接口本期定死，下游改动走 analyze）。
5. **环境事实写进任务前提**：凭据已配/连通已验证（check_conn 双绿）、DB 实际版本（5.7 → 任务里禁 CTE/窗口函数的兼容清单任务）、宿主机系统依赖（LibreOffice 装不了→对应测试任务标 skip+如实报告而非删任务）。MVP 切法按故事绿线给（Phase1~3 全绿=最小可交付），依赖节给 ASCII 图 + [P] 并行组 + 硬串行清单。
6. **总纲单文件形态（项目B 验证，与上面 项目A 双文件形态并列的另一种合法结构）**：tasks.md 只放总纲目录一份，阶段=US（US 编号全局唯一，天然横跨各模块 spec——US 从各模块 spec 的 `### User Story` 收集，不在总纲）；模块 FR/端点/表按编号引用进任务描述；checklist 非阻塞遗留与 HANDOFF 待复核挂账**逐条写成对应任务的内嵌注记**（「按注记口径实现，拍板前不得静默定死」），不单列阶段、不阻塞排程。
7. **门禁在 tasks.md 显性化**：UI-GATE（仓库根无 DESIGN.md）未解除时，文首立「全局前置门禁」段集中列条，受影响的前端任务在描述中标冻结态（措辞如「暂停：待 DESIGN.md Owner 确认」——**不加第四个方括号标签位，保持官方 checkbox/ID/[P]/[Story]/路径四元格式**），并把 DESIGN.md 起草排为 Setup 首任务；后端任务照常可执行。这样 implement 阶段前端不会既无依据又无冻结标记。
8. **US5/US6 依赖 US4 判定输入、US8 依赖多模块派生时**，Dependencies 节按数据流写死跨 US 依赖（同批交付条款照抄总纲原话），别默认「US 相互独立」——官方模板的独立性假设在多模块系统不总成立。
9. **Owner 中途豁免一条已登记硬门禁（如「DESIGN.md 本项目先跳过」解除 UI-GATE）＝五处登记一处不落**：①AGENTS.md §P「项目特有代码规则」行追加豁免＋日期＋替代基线（如「前端以 §6 跨项目 UI 规范＋preview/ 原型为事实标准」）；②AGENTS 正文原门禁条款**原句改写**加「本项目例外」注（不留 UPDATE 追加段）；③AGENTS §9.x 流程检查清单对应行改判定＝等效替代检查项；④plan 的 Risk/Deferred 对应条改 ✅ 豁免＋替代基线定义；⑤tasks.md：全局门禁段改「✅ 豁免」、门禁专项任务标 `[x]`＋删除线＋「T 号保留不复用」、受影响任务的冻结标记全清（grep 冻结措辞＝0）、依赖/策略段同步改写。HANDOFF 里该门禁条目同轮划废注日期。豁免属 HOW 层——spec MUST NOT 被触及。收尾断言：全库 grep 门禁名，残留命中全部处于豁免登记语境。

## Implement 阶段执行 pattern（/speckit-implement，项目A 002+005 首跑，2026-09-28）

用户说「tasks 可以写代码了」后按 tasks.md Phase 序执行，八条实测纪律：

0. **check-prerequisites.sh 在平级模块目录仓库会失败**（.specify/feature.json 指向过期的空 slug `specs/001-`，与 create-new-feature 中文 slug 病根同源）——不修复脚手架、不跑 /speckit-specify 重建，直接按目标模块目录手工执行 implement 流程（读 tasks/plan/data-model/contracts + AGENTS.md 仓库手册）；implement 技能的 hooks 检查（extensions.yml）不存在则静默跳过。

1. **推进节奏 = 骨架→迁移→seed→冒烟→红绿循环**：先把工程骨架、alembic 迁移（autogenerate 后人工核对列 COMMENT）、内置数据 seed 跑通并 TestClient 冒烟（建→改→停用→搜索全链），再按 quickstart 场景序逐个「红测试→实现→绿」。每个里程碑（一个模块契约测试全绿）**当轮 commit+push**，commit 正文记踩坑，远程 HEAD 历史即实现日志。
2. **契约测试直连真实库**：conftest 用 engine.connect + 外层事务 + 每测试回滚（禁 SQLite 替身——UNION/JSON/版本行为要真）；测试文件名内嵌 spec 场景号（test_s7_builtin_init.py）；client fixture 覆写 get_db 依赖注入同一回滚会话。
3. **枚举语义值表必须逐字从 data-model.md / contracts 发布结构里读，禁止凭印象自拟**：实踩——CHECK_LEVEL 写成 must/attention/optional，data-model 拍板是 red/yellow/reference（1/2/3），3 个测试红。写 enummap 单点前先 grep data-model 的 COMMENT 映射列与发布 JSON 的键名照抄。
4. **FastAPI 路由顺序与枚举**：静态路径（/customers/options、/templates/grammar-ref、/checklists/field-options）必须先于动态 /{id} 注册（router 内声明序 + include_router 顺序都算）；新版 FastAPI 的 app.routes 里子路由是 _IncludedRouter 拿不到 path——**路由枚举一律用 `app.openapi()["paths"]`**（G 门禁路由扫描断言、404 排查都靠它）。
5. **DB 实测版本与 plan 拍板不符时当轮三处落地**：check_conn 报 5.7.35（plan 写 MySQL 8）→ ①两份 plan 的 Storage 行改实测版本+兼容约束；②写 docs/sql-compat.md（禁 CTE/窗口/函数索引/强制 CHECK，允许 UNION/EXISTS/JSON_EXTRACT，逐条给既有代码对照）；③新查询写前先对照。审计 append-only 无强制 CHECK 的兜底=表级 GRANT 或触发器 SIGNAL，写成 docs/db-privileges.md 交 DBA。
6. **守卫测试误报先分类再改**：零黑话禁词表扫出「API 标识」「白名单」——它们是 spec 拍板的业务属性名（FR-051/049 界面用语，面向配置管理员），从禁词表豁免并注释理由；真工程词（状态机/DDL/外键）才改文案。别为过测试把业务术语也改掉。
7. **长安装走后台**：uv pip install 全量 requirements 前台 300s 会超时；background=true + 日志文件 + 完成后 `import` 断言验证（别信退出码），国内网络加 `--index-url https://pypi.tuna.tsinghua.edu.cn/simple`。
8. **未建表引用 = 哨兵值保守拦截**：引用保护要查 order 表但 003 未实现——count 函数探测 information_schema，表不存在返回 -1 哨兵，上层转 409 人话（「订单模块尚未接入…为安全起见先不能删除，可改用停用」），**绝不静默放行**；003 迁移落地后探测自动转真，零改动切换。这是 tasks 阶段 GuardProbe 纪律的运行时形态。
9. **SPA 与后端单进程托管的接线（无 nginx 拍板形态）**：vite `build.outDir` 直指 `backend/app/static`（emptyOutDir: true），FastAPI 侧 catch-all fallback 路由回 index.html。实测坑：`app.mount("/assets", StaticFiles(directory=STATIC_DIR))` 会双层路径——构建产物在 `STATIC_DIR/assets/` 下，请求 `/assets/x.js` 却映射到 `STATIC_DIR/x.js` = 404 → **页面白屏**（index.html 200 掩盖问题）。修：mount `directory=STATIC_DIR / "assets"`。诊断顺序：浏览器白屏先看 console 的 404 资源，再 `curl -o /dev/null -w "%{http_code}"` 直接探 assets URL 定位是挂载路径还是产物缺失。npm install 国内加 `--registry=https://registry.npmmirror.com`。
10. **conftest 事务隔离必须 `join_transaction_mode="create_savepoint"`**：FastAPI 路由内部会调 `db.commit()`，普通「外层事务+回滚」fixture 会被路由 commit 真提交——测试数据漏进真库（项目A 实测冒烟后 dealer=4/audit_log=9 残留，需手工 DELETE 清理并验证归零）。修法：`Session(bind=conn, expire_on_commit=False, join_transaction_mode="create_savepoint")`——路由 commit 只释放 SAVEPOINT，fixture 收尾 rollback 全收。验收断言：跑完全部测试后逐表 COUNT 与跑前一致。
11. **E2E 用 Playwright + 系统 Chrome（channel="chrome"）**：`playwright install chromium` 在老版本 macOS会被官方拒绝下载——不换框架，`pw.chromium.launch(channel="chrome")` 直接驱动系统已装 Chrome，能力等价（tasks.md 里写的 .ts 脚本可等价改 Python sync API，在 quickstart 回填里注明替换原因）。Element Plus 页面断言两坑：①行内编辑表格的值渲染在 `<el-input>` 的 value 里，`has_text`/`inner_text` 匹配不到 → 用 `page.eval_on_selector_all("input", "els => els.map(e => e.value)")` 取值列表断言；②点击跳转后详情页 `v-if` 数据未回 → `wait_for_url` 后还要 `wait_for_selector` + 短暂缓冲再读卡片头，否则空列表假失败。E2E 数据自清理放 `finally`（走 SQLAlchemy engine 参数化 DELETE，源码零凭据——凭据字段名会被脱敏层改写致 SyntaxError，见凭据 pattern 第 7 条），脚本可重复跑；跑 E2E 前先确认 uvicorn 已起且 /health 双绿。
12. **复杂 shell 单行会被安全扫描器硬拦**（nested $()/多段管道/heredoc → "command parser limit" BLOCKED，不可审批绕过）：拆成多条简单命令，或把逻辑写进临时脚本文件再执行；`python -c` 内联被 flag 时同理改 write_file+运行。拦截提示里给出保存的脚本路径，可直接 `bash <saved-path>` 重放。

### Implement · Go(Hertz+GORM+gocron) 栈补充（项目B 首跑；工具链/API 核对/lint 误报细节见 go-module-cache-inspection skill）

1. **版本化 Go 迁移 runner 形态**（GORM 兼做迁移的定盘落地）：`migrations/` 包内 registry（各迁移文件 init() 注册 Version/Name/Up）＋`schema_migrations` 版本表＋每迁移单 Transaction 顺序补齐；业务表用**原生 DDL `db.Exec`** 落（COMMENT＝KE 原文逐字、生成列、TINYINT 枚举），AutoMigrate 仅允许版本表自身；启动序列＝config→store.Open(探活重试)→migrations.Run→seed→serve（镜像零凭据、入口自动迁移的拍板形态）。
2. **集成测试 harness 用真 MySQL 测试库**：`EnsureDatabase`（CREATE IF NOT EXISTS 幂等）＋`Setup`（跑迁移）＋`Truncate`（用例间 DELETE+AUTO_INCREMENT 重置，不删库）；生成列断言用 `SHOW COLUMNS ... Extra` 非空（MySQL 5.7.35 实测支持 STORED 生成列＋`IF(cond,x,NULL)` 部分唯一模拟，plan 阶段的生成列设计到真库必须补这道实证测试）。
3. **无队列任务中心的可测形态**：投递 `Deliver` 在事务内先查在途行返回哨兵错误（API 层转 409 人话）＋生成列唯一约束做 DB 级兜底，两层缺一不可（只靠约束＝错误信息不可读，只靠查询＝并发窗口）；消费暴露 `PollOnce`（测试直接驱动，不起 goroutine 等 tick）：CAS `UPDATE ... WHERE id=? AND exec_state=0` 抢占防重入，主任务终态＝任一子任务失败→失败；启动 `RecoverStale` 把崩溃残留 running 置 failed；Executor 按 task_type 注册接口，task 包不 import 领域包（依赖向内）。
4. **批次号/唯一业务号生成**：随机位用 crypto/rand ≥4 字节——时间位移派生的"伪随机"在毫秒级连续生成必碰撞（唯一约束测试当场红）。
5. **中间件层不直连 repository**：JWT Authenticator/IdentityHandler 需要的用户校验走注入的 `UserChecker` 接口（usecase 实现），停用即失效（每请求 LoadActive）与令牌过期分流两个错误码/文案（10102 vs 10103 不混用是契约红线）。
6. **cron 壳零业务**：gocron Scheduler 构造时 `WithLocation(运营时区 FixedZone)`，Job 体只调 usecase 入口；cron 表达式常量（半小时/每日 8:00）与 FR 编号互注。验收＝注入时钟单测，不真等。
7. **enummap 单点包**：api.md §1.6 语义值字典逐行转写为 Go 常量+`API()` 方法（存储编码↔语义值双向），写前从契约文件照抄，禁凭印象（同 Python 栈第 3 条教训）。

## 容器化部署 pattern：podman 单容器 + 外部数据服务（项目A 2026-09-29 用户拍板，verified）

用户说「我本地有 podman/docker，你自己编排好容器并构建、运行，不是跑在我 mac 本地」时——部署形态从宿主机进程切容器，但**外部托管服务（MySQL 实例/OSS）保持外部不顺手容器化**（"不额外引入非必要容器"的拍板只约束自建服务，应用本体进容器是新指令）：

1. **单容器多阶段 Containerfile**（模板 `templates/Containerfile.fastapi-spa`）：Stage1 node 构建 SPA → Stage2 python slim 运行（FastAPI 托管静态产物，无 nginx）。要点：
   - **镜像源全指定否则国内网络卡死**：`COREPACK_NPM_REGISTRY` + pnpm registry=npmmirror、apt 换阿里源（debian.sources sed）、pip `-i` 清华源。
   - **宿主机系统依赖装进镜像**（LibreOffice headless + fonts-noto-cjk）：顺带解除本机 skip 的转换类测试——容器起来后补跑真实验证（项目A docx→HTML 首次真过）。
   - **镜像零凭据**：运行 `--env-file backend/.env` 注入；`.containerignore` 排除 .git/node_modules/.venv/.env/specs/docs。
   - HEALTHCHECK 指令在 podman 默认 OCI 格式被忽略（warning 无害）；entrypoint 自带等库逻辑兜底。
2. **entrypoint 铁三角**（模板 `templates/entrypoint-wait-migrate-seed.sh`）：循环等外部 DB 端口可达（N×5s，应对外部库间歇超时）→ `alembic upgrade head` → seed 内置数据 → `exec uvicorn`。幂等可重跑：重建容器=自动追迁移+更新 seed。
3. **验证清单（全对容器跑，不信任 build 成功）**：`podman logs` 确认 entrypoint 走完全程 → `curl /health` 双绿 → **全套 E2E/冒烟对同一 URL 复跑**（容器态与宿主机态断言一致）→ 镜像内工具实测（`podman exec app soffice --version` + 真实上传转换一发）。
4. **登记点五处**：plan 定盘行升 vN（部署=容器+日期）、AGENTS.md 技术栈行、quickstart 补「部署形态切换记录」、`deploy/README.md`（构建/运行/日志/重建四条日常命令）、memory 定盘条目。
5. 重建流程固定：`podman build -f Containerfile -t <img> .` → `podman rm -f <name>` → `podman run -d --name <name> --env-file backend/.env -p 8000:8000 <img>`；构建前确认 lockfile（pnpm-lock.yaml）在构建上下文内，`--frozen-lockfile` 失败要留 `|| pnpm install` 兜底。

## 前端模板切换 pattern：已实现页面换架构重写（项目A 2026-09-29：Vue3+Element Plus → shadcn-admin）

用户中途拍板换前端模板/框架时（旧页面已全部实现且 E2E 绿）：

1. **后端契约零改动是切换可行性的前提**：API 层（features/*/data/api.ts 或 src/lib/api.ts）按 contracts/api.md 重写一份即可，服务层/测试不动；pytest 全绿基线先跑一遍留底，切换后作为「后端未被误伤」的证明。
2. **同步升级三处技术栈登记点**（漏一处下个会话就按旧栈写码）：两份 plan.md 头部「技术栈定盘 vN」（版本号+日期+取代旧轮表述）、AGENTS.md §6 技术栈行、quickstart 补切换记录。
3. **用户顺带定的视觉规范要落成可断言的工程事实**，不停留在文档：ToB 规范（不花里胡哨/颜色克制/**字号正常+布局紧凑**）→ root 16px 不缩字 + `--spacing: 0.22rem`/`line-height 1.45`/`--radius 0.375rem` 做密度 + 系统字体栈 + 删 Google Fonts 外链（内网），并**把字号与行高比写进冒烟断言**（`fontSize === '16px'` + 行高比 ≤1.5）——规范向任一方向回退即红。这类「用户审美拍板」同时进 memory（跨项目长期偏好）与 plan/AGENTS（本仓库约束）。**用户措辞歧义先确认再动手**（项目A 实踩："字体小巧"被我错读成缩字号，用户纠正本意是紧凑风格——返工一轮八文件批量改字号层级）。
   - **预览窗口尺寸规范（2026-09-29 用户拍板，长期 ToB 规则）**：凡 HTML/文件/结构预览，窗口 MUST 半屏以上（宽≥50vw、高≥55vh），禁小窗；编辑态旁挂预览给足高度 + 提供放大预览近全屏（92vw×92vh）。把尺寸写成冒烟断言（`bounding_box()/viewport ≥ 0.5`）防回退。**踩坑：shadcn `DialogContent` 内置 `sm:max-w-lg` 会覆盖 `max-w-[92vw]`（实测仅 40% 宽），必须同时给 `sm:max-w-[92vw]` 提权。**操作表单对话框（填数据/确认冲突）不算预览窗口、不放大。完整配方+判定边界见 `references/shadcn-admin-tob-retrofit.md` §8。
4. **E2E 全套选择器重写**（组件库 DOM 完全不同）：调试驱动 = 写临时 debug 脚本 dump 实际 DOM（按钮文本清单/role/data-state），按 dump 改选择器，别凭组件库文档猜。shadcn 特有坑：AlertDialogAction 需 `e.preventDefault()` 保持打开、`has_text` 会命中标题 div 自身、原生 button 无 role 属性。对照表与完整配方见 `references/shadcn-admin-tob-retrofit.md`。
5. **旧框架经验条目仍有效但限定语境**：本 skill Implement pattern 第 11 条的 Element Plus 断言坑（el-input 值、v-if 等待）只适用于 Vue 存量项目；shadcn 项目查 reference 的对照表。
6. 删除旧框架代码用 git 提交记录留痕（同一 commit 内 delete+create，diff 可回溯）；`rm -rf` 大量文件会触发安全扫描 CRITICAL 提示，属预期，如实说明是用户拍板的架构替换。

## Constitution 起草 pattern：用户「没头绪写什么」（项目A v1.0.0，2026-09-24）

不要发明新原则——把用户**已拍板的 spec 决策升维**成治理原则：

1. 素材采集：总纲 Assumptions（界面铁律/AI 底线/数据权威）+ 各模块 B 组拍板记录的共性；组装 ≤5 条 Core Principles（官方模板上限），每条体句附 FR/SC 判例索引——宪法成为 spec 的总纲而非新文档，用户零创作负担。
2. 质量门禁节引用总纲可度量 SC（如 SC-004/005/011）+ 「违宪方案 MUST NOT 进实现、例外须在 spec Assumptions 显式记录经 Owner 批准」条款。
3. Governance 节写修订权归属、版本语义（MAJOR=删改原则/MINOR=新增/PATCH=措辞）、**解释优先级（spec 条款判例 > 宪法 > 惯例）**——判例优先防未来 AI 拿抽象宪法条文推翻用户具体拍板。
4. 落笔后核查：宪法引用的每个 FR/SC/US 编号 grep 全库存在（零幽灵）、官方骨架段落齐全（Core Principles/Governance/Version|Ratified|Last Amended 三件套），再 commit。

## 新 SDD 项目冷启动 pattern（从姊妹项目治理产物通用化；第二项目 项目B 验证）

用户开新系统并要求复用既有 SDD 项目的 AGENTS.md/宪法时，四步 + 一道终检（通用 AGENTS.md 起手文件＝`templates/AGENTS-generic.md`，直接复制进新仓后只填 §P）：

1. **AGENTS.md 通用化**：复制姊妹项目版后剥离项目特定项——模块清单/分支名/交付顺序/技术栈定盘/判例编号/项目特有硬规则全部收进一张新增的「项目参数（开工前必填）」表（§P），§P 为空的动作必须先问 Owner；正文改引用 §P。跨项目长期规则（界面铁律、预览窗口规范、git 纪律、AI 候选底线）留在正文不参数化。收尾断言：grep 旧项目专名（业务名词/框架名/编码值/拍板日期）=0。**新拍板纪律与旧规则冲突时按最新指令改写原句（不留 UPDATE 追加段），冲突取舍在汇报里显式说明**——例：FR 分组从「能力树、CRUD 仅组内检查表」改为「CRUD 决定分组」时，同步保留流程/状态机型模块的流程段例外并向用户点破。
2. **宪法通用化**：判例编号引用（FR-xxx/SC-xxx）从原则正文剥离（新项目无判例），原则改通用业务语言重写；「交付与流程治理」加一行首期范围（按用户拍板）；Version 1.0.0、Ratified 用新日期。
3. **范围 clarify 一轮批量问齐**：4~5 问（系统定位给谁用/业务模式/与姊妹系统的数据关系/宪法来源/要不要开源参考），推荐项在前；choices 只能是纯字符串列表（说明文字内联在选项里，传 {label,description} 对象会被 schema 拒绝；用竖线把多个选项拼成单个字符串同样被拒——每个选项必须是数组的独立元素）；用户自由文本覆盖选项框架的（如「第一期只做 X」）即最终范围，总纲 Assumptions B 组编号留痕；**用户跳过某问＝按常理默认值落地 +【待复核】编号清单交后置复核，不再问、不阻塞**。
4. **总纲先建再建模块，蓝图编号要预留**：首期不写详细 spec 的后续期业务（租约/计费等）在总纲模块索引表锁预留号段（如 030~039、060+）并写明「首期 MUST NOT 占用」——否则后续插模块时全局唯一编号被首期填满。首期无用户故事的总纲文件合法（US 全在模块里），G1 覆盖率核对时总纲不计 US。
5. **全套 spec 落盘后一次 execute_code 终检**（新写仓库版，先于 commit）：①FR 定义集合全局唯一无重复、每条含 MUST；②SC 权威定义只出现在总纲（模块仅引用）；③NC=0；④实现层措辞=0；⑤跨文件 FR/SC 引用全部命中定义集（幽灵=∅）；⑥>200 字行=0；⑦FR 区粗体分组标题逐组打印，人工核＝实体/流程段的 CRUD 集合、无页面/控件组；⑧逐模块 US 计数与总纲模块索引表一致；⑨总纲模块索引表的 FR 段范围与各模块实际定义号段逐模块比对（手抄范围易 off-by-one，如写 010~024 实际到 023）。
6. **用户回「其它默认」＝批量确认待复核项**：总纲 B 组记一条覆盖式决议（逐项列默认内容），各模块把【待复核】标记替换为对该决议编号的引用，然后全库断言 `【待复核` 残留=0（Updated 修订记录句里的历史提及除外）；后续某项被单独推翻时改这条决议并同步受影响模块，不新开重复条目。

## 多轮增量拍板修订 pattern（同一天用户连续追加范围/改判；项目B B13/B14 两轮验证）

SDD 项目 spec 落定后，用户常以「新增功能 + 确认/推翻上轮【待复核】」的混合清单回稿。按轮执行，不整篇重写：

1. **冲突先扫后写**：新指令落地前，把与既有 MUST/MUST NOT 逐条对撞（本轮实例：新「批量处理」撞旧 FR「MUST NOT 提供批量放行入口」）。取舍规则：**只废除被点名推翻的那半句禁令，同条内未被提及的安全禁令原样保留**（自动处理/撤销入口的禁令仍在），并在汇报里明示「你没让放我就不放」让用户可一键再推翻；B 组被取代条目加「被 BNN 取代」注记留痕，不删史。新属性 vs 全局无感知条款的变体冲突（用户给实体加「来源平台」类枚举留痕属性，而既有铁律要求界面对来源无感知）：两全保法——属性 MUST 落库为数据层留痕、界面 MUST NOT 增展示/筛选控件，取舍写进 FR 注记并在汇报点破「要展示另行拍板」。
1b. **用户「FR-XXX 不要了 / 去掉 X 功能」＝废止三步**：①该条款转 MUST NOT 负向句原地留位（编号永不复用，防后来模块拿同号写新功能）；②全链清痕：US 场景（删行处留注释「场景 N 随 FR-XXX 废止，跳号不重编」）、Edge、Key Entities 承载属性、原型的行/筛选项/按钮/文案同轮扫净——如废止「源已下线」后列表不再有灰行与下线筛选，对象改按普通状态呈现；③B 组记取代关系 + 溯源表加行。
1c. **机制替换型拍板（新规则顶掉旧机制，如「按 md5(字段组合) 排重」取代「同事件去重」）三连**：①用户拍板句逐字入 FR（零虚构优先——即使原句含实现级词也不能洗成业务语言，泄漏词扫描按行语境豁免：含拍板/取代/指纹等判定语境的行放行）；②旧机制的散落措辞（FR 子弹、US 验收场景、SC 断言行、Edge）同轮全部改写到新口径并加废止注；③把新规则**静默改变的既有语义**显式列给用户（如旧「恢复后新事件新预警」→ 新「处理完毕后再触发＝指纹变化可新插入；未处理期间再触发被拦」），Owner 可当场推翻；④**输出字段来源扫描**——改写输入侧条款不会自动覆盖输出侧措辞：旧机制负责计算/填充的字段（内容摘要里的起点时刻、计时口径、SC 计量起点、时间窗组合规则）在新机制下断源，逐个找出处定义补拍板；漏网的会在后续 checklist 暴露，宁可当轮扫出。
1c-3. **拟定机制经复核转正时的清扫**：Owner 批准拟定方案后，所有落点的「拟定/采否待复核」措辞翻正为定稿；**主句若曾逐字引用 Owner 旧字面公式（零虚构承接进过 FR），转正同轮把主句改写为引用新机制＋转正史编号链（B24→B50→B52 注记留痕）**——主句字面公式与子弹新机制并存＝两条打架规则，实现会话会照主句写码。转正落点清单（判例/模块 FR/data-model 注释/checklist 注）四处一次扫平，缺一处下轮又被当待复核项追问。
1c-2. **字段改义型拍板（标识属性换语义来源：「同步落库」→「本系统自动生成唯一标识、恒非空」）**＝FR-011 匹配键连带规则的触发器，三件套一个别漏：①同步匹配键改指真实来源键（平台标识）+「来源键↔本地生成号」映射列（HOW 列入 data-model 非实体属性节，生成号不参与批次匹配）；②凡「经该标识关联/解析」的链路（绑定翻译、搜索解析）同轮改双跳；③检索面按 Owner 点名扩展（列表搜索关键词集合只改被点的列表，未点名的列表不动=零虚构）。收尾断言：旧「X 同步落库」措辞在被改义实体清零。
1d. **头部字段行（Updated / Why this priority / Independent Test）是多轮 patch 的连环损伤高发点**：版本行就地续写易产出跨版本拼接残段（两轮 patch 半句相撞），整块替换叙事区又易把别的 US 字段误抄进来。规矩：这类单行字段每轮整行替换不追加；终检加两项——Updated 行通读无拼接痕迹，逐 US 的 Why/Test 主语与本故事内容对表（US 计数正确不代表字段没串行）。**批量 rep() 循环的非幂等插入会把判例块/溯源表行复制成相邻重复对**（重试轮再插一次、对账脚本只验「替换成功」不验「插入幂等」都会中招）：终检加 `s.count(判例标题)==1`、表格行按 Counter 查相邻重复；修复重复对时与本轮新拍板同 commit 落，并在 Updated 行注明「修复重复行」——静默删史会丢判例，静默留双会让编号盘点翻倍。
1e. **新拍板作废多条既有 FR 机制且处置方向无法从原文推得 → 动手前先发一轮定向 mini-clarify**：硬红线类指令（如「轨迹唯一来源=外部平台、本系统不做轨迹计算」）会同时顶掉既有「自动周期采集并写日志」与「本地由点位派生展示量」两类机制，收窄还是废止每条后果不同、牵动 FR/US 场景/KE 注记/契约多面改写。做法：≤3 问，每问**引用冲突双方条款原文**+列可行处置选项（含推荐的折中口径，如「点位不合成、允许点级派生时长/里程」）；用户自由文本答案（如「两属性存放不同、都要保持新鲜」）按最新指令定案，口径以「Qx 口径」标注写进 B 组判例与 research 新 D 节，再同轮级联改写。绝不二选一静默改——选错=全连带面返工，且用户会在 checklist/评审时才抓出。
1f. **抽象归并型拍板（用户提新父/子实体替代既有实体的留痕职责，如「同步日志抽象为任务中心：主任务+子任务」）＝结构重构不是加字段**：先按 1e 发定向 mini-clarify（每问引用冲突条款：与既有逐轮机制的衔接方式／各任务类型的形态／界面红线是否反转／旧实体六字段如何处置），然后五步闭环——①新实体属性清单逐字入 Key Entities 与总纲实体清单表（标「用户原文逐字」）；②写**旧实体字段映射条款**（旧每个属性→新哪实体哪列承载，逐字列出），旧实体行移除但留划线留痕，B 组历史拍板原文不回改；③新机制**只反转旧红线的被点名半句**（如「不展示进度」半句反转、'不展示逐条明细'保留），反转范围与新保留部分都写进同一条 FR 并明示取代关系；④data-model 表替换、契约端点、原型新页+全站导航、quickstart 场景、SC 口径同轮全换，不留双轨；⑤用户属性清单没给的 HOW 细节（如三态里没有「执行中」）用实现列/HOW 承载＋【待复核】登记，MUST NOT 擅自扩枚举值域。
1g. **属性移除型拍板**（用户说「列表都不显示X；关于<实体>的信息只显示 <字段白名单>」）：语义层级按后半句范围判——给了完整字段清单＝**实体级属性移除**（KE 清单、data-model 删列、契约响应字段、原型列与示例数据全改），不是仅列表隐列；移除前先 grep 属性全部用途再按面处置：①展示面清零；②**计算面重定义**——由该属性参与组成的东西（如 md5 匹配键公式、快照子数组、"编号与名称"式任务内容行）逐一对冲改公式/改承载字段，替代要素（如用车牌号顶替名称作展示名）属推导标【待复核】；③依赖该属性的悬置【待复核】项**自动关闭**并明示（名称属性删除→"别名是否充当名称要素"议题消亡）。历史实体清单原文不回改靠注承接（命名史惯例）。
1o. **「记一下」型口头指令与当日判例冲突＝两阶段落，不即时执行**：Owner 说「记一下」而该指令推翻当天刚拍板的 BNN 判例时——①第一阶段零代码动作：HANDOFF 新开「待拍板需求」区登记一条（指令意图＋与哪个 BNN 冲突＋拍板后的完整回退步骤清单＋不受影响的已定正确性面），回复里显式呈报冲突与「最新为准」取舍；②Owner 回「执行」才按 1c/1h 替换型 pattern 全链落地，登记行同步划掉标✅。判例链覆盖注法＝被覆盖 BNN 原文不回改、行首加「〔已被 BNN 覆盖废止〕」，版本史两行并存（旧 B 一行＋新 B 一行注明取代），测试与原型注记同轮改判到新口径。Owner 若改主意，删登记行即可，判例体系零损伤——这正是「记一下」不进 spec 的原因。
1h. **判定源替换型拍板**（如地图路由判据「设备国家→访问者IP」）：research 对应 D 节只换判定源、方案骨架（双商/后端收敛/前端加载）不动，旧方案降入 Alternatives 标「被 BNN 取代」；spec 承载句同轮改，旧判据的依赖物（如「国家=CN 精确匹配」风险项）当场降级改写；被换下的属性职责收窄要在条款里显式写新用途（国家＝仅供展示与筛选），防读者以为也删了。
1j. **属性批量增补型拍板**（Owner 一次给多实体加属性，其中配置属性接管全局约定的判定职责，如「员工加工作国家/时区＋设备加时区与停留预警开关/时间段＋判定改双前提」）：①**模块归属按实体真相源不按 Owner 口述**——用户说「003spec 每日预警报告…」「003spec 停留触发前提」，但报告/预警判定实体的条款在 004 → 写进属主模块，判例里记一句归属纠正，绝不随口述归属造双定义；②只读实体（台账零人工入口铁律/SC）新增**可编辑配置属性** → 既有只读 FR 原地写「唯一例外」并限定例外字段清单，MUST NOT 只另立新 FR 而旧禁令原样留着（实现会话会照旧禁令拒绝开编辑入口）；③新增属性未给用途 → 写负向边界 FR（首期 MUST NOT 参与判定/调度/展示，标【待复核】），防实现自由联想；④判定依据从全局约定改为实体属性时，全局约定句分层改写：判定类条款改引实体属性、展示/报告/调度类条款保留全局值，两句同区互指防读者以为全局锚点作废；⑤新号占用「后续期自 X 续取」的号 → 编号纪律整句改写（已用范围＋新起点）并同步模块索引表 FR 段。
1j-2. **批次未落盘即被新指令改位＝合并落终态，不重放被废中间态**：上一批拍板的脚本尚未成功落盘（锚点失败/中断都算未落）时，新指令若重排了该批的属性设计（属性删/增、职责从实体 A 移到实体 B），MUST NOT 先落旧设计再补一轮改位——直接按终态一次性落地，判例双记：旧批判例把受影响条目标「经 BNN 改位，见下」，新批判例写明「最新为准修订旧批第 x 条」，取代关系可 grep。连带面按终态重算：data-model 列、契约端点（新增写端点给只读实体开例外时要同步改组标题的「零人工」声明句）、原型表单/弹层、旧全局口径的散落措辞（US 叙述/Independent Test/Edge/示例文案/Assumptions 拍板值注）逐处对平——拍板值换了承载实体≠该值消失，旧「用户拍板 8:00–20:00」类句要改写成新承载并注明取代。
1j-3. **多对替换脚本的锚点必须逐字来自本轮 grep 输出**：凭记忆/凭「将要写入的计划文本」拼 old_string 必 MISS（脚本 assert 中止后，已按文件逐个落盘的 ok 不回滚——touch() 函数级原子、跨文件不原子，报错后按脚本 stdout 的 `ok <path>` 清单核对哪些落了盘，只重跑未落文件且重锚盘上现文）。new_string 永远不许是占位符/「稍后修正」的自造文本——占位对一旦锚点碰巧命中就是内容毁伤；拿不准锚点就先 grep 再写脚本。
1n. **属性改名+语义反转型拍板**（如「停留超时预警开关→总预警开关且默认从关翻为开」）：改名之外必带三道拍板——①**存量行迁移口径**（默认值翻转后大量存量 0 是「没动过」不是「想关」，值平移还是按伴随属性重建意图，列选项交 Owner；Owner 可一句「项目未上线，直接改」整体豁免此问——豁免只免①，②③④仍需逐条拍板）；②**拦截/作用范围的新旧差集**（新语义覆盖旧语义未触的动作，如总开关拦离线+停留而旧开关只拦停留，历史数据可见性也要定）；③旧机制先例的规则平移声明（必填/清空/权限/审计四条沿用或推翻，逐项点名）。④需求涉及**新实体且数据源在外部平台**时，先核平台契约有无对应接口再定形态：无接口＝本地同步 diff 派生，起算点与不可追溯历史写进 Edge 明示，别默认「同步就能拿到全量历史」。⑤交 Owner 的拍板清单**超时未答＝零改动**：不动 spec 一行不建实体，汇报里声明「未下笔」并用表格重发待拍项
1k. **视图展示项增补型拍板**（Owner 说「X 视图需要额外展示 A/B」）：先做两道判定再动手——①A/B 是否已在某实体的属性清单里（在＝扩既有 FR 的「可查属性」列表，B16② 下无需人工确认新属性；不在＝走 KE 人工确认流程，不得静默加属性）；②契约响应字段表是否已含 A/B（已含＝纯前端呈现层调整，后端/契约零改动，判例里明写这句，防后来会话以为漏改）。FR 改写用「（既有判例；A/B＝BNN 增补）」式内联注保留原句主干，**同轮必改对应 US 的 GWT 场景**——场景是 FR 的验收面，只改条款会让场景与 FR 口径分叉。登记面：总纲 B 组判例（注明扩展哪条旧判例）＋模块溯源表加行＋两份版本头升版＋原型要素卡/表格增格＋PREVIEW.md 映射状态列与决策日志。实装后用临时 Playwright spec 断言新字段的**真实渲染值**（正则匹配数值/标注），不看截图。派生显示格式（小数位、坐标系标注）属实现层细节，不进 spec。
1l. **全局口径型拍板（横切展示/存储格式变更，如「所有具体日期时间带时区标注」「定位时间改时间戳存储」）**：
  - **冲突先行——新指令可能顶掉 Owner 旧定稿**：动手前 grep 既有锚点条款（如全局约定里「界面展示＝运营时区」已拍板）；有冲突时 MUST 把冲突面＋两种形态列 clarify 让用户选，**用户跳过形态题≠采纳你的推荐项**——推荐默认若会改写既有定稿，就是选错了默认。用户事后追问「为什么是 X 不是 Y」＝你选的默认与其心智模型冲突的信号。
  - **形态选项成对给**：值换算＋标注（UTC）vs 保留运营时区值＋偏移标注（UTC+8）——系统有运营锚点（8:00 报告、判定窗口按运营时区跑）时，保留值让展示数字与逻辑时区对得上、团队零认知成本，通常是正解。**双模式实现＋配置开关**（翻默认＝改一行 env 零代码改动），契合用户「重灵活配置化」偏好；换算模式的实现保留且有单测，海外场景可切。
  - **范围边界显式列**：展示层变更 MUST 把「调度/切日/判定窗口等逻辑时区不动」写进判例条款，并在同一轮 clarify 里让用户确认边界，防实现自由发挥。
  - **存储/展示解耦**：存储改时区无关形态（Unix 秒整数），展示经**单一格式模块**出口（顺手收敛散落各包的重复格式常量）；API 响应仍是带标注字符串＝前端与契约字段零改动。前端截断显示（月日时分形态）必须走保留后缀的 helper（fmtShort 类），禁裸 `slice()` 把时区标注切掉——切掉＝退回无时区歧义原点。
  - **输出形态变更会打破字符串断言**：先 grep 测试里的时间字面量/内容文案断言（含冻结进 DB 行的内容字段）同轮更新；断言期望值按新口径**动态计算**（解析→换算→拼标注）优于硬编码，跨机器时区健壮。开发库里旧二进制生成的冻结字符串要清库重造再验证，别把旧行当新 bug 追。
  - 登记面：全局约定条款改写＋新判例号（注明取代旧判例哪半句）＋契约公共约定节＋data-model（COMMENT＝KE 原文不动、存储形态注记落 HOW 字典）＋两份版本头＋PREVIEW 日志。
1m. **页面撤销/入口合并型拍板**（如「同步只有一个按钮，放到设备列表页」）：入口/布局变更＝实现层——FR 语义不绑定页面位置（「唯一入口」仍成立）时 **spec 零改动**，判别式＝换一套 UI 该条是否仍成立。清扫七处：旧路由改 redirect（旧链接/书签不断）、侧栏＋命令面板去入口、跨页文案 grep 旧页名（空态引导/提示语）、原型页删除＋PREVIEW 映射行并入接收页＋决策日志、e2e spec 的路径与按钮文案、DESIGN.md 导航节补拍板条款、quickstart 操作文案。常伴生**列表列收敛＋详情弹层**反馈：主列收敛回界面铁律口径（≤6），被砍字段进详情弹层（行主键可点＋操作列详情按钮、弹层展示实体全属性＋未处理行弹层内可直转处理），API 契约字段不动＝纯呈现层；PREVIEW 记「实现层收敛」日志（契约字段全保留是判据）。
1i. **新建模块型拍板**（用户说「增加一个 005 模块 X」并给功能点）＝十二处联动，缺一处后续会话就按旧结构走：①specs/NNN-slug/spec.md 新建（标准章节齐全＋Owner 指令原文逐字入判例）；②001 模块索引加行、原「005+ 蓝图」行改「006+」；③**后续期预留号段被新模块占用时编号纪律整句改写**（「086+ 原留后续期，经本轮指令改用现期，后续期自 090 续取」），MUST NOT 静默消耗预留段；④新模块实体若是纯派生统计视图，实体总表登记行标注「派生只读、不落库」（零新表时 data-model 不动）；⑤溯源行；⑥判例段（推导口径逐项标【待复核】）；⑦Updated 升版；⑧新模块改变既有模块行为（如登录落地页改指工作台）→ 相关模块 FR/场景同轮加引用注，不在两边各写一套；⑨原型新页＋全站 topnav 批量插入口（见校验断言第 4 条补：锚正则须容忍 class=on）；⑩quickstart 场景表第一列是行序号不是 US 号——新 US 按其位置插入后**原占该序号的行（如「8 越权矩阵」）必须顺延重编**；⑪PREVIEW 决策日志；⑫终检 FR 数==旧集合＋新开号段、导航集合断言页数+1。派生统计页的示例数字从既有原型页反推对账（设备/预警行数），不给新页另造样本——三向对平同样适用新页。
2. **用户点名新实体与既有名撞车 → 显式命名区分条款**：如用户把每条预警记录定名「预警报告」，而已有导出物料叫「离线预警风控报告」——在总纲加一句命名区分注（两词在 spec/原型/界面 MUST NOT 混用），不擅自改名也不混用；受影响列表/详情/物料三处列名同步对齐用户属性原文。
3. **用户给的实体属性清单逐字承接，但派生/系统留痕属性要分层标注**：Key Entities 写成「用户确认 N 属性（逐字）」+「系统留痕（非用户清单，引用判例 FR）」两段子弹——既锁域模型又不假装快照/结果字段是用户定的。
4. **取号跳过预留段并回写编号纪律**：存在编号预留段时新 FR 从预留段之后续取（…052→060、061~070→071/072），总纲编号纪律加一行「后续期新号自 X 续取」，模块索引表 FR 段同步；改完必跑「索引表范围==各模块实际号段」的 off-by-one 断言（本 pattern 首用即抓到 010~024 vs 实到 023）。
5. **每轮闭环 = 定点 patch spec → execute_code 全库终检（FR 集合/幽灵引用/长行>200 拆子弹/待复核清零/用户属性清单逐条断言存在/Updated 行与 US 字段行无拼接串行）→ spec 自动驱动原型：受影响页重写 + 未变页版本标注批量 replace（spec vN 驱动）+ 与重写页对平的其它页计数重算 → PREVIEW.md 映射表与决策日志 → 一次 commit+push**。新增页面（如报告页）时同步给全部旧页插 topnav 入口并跑导航集合断言。**重生成任何页面后必须回扫全站**：顶栏导航集合（新页入口插回旧页）、版本标注、与它数据对平的其它页计数——重写页会静默丢掉这三处增量。
6. **交 Owner 拍板的清单每条必须自带人话解释**（用户对纯术语条目会直接回「没看懂什么意思」）：每条写三件事——这是什么（用业务场景举例，不用列名/类型术语）、为什么需要它、砍掉会怎样；技术名词首次出现就地括注。清单不是枚举缩写而是可决策的问句，判据＝不懂实现的人能逐条回答"保留/砍掉"。
7. **全局术语改名要走「替换→搭配顺化→grep 残留→白名单放行」四段**：机械 replace 后先通读含新词的句子——新旧词词性/搭配不同会破句（如「生成X报告一条」换词后变「生成Y一条」缺量词，应顺化为「生成一条Y记录」），顺化完再扫残留。残留句要分类——B 组拍板记录里「弃用 X 术语」的禁令句、Updated 行的改名说明、定名史原文是合法历史留痕（保留），其余清零；改名词同时同步所有引用面（spec 编号纪律行/原型导航/对平注/trace 标签/物料文件名注），漏一处下轮用户一点就破。撞名合并（两个概念归一术语）时写「同名两用+注记区分」条款并让界面词直接说人话（按钮写「生成预警报告」不写系统名词）。**新词包含旧词（X→定语+X 类，如 平台→开放平台）时，机械 replace 必产叠加伤**——用负向后视正则 `(?<!开放)平台` 替换，改完断言两组：旧词残留=0（历史留痕白名单除外）且叠字串（"开开放/外部外部"）=0；**清扫后同轮及后续所有 patch 的锚点必须重新 grep 盘上现文**——锚句里的旧词已被扫描改掉，凭记忆取旧原文必 no-match 或 fuzzy 撞错区（与「同文件连环 patch 锚点漂移」同根因，全库清扫是其最高频触发器）。
6. **用户把整轮待复核一次回「其它默认」= 覆盖式决议**（冷启动节第 6 条在多轮场景同样适用）：B 组记一条逐项决议，各模块【待复核】替换为对该决议的引用，残留断言=0。

## Clarify 阶段执行 pattern（/speckit-clarify 实跑验证，项目B 2026-10-15）

官方命令模板要求逐问交互、每问等答再问下一问；本项目按用户习惯（批量拍板）一次 clarify 调用打包 ≤5 题、每题推荐项在前，一次 submitted 拿全部答案——题间独立才批量，某答案会改变后续问题含义时仍逐问。**choices 在任何 clarify 场景（不只冷启动范围问）都只接受纯字符串数组——传 {label,description,preview} 对象数组会被 schema 拒绝；选项说明内联进字符串本身**（本 skill 冷启动节第 3 条同款错误在修法拍板类提问上复发，两处同规）。**升级形态：载荷已确认良构（纯字符串 choices、对象数组形状正确）仍连续 2 次以上被同一 schema 报错拒绝时，停止重试表单——把选项编号列成正文文字发给用户回编号拍板；重试循环只烧轮次，文字选项与表单对用户等价**（触发 loop warning 即已到该判据）。执行要点：

1. **问题队列来源＝现存开放标记，不是重扫全类**：`grep -rn "待复核\|由 plan 定\|NEEDS CLARIFICATION" specs/*/spec.md` 收集（spec 多轮拍板后 NC 通常已=0，开放项以【待复核】与"阈值归 plan 定"形式散落）；按 (影响×不确定) 取前 5 高影响项，低影响项（邮箱分隔符之类 HOW 细节）不占额度、直接归 plan。
2. **用户可用自由文本推翻整题选项框架**（实踩：容差半径五选项，用户答"从第三方平台同步停留时间值"＝判定输入源整个换掉）：按最新指令定案处理，同轮级联——FR 定义重写 + Edge 改口径 + Key Entities 属性来源注记 + 总纲全局约定行 + 受影响原型页（示例数据/标签/注记）+ PREVIEW 决策日志；被推翻的"由 plan 定"条款原地写废止线（编号/条目保留），Assumptions 里【待复核】项被确认的改写成"Clarify Cx 确认，不再是假设"。
3. **每份被触及 spec 加 `## Clarifications` + `### Session YYYY-MM-DD`**（放 `## 溯源` 之前），每答一条 `- Q: … → A: …` 子弹；跨模块结论在总纲记一条汇总（覆盖 002/003/004 时），各模块记自己那份。总纲 Updated 行升版本注 clarify 结论。
4. **收尾断言**：全库 `【待复核】` 残留=0（Updated 修订史句里的历史提及除外——grep 定位后逐个判语境）；章节结构存在性断言（## Clarifications/## 溯源）；`check_preview_consistency.py` PASS；commit+push 验证 HEAD==origin。
5. 过了 G0'（NC=0＋待拍板清零）才进 plan；plan 前置材料（栈/平台/凭据通道/部署）**不属于** clarify 额度，归 plan 首轮批量问（见下方 Plan pattern 第 2 条）。
6. `checklists/requirements.md` 不存在时清单复验步骤静默跳过，如实写进完成报告而非略过不提。

- **contracts/api.md 纪律（用户 2026-10-15 项目B 拍板，plan 阶段产物）**：api.md MUST 是**完整接口文档**非端点速查表——五段：①公共请求头+请求体约定 ②公共响应头+响应体约定 ③认证约定 ④错误码约定 ⑤逐接口文档（所属模块/名称/描述/路由/方法/可选请求头/请求体）。**每个 header 与 payload 字段四列齐：字段名称、字段类型、字段备注、是否必须**，禁只写示意 JSON。响应统一信封 `{code:int, data:object, message:string}`、**code=0＝成功**、错误码表列全（HTTP 双轨映射）。文件级例外显式声明（如 CSV 流不走信封）。写完跑机械断言：五段标题、每接口六要素、字段行计数、code=0 声明；旧速查式文件整页重写非 patch。**整文件重写的 stale-read 守卫（对 api.md 与 platform 契约文件通用）**：本轮只分页读过、或 read_file 去重命中返回「unchanged / 无内容」都算没见过全文、write_file 必拒——先 `git log -1 -- <file>` 确认无未提交历史后 rm 再 write_file 一次过，别反复重试读。
- **共享枚举端点 MUST NOT 携带单一消费方的固定项**（项目B B67 拍板）：值域类端点（如国家下拉 `/countries`）常被 ≥2 个筛选页＋1 个表单页共用——某一消费方的「固定默认选项」诉求（如「中国」置首）MUST NOT 服务端注入端点返回值（其余消费方全部得到永远筛不到数据的选项，违反『值域＝真实集合』条款语义），正确形态＝端点保持纯值域并在契约描述写明「MUST NOT 含固定项（BNN）」、固定项由提出诉求的那个页面在装配层叠加（置首＋去重）。协作 agent 已服务端注入时的纠正顺序＝判例先行（新开 BNN 记冲突与取舍）→ 契约描述 → 代码回退 → 集成测试改锁「无对应数据时端点不含该固定项」；纠正 commit 后主动对 Owner 点破生效链路（对方 agent pull＋重建前线上仍是旧码）。
- 模板 templates/AGENTS-generic.md 已同步 contracts/api.md 纪律。

### Implement · 显示值 vs 存储值的「精度/坐标/时区」争议排查（项目B 2026-10-19 验证）

Owner 质疑「库里数与页面数对不上/是不是精度损耗」＝三类病同症状，先取证分类再改码，别默认是精度：

7. **量化取证代替口头保证**：用真实形态值在 scratch 复刻整条链路（ParseFloat → DECIMAL(10,6) 舍入模拟 → JSON 往返 → 坐标转换+round6），逐步打印误差量级出表（float64 ~1e-15°≈纳米、列 6 位小数 ≈≤5.5cm、JSON 往返=0、出口 round6 有意收敛）——结论带数，不空谈「双精度够」。全链路先 grep `float32` 与裸转换点，确认无窄化才进下一步。
8. **坐标系错配的指纹＝偏移数百米**（亚米级才是真损耗）：境外坐标被强套中国境内定义的加密偏移链（GCJ02/BD09 固定 +0.0065/+0.006）。审式：守卫 MUST 在转换链入口（`Export` 级），只挂中间一步（GCJ02 的 outOfChina 直通）会留后半链无守卫＝系统性偏移。修复形态＝境外落点原样透传 WGS84＋出口 struct 携带**实际坐标系**字段（Coord.CoordType）如实上报，调用方不得按 map_type 静态推导 coord_type（两值会解耦）。
9. **改判类拍板把「数值正确性」与「路由判定」分开回退**：Owner 说「显示不对」未必两层都要动——守卫（数值）保留、路由（选哪个地图商/SDK）可独立被覆盖；判例链写清覆盖关系（B68→B69：路由回纯员工属性、坐标守卫保留＝「回退不重新引入偏移」）。
10. **时间戳争议＝一个整数三种读法**：`date -u -r E` + `TZ=Asia/Shanghai date -r E` + `TZ=<当地> date -r E` 并排，外加 `SELECT FROM_UNIXTIME(col), NOW(), @@global.time_zone FROM DUAL` 探 MySQL 服务器实际返回串（库会话时区与展示时区可能同为 +8）；存储 Unix 秒＋标注形态（B58/B59）下「UTC 06:54=北京 14:54=塔什干 11:54」是同一瞬间，Owner 拿别的时区心算就会报「不对」。判平台串时区归属：拿行驶中设备的最新 gpsTime 与三时区当前时刻做秒差对比，贴哪个时区即归属。
11. **回归锚用线上实例的具体值**（设备编号+库值+期望出口值写进测试名）：判例改判只改断言口径、不重取数据。
12. **`gofmt -l` 的输出含存量违例**＝他人/历史遗留，只对本次触碰文件 `gofmt -w`，勿顺手动无关文件（扩大 diff、撞单写者文件域）。

## 第三方平台对接契约 pattern（contracts/platform/，plan 阶段，项目B 首跑）

用户给出外部平台文档 URL 并要求「适配层接口契约伪代码 + 用到的 API 全量文档进 contracts」时：

1. **抓机读源优先于渲染文档页**：开放平台文档站常直接暴露 OpenAPI/Swagger JSON（先 curl 文档页源码找 JSON URL 或试 `/openapi.json` 类路径）；下载后本地 Python 按接口 path 逐个提取 parameters/responses/嵌套 schema，比抓 HTML 全文更完整且无需登录。渲染 SPA 文档壳页（无 SSR）是低效路径——bundle.js 里 grep 不到接口数据。
   **但定论「需登录」前 MUST 穷尽 URL 变体**：Owner 说「我没登录也能看」时，按其给的原始 URL（含协议原样）直接 web_extract——http 与 https 可命中不同渲染路径（一侧出 SSR 正文、另一侧只回 SPA 壳/bot 墙），单一 scheme 失败不构成「需登录」的证据。反向也成立：**用户「我能看到」≠ 内容在 HTML 里**——用户看的可能是渲染后页面，无登录墙时 served HTML 仍可能是空壳；凡壳页确认＝SPA，字段表全量一律走 chunk 逆向，@url 投喂的渲染文本作互证不作替代（渲染文本会丢版本字典等页面不可见数据）。
   **React SPA 文档站的字段表无需登录也能全量提取（项目B 平台实测）**：子页正文内联在 webpack 异步 chunk 里（umi 系是每接口一个 `{field:"…",dataType:"…",require:"…",example:"…",explain:"…"}` JS 数组）。步骤：①curl 壳页拿主 bundle URL；②在主 bundle 的 loader 函数（`.u=function(C){return"static/js/"+{名表}[C]+"<版本段>"+{hash表}[C]+".chunk.js"}`）里**逐字抄全部三段拼接**——name 字典、版本段字符串字面量、hash 字典——拼 chunk URL；勿凭常见格式猜（点段数量/版本段位置猜错＝100% 404 空转，本 session 实踩两轮）；③批量下载全部接口 chunk，正则提内联数组＝一次拿到全站端点清单+字段表+各接口版本字典。chunk 是页面数据源，比人贴的渲染文本更全（含页面上看不见的旧版本数组）。
2. **三件套结构**：`contracts/platform/adapter.md`＝Adapter interface 伪代码（每能力一方法）+ 归一化 DTO 定义（每个 DTO 标注落哪张表/哪些列）+ 同步编排流，伪代码硬约束逐条对齐 spec 拍板（批次上限、覆盖写、唯一数据来源红线——业务逻辑 MUST NOT 进适配层，适配层只产 DTO）；每平台一个 `<platform>.md`＝鉴权算法（签名公式写全）+ 所用端点逐一四列字段表 + 平台字段→DTO 映射注 + 显式「其余 N 端点本期不接」清单。
3. **平台文档抓不到＝零虚构占位，不猜字段**：占位文件 MUST NOT 按平台名或同类产品臆造接口；把文档站 URL/路径结构透露的形态信号登记为**结构性风险**（如路径含 `interfacePush`＝可能只有推送回调，与「本期只主动请求」拍板直接冲突），列为登录后第一核实项，并预列核实后需补的条目模板。
4. **「文档未声明」的东西单独成「联调核对项」节**：令牌传递位置、字段单位（停留=分钟还是秒）、轨迹时间跨度/回溯限制、分页上限——这些实现期才炸的点，契约阶段逐接口如实登记，不写死假设。
5. **平台字段缺口逐条【待复核】交 Owner**：外部字段对不上内部实体（如平台无设备编号/国家字段、状态枚举映射不到本地态、同一语义有两个候选取数口径）＝给「建议口径+影响面」列成编号清单让用户拍板，MUST NOT 静默映射或留空绕过；拍板前 data-model 不落该映射。
6. **需登录文档的抓取路径**：用真实 profile 浏览器时，本机 Chrome 在跑会占住 profile 锁——不重试硬闯、不绕锁拷贝用户浏览器数据；给用户二选一（A 完全退出 Chrome 后我起浏览器到登录页停手、用户人工登录后我再抓；B 关 use_real_profile 走云端浏览器、用户在窗口登录一次）。凭据仍走 vault 纪律，代理不转录。走 A/B 之前先执行第 1 步的 scheme 变体检——多数「登录墙」其实是协议/渲染路径误判。
7. **拿到平台文档的第一动作＝配额与全局前提对账**：开放平台首页常带「访问配额」表与「对接须知」（坐标系等），逐行对撞 spec 的周期类 FR——刷新频次 × 设备存量 ≤ 日配额该节奏才成立（实踩：定位配额 8640 次/天 ÷500 台≈17 次/台/天 → 「每半小时自动刷新」在该平台不成立），冲突登记为 Owner 拍板项并预列候选（统一降频 / 按平台分档 / 找平台谈提额）。文档声明的坐标系与入库基线一致时直接闭环对应 plan 风险项并写明闭环依据；此前凭 URL 路径语义登记的结构性风险（如路径含 interfacePush 推断「只有推送回调」），文档到手后立刻以正文证据复核销项，MUST NOT 让推断风险在证据出现后仍挂账。SPA 子页字段表拿不到时：先走第 1 条的 chunk 逆向，仍拿不到才登记逐接口缺口清单（需要哪些页、供 Owner 逐页 @url 投喂），不臆造字段。
7b. **配额冲突结论前 MUST 先核实接口调用形态（单车 vs 批量/全量）**：用「频次×台数 vs 日配额」判周期类 FR 不成立之前，先确认该接口是逐台调用还是整账户一次返回——形态误判会让风险结论整个反转（实踩：定位配额 8640/天先判「半小时全量刷新不成立」，子文档到手发现是批量全量接口＝48 次/天远低于配额，风险撤销）。撤销旧风险结论时同轮改写登记处（契约+核对表+给 Owner 的播报），不留矛盾两版。**契约声明句＝联调前假设**：文档写「N.0.0 版含字段 X」而真实响应无 X、声明整型实为中文串这类落差实测频发——凡下游逻辑依赖某字段存在/类型，联调当场以真实响应回写契约注记（「与真实响应不符」句留档），别默认声明成立；下游按「字段可缺失」编程（omitzero/RawMessage 容忍）。
11b. **平台契约文件只有一个权威位置**（`specs/NNN-总纲/contracts/platform/<platform>.md`，与 adapter.md 互链）：协作 agent 被 Owner 口头确认后在仓库根另建平行 `contracts/` 副本＝双真相源，权威文件仍写旧映射会误导实现会话——发现即：映射与实测注记合并回权威文件（注「并入自根目录副本，日期」）、删根副本单独 commit、汇报与 HANDOFF 点破该流程违规（对方同样能看见）。
8. **「一律用最新版」是复核触发器，不是版本号替换**：Owner 拍板版本指令后，先分两种版本体系再 diff：**平台无全局版本字典时（OpenAPI info 无 version 字段），「最新」＝端点代际——全端点清单盘点 `path` 的 /v2 类后缀、v1↔v2 字段集对比、v1 系显式标禁用**；有版本字典的平台对每个接口做**逐版字段集 diff**（chunk 里 `{"2.0.0":[…],"3.0.0":[…]}` 各数组取集合差），三类后果逐一核：①旧版字段曾作为闭环依据而**新版已移除**的（键来源、单位标注类——实踩：deviceId、注明"秒"的 stayTimes 均在 3.0.0"返回值优化"被删）→ 已登记的 ✅ 结论 MUST 主动降级为待核并报告，不得让旧版字段撑着假闭环；登记字段依据时当场注明所据版本。②鉴权入参跨版换代（password→固定 secret 类），契约按最新版定稿、旧版仅存档注记。③全局 Version 头取值与公共表示例滞后矛盾时按子页实际版本为准。④Owner 裁决「缺字段先假数据占位、联调验真」时：占位值 MUST NOT 参与唯一键/匹配键（匹配改用真实存在的平台键），假号生成后保持稳定防每轮同步重复插档（稳定性细节标【待复核】），联调项写明「真实响应含该字段则弃假号」——占位是契约层 HOW，不回改 spec 需求文字。交付形态：Owner 要的是**全站接口版本矩阵**（三版并存/两版/单版分组+每接口最新版差异），不只所用那几个；批量 chunk 逆向顺手就能盘全。
10. **Owner 契约评审批次（方法签名级裁决）＝契约与 spec 双向改写**：Owner 拿到 adapter 伪代码后会给出改名/入参形态/数值上限/窗口与入库语义的批次裁决——契约是第一落点（接口与 DTO 注释逐条标 BNN），但 MUST 反扫 spec 面：批次上限这类数字同时活在 003 FR、research、plan 源码树注释、原型注记里；窗口/覆盖语义若取代历史判例（如「可查全量历史」），003 Assumptions 与 004 FR 同轮改写并在判例记取代关系，不留两版并存。两个伴随动作：①**裁决数值与平台实证对账后分层措辞**——Owner 说「size 调 200 因为某些平台有单请求限制」时，spec 落「本地批次上限 200、各开放平台按其声明上限取小执行」（附实证值，如 iop 分页类 100、某平台台账接口不分页不受限），MUST NOT 写成「所有平台支持 200」；②**契约评审面＝残留旧机制措辞的又一收集点**——本轮重写契约时抓到过查看端点仍写「按需触发同步」＝更早判例前的旧口径，修正时契约与 spec 两面成对登记。契约签名保持数组语义：开放平台没有对应批量能力（详情/轨迹只有单车接口）时不改签名，在实现层拆批逐台调用＋组失败隔离，契约写「拆批语义」注。
11. **每平台契约文件头部 MUST 有「Adapter 方法 ↔ 本平台 API 映射表」**（Owner 评审要求）：逐条列 Adapter 接口全部方法（含 Code/Auth/单车兜底/停留辅源这类辅助通道），每方法标注所用 API＋切组上限/配额/联调待核注，表尾注「其余 N 端点本期不接」排除清单；adapter.md 另设方法×双平台总览表（正向），与两平台反查表同轮维护。方法改名/新增时三张表同轮改。
12. **匹配锚与开放平台原生键分家 & 配置注入属性**：字段缺口拍板后常带出两种配套形态——①本地匹配键若为派生值（md5(字段组合) 类），后续请求开放平台 API 仍需要的平台原生字段（vkey 类）MUST NOT 按实体逐列建名，收进单一 JSON 容器列（HOW 列，按 data_source 编码分子对象、合并写、结构说明进 JSON 字典节不进 COMMENT），两键各司其职——写进 adapter 伪代码 DTO 与 data-model 两处；②凡两平台都无法提供的实体属性，Owner 可裁「配置注入」通道（.env 一组 apiKey/apiSecret 绑定一个属性值，同步落库时由适配层按所用密钥组写入，与 data_source 同机制）——向 Owner 提缺口清单时把这个候选摆上，绝不静默置空或硬造来源；注入类属性同样 MUST NOT 开界面编辑入口（台账只读纪律不破）。组↔值的对应关系（一组密钥一国）若一个账户覆盖多值需申请多组密钥，该运营前提是契约联调项。
13. **支撑度体检 pattern**（Owner 令「分析契约方法响应字段是否被各平台映射的 API 响应字段足够支持」）：产出＝逐方法×逐 DTO 字段×逐平台的「支撑/缺口」对账表，缺口编号（G1/G2…）并附候选处置呈报——**只呈报不擅改既有路由裁决**，契约留「要改说一声」注。**头号错源＝凭字段名猜语义**：时长/时间类字段必须按平台字段说明原文对语义（如 offlineDuration＝离线时长、statusTime＝状态开始时间戳——都不是停留时长；据此才发现更早登记的「停留主源走某接口」是错映射）。发现既往错映射的处置三件套：撤销原映射措辞、相关候选恢复为【待复核】开放项、契约+adapter 核对表+映射表三处同轮对平；体检同时主动呈报对 Owner 既有裁决可能构成诱因的字段事实（如另一接口带该字段而现用接口缺），但维持原裁决不动。
14. **DTO 结构收敛裁决**（Owner 令「DTO B 字段全部融入 A 后删除 B」或「方法 X 返回字段与方法 Y 相同」）：融合改变的不只是签名，还有**消费语义**——两方法返回同一全量装配后，原「重查」类方法降级为指定对象重查/补查通道、主编排伪代码同轮改写（标注哪些字段由哪个方法填充，Page 单批即含全量则 List 不再必须二跳）；逐平台判定**装配支撑形态**并在映射表写明：单接口原生直出（响应字段齐）vs 实现层组合装配（列表字段与详情字段分属两个接口、或按声明上限切组）。三张表（adapter DTO 注释、§3.1 总览、各平台反查表）与编排节同轮统一；全库 grep 被删结构名＝0（溯源史行白名单除外）。
15b. **契约方法「实现但不接线」裁决**（Owner 说「可以先实现，但不调用（停用可没有影响）」）：签名/DTO/单测照常保留交付，消费编排伪代码处改为「无消费点、需要时一行接线启用」注记；MUST 把该方法原本供给的平台字段改指到实际生效通道并标注生效源切换，连带登记配额/成本收益；三张映射表＋主 spec FR 的装配措辞（"按数组批量查询"类旧句）同轮被编排实际形态取代，全库 grep 该方法名＝只命中契约与注记位。
15. **文档站字段表抓取完整性不稳定**：同一 URL 同一协议，一次抓全、下次关键表格显示 `...` 截断——单次抓取为空不构成「数据不存在」的结论；对 Owner 点名补采的页连续抓 2~3 次取并集，与 Owner @url 投喂的渲染文本互证，并把抓取方式（协议/日期/两次结果差异）记进契约来源注——取证链完整比单轮结论重要。

14. **标识键/同步主键字段的改判是全方向手术，不是台账映射一行**：`<identity>`→`entity_no` 类映射改动只覆盖写入方向（枚举接口一次同时下发新旧两键，正向同步照跑不误），而反向取数方法（定位/轨迹/停留）全拿库里主键当原键传平台——键一换**静默全断**，台账同步成功还会掩盖它。改标识键前四步：①枚举全部消费方向（正向同步 vs 反向以键为参的调用）列清单；②真实凭据实测候选键在反向通道的命中（旧号当键传＝「设备不存在」类错误码，原键才命中 code=0）；③文档声明的批量端点实测形态与响应结构（GET query 多值参数被平台忽略 ≠ POST body 数组被过滤；返回 data={list,total} 且元素与单台详情同构；数组顺序不保证与请求一致→映射键 MUST 按响应自带主键建；按平台声明上限 ≤N/组切组）；④存量迁移三态（有留档键＝改号并连带引用表；无留档键＝软删靠下轮重建并标【待复核】；目标号已有活跃行＝合并，注意「当前态唯一」类行——如 bound_ended_at IS NULL 的当前绑定段——改号会造双当前，应软删当前段只改挂已封闭历史段）。改判回退时数值正确性层与路由/选择层分开处置并显式写覆盖关系（守卫保留、判定改判＝「回退不重新引入错误」）。迁移测试用表名/列名照 v001 实际结构造数（alert_item 非直觉列名会当场挂），断言含幂等重跑＝空转不报错。

## Checklist 阶段执行 pattern（/speckit-checklist 首跑验证）

- 定位红线：条目 MUST 问「需求文本写清了没有」（requirements 的单元测试），禁写验证系统行为的条目；每条带质量维度标签 [Completeness/Clarity/Consistency/Measurability/Gap/Conflict] + 编号引用，引用的 FR/SC 对全库 spec 核验存在（幽灵=断言不过）。
- 首跑先一轮 clarify 定范围与深度（≤2 问：检查面/条目量级）；用户跳过某问＝按推荐默认执行不追问。文件＝`FEATURE_DIR/checklists/<domain>.md`，轻量档 ≤20 条，同类低影响 edge 合并成一条。
- 生成后全部留 `[ ]`：勾选权归 Owner（reviewer-owned 工件），代理 MUST NOT 代勾；⛔ 标阻塞项并在 Notes 写死 G2' 通过口径——阻塞项处置＝勾选或在 spec/plan 落有结论引文，非阻塞项转 tasks 遗留跟踪。
- **checklist 主要价值＝捞历史机制替换的残留冲突**：推翻型拍板（判定输入源整个换掉）之后，输出字段来源、SC 计量起点、时间窗组合规则最容易保持旧措辞（见「机制替换型拍板」第④扫）；tasks 前跑一轮把这类问题集中成待拍板清单，比 implement 中返工便宜。
- **清单生成后的结构改判会静默失效旧条目**：阻塞项⛔的引用条款被后续拍板改写/取代时，对应检查项或自动消解、或含义漂移——G2' 判「阻塞清零」前 MUST 逐条 re-check 引用锚点是否仍在现文中（grep 引用编号/关键词），失效条要么勾销要么改写重发，别拿旧清单判新 spec。**重跑（第二轮）产出分四类**：✅收口（注依据，残余属纯联调事实的移出阻塞面）；**部分解决**——冲突在一侧平台/模块闭环而另一侧仍悬的，改写条目本体分侧列明已解决面与悬空面，不整条算已关也不整条维持阻塞；仍阻塞；§E 新增项（以本轮拍板增量为核对面扫新洞，如契约语义变化破坏旧指纹链、无消费点方法的验收口径）。Notes 阻塞计数与重跑结果同步；阻塞项若被后续评审判出更强依赖（定时任务盘点发现「两个 cron 全靠时区值锚定」），当轮给该项加依赖升级注，不另开新 CHK。
- 提交前自检断言：条目数、Notes 里阻塞项计数==实际 ⛔ 行数、无 Verify/Test/Confirm 开头条目、编号引用零幽灵。
- **G2' 收口交付形态**（Owner 问「还有什么阻塞进 tasks，列出来让我选择」时）：先实测取证（checklist ⛔ 行、DESIGN.md/UI-GATE 存在性、tasks.md 是否已存在、全库【待复核】分布），再按三档分层呈报，禁平铺混列：**A 硬阻塞**（checklist ⛔ 项——每条给问题一句话＋候选处置 a/b/c＋推荐项在前＋一句影响）；**B 时序性阻塞**（UI-GATE 缺 DESIGN.md 这类「看 tasks 是否含前端」的条件闸——给出「先补产物」或「缩小首期范围绕开」两条路）；**C 非阻塞可转遗留**（联调事实项、外部凭据、低影响待复核——明示「G2' 允许留 tasks 遗留跟踪」，但其中成本低的顺手裁项要点名建议裁而非遗留，并给「X 项按下建议 a 一把拍掉即可跑 /speckit-tasks」的最小清零路径收尾。判据：Owner 拿到清单应能逐条回字母完事，不需要再问第二句"这是什么意思"（呼应"交 Owner 拍板的清单每条自带人话解释"）。
- **Owner 回"没明白/不要用黑话"＝就地重写清单条目本身，不另发一段解释**：重写格式＝具体反例（带真实时刻与数字演示冲突场景）＋决策点拆 2~3 个选项、每项"效果＋代价"一行；同域条目（同一口径引发的多条 CHK）互相标注编号、合并一次回答覆盖一片。
- **Owner 按编号回决策批次可能漏题**：漏答 ≠ 否决——维持拟定方案标【待复核】推进，在阻塞计数里显式写"待复核但不阻塞"、排任务按拟定默认并留改裁口子（改裁只动受影响的最小落点）；已答的按答案即时生效。绝不把漏答当拒绝丢弃，也不静默当采纳。

## Owner 点名的能力面盘点评审（定时任务/字段/状态值类「列出所有 X 我要评审」）

产出 MUST 三档分类＋全部从源文 grep 取证（禁凭记忆答题）：①**正式项**——逐项列 触发/动作/写范围/失败语义/溯源 FR 编号 五列，数字核算附公式（如 频次×设备存量≤平台日配额、频控下轮耗时）；②**准实现层节律**——token 续期、窗口取数参数这类系统内部时钟，标明归属层（adapter/HOW），不混进业务项计数；③**显式非项**——Owner 易误记的排除清单逐条点名（「仅手动触发」「进页实时算无定时」「随批次执行无独立定时器」），防下轮被重新问起。收尾两块：盘点暴露的依赖项回注对应 CHK 编号并升级其阻塞注（如时区值未定→cron 表达式不可实现）；给出「一句话评审结论」定调（几个真项、哪个不可实现、哪个口径冲突）。用户评审这类清单时会追问看不懂的黑话——同 checklist「就地重写条目」规则处理。

## Workflow order
**`specs/NNN-*/intent.md`（团队扩展、GI 门禁＝四段齐备非空 + grill-me＋domain-modeling 拷问至 frontier 清空；置于流程最前，细节见 sdd-speckit-research 的 team-extension 条）** → `/speckit-constitution` → `/speckit-specify` (or hand-write spec.md) →
**Spec Kit Preview (低保真原型，用户新增的固定步骤，见下)** →
**`/speckit-clarify`（用户 2026-10-14 定为必做，位置＝原型之后、plan 之前）** →
`/speckit-plan` → **`/speckit-checklist`（用户 2026-10-14 定为必做，紧跟 plan）** →
optional `/speckit-analyze` → `/speckit-tasks` → `/speckit-implement` →
`/speckit-converge`.

两步的用途分界：clarify 澄清 spec 需求缺口（NEEDS CLARIFICATION/歧义）**与原型
评审暴露的业务问题**，产出回写 spec 后再进 plan；checklist 在 plan 后对
"实现就绪"生成质量清单（阻塞项处置完才进 tasks）。用户明确纠正过 clarify
不要放 specify 紧后面——原型评审的反馈需要 clarify 收口，顺序错一步会漏
"看原型后才浮现"的问题。AGENTS.md 模板 §3 已同步为同一顺序并配 G0'/G2' 门禁。

## Spec Kit Preview（spec ↔ plan 之间的低保真原型，用户 2026-09-22 定）

项目A 项目已落地：`specs/001-项目A/preview/`（PREVIEW.md=工作流约定+
溯源映射表+原型层决策日志；wireframe.css；静态多页灰色线框 HTML）。
可复用配方（目录结构/CSS class 清单/页面骨架/校验方法）见 `references/preview-wireframe-kit.md`。

铁律：
1. spec.md 单向驱动原型；每个控件带 `US n`/`FR-nnn`/`SC-nnn` 溯源标签。
   **原型零虚构（用户 2026-09-22 硬规定）：spec 未提及的内容绝不在原型上显示**
   （搜索框/按钮/字段/状态/列都算）——用户靠原型反向改进 spec，原型上无依据
   的内容会让用户误判为已定需求。觉得该有某控件 → 先提 spec 修改建议，拍板后
   才画进原型；演示辅助控件必须显式标「原型演示用」。
   **全量审计方法（用户下此规定时跑一遍）**：逐页提取 label/button/th/状态条文本，
   逐个控件问“指得回哪条 FR/US/Edge”。处置分三类：①spec 无依据且无 FR 引用该概念
   → 删控件；②与 spec 矛盾（如示例单未提交审核但入账按钮亮、SC 指标当成界面行为画进 UI）
   → 改成与 spec 一致（置灰+人话原因/删行为描述）；③**控件无直接 FR 但其他 FR 已引用
   该概念 → 这是 spec 缺口，补 spec 而非删控件**（项目A 实例：原型画了“客户聊天账号”、
   FR-002 也引用它，但 FR-004 字段清单与 Key Entities 都漏了 → 补进 FR-004+实体，
   新歧义另标 NEEDS CLARIFICATION）。审计结果逐页列表汇报（违规内容/处置/依据），
   并记入 PREVIEW.md 决策日志。
   **spec.md 每次变更后自动重生成受影响页面**（不等用户叫），并更新 PREVIEW.md 映射表。
2. 用户看原型提反馈 → 先分类：spec 层（WHAT）→ 翻译成 spec 修改建议给用户确认 →
   改 spec.md → 跑规范核查 → 重生成页面；原型层（布局/交互琐事）→ 直接改 HTML +
   记入 PREVIEW.md 决策日志。
3. **红线：绝不允许借原型往 spec.md 塞不符合规范的内容**（实现细节/视觉设计/交互琐事）。
4. **ToB 界面设计铁律（用户 2026-09-22 拍板「记住」，已同步写入 项目A 总纲 Assumptions）**：简单易理解、人工介入少、单屏数据不过多不分散（低认知负荷）。**北极星条款（同日追加）：使用者每天只做三件事——丢物料（统一入口丢、系统自动判去向）、清黄格（全系统黄项聚合成一个队列、点即直达字段）、点亮着的按钮（不可达动作在本屏完全不出现）；其余一切要么系统自动、要么置灰。** 可执行落点：表格默认主列 ≤6（模块 FR 可细化到列清单，如 项目A FR-004a：合同号/买方/卖方/总价+币种/台数/状态，次要列收展开行）、次要字段收 ▸ 展开行；主操作按钮 ≤3、低频/高危动作收 ⋯ 菜单；只读记录（时间线/日志）默认 `<details>` 折叠；审查/比对类界面异常优先、正常态仅计数（如「2 红项」表格 + 「6 绿项已通过」折叠）；每屏只呈现一个决策点；「今日待办」以黄格计数+亮按钮为唯一入口。低保真原型直接用 `<details>`/展开行/底部固定操作栏静态演示这些机制，无需 JS。用户给出此类全局设计规则时，双落点：spec 层（总纲 Assumptions，约束后续所有模块与 plan 阶段）+ 原型层（当场改出可点示例），并在回复里用该铁律主动扫现有页面报出不达标项。

生成范围约定（用户拍板）：先出 P1 全部页面，P2/P3 用 todo.html 占位页列出驱动段落与
计划页面拆解；后续迭代补。原型页面文案同样遵守零黑话 FR。

spec 拆分为模块后（见 Split pattern）：驱动源变为总纲+各模块 spec；因 FR 编号不变，
已生成页面无需重做，只更新 PREVIEW.md 溯源映射表（加驱动模块列）。

## 校验断言的正确写法（本 session 4 次误报/漏报教训，verified）

自检脚本是这套流程的主力，但**断言写错比不写更糟**（会把"已修好"报成失败、把虚构报成通过）：

1. **跨模块引用校验必须读全部模块文件**：只读了总纲+订单+客户就去校验原型引用的 FR，
   结果 `FR-034`（定义在 005 工具模块）被误报"未定义"。校验集 = specs/ 下**所有** spec.md。
2. **关联型断言必须限定在同一区块**：`"SO-2026-0142" in page and "北亚-中行" in page`
   这种全文 `in` 会误报（两个字符串在页面不同处）。正确做法：先切出目标表格行/卡片
   （`i=page.index(锚点); j=page.index("</tr>", i); row=page[i:j]`）再在切片内断言。
3. **演示数据要三向对齐**（本次抓到 2 处矛盾）：列表页计数 == 详情页实际行数 ==
   其他模块页面里该主体的记录数（北亚账号数 2 ↔ 详情页 Anna+Boris 两行 ↔
   order-list 里买方=北亚的 3 单）。引用方向也要对：订单指定的是**卖方**账户，
   就不能把该单号挂到买方客户的账户行上。
4. **全站导航用集合断言**：逐页提取 topnav 的 href 集合，断言
   `全部页面集合 - 本页链接集合 - {本页} == ∅`；再跑死链扫描（href 目标必须在文件集内）。
   本次靠它发现 workbench.html 一直漏 todo 链接（批量插入口时该页文案不同未被匹配）。
   **批量插导航入口的锚正则必须容忍当前页属性变体**——当前页链接带 `class=on`，字面
   replace `<a href="x.html">登录</a>` 会漏掉激活页（实踩 assert 中止）；用
   `(<a href="x.html"[^>]*>登录</a>)` 定位插入点，改完断言全页 href 集合一致。
5. 语义断言优先用**长短语原文**而非自造措辞；出 ❌ 先 grep 实际原文确认是真冲突
   还是断言词不匹配，再决定改 spec 还是改断言——不要把误报当失败报给用户。
6. **泄漏词表要区分「我写串了」与「用户原文自带」**：拍板句逐字承接的实现级词（md5/路径式标识等）是合法域术语，MUST NOT 为过扫描而改写用户规则原文——豁免按行语境（该行含拍板/取代/排重等判定标记）而非全局删词；改写原文＝违反零虚构，比误报严重。
7. **精确计数断言（==N）几乎必误报**：同一标记会合法地出现在多处（"设为默认"
   在按钮+表尾说明各 2 次；旧措辞在 Assumptions 决策史里有意保留）。存在性用
   `>=N`，打印实际值供人判断；只有"旧措辞清零"这类否定断言才用严格 0，且要先
   确认历史留痕不是合法命中。本 session 两处 ❌ 均属此类（非真缺陷）。

可复用校验脚本：`scripts/check_preview_consistency.py`（打包上述 1/2/4 与
HTML 标签配平、FR 重复定义、实现层泄漏词、NEEDS CLARIFICATION 计数、>200 字长行），
用法 `python3 scripts/check_preview_consistency.py <specs_root> <preview_dir>`。

## Promote pattern: 口头设计原则 → 一等公民跨模块故事（verified on 项目A「今日工作台」US8, 2026-09-22）

当用户拍板的全局设计原则只在 Assumptions/原型视觉里存在、没有任何 FR 承诺该界面本身时，主动向用户点破这个缺口（一句提醒即可，别擅自开工）；用户说「要加」后按序升格：

1. **跨模块产物落总纲**（符合「跨模块共享产物归 001」纪律，不新建 specs 目录）：001 spec 新增「## 跨模块用户故事：X（北极星屏）」节——全新 US/FR 编号段（US8、FR-044~047），GWT 必须含负面场景（状态被他人推进→幂等拦截、不可达动作本屏完全不出现、激励无排名），需求条全部引用既有模块编号（纯聚合、溯源表注明「无新实体」）。
2. **登记四处一个不漏**：模块表加行（目录=本文件 §US8）、编号纪律的已用范围数字更新（043→047）、SC 总表加量化条款（如「进功能页 ≤3 次/日」「黄格滞留 <4h」——自定阈值要在回复里明示是可推翻假设）、溯源表加行（注明无旧 PRD 对应及旧流程对照）。
3. **原型侧三件套**：新建专页 + 全站 topnav 批量插入口（python 逐文件 replace、打印 skip 项防漏）+ PREVIEW.md 映射表登记新行。
4. **HTML patch 后必须配平校验**：`s.count('<div')==s.count('</div>')`——本 session fuzzy patch 把 nav span 行尾的 `</div>` 连带吞掉，靠数标签才暴露。

## 排期与进度体现 + 跨会话接力（schedule & progress）

SDD 不排日期——排期用优先级+依赖序表达；进度落在既有产物内，禁止自造状态文件（用户正统性偏好）：
- **排期载体**：spec.md US 的 P1/P2/P3（P1 单独可交付=MVP）+ tasks.md Phase 序（Setup→Foundational→US按P序→Polish）+ Dependencies 节。团队要日历/燃尽走官方桥 `/speckit-taskstoissues` → GitHub issues + Projects milestones，仓库内不引入日期字段。
- **进度载体**：tasks.md checkbox（`grep -c '\- \[x\]'` 直接拿数）。进度单位是**用户故事**（该 US Phase 全勾 + 其 quickstart/契约测试绿 = 一个可交付增量），不是任务完成百分比；MAP.md 的 FR/场景→测试文件绿灯率是最硬信号；怀疑手勾框失真时跑 `/speckit-converge` 出「代码 vs spec/plan/tasks」缺口复核，防勾了未实现。
- **跨会话接力棒**写进 AGENTS.md 开局协议：续做会话第一动作 = 读当前模块 spec + tasks.md，从**第一个未勾任务**继续——tasks.md 即状态，无需任何会话复述。
- **HANDOFF 是消耗品，执行完必须回写终态**：新会话按 HANDOFF「第一动作」做完该动作后，同轮把 HANDOFF 改掉——已完成项划删除线标 ✅（含产物路径+commit 号），「第一动作」整节**替换为下一条动作**（命令级），再单独 commit+push。不回写则下一个冷启动会话会重做已完成的工作或对着过时指令犹豫。回写属文档对平，与被交接的产物分两个 commit，各自验证 HEAD==origin。
- **用户说「归档本会话、新开会话继续」且产物链未走到 tasks.md**（接力棒无载体可接时）：先把交接写成 `specs/NNN-<feature>/HANDOFF.md` 入仓——内容四块＝①各文档版本锚（spec 版本号/tag/HEAD==origin 已验证）②新会话第一动作（命令级，含设计输入已核清单）③待复核挂账（逐项列，标不阻塞）④关键定稿速查＋协作纪律要点。commit+push 后按 hermes-session-maintenance 软归档旧会话，并给用户新会话首条消息原文（引用 HANDOFF.md 路径），新会话冷启动只凭该文件即可续上。归档前必 `git ls-remote origin <branch>` 实测远端==本地 HEAD，未推送的改动绝不带进归档。
- **会话边界 = 产物提交点**：一个会话只做一个可验收单元（一批 tasks / 一轮评审修复），完成即 commit 即 `/new`；单会话拖数周反复压缩是反模式（越跑越贵，官方明示）。旧来龙去脉靠 session_search 翻原文，不留在窗口里。
- **双 agent 同仓协作（一机写码、一机构建部署）三规**（2026-10-19 拍板，项目B 验证）：①**每次响应前先 `git pull --rebase`，不限开发——回答任何关于本项目的问题/分析/查代码之前都要先同步**，对方随时可能已推送改动，基于陈旧工作区下结论＝错误答案（改的是仓库 AGENTS.md §10.1 原句，不留追加段）；配套：commit 后立即 pull+push 的三连同步写进 §10.2 提交纪律表首行，纪律升级本身也按此三连落库；pull 后 rebase 冲突处理＝自己的 commit 后可能夹着对方推送，同文件交叉改动要自己解冲后再 push，判例编号取下一个全局未用号并与对方落点同轮对平。②**代码 push ≠ 线上生效**：部署 agent 是被动会话，不会监听仓库——向用户主动说明生效链路卡在哪一环（对方下次 pull+重建前线上仍是旧码），别让用户误以为推上去就变了。③rebase 后 MUST 跑**全仓** build＋test（`go build ./... && go test ./...` 或栈等价物），不止自改包——远端提交可能改公共函数签名未适配包内测试，HEAD 处于编译挂起而单包验证恰好绕开它（实测：对方给平台客户端 New() 加 logger 参数没改自己的包内测试，我方 rebase 后全仓挂、单包测全绿的假象靠全仓 test 才抓出）；发现的破口单独 commit 修，message 注明归属（「XX 提交遗留测试破口」），不混进自己的判例提交替他人背账。④**用户问「改了什么/怎么没生效」＝先摆生效链**：pull→push→对方 pull→重建容器→线上验证，逐环指到卡点；对方 pull 是被动会话（无 webhook 轮询，不叫不动），改判拍板执行完当轮把「待部署」回写 HANDOFF 并告知用户催部署方式，别让 HEAD==origin 被当成线上已生效（同 HANDOFF 回写终态规）。
- **实现阶段并行阶梯**（按时长选，治「一直等着」）：分钟级独立任务 → `delegate_task` 批量；小时级自主任务 → `hermes -w` / `/worktree new`；跨天/需人审 → 一 repo 一 kanban board（workspace `worktree:`），任务卡 body+comment 就是每个 worker 自带的上下文，board 状态（running/blocked/review）是 tasks.md 静态勾选看不到的执行层进度。
