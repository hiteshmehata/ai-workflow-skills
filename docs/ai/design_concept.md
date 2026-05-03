# Design Concept

## Product

Define a workflow-driven planning and implementation system for AI coding agents. The system should force clarity about what needs to be built and why before implementation starts, then let the agent execute with bounded autonomy using specialized skills.

## Primary User

- Primary user: the developer operating an AI coding agent
- Secondary user: other developers who adopt the same workflow and skill set

## Problem

The current failure mode is building the wrong feature because the request is ambiguous, underspecified, or missing explicit agreement on scope and goals. The system needs a repeatable way to detect ambiguity, force clarification, and establish the artifacts required before implementation begins.

## Goal

Before code is written, the developer and agent should be aligned on:

- what will be built
- why it is being built
- what is in scope and out of scope
- the implementation slices that will be executed
- the approval boundary for starting implementation

The agent should then determine how to implement the work using the workflow and relevant skills.

## Non-Goals

- Turning planning artifacts into rigid compiler-style specifications
- Requiring full upfront implementation detail for every task
- Running the full planning workflow for trivial changes
- Replacing human approval for medium or large changes

## Desired Outcome

For medium and large work, the workflow should prevent ambiguous requests from going straight into coding. It should produce explicit, durable artifacts under `docs/ai/` that authorize implementation only after the user approves the PRD.

## Workflow Shape

The workflow is a sequence of specialized skills and review steps:

1. `grill-me`
2. `ubiquitous-language` when triggered
3. `write-prd`
4. `slice-planner`
5. implementation loop using TDD and the broader AI coding workflow
6. reviewer agents after every implementation slice

`grill-me` and `ubiquitous-language` are general-purpose skills that this workflow reuses rather than workflow-specific skills that exist only for coding-agent execution.

## Artifact Gate

### Required Always

- `docs/ai/prd.md`
- `docs/ai/backlog.md`

### Required Sometimes

- `docs/ai/ubiquitous_language.md`
- `docs/ai/research.md`

### Optional

- `docs/ai/handoff.md`

## Minimum Gate By Task Type

### Required When `grill-me` Runs

- `docs/ai/design_concept.md`

`docs/ai/design_concept.md` is required for any medium or large work item and any task that triggers `grill-me`.

### Greenfield Feature

Required artifacts:

- `docs/ai/design_concept.md`
- `docs/ai/research.md`
- `docs/ai/prd.md`
- `docs/ai/backlog.md`

### Existing Feature Change

Required artifacts:

- `docs/ai/prd.md`
- `docs/ai/backlog.md`

`docs/ai/design_concept.md` is additionally required for any behavior change or architecture change that triggers `grill-me`.

### Bug Fix

Required artifacts:

- `docs/ai/prd.md`
- `docs/ai/backlog.md`

Bug fixes use the same PRD template as other work.

### Refactor Or Architecture Cleanup

Required artifacts:

- `docs/ai/design_concept.md`
- `docs/ai/prd.md`
- `docs/ai/backlog.md`

## Medium Or Large Work Trigger

`grill-me` runs for medium or large work. Medium or large work is any request that matches one or more of these signals:

- touches multiple subsystems
- changes user-visible behavior
- has more than one plausible implementation path
- needs rollout or migration thinking

Trivial changes are exempt from this requirement.

## Ambiguity Detection

The request is too ambiguous to implement when any of these conditions hold:

- missing user-visible outcome
- unclear in-scope or out-of-scope boundary
- unknown integration boundary
- undefined failure behavior
- undefined data model change

When ambiguity is detected, the agent should stop and clarify rather than start coding blindly.

## User Interaction Policy

When ambiguity is detected, the agent should:

1. call out what is unclear
2. ask targeted follow-up questions
3. prefer yes/no questions or a short set of explicit options
4. wait for confirmation before moving forward on medium or large work

## Grill-Me Contract

`grill-me` produces `docs/ai/design_concept.md`.

Its purpose is to force shared understanding of the problem, goals, scope, and start conditions before PRD generation.

## PRD Contract

`docs/ai/prd.md` must include:

- problem
- goal
- non-goals
- user stories
- constraints
- acceptance criteria
- rollout
- testing expectations

## Backlog Contract

Each slice in `docs/ai/backlog.md` must include:

- title
- behavior statement as the outcome
- touched systems or files
- blockers or dependencies

Acceptance criteria and tests are not mandatory as separate fields in the backlog because the outcome should be written in a testable way.

## Ubiquitous Language Trigger

`docs/ai/ubiquitous_language.md` is required for existing codebases with domain terms.

## Research Trigger

`docs/ai/research.md` is required when the work includes:

- an architecture decision with multiple viable options
- integration with an unfamiliar subsystem

## Architecture Skill Trigger

The architecture improvement skill for deep modules and simple interfaces runs only during refactors.

## Implementation Start Condition

Implementation is authorized when the PRD is approved by the user.

## Implementation Planning Boundary

Before coding starts, the implementation plan must include:

- slices
- touched systems or files
- design decisions

The workflow should not require full detailed implementation before coding. It should specify enough structure to constrain execution without turning planning into premature coding.

## TDD Policy

TDD is mandatory except for trivial changes.

The implementation loop should prefer a red-green-refactor sequence so that each slice has immediate feedback.

## Reviewer Agent Policy

Reviewer agents run after every implementation slice.

Initial reviewer specializations:

- security
- reliability
- UX consistency
- architecture
- test quality

## Artifact Ownership

During execution, the implementation loop may refine `docs/ai/backlog.md` or `docs/ai/prd.md` when reality changes, but it must call out those refinements explicitly.

## Success Criteria

This workflow succeeds when:

- medium and large requests are clarified before implementation
- the user approves the PRD before coding starts
- the backlog is broken into independently grabbable slices
- implementation proceeds with TDD and review loops
- the system reduces the chance of building the wrong feature
