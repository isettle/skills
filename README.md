# skills

各类目的 agent 技能与配套物料集合。目录约定：**每个类型/流程一个顶层目录**，目录内含各自 skills 与配套物料，互不依赖。

| 目录 | 类型 | 内容 |
|---|---|---|
| [`tob-sdd/`](tob-sdd/README.md) | ToB 后台 × spec-kit SDD 流程 | 5 个执行技能（spec-kit-sdd / sdd-speckit-research / grill-me / domain-modeling / shadcn-admin-frontend）＋ 6 件治理物料模板（AGENTS/宪法/DESIGN/intent/落位与回写规则） |
| [`coding-rule/`](coding-rule/SKILL.md) | 多 Agent 编码项目全局规则 | **多 agent 共开发同一代码项目时才触发**的全局规则模板（skill 分发）：Agent 花名册登记制／机器默认根／同步·交接·部署·裁决纪律＋装法与踩坑 |

## 安装方式

- **Hermes**：`cp -R <集合>/skills/* ~/.hermes/skills/`（如 `tob-sdd`）；单技能顶层目录直接 `cp -R coding-rule ~/.hermes/skills/`
- **Claude Code**：`cp -R <集合>/skills/* ~/.claude/skills/`（SKILL.md 格式兼容）
- **Codex / Qoder / Cursor**：拷各自 `<集合>/materials/` 进项目仓库根（AGENTS.md 原生识别），无自动加载机制

## 收录红线（入库前必跑，零命中才 commit）

```bash
python3 scripts/sanitize_scan.py    # 命中即退出码 1，并列出文件:行号
```

- 公司名、真实项目名、内网域名/IP、服务器地址
- 个人机器绝对路径（home 目录开头的路径）、凭据与凭据字样实值
- 真实业务域例子（统一改写为电子商城等虚构域）

新增敏感词直接往 `scripts/sanitize_scan.py` 的 `TOKENS`/`PATTERNS` 里加。
