# ToB SDD 物料与技能包（tob-sdd）

技术部 SDD（spec-kit）开发流程的团队共享包，含**治理物料模板**与**AI 代理执行技能**两层。
沉淀自两个内部 ToB 后台项目实际跑通的流程，例子域统一为电子商城。

## 目录结构

```
sdd-team-pack/
├── materials/        # 治理物料模板（与 agent 无关，任何项目/任何 AI 都可拷用）
│   ├── README.md                      # 物料集导航 + 新项目接入 5 步
│   ├── AGENTS.template.md             # → 仓库根 AGENTS.md（填 §P）
│   ├── constitution.template.md       # → .specify/memory/constitution.md
│   ├── DESIGN.template.md             # → 仓库根 DESIGN.md（UI-GATE 真相源）
│   ├── intent.template.md             # → specs/NNN-*/intent.md（流程最前端，GI 门禁）
│   └── spec-kit物料落位与回写规则.md   # 内容写哪个文件 + 原型回写三分类
└── skills/           # AI 代理技能（SKILL.md 通用格式）
    ├── spec-kit-sdd/          # SDD 全流程执行经验（各阶段 pattern + 踩坑）
    ├── sdd-speckit-research/  # spec-kit 官方结构已验证事实（答规范问题先查它）
    ├── grill-me/              # GI 门禁第二段：需求对抗拷问（等价 grill-with-docs）
    └── shadcn-admin-frontend/ # React+shadcn-admin 前端搭建铁律与 CN 网络配方
```

## 流程一图（本包定稿版）

`intent.md（GI 门禁：四段＋拷问）→ constitution → specify → preview 原型（G1）→ clarify（G0'）→ plan → checklist（G2'）→ (analyze) → tasks → implement（G2 六件套 + UI-GATE）→ converge（G3）`

## 怎么用（分角色）

### 项目 Owner / 任何开发者：materials/

新项目开工时按 `materials/README.md` 的 5 步接入；也可整目录拷到项目参考位置。
这层是纯 Markdown，不依赖任何 AI 工具。

### Hermes 用户：装 skills/

```bash
git clone git@github.com:isettle/skills.git   # 或 https://github.com/isettle/skills.git
cp -R skills/tob-sdd/skills/* ~/.hermes/skills/
# 有同名 skill 已存在时先备份再覆盖，或逐目录 diff 后合并
```

装完在会话里 `/skills` 或让 agent `skills_list` 可见即生效；agent 会按任务自动加载。

### Claude Code 用户：转成 plugin 安装

SKILL.md 与 Claude Code 的 Agent Skills 格式相同，目录名即技能名。

```bash
# 最简：把 tob-sdd/skills/<name>/ 逐个拷入 ~/.claude/skills/
cp -R skills/tob-sdd/skills/* ~/.claude/skills/
```

### Codex / Qoder / Cursor 用户

无自动加载机制，但物料层的 `AGENTS.md`（Qoder/Codex 原生识别）+ 各 spec 目录文件已覆盖流程约束；把 `materials/` 拷进仓库即可，agent 读 AGENTS.md 就按本流程干活。

## 与 /speckit-* 斜杠命令的关系

`/speckit-specify` 等命令由 spec-kit CLI 在每个项目里生成（`specify init --here --integration hermes`），**不在本包内**。本包负责的是：命令之外的流程约束（intent/GI、原型门禁、回写三分类）+ 执行经验（skills/）。

## 维护约定

- 本目录（isettle/skills 仓库的 `tob-sdd/`）是**唯一分发源**；各人本机 skills/ 与项目内物料是消费副本。
- 流程规则变化（门禁、回写分类、落位判据）改 `materials/` 并走一次团队评审；执行经验（pattern、踩坑）由各人会话沉淀后 PR 合入 `skills/`。
- 提交前跑脱敏自查：真实凭据 / 个人绝对路径 / 内网主机 IP 不得入库（示例用 `<待填>` 与电子商城虚构数据）。
- commit message 禁 conventional 前缀（`feat:`/`fix:`），一行摘要＋要点列表；commit 后 pull --rebase＋push，`rev-parse HEAD == origin/master` 验证。

## 已知待复核（Owner 未最终拍板项）

- `intent.md` 拼写（英文习惯 intent/intend）与 GI 门禁命名已按 2026-10-22 拍板定稿。
- G0'（clarify）与 G2'（checklist）在 AGENTS 模板中标【待复核】，团队试用后定去留。
- `grill-me` 为 mattpocock `grill-with-docs` 的本机等价执行体；若团队引入上游原 skill，替换 skills/grill-me 并把 intent 模板引用改指 grill-with-docs。
