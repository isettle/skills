---
name: multi-agent-global-agents
description: "Use when maintaining a multi-agent global AGENTS.md."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [agents, collaboration, workflow, multi-agent]
---

# 多 Agent 全局项目规则（GLOBAL-AGENTS 模板）

## When to Use

用户在一组 git 仓库上用**多个编码 agent 并行开发**（本机一个、开发机一个、未来更多），需要一份机器级全局规则统一它们的协作行为；或既有全局 AGENTS.md 还写着「双 Agent」需要升级为任意数量 agent。本技能给出模板、装法与改版踩坑。

## 内含

- `templates/GLOBAL-AGENTS.template.md`：通用模板（已脱敏，虚构域示例）。章节：
  - §0 一分钟版（项目在哪 / 开工四步 / 收工三步 / 自报身份）
  - §1 **Agent 花名册（登记制）**——新增 agent＝加一行（名称/位置/角色/职责/禁区），其余节不动；部署职责只归部署机侧角色
  - §2 **项目根与路径规则**——机器级默认根：Linux 开发机＝`/opt/www`；macOS 本机＝填写项（如个人代码工作区根，各机自登）；根下按 `{git域名}/{项目组名}/{项目名称}` 落位，禁止乱放
  - §3 会话初始化（扫默认根选项目、cd 前缀/dir_path、开工 MUST pull、非本人未提交改动停下报 Owner、单写者认领署名）
  - §4 提交与同步（小步 commit 即 push、push 后 `HEAD==origin/<branch>` 验证、rebase 后全仓 build+test 防假绿、判例取号 pull 后取 push 前复核、禁 force-push、禁 conventional 前缀、敏感物零入库）
  - §5 交接载体（HANDOFF 唯一跨 agent 载体、spec > HANDOFF、push≠线上生效先摆链）
  - §6 部署（幂等 deploy 脚本、凭据进 gitignore 区、单实例红线、部署后逐条健康复核）
  - §7 冲突与裁决（spec 编号 > 宪法 > 惯例；已推送判例沿用；解冲不丢对方语义行）

## 装到机器（用法）

1. **规则加载链＝skill**：把本技能目录拷进该机每个 agent 的技能目录（Hermes：`cp -R multi-agent-global-agents ~/.hermes/skills/`；Claude Code：`~/.claude/skills/`；其它支持 SKILL.md 的 CLI 按各自约定）——会话开始由触发词自动载入，无需任何"全局记忆引用行"。
2. 留底副本（可选兜底，非加载入口）：把 `templates/GLOBAL-AGENTS.template.md` 拷到 `~/AGENTS.md`（Linux root＝`/root/AGENTS.md`；macOS＝家目录），供不认 skill 机制的工具人工取读。
3. 填机器参数：副本 §2 表格里本机的默认项目根（可写真实绝对路径——机内副本是私有位）；§1 花名册行换成实际在册 agent 名。
4. 接入新 agent＝§1 加一行 + 该 agent 装本 skill + 会话开场自报身份；有项目特殊性再写该仓库 `AGENTS.md` 协作节（细则归项目，全局只管共性）。
5. 规则更新＝分发源 PR 改版 → 合入后通知各 agent `git pull` ＋ 重拷技能目录（及留底副本）；各机私有副本 MUST NOT 回传分发源。

## 踩坑（实跑验证）

- 改既有全局文件三连：`cp -a` 带日期备份 → 写 `*.new` 临时文件再 `mv -f` 原子替换 → 落盘后远端 `md5sum` 与本地比对＋抽验头尾行。
- 长文件经 ssh 传输用 base64 包裹（`echo <b64> | base64 -d >`），避开引号/Tcl 注入把命令解析坏；密码走 env 传，绝不进对话/命令行。
- 「双 Agent」改「多 Agent」的清扫：全文搜残留单数措辞（两 agent/对方/两个 → 所有 agent/其他 agent），职责表、冲突节都过一遍。
- 模板与机内副本分家：**机内副本含真实路径/域名，永不回传本仓库**；向本仓库提 PR 的内容必须过 `scripts/sanitize_scan.py` 零命中（禁个人绝对路径、真实域名/IP/项目代号/凭据）。

## 版本与来源

v2 规则集沉淀自两个 ToB 项目实跑的多 agent 协作纪律（2026-10-19 首版双 Agent，2026-10-23 升级登记制＋机器级默认根：Linux `/opt/www`、macOS 自登工作区根）。
