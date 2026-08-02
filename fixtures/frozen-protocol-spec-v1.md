# Frozen Protocol Specification v1.0

*Standalone specification for the frozen-protocol verification layer in the contract-driven harness repair loop. Companion to paper §3.5.*

## 1. Frozen Items

| # | Frozen item | What is recorded | Example identifier |
|---|---|---|---|
| 1 | Sampling parameter: temperature | The exact temperature value used for all model calls. | `temperature = 0` |
| 2 | Provider and model version snapshot | Provider endpoint and exact model identifier, including any date-stamped version or snapshot tag. | `SiliconFlow / Qwen/Qwen3-8B` |
| 3 | Prompt artifacts | All model-visible prompt files exported before execution, identified by SHA-256 hash. | `prompt-main-v5.4.sha256 = abc123...` |
| 4 | Evaluator version | The exact validator or probe code and fixture version used to score outputs. | `evaluator-stage-b-v5.4.sha256 = def456...` |
| 5 | Known-bad set version | The set of regression fixtures defining the failure modes the protocol claims to avoid. | `known-bad-set-v10.sha256 = ghi789...` |
| 6 | Perturbation set version | The designed perturbations used to test stability. | `perturbation-set-v5.sha256 = jkl012...` |

All frozen items are recorded in a machine-readable manifest at freeze time. The manifest is itself versioned and hashed.

## 2. Why Each Item Must Be Frozen

| Frozen item | Claim invalidated if the item is not pinned |
|---|---|
| Temperature | A non-zero or changed temperature can alter the sample distribution; the observed pass rate would no longer describe a fixed sampling process. |
| Provider and model version snapshot | Provider routing, model updates, or quantization changes can change behavior; a stability claim becomes unanchored. |
| Prompt hash | Any change to the model-visible prompt changes the task; results are not comparable across runs. |
| Evaluator version | A revised validator can reclassify passing outputs as failures; adherence metrics become uninterpretable. |
| Known-bad set version | Missing or altered regression fixtures change the meaning of "stable" for the repaired failure modes. |
| Perturbation set version | Different perturbations test different robustness boundaries; the claim no longer refers to the same test suite. |

A frozen-protocol claim is a claim about one specific artifact stack. Changing any item without re-freezing voids the claim.

## 3. SHA-256 Verification Script Specification

### 3.1 Inputs and Outputs

- **Input:** `manifest_path` pointing to a manifest with `manifest_version` and a `frozen_items` list. Each item has `name`, `path`, `expected_hash`, and `type` (`file` or `literal`).
- **Output:** a verification record with `manifest_version`, `timestamp`, per-item `{name, path, expected_hash, actual_hash, status}`, and overall `outcome` (`verified` or `abort`). The record is appended to the trace log.

### 3.2 Behavior

1. Load the manifest.
2. For each frozen item, compute the SHA-256 hash of the file if `type == "file"`, or read the literal value if `type == "literal"`. Compare with `expected_hash` and record `match` or `mismatch`.
3. If any item does not match, set `outcome = "abort"`, log the mismatch, and raise an exception or exit with a non-zero status so the run batch cannot proceed without explicit override.
4. If all items match, set `outcome = "verified"`, append the record to the trace log, and return the record.

### 3.3 Pseudocode

```python
def verify_frozen_protocol(manifest_path):
    manifest = load_manifest(manifest_path)
    record = {
        "manifest_version": manifest["manifest_version"],
        "timestamp": now_iso(),
        "frozen_items": [],
        "outcome": "verified",
    }

    for item in manifest["frozen_items"]:
        if item["type"] == "file":
            actual = sha256_file(item["path"])
        elif item["type"] == "literal":
            actual = read_literal(item["path"])
        else:
            raise ValueError(f"Unknown item type: {item['type']}")

        status = "match" if actual == item["expected_hash"] else "mismatch"
        record["frozen_items"].append({
            "name": item["name"],
            "path": item["path"],
            "expected_hash": item["expected_hash"],
            "actual_hash": actual,
            "status": status,
        })

        if status == "mismatch":
            record["outcome"] = "abort"
            log_mismatch(record)
            raise FrozenProtocolMismatch(item)

    append_to_trace_log(record)
    return record
```

The manifest must be generated at freeze time, not reconstructed afterward. The script is invoked as the first step of any run batch contributing to a frozen-protocol claim; if it is skipped, the claim is void. A mismatch means the current run is not the frozen protocol; any deviation must be logged and either corrected or treated as a new protocol version requiring a new freeze record.

## 4. Relation to the V4 Body

The V4 paper pinned provider settings and exported prompt artifacts before execution, but it did not explicitly list `temperature` among the frozen items. This specification retroactively closes that gap: `temperature = 0` is now a pinned, verified, and logged item for every frozen-protocol claim. Subsequent replications showed that unpinned sampling parameters make cross-framework comparison impossible, so the freeze must include them.
