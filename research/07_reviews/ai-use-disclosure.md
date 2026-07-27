## Use of AI Assistance

Kimi Agent, a commercial large-language-model assistant operated by Moonshot AI, was used to execute parts of the empirical work reported in this paper. The experiments in \S4.9--4.12 were carried out by Kimi under the author's direction, with the generated records, logs, and code artifacts archived in the reproducibility package.

Kimi executed four experimental batches: (a) the Stage B v5.4 protocol replication on Qwen/Qwen3-8B, with controlled state-mutation perturbations (five conditions \(\times\) eight repetitions = 40 runs); (b) the multi-model interchangeability sweep across five models (Qwen3-8B, GLM-4-9B, Qwen3-14B, DeepSeek-V3.2, Qwen2.5-7B), 40 runs each; (c) the cross-framework comparison between the petfishframework and LangChain execution pipelines on the same Stage B v5.4 protocol; and (d) the floor-model probe suite, comprising eight probe conditions across the same five models. For each batch Kimi ran the protocol, collected raw model outputs, applied the deterministic evaluator, and produced the pass-rate and Wilson-interval summaries reported here.

Kimi did not author this paper, did not design the original contract or the harness methodology, and did not select the evaluation criteria, thresholds, or claim boundaries on its own. Those decisions were made by the human author and recorded in the preregistered protocol documents.

The author verification of Kimi's outputs is **TO BE CONFIRMED**. The author will re-run the published Stage B v5.4 protocol as a sanity check before submission. Until that confirmation is complete, all \S4.9--4.12 results are labeled as **automated replication by an LLM agent (Kimi Agent)** and are not described as a separate, third-party, or author-confirmed replication.

Kimi is itself a large language model. It may therefore share failure modes with the models under test, or it may interpret the contract in ways that flatter the protocol rather than stress it. Using an LLM agent to run an LLM-evaluation pipeline is a form of circular instrumentation: the executor and the evaluated system belong to the same model class. The replication should therefore be treated as an automated execution trace subject to the same validity threats as any LLM-mediated measurement, and it should be confirmed by the author's own runs.

A resource-level conflict of interest also exists. The author provided a personal SiliconFlow API key for all Kimi-executed runs; the compute was paid for by the author. The automation was operational---Kimi followed the published protocol---but it was not resource-neutral.

This disclosure is provided in line with the AI assistance and reproducibility policies of ACL, EMNLP, AAAI, and NeurIPS, which require authors to report when generative AI or LLM-based tools were used in research execution, analysis, or writing.
