# Expect-the-Unexpected-Bioinformatics-AI-Agent-Skills

_When running bioinformatics tools, one just has to expect the unexpected sometimes. Hopefully these AI agent skills could help!_

Last Updated: 2026-11-16

AI agents have potentials to improve bioinformatics analysis. Below is how I think they can be useful, based on my years of experience running bioinformatics pipelines. 

![Logo for the repo](/assets/images/logo.png)

**Note**: Many of my skills expect `web_search` or `web_extract` dependencies in the agent of choice. It would not work if your agent is working in a closed system. It also may be a good idea to try these skills with a cost-effective AI model first.

**Note**: The effect of `SKILL.md` depends a lot on the underlying model. The list below is meant to serve as a starting point to understanding the kind of issues that bioinformaticians encounter.

## Table of Contents

- [**List of Skills**](#list-of-skills)
- [**Skill Installation to Your AI Agent**](#skill-installation-to-your-ai-agent)
- [**Examples**](#examples)
- [**Environment Dependencies**](#environment-dependencies)

## List of Skills

||Skill|Description|Use Case|Main|Hermes Default|Dependent On`*`|
|--------|--------|--------|--------|--------|--------|--------|
|1|cli-version-diff|Diff CLI parsers and output specs from tagged source code.|You are focused on the code. You find an old script that uses a bioinformatics tool that has a github repository. By how much is the latest version different from the version used on the old script? |:white_check_mark:|||

`*` Also install this other skill because without it the skill may not work as the repository manager expected.

## Skill Installation to Your AI Agent

In case you have not used an AI agent before, think of it as a _harness_ that allows large language models to behave more consistently. It essentially allows you to use large-language models with a conversational user interface, just like you would with **ChatGPT**. As an agent with the core of a large language model, it will have access to internet and local files in your computer system, so be wary. As for the _core_, you can use [local large language models](https://ollama.com/search?c=local) if you have GPUs; if not, you can use [API-based large language models](https://openrouter.ai/discover) and pay per token. Choose the model that makes sense for your situation.

My current favorite AI agent is [**Hermes AI Agent by Nous Research**](https://hermes-agent.nousresearch.com). These days, I alternate between `z-ai/glm-5.3-flash` via OpenRouter and `gemma4:31b` locally using Ollama. Below is how you would install the skill for Hermes. However, you could simply download the `<skill-name>/SKILL.md` file, and put it in the format that your own favorite AI Agent expects. 

```
bash
1. Add the repo as a skill tap
hermes skills tap add hannahkimincompbio/Expect-the-Unexpected-Bioinformatics-AI-Agent-Skills

2. List available skills in that tap
hermes skills list --tap hannahkimincompbio/Expect-the-Unexpected-Bioinformatics-AI-Agent-Skills

3. Install a specific skill by name
hermes skills install hannahkimincompbio/Expect-the-Unexpected-Bioinformatics-AI-Agent-Skills/<skill-name>
```



## Examples

- [`examples/cli-version-diff-hyphy-v2.5.93-vs-v2.5.103.example.md`](examples/cli-version-diff-hyphy-v2.5.93-vs-v2.5.103.example.md) — worked output of cli-version-diff on [veg/hyphy](https://github.com/veg/hyphy), HyPhy v2.5.93 vs HyPhy v2.5.103
- [`examples/cli-version-diff-hyphy-v2.5.93-vs-hyphy3-vv0.0.1.example.md`](examples/cli-version-diff-hyphy-v2.5.93-vs-hyphy3-vv0.0.1.example.md) — worked output of cli-version-diff on [veg/hyphy](https://github.com/veg/hyphy), Hyphy v2.5.93 vs Hyphy3 v0.0.1

## Environment Dependencies

The skills' bundled scripts use only the Python 3 standard library (no pip installs). Beyond Python 3, the skills assume:
- `git` and `curl` — cli-version-diff fetches tagged sources via `git`/`raw.githubusercontent.com` and diffs tags.
