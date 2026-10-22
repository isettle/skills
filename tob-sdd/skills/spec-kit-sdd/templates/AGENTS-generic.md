# AGENTS.md — SDD 项目 · 代理工作规则（通用模板）

本文件是任何 AI 编码代理（Hermes / Claude Code / Codex / Cursor）在本仓库工作时的手册。
它只规定「怎么干活」，不重复业务规则。做任何改动前先读本文件全文。
本模板适用于所有 **spec 驱动开发（Spec Kit / SDD）** 项目；项目特有的事实一律填在 §P，正文不写死。

## 0. 一句话

本仓库是 **spec 驱动开发（Spec Kit / SDD）** 项目：`spec → 原型 → plan → tasks → 实现 → 收敛`。
**spec 是需求真相源，代码服从 spec；发现 spec 有问题就停下来报告，不得静默改需求、不得绕过 spec 写码。**

## P. 项目参数（开工前必填）

| 参数 | 值 | 说明 |
|---|---|---|
| 项目名 | `<待填>` | 用于标题、汇报、外部标识 |
| 总纲模块 | `specs/001-<slug>/` | 系统级总纲 spec 所在目录 |
| 模块清单 | `<待填>` | 如：001 总纲 · 002 xx · 003 xx（平级目录 `specs/NNN-slug/`） |
| 主工作分支 | `<待填>` | 单分支仓库的当前工作分支 |
| 交付顺序 | `<待填>` | P1 → P2 → P3 的模块排期 |
| 技术栈 | `<待 plan.md 定盘后回填>` | 语言/框架/数据库/部署方式，见 §6 |
| 项目特有代码规则 | `<待填>` | 仅对本项目成立的硬规则（如特定业务唯一键、特定编码映射） |

**任一项为空时，涉及该参数的动作必须先问项目 Owner，不得按默认值自行决定。**

## 1. 真相源与优先级

| 内容 | 位置 | 地位 |
|---|---|---|
| 治理原则 | `.specify/memory/constitution.md` | 项目宪法，违反者不得进入实现（G4） |
| 业务需求（WHAT） | `specs/NNN-*/spec.md`（含 §P 总纲模块） | 唯一需求真相源；条款编号即判例 |
| 需求入口快照 | `specs/NNN-*/intent.md` | specify 前置物料；定稿后冻结为溯源快照（GI 门禁，衔接见 §4.5） |
| 实现方案（HOW） | 各模块 `plan.md` / `research.md` / `data-model.md` / `contracts/` / `quickstart.md` | 技术决策在此，不在 spec |
| 低保真原型 | 总纲模块 `preview/`（+ `PREVIEW.md` 映射与决策日志） | spec 的零虚构投影 |
| 仓库级术语表 | 仓库根 `GLOSSARY.md` | 跨 feature 词汇唯一权威；grill 拷问敲定即写入，只收本项目特有概念、不夹实现细节（衔接见 §4.5） |
| 架构决策记录 | 仓库根 `docs/adr/NNNN-<题>.md` | 「难逆转＋脱离上下文费解＋真实权衡」技术决策的家（升格条件见 §4.5） |
| 工作流模板 | `.specify/`（templates / scripts / workflows） | 上游生成物，**只读，不得手改** |

解释优先级：**spec 条款编号 > 宪法原则 > 通用惯例**；冲突一律上报项目 Owner 裁决。

## 2. 目录与编号纪律（硬性）

- 模块为平级目录 `specs/NNN-slug/`，具体清单见 §P。
- FR/US/SC 全局唯一、永不重编；跨模块、跨原型一律用编号引用（如 `FR-013`、`US1b-场景6`）。
- **废止条款原地留位**：用户叫停某功能时，对应 FR 转 MUST NOT 负向句保留编号（编号永不复用），并全链清除该功能在 US 场景/Edge/Key Entities 属性/原型控件中的痕迹，B 组拍板记录写明取代关系。
- 每条 FR 只在**一处**定义，其他模块引用编号而非复制条款；行为与实体可分家时两侧各写一句注释。
- **FR 分组与新增编号（用户拍板）**：FR 区 MUST 用**粗体分组标题行**分组，分组方式为按实体的**增删改查行为**——一个标题对应一个业务实体（或一个流程段）的完整增删改查集合，FR 归入其操作实体所在标题下，组内按 增→删→改→查 排列；新 FR 归入现有组的对应行为段或新开组，编号一律取**下一个全局未用号**，MUST NOT 再开字母后缀（US 后缀照旧，如 `US1c`；存量 FR 字母后缀保留原号、永不重编）；禁止插入重排既有编号。**流程/状态机型条款（双分支、快照冻结、裁决闸门）不属于任何实体 CRUD 格，此类标题按业务流程段分组。**
- FR 按业务能力组织，MUST NOT 按页面/控件组织（判别式：换一套 UI 该条是否仍成立）；页面↔FR 映射只维护在 `preview/PREVIEW.md`——原型是 FR 的实现证据，方向永远是 spec→原型，不得反向由页面推导 FR。
- SC 是独立编号维度，不与 FR 绑定、不随 FR 加后缀；一条 SC 可验证多条 FR。
- 单分支仓库：主工作分支见 §P。

## 3. 引擎流程（按序，不跳步）

**`intent.md`（流程最前端入口物料：需求说明/痛点/草稿/泳道图＋grill-me 拷问＋domain-modeling 落纸，过 GI 门禁）** → `/speckit-constitution`（项目首建一次；后续 feature 跳过）→ `/speckit-specify`（或手写 spec.md）
→ **Spec Kit Preview（低保真原型，必做步骤）** → **`/speckit-clarify`（必做，位置＝原型后、plan 前：收口 spec 缺口/歧义与原型评审反馈，拍板后回写 spec）** → `/speckit-plan` → **`/speckit-checklist`（必做，紧跟 plan）** → 可选 `/speckit-analyze`
→ `/speckit-tasks` → `/speckit-implement` → `/speckit-converge`。

**硬性门禁（违反者不得进入下一阶段）**：

- **GI intent 门禁**：`intent.md` 先于 constitution/specify 编写；①四段齐备非空（痛点带代价数字、泳道图能画主流程）②grill-me 拷问＋domain-modeling 落纸至 frontier 清空，决定/术语表回写 intent「拷问记录」段——两段齐过才进下一流程。spec 定稿后 intent.md 冻结为溯源快照，需求变化走回写三分类改 spec，不回改 intent。
- **G0' clarify 门禁**：进入 `/speckit-plan` 前 MUST 跑过 `/speckit-clarify`——spec 中 `[NEEDS CLARIFICATION]` 与原型评审产生的开放问题（含【待复核】）全部清零或经 Owner 裁决；未过不得进 plan。技术选型（栈/凭据/部署）不占 clarify 额度、归 plan 首轮问；各被触及 spec 新增 `## Clarifications`+`### Session 日期` 段逐条记 Q→A。
- **G1 原型门禁**：进入 clarify/plan 前，必须验证 `PREVIEW.md` 映射表已覆盖 spec 中所有 US（每个 US 至少有一个原型页面）；缺原型不得进入后续阶段，更不得进入实现。验证命令：`grep "^### User Story" specs/NNN-*/spec.md` 提取 US 列表，比对 `PREVIEW.md` 页面↔spec 溯源映射表。
- **G2 文档完整性门禁**：进入 `/speckit-implement` 前，模块必须备齐六件套：`spec.md` + `plan.md` + `tasks.md` + `data-model.md` + `contracts/api.md` + `research.md`（缺任何一件不得开工写码）。
- **G3 收敛门禁**：`/speckit-converge` 必跑且 CONVERGE_REPORT.md 无 major gap（允许 minor gap 但必须显式列出）；标"完成"的模块必须测试全绿 + lint 通过 + spec 条款逐条可对照。
- **G2' checklist 门禁**：`/speckit-plan` 之后 MUST 跑 `/speckit-checklist`；清单阻塞项未处置不得进入 `/speckit-tasks`（非阻塞项列入遗留记录）。
- 未走完 spec + clarify + plan + checklist + tasks 的模块，**不得开始写实现代码**。
- 实现完成后 `/speckit-converge` 必跑：代码与 spec 不一致时**改代码**。
- 交付顺序：按 §P 排期执行，不得打乱模块优先级。

## 4. spec.md 编辑纪律（最容易出事的地方）

**格式**：只允许官方模板章节（User Scenarios / Edge Cases / Requirements(FR + Key Entities) / Success Criteria / Assumptions）。
不新造章节或表格——字段填写规则、读写边界、前置条件一律转写成 **FR-MUST 条目**。

**实体/属性术语纪律（用户 2026-10-14 拍板）**：spec 中出现的任何实体/属性名称 MUST 在 Key Entities 有明确定义；Key Entities 的新增/编辑 MUST 经人工确认后落笔（用户直接给出实体属性清单即视为确认），代理不得静默增改实体或属性；原型 MUST NOT 出现 Key Entities 未定义的实体/属性——新字段顺序固定＝人工确认 Key Entities → FR → 同步原型。审计日志类全局实体 MUST 在总纲实体关系总表有定义行。

**红线**：spec 里不得出现表名、字段类型、DDL、HTTP 路径、框架/库名、视觉设计。判别式：**换技术栈后这句话是否仍成立**——成立留 spec，否则挪 plan / data-model / contracts。

**可读性**：单条 FR ≤3 行，超了拆子弹列表；US 叙述 ≤3 行讲完旅程，尾部用「规则见 FR-xxx」指向 FR，不互相复述；禁 200+ 字单行复合长句。

**每次改完 spec.md，收尾必做两道核查**（结果写进汇报）：

1. **合规核查**：实现层措辞清零；`[NEEDS CLARIFICATION]` 清零或列出待拍板；Key Entities 只留业务属性+基数；FR 全为 MUST 语句。
2. **一致性冲突扫描**：逐条比对新旧内容并跨模块找矛盾（同概念两处定义不同、状态机/触发条件互斥、引用编号悬空、动作双头归属、总纲常量与模块 FR 打架）。
   - 低级（措辞/引用/覆盖瑕疵）→ 自行合并修掉，汇报里列「已修」。
   - 中高级（业务语义矛盾、需二选一、影响多模块）→ **列表交人工拍板**，给证据与建议修法，**不得自选**。

**编辑安全**（上游项目有事故先例）：

- 动 spec 前先 `git commit` 或存一份 FR 清单快照，作为守恒基准。
- 替换文本的锚点必须**逐字复制自文件原文**（≤10 行，取目标条款本身）；**禁止**用「代码里算出来的坐标切片」当锚点。
- 改完立刻跑断言：① FR 定义集合与开工前快照一致（缺/多都报警）；② 每个文件含预期章节标题（`## 溯源` / `### Key Entities` / `### Edge Cases`）；③ 编号集合连续；④ 关键语义词 grep 无丢失。
- 表格类编辑收尾查重（同一行首文本不得重复出现）。

### 4.5 grill 产出与 spec 体系的衔接（术语表 / ADR / 决策单家）

- **术语双柜面（防双真相源）**：`GLOSSARY.md`＝跨 feature 词汇权威——grill 拷问中新术语敲定**当场**写入（不攒批）、只收本项目特有概念、表内禁实现细节；`spec.md Key Entities`＝本 feature 数据模型（业务属性+基数，改动仍走 §4 人工确认纪律）。喂料方向：GLOSSARY → KE 逐条人工确认 → 落 spec；两处定义冲突时**当场摊开交 Owner 裁决、改 GLOSSARY 收敛**——词汇以 GLOSSARY 为准，KE 不重定义词汇。
- **决策单家（一条决策只有一个家）**：需求裁决（WHAT）→ spec Assumptions B 组判例（判例编号即真相）；满足 ADR 三条件（**难以逆转 ＋ 脱离上下文会令人费解 ＋ 真实权衡的结果**，三者同时成立）的技术决策 → `docs/adr/NNNN-<题>.md`（格式照 domain-modeling 的 ADR-FORMAT，不满足条件不建）；可逆技术取舍/选型细节 → `plan.md` Decision ＋ `research.md` Alternatives。家与家之间只以编号/路径引用，MUST NOT 复制全文；ADR 正文可引 FR/判例编号回溯需求。
- **plan 阶段复用拷问**：`/speckit-plan` 首轮批量定盘（栈/DB/部署/前端形态）即一场 grill——frontier 轮次制、每题附推荐答案、事实由代理自查、裁决归 Owner；拍板中命中 ADR 三条件的当场升格进 `docs/adr/`，不散落各模块 plan/research。
- 拷问中压测出的边缘场景（domain-modeling 编造的违例/边界反例）→ 转写进 spec 的 Edge Cases ＋ GWT 验收场景素材。

## 5. 原型纪律（Spec Kit Preview）

- **零虚构**：spec 未提到的控件/字段/状态/列，绝不出现在原型上。实体/属性名词同样守门：Key Entities 未定义的实体/属性不得出现在原型；觉得该有 → 先人工确认补 Key Entities 与 spec，拍板后再画。
- **全覆盖**：spec 中的每个 US 必须在 `PREVIEW.md` 映射表有对应条目，且 `preview/` 目录有实际 HTML 文件（允许占位页但必须显式标注 `⬜ 占位`）。判别式：`grep "^### User Story" specs/NNN-*/spec.md | wc -l` == `PREVIEW.md` 中该模块驱动的行数。不等则报警，缺的 US 必须补原型或显式标注"占位，待要求时出线框"。
- 每个控件带 `US n` / `FR-nnn` / `SC-nnn` 溯源标签；演示辅助控件显式标注「原型演示用」。
- **spec.md 每次变更后，自动重生受影响原型页并更新 `PREVIEW.md` 映射表与决策日志**（不等用户叫）。验证方式：改完 spec 后检查 PREVIEW.md 的"页面 ↔ spec 溯源映射"表，受影响页面的"状态"列必须更新为最新版本号。
- 原型层反馈分流：业务规则变化 → 改 spec；布局/交互琐事 → 直接改 HTML + 记决策日志（不许借原型往 spec 塞不规范内容）。
- 界面铁律（宪法 II）：表格主列 ≤6、次要列收展开行；主操作按钮 ≤3、低频高危收 `⋯`；只读记录默认折叠；异常置顶、一致项折叠为计数；不可达动作不放本屏。
- 演示/示例数据必须**跨页自洽**（列表计数 = 详情行数 = 其他模块引用数）且**全虚构**，禁止真实客户名、单号、内部数据。
- 原型页面文案同样零黑话。

## 6. 实现阶段代码规范（首批代码产出后生效）

**技术栈以本项目 `plan.md` 定盘内容为准并回填 §P，不得擅自另引框架**。定盘前参考团队现行默认栈：Python + FastAPI + SQLAlchemy 2.x + Alembic + Pydantic v2 + pytest；前端 React 19 + Vite + TanStack Router/Query/Table + Tailwind v4 + shadcn/ui（shadcn-admin 模板）；数据库与对象存储用项目内 `.env` 直配外部服务，应用本身跑**单容器部署**（多阶段构建，镜像零凭据，凭据运行时注入）；部署细节记录在 `deploy/README.md` 与 §P。

**跨项目长期规范（用户定，不随项目变化）**：

- **ToB UI 视觉规范**：不花里胡哨、实用简洁干脆；颜色少而克制防视觉疲劳；字号正常（root 16px），紧凑靠间距/行高/控件高度而非缩小字号。
- **预览窗口规范**：凡 HTML/文件/结构预览，窗口必须半屏以上（宽≥50vw、高≥55vh），禁止小窗；编辑态旁挂预览给足高度并提供「放大预览」近全屏（≥92vw×92vh）。

**工程纪律**：

- **UI 纪律（硬门禁 UI-GATE）**：所有 UI 实现 MUST 遵循仓库根的 `DESIGN.md`——生成或修改任何前端代码之前 MUST 先通读它（All UI implementation must follow `DESIGN.md` in the repository root. Read it before generating or modifying any frontend code.）。**仓库无 `DESIGN.md` ＝ 不允许写任何前端代码**：先补 DESIGN.md 并经 Owner 确认再开工；产出 UI 与 DESIGN.md 冲突时改代码，不反向放宽文档。
- **后端工程结构纪律（用户定 2026-10-15）**：Golang 工程 MUST 采用 `cmd/`（薄入口）+ `internal/<模块>/`（按领域组织的 handler/usecase/repository/model）结构，**依赖严格向内**（handler→usecase→repository→model；跨域仅经 usecase 暴露接口），**MUST NOT 在 `internal/` 之外放置业务逻辑**（cmd 仅装配/启动，`pkg/` 等 internal 外目录禁装业务代码）。非 Go 栈遵循同类原则：入口薄、按领域内聚、依赖向内、业务代码不出领域边界。
- **contracts/api.md 纪律（用户定 2026-10-15）**：plan 阶段生成的 `contracts/api.md` MUST 是**完整 API 接口文档**，必含五段：① 公共请求头＋请求体约定；② 公共响应头＋响应体约定；③ 认证约定；④ 错误码约定；⑤ API 接口文档——每个接口列出：所属模块、名称、描述、路由、方法、可选请求头、请求体。**所有 header 与 payload 字段 MUST 详细列出＝字段名称、字段类型、字段备注、是否必须**，MUST NOT 只写示意 JSON。响应体默认统一 `{code: int, data: {}, message: string}`；**code＝0 为成功**，非 0 为错误码（码表列全）。
- 工程结构：单仓双目录 `backend/`（Go 按上条纪律）+ `frontend/`（views · api），按模块分路由。
- 契约优先：接口改动必须先改 `contracts/api.md`，再改代码。
- 金额一律以**最小货币单位的整数**运算（人民币＝分），禁止浮点存算。
- 枚举/状态类字段在 `data-model.md` 定义数据库编码与语义值的双向映射（如币种、状态机），API 层收发语义值、存储层用紧凑编码；具体编码表属项目参数，写入 §P 或 data-model。
- 业务状态字段 ≠ 数据层软删除，两者独立实现，不得合并。
- 审计日志**只增不删改**，支持完整回放；AI 相关产出（审查/改稿）永远只提候选，生效必经确定性比对或人工确认——不得新增「自动通过」开关。
- 对外物料不得内嵌任何内部处理事项（回填/待确认/覆盖率/AI 术语）。
- ToB 项目不写游戏化元素（积分/徽章/排行榜/连击），不写个人工时或操作量报表。
- 无依据不落库：`mock`/示例数据不得作为正式取数来源。

## 7. 完成判据（不许口头完成）

- 任务完成 = **验收场景已映射为自动化测试且通过** + lint/typecheck 通过 + 相关 spec 条款可逐条对上 + **原型覆盖率 100%**（spec 中每个 US 在 PREVIEW.md 有映射且 preview/ 有对应 HTML，或显式标注"占位"）。
- 测试基线：API 契约测试（按栈选 pytest+httpx / vitest 等）+ Playwright（quickstart 场景）。
- 每个模块带 `seed/` 上线初始化数据（内置项可编辑不可删）。
- 没跑过的结论不许写成「已完成」；跑不了就如实说卡在哪一步。
- **CONVERGE_REPORT.md 无 major gap**：允许 minor gap（如前端 UX 未验证）但必须显式列出并说明影响；标"完成"的模块如果 CONVERGE_REPORT 列出未测试的 FR，则该 FR 不得标完成。

## 8. 版本控制与汇报

- **每次 commit 后立即 push**；push 后用 `git rev-parse HEAD` == `git rev-parse origin/<branch>` 验证才算成功；首次推新分支用 `-u`。
- commit message 禁用 `feat:`/`fix:`/`chore:` 等 conventional 前缀；格式＝一行摘要 + 空行 + 要点列表。
- 汇报用中文，结论先行；自行判断的细节标 **【待复核】** 列给 Owner 确认，不得静默决定。
- 规范正统性：产出严格贴合 Spec Kit 官方模板与社区实践，不造自创章节；缺内容转写成模板内既有形式。

## 9. 流程合规检查清单（AI 代理与人工审查共用）

**用途**：每次分析"开发流程是否合规"、"模块是否可以标完成"、"是否可以进入下一阶段"时，必须逐条核对本清单。**不得凭经验泛泛检查通用工程实践而忽略本项目特有的 SDD 流程**。

### 9.1 引擎流程完整性（对应 §3）

| 检查项 | 验证方法 | 门禁级别 |
|--------|----------|----------|
| §P 项目参数已填齐 | 读 §P 表格，`<待填>` 出现次数＝0 | G0 |
| spec.md 已完成且通过合规核查 | 读 spec.md 检查章节完整性（User Scenarios / Edge Cases / Requirements / Success Criteria / Assumptions）；grep 实现层措辞=0 | G2 |
| 原型覆盖率 100% | `grep "^### User Story" specs/NNN-*/spec.md` 提取 US 列表，比对 `PREVIEW.md` 映射表；preview/ 目录有对应 HTML 或显式标注占位 | **G1** |
| clarify 已执行（原型后、plan 前） | `grep -c "NEEDS CLARIFICATION" specs/NNN-*/spec.md`＝0 ＋ 开放【待复核】逐条有 Owner 结论 ＋ 各被触及 spec 含 `## Clarifications` 段 | G0' |
| plan.md + data-model.md + contracts/api.md + research.md 齐备 | `ls specs/NNN-*/` 检查六件套 | G2 |
| checklist 已生成且阻塞项清零 | `ls specs/NNN-*/checklists/` ＋ 读阻塞项状态 | G2' |
| tasks.md 按 Phase 分组且任务有明确文件路径 | 读 tasks.md 检查格式 `[TaskID] [P?] [Story?] 描述 + 精确文件路径` | G2 |
| CONVERGE_REPORT.md 无 major gap | 读 CONVERGE_REPORT.md 检查 Gaps Identified 段，major gap 必须清零 | **G3** |
| 提交历史按 spec → 原型 → plan → tasks → 实现 顺序 | `git log -- specs/NNN-*/` 检查提交时间线，原型提交必须早于实现提交 | G1 |

### 9.2 原型纪律（对应 §5）

| 检查项 | 验证方法 |
|--------|----------|
| PREVIEW.md 映射表覆盖所有 US | 对比 spec 中 US 数量与 PREVIEW.md 中该模块驱动的页面数 |
| 每个原型页面有 FR/US 溯源标签 | `grep -c "FR-\|US\|SC-" preview/*.html` 计数 > 0 |
| spec 变更后原型已同步重生 | 检查 PREVIEW.md 决策日志最新条目日期 ≥ spec.md 最后修改日期 |
| 演示数据全虚构且跨页自洽 | 抽查原型页面，grep 真实公司名/人名=0；列表计数=详情行数 |

### 9.3 spec 编辑纪律（对应 §4）

| 检查项 | 验证方法 |
|--------|----------|
| spec 无实现层措辞 | `grep -iE "table\|column\|varchar\|http\|api\|sql" specs/NNN-*/spec.md` 应为 0（除 Assumptions 段的技术约束） |
| FR 全为 MUST 语句 | `grep "^\*\*FR-" specs/NNN-*/spec.md` 检查每条含 MUST |
| FR 分组符合 CRUD 纪律（对应 §2） | `grep "^\*\*.*\*\*$" specs/NNN-*/spec.md` 列出分组标题，逐组确认＝一个实体（或流程段）的增删改查集合，无按页面/控件分的组 |
| 无 `[NEEDS CLARIFICATION]` 残留 | `grep "NEEDS CLARIFICATION" specs/NNN-*/spec.md` 应为 0，或显式列出待拍板 |
| 实体/属性术语纪律（对应 §4） | 收集各 spec Key Entities 定义集 → 扫 spec 非 KE 章节与原型 label/button/th 用词 → 逐个回定义集；无定义＝折回已定义词或交人工确认补 KE；派生/状态属性的示例值还须与属性定义自洽（如「当前停留」不得给离线设备填进行中值） |
| 编号连续无重编 | 提取所有 FR 编号排序后检查连续性（允许跳号但不允许重编） |
| 术语双柜面对平（对应 §4.5） | 本轮涉及实体/属性名词逐条对 `GLOSSARY.md` 与 Key Entities 查两处定义——两处并存且含义分叉＝违规，摊开交 Owner 裁决后收敛 GLOSSARY |

### 9.4 完成判据（对应 §7）

| 检查项 | 验证方法 |
|--------|----------|
| 测试全绿 | 后端测试命令全过；前端 `npm test` 全过 |
| lint/typecheck 通过 | 前端 `npm run lint` 无 error；`npx tsc --noEmit` 无 error |
| spec 条款可逐条对照 | CONVERGE_REPORT.md Coverage Table 每条 FR 标 ✅ 或显式列出 gap |
| seed 数据齐备 | seed 目录有对应模块的初始化数据脚本 |

### 9.5 工程化门禁（通用最佳实践）

| 检查项 | 验证方法 | 备注 |
|--------|----------|------|
| CI/CD 流水线 | 检查 `.github/workflows/` 或 `.gitlab-ci.yml` | 新项目属改进项 |
| 代码审查流程 | 检查是否有 PR/MR 流程，禁止直推主分支 | 新项目属改进项 |
| pre-commit hook | 检查 `.pre-commit-config.yaml` | 新项目属改进项 |
| 敏感信息未入库 | `git log -p \| grep -iE "password\|secret\|api_key"` 应为 0；`.gitignore` 排除 `.env` | 硬性要求 |
| UI 纪律（对应 §6） | 写/改任何前端代码前确认仓库根存在 `DESIGN.md` 且已通读；无文档＝前端实现阶段禁止开工 | **UI-GATE** |

**使用示例**：分析某模块是否合规时，必须按 9.1 表格逐条检查，不得跳过"原型覆盖率"行。如发现 US 无原型，立即标红并上报，不得以"代码已写完"为由放行。
