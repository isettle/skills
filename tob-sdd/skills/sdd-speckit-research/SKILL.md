---
name: sdd-speckit-research
description: "Use for spec-kit/SDD artifact or command questions."
license: MIT
metadata:
  hermes:
    tags: [spec-kit, SDD, spec-driven-development, github]
    related_skills: []
---

# Spec-Kit (SDD) verified facts

Answering questions about GitHub spec-kit artifacts/commands from memory risks stale or invented structure. This skill holds facts verified against the repo and docs site (as of 2026-09).

## Where to verify (fetch order)

1. Real templates that exist: `raw.githubusercontent.com/github/spec-kit/main/templates/` → `spec-template.md`, `plan-template.md`, `tasks-template.md`, `checklist-template.md`, `constitution-template.md`.
   Pitfall: `data-model-template.md` and `quickstart-template.md` are 404 — data-model/contracts/quickstart structure is defined in `templates/commands/plan.md` (the plan command workflow), not standalone template files.
2. Docs site (cleaner than repo): `github.github.com/spec-kit/quickstart.html`, `/guides/existing-projects.html`, `/reference/agentic-sdd.html`.
3. Full repo tree listing when unsure which file exists: `api.github.com/repos/github/spec-kit/contents/templates`.
4. Workflow subsystem (engine, steps, gates, overlays, catalog, feature provenance): `references/workflows.md` — verified against `docs/reference/workflows.md` on main.

Pitfall: the release-notes changelog only lists PR titles — for a feature's WHY, read the introducing PR's body via `api.github.com/repos/github/spec-kit/pulls/<n>` (find the PR number by scanning release bodies for the feat line).

## Core facts

- Full command chain (9 steps): constitution → specify → clarify → plan → checklist → tasks → analyze → implement → converge. Short path for small features: specify → plan → tasks → implement → converge. Only specify-before-plan is strictly required; clarify/checklist/analyze are optional quality gates.
- spec.md mandatory sections (marked `*(mandatory)*` in template): User Scenarios & Testing (prioritized P1/P2/P3 user stories, each independently testable, Given/When/Then acceptance, Edge Cases), Requirements (FR-xxx, `[NEEDS CLARIFICATION: ...]` markers), Success Criteria (SC-xxx, measurable + technology-agnostic). Conditional: Key Entities (only if data). Optional: Assumptions.
- Official spec-template structure verified against upstream raw template (2026-10): NO top-level Overview/Purpose/Scope section; Edge Cases is a `###` subsection UNDER `## User Scenarios & Testing`, not a top-level section; all major sections are H2; FRs are list items `- **FR-001**:` (no heading-per-FR). A third-party "team spec template" carrying numbered top-level sections (1. Overview … 6. Assumptions) is a self-invented skeleton — judge principle-layer vs skeleton-layer separately before adopting (see spec-kit-sdd 合规性判定变体).
- plan.md: Summary, Technical Context (unknowns as NEEDS CLARIFICATION), Constitution Check (gate before Phase 0 + re-check after Phase 1), Project Structure, Complexity Tracking (only when constitution violated). Phase 0 → research.md; Phase 1 → data-model.md + contracts/ + quickstart.md.
- Artifact placement rule: API docs → `contracts/` (machine-readable, OpenAPI/AsyncAPI/Proto), data dictionary → `data-model.md` (entities/fields/relations/state machines); never in spec.md. Litmus test: statement survives a tech-stack swap → spec.md, else data-model/contracts.
- State machine placement, refined (项目A 2026-09-22, user-confirmed): spec.md MAY carry the closed state ENUMERATION + WHAT-level transition rules as FR MUSTs (e.g. "唯一合法回退 = 签署中→草稿"、完成态=系统推导无人工入口、作废前提); the per-transition table (当前状态×动作×触发方→目标态 + 非法流转处理 + 副作用如回补库存/释放占用) belongs to plan-phase `data-model.md` — say so explicitly in spec Assumptions so the handoff is visible. Litmus refinement: "which states exist and legal/illegal movement" = spec; "exact transition mechanics and side effects" = data-model.md.
- 低保真原型/交互流程 placement (same session): page-level interaction (button names, dialogs, field layout, multi-step forms) NEVER in spec.md — no 「点击XX按钮」「跳转到XX页」 wording in spec. Prototype files live IN the feature dir (e.g. `specs/NNN/design/` or `preview/`) so `/speckit-converge` versions spec ↔ prototype together; walkthrough steps derived from the flow go to quickstart.md. Legacy-SDLC mapping: 低保真原型 ≈ UI图 → plan-phase referenced design source, same position as API doc/data dictionary. 原型改动回写三分类（用户定）：① 业务规则冲突＝以 spec.md 为准修正原型；若原需求本身变化，先改 spec.md 再同步原型。② 纯 UI 表达变化（弹层改抽屉、按钮位置调整）＝只改原型，不回写 spec.md，留在 design/。③ 交互流程实质变化——凡触及完成任务步骤数、确认义务、数据丢失风险、系统行为之一，不得一概归为 UI 微调，须先判定是否构成需求变化：是 → 走①的先改 spec.md（写成 FR）再同步原型与 quickstart.md；否 → 才降级为②。分界例：确认弹层改抽屉=②；去掉确认弹层直接落单=③；弹层关闭不提示丢弃已填内容=③。
- Active feature tracked by `.specify/feature.json` (or `SPECIFY_FEATURE_DIRECTORY` env), NOT the git branch; git feature branches are an opt-in extension.
- Team extension (NOT upstream): this team's `intent.md` (需求说明/需求痛点/需求草稿/泳道图 four sections + §5 grill拷问记录) sits at the very front of the flow — BEFORE /speckit-constitution (first build) and /speckit-specify — at `specs/NNN-*/intent.md`. GI gate is two-stage: ① four sections non-empty (pain points carry cost numbers, swimlane renders) → ② once basic content exists, MUST run skill `grill-me` (frontier rounds; Owner ruling 2026-10-22 removed upstream grill-with-docs/grilling) together with vendored `domain-modeling` until no open branch, with decisions (ADR-style) + glossary written back into §5 (glossary feeds Key Entities confirmation). Naming: hand-create the feature dir for intent.md, then pass SPECIFY_FEATURE_DIRECTORY explicitly to /speckit-specify (else it auto-creates a different dir = duplicate). intent.md freezes as a traceability snapshot once spec is finalized — later changes go through 回写三分类 into spec.md, never back into intent.md. Upstream spec-kit has no such artifact.
- tasks.md format: `T0XX [P] [US1] description + exact file paths`; phases Setup → Foundational (blocks all stories) → one phase per user story with Checkpoint → Polish. Test tasks optional (only if spec requests).
- checklist `[x]` = reviewer-confirmed requirements quality, NOT implementation done.
- Command invocation form varies by agent: `/speckit.*`, `$speckit-*` (Codex), `/skill:speckit-*` (Kimi).
- The specify CLI's workflow subsystem is a YAML step engine distinct from GitHub Actions (command/prompt/shell/gate/fan-out steps, catalog-distributed); answering anything about it requires `references/workflows.md`, not memory.

## User context (this team)

This team is migrating a traditional e-commerce SDLC (PRD → backend API doc + data dictionary → UI mockups → frontend → joint debugging → QA) to spec-kit. Team note-format convention: one running e-commerce (电子商城) example threaded through every artifact/item, tables over prose. The reusable ToB 后台物料集（AGENTS/constitution/DESIGN/intent 模板＋落位与回写规则）ships in this pack's `materials/` directory — new ToB projects copy from there and fill §P.
