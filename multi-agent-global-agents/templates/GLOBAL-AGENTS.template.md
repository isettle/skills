# 全局项目规则模板（机器级 · GLOBAL-AGENTS.md）

> 用法：本规则集以 **skill 形态分发与触发**（isettle/skills 仓库 `multi-agent-global-agents/`），拷到该机 agent 全局规则统一入口位＝**`~/AGENTS.md`**（Linux root 用户＝`/root/AGENTS.md`；macOS＝家目录 `~/AGENTS.md`）仅作该机留底/兜底副本；项目级细则见各仓库根 `AGENTS.md`。
> **本模板＝多 Agent 登记制**：在表里加一行即可接入新 agent，其余节不改。填 §2 机器参数（项目根/主机别名）后启用。
> **接入前提**：不再经「各 agent 全局记忆 md 顶部引用行」接线；规则加载链＝每个 agent 安装本 skill（见 §1 登记制第 6 条），由 skill 触发在编码会话开始自动载入。

## 0. 一分钟版

- 项目在哪：**机器级默认根**（§2）——按本机类型取；根下再按 `{git域名}/{项目组名}/{项目名称}` 落位
- 开工四步：`git pull` → 读交接文件＋`git log`/`git status` → 认领登记署名 → 动手
- 收工三步：commit（一行摘要＋要点，禁 conventional 前缀）→ push（`HEAD == origin/<branch>` 才算成功）→ 回写交接文件
- 我是谁：§1 花名册里找到本 agent 行，职责/禁区按那行走；会话开头自报身份

## 1. Agent 花名册（多 Agent 协作 · 登记制）

| Agent | 运行位置 | 角色 | 职责 | 禁区 |
|---|---|---|---|---|
| `<agent-1，例：本机 IDE/CLI agent>` | `<Owner 本机>` | 开发侧 | 编写/修改仓库文件（spec、代码、文档）、本地测试与构建自检、commit＋push | MUST NOT 部署：不建容器、不改服务器、不 scp 凭据 |
| `<agent-2，例：开发机上的 coding CLI>` | `<开发机（仓库在 {根}/{域名}/{组}/{项目}）>` | 开发侧＋部署侧 | 编写/修改仓库文件、本地测试与构建自检、git pull 取最新；**并担**构建、部署、服务器端验证、回写部署结果 | MUST NOT 绕过 spec 改需求；MUST NOT 把服务器凭据/runtime 产物提交进 git |
| `<agent-3（按需，例：审查侧 agent）>` | `<位置>` | `<角色>` | `<职责>` | `<禁区>` |

**登记制规则**：
1. 新增 agent ＝ 本表加一行（名称/位置/角色/职责/禁区齐备），其余节不改；项目特殊性写进该仓库 `AGENTS.md` 协作节。
2. 每个 agent 会话开始 MUST 自报身份：`本次会话＝<Agent 名称>（角色：<...>）`，认领登记署名与表内名称一致。
3. 角色划职责不锁工具：同一 agent 可兼多角色（如开发＋部署；也可设纯审查侧 agent）。
4. **部署职责只归运行在部署机上的角色**；本机侧角色禁部署（Owner 临时要求时也先拍板登记例外）。
5. 表中角色被移除/合并＝改表走 Owner 拍板，agent 不得自行扩权。
6. **规则分发链＝skill 触发（不走全局记忆引用行）**：本规则集以 skill 形态随 isettle/skills 仓库分发；每个 agent MUST 把 `multi-agent-global-agents` 安装进自己的技能目录（Hermes＝`~/.hermes/skills/`；Claude Code＝`~/.claude/skills/`；其它支持 SKILL.md 的 CLI 按该工具约定），由 skill 描述触发词在编码/部署会话开始自动载入规则。规则变更＝分发源改版合 PR，各机技能副本同步拉新；`~/AGENTS.md` 只作该机留底副本（内容从分发源同步），不再是 agent 的加载入口。

## 2. 项目根目录与路径规则

**机器级项目根目录默认（所有 agent 遵守）**：

| 系统 | 默认项目总目录 | 说明 |
|---|---|---|
| Linux（开发机） | `/opt/www` | 服务器/开发机侧 agent 一律在此找项目 |
| macOS（本机） | `<启用时填写：本人代码工作区绝对路径>` | 本机侧 agent 的默认项目总目录 |

- 项目落位＝**根目录之下**按仓库远程地址展开：`{根}/{git域名}/{项目组名}/{项目名称}`。
- 示例（虚构域演示）：
  - Linux：`git.example.com:team/order-system.git` → `/opt/www/git.example.com/team/order-system`
  - macOS：`github.com:myorg/myproject.git` → `<macOS 项目根>/github.com/myorg/myproject`
- 项目不在默认根（历史遗留/特殊位置）＝以实际路径为准，并在该仓库 `AGENTS.md` 项目参数节登记例外；不强行迁移。
- 新 clone MUST 按此格式落位，禁止随手放到 `~`、`/tmp` 或根目录第一层。

## 3. 会话初始化规则（所有 agent 同一套）

1. 扫描**本机默认项目总目录**（§2）下所有含 `.git` 的目录，列表呈给 Owner 选项目（会话已明示项目则直接进）。
2. 选定后**立即切到项目根目录**；因 shell 每次命令重置，每条命令 MUST 用 `cd <项目根> && <命令>` 前缀或工具的 `dir_path` 参数。
3. 切换后 MUST 输出：当前工作目录 ＋ 已加载的静态记忆/规则文件清单 ＋ 项目问题与进度自动分析。
4. **开工前 MUST `git pull`**（或 fetch＋reset 到 origin 当前分支），禁止基于陈旧工作区动手——任何 agent 随时可能推送。
5. pull 后先做现状分析：读交接文件（如 `specs/*/HANDOFF.md`）＋ `git log --oneline -10` ＋ `git status`，识别各 agent 已完成/进行中的工作。
6. 工作区有非本人未提交改动＝MUST 停下报 Owner，MUST NOT 覆盖或 `reset --hard` 丢弃。
7. 在交接文件「进行中」区登记任务并**署名本 agent**；**同一任务同时只允许一个 agent 改码（单写者）**，跨任务并行须文件级不重叠。

## 4. 提交与同步纪律

- 小步快跑：一个逻辑单元＝一次 commit，完成即 push（其他 agent 靠 pull 感知进度）。
- push 前必 pull；diverged 用 `git pull --rebase`；禁 force-push、禁改写已推送历史。
- push 后验证 `git rev-parse HEAD` == `origin/<branch>` 才算成功。
- **rebase 后 MUST 跑全仓构建＋测试**（栈等价物，如 `go build ./... && go test ./...`），不止自改包——他人提交可能改公共签名未适配他包测试，单包验证会假绿。发现的破口单独 commit 修，message 注明归属，不替他人背账。
- 判例/编号取号：MUST 在 pull 之后取「下一个全局未用号」，push 前再 pull 复核无撞号；撞号＝后推送方顺延重编并同轮改齐全部引用。
- commit message：一行摘要＋要点列表；禁 conventional 前缀（`feat:`/`fix:` 等）。
- 敏感物零入库：`.env`、`runtime/`、`*.sqlite`、临时凭据文件 MUST NOT 进 git；提交前 `git status` 复核。

## 5. 交接载体

- 项目内 `HANDOFF.md`（或等价文件）是唯一跨 agent 交接载体；真相源层级：spec > HANDOFF。
- 每次会话结束/阶段完成 MUST 更新：版本锚、本轮完成项（署名哪一 agent）、进行中/待接手项、已知坑与复验方法、测试现状。
- 写「完成」前必须测试跑过、可复核；跑不了如实写卡在哪一步。
- 部署结果由部署机侧 agent 回写（时间、commit、健康检查摘要）；其他 agent 不臆测线上状态。
- Owner 问「改了什么/怎么没生效」＝先摆生效链：本方 pull→push→对侧 agent pull→重建→线上验证，逐环指卡点；**push ≠ 线上生效**（对侧是被动会话，不叫不动）。

## 6. 部署（只由部署机侧角色执行）

- 入口＝仓库内 deploy 脚本（幂等：pull → 构建 → 滚动重启 → 健康检查）；路径规则见 §2。
- 凭据与运行时文件放仓库内 gitignore 区（如 `backend/.env`、`runtime/`），不入库、不经对话明文。
- 单实例红线应用 MUST NOT 并行跑两个实例（更新先摘旧再起新）。
- 部署后 MUST 逐条复核健康检查（接口探活、页面状态码、域名路由），不得只看进程/容器 Up。
- 改判拍板执行完当轮，把「待部署」回写交接文件并告知 Owner 催部署方式。

## 7. 冲突与裁决

- 任意两方以上结论冲突、或实现与 spec 冲突：**spec 条款编号 > 项目宪法 > 通用惯例**；无法自决列证据交 Owner 裁决，MUST NOT 静默改需求。
- 任何一方已推送的判例/编号（B 编号、FR 编号等）MUST 沿用，禁止重编号或反向推翻。
- 语义不明的历史改动：先读 spec/交接文件/commit message 溯源，仍不明问 Owner，不按猜测动手。
- 多 agent 同文件 rebase 冲突：自己解冲后再 push；解冲不得静默丢对方语义行（保留双方判据行，冲突处报 Owner）。
