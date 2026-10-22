# Meeba Brain

**Know what your code change really breaks, with evidence.**

Meeba Brain is an evidence-first code intelligence layer for teams using AI coding tools. It traces impact and root causes across large codebases, cites the exact code behind every claim, and marks what it couldn't verify. It works in the web app and inside Cursor and Claude Code via MCP.

This repository holds public, checkable examples of Meeba Brain on real open-source code: the question, the answer, the exact lines behind it, and where the answer fell short.

- Try it: [meeba.ai/brain](https://meeba.ai/brain) (free to start, read-only GitHub access)
- Discuss a case or send a counterexample: [Discussions](https://github.com/meemoprasad/meeba-brain/discussions)

## Case studies

| Case | Question | What to check |
|---|---|---|
| [Composio Python SDK: unresolved annotation error](demos/composio-5022-annotation-resolution.md) | What does the proposed fix for issue [#5022](https://github.com/ComposioHQ/composio/issues/5022) ([PR #5024](https://github.com/ComposioHQ/composio/pull/5024)) really change? | Behaviour changes, the tests that cover them, one caller of the changed private function, and one test the answer named wrongly |

Each case study is an independent analysis. It is not an endorsement by the project's maintainers, and it says whether the change was merged.

## Where Meeba Brain fits

| If your team uses | They're good at | Meeba Brain adds |
|---|---|---|
| AI coding agents (Cursor, Claude Code, Copilot, Codex) | Writing and editing code | Evidence for every claim, in the same editor through MCP |
| AI code review (CodeRabbit, Greptile, Qodo) | Comments on the pull request | What the change affects outside its diff |
| Code search (Sourcegraph, DeepWiki) | Finding where code lives | Whether a claim about that code is true, with the lines that show it |
| Production RCA (Sentry Seer, observability AI) | Finding the incident in logs and traces | The code path behind the error, and what else a fix will touch |

## How to judge an answer

Use this on our case studies, and on any AI answer about code:

1. Are the cited files and lines real, and do they say what the answer claims?
2. Is a claim marked verified only when the code or a run shows it?
3. Does the answer say what it did not check?
4. Can the behaviour be reproduced, and is the fix covered by a test?

## What to expect today

- On a large repository an answer usually takes 1 to 2 minutes, because it reads the code before answering.
- It can still be wrong. That's why every claim links to the exact lines, so you can check it in one click.
- It asks for read-only GitHub access. We don't have SOC 2 yet, so many teams start on a public or non-sensitive repository.

## Contributing a case

Open a discussion with: the repository and commit, the question you asked, the answer, the lines you checked, and what was right or wrong. Counterexamples are as welcome as good results. Please don't post credentials, private code, personal data or production logs.

---

Built by [Meeba AI](https://meeba.ai) (Inteligrator Technologies Pvt. Ltd., Raipur, India).
