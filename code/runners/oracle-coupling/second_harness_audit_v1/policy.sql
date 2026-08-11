PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS policy (
    fixture_id TEXT PRIMARY KEY,
    family TEXT NOT NULL,
    decision TEXT NOT NULL CHECK (decision IN ('apply', 'block')),
    gate_status TEXT NOT NULL,
    gate_reason TEXT NOT NULL,
    permitted_action TEXT NOT NULL,
    next_action TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS policy_patch (
    path TEXT PRIMARY KEY,
    from_json TEXT NOT NULL CHECK (json_valid(from_json)),
    to_json TEXT NOT NULL CHECK (json_valid(to_json))
);

CREATE TABLE IF NOT EXISTS policy_patch_evidence (
    path TEXT NOT NULL REFERENCES policy_patch(path) ON DELETE CASCADE,
    evidence_id TEXT NOT NULL,
    PRIMARY KEY (path, evidence_id)
);

CREATE TABLE IF NOT EXISTS policy_preserved (
    path TEXT PRIMARY KEY,
    value_json TEXT NOT NULL CHECK (json_valid(value_json))
);

CREATE TABLE IF NOT EXISTS policy_decision_evidence (
    evidence_id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS policy_unknown (value TEXT PRIMARY KEY);
CREATE TABLE IF NOT EXISTS policy_forbidden (value TEXT PRIMARY KEY);

CREATE TABLE IF NOT EXISTS state_kv (
    path TEXT PRIMARY KEY,
    value_json TEXT NOT NULL CHECK (json_valid(value_json)),
    version INTEGER NOT NULL DEFAULT 0 CHECK (version >= 0)
);

CREATE TABLE IF NOT EXISTS candidate (
    singleton INTEGER PRIMARY KEY CHECK (singleton = 1),
    raw_json TEXT NOT NULL CHECK (json_valid(raw_json))
);

DROP VIEW IF EXISTS candidate_violations;
CREATE VIEW candidate_violations AS
WITH
raw AS (
    SELECT raw_json AS value FROM candidate WHERE singleton = 1
),
required_top_level(value) AS (
    VALUES
        ('task_id'), ('decision'), ('state_patch'), ('preserved_state'),
        ('evidence_bindings'), ('unknown_state'), ('forbidden_inferences'),
        ('gate'), ('next_action')
),
candidate_top_level AS (
    SELECT key AS value FROM raw, json_each(raw.value)
),
candidate_patches AS (
    SELECT json_each.value AS value FROM raw, json_each(raw.value, '$.state_patch')
),
candidate_preserved AS (
    SELECT
        json_extract(json_each.value, '$.path') AS path,
        json_extract(json_each.value, '$.value') AS value
    FROM raw, json_each(raw.value, '$.preserved_state')
),
candidate_decision_bindings AS (
    SELECT json_each.value AS value
    FROM raw, json_each(raw.value, '$.evidence_bindings')
    WHERE json_extract(json_each.value, '$.slot_id') = 'decision'
),
violations(reason) AS (
    SELECT 'candidate_not_object'
    FROM raw
    WHERE json_type(raw.value, '$') <> 'object'

    UNION ALL
    SELECT 'top_level_field_set_mismatch'
    WHERE EXISTS (SELECT value FROM required_top_level EXCEPT SELECT value FROM candidate_top_level)
       OR EXISTS (SELECT value FROM candidate_top_level EXCEPT SELECT value FROM required_top_level)

    UNION ALL
    SELECT 'invalid_collection_shape'
    FROM raw
    WHERE json_type(raw.value, '$.state_patch') <> 'array'
       OR json_type(raw.value, '$.preserved_state') <> 'array'
       OR json_type(raw.value, '$.evidence_bindings') <> 'array'
       OR json_type(raw.value, '$.unknown_state') <> 'array'
       OR json_type(raw.value, '$.forbidden_inferences') <> 'array'
       OR json_type(raw.value, '$.gate') <> 'object'

    UNION ALL
    SELECT 'task_identity_mismatch'
    FROM raw, policy
    WHERE json_extract(raw.value, '$.task_id') IS NOT policy.fixture_id

    UNION ALL
    SELECT 'decision_mismatch'
    FROM raw, policy
    WHERE json_extract(raw.value, '$.decision') IS NOT policy.decision

    UNION ALL
    SELECT 'patch_count_mismatch'
    WHERE (SELECT count(*) FROM candidate_patches)
       <> (SELECT count(*) FROM policy_patch)

    UNION ALL
    SELECT 'patch_field_or_target_mismatch'
    FROM candidate_patches AS cp
    LEFT JOIN policy_patch AS pp
      ON json_extract(cp.value, '$.path') = pp.path
    WHERE pp.path IS NULL
       OR json_type(cp.value, '$') <> 'object'
       OR (SELECT count(*) FROM json_each(cp.value)) <> 4
       OR json_extract(cp.value, '$.from') IS NOT json_extract(pp.from_json, '$')
       OR json_extract(cp.value, '$.to') IS NOT json_extract(pp.to_json, '$')

    UNION ALL
    SELECT 'patch_evidence_mismatch'
    FROM candidate_patches AS cp
    JOIN policy_patch AS pp
      ON json_extract(cp.value, '$.path') = pp.path
    WHERE json_type(cp.value, '$.evidence_ids') <> 'array'
       OR EXISTS (
            SELECT CAST(value AS TEXT) FROM json_each(cp.value, '$.evidence_ids')
            EXCEPT
            SELECT evidence_id FROM policy_patch_evidence WHERE path = pp.path
       )
       OR EXISTS (
            SELECT evidence_id FROM policy_patch_evidence WHERE path = pp.path
            EXCEPT
            SELECT CAST(value AS TEXT) FROM json_each(cp.value, '$.evidence_ids')
       )

    UNION ALL
    SELECT 'stale_live_state'
    FROM candidate_patches AS cp
    JOIN state_kv AS state
      ON json_extract(cp.value, '$.path') = state.path
    WHERE json_extract(cp.value, '$.from') IS NOT json_extract(state.value_json, '$')

    UNION ALL
    SELECT 'preserved_state_mismatch'
    WHERE EXISTS (
        SELECT path, json_extract(value_json, '$') FROM policy_preserved
        EXCEPT
        SELECT path, value FROM candidate_preserved
    ) OR EXISTS (
        SELECT path, value FROM candidate_preserved
        EXCEPT
        SELECT path, json_extract(value_json, '$') FROM policy_preserved
    )

    UNION ALL
    SELECT 'preserved_live_state_mismatch'
    FROM policy_preserved AS preserved
    LEFT JOIN state_kv AS state ON state.path = preserved.path
    WHERE state.path IS NULL
       OR json_extract(state.value_json, '$')
          IS NOT json_extract(preserved.value_json, '$')

    UNION ALL
    SELECT 'decision_binding_cardinality'
    WHERE (SELECT count(*) FROM candidate_decision_bindings) <> 1
       OR (SELECT count(*) FROM raw, json_each(raw.value, '$.evidence_bindings')) <> 1

    UNION ALL
    SELECT 'decision_evidence_mismatch'
    FROM candidate_decision_bindings AS binding
    WHERE json_type(binding.value, '$.evidence_ids') <> 'array'
       OR EXISTS (
            SELECT evidence_id FROM policy_decision_evidence
            EXCEPT
            SELECT CAST(value AS TEXT) FROM json_each(binding.value, '$.evidence_ids')
       )
       OR EXISTS (
            SELECT CAST(value AS TEXT) FROM json_each(binding.value, '$.evidence_ids')
            EXCEPT
            SELECT evidence_id FROM policy_decision_evidence
       )

    UNION ALL
    SELECT 'unknown_state_mismatch'
    FROM raw
    WHERE EXISTS (
        SELECT value FROM policy_unknown
        EXCEPT
        SELECT CAST(value AS TEXT) FROM json_each(raw.value, '$.unknown_state')
    ) OR EXISTS (
        SELECT CAST(value AS TEXT) FROM json_each(raw.value, '$.unknown_state')
        EXCEPT
        SELECT value FROM policy_unknown
    )

    UNION ALL
    SELECT 'forbidden_inferences_mismatch'
    FROM raw
    WHERE EXISTS (
        SELECT value FROM policy_forbidden
        EXCEPT
        SELECT CAST(value AS TEXT) FROM json_each(raw.value, '$.forbidden_inferences')
    ) OR EXISTS (
        SELECT CAST(value AS TEXT) FROM json_each(raw.value, '$.forbidden_inferences')
        EXCEPT
        SELECT value FROM policy_forbidden
    )

    UNION ALL
    SELECT 'gate_attestation_mismatch'
    FROM raw, policy
    WHERE json_type(raw.value, '$.gate') <> 'object'
       OR (SELECT count(*) FROM json_each(raw.value, '$.gate')) <> 3
       OR json_extract(raw.value, '$.gate.status') IS NOT policy.gate_status
       OR json_extract(raw.value, '$.gate.reason_code') IS NOT policy.gate_reason
       OR json_extract(raw.value, '$.gate.permitted_action') IS NOT policy.permitted_action

    UNION ALL
    SELECT 'next_action_mismatch'
    FROM raw, policy
    WHERE json_extract(raw.value, '$.next_action') IS NOT policy.next_action
)
SELECT DISTINCT reason FROM violations ORDER BY reason;
