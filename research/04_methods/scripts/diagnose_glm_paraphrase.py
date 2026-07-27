"""Quick diagnostic: what does GLM actually output for unknown_state_paraphrase?"""
import sys, json, os, re
sys.path.insert(0, 'research/04_methods/scripts')
from verify_stage_b_v54_live import load_prompt, load_reference_output, call_api, extract_json

# Load env
for line in open('.env'):
    parts = line.strip().split('=', 1)
    if len(parts) == 2:
        os.environ[parts[0]] = parts[1]

prompt = load_prompt('unknown_state_paraphrase')
ref = load_reference_output('unknown_state_paraphrase')

print('=== Reference unknown_state (what evaluator expects): ===')
print(json.dumps(ref['state_inventory']['unknown_state'], indent=2))
print()
print('=== Reference forbidden_inferences: ===')
print(json.dumps(ref['state_inventory']['forbidden_inferences'], indent=2))
print()

# Find what the prompt declares as initial/residual state labels
print('=== Prompt snippet: residual_unknown_state ===')
idx = prompt.find('residual_unknown_state')
if idx >= 0:
    print(prompt[idx-20:idx+200])
print()

print('=== Calling GLM-4-9B... ===')
result = call_api('THUDM/GLM-4-9B-0414', prompt)
output = extract_json(result['content'])

if output is None:
    print('PARSE FAILED. Raw output:')
    print(result['content'][:800])
else:
    glm_unknown = output.get('state_inventory', {}).get('unknown_state', [])
    glm_forbid = output.get('state_inventory', {}).get('forbidden_inferences', [])

    print('=== GLM actual output unknown_state: ===')
    print(json.dumps(glm_unknown, indent=2))
    print()
    print('=== GLM actual output forbidden_inferences: ===')
    print(json.dumps(glm_forbid, indent=2))
    print()

    # Direct comparison
    ref_unknown = ref['state_inventory']['unknown_state']
    ref_forbid = ref['state_inventory']['forbidden_inferences']

    print('=== Diagnosis ===')
    unknown_match = sorted(glm_unknown) == sorted(ref_unknown)
    forbid_match = sorted(glm_forbid) == sorted(ref_forbid)
    print(f'unknown_state exact match: {unknown_match}')
    print(f'forbidden_inferences exact match: {forbid_match}')

    if not unknown_match:
        print(f'  Reference: {sorted(ref_unknown)}')
        print(f'  GLM:       {sorted(glm_unknown)}')
        # Check if GLM output canonical labels instead of paraphrased
        canonical = ['current_git_branch', 'ci_status']
        if sorted(glm_unknown) == sorted(canonical):
            print('  --> GLM output CANONICAL labels instead of paraphrased!')
            print('  --> This is terminology normalization, not capability failure')
