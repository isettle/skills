# AGENTS.md — SDD 项目 · 代理工作规则（ToB 后台管理系统通用模板）

本文件是任何 AI 编码代理（Hermes / Claude Code / Codex / Cursor）在本仓库工作时的手册。
它只规定「怎么干活」，不重复业务规则。做任何改动前先读本文件全文。
本模板适用于所有 **spec 驱动开发（Spec Kit / SDD）** 项目；项目特有的事实一律填在 §P，正文不写死。

## 0. 一句话

本仓库是 **spec 驱动开发（Spec Kit / SDD）** 项目：`intent → spec → 原型 → plan → tasks → 实现 → 收敛`。
**spec 是需求真相源，代码服从 spec；发现 spec 有问题就停下来报告，不得静默改需求、不得绕过 spec 写码。**

## P. 项目参数（开工前必填）

| 参数 | 值 | 说明 |
|---|---|---|
| 项目名 | `<待填>` | 用于标题、汇报、外部标识 |
| 总纲模块 | `specs/001-<slug>/` | 系统级总纲 spec 所在目录 |
| 模块清单 | `<待填：001 总纲 · 002 xx · 003 xx>` | 平级目录 `specs/NNN-slug/` |
| 主工作分支 | `<待填：master（单分支）/ 分支模型>` | 工作分支约定 |
| 交付顺序 | `<待填：P1 → P2 → P3 的模块排期>` | 以总纲 spec 定序为准 |
| 技术栈 | `<待填>` | 语言/框架/数据库/部署方式，定盘后见 §6 |
| 项目特有代码规则 | `<待填：仅对本项目成立的硬规则，如业务唯一键、编码映射、门禁豁免>` | 例：商品编号全局唯一、币种用 TINYINT 枚举 |

**任一项为空时，涉及该参数的动作必须先问项目 Owner，不得按默认值自行决定。**

## 1. 真相源与优先级

| 内容 | 位置 | 地位 |
|---|---|---|
| 治理原则 | `.specify/memory/constitution.md` | 项目宪法，违反者不得进入实现（G4） |
| 业务需求（WHAT） | `specs/NNN-*/spec.md`（含 §P 总纲模块） | 唯一需求真相源；条款编号即判例 |
| 实现方案（HOW） | 各模块 `plan.md` / `research.md` / `data-model.md` / `contracts/` / `quickstart.md` | 技术决策在此，不在 spec |
| 低保真原型 | 总纲模块 `preview/`（+ `PREVIEW.md` 映射与决策日志） | spec 的零虚构投影 |
| UI 设计规范 | 仓库根 `DESIGN.md` | 视觉 token 与交互行为规则的唯一真相源（含弹层/抽屉/确认形态） |
| 仓库级术语表 | 仓库根 `GLOSSARY.md` | 跨 feature 词汇唯一权威；grill 拷问敲定即写入，只收本项目特有概念、不夹实现细节（衔接见 §4.5） |
| 架构决策记录 | 仓库根 `docs/adr/NNNN-<题>.md` | 「难逆转＋脱离上下文费解＋真实权衡」技术决策的家（升格条件见 §4.5） |
| 工作流模板 | `.specify/`（templates / scripts / workflows） | 上游生成物，**只读，不得手改** |

解释优先级：**spec 条款编号 > 宪法原则 > 通用惯例**；冲突一律上报项目 Owner 裁决。

**落位判据（一句话测试）**：换一套技术栈这句话仍成立 → 写 spec；失效 → 挪 plan / data-model / contracts；换一套 UI（弹层改抽屉、按钮换位）这句话仍成立 → 语义写 spec，形态写 DESIGN.md；整句随 UI 变形（「点击创建弹出 Modal」）→ 只进 DESIGN.md + 原型。

## 2. 目录与编号纪律（硬性）

- 模块为平级目录 `specs/NNN-slug/`，具体清单见 §P。
- **FR / US / SC 编号全局唯一、永不重编**；跨模块、跨原型一律用编号引用（如 `FR-013`、`US1b-场景6`）。
- 每条 FR 只在**一处**定义，其他模块引用编号而非复制条款；行为与实体可分家时两侧各写一句注释。
- **FR 分组与新增编号**：FR 区 MUST 用**粗体分组标题行**分组，分组方式为按实体的**增删改查行为**——一个标题对应一个业务实体（或一个流程段）的完整增删改查集合，FR 归入其操作实体所在标题下，组内按 增→删→改→查 排列；新 FR 归入现有组的对应行为段或新开组，编号一律取**下一个全局未用号**，MUST NOT 再开字母后缀（US 后缀照旧，如 `US1c`；存量 FR 字母后缀保留原号、永不重编）；禁止插入重排既有编号。
- FR 按业务能力组织，MUST NOT 按页面/控件组织（判别式：换一套 UI 该条是否仍成立）；页面↔FR 映射只维护在 `preview/PREVIEW.md`——原型是 FR 的实现证据，方向永远是 spec→原型，不得反向由页面推导 FR。
- SC 是独立编号维度，不与 FR 绑定、不随 FR 加后缀；一条 SC 可验证多条 FR。
- 单分支仓库：主工作分支见 §P。

## 3. 引擎流程（按序，不跳步）

**`intent.md`（整个流程最前端的入口物料，必做：四段齐备＋grill-me 拷问＋domain-modeling 落纸，过 GI 门禁）** → `/speckit-constitution`（项目首建一次；后续 feature 跳过）→ `/speckit-specify`（或手写 spec.md）
→ **Spec Kit Preview（低保真原型，必做步骤）** → **`/speckit-clarify`（必做，位置在原型后、plan 前：把 spec 缺口/歧义与原型评审反馈逐项澄清，拍板后回写 spec）** → `/speckit-plan` → **`/speckit-checklist`（必做：plan 产出后生成质量检查清单）** → 可选 `/speckit-analyze`
→ `/speckit-tasks` → `/speckit-implement` → `/speckit-converge`。

`/speckit-plan` 首轮技术栈/架构定盘采用与 GI 拷问同一套 grill 机制（frontier 轮次制），产出衔接按 §4.5——`GLOSSARY.md` 与 `docs/adr/` 随项目首启建立。

**硬性门禁（违反者不得进入下一阶段）**：

- **GI intent 门禁**：`intent.md` MUST 先于 `/speckit-constitution`（首建）与 `/speckit-specify` 编写，两段齐过才允许进入下一流程：① `specs/NNN-*/intent.md` 四段齐备非空（需求说明/需求痛点/需求草稿/泳道图），痛点段无代价数字、泳道图画不出主流程的＝视为未想清楚；② 四段有基本内容后 MUST 跑 `grill-me` 逐轮对抗拷问（frontier 轮次制）＋ `domain-modeling` 边问边写 ADR/术语表，至 frontier 清空，决定与术语表回写 intent.md「拷问记录」段。spec 定稿后 intent.md 冻结为溯源快照，需求变化走回写三分类改 spec，不回改 intent.md。**目录落位**：先手建 `specs/NNN-<slug>/` 放 intent.md，调 `/speckit-specify` 时 MUST 显式提供该 `SPECIFY_FEATURE_DIRECTORY`（官方支持），否则会另生成新目录造成双份。
- **G0' clarify 门禁**：进入 `/speckit-plan` 前 MUST 跑过 `/speckit-clarify`——spec 中 `[NEEDS CLARIFICATION]` 与原型评审产生的开放问题全部清零或已列待拍板清单并经 Owner 裁决；未过不得进 plan。
- **G1 原型门禁**：进入 `/speckit-plan` 前，必须验证 `PREVIEW.md` 映射表已覆盖 spec 中所有 US（每个 US 至少有一个原型页面）；缺原型不得进入 plan，更不得进入实现。验证命令：`grep "^### User Story" specs/NNN-*/spec.md` 提取 US 列表，比对 `PREVIEW.md` 页面↔spec 溯源映射表。
- **G2 文档完整性门禁**：进入 `/speckit-implement` 前，模块必须备齐六件套：`spec.md` + `plan.md` + `tasks.md` + `data-model.md` + `contracts/api.md` + `research.md`（缺任何一件不得开工写码）。
- **G2' checklist 门禁**：`/speckit-plan` 之后 MUST 跑 `/speckit-checklist`；清单中阻塞项未处置不得进入 `/speckit-tasks`（非阻塞项列入遗留记录）。
- **G3 收敛门禁**：`/speckit-converge` 必跑且 CONVERGE_REPORT.md 无 major gap（允许 minor gap 但必须显式列出）；标"完成"的模块必须测试全绿 + lint 通过 + spec 条款逐条可对照。
- **UI-GATE**：见 §6 UI 纪律——仓库根无 `DESIGN.md` 不得写任何前端代码。
- 未走完 spec + plan + tasks 的模块，**不得开始写实现代码**。
- 实现完成后 `/speckit-converge` 必跑：代码与 spec 不一致时**改代码**。
- 交付顺序：按 §P 排期执行，不得打乱模块优先级。

## 4. spec.md 编辑纪律（最容易出事的地方）

**格式**：只允许官方模板章节（User Scenarios / Edge Cases / Requirements(FR + Key Entities) / Success Criteria / Assumptions）。
不新造章节或表格——字段填写规则、读写边界、前置条件一律转写成 **FR-MUST 条目**。

**实体/属性术语纪律**：spec 中出现的任何实体/属性名称 MUST 在 Key Entities 有明确定义；Key Entities 的新增/编辑 MUST 经人工确认后落笔，代理不得静默增改实体或属性；原型 MUST NOT 出现 Key Entities 未定义的实体/属性——新字段顺序固定＝人工确认 Key Entities → FR → 同步原型。

**红线**：spec 里不得出现表名、字段类型、DDL、HTTP 路径、框架/库名、视觉设计，以及「点击XX按钮」「弹出弹层」「跳转到XX页」等控件级措辞。判别式：**换技术栈后这句话是否仍成立**——成立留 spec，否则挪 plan / data-model / contracts / DESIGN.md。

**状态机分层**：状态枚举 + WHAT 层流转规则（合法/非法、唯一回退路径）可作为 spec 的 FR MUST；逐转移表（当前状态×动作×触发方→目标态 + 非法流转处理 + 副作用）归 plan 阶段 `data-model.md`，并在 spec Assumptions 显式写明交接，让移交可见。

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
- **状态特定功能须配该状态示例数据 + 可点击路径**，否则评审者会认定「没改动」。
- **spec.md 每次变更后，自动重生受影响原型页并更新 `PREVIEW.md` 映射表与决策日志**（不等用户叫）。验证方式：改完 spec 后检查 PREVIEW.md 的"页面 ↔ spec 溯源映射"表，受影响页面的"状态"列必须更新为最新版本号。
- 界面铁律（宪法 II）：表格主列 ≤6、次要列收展开行；主操作按钮 ≤3、低频高危收 `⋯`；只读记录默认折叠；异常置顶、一致项折叠为计数；不可达动作不放本屏。
- 演示/示例数据必须**跨页自洽**（列表计数 = 详情行数 = 其他模块引用数）且**全虚构**，禁止真实客户名、单号、内部数据。
- 原型页面文案同样零黑话。

### 5.1 原型改动回写三分类（决策树，Owner 定）

| 序号 | 变化类型 | 判定 | 动作 |
|---|---|---|---|
| ① | 业务规则冲突 | 原型与 spec.md 打架 | 以 spec.md 为准修正原型；若原需求本身变化，**先改 spec.md 再同步原型** |
| ② | 纯 UI 表达变化 | 换端后规则不变、用户完成任务的步骤/义务/风险不变（弹层改抽屉、按钮位置调整） | 只改原型 + 记 PREVIEW.md 决策日志，**不回写 spec.md** |
| ③ | 交互流程实质变化 | 触及任一：**完成任务的步骤数、确认义务、数据丢失风险、系统行为** | 不得一概视为 UI 微调；MUST 先判定是否改变需求：是 → 走 ① 先改 spec（写成 FR）再同步原型与 quickstart；否 → 才降级为 ② |

②/③ 分界例（电子商城后台）：确认弹层改抽屉＝②；去掉确认弹层点创建直接落单＝③（确认义务消失）；弹层关闭不提示丢弃已填内容＝③（数据丢失风险）；弹层字段 5 个减到 3 个、必填变选填＝③。

**两条禁止**：不得借原型往 spec 塞不规范内容；不得借「UI 调整」名义静默改需求。

## 6. 实现阶段代码规范（首批代码产出后生效）

**技术栈以本项目 `plan.md` 定盘内容为准并回填 §P，不得擅自另引框架**。定盘前参考团队现行默认栈：后端 Python + FastAPI + SQLAlchemy 2.x + Alembic + Pydantic v2 + pytest，或 Go + Hertz + GORM；前端 React 19 + Vite + TanStack Router/Query/Table + Tailwind v4 + shadcn/ui（shadcn-admin 模板）；数据库与对象存储用项目内 `.env` 直配外部服务，应用本身跑**单容器部署**（多阶段构建，镜像零凭据，凭据运行时注入）；部署细节记录在 `deploy/README.md` 与 §P。

**跨项目长期规范（不随项目变化）**：

- **ToB UI 视觉规范**：不花里胡哨、实用简洁干脆；颜色少而克制防视觉疲劳；字号正常（root 16px），紧凑靠间距/行高/控件高度而非缩小字号。
- **预览窗口规范**：凡 HTML/文件/结构预览，窗口必须半屏以上（宽≥50vw、高≥55vh），禁止小窗；编辑态旁挂预览给足高度并提供「放大预览」近全屏（≥92vw×92vh）。

**工程纪律**：

- **UI 纪律（硬门禁 UI-GATE）**：所有 UI 实现 MUST 遵循仓库根目录的 `DESIGN.md`——生成或修改任何前端代码之前 MUST 先通读它。**仓库根无 `DESIGN.md` ＝ 不允许写任何前端代码**（先补 DESIGN.md 并经 Owner 确认，再开工）。**前端技术与 UI 方案 MUST 经 `DESIGN.md` §0 多方案候选呈报（A＝satnaing/shadcn-admin；B＝ant-design/ant-design-pro v6，推荐项、默认 shadcn 主题映射＋动态主题，见附录 B；可扩展）由 Owner 选定一套并登记 §0.3——未选定＝门禁不解除；方案选择属 HOW 层，MUST NOT 进 spec。**选 B 时前端实现会话 MUST 先读所用 ant-design-pro 仓库的 `AGENTS.md` 与 `.agents/skills`（`antd`、`pro-upgrade` 两技能）再写码，API/token 以 `@ant-design/cli` 查询结果为准，禁凭记忆。**产出 UI 与 DESIGN.md 冲突时按纪律条款改代码，**不反向放宽 DESIGN.md**（DESIGN.md 由 Owner 拍板产生）。页面级交互规则（弹层/抽屉/确认/字段布局/四态）落 `DESIGN.md` §11 + `preview/` 原型，不落 spec。
- **data-model 纪律**：①表名 MUST 单数（`user`/`product`/`order_record`，禁复数）；②表名与每个字段的 COMMENT MUST **严格等于** spec Key Entities 的属性原文——MUST NOT 夹带 FR 编号、判例、单位、实现注记；枚举值域、JSON 元素结构、批次/去重/互斥等实现性列另立「非实体属性列 + HOW 字典」节承接。③要新增字段/原因类内容 MUST 先人工判断→写 spec Key Entities→再落库（零虚构红线）。④**状态类字段 COMMENT MUST 含具体枚举值**（如【在线/离线】）；**JSON 类字段 COMMENT MUST 含元素结构说明**；缺者两步走：先完善 spec Key Entities 属性括注、再回补 data-model 字段注释。spec 无定义或含义模糊的，MUST NOT 自行编造命名/注释/字段，MUST 停下交 Owner 确认；确认要补实体属性时先改 spec 再回 data-model。
- **后端工程结构纪律**：采用薄入口 + 按领域分层的内部包结构（如 Go `cmd/` + `internal/<模块>/{handler,usecase,repository,model}`），**依赖严格向内**（handler→usecase→repository→model；跨域仅经 usecase 暴露的接口），**MUST NOT 在业务包之外放置业务逻辑**（入口只做配置加载/装配/启动；`pkg/` 一类外部公共目录禁装业务代码）。第三方平台适配、地图路由、cron 等归基础设施目录，业务判定一律收敛在领域 usecase。
- **contracts/api.md 纪律**：plan 阶段生成的 `contracts/api.md` MUST 是**完整 API 接口文档**，必含五段：① 公共请求头＋请求体约定；② 公共响应头＋响应体约定；③ 认证约定；④ 错误码约定；⑤ API 接口文档——每个接口列出：所属模块、名称、描述、路由、方法、可选请求头、请求体。**所有 header 与 payload 字段 MUST 详细列出＝字段名称、字段类型、字段备注、是否必须**，MUST NOT 只写示意 JSON。响应体默认统一 `{code: int, data: {}, message: string}`；**code＝0 为成功**，非 0 为错误码（码表在错误码约定段列全）。
- 工程结构：单仓双目录 `backend/` + `frontend/`（views · api），按模块分路由。
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
- 测试基线：API 契约测试（按栈选 pytest+httpx / go test / vitest 等）+ Playwright（quickstart 场景）。
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
| GI intent 门禁两段：四段齐备（需求说明/痛点/草稿/泳道图）＋ grill-me＋domain-modeling 拷问完成（frontier 清空，决定/术语表已回写） | `ls specs/NNN-*/intent.md` ＋ 逐段非空；痛点表有代价数字；泳道图 mermaid 可渲染；§5 拷问记录含轮次与结论 | **GI** |
| spec.md 已完成且通过合规核查 | 读 spec.md 检查章节完整性；grep 实现层措辞=0 | G2 |
| 原型覆盖率 100% | `grep "^### User Story" specs/NNN-*/spec.md` 提取 US 列表，比对 `PREVIEW.md` 映射表；preview/ 目录有对应 HTML 或显式标注占位 | **G1** |
| clarify 已执行（原型评审后、plan 前；NC=0 或待拍板已裁决） | `grep -c "NEEDS CLARIFICATION" specs/NNN-*/spec.md`＝0 ＋ 开放【待复核】清单逐条有 Owner 结论 | G0' |
| plan.md + data-model.md + contracts/api.md + research.md 齐备 | `ls specs/NNN-*/` 检查六件套 | G2 |
| checklist 已生成且阻塞项清零 | `ls specs/NNN-*/checklists/` + 读阻塞项状态 | G2' |
| data-model 表名全单数＋命名/COMMENT 可溯源 | `grep -E "^CREATE TABLE" data-model.md` 无复数结尾；逐字段对照 Key Entities 原文，无来源项已列人工确认清单 | §6 |
| tasks.md 按 Phase 分组且任务有明确文件路径 | 读 tasks.md 检查格式 `[TaskID] [P?] [Story?] 描述 + 精确文件路径` | G2 |
| CONVERGE_REPORT.md 无 major gap | 读 Gaps Identified 段，major gap 必须清零 | **G3** |
| 提交历史按 spec → 原型 → plan → tasks → 实现 顺序 | `git log -- specs/NNN-*/`，原型提交必须早于实现提交 | G1 |

### 9.2 原型纪律（对应 §5）

| 检查项 | 验证方法 |
|--------|----------|
| PREVIEW.md 映射表覆盖所有 US | 对比 spec 中 US 数量与 PREVIEW.md 中该模块驱动的页面数 |
| 每个原型页面有 FR/US 溯源标签 | `grep -c "FR-\|US\|SC-" preview/*.html` 计数 > 0 |
| spec 变更后原型已同步重生 | PREVIEW.md 决策日志最新条目日期 ≥ spec.md 最后修改日期 |
| 演示数据全虚构且跨页自洽 | 抽查原型页面，grep 真实公司名/人名=0；列表计数=详情行数 |
| 回写分类正确（对应 §5.1） | 逐条核对决策日志：③ 类改动是否都有对应 spec 修订；有无「去掉确认/新增丢弃风险」却未回写 spec 的漏项 |

### 9.3 spec 编辑纪律（对应 §4）

| 检查项 | 验证方法 |
|--------|----------|
| spec 无实现层措辞 | `grep -iE "table|column|varchar|http|api|sql" specs/NNN-*/spec.md` 应为 0（除 Assumptions 段的技术约束） |
| spec 无控件级措辞 | `grep -E "点击|弹层|弹窗|按钮|跳转到|下拉框" specs/NNN-*/spec.md` 应为 0 |
| FR 全为 MUST 语句 | `grep "^\*\*FR-" specs/NNN-*/spec.md` 检查每条含 MUST |
| FR 分组符合 CRUD 纪律（对应 §2） | 列出分组标题，逐组确认＝一个实体（或流程段）的增删改查集合，无按页面/控件分的组 |
| 无 `[NEEDS CLARIFICATION]` 残留 | grep 应为 0，或显式列出待拍板 |
| 实体/属性术语纪律 | ①收集 Key Entities 全部实体/属性名；②提取 spec 非 KE 章节与原型 HTML 的控件/字段标签名词；③每个名词回①找定义，无定义=违规；④审计日志类实体须在总纲定义；⑤新机制界面呈现词须有 FR 落点（演示辅助除外） |
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
| 敏感信息未入库 | `git log -p \| grep -iE "password|secret|api_key"` 应为 0；`.gitignore` 排除 `.env` | 硬性要求 |
| UI 纪律（对应 §6） | 写/改任何前端代码前先读仓库根 `DESIGN.md`；**仓库根无 `DESIGN.md` ＝ 不允许写任何前端代码**；`DESIGN.md` §0 方案已由 Owner 选定并登记 §0.3（未选定＝门禁不解除） | **UI-GATE** |
| 前端与 DESIGN.md 一致 | 抽查色值是否全走 token（无硬编码 `#`/`rgb()`）、状态用 Badge 非纯文字、Dialog 内 Card 有 `w-full` | §11/§12 |

**使用示例**：分析某模块是否合规时，必须按 9.1 表格逐条检查，不得跳过"原型覆盖率"行。如发现 US 无原型，立即标红并上报，不得以"代码已写完"为由放行。

## 10. 双 Agent 协作与部署分工（如适用；单 agent 项目可整节删除）

本项目由**两个 agent 并行开发**：

| Agent | 运行位置 | 职责 | 禁区 |
|---|---|---|---|
| 本机 Agent | Owner 本机仓库路径 | 编写/修改仓库文件（spec、原型、代码、文档）、本地跑测试与构建自检、commit＋push | **MUST NOT 部署**：不建容器、不改服务器、不 scp 凭据 |
| 开发机 Agent | 备用机（部署侧） | git pull 取最新、构建、部署、服务器端验证、回写部署结果 | MUST NOT 绕过 spec 改需求；MUST NOT 把服务器凭据/runtime 产物提交进 git |

### 10.1 会话启动（两个 agent 同一套）

1. **每次响应前 MUST 先 `git pull --rebase`（或 fetch＋reset 到 origin/主分支）**——不止开发，回答任何关于本项目的问题/分析/查代码之前都要先同步，禁止基于陈旧工作区开工或下结论。
2. pull 后 MUST 做**现状分析**再动手：读 `specs/001-*/HANDOFF.md`（交接载体）＋ `git log --oneline -10` ＋ `git status`；识别对方 agent 已完成/进行中的工作。
3. 发现工作区有未提交改动（非本人所为）＝MUST 停下报告 Owner，MUST NOT 直接覆盖或 `reset --hard` 丢弃。
4. 开工前在 HANDOFF.md「进行中」区**登记本次任务与认领方**，同一任务同时只允许一个 agent 改码（单写者原则）；跨任务并行须文件级不重叠。

### 10.2 提交与同步纪律

| 规则 | 说明 |
|---|---|
| **commit 后必同步** | 每次 `git commit` 之后 MUST **立即**依次执行 `git pull --rebase` ＋ `git push`——commit→pull→push 绑定为一个动作，禁止「只 commit 滞未推送」 |
| 小步快跑 | 一个逻辑单元＝一次 commit；完成即 push，不攒大提交 |
| push 前必 pull | diverged 时用 `git pull --rebase`，禁 force-push、禁改写已推送历史 |
| push 后验证 | `git rev-parse HEAD` == `origin/<branch>` 才算成功（§8） |
| commit message | 中文一行摘要＋要点列表；禁 conventional 前缀（§8） |
| 敏感物零入库 | `.env`、`runtime/`、`*.sqlite`、临时凭据/打码残值文件 MUST NOT 进 git |

### 10.3 交接载体（HANDOFF.md）

- `specs/001-*/HANDOFF.md` 是**唯一跨 agent 交接文件**；细节真相源仍是 spec 体系（spec > HANDOFF）。
- 每次会话结束（或阶段性完成）MUST 更新：版本锚（HEAD 短哈希）、本轮完成项、**进行中/待接手项**、已知坑与复验方法、测试现状。
- 写"完成"前必须满足 §7 完成判据；跑不了的如实写"卡在哪一步"。
- 部署结果由开发机侧 agent 回写 HANDOFF，本机 agent 不臆测线上状态。

### 10.4 冲突与裁决

- 两个 agent 对同一问题结论冲突、或实现与 spec 冲突：**spec 条款编号 > 宪法 > 通用惯例**；无法自决时列证据交 Owner 裁决，MUST NOT 各自静默改需求（§1/§4）。
- 对方 agent 已推送的判例/决策编号 MUST 沿用，禁止重编号或反向推翻（§2 编号纪律）。
- 语义不明的历史改动：先读 spec/HANDOFF/commit message 溯源，仍不明则问 Owner，不按猜测动手。
