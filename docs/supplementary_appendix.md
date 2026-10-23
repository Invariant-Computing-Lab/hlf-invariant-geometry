---
title: "Supplementary Appendix: Formal Derivations, Synthetic Protocols, Collision Tests, and Reproducibility"
author: "Emirhan Yıldırım"
date: "12 August 2026"
geometry: margin=1in
fontsize: 10.5pt
---

# S1. Scope

This supplement contains the full mathematical derivations and computational protocol for the manuscript *Invariant-First Reformulation of the Hyper-Lepton Framework*. The supplement validates properties of candidate invariants. It does not provide a physically complete compactification and does not establish the existence of a new lepton sector.

# S2. Source-formulation audit

## S2.1 Simple orbifold versus three-mode domain-wall model

The source technical appendix gives a simple $S^1/Z_2$ parity construction in which only the even chiral component has a constant zero mode. The three-generation mechanism is added later through a two-kink bulk mass profile. Therefore the simple orbifold and the three-localized-mode construction are distinct stages of the source theory.

## S2.2 Convex-hull lemma for the stated Yıldırım production rule

**Lemma S1.** Let $P\subset\mathbb R^n$ be nonempty and convex. Define

$$
Q=\operatorname{Conv}\left(P\times\{-1\}\cup P\times\{0\}\cup P\times\{1\}\right).
$$

Then

$$
Q=P\times[-1,1].
$$

**Proof.** For every $p\in P$,

$$
(p,0)=\frac12(p,-1)+\frac12(p,1),
$$

so $P\times\{0\}$ is already contained in the convex hull of the outer copies. Conversely, convexity of $P$ implies every convex combination of points from $P\times\{-1\}$ and $P\times\{1\}$ has first coordinate in $P$ and last coordinate in $[-1,1]$. Thus the hull is exactly $P\times[-1,1]$. $\square$

This establishes that the stated three-copy convex construction contains no irreducible ternary information.

## S2.3 Euler-characteristic lemma

**Lemma S2.** If $P$ is a convex $d$-polytope, then

$$
\partial P\simeq S^{d-1}.
$$

Therefore

$$
\chi(\partial P)=1+(-1)^{d-1}.
$$

For $d=6$,

$$
\chi(\partial P)=0.
$$

Hence $\chi(\partial Y_6)=0$ cannot distinguish the proposed polytope from generic convex six-polytopes.

# S3. Proposed invariant data

The reformulated datum is

$$
\mathfrak H=(X,E,\rho,\sigma,L_H,h,g).
$$

The main candidate observables are grouped as

$$
\mathfrak I_{\mathrm{HLF}}=
\left[
\mathcal T_{\mathrm{gen}};
\mathcal A_{\mathrm{alg}};
\mathcal C_{\mathrm{gauge}};
\Pi_M;
\mathcal S_D;
\mathcal D
\right].
$$

The grouping is intentionally heterogeneous: topology, algebraic moduli, operator-orbit coordinates, spectra, and discriminants do not carry the same kind of information.

# S4. Index and cohomological counting

Define

$$
I_{\mathrm{gen}}=\chi(X,E)=\sum_q(-1)^qh^q(X,E).
$$

An adjacent pair addition

$$
(h^q,h^{q+1})\mapsto(h^q+k,h^{q+1}+k)
$$

changes the index by

$$
(-1)^qk+(-1)^{q+1}k=0.
$$

This is the synthetic positive control.

A one-degree perturbation

$$
h^q\mapsto h^q+k
$$

changes the index by

$$
\Delta I=(-1)^qk,
$$

which is the negative control.

## S4.1 Monte Carlo result

With seed 20260812:

- admissible pair additions: 20,000/20,000 preserved the index;
- single-degree changes: 20,000/20,000 changed the index.

For $n=20{,}000$ all-success trials, the exact two-sided 95% lower bound is approximately 0.999816.

## S4.2 Collision enumeration

The exact bounded set

$$
\mathcal H_{12}=
\{h\in\{0,\ldots,12\}^4:h^0-h^1+h^2-h^3=3\}
$$

contains

$$
|\mathcal H_{12}|=1364.
$$

Thus the map

$$
h\mapsto I_{\mathrm{gen}}
$$

is highly many-to-one. Adding total mode count does not make it injective; the largest multiplicity of a shared $(I_{\mathrm{gen}},N_{\mathrm{total}})$ pair in the enumerated domain is 132.

# S5. Concrete $\mathbb P^3$ index sanity check

For

$$
\chi(\mathbb P^3,\mathcal O(k))
=\frac{(k+1)(k+2)(k+3)}{6},
$$

rank-three split bundles in degree range $[-8,8]$ with Euler characteristic three include

$$
(-4,-3,1),\quad(-4,-2,1),\quad(-4,-1,1),\quad(0,0,0).
$$

This is a deliberately elementary algebraic benchmark. It proves existence of multiple split-bundle data with the same integer target, not a realistic lepton compactification.

# S6. Hilbert-polynomial collision analysis

For

$$
E=\bigoplus_{i=1}^4\mathcal O(a_i),
$$

$$
P_E(m)=\sum_i\frac{(m+a_i+1)(m+a_i+2)(m+a_i+3)}{6}.
$$

Expanding gives

$$
P_E(m)
=\frac{r}{6}m^3
+\frac{3p_1+6r}{6}m^2
+\frac{3p_2+12p_1+11r}{6}m
+\frac{p_3+6p_2+11p_1+6r}{6},
$$

where

$$
p_j=\sum_i a_i^j,
$$

and here $r=4$.

Therefore the Hilbert polynomial determines $(r,p_1,p_2,p_3)$, but does not generically determine $p_4$.

## S6.1 Exact enumeration

The sorted degree multisets

$$
-6\le a_1\le a_2\le a_3\le a_4\le6
$$

number 1,820.

Results:

- unique Hilbert polynomials: 1,809;
- collision groups: 11;
- bundles in collision groups: 22;
- maximum collision multiplicity: 2.

Example:

$$
A=(-6,-3,-2,1),
$$

$$
B=(-5,-5,0,0).
$$

Both have

$$
(p_1,p_2,p_3)=(-10,50,-250)
$$

and

$$
P_A=P_B=\frac23m^3-m^2+\frac{37}{3}m-6,
$$

but

$$
p_4(A)=1394,
$$

$$
p_4(B)=1250.
$$

The complete collision table is provided in `data/hilbert_collisions.csv`.

# S7. Why $p_4$ completes the rank-four split degree multiset

Newton identities relate power sums $p_k$ and elementary symmetric polynomials $e_k$:

$$
e_1=p_1,
$$

$$
2e_2=e_1p_1-p_2,
$$

$$
3e_3=e_2p_1-e_1p_2+p_3,
$$

$$
4e_4=e_3p_1-e_2p_2+e_1p_3-p_4.
$$

Thus $(p_1,p_2,p_3,p_4)$ determines $(e_1,e_2,e_3,e_4)$ and therefore determines the monic polynomial

$$
\prod_{i=1}^4(t-a_i)
=t^4-e_1t^3+e_2t^2-e_3t+e_4.
$$

The multiset $\{a_1,a_2,a_3,a_4\}$ is its root multiset. Hence, for rank-four split degree data,

$$
\boxed{(P_E,p_4)}
$$

is complete up to summand permutation. The enumeration returned zero collisions after this augmentation.

# S8. Gauge-orbit invariants

For Hermitian $C$ define

$$
H=C-\frac{\operatorname{Tr}C}{3}I.
$$

Under unitary conjugation,

$$
H\mapsto U^\dagger H U,
$$

and therefore

$$
q_2=\operatorname{Tr}H^2,
\qquad
q_3=\operatorname{Tr}H^3
$$

are invariant.

For a traceless $3\times3$ matrix, Newton identities give

$$
\det(tI-H)=t^3-\frac{q_2}{2}t-\frac{q_3}{3}.
$$

Thus $(q_2,q_3)$ reconstructs the eigenvalue orbit.

## S8.1 Numerical results

Across 20,000 random Hermitian matrices and independent Haar-unitary transforms:

- median preservation error: $4.30\times10^{-16}$;
- maximum preservation error: $3.46\times10^{-15}$;
- median reconstruction error: $4.63\times10^{-16}$;
- maximum reconstruction error: $2.75\times10^{-15}$.

## S8.2 $q_2$ collision

$$
H_1=\operatorname{diag}(1,-1,0),
$$

$$
H_2=\operatorname{diag}(1/\sqrt3,1/\sqrt3,-2/\sqrt3).
$$

Then

$$
q_2(H_1)=q_2(H_2)=2,
$$

while

$$
q_3(H_1)=0,
$$

$$
q_3(H_2)=-\frac{2}{\sqrt3}\approx-1.1547.
$$

Hence $q_2$ is a universality-distance statistic, not a full non-universal orbit identifier.

## S8.3 Perturbation law

For

$$
C_\epsilon=I+\epsilon H,
$$

with $H$ traceless and $\|H\|_F=1$,

$$
q_2=\epsilon^2.
$$

The numerical fit returns slope $2.000000000005$ and $R^2=1.0$.

# S9. Mass quotient and exact reconstruction

Let singular values be $m_i\ge0$ and define

$$
x_i=m_i^2,
$$

$$
s_1=x_1+x_2+x_3,
$$

$$
s_2=x_1x_2+x_1x_3+x_2x_3,
$$

$$
s_3=x_1x_2x_3.
$$

Normalize:

$$
\widehat s_2=s_2/s_1^2,
$$

$$
\widehat s_3=s_3/s_1^3.
$$

Writing

$$
y_i=x_i/s_1
$$

gives

$$
y_1+y_2+y_3=1,
$$

and Vieta's formulas yield

$$
z^3-z^2+\widehat s_2z-\widehat s_3=0.
$$

Therefore the normalized squared singular-value multiset is determined exactly by $(\widehat s_2,\widehat s_3)$.

## S9.1 Numerical results

For 20,000 log-uniform spectra over six orders of magnitude, transformed by random $U(3)_L\times U(3)_R$ and $c\in[10^{-6},10^6]$:

- median preservation error: $9.23\times10^{-16}$;
- maximum preservation error: $4.86\times10^{-11}$;
- median reconstruction error: $3.33\times10^{-16}$;
- 95th percentile: $1.23\times10^{-15}$;
- maximum reconstruction error: $5.71\times10^{-12}$;
- reconstruction failures $>10^{-8}$: 0/20,000.

# S10. Mass perturbation and discriminant

For a baseline mass matrix $M_0$ and complex perturbation $\Delta M$ satisfying

$$
\|\Delta M\|_F/\|M_0\|_F=\delta,
$$

the small-noise log-log fit gave

$$
D_M\propto\delta^{0.99579},
$$

$$
R^2=0.999882.
$$

The normalized discriminant

$$
\Delta_M=\prod_{i<j}(y_i-y_j)^2
$$

was tested along

$$
(1,1+\epsilon,4)
$$

followed by normalization. The fitted vanishing law was

$$
\Delta_M\propto\epsilon^{1.99350},
$$

$$
R^2=0.999984.
$$

# S11. Normalized spectral test

For positive finite spectra

$$
0<\lambda_1\le\cdots\le\lambda_K,
$$

define

$$
I_{\mathrm{spec}}=(\lambda_2/\lambda_1,\ldots,\lambda_K/\lambda_1).
$$

Under

$$
D\mapsto aUDU^\dagger,
$$

the complete finite normalized spectrum is invariant.

Across 20,000 random eight-level spectra:

- median preservation error: $3.97\times10^{-14}$;
- maximum preservation error: $1.93\times10^{-12}$.

Under non-admissible Hermitian perturbations, small-noise displacement obeyed

$$
D_{\mathrm{spec}}\propto\eta^{0.99539},
$$

$$
R^2=0.999923.
$$

A truncated spectral window is non-reconstructive. For example,

$$
(1,2,3,4,5,6)
$$

and

$$
(1,2,3,4,9,12)
$$

share the first ratios $(2,3,4)$.

The supplement deliberately does not infer geometry from a full spectrum: isospectral non-isometric manifolds are a known obstruction to that inference.

# S12. Invariant-strength table

| Quantity | Class | Quotient-invariant? | Reconstructive? | Role |
|---|---|---:|---:|---|
| domain-wall positions, raw Higgs-profile parameters | $I_0$ | no | no | benchmark realization only |
| raw mass-matrix entries | $I_0$ | no | no | representation data |
| raw KK masses under scale quotient | $I_0/I_1$ | no | no | replace by normalized spectrum |
| chiral index | $I_2$ | yes | no | necessary topology gate |
| Hilbert polynomial | $I_1$ structural | yes | no | coarse algebraic fingerprint |
| $(P_E,p_4)$, rank-4 split $\mathbb P^3$ | restricted complete | yes | yes | split-degree multiset |
| $q_2$ | $I_1$ | yes | no | distance from LFU locus |
| $(q_2,q_3)$ | $I_1$ | yes | yes, finite Hermitian orbit | gauge spectral fingerprint |
| $(\widehat s_2,\widehat s_3)$ | $I_1$ | yes | yes, 3-level normalized spectrum | core mass invariant |
| normalized full finite spectrum | $I_1$ | yes | yes, finite Hermitian orbit | spectral fingerprint |
| $\Delta_M=0$ | $I_3$ | yes | stratum marker | spectral-degeneracy boundary |

# S13. Reproducibility protocol

The package layout is:

```
HLF_Invariant_Q1_Submission_Package/
  code/
    final_experiment.py
    requirements.txt
  data/
    final_results.json
    final_experiment_summary.csv
    gauge_sensitivity.csv
    mass_sensitivity.csv
    mass_discriminant.csv
    spectral_sensitivity.csv
    hilbert_collisions.csv
    results_macros.tex
  figures/
    fig_gauge_sensitivity.png
    fig_mass_sensitivity.png
    fig_mass_discriminant.png
    fig_spectral_sensitivity.png
  docs/
    Main_Manuscript.docx/pdf
    Supplementary_Appendix.docx/pdf
  README.md
  CITATION.cff
  SHA256SUMS.txt
```

Reference execution:

```bash
python code/final_experiment.py --out . --n-mc 20000
```

Software used for the archived run:

- Python 3
- NumPy 2.3.5
- pandas 2.2.3
- Matplotlib 3.10.8

No external datasets are required.

# S14. Recommended next-stage experiment

A physically meaningful Phase II must replace the synthetic cohomology and matrix sectors with explicit compactification data. At minimum it should construct $(X,E,\sigma)$ and calculate:

1. $\operatorname{Ind}(D_E|_{\mathrm{phys}})$ or the appropriate equivariant index;
2. actual $H^q(X,E)$ dimensions and mirror/vector-like content;
3. Chern classes, stability, and consistency constraints;
4. the Higgs/Yukawa cohomological pairing;
5. $(\widehat s_2,\widehat s_3)$ implied by that pairing;
6. the Dirac/KK spectrum or controlled numerical approximation;
7. experimental bounds on any predicted vector-like states.

A synthetic success should not be promoted to a physical claim until these stages are passed.
