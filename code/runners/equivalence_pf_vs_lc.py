"""Equivalence test (TOST) for paired framework comparison.

Implements Two One-Sided Tests to determine whether two framework adapters
(pf and LangChain) produce statistically equivalent pass rates on the same
set of paired inputs under a frozen protocol.

Replaces the original McNemar-based "indistinguishable" claim, which is
underpowered when both arms have near-ceiling pass rates (e.g., 40/40 vs
37/40 yields only 3 discordant pairs, making McNemar p > 0.05 nearly
guaranteed regardless of true difference).

Reference: Schuirmann (1987), Westlake (1981).

Usage
-----
    python equivalence_pf_vs_lc.py \\
        --pf-records research/05_analysis/author-confirmation-records/pf_v5_confirmed.json \\
        --lc-records research/05_analysis/author-confirmation-records/lc_v5_confirmed.json \\
        --delta 0.10 \\
        --alpha 0.05 \\
        --output research/05_analysis/equivalence-pf-vs-lc-result.json

Input format
------------
Each records JSON file must be a list of run objects, each with at least:
    {
        "run_id": "canonical_001",      # paired key, must match across files
        "strict_pass": true,             # bool, the binary outcome
        "condition": "canonical",        # perturbation condition
        ...
    }

Pairing is by `run_id`. Records without a match in the other file are dropped
with a warning.

Output
------
JSON with fields:
    {
        "n_paired": 40,
        "pf_pass_count": 40,
        "lc_pass_count": 37,
        "pf_pass_rate": 1.0,
        "lc_pass_rate": 0.925,
        "observed_diff": 0.075,
        "delta": 0.10,
        "alpha": 0.05,
        "tost_lower_p": 0.012,    # H0: diff <= -delta
        "tost_upper_p": 0.008,    # H0: diff >= +delta
        "tost_combined_p": 0.012, # max of the two
        "equivalence_rejected": true,   # True = equivalent within delta
        "interpretation": "..."
    }

Decision rule
-------------
- equivalence_rejected = True  =>  pass rates are equivalent within delta
- equivalence_rejected = False =>  sample cannot establish equivalence
  (either true difference >= delta, or sample too small to tell)
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


def load_records(path: Path) -> dict[str, dict[str, Any]]:
    """Load run records keyed by run_id."""
    text = path.read_text(encoding="utf-8")
    raw = json.loads(text)
    if not isinstance(raw, list):
        raise ValueError(f"{path}: expected a JSON list of run objects")
    keyed: dict[str, dict[str, Any]] = {}
    for run in raw:
        rid = run.get("run_id")
        if rid is None:
            raise ValueError(f"{path}: run object missing 'run_id': {run!r}")
        if rid in keyed:
            raise ValueError(f"{path}: duplicate run_id {rid!r}")
        if "strict_pass" not in run:
            raise ValueError(f"{path}: run {rid!r} missing 'strict_pass'")
        keyed[rid] = run
    return keyed


def pair_records(
    pf: dict[str, dict[str, Any]], lc: dict[str, dict[str, Any]]
) -> list[tuple[str, int, int]]:
    """Pair records by run_id. Returns list of (run_id, pf_pass, lc_pass)."""
    pairs = []
    missing_in_lc = sorted(set(pf) - set(lc))
    missing_in_pf = sorted(set(lc) - set(pf))
    if missing_in_lc:
        print(
            f"WARNING: {len(missing_in_lc)} pf run_ids have no lc pair; dropped: {missing_in_lc[:5]}{'...' if len(missing_in_lc) > 5 else ''}",
            file=sys.stderr,
        )
    if missing_in_pf:
        print(
            f"WARNING: {len(missing_in_pf)} lc run_ids have no pf pair; dropped: {missing_in_pf[:5]}{'...' if len(missing_in_pf) > 5 else ''}",
            file=sys.stderr,
        )
    for rid in sorted(set(pf) & set(lc)):
        pf_pass = 1 if bool(pf[rid]["strict_pass"]) else 0
        lc_pass = 1 if bool(lc[rid]["strict_pass"]) else 0
        pairs.append((rid, pf_pass, lc_pass))
    return pairs


def proportion_diff_ci_mcnemar(pairs: list[tuple[str, int, int]]) -> dict[str, float]:
    """Compute observed proportions and discordant counts."""
    n = len(pairs)
    if n == 0:
        raise ValueError("no paired records")
    pf_passes = sum(p for _, p, _ in pairs)
    lc_passes = sum(l for _, _, l in pairs)
    # discordant cells
    pf_only = sum(1 for _, p, l in pairs if p == 1 and l == 0)  # b
    lc_only = sum(1 for _, p, l in pairs if p == 0 and l == 1)  # c
    return {
        "n_paired": n,
        "pf_pass_count": pf_passes,
        "lc_pass_count": lc_passes,
        "pf_pass_rate": pf_passes / n,
        "lc_pass_rate": lc_passes / n,
        "observed_diff": (pf_passes - lc_passes) / n,
        "discordant_pf_only": pf_only,  # b
        "discordant_lc_only": lc_only,  # c
    }


def tost_paired_binary(
    pairs: list[tuple[str, int, int]], delta: float, alpha: float = 0.05
) -> dict[str, Any]:
    """TOST for paired binary outcomes.

    Uses the paired-difference standard error on the discordant proportion
    difference: SE = sqrt((b + c) / n^2) where b, c are discordant counts.
    This is the same SE used by McNemar's test for the difference in
    marginal proportions.

    Tests:
        H0_lower: diff <= -delta    vs   H1: diff > -delta
        H0_upper: diff >= +delta    vs   H1: diff < +delta

    Equivalence is declared if both one-sided tests reject at level alpha.
    """
    stats = proportion_diff_ci_mcnemar(pairs)
    n = stats["n_paired"]
    b = stats["discordant_pf_only"]
    c = stats["discordant_lc_only"]
    observed = stats["observed_diff"]

    # Standard error of the marginal proportion difference (McNemar form)
    # SE = sqrt((b + c)) / n
    se = math.sqrt(b + c) / n if n > 0 else float("inf")

    if se == 0:
        # No discordant pairs: observed_diff == 0 and SE == 0
        # TOST reduces to: -delta < 0 < delta => equivalent if delta > 0
        lower_p = 0.0 if observed > -delta else 1.0
        upper_p = 0.0 if observed < delta else 1.0
        interpretation_zero_se = (
            "No discordant pairs (b=c=0). Both arms identical on all paired runs. "
            "Equivalence trivially holds for any delta > 0."
        )
    else:
        # Lower one-sided test: H0: diff <= -delta
        z_lower = (observed - (-delta)) / se
        lower_p = 1.0 - _std_normal_cdf(z_lower)
        # Upper one-sided test: H0: diff >= +delta
        z_upper = (delta - observed) / se
        upper_p = 1.0 - _std_normal_cdf(z_upper)
        interpretation_zero_se = None

    combined_p = max(lower_p, upper_p)
    equivalence_rejected = (lower_p < alpha) and (upper_p < alpha)

    if equivalence_rejected:
        interpretation = (
            f"TOST rejects non-equivalence at alpha={alpha} with delta={delta}. "
            f"Observed diff={observed:.4f} is within [{-delta}, {delta}]. "
            f"Pass rates can be claimed equivalent within delta={delta}."
        )
    else:
        worse_side = "lower" if lower_p >= upper_p else "upper"
        worse_p = combined_p
        interpretation = (
            f"TOST cannot reject non-equivalence (worse side: {worse_side}, "
            f"p={worse_p:.4f} >= alpha={alpha}). Either true difference >= delta={delta}, "
            f"or sample is underpowered to establish equivalence at this delta. "
            f"Recommend: increase n, narrow delta, or report observed_diff without equivalence claim."
        )

    if interpretation_zero_se:
        interpretation = interpretation_zero_se

    return {
        **stats,
        "delta": delta,
        "alpha": alpha,
        "se_mcnemar": se,
        "tost_lower_p": lower_p,
        "tost_upper_p": upper_p,
        "tost_combined_p": combined_p,
        "equivalence_rejected": equivalence_rejected,
        "interpretation": interpretation,
    }


def _std_normal_cdf(z: float) -> float:
    """Standard normal CDF via math.erf."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pf-records", required=True, type=Path, help="PEtFiSh records JSON")
    ap.add_argument("--lc-records", required=True, type=Path, help="LangChain records JSON")
    ap.add_argument("--delta", type=float, default=0.10, help="Equivalence threshold (default 0.10)")
    ap.add_argument("--alpha", type=float, default=0.05, help="Significance level (default 0.05)")
    ap.add_argument("--output", type=Path, required=True, help="Output JSON path")
    args = ap.parse_args()

    pf = load_records(args.pf_records)
    lc = load_records(args.lc_records)
    pairs = pair_records(pf, lc)
    if len(pairs) < 10:
        print(
            f"WARNING: only {len(pairs)} paired runs; TOST result will be weak",
            file=sys.stderr,
        )

    result = tost_paired_binary(pairs, delta=args.delta, alpha=args.alpha)
    result["pf_records_path"] = str(args.pf_records)
    result["lc_records_path"] = str(args.lc_records)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=" * 60)
    print(f"TOST equivalence result: pf vs LangChain (delta={args.delta}, alpha={args.alpha})")
    print("=" * 60)
    print(f"  paired n         : {result['n_paired']}")
    print(f"  pf pass rate     : {result['pf_pass_count']}/{result['n_paired']} = {result['pf_pass_rate']:.4f}")
    print(f"  lc pass rate     : {result['lc_pass_count']}/{result['n_paired']} = {result['lc_pass_rate']:.4f}")
    print(f"  observed diff    : {result['observed_diff']:+.4f}")
    print(f"  discordant (b,c) : ({result['discordant_pf_only']}, {result['discordant_lc_only']})")
    print(f"  SE (McNemar)     : {result['se_mcnemar']:.4f}")
    print(f"  TOST lower p     : {result['tost_lower_p']:.4f}")
    print(f"  TOST upper p     : {result['tost_upper_p']:.4f}")
    print(f"  TOST combined p  : {result['tost_combined_p']:.4f}")
    print(f"  equivalent?      : {'YES' if result['equivalence_rejected'] else 'NO (cannot establish equivalence)'}")
    print()
    print(f"Interpretation: {result['interpretation']}")
    print()
    print(f"Wrote: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
