# Stage B v3 Hierarchical Shape Repair Smoke Preregistration

Prepared: 2026-06-13

Status: prepared before provider execution

## Hypothesis

H1: Qwen3-8B with G9 and a literal JSON skeleton will preserve the required
`state_inventory` hierarchy and pass the unchanged macro evaluator in at least
2/3 canonical runs.

H1 is falsified if fewer than two of three runs pass.

## Mechanism Atom

Name: `hierarchical_output_shape_preservation`

Input: the failed Stage B v2 canonical method-plan macro.

Single changed factor: the model-visible descriptive output template is
replaced by a literal JSON skeleton whose keys and nesting can be copied
directly.

Output contract:

- `state_inventory` is an object;
- it contains `known_state`, `unknown_state`, and `forbidden_inferences`;
- no nested state field may be promoted to the root or omitted;
- all other Stage B v2 semantic obligations remain unchanged.

## Controls

- provider: SiliconFlow;
- model: `Qwen/Qwen3-8B`;
- harness: G9;
- temperature: 0;
- maximum output tokens: 3000;
- `enable_thinking=false`;
- evaluator and thresholds: unchanged from Stage B v2;
- fixture semantics, evidence, state labels, selected option, and stage gate:
  unchanged;
- repetitions: three.

## Baseline

Historical baseline: Stage B v2 canonical method-plan cell, 0/3 passes. Its
three outputs consistently flattened the nested state hierarchy.

The historical baseline is diagnostic and not poolable with v3.

## Metrics

Primary:

- binary full-contract pass;
- `schema_validity`;
- `state_accuracy`;
- `atom_primary_metric`.

Secondary:

- all remaining contract metrics;
- prompt/completion/total tokens;
- latency, timeout, truncation, and provider errors.

These metrics test contract adherence, not human preference or open-ended
writing quality.

## Local Gates

Before provider execution:

1. golden output passes;
2. flattened-state known-bad fails schema and state metrics;
3. root-promoted-state known-bad fails schema and state metrics;
4. omitted-nested-state known-bad fails schema and state metrics;
5. all inherited Stage B v2 known-bads remain rejected;
6. Stage B v2 regression gate remains unchanged.

## Decision Rule

- 2/3 or 3/3 passes: admit preparation of a separately frozen full Stage B v3
  perturbation slice.
- 0/3 or 1/3 passes: reject the literal-skeleton repair and diagnose before any
  further provider calls.

Provider error, ambiguous evaluator behavior, or protocol drift stops execution
for diagnosis.

## Ablation Boundary

This smoke isolates literal skeleton versus descriptive template. It does not
test provider-native structured output, JSON Schema enforcement, grammar
decoding, thinking mode, or a different model. Those require separate
protocols.

## Validity Threats

- Three runs provide only a repair gate, not a precise stability estimate.
- The mechanism is tested on one failed macro.
- The literal skeleton includes exact required state IDs and may increase prompt
  guidance beyond hierarchy alone.
- Provider behavior may vary despite temperature 0.
- A pass supports this bounded contract only, not arbitrary nested schemas.

## Pooling Policy

Do not pool Stage B v2 and Stage B v3 runs. Preserve both outcomes and their
protocol lineage.
