---
name: coding-rule
description: "Use when multiple agents co-develop one code project."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [agents, collaboration, workflow, multi-agent]
---

# 多 Agent 编码项目全局规则（coding-rule）

## When to Use

**仅在多个 agent 共同开发同一个代码项目时触发**（本机一个＋开发机一个、或多台多 agent 并行）。触发场景：agent 进入此类项目的编码/部署/交接会话，或用户要求维护/升级多 agent 协作规则（如既有规则还写着「双 Agent」需升级为任意数量 agent）。单 agent 项目、非代码项目不触发。本技能给出规则模板、装法与改版踩坑。

## 内含

- `templates/global-rules.md`：规则正文（已脱敏，虚构域示例）。章节：
  - §0 一分钟版（项目在哪 / 开工四步 / 收工三步 / 自报身份）
  - §1 **Agent 花名册（登记制）**——新增 agent＝加一行（名称/位置/角色/职责/禁区），其余节不动；部署职责只归部署机侧角色
  - §2 **项目根与路径规则**——机器级默认根：Linux 开发机＝`/opt/www`；macOS 本机＝填写项（如个人代码工作区根，各机自登）；根下按 `{git域名}/{项目组名}/{项目名称}` 落位，禁止乱放
  - §3 会话初始化（扫默认根选项目、cd 前缀/dir_path、开工 MUST pull、非本人未提交改动停下报 Owner、单写者认领署名）
  - §4 提交与同步（小步 commit 即 push、push 后 `HEAD==origin/<branch>` 验证、rebase 后全仓 build+test 防假绿、判例取号 pull 后取 push 前复核、禁 force-push、禁 conventional 前缀、敏感物零入库）
  - §5 交接载体（HANDOFF 唯一跨 agent 载体、spec > HANDOFF、push≠线上生效先摆链）
  - §6 部署（幂等 deploy 脚本、凭据进 gitignore 区、单实例红线、部署后逐条健康复核）
  - §7 冲突与裁决（spec 编号 > 宪法 > 惯例；已推送判例沿用；解冲不丢对方语义行）

## 装到机器（用法）

1. **规则加载链＝skill（唯一生效链）**：把本技能目录拷进该机每个 agent 的技能目录（Hermes：`cp -R coding-rule ~/.hermes/skills/`；Claude Code：`cp -R coding-rule ~/.claude/skills/`；其它支持 SKILL.md 的 CLI 按各自约定）——会话开始由触发词自动载入，规则正文＝本技能包内 `templates/global-rules.md`（或经 skill_view 读 SKILL.md）。**不依赖任何机器本地规则文件或 agent 全局记忆副本作加载入口。**
2. 填机器参数：§2 表格里本机的默认项目根、§1 花名册行的实际 agent 名——直接改各机技能副本内文件（属各机私有配置），或经 Owner 在会话里口述生效。
3. 接入新 agent＝§1 加一行 + 该 agent 装本 skill + 会话开场自报身份；有项目特殊性再写该仓库自己的项目级细则文档（细则归项目，全局只管共性）。
4. 规则更新＝分发源 PR 改版 → 合入后通知各 agent `git pull` ＋ 重拷技能目录；各机技能副本的私有参数改动 MUST NOT 回传分发源。

## 踩坑（实跑验证）

- 历史形态演变（避免再绕回去）：「各机放一份本地规则文件当入口」→「agent 记忆文件顶部加引用行」→ 现行＝**skill 唯一生效链**。前两种形态遗留的本地文件/引用行应清理或明确标仅留档，防多真相源歧义。
- 改机内文件三连（仍适用于清理旧遗留）：`cp -a` 带日期备份 → 写 `*.new` 临时文件再 `mv -f` 原子替换 → 落盘后远端 `md5sum` 与本地比对＋抽验头尾行。
- 长文件经 ssh 传输用 base64 包裹（`echo <b64> | base64 -d >`），避开引号/Tcl 注入把命令解析坏；密码走 env 传，绝不进对话/命令行。
- 「双 Agent」改「多 Agent」的清扫：全文搜残留单数措辞（两 agent/对方/两个 → 所有 agent/其他 agent），职责表、冲突节都过一遍。
- 技能包与机内副本分家：**机内副本含真实路径/域名，永不回传本仓库**；向本仓库提 PR 的内容必须过 `scripts/sanitize_scan.py` 零命中（禁个人绝对路径、真实域名/IP/项目代号/凭据）。

## 版本与来源

v1.1（2026-10-23）：分发链定稿＝skill 唯一生效链，包内不再出现任何本地规则文件路径表述（Owner 拍板防歧义）。规则集沉淀自两个 ToB 项目实跑的多 agent 协作纪律（2026-10-19 首版双 Agent，2026-10-23 升级登记制＋机器级默认根：Linux `/opt/www`、macOS 自登工作区根）。
