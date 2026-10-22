# ToB 后台管理系统 · spec-kit 公共物料集

> 沉淀来源：两个内部 ToB 后台项目实际跑通的 AGENTS.md、项目宪法、DESIGN.md 与跨项目长期规范（Owner 逐项拍板）。
> 适用对象：所有 **spec 驱动开发（Spec Kit / SDD）** 的 ToB 后台管理系统项目。
> 例子域：一律用「电子商城后台」虚构场景，接入新项目时替换为业务自己的场景。

## 文件清单

| 文件 | 是什么 | 放到新项目的哪里 |
|---|---|---|
| `AGENTS.template.md` | AI 编码代理工作手册（流程、门禁、编辑纪律、合规检查清单） | 仓库根 `AGENTS.md`，填 §P 项目参数 |
| `constitution.template.md` | 项目宪法（五条治理原则 + 质量门禁 + Governance） | `.specify/memory/constitution.md` |
| `intent.template.md` | 需求入口物料（四段＋grill-with-docs 拷问记录，GI 门禁） | 每个 feature `specs/NNN-*/intent.md`，置于 constitution/specify 之前 |
| `DESIGN.template.md` | 前端设计规范（视觉 token + 布局 + 交互行为规则 + 组件约束） | 仓库根 `DESIGN.md`（UI-GATE 硬门禁的真相源） |
| `spec-kit物料落位与回写规则.md` | 每类内容写进哪个物料文件 + 原型改动何时回写 spec | 使用规则，不入库；核心条款已嵌入 AGENTS §1/§4/§5 |

## 新项目接入步骤（约 30 分钟）

1. **先写 `intent.md`**：复制 `intent.template.md` → 手建目录 `specs/001-<slug>/intent.md`，四段填齐后跑 grill-with-docs 拷问（过 GI 门禁）。后续每个 feature 同样先 intent.md。
2. 复制 `AGENTS.template.md` → 仓库根 `AGENTS.md`，**填齐 §P 项目参数表**（任一项空着必须先问 Owner，禁止按默认值自行决定）。
3. 复制 `constitution.template.md` → `.specify/memory/constitution.md`，替换 `<项目名>`，跑 `/speckit-constitution` 校验格式。
4. 复制 `DESIGN.template.md` → 仓库根 `DESIGN.md`。不打算改皮的 ToB 项目可直接沿用默认「Soft-UI 黑白灰体系」；有参考图/品牌色的按参考图重皮（token 层→组件层→布局层→页面层顺序落地），重皮后 §2/§3/§4 数值必须全部替换为实际值。
5. `/speckit-specify` 时显式提供 intent 所在目录（`SPECIFY_FEATURE_DIRECTORY`），然后按 AGENTS §3 引擎流程走：`specify → 原型 → clarify → plan → checklist → (analyze) → tasks → implement → converge`。

## 三个物料的权威分工（一图记牢）

| 问题 | 去哪找答案 |
|---|---|
| 业务上要什么（WHAT） | `specs/NNN-*/spec.md`（唯一需求真相源，条款编号即判例） |
| 治理红线 / 能不能进实现 | `.specify/memory/constitution.md` |
| 怎么实现（HOW：栈、表、接口） | 各模块 `plan.md` / `data-model.md` / `contracts/` |
| 长什么样、弹层/抽屉/按钮怎么交互 | `DESIGN.md` + `specs/NNN-*/preview/`（原型） |
| 干活流程与门禁 | `AGENTS.md` |

解释优先级：**spec 条款编号 > 宪法原则 > 通用惯例**；冲突一律上报 Owner 裁决，代理不得静默改需求。

## 跨项目长期规范速览（不随项目变化，已嵌入上述模板）

- ToB UI：不花哨、颜色少而克制、root 16px（紧凑靠密度不缩字号）、文案零黑话。
- 禁游戏化：积分/连击/徽章/成就墙/排行榜 = 绩效 PUA；人文关怀一次性、可静音、永不拦截；禁个人工时/操作量管理侧报表。
- 预览窗口：半屏以上（宽 ≥50vw、高 ≥55vh），禁小窗；编辑态旁挂预览须有「放大预览」近全屏。
- 单屏三件事：丢物料、清黄格、点亮着的按钮；其余自动或置灰。
- AI 只提候选，人下结论；审计日志只增不删改。
