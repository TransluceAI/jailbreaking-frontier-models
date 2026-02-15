# Jailbreak Dashboard - February 2026

## Executive Summary

This dashboard provides evidence-backed analysis of jailbreak attack trends, defense mechanisms, and evaluation methodologies for frontier language models as of February 2026. All quantitative claims are supported by standardized benchmarking studies and peer-reviewed research.

**Key Finding**: No single-layer defense suffices against the evolving landscape of jailbreak attacks. Multi-layered defenses combining system prompts, safety fine-tuning, and adversarial training are essential, with continuous evaluation required to maintain robustness.

---

## Key Validated Attack Trends

### 1. Many-shot and Long-context Attacks

**Impact**: Large context windows materially increase jailbreak success rates.

**Evidence**:
- Standardized benchmarking shows high Attack Success Rate (ASR) in long-context settings
- TAP on AdvBench reports ASR ≈ 0.88 in summarized survey tables
- Robustness does not monotonically increase with model size
- Fine-tuning and safe system prompts shift ASR but do not eliminate risk

**Quantitative Scope**:
- ~354 experiments conducted
- ~55,000 GPU hours invested in evaluation
- Performance highly model- and context-size dependent

**Citations**: (1.1, 2.1, 2.2)

---

### 2. Few-shot and Adaptive Variants

**Impact**: Improved few-shot approaches achieve very high success rates on some open models.

**Evidence**:
- Optimized few-shot approaches can reach >80-95% ASR on some open models
- Performance depends on demonstration design and special token usage
- Benchmarks corroborate strong performance under certain settings

**Key Insight**: Carefully engineered few-shot demonstrations and special tokens can circumvent defenses without requiring large context windows.

**Citations**: (2.1, 2.2)

---

### 3. Optimization-based Attacks (GCG Family)

**Impact**: Significant improvements in both success rates and efficiency.

**Variants**: I-GCG, Faster-GCG, MAGIC, AmpleGCG

**Evidence**:
- Near-100% ASR achieved on some open models
- Faster-GCG: ~10x compute reduction compared to original GCG
- MAGIC: ~1.5x speedup
- Transfer effectiveness varies by target model

**Key Insight**: Token-optimization attacks are highly effective on vulnerable models, but transfer and per-model success vary substantially. Recent variants demonstrate both improved success rates and computational efficiency.

**Citations**: (2.1, 2.2)

---

### 4. Simple Adaptive Attacks on Leading Models

**Impact**: Manual adaptive approaches can achieve perfect success rates against safety-aligned models.

**Evidence**:
- Manual adaptive templates + random-search over suffix tokens achieve **100% ASR** on a 50-item AdvBench suite
- Successful across many leading safety-aligned LLMs
- Effective via transfer/prefill on non-logprob APIs
- Adaptivity to model/API is crucial for success

**Key Insight**: Simple, model-adaptive methods using logprobs or tailored templates can break top models when properly adapted to the specific target.

**Citations**: (3.1)

---

### 5. Black-box Iterative Attacks (PAIR)

**Impact**: Semantic attacker-LM refinement yields competitive ASR with low query budgets.

**Evidence**:
- Cross-model evaluations report PAIR ASR ranging from 0.14 to 0.61 on prominent black-box models
- Low query budgets demonstrated (<20 queries in original results)
- Effectiveness varies substantially by target model

**Key Insight**: Prompt Automatic Iterative Refinement leverages semantic refinement rather than token-level optimization, achieving competitive results with minimal queries.

**Citations**: (4.1)

---

### 6. VLM/MLLM Jailbreaks

#### Typography-based Visual Prompts

**Impact**: Converting harmful text into images bypasses text-only alignment.

**Evidence**:
- Typography attacks reach average ASR ≈ 80-83% in reported studies
- OCR-encoded prompts exploit visual embedding alignment weaknesses
- Successful against both open-source and commercial Large Vision-Language Models (LVLMs)

**Key Insight**: Visual embedding alignment is a weak link; OCR gaps enable bypass of text-only safety measures.

**Citations**: (1.1, 5.1)

#### Bi-modal Attacks (BAP)

**Impact**: Joint optimization of visual and textual components substantially increases effectiveness.

**Evidence**:
- BAP (Bi-modal Adversarial Prompt): **+29.03% mean ASR improvement** vs. baselines
- Successful white-box and black-box compromise of commercial LVLMs
- Demonstrates cross-modal alignment weaknesses

**Key Insight**: Jointly optimizing visual perturbation with refined textual prompts creates highly effective and transferable attacks.

**Citations**: (5.1)

#### Universal/Transferable VLM Attacks

**Evidence**:
- Universal adversarial images show high model-dependent ASRs
- Examples: human-eval ~0.87, with variation by model/version
- Success varies with model version and OCR/preprocessing defenses

**Key Insight**: Universal visual triggers can transfer across models but effectiveness is sensitive to model architecture and defensive preprocessing.

**Citations**: (1.1, 5.1)

---

### 7. Multi-agent Vulnerabilities

**Impact**: Multi-agent systems substantially amplify jailbreak risk.

**Evidence**:
- Multi-Agent Debate (MAD) and agent red-teaming can raise harmfulness/ASR substantially
- Examples reporting increases from ~28% → ~80% in some configurations
- Agent coordination and conformity can be exploited

**Key Insight**: Multi-agent setups often amplify jailbreak risk through debate dynamics and emergent coordination effects.

**Citations**: (1.1)

---

### 8. Stylistic and Format Obfuscation

**Status**: General vulnerability confirmed; specific quantitative claims require qualification.

**Evidence**:
- Stylistic and format obfuscation (e.g., base64 encoding, role-play scenarios) can bypass naive input filters
- Effectiveness varies widely by model and defense sophistication

**Important Qualification**: Earlier claims of "100% ASR" for poetry-based jailbreaks are **not supported by peer-reviewed, citable evidence** in retrieved sources for state-of-the-art models. While obfuscation techniques remain a concern, specific success rates depend on target model and defense layers.

**Citations**: (6.1, 7.1)

---

## Defense and Evaluation Updates

### Defense Efficacy

**Key Finding**: Guardrail efficacy varies widely; no single-stage filter suffices.

**Evidence**:
- Benchmarks show some attacks (GPTFuzz, AutoDAN) maintain high ASR (≈90%+) under certain defenses
- Other attacks are more effectively suppressed
- Robustness depends on defense stacking:
  - System prompts
  - Safety fine-tuning
  - Adversarial tuning
- Evaluator choice significantly affects measured harmfulness

**Recommended Approach**: Multi-layered defenses combining multiple strategies, with continuous evaluation against evolving attacks.

**Citations**: (2.1, 2.2, 4.1)

---

### Input vs. Output Filters

**Important Correction**: Earlier dashboard claims about specific WASR/percentage breakdowns for input vs. output filter performance are **not supported by retrieved sources**.

**Evidence-backed Guidance**:
- Both input- and output-stage defenses show uneven efficacy
- Performance varies by specific attack type and model
- Refer to model- and attack-specific ASR matrices from standardized evaluations (e.g., TeleAI-Safety tables)

**Citations**: (4.1, 2.1)

---

### Model Safety Rankings

**Important Correction**: Replace bespoke rankings with model-specific ASR snapshots from standardized benchmarks.

**Evidence**:
- TeleAI-Safety benchmark shows lower ASR for certain proprietary models relative to open-source
- Results vary significantly by attack type
- Model-specific vulnerabilities require granular, attack-stratified evaluation

**Citations**: (4.1)

---

### Evaluation Toolchains

**Key Finding**: Standardized benchmarks reveal large variability and are essential for repeatable metrics.

**Major Benchmarks**:

1. **JailTrickBench**
   - ~354 experiments reported
   - ~55,000 GPU hours of evaluation
   - Characterizes eight key factors affecting jailbreak success

2. **TeleAI-Safety**
   - 342 curated samples
   - 19 attacks × 29 defenses
   - Per-model ASR matrices for major proprietary and open models

**Key Insight**: Jailbreak evaluation methods differ materially; evaluator choice (e.g., external API toxicity scores) significantly affects measured harmfulness and can under- or over-estimate risk.

**Citations**: (2.1, 4.1, 2.3)

---

## Comprehensive Evidence Table

| Area | Representative Method/Benchmark | Key Quantitative Findings | Notable Qualitative Insights | Citation IDs |
|------|--------------------------------|---------------------------|------------------------------|--------------|
| **Many-shot jailbreaking** | Many-Shot / TAP (AdvBench) | ASR up to ~0.88 reported (TAP on AdvBench); effectiveness rises with longer context windows | Long-context (many-shot) attacks markedly increase success; performance highly model- and context-size dependent | (1.1, 2.1) |
| **Few-shot / improved few-shot** | Improved Few-Shot (I-FSJ) / adaptive few-shot variants | Few-shot variants report ASR often >80% and can approach ~95%+ on some open models | Carefully engineered few-shot demos and special tokens can circumvent defenses without huge context | (2.1, 2.2) |
| **PAIR (black-box iterative)** | PAIR / Prompt Automatic Iterative Refinement | TeleAI: PAIR ASR range ≈0.14–0.61 across tested black-box models (varies by model) | Semantic attacker-LM refinement yields competitive ASR and transfer; performance varies widely by target | (4.1, 2.1) |
| **Optimization-based (GCG family)** | GCG, I-GCG, Faster-GCG, MAGIC (optimizer variants) | I-GCG / AmpleGCG / Faster-GCG reach near-100% ASR on some open models; Faster-GCG ~10x compute reduction; MAGIC ~1.5x speedup (efficiency gains) | Token-optimization attacks can be highly effective but transfer and per-model success vary; optimization advances improve speed and scale | (2.1, 2.2) |
| **Simple adaptive attacks** | Manual adaptive templates + random-search suffix | 100% ASR on a 50-item AdvBench suite reported against multiple leading safety-aligned models | Simple, model-adaptive methods (using logprobs or tailored templates) can break top models; adaptivity critical | (3.1) |
| **VLM typography attacks (FigStep-style)** | Typographic visual prompts / OCR-encoded prompts | Reported LVLM typography attacks reach avg ASR ≈80–83% in reported studies (typography experiments) | Converting harmful text into images/typography bypasses text-only alignment and OCR gaps; visual embedding alignment is a weak link | (1.1, 5.1) |
| **Bi-modal VLM attacks (BAP)** | BAP (bi-modal adversarial prompt) | BAP: +29.03% mean ASR improvement vs baselines; successful white-box & black-box compromise of commercial LVLMs reported | Jointly optimizing visual perturbation + refined textual prompt substantially increases success and transferability | (5.1) |
| **Universal / transferable VLM attacks** | Universal adversarial images / transfer pipelines | Universal/transfer attacks report high model-dependent ASRs (examples: human-eval ~0.87 vs model/version sensitivity observed) | Universal visual triggers can transfer but success varies with model/version and OCR/preprocessing defenses | (1.1, 5.1) |
| **Multi-agent / MAD vulnerabilities** | Multi-Agent Debate (MAD) / agent red-teaming | Structured multi-agent attacks can raise harmfulness/ASR substantially (examples reporting increases from ~28% → ~80% in some setups) | Multi-agent setups often amplify jailbreak risk; agent coordination and conformity can be exploited | (1.1) |
| **Defense efficacy & guardrails** | System prompts, fine-tuning, safety training, detection stacks | Benchmarks show defenses variably reduce ASR; some attacks (GPTFuzz, AutoDAN) retain high ASR (~90%+) vs some defenses; system prompts and targeted fine-tuning improve robustness | No single defense is universally effective; combination (prompt guarding, adversarial tuning, multi-agent defenses) needed; performance-utility tradeoffs noted | (2.1, 2.2, 4.1) |
| **Benchmarks & toolkits** | JailTrickBench / TeleAI-Safety / JailbreakEval-style suites | JailTrickBench: ~354 experiments (~55k GPU hours) reported; TeleAI-Safety: 342 curated samples, 19 attacks × 29 defenses with per-model ASR matrices | Standardized benchmarks reveal large variability across attacks/models/defenses and are essential for repeatable dashboard metrics | (2.1, 4.1, 2.3) |

---

## Prioritized Action Items (February 2026)

### 1. Correct Unsupported Claims

- **Poetry-based jailbreak**: Replace unsupported "100% ASR" claim with evidence-backed note on obfuscation and formatting attacks
- Cite standardized results where available
- Status: **COMPLETED** (see Section 8: Stylistic and Format Obfuscation)

**Citations**: (6.1, 7.1)

### 2. Populate Attack Panels with Quantitative Ranges

All attack categories now include evidence-backed quantitative metrics:

- **Many-shot**: High ASR with long contexts (ASR up to ~0.88)
- **PAIR**: ASR ~0.14–0.61 on black-box models; low queries (<20)
- **GCG-family**: Near-100% on some open models; improved efficiency (10x speedup)
- **Adaptive manual attacks**: 100% ASR on 50-item AdvBench suite
- **VLM bi-modal/typography attacks**: Avg ASR ≈80–83%; BAP +29% over baselines

**Status**: **COMPLETED**

**Citations**: (3.1, 2.1, 2.2, 4.1, 5.1, 1.1)

### 3. Defense Section Enhancement

- Emphasize: No single-layer solution suffices
- Report per-defense reductions from standardized benchmarks
- Encourage multi-layered defenses and continuous evaluation
- Note evaluator sensitivity (API toxicity scores can under- or over-estimate harmfulness)

**Status**: **COMPLETED** (see Defense and Evaluation Updates section)

**Citations**: (2.1, 4.1, 2.3, 1.1)

---

## Important Limitations

### Data Interpretation

Some quantitative entries are ranges summarized from survey/benchmark tables. For dashboard applications:

1. **Pull exact per-model/per-attack cells** directly from benchmark matrices (e.g., TeleAI-Safety per-model ASR)
2. **Avoid overgeneralization** across different models and attack configurations
3. **Note context dependencies**: ASR varies significantly with:
   - Specific model version
   - Defense configurations
   - Evaluation methodology
   - Judge model selection

**Citations**: (4.1, 2.1)

### Evaluator Sensitivity

- Different evaluation methods yield materially different harmfulness scores
- External API toxicity scores may under- or over-estimate actual risk
- Standardized evaluation protocols are essential for reproducibility
- Multiple evaluators recommended for robust assessment

**Citations**: (2.3, 4.1)

### Temporal Context

This dashboard reflects the state of jailbreak research as of **February 2026**. The field evolves rapidly:

- New attack techniques emerge regularly
- Model defenses are continuously updated
- Benchmark methodologies are refined
- Previously effective attacks may become less effective as defenses improve

**Recommendation**: Regular updates (monthly or quarterly) are essential to maintain accuracy.

---

## Methodology

All claims in this dashboard are supported by:

1. **Peer-reviewed research** or standardized benchmark results
2. **Quantitative evidence** from reproducible experiments
3. **Multiple independent sources** where possible
4. **Explicit citation IDs** linking to source materials

Claims lacking sufficient evidence have been:
- Removed entirely
- Qualified with appropriate caveats
- Marked for future validation

---

## Citation Index

- **(1.1)**: Multi-modal and multi-agent vulnerability surveys
- **(2.1)**: JailTrickBench comprehensive evaluation study
- **(2.2)**: GCG family optimization attack studies
- **(2.3)**: Evaluation methodology and judge model sensitivity studies
- **(3.1)**: Simple adaptive attack studies on frontier models
- **(4.1)**: TeleAI-Safety standardized benchmark
- **(5.1)**: VLM/LVLM bi-modal attack studies
- **(6.1)**: Stylistic and format obfuscation studies
- **(7.1)**: Poetry-based jailbreak investigation (lack of supporting evidence noted)

---

## Conclusion

The jailbreak threat landscape continues to evolve with:

1. **Increasing sophistication** in attack techniques (multi-modal, adaptive, optimization-based)
2. **Persistent vulnerabilities** even in frontier safety-aligned models
3. **Variable defense efficacy** requiring multi-layered approaches
4. **Critical need** for standardized evaluation and continuous monitoring

**Key Takeaway**: No single defense mechanism provides comprehensive protection. Effective security requires combining multiple defense layers with continuous evaluation against evolving attack methodologies.

---

*Last updated: February 2026*
*Dashboard maintained with evidence-backed research only*
