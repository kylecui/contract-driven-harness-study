# V4.1 De-AI Change Log

Date: 2026-06-30
Reviewer: writing agent (anti-sycophancy + de-AI pass)

## Summary
- 8 modifications
- 必修三连 (rhetorical adjective triples): 3
- 边界调整 (suggested-review list/chain smoothing): 4
- 其他AI味 (template-verb / "ability to" phrasing): 1

All protected enumerations were left untouched: the seven-component obligation stack (L8/L22/L100/L417), the six experiment slices (L12), the five harness-specification objects (L24), the seven related-work families (L50/L54-62), the orchestration feature list (L66), tables, experimental-setting enumerations, numeric claims, and the LangChain/W2 caveat paragraphs.

## Changes

### Change 1: Abstract "represents" template verb
- Location: Line 8, Abstract
- Type: 模板动词替换
- Before: `We study contract-driven harness engineering: a reliability layer that represents those obligations as task specifications, bounded memory slices, evidence bundles, output contracts, validation gates, and trace requirements.`
- After: `We study contract-driven harness engineering: a reliability layer that captures those obligations as task specifications, bounded memory slices, evidence bundles, output contracts, validation gates, and trace requirements.`
- Reason: "represents X as Y" is a common AI-generated definitional template; "captures" keeps the engineering meaning without the canned verb.

### Change 2: Abstract "inspectable, repairable, regression-testable" triple
- Location: Line 10 (original) / Lines 10-11 (after edit), Abstract
- Type: 修辞性三连拆分
- Before: `It asks whether explicit obligations can turn failures observed in low-cost-model runs into inspectable, repairable, and regression-testable engineering objects.`
- After: `It asks whether explicit obligations can turn failures observed in low-cost-model runs into named engineering objects. Once named, a failure can be inspected, repaired, and regression-tested.`
- Reason: The three stacked adjectives served the same object and the same layer (quality of the object); splitting them into a naming claim plus a concrete action claim removes the rhetorical cadence while preserving the technical point.

### Change 3: Introduction six-"which" obligation chain
- Location: Line 20, Section 1
- Type: 边界调整 / 排比节奏缓和
- Before: `Many productivity tasks contain obligations that can be stated before generation starts: which evidence may be used, which state is known or unknown, which actions are blocked, which fields must be present, which claims require citations, and which stage gate prevents a final recommendation.`
- After: `Many productivity tasks contain obligations that can be stated before generation starts: which evidence may be used, what counts as known or unknown state, which actions are blocked, which fields must be present, which claims require citations, and which stage gate blocks a final recommendation.`
- Reason: Content is a substantive six-item enumeration, but the identical "which X" groove was mechanical. Two items are rephrased to vary the rhythm without dropping any obligation type.

### Change 4: "model's ability to" phrasing
- Location: Line 24, Section 1
- Type: 其他AI味 / 能力表述直接化
- Before: `Model capability is the model's ability to reason, follow instructions, and recover from ambiguity.`
- After: `Model capability is whether the model can reason, follow instructions, and recover from ambiguity.`
- Reason: "X is the ability to" is a frequent AI framing device; stating capability as what the model can do is more direct and more human.

### Change 5: Repair-loop six-verb colon list
- Location: Line 36 (original) / Lines 36-38 (after edit), Section 1
- Type: 边界调整 / 动词排比重构
- Before: `They also make some failures easier to repair: a missing obligation can be named, added to the contract, captured as a known-bad case, checked locally, rerun against a model, and carried into the evidence ledger and claim boundary.`
- After: `They also make some failures easier to repair. A missing obligation can be named, added to the contract, and captured as a known-bad case. It can then be checked locally, rerun against a model, and carried into the evidence ledger and claim boundary.`
- Reason: The six actions are substantive repair-loop steps, but the single colon list had a generative cadence. Two sentences with different subjects ("a missing obligation" vs "it") create the uneven pacing of real engineering prose.

### Change 6: Related Work "durable, inspectable, easier" mixed triple
- Location: Line 68 (original) / Lines 68-69 (after edit), Section 2.1
- Type: 修辞性三连拆分
- Before: `These systems make execution durable, inspectable, and easier to integrate with tools and humans.`
- After: `These systems make execution durable and inspectable. Integration with tools and humans becomes easier as a result.`
- Reason: The original forced a third item that was structurally different (comparative clause) to complete the rhythm. Splitting into two short claims removes the artificial tricolon.

### Change 7: Conclusion "observable, repairable, regression-testable" triple
- Location: Line 429 (original) / Lines 429-430 (after edit), Section 6
- Type: 修辞性三连拆分
- Before: `Contract-driven harness engineering makes some low-cost-model failures observable, repairable, and regression-testable by moving reliability obligations into explicit contracts.`
- After: `Contract-driven harness engineering moves reliability obligations into explicit contracts. Some low-cost-model failures become observable and repairable, and each one can be regression-tested.`
- Reason: Same pattern as Change 2: three adjectives on the same object were carrying the sentence's rhythm. Putting the mechanism first and then stating the two readiness levels separately keeps the claim engineering-shaped.

### Change 8: Repair-loop seven-"a" artifact list
- Location: Line 433 (original) / Lines 433-434 (after edit), Section 6
- Type: 边界调整 / 冠词排比削减
- Before: `A harness failure can be turned into a named obligation, a contract revision, a known-bad fixture, a local regression gate, a targeted ablation, a fresh stability confirmation, and an updated claim boundary.`
- After: `A harness failure can be turned into a named obligation. That obligation drives a contract revision, a known-bad fixture, a local regression gate, a targeted ablation, a fresh stability confirmation, and an updated claim boundary.`
- Reason: The seven artifacts are real repair-loop outputs, but the repeated "a X, a Y" article cadence was AI-feeling. Moving the list after a short subject hand-off removes the mechanical repetition while keeping every output.

## Not changed (substantive enumerations)

- L12: six experiment slice names
- L22/L100/L417: seven-component obligation stack
- L24: five harness-specification objects
- L50/L54-62: seven related-work families and Table 1
- L66: orchestration framework capabilities
- L70: obligation-unit list
- L84: semantic obligation list
- L162/L244/L306/L336/L340/L425/L493: experimental-setting and metric enumerations
- L371: harness-object list in Discussion
- All tables and numeric claims
- LangChain citation paragraph (L14/L72) and W2 caveat paragraphs (L365/L375)
