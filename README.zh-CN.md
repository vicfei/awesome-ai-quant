# Awesome AI Quant（中文版）

> AI 工程师进量化金融的桥梁：交易 Agent、LLM 因子挖掘、市场中的决策模型、金融表格基础模型——每条标注 AI 原生视角。
>
> **English version is [here](README.md).**

[![License: CC0](https://img.shields.io/badge/license-CC0-007ec6)](#许可)

与现有清单的差异：

- [awesome-quant](https://github.com/wilsonfreitas/awesome-quant)（30k★）——通用量化资源，按传统类别组织
- [awesome-ai-in-finance](https://github.com/georgezouq/awesome-ai-in-finance)（6.7k★）——ML/DL 模型应用于金融数据
- [awesome-trading-agents](https://github.com/LLMQuant/awesome-trading-agents)（948★）——只覆盖交易 Agent

**本清单按 AI 工程师进入量化金融时遇到的任务组织**——每个板块回答"我的 AI 知识在这个领域对应什么"。

---

## 目录

- [交易 Agent](#交易-agent)——多 Agent 框架做交易决策
- [LLM 因子挖掘](#llm-因子挖掘)——用 LLM 挖 alpha
- [决策模型 × 金融](#决策模型--金融)——市场中的类型化问题
- [基础模型 × 金融](#基础模型--金融)——表格上下文学习与 K 线序列生成
- [量化平台](#量化平台)——基础设施层
- [AI 量化数据](#ai-量化数据)——兼容这些工具的数据集
- [风险与组合](#风险与组合)——优化、风险模型、仓位
- [论文](#论文)——AI × 金融交叉领域关键论文
- [保险资管](#保险资管)——买方约束的来源，量化固收的最大机构场景
- [中文生态](#中文生态)

---

## 交易 Agent

| 项目 | ★ | 做什么 | AI 工程师为什么在意 |
|---|---:|---|---|
| [TradingAgents](https://github.com/TauricResearch/TradingAgents) | 117k | 多 Agent：分析师→研究员（多空辩论）→交易员→风控。arXiv:2412.20138 | 金融决策最完整的 Agent 架构；用 Jev 筛选社交帖子 |
| [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) | 64k | AI 对冲基金团队：Graham/Buffett/Munger 投资人 Agent→基金经理综合 | 每个"投资人"是一个系统提示词 Agent——人设即策略的最干净示例；把 TypeSafe (Jev) 列为一等提供商 |
| [Vibe-Trading](https://github.com/HKUDS/Vibe-Trading) | 37k | 个人交易 Agent；FastAPI + React；影子账户（先模拟再实盘） | "安全上手"设计（先影子后真实）是每个 AI-金融产品都需要的信任模式 |

**三个项目的共同模式**：LLM Agent 提议（分析、辩论、论点），决策模型判断（是信号吗？确信度多高？），代码组合交易。

## LLM 因子挖掘

| 项目 | ★ | 做什么 | AI 工程师为什么在意 |
|---|---:|---|---|
| [RD-Agent](https://github.com/microsoft/RD-Agent)（微软） | 15k | 通用 R&D 自动化；量化场景做因子-模型协同优化。$10 成本、2× ARR | "Agent 做研究"范式——因子假设→代码→评估→迭代，全自动 |
| [QuantaAlpha](https://github.com/QuantaAlpha/QuantaAlpha) | 1.6k | LLM 驱动的自进化因子挖掘。arXiv:2602.07085 | 进化策略 + LLM 假设生成 = 不需要人类因子直觉的自动 alpha 发现 |
| [AlphaAgent](https://github.com/RndmVariableQ/AlphaAgent) | 426 | A 股多因子框架：DSL 因子表达 + FactorZoo 评估 + 可选 LLM 挖掘 | 工程化好：因子用 DSL（不是 Python）、评估管线带 IC/换手/分位报告 |

**共同洞见**：因子挖掘是搜索问题（巨大表达式空间）× 评估问题（过拟合风险）。LLM Agent 收窄搜索；纪律性评估（walk-forward、样本外）防止自欺。

## 决策模型 × 金融

| 资源 | 提供什么 |
|---|---|
| [awesome-jev-prompts](https://github.com/vicfei/awesome-jev-prompts)（60 条） | 问题模式库，含 3 条金融条目：信号-噪声筛选（Noul 门）、研报确信度评分（4 级尺）、市场状态路由（含逃逸选项的 Choice） |
| [Jev API](https://docs.typesafe.ai/) | 决策模型参考 API；按输入 Mtok 计费、输出免费 |
| [StartLux](https://github.com/StartLuxLabs/Startlux-Decision)（1.6k★） | 开源权重替代品，Jev 兼容线格式，免费 27B AutoThink 托管 |
| [Clef](https://huggingface.co/Cloudflare/clef)（Cloudflare） | Apache-2.0 开放权重；视觉 + 64k 上下文；Jev 兼容 |

**为什么这对量化重要**：金融决策是高频小判断（"这是信号吗""证据多强""什么市场状态"）——恰好是决策模型优化的形态。校准（0.7 = 十次对七次）直接映射到仓位规则。

## 基础模型 × 金融

| 模型 | ★ / 出品方 | 做什么 | 金融任务 |
|---|---|---|---|
| [Kronos](https://github.com/shiyu-coder/Kronos) | 44k, 清华（AAAI 2026） | 首个开源 K 线基础模型：OHLCV 量化为层级 token + 自回归 Transformer，45 个交易所预训练；4M–102M 开放权重 | K 线路径概率预测（多路径采样）；官方微调+回测管线基于 qlib |
| [TabPFN](https://github.com/PriorLabs/TabPFN) | 8.3k, Prior Labs | 表格基础模型开山；v3.5；CPU ≤5k 样本 | 信用评分、流失、任何小表格分类 |
| [LimiX-2](https://github.com/limix-ldm-ai/LimiX) | 4.4k, StableAI | 联合建模 p(x,y\|上下文)；因果感知 | 信用评分（BCCO 基准第一）、插补、特征因果分析 |
| [TabFM](https://github.com/google-research/tabfm) | 2.8k, Google Research | scikit-learn 兼容；混合列类型零样本 | 类似范围；JAX/PyTorch 双后端 |

**桥梁**：金融特征矩阵（因子×日期×标的）是表格数据。表格基础模型做上下文内预测免训练——小样本因子合成的 LightGBM 替代方案。但它们假设行独立，时序依赖违背核心假设。Kronos 从另一侧回答：不把时间压平成行，而是直接生成未来 K 线路径——生成式路线，官方微调管线就构建在 qlib 数据上。

## 量化平台

| 平台 | ★ | 角色 |
|---|---:|---|
| [qlib](https://github.com/microsoft/qlib)（微软） | 50k | 统治级 AI 量化平台：数据管线、模型训练、回测、RL 支持 |
| [backtrader](https://github.com/mementum/backtrader) | 24k* | Python 回测库 |
| [zipline-reloaded](https://github.com/stefan-jansen/zipline-reloaded) | 2k* | 事件驱动回测，Quantopian 血统 |

*Star 数为近似值，以链接页为准。

## AI 量化数据

| 数据集 | 平台 | 覆盖 | 格式 |
|---|---|---|---|
| [qlib_csi300](https://huggingface.co/datasets/QuantaAlpha/qlib_csi300) | HF | 沪深 300 日线 | qlib 格式 |
| [LightGBM_Alpha300](https://www.modelscope.cn/datasets/qusong0627/LightGBM_Alpha300) | ModelScope | A 股全市场（~5,500 只），2016 至今 | Parquet 按日分区 |
| [ths-quant-factor-dictionary](https://huggingface.co/datasets/obaydata/ths-quant-factor-dictionary) | HF | 同花顺因子字典（Barra 风格 + 卖方预测） | xlsx |

## 风险与组合

| 资源 | 覆盖 |
|---|---|
| [QOBLIB](https://github.com/ZIB-AOPT/QOBLIB)（59★） | 量子优化基准套件——组合优化是其十大问题类之一（注意：量子计算，非量化金融） |
| [PyPortfolioOpt](https://github.com/robertmartin8/PyPortfolioOpt) | 经典组合优化（均值-方差、Black-Litterman、风险平价） |
| [riskfolio-lib](https://github.com/dcajasn/Riskfolio-Lib) | 组合风险分析与优化 |

## 论文

| 论文 | 时间 | 关键贡献 |
|---|---|---|
| [TradingAgents](https://arxiv.org/abs/2412.20138) | 2024-12 | 金融交易的多 Agent 架构 |
| [QuantaAlpha](https://arxiv.org/abs/2602.07085) | 2026-02 | 轨迹自进化 alpha 发现 |
| [RD-Agent(Q)](https://arxiv.org/abs/2505.15155) | 2025-05 | 首个数据中心多 Agent 量化框架；$10 成本 2× ARR |
| [LimiX-2](https://arxiv.org/abs/2609.17488) | 2026-09 | 联合建模 + 因果感知；BCCO 信用评分第一 |
| [TabPFN](https://arxiv.org/abs/2504.05341) | 2025-04 (Nature) | 表格基础模型，上下文学习 |

## 保险资管

保险资管是中国固收市场最大的机构资金池（38 万亿+），也是量化工程师进入买方的天然雇主场景。它的配置是约束驱动而非预测驱动：账户结构决定负债，ALM/SAA/TAA 决定打法。完整的[学习地图](notes/insurance-asset-management.md)提炼自下面这个系列（来源：公众号"漫绘资管"，微信内打开）。

**主线阅读**——六篇，按依赖顺序：

| 文章 | 一句话内核 |
|---|---|
| [保险资管到底是什么？管的是谁的钱](https://mp.weixin.qq.com/s/fWXBEu5hbrk9_0LRWCBZCA) | 三种资金来源：系统内保险资金约七成、第三方（银行/养老金）约 18%、保险资管产品——只对机构，没有散户 |
| [国寿、平安、泰康，头部三家谁强](https://mp.weixin.qq.com/s/XEell8r8rZXMppLU0PLPBw) | 国寿强在母体、平安强在平台、泰康强在市场化（第三方 2.8 万亿，占全行业业外资金约四成） |
| [怎么赚钱？和公募不是一个生意](https://mp.weixin.qq.com/s/WTdzFTqT1EpoXLFCIcNR5A) | 38 万亿盘子平均费率 9.68bp、净利率约 45%、前三家拿走全行业 58% 净利——赚规模的钱，不是费率的钱 |
| [账户内部构成：传统、分红、万能](https://mp.weixin.qq.com/s/wQ4PPc1CKcO3RHBflSUGig) | 预定利率 2.0%/1.75%/1.0% 决定负债刚性：传统 > 分红 > 万能，刚性决定每个池子能买什么（高股息进 OCI 的逻辑） |
| [SAA 和 TAA](https://mp.weixin.qq.com/s/usYoK_EUT7MCPe-HfdniMw) | 配置起点是负债不是市场；SAA 在偿付能力/久期/覆盖率约束下定锚，TAA 在带内微调 |
| [为什么险资天然爱买长债（ALM）](https://mp.weixin.qq.com/s/RaDsV095pRIxPlGWUqEEfw) | 负债久期 13–16 年 vs 资产约 5.6 年；久期缺口 ±5 年新规下，超长债是结构性需求而非观点 |

**产品、运营与 AI**：

| 文章 | 一句话内核 |
|---|---|
| [一文看懂什么是保险资管产品](https://mp.weixin.qq.com/s/PmWvrb9W8dRTURl8Qp9Nlg) | 债权/股权投资计划与组合类产品：私募信托结构、全生命周期六环节及每环节背后的系统 |
| [漫绘资管业务-保险资管产品](https://mp.weixin.qq.com/s/nF-mQgLaD17mDpASECNUrw) | 上文的图解版（漫画形式走一遍业务流程） |
| [一文看懂资产管理公司业务体系](https://mp.weixin.qq.com/s/5FPwtSgTlkzG_F6bK-D68g) | 通用资管价值链：募集→投资→投后→退出，前中后台分工全图 |
| [一文看懂资产管理公司技术体系](https://mp.weixin.qq.com/s/GPWIvh_gxPEEplsPdAYcRQ) | 投研/交易/风控/估值系统栈与供应商版图——工程师入职资管公司第一天见到的东西 |
| [大资管运营智能化转型之路](https://mp.weixin.qq.com/s/0bgCTKQbNhUXNs78nwIdMw) | 从流程自动化到认知自动化：SOP 拆成原子 Skill，Agent 成为新的编排层 |
| [当资管运营遇见 Claude Code](https://mp.weixin.qq.com/s/tkkYtntrVa28P1vkb97D-w) | 六个 agent 实战场景（报告比对 2 天→10 秒、表单自动化、PPT/爬虫/技能工厂）——AI 工程师切入这个行业最直接的角度 |

## 中文生态

| 资源 | ★ | 说明 |
|---|---|---|
| [thuquant/awesome-quant](https://github.com/thuquant/awesome-quant) | 5.7k | 中国的 Quant 相关资源索引 |
| [QuantaAlpha](https://github.com/QuantaAlpha/QuantaAlpha) | 1.6k | 中文优先的 LLM 因子挖掘框架 |
| Vibe-Trading 飞书/微信群 | — | 见 [Vibe-Trading 仓库](https://github.com/HKUDS/Vibe-Trading) |

---

## 贡献

PR 欢迎。每条需要：做什么（一行）+ AI 工程师为什么在意（一行）。链接必须可访问（CI 跑链接检查）。

## 许可

[CC0 1.0](LICENSE) — 公共领域。

**免责声明**：教育资源，非投资建议。过往表现不代表未来。
