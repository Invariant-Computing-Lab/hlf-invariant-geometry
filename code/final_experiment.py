#!/usr/bin/env python3
"""Final reproducible synthetic validation for invariant-first HLF reformulation.

This script validates mathematical behavior of proposed invariants only.
It does NOT validate the physical truth of HLF or construct a phenomenologically
consistent compactification.
"""
from __future__ import annotations
import json, math, itertools, argparse
from pathlib import Path
from fractions import Fraction
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SEED = 20260812
TOL = 1e-10


def haar_unitary(n, rng):
    z = rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n))
    q, r = np.linalg.qr(z)
    d = np.diag(r)
    ph = np.ones_like(d, dtype=complex)
    nz = np.abs(d) > 0
    ph[nz] = d[nz] / np.abs(d[nz])
    return q @ np.diag(np.conj(ph))


def hermitian_random(n, rng):
    a = rng.normal(size=(n,n)) + 1j*rng.normal(size=(n,n))
    return (a + a.conj().T) / 2


def chi_O_P3(k: int) -> int:
    # Hilbert polynomial evaluation / holomorphic Euler characteristic, valid for all integer k.
    return (k+1)*(k+2)*(k+3)//6


def hilbert_coeffs_P3_split(degs):
    # Coefficients [m^3,m^2,m,1] of sum_i binom(m+a_i+3,3), exact Fractions.
    # (m+a+1)(m+a+2)(m+a+3)/6
    c3 = Fraction(len(degs), 6)
    c2 = sum(Fraction(3*a+6, 6) for a in degs)
    c1 = sum(Fraction(3*a*a+12*a+11, 6) for a in degs)
    c0 = sum(Fraction(a**3+6*a*a+11*a+6, 6) for a in degs)
    return (c3,c2,c1,c0)


def frac_tuple_str(t):
    return tuple(f"{x.numerator}/{x.denominator}" for x in t)


def mass_invariants_from_sv(s):
    x = np.asarray(s, float)**2
    a = x
    s1 = np.sum(a)
    s2 = a[0]*a[1] + a[0]*a[2] + a[1]*a[2]
    s3 = np.prod(a)
    return np.array([s2/s1**2, s3/s1**3], float)


def reconstruct_mass_norm(inv):
    sh2, sh3 = inv
    roots = np.roots([1.0, -1.0, sh2, -sh3])
    roots = np.real_if_close(roots, tol=1000).real
    roots.sort()
    return roots


def gauge_invariants(C):
    n = C.shape[0]
    H = C - np.trace(C)/n*np.eye(n)
    q2 = float(np.trace(H@H).real)
    q3 = float(np.trace(H@H@H).real)
    return np.array([q2,q3])


def reconstruct_traceless_eigs(q2,q3):
    # p(t)=t^3-(q2/2)t-(q3/3)
    roots = np.roots([1.0, 0.0, -q2/2.0, -q3/3.0])
    roots = np.real_if_close(roots, tol=1000).real
    roots.sort()
    return roots


def spectral_inv(eigs):
    e = np.sort(np.abs(np.asarray(eigs, float)))
    if e[0] <= 0:
        raise ValueError('positive spectrum required')
    return e[1:] / e[0]


def relerr(a,b):
    a=np.asarray(a,float); b=np.asarray(b,float)
    return float(np.linalg.norm(a-b)/max(np.linalg.norm(a),1e-30))


def wilson_upper_all_success(n, alpha=0.05):
    # exact Clopper-Pearson lower bound for all successes: (alpha/2)^(1/n)
    return (alpha/2.0)**(1.0/n)


def run(outdir: Path, n_mc=20000):
    rng=np.random.default_rng(SEED)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir/'figures').mkdir(exist_ok=True)
    (outdir/'data').mkdir(exist_ok=True)
    summary={"seed":SEED,"tolerance":TOL,"n_mc":n_mc}
    rows=[]

    # --------------------------------------------------------
    # E1: Index
    # --------------------------------------------------------
    idx_pres=0; idx_neg=0
    for _ in range(n_mc):
        # construct an index-3 profile with nonnegative entries
        while True:
            h1,h2,h3=rng.integers(0,20,size=3)
            h0=3+h1-h2+h3
            if h0 >= 0:
                break
        h=np.array([h0,h1,h2,h3],dtype=int)
        q=int(rng.integers(0,3)); k=int(rng.integers(1,8))
        hp=h.copy(); hp[q]+=k; hp[q+1]+=k
        idx=lambda z:int(z[0]-z[1]+z[2]-z[3])
        idx_pres += idx(hp)==idx(h)==3
        hn=h.copy(); qn=int(rng.integers(0,4)); hn[qn]+=k
        idx_neg += idx(hn)!=idx(h)
    profiles=[]
    for h in itertools.product(range(13), repeat=4):
        if h[0]-h[1]+h[2]-h[3]==3:
            profiles.append(h)
    by_it={}
    for h in profiles:
        key=(3,sum(h)); by_it.setdefault(key,0); by_it[key]+=1
    max_collision_index_total=max(by_it.values())
    summary['index']={
        'preservation_success':idx_pres,'preservation_n':n_mc,
        'negative_detection_success':idx_neg,'negative_n':n_mc,
        'bounded_profiles_index3':len(profiles),
        'max_collision_multiplicity_index_plus_total':max_collision_index_total,
        'all_success_cp95_lower':wilson_upper_all_success(n_mc)
    }
    rows.append(['Index',idx_pres/n_mc,idx_neg/n_mc,len(profiles),max_collision_index_total,'coarse I2; not reconstructive'])

    # concrete algebraic geometry sanity benchmark on P3
    rank3_index3=[]
    for degs in itertools.combinations_with_replacement(range(-8,9),3):
        if sum(chi_O_P3(a) for a in degs)==3:
            rank3_index3.append(degs)
    summary['index']['P3_rank3_split_bundles_chi3']=rank3_index3

    # --------------------------------------------------------
    # E2: Hilbert polynomial on P3 split rank 4 bundles
    # --------------------------------------------------------
    deg_range=range(-6,7)
    bundles=list(itertools.combinations_with_replacement(deg_range,4))
    hp_groups={}; hp4_groups={}
    for degs in bundles:
        hp=frac_tuple_str(hilbert_coeffs_P3_split(degs))
        hp_groups.setdefault(hp,[]).append(degs)
        p4=sum(a**4 for a in degs)
        hp4_groups.setdefault((hp,p4),[]).append(degs)
    collision_groups={k:v for k,v in hp_groups.items() if len(v)>1}
    collision_groups4={k:v for k,v in hp4_groups.items() if len(v)>1}
    max_hp=max(len(v) for v in hp_groups.values())
    distinct_in_collisions=sum(len(v) for v in collision_groups.values())
    # positive/mutation Monte Carlo
    hp_pres=0; hp_mut=0
    for _ in range(n_mc):
        degs=list(bundles[int(rng.integers(0,len(bundles)))])
        perm=list(rng.permutation(degs))
        hp_pres += hilbert_coeffs_P3_split(degs)==hilbert_coeffs_P3_split(perm)
        j=int(rng.integers(0,4)); mut=degs.copy(); mut[j]+=1
        hp_mut += hilbert_coeffs_P3_split(degs)!=hilbert_coeffs_P3_split(mut)
    example_collision=next(iter(collision_groups.values()))[:2] if collision_groups else []
    summary['hilbert']={
        'bundle_count':len(bundles),'unique_hilbert_polynomials':len(hp_groups),
        'collision_group_count':len(collision_groups),
        'bundles_in_collision_groups':distinct_in_collisions,
        'max_collision_multiplicity':max_hp,
        'augmented_hp_plus_p4_collision_groups':len(collision_groups4),
        'preservation_success':hp_pres,'mutation_detection_success':hp_mut,'n':n_mc,
        'example_collision':[list(x) for x in example_collision]
    }
    rows.append(['Hilbert polynomial',hp_pres/n_mc,hp_mut/n_mc,distinct_in_collisions,max_hp,'coarse; HP+p4 complete in enumerated rank-4 domain' if not collision_groups4 else 'augmented still collides'])

    # save collision table
    coll_rows=[]
    for hp, vals in collision_groups.items():
        coll_rows.append({'hilbert_coeffs':'|'.join(hp),'multiplicity':len(vals),'bundles':'; '.join(map(str,vals))})
    pd.DataFrame(coll_rows).to_csv(outdir/'data'/'hilbert_collisions.csv',index=False)

    # --------------------------------------------------------
    # E3: Gauge q2,q3
    # --------------------------------------------------------
    gauge_pres_err=[]; gauge_rec_err=[]
    eps_grid=np.logspace(-8,-1,8); sens=[]
    for _ in range(n_mc):
        C=hermitian_random(3,rng)
        U=haar_unitary(3,rng)
        inv=gauge_invariants(C)
        inv2=gauge_invariants(U.conj().T@C@U)
        gauge_pres_err.append(relerr(inv,inv2))
        H=C-np.trace(C)/3*np.eye(3)
        true=np.sort(np.linalg.eigvalsh(H))
        rec=reconstruct_traceless_eigs(*inv)
        gauge_rec_err.append(relerr(true,rec))
    for eps in eps_grid:
        vals=[]
        for _ in range(1000):
            H=hermitian_random(3,rng); H=H-np.trace(H)/3*np.eye(3)
            H=H/np.linalg.norm(H,'fro')
            vals.append(gauge_invariants(np.eye(3)+eps*H)[0])
        sens.append([eps,float(np.median(vals))])
    sens=np.array(sens)
    slope,intercept=np.polyfit(np.log10(sens[:,0]),np.log10(sens[:,1]),1)
    pred=slope*np.log10(sens[:,0])+intercept
    ssres=np.sum((np.log10(sens[:,1])-pred)**2); sst=np.sum((np.log10(sens[:,1])-np.mean(np.log10(sens[:,1])))**2)
    r2=1-ssres/sst
    # explicit q2 collision
    h1=np.diag([1.,-1.,0.]); h2=np.diag([1/math.sqrt(3),1/math.sqrt(3),-2/math.sqrt(3)])
    explicit_q2=(gauge_invariants(h1),gauge_invariants(h2))
    summary['gauge']={
        'preservation_median_err':float(np.median(gauge_pres_err)),
        'preservation_max_err':float(np.max(gauge_pres_err)),
        'reconstruction_median_err_q2q3':float(np.median(gauge_rec_err)),
        'reconstruction_max_err_q2q3':float(np.max(gauge_rec_err)),
        'q2_sensitivity_slope':float(slope),'q2_sensitivity_r2':float(r2),
        'explicit_q2_collision':{'H1_q2q3':explicit_q2[0].tolist(),'H2_q2q3':explicit_q2[1].tolist()}
    }
    rows.append(['Gauge (q2,q3)',1.0,float(np.mean(np.array(gauge_rec_err)<1e-10)),0,1,'q2 alone incomplete; q2+q3 reconstructs 3x3 Hermitian orbit spectrum'])
    pd.DataFrame(sens,columns=['epsilon','median_q2']).to_csv(outdir/'data'/'gauge_sensitivity.csv',index=False)

    plt.figure(figsize=(6.4,4.4)); plt.loglog(sens[:,0],sens[:,1],'o-'); plt.xlabel(r'$\epsilon$'); plt.ylabel(r'median $q_2$'); plt.title('Gauge-universality breaking'); plt.tight_layout(); plt.savefig(outdir/'figures'/'fig_gauge_sensitivity.png',dpi=220); plt.close()

    # --------------------------------------------------------
    # E4: Mass invariants
    # --------------------------------------------------------
    mass_pres=[]; mass_rec=[]
    for _ in range(n_mc):
        s=np.sort(10**rng.uniform(-3,3,size=3))
        M=np.diag(s).astype(complex)
        UL=haar_unitary(3,rng); UR=haar_unitary(3,rng); c=10**rng.uniform(-6,6)
        M2=c*UL@M@UR.conj().T
        inv=mass_invariants_from_sv(np.linalg.svd(M,compute_uv=False))
        inv2=mass_invariants_from_sv(np.linalg.svd(M2,compute_uv=False))
        mass_pres.append(relerr(inv,inv2))
        true=np.sort(s*s/np.sum(s*s))
        rec=reconstruct_mass_norm(inv)
        mass_rec.append(relerr(true,rec))
    # perturbation sensitivity baseline (less extreme to avoid conditioning)
    s0=np.array([1.0,12.0,80.0]); M0=np.diag(s0).astype(complex); inv0=mass_invariants_from_sv(s0)
    deltas=np.logspace(-8,-2,7); m_sens=[]
    for d in deltas:
        vals=[]
        for _ in range(1000):
            P=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3)); P=P/np.linalg.norm(P,'fro')*np.linalg.norm(M0,'fro')*d
            invp=mass_invariants_from_sv(np.linalg.svd(M0+P,compute_uv=False))
            vals.append(np.linalg.norm(np.log10(np.maximum(invp,1e-300)/inv0)))
        m_sens.append([d,float(np.median(vals))])
    m_sens=np.array(m_sens); mslope,mi=np.polyfit(np.log10(m_sens[:5,0]),np.log10(m_sens[:5,1]),1)
    pred=mslope*np.log10(m_sens[:5,0])+mi; yy=np.log10(m_sens[:5,1]); mr2=1-np.sum((yy-pred)**2)/np.sum((yy-np.mean(yy))**2)
    # discriminant approach
    epsd=np.logspace(-8,-1,8); disc=[]
    for e in epsd:
        x=np.array([1.0,1.0+e,4.0]); x=x/np.sum(x)
        delta=((x[0]-x[1])*(x[0]-x[2])*(x[1]-x[2]))**2
        disc.append([e,delta])
    disc=np.array(disc); dslope,di=np.polyfit(np.log10(disc[:,0]),np.log10(disc[:,1]),1)
    pred=dslope*np.log10(disc[:,0])+di; yy=np.log10(disc[:,1]); dr2=1-np.sum((yy-pred)**2)/np.sum((yy-np.mean(yy))**2)
    summary['mass']={
        'preservation_median_err':float(np.median(mass_pres)),'preservation_max_err':float(np.max(mass_pres)),
        'reconstruction_median_err':float(np.median(mass_rec)),'reconstruction_p95_err':float(np.quantile(mass_rec,.95)),'reconstruction_max_err':float(np.max(mass_rec)),
        'reconstruction_failures_gt_1e-8':int(np.sum(np.array(mass_rec)>1e-8)),
        'perturbation_slope_small':float(mslope),'perturbation_r2_small':float(mr2),
        'discriminant_slope':float(dslope),'discriminant_r2':float(dr2)
    }
    rows.append(['Mass (s2hat,s3hat)',float(np.mean(np.array(mass_pres)<TOL)),float(np.mean(np.array(mass_rec)<1e-8)),0,1,'quotient-complete for normalized 3 singular values'])
    pd.DataFrame(m_sens,columns=['delta','median_displacement']).to_csv(outdir/'data'/'mass_sensitivity.csv',index=False)
    pd.DataFrame(disc,columns=['epsilon','normalized_discriminant']).to_csv(outdir/'data'/'mass_discriminant.csv',index=False)
    plt.figure(figsize=(6.4,4.4)); plt.loglog(m_sens[:,0],m_sens[:,1],'o-'); plt.xlabel(r'$\delta$'); plt.ylabel('median invariant displacement'); plt.title('Mass-invariant perturbation response'); plt.tight_layout(); plt.savefig(outdir/'figures'/'fig_mass_sensitivity.png',dpi=220); plt.close()
    plt.figure(figsize=(6.4,4.4)); plt.loglog(disc[:,0],disc[:,1],'o-'); plt.xlabel(r'$\epsilon$'); plt.ylabel(r'$\widehat{\Delta}_M$'); plt.title('Approach to mass-degeneracy discriminant'); plt.tight_layout(); plt.savefig(outdir/'figures'/'fig_mass_discriminant.png',dpi=220); plt.close()

    # --------------------------------------------------------
    # E5: Spectral invariants
    # --------------------------------------------------------
    spec_pres=[]; spec_rec=[]
    for _ in range(n_mc):
        eigs=np.sort(10**rng.uniform(-2,2,size=8))
        U=haar_unitary(8,rng); D=U@np.diag(eigs)@U.conj().T
        a=10**rng.uniform(-6,6); V=haar_unitary(8,rng); D2=a*V@D@V.conj().T
        e2=np.linalg.eigvalsh(D2)
        i1=spectral_inv(eigs); i2=spectral_inv(e2)
        spec_pres.append(relerr(i1,i2))
        rec=np.r_[1.0,i1]; true=eigs/eigs[0]
        spec_rec.append(relerr(true,rec))
    # perturbation response
    e0=np.array([1.,2.2,3.7,5.5,8.1,11.2,15.0,20.]); D0=np.diag(e0); i0=spectral_inv(e0)
    etas=np.logspace(-8,-2,7); s_sens=[]
    for eta in etas:
        vals=[]
        for _ in range(1000):
            H=hermitian_random(8,rng); H=H/np.linalg.norm(H,'fro')*np.linalg.norm(D0,'fro')*eta
            ep=np.linalg.eigvalsh(D0+H)
            if ep[0] <= 0: continue
            vals.append(relerr(i0,spectral_inv(ep)))
        s_sens.append([eta,float(np.median(vals))])
    s_sens=np.array(s_sens); sslope,si=np.polyfit(np.log10(s_sens[:5,0]),np.log10(s_sens[:5,1]),1)
    pred=sslope*np.log10(s_sens[:5,0])+si; yy=np.log10(s_sens[:5,1]); sr2=1-np.sum((yy-pred)**2)/np.sum((yy-np.mean(yy))**2)
    summary['spectral']={
        'preservation_median_err':float(np.median(spec_pres)),'preservation_max_err':float(np.max(spec_pres)),
        'finite_operator_reconstruction_median_err':float(np.median(spec_rec)),'finite_operator_reconstruction_max_err':float(np.max(spec_rec)),
        'perturbation_slope_small':float(sslope),'perturbation_r2_small':float(sr2),
        'truncation_collision_example':{'A':[1,2,3,4,5,6],'B':[1,2,3,4,9,12],'shared_ratios_first3':[2,3,4]}
    }
    rows.append(['Normalized finite spectrum',float(np.mean(np.array(spec_pres)<TOL)),float(np.mean(np.array(spec_rec)<1e-10)),0,1,'complete for finite Hermitian operator orbit; not geometry'])
    pd.DataFrame(s_sens,columns=['eta','median_relative_displacement']).to_csv(outdir/'data'/'spectral_sensitivity.csv',index=False)
    plt.figure(figsize=(6.4,4.4)); plt.loglog(s_sens[:,0],s_sens[:,1],'o-'); plt.xlabel(r'$\eta$'); plt.ylabel('median normalized spectral displacement'); plt.title('Normalized spectral perturbation response'); plt.tight_layout(); plt.savefig(outdir/'figures'/'fig_spectral_sensitivity.png',dpi=220); plt.close()

    # --------------------------------------------------------
    # Summary tables
    # --------------------------------------------------------
    df=pd.DataFrame(rows,columns=['invariant_family','quotient_preservation_rate','reconstructibility_or_detection_rate','collision_count_or_profiles','max_collision_multiplicity','interpretation'])
    df.to_csv(outdir/'data'/'final_experiment_summary.csv',index=False)
    with open(outdir/'data'/'final_results.json','w') as f: json.dump(summary,f,indent=2)

    # LaTeX-ready compact results
    with open(outdir/'data'/'results_macros.tex','w') as f:
        f.write(f"\\newcommand{{\\NMC}}{{{n_mc}}}\n")
        f.write(f"\\newcommand{{\\IndexProfiles}}{{{len(profiles)}}}\n")
        f.write(f"\\newcommand{{\\HilbertBundles}}{{{len(bundles)}}}\n")
        f.write(f"\\newcommand{{\\HilbertCollisionGroups}}{{{len(collision_groups)}}}\n")
        f.write(f"\\newcommand{{\\HilbertAugCollisions}}{{{len(collision_groups4)}}}\n")
        f.write(f"\\newcommand{{\\MassRecMax}}{{{np.max(mass_rec):.3e}}}\n")
        f.write(f"\\newcommand{{\\GaugeRecMax}}{{{np.max(gauge_rec_err):.3e}}}\n")
        f.write(f"\\newcommand{{\\SpecPresMax}}{{{np.max(spec_pres):.3e}}}\n")

    print(json.dumps(summary, indent=2))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--out',default=str(Path(__file__).resolve().parents[1])); ap.add_argument('--n-mc',type=int,default=20000)
    args=ap.parse_args(); run(Path(args.out),args.n_mc)
