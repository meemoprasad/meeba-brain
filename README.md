# Meeba Brain — Evidence for Code Changes

**Know what your AI-generated code changes affect.**

AI coding agents can write code quickly. Understanding the consequences of those changes—and verifying debugging claims—takes evidence.

Meeba Brain helps developers investigate code changes and connect findings to concrete source-code locations.

> Don't just give an answer. Show the evidence behind it.

## What we're exploring

- **Code-change impact:** Investigate which files, callers, and behaviors may be affected by a change.
- **Evidence-linked debugging:** Connect findings to relevant file-and-line references.
- **AI-generated code verification:** Check claims against available source code instead of treating plausible output as proof.
- **Real engineering cases:** Document reproduction steps, supporting evidence, test results, and limitations.

## Try Meeba Brain

Explore the product: https://meeba.ai/brain

Bring a concrete debugging or code-change question. Check whether the answer identifies relevant source locations, distinguishes verified facts from hypotheses, and gives you enough evidence to validate the conclusion.

## Demos and experiments

We will publish reproducible engineering examples covering:

1. **Code-change impact:** What could be affected by a particular change?
2. **Evidence-linked debugging:** Can a suspected bug be traced to relevant code?
3. **Production-log-assisted debugging:** Can available GCP logs help investigate a failure?

Each published case should document its inputs, setup, evidence, findings, verification, and limitations. Results will be added when the demonstrations are ready and verified.

## Open-source contributions

This project also documents relevant engineering problems investigated in public repositories.

- **Issues:** Links to actual upstream bug reports and reproductions.
- **Pull requests:** Links to actual code changes and their current review status.
- **Evaluation cases:** Minimal examples that developers can inspect and reproduce.

Upstream issues and pull requests remain in their original repositories. Their maintainers independently determine whether changes are accepted or merged.

## How to evaluate an answer

Ask these questions:

- Are the cited files and lines real and relevant?
- Can the claimed behavior be reproduced?
- Does the answer separate verified facts from hypotheses and unknowns?
- Does it acknowledge missing context instead of inventing details?
- Is the proposed fix validated by a test or observable result?

Counterexamples and incorrect findings are welcome. They help expose where evidence is incomplete or conclusions need improvement.

## Share an engineering case

Open an issue in this repository: https://github.com/meemoprasad/meeba-brain/issues

Include a clear problem statement, reproduction steps, expected and actual behavior, relevant source locations, and verification details.

Never publish credentials, access tokens, private source code, personal data, or sensitive production logs.

## Project status

This repository is an evolving collection of engineering demonstrations and evaluation cases. It is not a claim of universal accuracy. Each published example should document its test conditions and limitations.

## About

Built by [Inteligrator Technologies](https://inteligrator.tech).

- **Product:** [Meeba Brain](https://meeba.ai/brain)
- **Source of examples:** Public engineering problems, reproducible cases, and documented experiments.

---

**Working principle:** A debugging conclusion is more useful when developers can inspect the evidence and verify it themselves.
