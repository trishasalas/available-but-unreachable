"""Recheck registered ablation artifacts without model inference.
Run from the repository root with Python, pandas, NumPy, and SciPy.
A failed assertion stops the audit; result artifacts are never modified.
"""
from pathlib import Path
import pandas as pd, numpy as np, json, re, hashlib, math, ast
from scipy.stats import spearmanr
root=Path.cwd(); base=root/'results/ablation/frequency_heads/pythia-2.8b'; stem='pythia-2.8b-natural-registered-'
read=lambda n:pd.read_csv(base/(stem+n+'.csv'))
p=read('primary'); r=read('random-controls'); rs=read('random-set-summary'); hs=read('head-sets'); s=read('summary').iloc[0]
split=pd.read_csv('results/analysis/effective_binding_compound_split.csv').sort_values('shuffle_position')
names=sorted(split.compound); np.random.default_rng(20260813).shuffle(names)
assert names==split.compound.tolist()
assert split.split.tolist()==['selection']*25+['held_out']*24
assert p.compound.tolist()==names[25:] and p.compound.is_unique
print('Split: exact seed/shuffle/order match; 25 selection / 24 test; no overlap')
for path,digest in re.findall(r'\|[^\n]*?`([^`]+)` \| `([a-f0-9]{64})` \|',(base/(stem+'primary.md')).read_text()):
 actual=hashlib.sha256(Path(path).read_bytes()).hexdigest()
 assert actual==digest,(path,actual,digest)
 print('Hash matches:',path)
f=pd.read_csv('results/frequency/frequency_table.csv')[['compound','bigram_count']].drop_duplicates()
raw=pd.read_csv('results/effective_binding/pythia/pythia-2.8b/natural/pythia-2.8b-natural-accessibility.csv')
x=raw[(raw.layer>=math.ceil(64/3)) & raw.compound.isin(names[:25])].merge(f,on='compound',validate='many_to_one')
rows=[]
for (l,h),g in x.groupby(['layer','head']):
 assert len(g)==25 and g.compound.nunique()==25
 rows.append((l,h,spearmanr(np.log1p(g.bigram_count),g.relative_weighted_ov_norm).statistic))
ranked=sorted(rows,key=lambda a:a[2]); selected=[list(a[:2]) for a in ranked[:5]]
assert all(json.loads(v)==selected for v in p.selected_heads)
print('Recomputed candidate selection from raw 25-compound data:',ranked[:5])
sets={row.set_id:json.loads(row.heads) for row in hs.itertuples()}
assert sets['selected']==selected and sets['empty']==[] and sets['positive_control']==[[30,h] for h in range(32)]
pool=[(l,h) for l in range(22,32) for h in range(32) if [l,h] not in selected]
rng=np.random.default_rng(20260813); draws=[]
for i in range(100):
 draw=sorted([list(pool[j]) for j in rng.choice(len(pool),5,replace=False)])
 assert draw==sets[f'random_{i+1:03d}']; draws.append(str(draw))
assert len(set(draws))==100
print('Random sets: exact first 100 seeded draws match; 315 eligible heads; no duplicate sets or selected heads')
assert len(r)==2400 and not r.duplicated(['compound','set_id']).any()
assert set(r.compound)==set(names[25:])
for row in r.itertuples(): assert json.loads(row.heads)==sets[row.set_id]
for _,g in r.groupby('set_id'): assert len(g)==24 and set(g.compound)==set(names[25:])
for d in [p,r]:
 check=d.merge(f,on='compound',suffixes=('','_canonical'),validate='many_to_one')
 assert (check.bigram_count==check.bigram_count_canonical).all()
 assert np.allclose(d.log_frequency,np.log1p(d.bigram_count),rtol=0,atol=1e-14)
assert np.isfinite(p[['selected_kl','empty_kl','positive_control_kl']]).all().all() and np.isfinite(r.kl).all()
assert p.empty_kl.abs().max()<=1e-8 and p.positive_control_kl.max()>1e-6
print('Gates: empty max',p.empty_kl.abs().max(),'positive max',p.positive_control_kl.max(),'positive >1e-6',int((p.positive_control_kl>1e-6).sum()),'/24')
for label in ['selected','positive_control']:
 changed=p.apply(lambda row:json.loads(row.baseline_top)[0][0]!=json.loads(row[label+'_ablated_top'])[0][0],axis=1)
 assert (changed==p[label+'_top_changed']).all()
obs=spearmanr(p.log_frequency,p.selected_kl).statistic
rng=np.random.default_rng(20260813)
extreme=sum(spearmanr(rng.permutation(p.log_frequency),p.selected_kl).statistic<=obs for _ in range(10000))
perm=(1+extreme)/10001
assert np.isclose(obs,s.selected_rho_frequency_kl,rtol=0,atol=1e-14)
assert np.isclose(perm,s.selected_permutation_p_one_sided,rtol=0,atol=1e-14)
for sid,g in r.groupby('set_id'):
 saved=rs.set_index('set_id').loc[sid]
 for col,v in [('rho_frequency_kl',spearmanr(g.log_frequency,g.kl).statistic),('mean_kl',g.kl.mean()),('median_kl',g.kl.median()),('top_changes',g.top_changed.sum())]:
  assert np.isclose(v,saved[col],rtol=1e-12,atol=1e-14),(sid,col,v,saved[col])
tail=(1+(rs.rho_frequency_kl<=obs).sum())/101
assert np.isclose(tail,s.selected_rho_random_tail_p,atol=1e-14)
for key,v in {'selected_mean_kl':p.selected_kl.mean(),'selected_median_kl':p.selected_kl.median(),'selected_top_changes':p.selected_top_changed.sum(),'empty_max_abs_kl':p.empty_kl.abs().max(),'positive_control_max_kl':p.positive_control_kl.max(),'positive_control_median_kl':p.positive_control_kl.median(),'positive_control_top_changes':p.positive_control_top_changed.sum(),'random_rho_median':rs.rho_frequency_kl.median()}.items():
 assert np.isclose(v,s[key],rtol=1e-12,atol=1e-14),(key,v,s[key])
print('Statistics: rho',obs,'extreme permutations',extreme,'p',perm,'random tail',tail)
print('Selected KL mean/median/range',p.selected_kl.mean(),p.selected_kl.median(),p.selected_kl.min(),p.selected_kl.max())
print('Selected top changes',p.selected_top_changed.sum(),'random top changes',r.top_changed.sum())
print('PASS: saved-artifact and statistical audit; no model inference rerun')
