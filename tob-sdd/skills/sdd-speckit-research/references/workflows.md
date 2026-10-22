# Spec Kit workflow subsystem — verified facts

Source of truth: `raw.githubusercontent.com/github/spec-kit/main/docs/reference/workflows.md` (or docs site `github.github.com/spec-kit/reference/workflows.html`). Provenance via GitHub releases API filtered for `workflow`+`feat` lines.

## What it is / why it exists

A YAML-declared multi-step automation engine inside the specify CLI (`specify workflow *`) — NOT GitHub Actions. Introduced with the workflow engine + catalog system at CLI v0.7.0. It solves five problems of manually driving the SDD command chain:

1. Chain specify→plan→tasks→implement in one declarable run instead of hand-typing each step.
2. Persistent run state — a chat-driven flow loses context on interruption; workflows resume from the exact step.
3. `gate` steps make human review an unskippable node instead of a discipline.
4. `command` steps name an `integration` per step — the process definition is decoupled from the agent (same YAML runs on claude/copilot/gemini/...).
5. Catalog + overlays make the team's process itself an installable, versioned, distributable artifact.

## CLI surface (all routine use is CLI; YAML only for authoring/customizing)

- `specify workflow search|add|run|resume|status|list|update|enable|disable|remove|info|validate`
- `specify workflow overlay add|list|<priority change>`; `specify workflow catalog list|add|remove`; `specify workflow step` (custom step packages)
- `run` accepts catalog id, URL, or local file; missing inputs prompt interactively; `--json` prints one machine object on stdout (progress goes to stderr).
- `workflow add <id> --version X` pins exact catalog release.

## Step types & expressions

`command`, `prompt`, `shell`, `gate`, `if` (then/else), `switch`, `while`, `do-while`, `fan-out`/`fan-in`, plus installed custom step packages. Expressions: `{{ inputs.x }}`, `{{ steps.<id>.output.<key> }}`, `item`, `context.run_id`, `context.workflow_dir`; filters `default, join, contains, map, from_json` (+ upper/lower/split/length/to_json).

## State & resume

Per run: `.specify/workflows/runs/<run_id>/{state.json, inputs.json, log.jsonl}`. `resume` replays completed steps and continues at the unfinished one (gate pause or failure). `verdict_input` binds a gate verdict to a declared workflow input.

## Overlays (the sanctioned customization path)

Project overlays live at `.specify/workflows/overlays/<id>/*.yml` — OUTSIDE the installed workflow dir, so they survive `workflow update`/reinstall/`bundle update`. Format: `id`, `extends` (base workflow id), `priority` (default 10; lower wins conflicts — confirm against current docs when composing multi-overlay setups), `enabled`, `edits[]` with operations `insert_after` / `insert_before` / `replace` / `remove` anchored on a base step id. Anchors resolve recursively into then/else/steps/cases blocks, but NOT fan-out templates.

Overlay limits (do not fight them): step-list edits only — cannot change inputs/metadata/`requires`/expression logic, cannot target steps added by another overlay.

## Pitfalls

- **Never edit an installed `workflow.yml` in place** — `specify workflow update` / `add` / bundle update overwrites it, losing customizations. Write an overlay instead. This is the #1 trap.
- An overlay referencing a nonexistent step id only errors at workflow resolution/run time, not at `overlay add`.
- Step ids must not contain `:` (engine-reserved for nested ids).
- Renaming/removing a step id or an output key breaks: (a) `resume` of paused runs (locates by id), (b) downstream `{{ steps.x.output.y }}` expressions (silently empty). Replace-with-same-id is the safe pattern.
- Maintainers do NOT audit workflow `run`/shell fields — read a community workflow's source before running it; expression interpolation into shell has an injection surface (docs have an interpolation-safety section).
- `workflow_id` is the `workflow.id` inside the YAML, not the filename.
- Only local-file runs (`specify workflow run ./x.yml`) work outside a project; other workflow commands need `specify init`.
- Gates pause forever waiting for human input; automation contexts must pre-bind `verdict_input` or plan for `resume`.

## Provenance table (feature → CLI version)

| Feature | Version |
|---|---|
| Workflow engine + catalog | 0.7.0 |
| `bug-assess` workflow (issue triage) | 0.11.2 |
| `assess` idea-assessment pipeline extension | 0.13.0 |
| `feature-assess` agentic workflow (self-installing) | 0.16.5 |
| First-party **bugfix + assess bundles** (formal promotion) | 1.0.9 |
| Workflow slots, per-step integration config | 1.0.5 / 1.0.6 |
| Exact version pins for workflows/steps/presets | 1.1.0–1.1.1 |
| Unified execution-tree composition | 1.1.3 |
| Built-in GitHub workflow step | 1.2.0 |
