# Contract-Driven Harness Reference Core

Framework-agnostic reference implementation of the contract stack and 7 deterministic evaluators for the controlled-state-mutation task family, accompanying the paper "Contract-Driven Harness Engineering for Reliable Low-Cost Agent Tasks".

## What This Is

A ~260-line Python module (`contract_core.py`) that implements:

- **Contract types**: TaskSpec, EvidenceBundle, MemorySlice, OutputContract, TransitionEvent, TransitionDelta, TransitionGate, RetentionAttestation
- **7 deterministic evaluators**: schema validity, evidence array preservation, residual unknown vocabulary accuracy, state transition accuracy, transition gate accuracy, retention attestation accuracy, controlled state mutation success
- **ContractHarness class**: evaluates model outputs against a frozen reference
- **FrameworkAdapter interface**: minimal interface for connecting to PEtFiSh, LangChain, or any other agent framework

## What This Is Not

- Not a general agent framework
- Not a benchmark (the task family is specific to controlled state mutation)
- Not affiliated with any specific agent framework — contains zero imports from PEtFiSh, LangChain, LangGraph, or similar

## Quick Start

```bash
python contract_core.py  # self-test
```

```python
from contract_core import ContractHarness, parse_json_output

# Load the golden reference output (from frozen protocol)
reference = json.load(open("golden_output.json"))

# Create harness
harness = ContractHarness(reference)

# Evaluate a model output
raw_output = model.generate(prompt)
result = harness.evaluate_raw(raw_output)

print(f"Strict pass: {result.strict_pass}")
print(f"Failed checks: {result.failed_checks}")
```

## Integration

To use with your agent framework, implement the `FrameworkAdapter` interface:

```python
from contract_core import FrameworkAdapter

class MyFrameworkAdapter(FrameworkAdapter):
    def build_prompt(self, task_spec, output_contract, evidence, memory):
        # Build prompt using your framework's prompt template
        return my_prompt_template(task_spec, output_contract, evidence, memory)

    def call_model(self, prompt, model_id, **kwargs):
        # Call model using your framework's API client
        return my_framework.generate(prompt, model_id, **kwargs)
```

## License

MIT

## Citation

If you use this reference core in your research, please cite:

```
@software{contract_driven_harness_core,
  title={Contract-Driven Harness Reference Core},
  version={1.0.0},
  license={MIT},
  year={2026}
}
```

## Verification

Independence from PEtFiSh verified by:

```bash
python research/04_methods/scripts/verify_zero_petfish_dep.py --core-path reference-core/
```

Result: 0 blockers, 0 warnings, 0 info findings (no textual coupling).
