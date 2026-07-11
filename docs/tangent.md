> ⚠️ **SUPERSEDED (2026-07-10).** This is a hand-transcription and contains
> confirmed paste-wounds (12B screen-reader / alt-text cross-contamination;
> GPT-2 XL screen-reader step-trace overwritten by a decision-point table).
> The authoritative regenerated data lives in **`results/logits/`**
> (`{model}_because_generations.csv`, `_because_steps.csv`, `_because_ranks.csv`),
> produced mechanically by `src/logit_export.py`; divergence report in
> `results/logits/REGEN_DIVERGENCE.md`. This document is retained **only** as
> the historical record of the paste-wound — do not cite figures from it.

# Logits

## Pythia 2.8B

### Skip Link Prompt

prompt = "A long navigation menu without a skip link is not accessible because"

1. Generation
A long navigation menu without a skip link is not accessible because the skip link is not present.

The navigation menu is not accessible because the skip link is not present.

The navigation menu is not accessible because the skip link is not present.

The navigation menu is not accessible because the skip

2. Where the correct token ranks
step  token_id   string               logit     
--------------------------------------------------
0     253        ' the'               16.270    
1     17049      ' skip'              14.730    
2     3048       ' link'              18.658    
3     310        ' is'                17.621    
4     417        ' not'               17.265    
5     1246       ' present'           16.180    
6     15         '.'                  18.964    
7     187        '\n'                 15.907    
8     187        '\n'                 18.250    
9     510        'The'                14.221

3. Top-15 logits at the decision point 
rank   token_id   string               logit     
--------------------------------------------------
0      253        ' the'               16.270    
1      352        ' it'                15.647    
2      273        ' of'                15.245    
3      627        ' there'             14.438    
4      247        ' a'                 14.197    
5      368        ' you'               13.798    
6      634        ' your'              12.932    
7      187        '\n'                 12.747    
8      16872      ' JavaScript'        12.731    
9      697        ' its'               12.647    
10     27030      ' browsers'          12.592    
11     359        ' we'                12.510    
12     4212       ' users'             12.437    
13     512        ' all'               12.275    
14     271        ' an'                12.107

### Screen Reader Prompt

prompt = "A website without screen reader support is not accessible because"
1. Generation
A website without screen reader support is not accessible because it is not designed to be used with assistive technologies such as screen readers.

A website without screen reader support is not accessible because it is not designed to be used with assistive technologies such as screen readers.

A website without screen
	
2. Where the correct token ranks 
step  token_id   string               logit     
--------------------------------------------------
0     352        ' it'                16.653    
1     310        ' is'                18.865    
2     417        ' not'               19.222    
3     4158       ' designed'          16.723    
4     281        ' to'                20.467    
5     320        ' be'                20.022    
6     908        ' used'              18.990    
7     342        ' with'              22.418    
8     10073      ' assist'            18.222    
9     422        'ive'                26.185
	
3. Top-15 logits at the decision point 
rank   token_id   string               logit     
--------------------------------------------------
0      352        ' it'                16.653    
1      3601       ' screen'            16.613    
2      253        ' the'               15.720    
3      273        ' of'                15.393    
4      368        ' you'               15.350    
5      247        ' a'                 14.861    
6      627        ' there'             14.573    
7      27         ':'                  13.952    
8      4212       ' users'             13.847    
9      1142       ' many'              13.749    
10     690        ' some'              13.726    
11     187        '\n'                 13.590    
12     9645       ' blind'             13.517    
13     634        ' your'              13.252    
14     417        ' not'               13.199 

### Alt Text Prompt
prompt = "An image without alt text is not accessible because"

1. Generation
An image without alt text is not accessible because it is not clickable.

The image is not accessible because it is not clickable.

The image is not accessible because it is not clickable.

The image is not accessible because it is not clickable.
	
2. Where the correct token ranks 
step  token_id   string               logit     
--------------------------------------------------
0     352        ' it'                16.208    
1     310        ' is'                17.757    
2     417        ' not'               16.849    
3     5532       ' click'             15.627    
4     494        'able'               21.515    
5     15         '.'                  17.986    
6     187        '\n'                 14.703    
7     187        '\n'                 16.851    
8     510        'The'                13.908    
9     2460       ' image'             12.977
	
3. Top-15 logits at the decision point 
rank   token_id   string               logit     
--------------------------------------------------
0      352        ' it'                16.208    
1      253        ' the'               15.858    
2      627        ' there'             14.425    
3      273        ' of'                14.329    
4      697        ' its'               13.495    
5      368        ' you'               13.288    
6      247        ' a'                 13.036    
7      6945       ' alt'               12.979    
8      634        ' your'              12.941    
9      436        ' this'              12.882    
10     642        ' no'                12.804    
11     359        ' we'                12.588    
12     326        ' that'              12.546    
13     187        '\n'                 12.382    
14     690        ' some'              12.205 

## Pythia 6.9B

### Skip Link Prompt
prompt = "A long navigation menu without a skip link is not accessible because"

1. Generation
	A long navigation menu without a skip link is not accessible because it is not a link.
	A long navigation menu without a skip link is not accessible because it is not a link.
	A long navigation menu without a skip link is not accessible because it is not a link.
	A long
	
2. Where the correct token ranks
	step  token_id   string               logit     
	0     352        ' it'                16.188    
	1     310        ' is'                17.084    
	2     417        ' not'               16.304    
	3     247        ' a'                 14.184    
	4     3048       ' link'              14.980    
	5     15         '.'                  17.950    
	6     187        '\n'                 16.169    
	7     187        '\n'                 17.707    
	8     34         'A'                  14.423    
	9     1048       ' long'              15.215

3. Top-15 logits at the decision point 
	rank   token_id   string               logit     
	0      352        ' it'                16.188    
	1      253        ' the'               16.014    
	2      273        ' of'                14.438    
	3      627        ' there'             14.226    
	4      247        ' a'                 14.092    
	5      368        ' you'               13.755    
	6      187        '\n'                 13.689    
	7      4212       ' users'             13.487    
	8      697        ' its'               13.345    
	9      309        ' I'                 12.578    
	10     642        ' no'                12.464    
	11     3601       ' screen'            12.445    
	12     27         ':'                  12.323    
	13     359        ' we'                12.273    
	14     512        ' all'               12.271

### Screen Reader Prompt
prompt = "A website without screen reader support is not accessible because"
1. Generation
	A website without screen reader support is not accessible because it is not usable.
	A website without screen reader support is not accessible because it is not usable.
	−
	A website without screen reader support is not accessible because it is not usable.
	+
	A website without
	
2. Where the correct token ranks 
	   step  token_id   string               logit     
	0     352        ' it'                16.873    
	1     310        ' is'                18.163    
	2     417        ' not'               17.260    
	3     31998      ' usable'            14.518    
	4     15         '.'                  19.765    
	5     187        '\n'                 15.894    
	6     187        '\n'                 18.633    
	7     34         'A'                  14.668    
	8     4422       ' website'           16.502    
	9     1293       ' without'           18.451
	
3. Top-15 logits at the decision point 
	   rank   token_id   string               logit     
	0      352        ' it'                16.873    
	1      253        ' the'               15.150    
	2      3601       ' screen'            14.550    
	3      273        ' of'                14.501    
	4      697        ' its'               13.803    
	5      247        ' a'                 13.631    
	6      368        ' you'               13.595    
	7      627        ' there'             13.530    
	8      4212       ' users'             13.529    
	9      187        '\n'                 13.406    
	10     642        ' no'                13.328    
	11     952        ' people'            13.238    
	12     1142       ' many'              13.224    
	13     512        ' all'               13.156    
	14     13         ','                  12.768   

### Alt Text Prompt
prompt = "An image without alt text is not accessible because"

1. Generation
	An image without alt text is not accessible because it is not descriptive enough. 
	The alt text is the text that is displayed in place of the image when the image is not displayed. The alt text is a text that describes the image. 
	The alt text is a text
	
2. Where the correct token ranks 
	step  token_id   string               logit     
	0     352        ' it'                16.795    
	1     310        ' is'                18.254    
	2     417        ' not'               17.360    
	3     27389      ' descriptive'       16.049    
	4     2217       ' enough'            19.975    
	5     15         '.'                  19.260    
	6     187        '\n'                 16.068    
	7     187        '\n'                 18.283    
	8     510        'The'                14.212    
	9     6945       ' alt'               15.697
	
3. Top-15 logits at the decision point 
	rank   token_id   string               logit     
	0      352        ' it'                16.795    
	1      253        ' the'               15.426    
	2      273        ' of'                14.806    
	3      3601       ' screen'            14.551    
	4      627        ' there'             14.355    
	5      952        ' people'            14.108    
	6      4212       ' users'             13.921    
	7      247        ' a'                 13.837    
	8      368        ' you'               13.722    
	9      697        ' its'               13.580    
	10     27030      ' browsers'          13.449    
	11     359        ' we'                13.419    
	12     187        '\n'                 13.391    
	13     642        ' no'                13.376    
	14     2505       ' text'              13.072  


## Pythia 12B
### prompt = "A long navigation menu without a skip link is not accessible because"

1. Generation
    A long navigation menu without a skip link is not accessible because of the following error:
    The page you are trying to reach is not available in the current context.
    The page you are trying to reach is not available in the current context.
    The page you are trying to reach is not

2. Where the correct token ranks

    step  token_id   string               logit     
    0     273        ' of'                16.110    
    1     253        ' the'               14.895    
    2     1563       ' following'         12.607    
    3     2228       ' error'             16.063    
    4     27         ':'                  20.141    
    5     187        '\n'                 15.541    
    6     187        '\n'                 16.488    
    7     510        'The'                14.520    
    8     3239       ' page'              14.032    
    9     368        ' you'               16.079    
 
3. Top-15 logits at the decision point 

    rank   token_id   string               logit     
    0      273        ' of'                16.110    
    1      253        ' the'               15.493    
    2      352        ' it'                15.168    
    3      368        ' you'               13.980    
    4      16872      ' JavaScript'        13.670    
    5      627        ' there'             13.655    
    6      697        ' its'               13.552    
    7      3601       ' screen'            13.499    
    8      247        ' a'                 13.060    
    9      27         ':'                  12.771    
    10     187        '\n'                 12.593    
    11     436        ' this'              12.557    
    12     17049      ' skip'              12.117    
    13     581        ' one'               12.053    
    14     4212       ' users'             11.983    

### prompt = "A website without screen reader support is not accessible because"

1. Generation
    A website without screen reader support is not accessible because it does not have a text alternative.

    The text alternative is a text version of the content that is read by a screen reader.

    The text alternative is not available because the website does not have a text alternative.

    The text

2. Where the correct token ranks
    step  token_id   string               logit     
    0     352        ' it'                15.918    
    1     1057       ' does'              17.358    
    2     417        ' not'               21.386    
    3     452        ' have'              18.644    
    4     247        ' a'                 17.893    
    5     2505       ' text'              14.780    
    6     5795       ' alternative'       19.329    
    7     15         '.'                  18.468    
    8     187        '\n'                 15.455    
    9     187        '\n'                 18.960
    
3. Top-15 logits at the decision point 
    rank   token_id   string               logit     
    0      352        ' it'                15.918    
    1      273        ' of'                15.307    
    2      3601       ' screen'            15.177    
    3      253        ' the'               14.982    
    4      187        '\n'                 13.523    
    5      952        ' people'            13.343    
    6      368        ' you'               13.312    
    7      359        ' we'                13.069    
    8      1142       ' many'              12.886    
    9      247        ' a'                 12.875    
    10     690        ' some'              12.802    
    11     436        ' this'              12.724    
    12     697        ' its'               12.716    
    13     411        ' W'                 12.559    
    14     16872      ' JavaScript'        12.543    
### prompt = "An image without alt text is not accessible because"
1. Generation
    An image without alt text is not accessible because it has no text alternative.
    The alt text is a short description of the image.
    The alt text is not a substitute for the image.
    The alt text is not a substitute for the image.
    The alt text

2. Where the correct token ranks
    step  token_id   string               logit     
    0     352        ' it'                15.040    
    1     556        ' has'               17.395    
    2     642        ' no'                18.231    
    3     2505       ' text'              17.793    
    4     5795       ' alternative'       20.451    
    5     15         '.'                  18.196    
    6     187        '\n'                 15.584    
    7     187        '\n'                 18.874    
    8     510        'The'                14.571    
    9     6945       ' alt'               14.015    
    
3. Top-15 logits at the decision point 
    rank   token_id   string               logit     
    0      352        ' it'                15.040    
    1      273        ' of'                14.435    
    2      253        ' the'               14.311    
    3      3601       ' screen'            13.589    
    4      6945       ' alt'               13.561    
    5      368        ' you'               13.499    
    6      2460       ' image'             13.170    
    7      2505       ' text'              12.747    
    8      436        ' this'              12.735    
    9      16872      ' JavaScript'        12.683    
    10     187        '\n'                 12.334    
    11     2600       ' content'           11.957    
    12     359        ' we'                11.941    
    13     634        ' your'              11.921    
    14     3888       ' images'            11.821    
---

## GPT2 Medium

### prompt = "A long navigation menu without a skip link is not accessible because"
1. Generation
   A long navigation menu without a skip link is not accessible because the navigation menu is not visible. 
   Solution 
   The navigation menu is not visible because the navigation menu is not visible. 
   Solution 
   The navigation menu is not visible because the navigation menu is not visible. 
   Solution
   
2. Where the correct token ranks
   step  token_id   string               logit     
--------------------------------------------------
0     262        ' the'               15.374    
1     16408      ' navigation'        14.316    
2     6859       ' menu'              16.593    
3     318        ' is'                16.589    
4     407        ' not'               16.168    
5     7424       ' visible'           14.909    
6     13         '.'                  17.760    
7     198        '\n'                 16.664    
8     198        '\n'                 26.862    
9     46344      'Solution'           17.201

3. Top-15 logits at the decision point
   rank   token_id   string               logit     
--------------------------------------------------
0      262        ' the'               15.374    
1      340        ' it'                15.101    
2      286        ' of'                14.824    
3      345        ' you'               13.534    
4      257        ' a'                 13.480    
5      612        ' there'             13.439    
6      534        ' your'              12.796    
7      428        ' this'              12.164    
8      16408      ' navigation'        12.118    
9      663        ' its'               12.095    
10     356        ' we'                11.877    
11     281        ' an'                11.755    
12     326        ' that'              11.618    
13     617        ' some'              11.600    
14     645        ' no'                11.539

### prompt = "A website without screen reader support is not accessible because"
1. Generation
   A website without screen reader support is not accessible because it is not supported by the browser. 
   If you are using a browser that does not support screen reader support, you will not be able to access the website. 
   If you are using a browser that does support screen reader support, you
2. Where the correct token ranks
   step  token_id   string               logit     
--------------------------------------------------
0     340        ' it'                16.173    
1     318        ' is'                18.392    
2     407        ' not'               16.756    
3     4855       ' supported'         15.500    
4     416        ' by'                18.737    
5     262        ' the'               15.611    
6     6444       ' browser'           14.770    
7     13         '.'                  17.165    
8     198        '\n'                 16.805    
9     198        '\n'                 27.345

3. Top-15 logits at the decision point
rank   token_id   string               logit     
--------------------------------------------------
0      340        ' it'                16.173    
1      262        ' the'               15.575    
2      286        ' of'                15.289    
3      534        ' your'              14.068    
4      345        ' you'               13.996    
5      257        ' a'                 13.728    
6      663        ' its'               13.623    
7      612        ' there'             13.544    
8      645        ' no'                13.361    
9      3159       ' screen'            12.829    
10     2985       ' users'             12.827    
11     25         ':'                  12.735    
12     484        ' they'              12.536    
13     11933      ' JavaScript'        12.361    
14     3012       ' Google'            12.334



### prompt = "An image without alt text is not accessible because"
1. Generation
   An image without alt text is not accessible because it is not displayed in the browser. 
   An image with alt text is accessible because it is displayed in the browser. 
   An image with alt text is accessible because it is displayed in the browser. 
   An image with alt text is
   
2. Where the correct token ranks
   step  token_id   string               logit     
--------------------------------------------------
0     340        ' it'                15.904    
1     318        ' is'                18.348    
2     407        ' not'               16.087    
3     9066       ' displayed'         14.927    
4     287        ' in'                18.271    
5     262        ' the'               15.959    
6     6444       ' browser'           13.722    
7     13         '.'                  17.278    
8     198        '\n'                 16.516    
9     198        '\n'                 26.857

3. Top-15 logits at the decision point
   rank   token_id   string               logit     
--------------------------------------------------
0      340        ' it'                15.904    
1      262        ' the'               15.338    
2      286        ' of'                14.782    
3      663        ' its'               13.179    
4      257        ' a'                 12.872    
5      612        ' there'             12.830    
6      345        ' you'               12.546    
7      281        ' an'                12.429    
8      534        ' your'              12.277    
9      25         ':'                  12.048    
10     617        ' some'              11.924    
11     428        ' this'              11.824    
12     356        ' we'                11.746    
13     645        ' no'                11.744    
14     5988       ' alt'               11.388

---


---

## GPT2 Large

### prompt = "A long navigation menu without a skip link is not accessible because"
1. Generation
	A long navigation menu without a skip link is not accessible because it is not a part of the navigation.
	
	The navigation menu is a part of the navigation.
	
	The navigation menu is a part of the navigation.
	
	The navigation menu is a part of the navigation.
	
	The navigation menu   
	
2. Where the correct token ranks
step  token_id   string               logit     
--------------------------------------------------
0     340        ' it'                15.867    
1     318        ' is'                17.336    
2     407        ' not'               15.663    
3     257        ' a'                 14.718    
4     636        ' part'              14.408    
5     286        ' of'                21.551    
6     262        ' the'               18.142    
7     16408      ' navigation'        15.581    
8     13         '.'                  15.647    
9     198        '\n'                 15.704

3. Top-15 logits at the decision point
 rank   token_id   string               logit     
--------------------------------------------------
0      340        ' it'                15.867    
1      286        ' of'                15.350    
2      262        ' the'               15.129    
3      345        ' you'               13.546    
4      612        ' there'             13.029    
5      257        ' a'                 13.002    
6      2985       ' users'             12.929    
7      25         ':'                  12.688    
8      356        ' we'                12.457    
9      11         ','                  12.418    
10     428        ' this'              12.332    
11     3012       ' Google'            12.313    
12     867        ' many'              12.307    
13     617        ' some'              12.289    
14     749        ' most'              12.251

### prompt = "A website without screen reader support is not accessible because"
1. Generation
A website without screen reader support is not accessible because it is not accessible.

The website you are trying to access is not accessible because it is not accessible.

The website you are trying to access is not accessible because it is not accessible.

The website you are trying to access

2. Where the correct token ranks
  step  token_id   string               logit     
--------------------------------------------------
0     340        ' it'                16.052    
1     318        ' is'                18.028    
2     407        ' not'               17.140    
3     9857       ' accessible'        15.265    
4     13         '.'                  18.483    
5     198        '\n'                 15.759    
6     198        '\n'                 20.828    
7     464        'The'                15.399    
8     3052       ' website'           13.351    
9     345        ' you'               15.801

3. Top-15 logits at the decision point
rank   token_id   string               logit     
--------------------------------------------------
0      340        ' it'                16.052    
1      286        ' of'                15.574    
2      262        ' the'               15.445    
3      345        ' you'               13.981    
4      257        ' a'                 13.668    
5      2985       ' users'             13.641    
6      534        ' your'              13.546    
7      612        ' there'             13.515    
8      663        ' its'               13.356    
9      25         ':'                  13.316    
10     3159       ' screen'            13.142    
11     661        ' people'            12.657    
12     749        ' most'              12.623    
13     867        ' many'              12.599    
14     356        ' we'                12.597



### prompt = "An image without alt text is not accessible because"
1. Generation
An image without alt text is not accessible because it is not a link.

An image without alt text is not accessible because it is not a link.

An image without alt text is not accessible because it is not a link.

An image without alt text is not accessible
   
2. Where the correct token ranks
step  token_id   string               logit     
--------------------------------------------------
0     340        ' it'                16.752    
1     318        ' is'                18.224    
2     407        ' not'               15.115    
3     257        ' a'                 15.267    
4     2792       ' link'              13.762    
5     13         '.'                  17.571    
6     198        '\n'                 16.469    
7     198        '\n'                 20.657    
8     2025       'An'                 15.454    
9     2939       ' image'             18.765

3. Top-15 logits at the decision point
rank   token_id   string               logit     
--------------------------------------------------
0      340        ' it'                16.752    
1      262        ' the'               15.852    
2      286        ' of'                15.324    
3      25         ':'                  13.887    
4      663        ' its'               13.608    
5      345        ' you'               13.543    
6      5988       ' alt'               13.357    
7      326        ' that'              12.914    
8      428        ' this'              12.836    
9      612        ' there'             12.644    
10     257        ' a'                 12.520    
11     534        ' your'              12.221    
12     11         ','                  12.113    
13     356        ' we'                12.083    
14     281        ' an'                11.885

---

## GPT2 XL

### prompt = "A long navigation menu without a skip link is not accessible because"
1. Generation
A long navigation menu without a skip link is not accessible because the user has not yet navigated to the desired page.

The navigation menu should be accessible to the user by providing a skip link.

The skip link should be a link that the user can click to skip to the desired page. 
	
2. Where the correct token ranks
step  token_id   string               logit     
--------------------------------------------------
0     262        ' the'               15.982    
1     2836       ' user'              13.480    
2     468        ' has'               16.522    
3     407        ' not'               16.357    
4     1865       ' yet'               15.783    
5     20436      ' navig'             15.771    
6     515        'ated'               22.907    
7     284        ' to'                18.456    
8     262        ' the'               18.720    
9     10348      ' desired'           14.845

3. Top-15 logits at the decision point
 rank   token_id   string               logit     
--------------------------------------------------
0      262        ' the'               15.982    
1      340        ' it'                15.318    
2      286        ' of'                15.030    
3      612        ' there'             13.828    
4      345        ' you'               13.706    
5      257        ' a'                 13.453    
6      534        ' your'              12.469    
7      663        ' its'               12.339    
8      428        ' this'              12.293    
9      356        ' we'                12.252    
10     326        ' that'              11.957    
11     25         ':'                  11.951    
12     645        ' no'                11.922    
13     281        ' an'                11.902    
14     617        ' some'              11.802

### prompt = "A website without screen reader support is not accessible because"
1. Generation
A website without screen reader support is not accessible because the website is not accessible to screen readers.

If you are using a screen reader, please try to access the website using the following link:

http://www.cbc.ca/news/canada/montreal/mont

2. Where the correct token ranks
rank   token_id   string               logit     
--------------------------------------------------
0      262        ' the'               15.982    
1      340        ' it'                15.318    
2      286        ' of'                15.030    
3      612        ' there'             13.828    
4      345        ' you'               13.706    
5      257        ' a'                 13.453    
6      534        ' your'              12.469    
7      663        ' its'               12.339    
8      428        ' this'              12.293    
9      356        ' we'                12.252    
10     326        ' that'              11.957    
11     25         ':'                  11.951    
12     645        ' no'                11.922    
13     281        ' an'                11.902    
14     617        ' some'              11.802

3. Top-15 logits at the decision point
rank   token_id   string               logit     
--------------------------------------------------
0      262        ' the'               15.777    
1      286        ' of'                15.259    
2      340        ' it'                15.126    
3      534        ' your'              14.152    
4      345        ' you'               13.960    
5      612        ' there'             13.602    
6      257        ' a'                 13.587    
7      3159       ' screen'            12.749    
8      11933      ' JavaScript'        12.693    
9      25         ':'                  12.687    
10     617        ' some'              12.600    
11     356        ' we'                12.397    
12     281        ' an'                12.314    
13     645        ' no'                12.109    
14     428        ' this'              12.040



### prompt = "An image without alt text is not accessible because"
1. Generation
An image without alt text is not accessible because the image is not in the alt text format.

An image without alt text is not accessible because the image is not in the alt text format.

An image without alt text is not accessible because the image is not in the alt text
   
2. Where the correct token ranks
step  token_id   string               logit     
--------------------------------------------------
0     262        ' the'               16.757    
1     2939       ' image'             15.220    
2     318        ' is'                17.401    
3     407        ' not'               16.934    
4     287        ' in'                15.673    
5     262        ' the'               18.237    
6     5988       ' alt'               14.011    
7     2420       ' text'              17.755    
8     5794       ' format'            15.736    
9     13         '.'                  18.434

3. Top-15 logits at the decision point
rank   token_id   string               logit     
--------------------------------------------------
0      262        ' the'               16.757    
1      340        ' it'                16.272    
2      5988       ' alt'               14.607    
3      286        ' of'                14.503    
4      534        ' your'              14.381    
5      345        ' you'               13.882    
6      612        ' there'             13.861    
7      257        ' a'                 13.325    
8      663        ' its'               13.297    
9      428        ' this'              12.781    
10     25         ':'                  12.776    
11     281        ' an'                12.508    
12     11         ','                  12.422    
13     326        ' that'              12.378    
14     198        '\n'                 12.336