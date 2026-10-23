# HLF Invariant-First Reproducibility Package

This package accompanies the manuscript **Invariant-First Reformulation of the Hyper-Lepton Framework: Quotient Geometry, Reconstructibility, and Synthetic Falsification of Candidate Lepton-Generation Invariants**.

## What this package establishes

It tests the **mathematical behavior** of proposed invariant observables: quotient preservation, selectivity, collision resistance, reconstructibility, and discriminant behavior.

It does **not** establish the physical validity of the Hyper-Lepton Framework, a realistic compactification, new particles, or a three-generation mechanism in nature.

## Reproduce the final experiment

From the package root:

```bash
python code/final_experiment.py --out . --n-mc 20000
```

The archived run uses deterministic seed `20260812` and preservation tolerance `1e-10`.

## Environment

- Python 3
- NumPy 2.3.5
- pandas 2.2.3
- Matplotlib 3.10.8

Install dependencies with:

```bash
pip install -r code/requirements.txt
```

## Key archived results

- Index positive controls: 20,000/20,000 preserved.
- Index negative controls: 20,000/20,000 detected.
- Bounded cohomology profiles with index 3: 1,364.
- Rank-4 split bundles on P3 tested: 1,820.
- Hilbert-polynomial collision groups: 11.
- Collisions after adding fourth power sum p4: 0 in the enumerated domain; for rank four the completion follows from Newton identities.
- Gauge `(q2,q3)` maximum eigenvalue reconstruction error: `2.75e-15`.
- Mass invariant maximum normalized-spectrum reconstruction error: `5.71e-12`; no failure above `1e-8` in 20,000 trials.
- Normalized finite-spectrum maximum quotient-preservation error: `1.93e-12`.

## Submission note

The scientific documents are formatted as a journal-style manuscript and supplementary appendix. Journal-specific cover letter, declarations, funding statement, competing-interest statement, and target-journal formatting should be completed once a journal is selected.
