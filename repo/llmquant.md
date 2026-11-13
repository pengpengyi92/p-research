# LLMQuant community and repository guide

**Inventory checked:** `2026-11-14T04:48:30+08:00` (Asia/Shanghai).

[LLMQuant](https://github.com/LLMQuant) is an independent community working at the intersection of AI, large language models, and quantitative finance. Its public projects cover quant education, financial data access, knowledge extraction, and agent workflows. See the [official site](https://www.llmquant.com/) for the community sign-up and the [GitHub profile](https://github.com/LLMQuant/.github/blob/main/profile/README.md) for its project map and contribution entry points.

## Start here

Start with **quant-mind** to frame an extraction or retrieval experiment, **llmquant-book** for notebook examples, and **awesome-trading-agents** to map related systems. Compare a small, pinned workflow with a simple baseline on a fixed public or synthetic fixture, and report errors and negative results as well as successes.

## Public repositories

All nine directly accessible public repositories under the `LLMQuant` GitHub organization at the check above, including its profile repository. The scope comes from the [organization listing](https://github.com/orgs/LLMQuant/repositories) and [paginated GitHub REST inventory](https://api.github.com/orgs/LLMQuant/repos?type=public&per_page=100), cross-checked with GitHub GraphQL and direct access checks for discrepancies. Linked websites and members’ personal repositories are outside this inventory.

| Repository | What to look at | GitHub license signal |
| --- | --- | --- |
| [`quant-wiki`](https://github.com/LLMQuant/quant-wiki) | Bilingual quantitative-finance wiki; a starting point for domain terminology and common methods. | Not detected |
| [`docs`](https://github.com/LLMQuant/docs) | Finance Context documentation for financial concepts and AI workflows. | Not detected |
| [`llmquant-book`](https://github.com/LLMQuant/llmquant-book) | LLMQuant book project with Jupyter notebooks for hands-on reading. | `NOASSERTION` |
| [`data-mcp`](https://github.com/LLMQuant/data-mcp) | MCP server for LLMQuant Data; an example of exposing financial data tools to agents. | MIT |
| [`quant-mind`](https://github.com/LLMQuant/quant-mind) | Agent-oriented framework for extracting and retrieving structured financial knowledge. | MIT |
| [`skills`](https://github.com/LLMQuant/skills) | Reusable agent instructions and workflows built around LLMQuant Data. | MIT |
| [`llmquant-hermes`](https://github.com/LLMQuant/llmquant-hermes) | Hermes integration for financial research and recurring monitoring tasks. | MIT |
| [`awesome-trading-agents`](https://github.com/LLMQuant/awesome-trading-agents) | Directory of trading agents, MCP servers, and agent skills; listing does not validate any tool. | CC0-1.0 |
| [`.github`](https://github.com/LLMQuant/.github) | Organization profile, project map, and community entry points. | Not detected |

GitHub's license signal is not a rights determination. Check upstream terms for the specific code, data, and other material before reuse. No upstream files are mirrored here, and the projects were not installed, executed, or benchmarked for this catalog.

### Access notes

- `LLMQuant/asset` is listed in the public REST inventory, but the repository endpoint and page return HTTP 451. It is recorded for completeness, not offered as an accessible resource.
- `LLMQuant/Magents` appears in older indexes, but its GitHub endpoint returned HTTP 404 and it is not in the current public inventory. No assumption is made about whether it moved or became private.

## Discuss and contribute

- Use [P-Research Repo Discussions](https://github.com/pengpengyi92/p-research/discussions/categories/repo) to share a finding or correct the catalog. Include the upstream URL, pinned commit or release when relevant, what you checked, and any limitations.
- For fixes to an upstream project, follow the contribution guidance in that LLMQuant repository. Use the community sign-up on the official site if you want to join LLMQuant itself.
- For this index, a focused PR with a primary source and date is welcome. Do not share credentials, private strategy information, or data you cannot redistribute.
