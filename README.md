# Awesome AI Quant

> The bridge from AI engineering to quantitative finance: trading agents, factor mining with LLMs, decision models in markets, tabular foundation models for finance — each entry annotated with the AI-native perspective, not just a link dump.
>
> **AI 工程师进量化金融的桥梁**：交易 Agent、LLM 因子挖掘、市场中的决策模型、金融表格基础模型——每条标注 AI 原生视角，不只是链接搬运。

[![License: CC0](https://img.shields.io/badge/license-CC0-007ec6)](#license)

**中文版在[这里](README.zh-CN.md)（含全部中文注释）。**

Different from existing lists:

- [awesome-quant](https://github.com/wilsonfreitas/awesome-quant) (30k★) — general quant resources, organized by traditional categories (data, backtesting, ML)
- [awesome-ai-in-finance](https://github.com/georgezouq/awesome-ai-in-finance) (6.7k★) — ML/DL models applied to financial data
- [awesome-trading-agents](https://github.com/LLMQuant/awesome-trading-agents) (948★) — specifically about trading agents

**This list is organized by the tasks an AI engineer encounters when entering quant finance** — and each section answers "what does my AI knowledge map to in this domain?"

---

## Contents

- [Trading Agents](#trading-agents) — multi-agent frameworks that trade
- [Factor Discovery with AI](#factor-discovery-with-ai) — LLM-driven alpha mining
- [Decision Models × Finance](#decision-models--finance) — typed questions in markets
- [Tabular Foundation Models × Finance](#tabular-foundation-models--finance) — ICL for tabular financial data
- [Quant Platforms](#quant-platforms) — the infrastructure layer
- [Data for AI Quant](#data-for-ai-quant) — datasets that work with these tools
- [Risk & Portfolio](#risk--portfolio) — optimization, risk models, position sizing
- [Papers](#papers) — key papers at the AI × finance intersection
- [Chinese Ecosystem](#chinese-ecosystem) — 中文资源

---

## Trading Agents

Multi-agent LLM frameworks that analyze markets, debate, and make trading decisions.

| Project | ★ | What it does | Why AI engineers care |
|---|---:|---|---|
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | 117k | Multi-agent: analysts → researchers (bull/bear debate) → traders → risk managers. arXiv:2412.20138 | The most complete agent-architecture for financial decisions; uses Jev for social-post screening |
| [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) | 64k | AI hedge fund team: Graham/Buffett/Munger investor agents → fund manager synthesis | Each "investor" is a system-prompt agent — cleanest example of persona-as-strategy; lists TypeSafe (Jev) as a first-class provider |
| [Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | 37k | Personal trading agent; FastAPI + React; Shadow Account (paper trading first) | The "safe onboarding" design (shadow before real) is the trust pattern every AI-finance product needs |

**The pattern across all three**: LLM agents propose (analysis, debate, thesis), decision models judge (is this signal? what conviction level?), code composes the trade. This maps directly to the [decision-model contract](https://github.com/vicfei/awesome-jev-prompts) (model proposes, Jev answers, code decides).

## Factor Discovery with AI

LLM agents that mine, evolve, and validate alpha factors.

| Project | ★ | What it does | Why AI engineers care |
|---|---:|---|---|
| [RD-Agent](https://github.com/microsoft/RD-Agent) (Microsoft) | 15k | General R&D automation; quant scenario (RD-Agent-Q) does factor-model co-optimization. $10 cost, 2× ARR vs benchmark factor libraries | The "agent that does research" paradigm — factor hypothesis → code → evaluate → iterate, all autonomous |
| [QuantaAlpha](https://github.com/QuantaAlpha/QuantaAlpha) | 1.6k | LLM-driven self-evolving factor mining via trajectory evolution. arXiv:2602.07085 | Evolutionary strategies + LLM hypothesis generation = automated alpha discovery without human factor intuition |
| [AlphaAgent](https://github.com/RndmVariableQ/AlphaAgent) | 426 | A-share multi-factor framework: DSL factor expressions + FactorZoo evaluation + optional LLM mining | Clean engineering: factors as DSL (not Python), evaluation pipeline with IC/turnover/quantile reports |

**The shared insight**: factor mining is a search problem (huge expression space) × evaluation problem (overfitting risk). LLM agents narrow the search; disciplined evaluation (walk-forward, out-of-sample) prevents self-deception. Same as hyperparameter search in ML, but the search space is financial logic.

## Decision Models × Finance

Typed questions (Choice/Score/Noul) applied to financial judgments — the question-design layer that trading agents need but haven't systematized.

| Resource | What it provides |
|---|---|
| [awesome-jev-prompts](https://github.com/vicfei/awesome-jev-prompts) (60 entries) | Question patterns including 3 financial entries: signal-vs-noise screening (Noul gate), research conviction scoring (4-level rubric), market regime routing (Choice with escape option) |
| [Jev API](https://docs.typesafe.ai/) | The reference decision-model API; per-Mtok input pricing with free output |
| [StartLux](https://github.com/StartLuxLabs/Startlux-Decision) (1.6k★) | Open-weight alternative, Jev-compatible wire format, free 27B AutoThink hosting |
| [Clef](https://huggingface.co/Cloudflare/clef) (Cloudflare) | Apache-2.0 open weights; vision + 64k context; Jev-compatible |

**Why this matters for quant**: financial decisions are high-frequency small judgments ("is this signal?", "how strong is the evidence?", "what regime?") — exactly the shape decision models optimize for. Calibration (0.7 = 7 out of 10 correct) maps directly to position sizing.

## Tabular Foundation Models × Finance

Foundation models that do in-context learning on tabular data — no training, just read your table and predict.

| Model | ★ / org | What it does | Financial tasks |
|---|---|---|---|
| [TabPFN](https://github.com/PriorLabs/TabPFN) | 8.3k, Prior Labs | Original tabular FM; v3.5 with row-wise + cross-row attention; CPU ≤5k samples | Credit scoring, churn, any small-tabular classification |
| [LimiX-2](https://github.com/limix-ldm-ai/LimiX) | 4.4k, StableAI | Joint modeling p(x,y\|context); causal awareness (feature attention recovers causal skeleton) | Credit scoring (BCCO benchmark #1), imputation, feature causal analysis |
| [TabFM](https://github.com/google-research/tabfm) | 2.8k, Google Research | scikit-learn compatible; zero-shot cls/reg on mixed column types | Similar range; dual JAX/PyTorch backend |

**The bridge**: financial feature matrices (factors × dates × tickers) are tabular data. Tabular FMs do in-context prediction without training — an alternative to LightGBM for small-sample factor synthesis. But they assume iid rows, so time-series dependence violates the core assumption (see [structured-state patterns](https://github.com/vicfei/awesome-jev-prompts/blob/main/categories/structured-state-patterns.md) for when to route to which paradigm).

## Quant Platforms

The infrastructure layer every AI-quant project builds on.

| Platform | ★ | Role |
|---|---:|---|
| [qlib](https://github.com/microsoft/qlib) (Microsoft) | 50k | The dominant AI-quant platform: data pipeline, model training, backtesting, RL support |
| [backtrader](https://github.com/mementum/backtrader) | 24k* | Python backtesting library |
| [zipline-reloaded](https://github.com/stefan-jansen/zipline-reloaded) | 2k* | Event-driven backtesting, Quantopian heritage |
| [DisconfirmAI](https://disconfirmai.com/en) | — | Investment research platform: find disconfirming evidence before conviction; reading, filings research, change radar, frameworks |

*Star counts approximate; check links for current.

## Data for AI Quant

| Dataset | Platform | Coverage | Format |
|---|---|---|---|
| [qlib_csi300](https://huggingface.co/datasets/QuantaAlpha/qlib_csi300) | HF | CSI 300 daily bars | qlib format |
| [LightGBM_Alpha300](https://www.modelscope.cn/datasets/qusong0627/LightGBM_Alpha300) | ModelScope | Full A-share (~5,500 tickers), 2016–now, 3 adjustment modes + fundamentals | Parquet by date |
| [ths-quant-factor-dictionary](https://huggingface.co/datasets/obaydata/ths-quant-factor-dictionary) | HF | THS (同花顺) factor dictionaries: Barra-style + sell-side forecasts | xlsx |

## Risk & Portfolio

| Resource | What it covers |
|---|---|
| [QOBLIB](https://github.com/ZIB-AOPT/QOBLIB) (59★) | Quantum optimization benchmark suite — portfolio optimization is one of ten problem classes (note: quantum computing, not quant finance) |
| [PyPortfolioOpt](https://github.com/robertmartin8/PyPortfolioOpt) | Classical portfolio optimization (mean-variance, Black-Litterman, risk parity) |
| [riskfolio-lib](https://github.com/dcajasn/Riskfolio-Lib) | Portfolio risk analysis and optimization |

## Papers

| Paper | Date | Key contribution |
|---|---|---|
| [TradingAgents: Multi-Agents LLM Financial Trading Framework](https://arxiv.org/abs/2412.20138) | 2024-12 | Multi-agent architecture for trading (analysts/researchers/traders/risk) |
| [QuantaAlpha: LLM-driven self-evolving factor mining](https://arxiv.org/abs/2602.07085) | 2026-02 | Trajectory-based self-evolution for alpha discovery |
| [RD-Agent(Q): Automated factor-model co-optimization](https://arxiv.org/abs/2505.15155) | 2025-05 | First data-centric multi-agent framework for quant; $10 cost 2× ARR |
| [LimiX-2: Structured-data foundation model with causal awareness](https://arxiv.org/abs/2609.17488) | 2026-09 | Joint modeling p(x,y\|context); BCCO credit-scoring #1 |
| [TabPFN: Accurate predictions on small data](https://arxiv.org/abs/2504.05341) | 2025-04 (Nature) | Tabular foundation model, in-context learning |

## Chinese Ecosystem

| Resource | ★ | Description |
|---|---|---|
| [thuquant/awesome-quant](https://github.com/thuquant/awesome-quant) | 5.7k | 中国的 Quant 相关资源索引（中文） |
| [QuantaAlpha](https://github.com/QuantaAlpha/QuantaAlpha) | 1.6k | 中文优先的 LLM 因子挖掘框架 |
| Vibe-Trading 飞书/微信群 | — | 见 [Vibe-Trading repo](https://github.com/HKUDS/Vibe-Trading) |

---

## Contributing

PRs welcome. Each entry needs: what it does (one line) + why AI engineers should care (one line). Links must be verified (CI runs a link check). See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[CC0 1.0](LICENSE) — dedicated to the public domain.

**Disclaimer:** educational resource; not investment advice. Past performance does not indicate future results.
