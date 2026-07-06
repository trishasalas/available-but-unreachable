# D8 calibration (offline join vs shared Pile-count cache)
- counts cached: 500/500 (index v4_piletrain_llama; Llama-2 tokenizer string counts — caveat per pre-reg)

- pythia-160m: rho(b_U, log Pile count) = 0.664 (n=500, p=6e-65)
- pythia-410m: rho(b_U, log Pile count) = 0.737 (n=500, p=9e-87)
- pythia-1b: rho(b_U, log Pile count) = 0.767 (n=500, p=6.1e-98)
- pythia-2.8b: rho(b_U, log Pile count) = 0.722 (n=500, p=1.1e-81)
- pythia-6.9b: rho(b_U, log Pile count) = 0.689 (n=500, p=1.3e-71)
- pythia-12b: rho(b_U, log Pile count) = 0.779 (n=500, p=4e-103)

Sign-disagreement rule (frozen): if this disagrees in sign with the token-ID proxy, report both, conclude nothing, stop.