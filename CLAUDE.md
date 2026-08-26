# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal 12-week system-design study curriculum, written entirely as Markdown content — there is no application code, build system, linter, or test suite. "Work" here means writing/editing lesson content, not running commands.

`ROADMAP.md` defines the full 12-week curriculum (topics + deliverables per day). Only Week 1 has been expanded so far, in `week-01-foundations/`. Future weeks should be added as `week-0N-<topic>/` directories following the same pattern once requested.

## Structure

- `README.md` — entry point; states what's built (Week 1 only) vs. planned.
- `ROADMAP.md` — the cumulative 12-week plan; each week builds on the previous one's mental model.
- `PROGRESS.md` — checkbox tracker per week/day; update checkboxes as days are completed, don't restructure it.
- `BOOK-READING-PLAN.md` — maps roadmap topics to specific chapters in the reference books (DDIA 2nd ed., Computer Networking: A Top-Down Approach 9th ed., Google SRE + Workbook, System Design Interview Vol. 1/2).
- `REVIEW-NOTES.md` — the editorial standard (see below) derived from a v1→v2 revision of Week 1. Treat this as the authoritative spec for how any week's content should be structured.
- `week-01-foundations/` — the expanded week: `README.md` (index), `day-0N-*.md` lessons, `cheat-sheet.md`, `resources.md`, `answer-key.md`.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `LICENSE` (MIT) — standard repo metadata.

## Editorial standard for lesson content

Every day-lesson file must contain, in order (per `REVIEW-NOTES.md`):

1. Goal
2. Mental model
3. Core explanation
4. Concrete example
5. Architecture diagram (Mermaid)
6. Tradeoff
7. Failure mode
8. Practical exercise
9. Retrieval questions
10. Exit criterion
11. Primary sources
12. Deep-dive reading

Every design-lab file must additionally contain: requirements, scale assumptions, SLOs, rough estimation (back-of-envelope), baseline architecture, bottleneck analysis, scaling path, failure matrix, observability, cost, tradeoffs, and a review rubric.

Design labs need measurable targets, not just discussion questions: SLOs, p50/p95/p99 figures, capacity estimates, observability metrics, load-test design, cost, and a scoring rubric.

## Content rules

- Don't teach beyond a week's stated scope. `REVIEW-NOTES.md` lists topics deliberately deferred out of Week 1 (crypto, BGP, DNSSEC, TCP congestion-control internals, Kubernetes, Kafka, DB internals, multi-region consensus) — adding them early increases vocabulary faster than understanding. Apply the same discipline to later weeks: stick to what that week's roadmap row promises.
- Cite verifiable primary sources (RFCs, official docs, production engineering writeups) per lesson, not just secondary explainers.
- `answer-key.md` files are meant to be opened only after the learner completes the corresponding review quiz — don't casually surface their contents when the learner is still mid-week.
- Keep `PROGRESS.md` checkboxes in sync with actual completion; don't mark days done speculatively.
- Never copy a book's worked-example diagram verbatim into a design lab — the reading plan's method is: hide the solution, design it yourself, compare, and write down which differences were requirement-driven.
- Keep `README.md`'s title and "Status" line accurate as more weeks get built out.
