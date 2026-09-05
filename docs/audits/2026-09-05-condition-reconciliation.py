"""Reconcile saved prompt conditions without editing originals or running models.

This re-evaluates existing binding results; it is NOT a token-count sensitivity.
Uniform coverage is incomplete and no 12-model substitute for the registered
13-model aggregate is calculated. Outputs are restricted to this audit directory.
"""
from pathlib import Path
import hashlib, json, math
import numpy as np
import pandas as pd
import yaml
from scipy.stats import rankdata, spearmanr
ROOT=Path.cwd(); OUT=ROOT/'docs/audits'; PREFIX='2026-09-05-condition-reconciliation'
SEED=20260813
cases={x['name']:x for x in yaml.safe_load((ROOT/'data/binding/accessibility.yaml').read_text())['compounds']}
f=pd.read_csv(ROOT/'results/frequency/frequency_table.csv')[['compound','bigram_count']].drop_duplicates()
assert len(f)==49
mapping=[]; groups={}
for p in sorted((ROOT/'results/effective_binding').glob('*/*/*/*-accessibility.csv')):
 d=pd.read_csv(p); meta=d[['compound','prompt']].drop_duplicates()
 assert len(meta)==53
 is_n=all(r.prompt==cases[r.compound]['prompt'] for r in meta.itertuples())
 is_u=all(r.prompt==f"A {cases[r.compound]['word1']} {cases[r.compound]['word2']} is" for r in meta.itertuples())
 assert is_n != is_u,p
 actual='natural' if is_n else 'uniform'; family=d.family.iloc[0]; model=d.model.iloc[0]
 key=(family,model,actual); duplicate=key in groups
 if duplicate:
  old=groups[key]; cols=[c for c in d if c!='prompt_condition'];assert d[cols].equals(old[cols])
 else:groups[key]=d
 mapping.append(dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),family=family,model=model,label=p.parent.name,actual_prompt_condition=actual,duplicate_measurements=duplicate))
rows=[]; summaries=[]
for (family,model,condition),d in sorted(groups.items()):
 layers=int(d.layer.max())+1;late=d[d.layer>=math.ceil(2*layers/3)]
 s=late.groupby('compound').relative_weighted_ov_norm.quantile(.95).rename('p95_relative').reset_index().merge(f,on='compound',validate='one_to_one').sort_values('compound')
 assert len(s)==49
 x=np.log1p(s.bigram_count.to_numpy());y=s.p95_relative.to_numpy()
 rho=spearmanr(x,y).statistic;rng=np.random.default_rng(SEED);boot=[]
 for _ in range(2000):
  idx=rng.integers(0,49,49);r=spearmanr(x[idx],y[idx]).statistic
  if np.isfinite(r):boot.append(r)
 lo,hi=np.quantile(boot,[.025,.975]);rows.append(dict(family=family,model=model,actual_prompt_condition=condition,measure='p95_relative',n_compounds=49,rho=rho,ci_low=lo,ci_high=hi))
 s=s.assign(family=family,model=model,condition=condition,log_frequency=x);summaries.append(s)
cor=pd.DataFrame(rows);summary=pd.concat(summaries,ignore_index=True)
# Rank-product evaluation of the exact registered shared-label permutation test.
# First verify against the original saved natural result, then apply condition reconciliation.
def aggregate(s):
 order=sorted(s.compound.unique());x=s.drop_duplicates('compound').set_index('compound').loc[order,'log_frequency'].to_numpy()
 ys=np.column_stack([g.set_index('compound').loc[order,'p95_relative'].to_numpy() for _,g in s.groupby(['family','model'],sort=True)])
 assert ys.shape==(49,13)
 xr=rankdata(x);xr-=xr.mean();yr=rankdata(ys,axis=0);yr-=yr.mean(axis=0)
 denom=np.sqrt((xr*xr).sum()*(yr*yr).sum(axis=0));r=xr@yr/denom
 for j in range(13):np.testing.assert_allclose(r[j],spearmanr(x,ys[:,j]).statistic,atol=1e-14)
 obs=float(np.arctanh(r).mean());rng=np.random.default_rng(SEED);extreme=0
 for _ in range(10000):
  z=float(np.arctanh(rng.permutation(xr)@yr/denom).mean());extreme+=z<=obs
 return dict(n_models=13,n_compounds=49,n_permutations=10000,random_seed=SEED,observed_mean_fisher_z=obs,extreme_permutation_count=int(extreme),one_sided_p_value=(extreme+1)/10001)
old=aggregate(pd.read_csv(ROOT/'results/analysis/effective_binding_compound_summary_natural.csv'))
reference=pd.read_csv(ROOT/'results/analysis/effective_binding_aggregate_permutation_natural.csv').iloc[0]
assert old['extreme_permutation_count']==reference.extreme_permutation_count
np.testing.assert_allclose(old['observed_mean_fisher_z'],reference.observed_mean_fisher_z,atol=1e-14)
new=aggregate(summary[summary.condition=='natural']);assert cor.actual_prompt_condition.value_counts().to_dict()=={'natural':13,'uniform':12}
pd.DataFrame(mapping).to_csv(OUT/f'{PREFIX}-mapping.csv',index=False)
cor.to_csv(OUT/f'{PREFIX}-correlations.csv',index=False)
summary.to_csv(OUT/f'{PREFIX}-compounds.csv',index=False)
pd.DataFrame([dict(version='original_labels',**old),dict(version='reconciled_natural_prompts',**new)]).to_csv(OUT/f'{PREFIX}-aggregate.csv',index=False)
print('Original natural aggregate:',old);print('Reconciled natural aggregate:',new)
print(cor[cor.model.str.contains('gpt2-large|gpt2-medium')].to_string(index=False))
print('Missing: gpt2-medium uniform. No uniform aggregate recomputed.')
