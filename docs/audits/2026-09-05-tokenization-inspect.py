"""Descriptive reconstruction of saved constituent spans only. No tokenizer, model, correlation, or sensitivity test is run. Execute from repository root."""
from pathlib import Path
import ast,pandas as pd,hashlib,json,yaml
root=Path.cwd(); rows=[]; hashes=[]; prompt_checks=[]
cases={x["name"]:x for x in yaml.safe_load(Path("data/binding/accessibility.yaml").read_text())["compounds"]}
f=set(pd.read_csv('results/frequency/frequency_table.csv').compound)
def spans(tokens,word):
 target=word.lower();out=[]
 for start in range(len(tokens)):
  joined=''
  for end in range(start,len(tokens)):
   joined+=tokens[end].strip().lower()
   if joined==target:out.append((start,end));break
   if len(joined)>len(target):break
 return out
for p in sorted(Path('results/effective_binding').glob('*/*/*/*-accessibility.csv')):
 d=pd.read_csv(p,usecols=['compound','word1','word2','tokens','word1_idx','word2_idx','prompt','model','family','prompt_condition']).drop_duplicates()
 assert len(d)==53 and d.compound.is_unique,(p,len(d))
 hashes.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 prompt_checks.append({'path':str(p),'natural_matches_of_53':sum(r.prompt==cases[r.compound]['prompt'] for r in d.itertuples()),'uniform_matches_of_53':sum(r.prompt==f"A {cases[r.compound]['word1']} {cases[r.compound]['word2']} is" for r in d.itertuples())})
 for r in d.itertuples():
  ts=ast.literal_eval(r.tokens);ss=[spans(ts,r.word1),spans(ts,r.word2)]
  # Reproduce exact-token priority, then first concatenated span.
  chosen=[]
  for w,sp in zip([r.word1,r.word2],ss):
   exact=[(i,i) for i,t in enumerate(ts) if t.strip().lower()==w.lower()]
   chosen.append(exact[0] if exact else sp[0])
  assert sorted(s[1] for s in chosen)==[r.word1_idx,r.word2_idx],(p,r.compound)
  counts=[e-s+1 for s,e in chosen]
  rows.append(dict(family=r.family,model=r.model,condition=r.prompt_condition,compound=r.compound,in_frequency_set=r.compound in f,word1_tokens=counts[0],word2_tokens=counts[1],compound_tokens=sum(counts),word1_spans=len(ss[0]),word2_spans=len(ss[1]),word1_pieces=json.dumps(ts[chosen[0][0]:chosen[0][1]+1]),word2_pieces=json.dumps(ts[chosen[1][0]:chosen[1][1]+1])))
r=pd.DataFrame(rows); out=Path('docs/audits');r.to_csv(out/'2026-09-05-tokenization-inventory.csv',index=False)
pd.DataFrame(prompt_checks).to_csv(out/'2026-09-05-tokenization-prompt-check.csv',index=False)
for input_path in ['data/binding/accessibility.yaml','results/frequency/frequency_table.csv']:
 hashes.append({'path':input_path,'sha256':hashlib.sha256(Path(input_path).read_bytes()).hexdigest()})
pd.DataFrame(hashes).to_csv(out/'2026-09-05-tokenization-inputs.csv',index=False)
for (family,model,c),g in r[r.in_frequency_set].groupby(['family','model','condition']):
 print(model,c,g.compound_tokens.value_counts().sort_index().to_dict(),'ambiguous',int(((g.word1_spans>1)|(g.word2_spans>1)).sum()))
print('Representative split compounds:')
print(r[r.in_frequency_set & (r.compound_tokens>2)].drop_duplicates(['family','condition','compound','word1_pieces','word2_pieces'])[['family','condition','compound','word1_pieces','word2_pieces']].head(28).to_string(index=False))
