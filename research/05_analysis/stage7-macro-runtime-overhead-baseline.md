# Stage 7 Macro Runtime And Payload Baseline

Prepared: 2026-06-13

Purpose: record what can and cannot be concluded about overhead from existing Stage 7e v4 and Stage 7-next artifacts.

## Available Measurements

The current adapter records:

- prompt bytes;
- output bytes;
- elapsed milliseconds;
- timeout and provider error events;
- configured maximum output tokens.

It does not retain provider-reported prompt tokens, completion tokens, total tokens, request price, or billing identifiers.

## Stage 7e v4

Initial attempts:

| Arm/run | Status | Prompt bytes | Output bytes | Elapsed |
|---|---|---:|---:|---:|
| G8 r1 | executed | 16209 | 4680 | 92.438 s |
| G8 r2 | executed | 16209 | 5080 | 289.765 s |
| G9 r1 | executed | 16314 | 6040 | 168.063 s |
| G9 r2 | timeout | 16314 | n/a | 420.094 s |

The first retry used `max_output_tokens=600`, returned 2113 bytes in 97.546 s, and was insufficient for the final strict artifact. The second retry restored `max_output_tokens=2000`, returned 4868 bytes in 126.203 s, and produced the admitted result.

Interpretation:

- the provider/runtime path is visibly variable even at temperature 0;
- retry overhead is material;
- byte counts are not token counts;
- four admitted outputs do not estimate a stable latency distribution.

## Stage 7-next

| Arm/run | Status | Prompt bytes | Output bytes | Elapsed |
|---|---|---:|---:|---:|
| G8 r1 | executed | 17030 | 5640 | 95.047 s |
| G8 r2 | executed | 17030 | 5784 | 104.687 s |
| G9 r1 | executed | 17135 | 5699 | 120.688 s |
| G9 r2 | executed | 17135 | 5118 | 212.469 s |

Successful-run median latency: 112.688 s.

Successful-run mean latency: 133.223 s.

Interpretation:

- G9 prompts are 105 bytes larger than G8 for this fixture;
- the observed latency spread is much larger than the prompt-size difference;
- no provider error occurred in these four runs;
- the sample is too small for an overhead or tail-latency claim.

## Current Claim Boundary

Supported:

- existing artifacts expose substantial runtime variance;
- Stage 7e v4 required timeout and truncation recovery;
- the harness adds prompt payload and engineering artifacts.

Not supported:

- exact token overhead;
- exact API cost;
- cost superiority of Qwen3-8B + G9 over DeepSeek-V3.2 + G0;
- stable P90/P95 latency;
- total engineering labor cost.

The next adapter revision must capture provider usage before a paper-level overhead comparison is attempted.
