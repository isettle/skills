# Changelog

本技能所有值得注意的变更都记录在此。
格式遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

发布约定：变更随手记入 `[Unreleased]` → 归入新版本号段落（同步 bump SKILL.md frontmatter `version`）→ commit＋push → `rev-parse HEAD == origin/main` 验证。

## [Unreleased]

- 技能改名（二）：`multi-agent-global-rules` → **`coding-rule`**（Owner 2026-10-23 拍板：名称直指用途，并明确**触发范围＝多个 agent 共同开发同一个代码项目时才触发**——单 agent 项目、非代码项目不适用）。目录/`name:`/`description:`/拷贝命令/仓库 README/模板用法行同步；When to Use 重写为触发条件优先。
- 技能改名（一）：`multi-agent-global-agents` → `multi-agent-global-rules`（旧名以载体 AGENTS.md 结尾易误导，且包内已不提 AGENTS.md，名实不符）。目录/`name:`/拷贝命令/仓库 README 全部同步；历史段落（1.0.0/1.1.0 条目内旧技能名与旧模板文件名）作为当时事实保留不改。

## [1.1.0] - 2026-10-23

Owner 拍板链定稿：**skill ＝ 唯一生效链**。

### Changed

- 规则分发链改为 skill 触发（`8a501e6`/`fb547b5`）：各 agent 把技能装进自己的技能目录，触发词在编码/部署会话开始自动载入；不再经由「机器本地规则文件入口」或「agent 全局记忆文件顶部引用行」两种旧形态。
- 包内清除全部 `AGENTS.md` 字样（`8a501e6`）：模板改名 `templates/GLOBAL-AGENTS.template.md` → `templates/global-rules.md`；仓库级点名（"见仓库根 AGENTS.md"）改泛称「项目级规则文档／项目级协作细则文档／项目参数文档」，本模板不点名他文档，防多真相源歧义。
- 删除本地规则文件路径表述（`d2f69a7`）：`~/AGENTS.md`、`/root/AGENTS.md` 等不再出现在技能内；§1 登记制第 6 条定稿＝「任何机器本地规则文件/全局记忆副本 MUST NOT 作为加载入口（历史遗留仅留档）」。
- 装法重排为 4 步：装 skill＝入口（第 1 步）→ 机器参数改技能副本内文件或 Owner 会话口述生效（第 2 步）→ 新 agent 接入＝花名册加行＋装 skill＋自报身份（第 3 步）→ 更新链＝分发源 PR→各 agent pull＋重拷，私有参数不回传（第 4 步）。

### Added

- SKILL.md 踩坑节新增「历史形态演变」条目：本地文件入口 → 全局记忆引用行 → skill 唯一链，警示旧遗留文件/引用行应清理或标仅留档。
- frontmatter `description` 去除 AGENTS.md 字样，改为「multi-agent collaboration rules」。

## [1.0.0] - 2026-10-23

首个发布版（`9fab9e9`，isettle/skills 顶层目录，独立于 tob-sdd）。

### Added

- 多 Agent 全局协作规则模板 `templates/GLOBAL-AGENTS.template.md`（当时形态＝机器级本地文件），七节：§0 一分钟版；§1 Agent 花名册（登记制——新 agent 加一行即可）；§2 项目根与路径（Linux 默认 `/opt/www`；macOS 默认自登工作区根；根下 `{git域名}/{组}/{项目}` 落位）；§3 会话初始化（pull 先行、单写者认领署名）；§4 提交同步（`HEAD==origin/<branch>` 验证、rebase 后全仓测、取号防撞、禁 force-push/禁 conventional 前缀、敏感物零入库）；§5 交接（HANDOFF 唯一载体、spec > HANDOFF、push≠生效摆链）；§6 部署（幂等脚本、单实例红线、逐条健康复核）；§7 裁决（spec > 宪法 > 惯例、判例沿用、解冲不丢行）。
- SKILL.md：When to Use、装法、改版踩坑（备份→原子替换→md5 复核；ssh 传输 base64 包裹防引号解析坏；双→多 Agent 措辞清扫；机内私有副本不回传＋sanitize_scan 零命中红线）。
- 规则集来源＝两个 ToB 项目实跑的多 agent 协作纪律（2026-10-19 首版双 Agent，2026-10-23 升级登记制＋机器默认根）。

<!-- 链接区 -->
[1.1.0]: https://github.com/isettle/skills/commit/8a501e6
[1.0.0]: https://github.com/isettle/skills/commit/9fab9e9
