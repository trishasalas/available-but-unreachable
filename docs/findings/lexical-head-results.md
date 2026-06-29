# Lexical Head Results

## 1. QK Circuit

layer  head  domain        compound  score
    29     7    a11y   screen reader 0.9019
    29     7 general    coffee table 0.2104
    29     7    a11y       skip link 0.0725
    29     7 medical     side effect 0.0479
    29     7   legal        case law 0.0465
    29     7 finance    stock market 0.0301
    29     7 finance      hedge fund 0.0209
    29     7 general   bicycle wheel 0.0178
    29     7 finance    credit score 0.0112
    29     7    a11y  color contrast 0.0080
    29     7 medical      heart rate 0.0058
    29     7   legal     due process 0.0057
    29     7 general      phone call 0.0029
    29     7    a11y        alt text 0.0029
    29     7    a11y focus indicator 0.0028
    29     7 medical  blood pressure 0.0011
    29     7   legal     court order 0.0008

---

{'query': 'reader', 'key': 'screen', 'attention': 0.9019}
{'query': 'reader', 'key': 'A', 'attention': 0.0001}
{'query': 'reader', 'key': 'reader', 'attention': 0.0121}

---

screen  bicycle    alt  stock    due
reader   -0.002   -0.001 -0.000  0.002  0.000
wheel     0.005    0.004  0.000  0.000  0.002
text     -0.003   -0.002  0.000  0.003  0.000
market   -0.001   -0.004  0.000  0.004 -0.001
process  -0.007   -0.003 -0.003  0.004 -0.002

---

## 2. OV Circuit

attention screen->reader: 0.9019

PROMOTED tokens:
            'fire'  0.515
        ' shooter'  0.455
           ' fire'  0.443
       ' shooting'  0.436
           'fires'  0.432
          ' shoot'  0.419
            'camp'  0.385
          ' fires'  0.383
            'Fire'  0.383
          'loader'  0.374
       ' firearms'  0.37
            'chin'  0.366
          'reload'  0.366
          'logger'  0.362
  ' photographers'  0.361
          ' firef'  0.361
            ' ear'  0.36
            'LAND'  0.355
           'lands'  0.353
         ' losing'  0.353

SUPPRESSED tokens:
         ' screen'  -1.409
        ' screens'  -1.291
          'screen'  -1.23
         ' Screen'  -1.158
          'Screen'  -1.114
      ' screening'  -1.014
       ' screened'  -0.972
            'scre'  -0.892
            'Scre'  -0.879
           ' Scre'  -0.866
           'creen'  -0.749
          ' Wings'  -0.57
           'clean'  -0.536
            ' air'  -0.52
       ' aviation'  -0.515
          ' clean'  -0.508
          ' plane'  -0.487
          ' wings'  -0.482
          ' airst'  -0.48
         ' filter'  -0.48

## 3. Causal Check

KL(base || ablated): 1e-05
baseline top: [(' a', 0.5137), (' an', 0.1712), (' software', 0.0329), (' used', 0.0288), (' not', 0.015), (' the', 0.0149), (' available', 0.0122), (' designed', 0.0105), (' often', 0.0103), (' typically', 0.0084)]
ablated  top: [(' a', 0.5136), (' an', 0.171), (' software', 0.0331), (' used', 0.0288), (' not', 0.0149), (' the', 0.0149), (' available', 0.0124), (' designed', 0.0106), (' often', 0.0103), (' typically', 0.0084)]


