# Contract-Driven Harness v4 Claim-Evaluation Map

## Purpose

This map constrains the v4 draft. New stability evidence strengthens one
bounded reliability claim but does not convert the paper into a general
state-machine or workflow result.

## Claims

| Claim ID | v4 contribution claim | Evaluation support | Boundary |
|---|---|---|---|
| C1 | Contract-rich harnessing improves absolute contract adherence in tested productivity slices. | Broad task slices, mechanism atoms, admitted macros. | Tested conditions only. |
| C2 | Gap compression is real but conditional. | Structured extraction positive; project initialization and research workflow mixed or undefined. | Requires a nonzero baseline gap and no reversed absolute gap. |
| C3 | Mechanism atoms make broad workflow failures interpretable. | Stage 6-7 atoms and local golden/known-bad gates. | Atom pass does not imply macro or workflow pass. |
| C4 | A repair loop can convert specific low-cost-model failures into explicit, testable obligations. | Stage 7e v1-v4; Stage B v5-v5.4. | Fixed mechanisms and contracts only. |
| C5 | Repaired obligations can transfer to a neighboring bounded macro. | Stage 7-next 4/4 targeted smoke. | Fixed-input, no-tool transfer only. |
| C6 | The frozen explicit-delta protocol is stable on one controlled state-mutation macro. | Stage B v5.4: 40/40 fresh strict passes; pooled Wilson 95% `[0.912, 1.000]`; each designed condition 8/8 with `[0.676, 1.000]`. | One model, provider, macro, harness, and designed perturbation suite. |
| C7 | Explicit delta shows directional but not preregistered engineering-scale improvement over exact postconditions. | Stage B v5.3: 15 matched pairs; 2 treatment-pass/control-fail, 0 reverse; risk difference `0.133`; exact McNemar `p=0.500`. | Mixed causal result; no `0.20` effect claim. |

## Evaluation Blocks

| Block | Primary question | Result | Paper use |
|---|---|---|---|
| Broad task slices | Does harnessing change absolute adherence and model gaps? | Positive absolute lift; conditional gap compression. | Motivation and boundary. |
| Mechanism atoms | Can obligations be isolated and tested? | Positive with boundary cases. | Method validity. |
| Composition and Stage 7e/next | Can repaired obligations survive bounded composition? | Targeted positive results after explicit repairs. | Repair-loop and narrow transfer. |
| Stage B v5.2 | Does evidence-binding separation have a large independent effect? | No engineering-scale effect observed. | Negative ablation. |
| Stage B v5.3 | Does explicit transition delta add a large effect over exact postconditions? | Mixed: 2 favorable discordant pairs, 0 reverse, threshold miss, exact McNemar `p=0.500`. | Causal boundary. |
| Stage B v5.4 | Does the frozen explicit-delta protocol remain stable over fresh repetitions? | 40/40 strict; all cells 8/8, with wide per-condition intervals. | Bounded stability claim. |

## Non-Claims

- low-cost and strong models are generally equivalent;
- harnessing universally compresses model gaps;
- explicit delta has a proven `0.20` causal advantage;
- full project initialization or research workflow is solved;
- arbitrary state-machine, tool, rollback, or concurrency reliability;
- favorable total cost or latency versus a strong model;
- provider-independent or model-family-independent reliability.

## v4 Position

The strongest new statement is:

> A contract-driven repair process produced one frozen controlled-state
> mutation protocol that Qwen3-8B executed correctly in 40/40 fresh runs
> across five bounded representation perturbations.

The paper must state beside it:

> The paired v5.3 ablation did not meet the preregistered `0.20` causal-effect
> threshold, so the stability result is not evidence of a large independent
> advantage over exact postconditions.
