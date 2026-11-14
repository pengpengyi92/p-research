# QuantAgent (2024 paper)

**QuantAgent: Seeking Holy Grail in Trading by Self-Improving Large Language Model**

Saizhuo Wang, Hang Yuan, Lionel M. Ni and Jian Guo.
[arXiv:2402.03755v1](https://arxiv.org/abs/2402.03755v1), 2024-02-06;
[full text](https://arxiv.org/html/2402.03755v1).
Reviewed 2026-11-15 (Asia/Shanghai). Preprint; no conference acceptance
established in this review.

## Reading observation

An inner loop refines responses using knowledge; an outer loop tests them and
updates knowledge. The efficiency argument depends on its stated theoretical
assumptions, not a general guarantee of trading profitability.

## Our assessment and next question

For us, memory should be an evidence ledger, not an accumulation of confident
stories. A rejected hypothesis needs a durable reason, dataset identity and
scope. Otherwise the next iteration can repeat the mistake under a new name.

Our proposed comparison freezes memory before the final audit and tests
fixed-prompt, inner-feedback and inner-plus-external-feedback arms at the same
resource budget. A mutation that writes held-out labels into memory must fail
the isolation check. Protocol **NOT RUN**; economic validity is not established.

This card refers only to the paper above. Same-name repositories or later
trading-agent projects are not assumed to be the authors' code. No matching
version-pinned implementation was established from the primary links inspected.
[Provenance](PROVENANCE.md) / [our reflection](../../report/2026-11-15-alpha-gpt-pengyi166/README.md).
