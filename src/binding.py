"""
Compound binding sweep module.

Measures attention binding between token pairs across all layers and heads.
Runs multiple compounds per model, saves per-model CSV.

Usage (from notebook):
    from src.binding import run_binding_sweep
    binding_df = run_binding_sweep(model, model_name, PROJECT_ROOT)
"""

from pathlib import Path
import pandas as pd


# Comounds with prompts for the binding run
ACCESSIBILITY = [

    ("screen_reader",            "screen",      "reader",          "A screen reader is"),
    ("alt_text",                 "alt",         "text",            "The purpose of alt text is"),
    ("skip_link",                "skip",        "link",            "A skip link is"),
    ("color_contrast",           "color",       "contrast",        "Color contrast is important because"),
    ("keyboard_navigation",      "keyboard",    "navigation",      "Keyboard navigation allows"),
    ("closed_captions",          "closed",      "captions",        "Closed captions are used for"),
    ("focus_indicator",          "focus",       "indicator",        "A focus indicator is"),
    ("semantic_html",            "semantic",    "HTML",             "Semantic HTML helps"),
    ("form_label",               "form",        "label",           "A form label is"),
    ("link_text",                "link",        "text",            "Link text describes"),
    ("page_title",               "page",        "title",           "A page title describes"),
    ("keyboard_interaction",     "keyboard",    "interaction",      "A keyboard interaction is"),
    ("section_heading",          "section",     "heading",          "A section heading is"),
    ("text_alternative",         "text",        "alternative",      "A text alternative is"),
    ("audio_description",        "audio",       "description",      "An audio description is"),
    ("sign_language",            "sign",        "language",          "Sign language is"),
    ("sensory_characteristics",  "sensory",     "characteristics",  "Sensory characteristics are"),
    ("input_purpose",            "input",       "purpose",          "An input purpose is"),
    ("target_size",              "target",      "size",             "A target size is"),
    ("touch_target",             "touch",       "target",           "A touch target is"),
    ("drag_movement",            "drag",        "movement",         "A drag movement is"),
    ("focus_appearance",         "focus",       "appearance",        "A focus appearance is"),
    ("consistent_help",          "consistent",  "help",             "Consistent help is"),
    ("redundant_entry",          "redundant",   "entry",            "A redundant entry is"),
    ("accessible_authentication","accessible",  "authentication",   "Accessible authentication is"),
    ("text_spacing",             "text",        "spacing",          "Text spacing is"),
    ("status_message",           "status",      "message",          "A status message is"),
    ("error_identification",     "error",       "identification",   "Error identification is"),
    ("pointer_cancellation",     "pointer",     "cancellation",     "Pointer cancellation is"),
    ("character_key",            "character",   "key",              "A character key is"),
    ("accessibility_tree",       "accessibility","tree",             "An accessibility tree is"),
    ("accessible_name",          "accessible",  "name",             "An accessible name is"),
    ("accessible_description",   "accessible",  "description",      "An accessible description is"),
    ("live_region",              "live",        "region",            "A live region is"),
    ("tab_panel",                "tab",         "panel",             "A tab panel is"),
    ("radio_group",              "radio",       "group",             "A radio group is"),
    ("tree_grid",                "tree",        "grid",              "A tree grid is"),
    ("menu_bar",                 "menu",        "bar",               "A menu bar is"),
    ("tool_tip",                 "tool",        "tip",               "A tool tip is"),
    ("combo_box",                "combo",       "box",               "A combo box is"),
    ("semantic_markup",          "semantic",    "markup",            "Semantic markup is"),
    ("focus_management",         "focus",       "management",        "Focus management is"),
    ("reading_order",            "reading",     "order",             "Reading order is"),
    ("text_formatting",          "text",        "formatting",        "Text formatting is"),
    ("form_field",               "form",        "field",             "A form field is"),
    ("landmark_region",          "landmark",    "region",            "A landmark region is"),
    ("low_vision",               "low",         "vision",            "Low vision is"),
    ("cognitive_disabilities",   "cognitive",   "disabilities",      "Cognitive disabilities are"),
    ("universal_design",         "universal",   "design",            "Universal design is"),
    ("decorative_image",         "decorative",  "image",             "A decorative image is"),
    ("informative_image",        "informative", "image",             "An informative image is"),
    ("responsive_design",        "responsive",  "design",            "Responsive design is"),
    ("empty_link",               "empty",       "link",              "An empty link is"),
]

CONTROL = [
    ('blue_sky',                    'blue',         'sky',            'I like to look at the blue sky'),
    ('cold_water',                  'cold',         'water',          'She drank a glass of cold water'),
    ('ice_cream',                   'ice',          'cream',          'My favorite ice cream is chocolate'),
    ('life_jacket',                 'life',         'jacket',         'We took a life jacket on the boat'),
    ('tea_cup',                     'tea',          'cup',            'My tea cup is pink'),
    ('living_room',                 'living',       'room',           'Our house has a formal living room'),
    ('roller_coaster',              'roller',       'coaster',        'The roller coaster is my favorite ride'),
    ('school_bus',                  'school',       'bus',            'The school bus is yellow'),
    ('grilled_cheese',              'grilled',      'cheese',         'She ordered a grilled cheese from the menu'),
    ('peanut_butter',               'peanut',       'butter',         'We need to buy peanut butter at the store'),
    ('hot_chocolate',               'hot',          'chocolate',      'He put whipped cream on his hot chocolate'),
    ('apple_pie',                   'apple',        'pie',            'The apple pie was still warm from the oven'),
    ('orange_juice',                'orange',       'juice',          'She drinks orange juice every morning'),
    ('baked_beans',                 'baked',        'beans',          'We had baked beans with dinner last night'),
    ('palm_tree',                   'palm',         'tree',           'The palm tree swayed gently in the breeze'),
    ('thunder_storm',               'thunder',      'storm',          'A thunder storm rolled in from the west'),
    ('coral_reef',                  'coral',        'reef',           'The coral reef is home to many fish'),
    ('shooting_star',               'shooting',     'star',           'We watched the shooting star cross the sky'),
    ('mountain_lion',               'mountain',     'lion',           'The mountain lion was spotted near the trail'),
    ('tidal_wave',                  'tidal',        'wave',           'A tidal wave warning was issued for the coast'),
    ('dining_table',                'dining',       'table',          'The dining table seats six people comfortably'),
    ('car_keys',                    'car',          'keys',           'He left his car keys on the counter'),
    ('washing_machine',             'washing',      'machine',        'The washing machine is making a strange noise'),
    ('bath_towels',                 'bath',         'towels',         'She bought new bath towels for the guest room'),
    ('alarm_clock',                 'alarm',        'clock',          'The alarm clock went off at six in the morning'),
    ('light_bulb',                  'light',        'bulb',           'He replaced the light bulb in the hallway'),
    ('post_office',                 'post',         'office',         'The post office closes at five on weekdays'),
    ('parking_lot',                 'parking',      'lot',            'We parked in the parking lot behind the building'),
    ('train_station',               'train',        'station',        'The train station is two blocks from here'),
    ('fire_station',                'fire',         'station',        'She works at the fire station downtown'),
    ('swimming_pool',               'swimming',     'pool',           'The swimming pool is open during the summer'),
    ('coffee_shop',                 'coffee',       'shop',           'They met at the coffee shop on the corner'),
    ('hard_drive',                  'hard',         'drive',          'The hard drive stores all of your files'),
    ('operating_system',            'operating',    'system',         'She updated her operating system last night'),
    ('search_engine',               'search',       'engine',         'The search engine returned millions of results'),
    ('user_name',                   'user',         'name',           'He forgot his user name for the website'),
    ('power_supply',                'power',        'supply',         'The power supply was disconnected during the storm'),
    ('data_base',                   'data',         'base',           'A data base stores information in structured tables'),
    ('sore_throat',                 'sore',         'throat',         'She has a sore throat from the cold weather'),
    ('blood_pressure',              'blood',        'pressure',       'The blood pressure reading was perfectly normal'),
    ('collar_bone',                 'collar',       'bone',           'He broke his collar bone playing football'),
    ('heart_rate',                  'heart',        'rate',           'The heart rate monitor beeped steadily'),
    ('dental_appointment',          'dental',       'appointment',    'She scheduled a dental appointment for Tuesday'),
    ('waiting_room',                'waiting',      'room',           'The waiting room was full of patients'),
]

LEGAL = [
    ('due_process',                 'due',          'process',        'The due process clause protects individual rights'),
    ('equal_protection',            'equal',        'protection',     'The equal protection argument was central to the case'),
    ('commerce_clause',             'commerce',     'clause',         'The commerce clause limits state regulatory power'),
    ('fifth_amendment',             'fifth',        'amendment',      'The fifth amendment protects against self incrimination'),
    ('free_speech',                 'free',         'speech',         'The free speech doctrine applies to public forums'),
    ('strict_liability',            'strict',       'liability',      'The strict liability standard applied to the manufacturer'),
    ('punitive_damages',            'punitive',     'damages',        'The punitive damages award exceeded ten million dollars'),
    ('sovereign_immunity',          'sovereign',    'immunity',       'The sovereign immunity doctrine shielded the government'),
    ('grand_indictment',            'grand',        'indictment',     'The grand indictment was handed down by the jury'),
    ('guilty_plea',                 'guilty',       'plea',           'A guilty plea was entered in exchange for reduced charges'),
    ('excessive_bail',              'excessive',    'bail',           'The excessive bail amount was challenged on appeal'),
    ('felony_conviction',           'felony',       'conviction',     'The felony conviction carried a mandatory minimum sentence'),
    ('conditional_parole',          'conditional',  'parole',         'The conditional parole required regular check ins'),
    ('joint_custody',               'joint',        'custody',        'The joint custody arrangement was approved by the court'),
    ('material_breach',             'material',     'breach',         'The material breach voided the entire agreement'),
    ('adequate_consideration',      'adequate',     'consideration',  'The adequate consideration requirement was not satisfied'),
    ('arbitration_clause',          'arbitration',  'clause',         'The arbitration clause required disputes be settled privately'),
    ('specific_performance',        'specific',     'performance',    'The specific performance remedy was granted by the court'),
    ('preliminary_injunction',      'preliminary',  'injunction',     'The preliminary injunction halted construction immediately'),
    ('oral_deposition',             'oral',         'deposition',     'The oral deposition lasted more than six hours'),
    ('personal_jurisdiction',       'personal',     'jurisdiction',   'The personal jurisdiction question was raised early'),
    ('electronic_discovery',        'electronic',   'discovery',      'The electronic discovery process produced thousands of documents'),
    ('summary_motion',              'summary',      'motion',         'A summary motion was filed to dismiss the case'),
    ('proper_venue',                'proper',       'venue',          'The proper venue for the trial was disputed'),
    ('patent_infringement',         'patent',       'infringement',   'The patent infringement suit was filed in federal court'),
    ('articles_incorporation',      'articles',     'incorporation',  'The articles incorporation were filed with the state'),
    ('hostile_merger',              'hostile',      'merger',         'The hostile merger attempt was blocked by the board'),
    ('statute_limitations',         'statute',      'limitations',    'The statute limitations period had already expired'),
    ('legal_standing',              'legal',        'standing',       'The legal standing requirement must be met before filing'),
    ('binding_precedent',           'binding',      'precedent',      'The binding precedent from the higher court controlled'),
    ('judicial_review',             'judicial',     'review',         'The judicial review process examined the agency decision'),
    ('civil_lawsuit',               'civil',        'lawsuit',        'The civil lawsuit was filed in state court last week'),
    ('criminal_record',             'criminal',     'record',         'His criminal record prevented him from getting the job'),
    ('search_warrant',              'search',       'warrant',        'The search warrant was issued by the federal judge'),
    ('plea_bargain',                'plea',         'bargain',        'The plea bargain reduced the sentence to five years'),
    ('witness_testimony',           'witness',      'testimony',      'The witness testimony contradicted the original statement'),
    ('expert_witness',              'expert',       'witness',        'An expert witness was called to explain the evidence'),
    ('court_order',                 'court',        'order',          'The court order required immediate compliance'),
    ('bench_trial',                 'bench',        'trial',          'The bench trial proceeded without a jury present'),
    ('jury_verdict',                'jury',         'verdict',        'The jury verdict was delivered after three days'),
    ('class_action',                'class',        'action',         'The class action included thousands of affected consumers'),
    ('double_jeopardy',             'double',       'jeopardy',       'The double jeopardy clause prevents being tried twice'),
    ('probable_cause',              'probable',     'cause',          'The probable cause standard must be met for an arrest'),
    ('restraining_order',           'restraining',  'order',          'A restraining order was granted to protect the victim'),
]

MEDICAL = [
    ('oxygen_saturation',           'oxygen',       'saturation',     'The oxygen saturation dropped below normal levels'),
    ('body_temperature',            'body',         'temperature',    'His body temperature was checked every four hours'),
    ('platelet_count',              'platelet',     'count',          'The platelet count was dangerously low'),
    ('metabolic_panel',             'metabolic',    'panel',          'A metabolic panel revealed elevated liver enzymes'),
    ('bacterial_infection',         'bacterial',    'infection',      'The blood culture confirmed a bacterial infection'),
    ('magnetic_resonance',          'magnetic',     'resonance',      'The magnetic resonance scan showed no abnormalities'),
    ('multiple_sclerosis',          'multiple',     'sclerosis',      'Multiple sclerosis affects the central nervous system'),
    ('complete_remission',          'complete',     'remission',      'The patient achieved complete remission after treatment'),
    ('bowel_resection',             'bowel',        'resection',      'The bowel resection was completed without complications'),
    ('organ_transplant',            'organ',        'transplant',     'An organ transplant requires lifelong medication'),
    ('therapeutic_dosage',          'therapeutic',  'dosage',         'The therapeutic dosage was adjusted based on lab results'),
    ('drug_interaction',            'drug',         'interaction',    'A drug interaction caused an unexpected side effect'),
    ('antibiotic_resistance',       'antibiotic',   'resistance',     'The antibiotic resistance made treatment more difficult'),
    ('gastrointestinal_absorption', 'gastrointestinal', 'absorption',     'The gastrointestinal absorption rate varied between patients'),
    ('respiratory_tract',           'respiratory',  'tract',          'The respiratory tract was inflamed from the infection'),
    ('cerebral_cortex',             'cerebral',     'cortex',         'The cerebral cortex processes sensory information'),
    ('informed_consent',            'informed',     'consent',        'The informed consent form was signed before the procedure'),
    ('clinical_trial',              'clinical',     'trial',          'The clinical trial enrolled five hundred participants'),
    ('nerve_damage',                'nerve',        'damage',         'The nerve damage caused numbness in her left hand'),
    ('chest_pain',                  'chest',        'pain',           'The chest pain started suddenly after dinner'),
    ('bone_marrow',                 'bone',         'marrow',         'The bone marrow sample was sent to the lab'),
    ('brain_stem',                  'brain',        'stem',           'The brain stem controls breathing and heart rate'),
    ('birth_defect',                'birth',        'defect',         'The birth defect was detected during the ultrasound'),
    ('wound_care',                  'wound',        'care',           'The wound care protocol was followed precisely'),
    ('pain_management',             'pain',         'management',     'The pain management plan included physical therapy'),
    ('blood_clot',                  'blood',        'clot',           'The blood clot was discovered during a routine scan'),
    ('tumor_growth',                'tumor',        'growth',         'The tumor growth was monitored every three months'),
    ('joint_replacement',           'joint',        'replacement',    'The joint replacement surgery was scheduled for Monday'),
    ('immune_response',             'immune',       'response',       'The immune response was stronger than expected'),
    ('viral_infection',             'viral',        'infection',      'The viral infection spread through the entire ward'),
    ('chronic_pain',                'chronic',      'pain',           'The chronic pain affected her ability to work'),
    ('mental_health',               'mental',       'health',         'The mental health evaluation was completed this morning'),
    ('spinal_cord',                 'spinal',       'cord',           'The spinal cord injury required emergency surgery'),
    ('scar_tissue',                 'scar',         'tissue',         'The scar tissue formed around the surgical site'),
    ('fluid_retention',             'fluid',        'retention',      'The fluid retention caused swelling in both legs'),
    ('sleep_apnea',                 'sleep',        'apnea',          'The sleep apnea diagnosis explained his constant fatigue'),
    ('muscle_spasm',                'muscle',       'spasm',          'The muscle spasm lasted for several painful minutes'),
    ('breast_cancer',               'breast',       'cancer',         'The breast cancer screening is recommended annually'),
    ('lung_cancer',                 'lung',         'cancer',         'The lung cancer diagnosis came as a complete shock'),
    ('skin_graft',                  'skin',         'graft',          'The skin graft healed well after the procedure'),
    ('stem_cell',                   'stem',         'cell',           'The stem cell therapy showed promising early results'),
    ('side_effect',                 'side',         'effect',         'The side effect was reported by several patients'),
]

FINANCE = [
    ('cash_flow',                   'cash',         'flow',           'The cash flow statement showed positive operating results'),
    ('balance_sheet',               'balance',      'sheet',          'The balance sheet reflected total assets and liabilities'),
    ('journal_entry',               'journal',      'entry',          'Each journal entry must have equal debits and credits'),
    ('accelerated_depreciation',    'accelerated',  'depreciation',   'The accelerated depreciation method reduced taxable income'),
    ('impairment_goodwill',         'impairment',   'goodwill',       'The impairment goodwill charge reduced reported earnings'),
    ('yield_maturity',              'yield',        'maturity',       'The yield maturity calculation determined the bond value'),
    ('bond_coupon',                 'bond',         'coupon',         'The bond coupon payment arrives every six months'),
    ('credit_spread',               'credit',       'spread',         'The credit spread widened during the market downturn'),
    ('modified_duration',           'modified',     'duration',       'The modified duration measure estimates interest rate risk'),
    ('interest_swap',               'interest',     'swap',           'An interest swap exchanges fixed for floating payments'),
    ('call_option',                 'call',         'option',         'A call option gives the right to buy at a set price'),
    ('commodity_futures',           'commodity',    'futures',        'The commodity futures contract expires next month'),
    ('currency_hedge',              'currency',     'hedge',          'A currency hedge protects against exchange rate movements'),
    ('implied_volatility',          'implied',      'volatility',     'The implied volatility rose sharply before the announcement'),
    ('zero_collar',                 'zero',         'collar',         'A zero collar strategy caps both gains and losses'),
    ('diluted_earnings',            'diluted',      'earnings',       'The diluted earnings per share declined this quarter'),
    ('price_ratio',                 'price',        'ratio',          'The price ratio suggested the stock was overvalued'),
    ('preferred_dividend',          'preferred',    'dividend',       'The preferred dividend was paid before common shareholders'),
    ('financial_leverage',          'financial',    'leverage',       'The financial leverage ratio exceeded industry standards'),
    ('debt_covenant',               'debt',         'covenant',       'The debt covenant restricted additional borrowing'),
    ('capital_structure',           'capital',      'structure',      'The capital structure included both equity and debt'),
    ('due_diligence',               'due',          'diligence',      'The due diligence review uncovered several risk factors'),
    ('public_offering',             'public',       'offering',       'The public offering raised two billion in new capital'),
    ('market_liquidity',            'market',       'liquidity',      'The market liquidity dried up during the crisis'),
    ('trade_settlement',            'trade',        'settlement',     'The trade settlement occurs two days after execution'),
    ('central_clearing',            'central',      'clearing',       'The central clearing house guaranteed all transactions'),
    ('maintenance_margin',          'maintenance',  'margin',         'The maintenance margin requirement triggered a call'),
    ('regulatory_compliance',       'regulatory',   'compliance',     'The regulatory compliance department reviewed the filing'),
    ('money_laundering',            'money',        'laundering',     'The money laundering investigation lasted several years'),
    ('asset_allocation',            'asset',        'allocation',     'The asset allocation strategy balanced growth and income'),
    ('systemic_risk',               'systemic',     'risk',           'The systemic risk assessment flagged several vulnerabilities'),
    ('stress_test',                 'stress',       'test',           'The stress test revealed weakness in the loan portfolio'),
    ('credit_default',              'credit',       'default',        'The credit default probability increased dramatically'),
    ('stock_market',                'stock',        'market',         'The stock market closed at a record high today'),
    ('mutual_fund',                 'mutual',       'fund',           'The mutual fund portfolio included both stocks and bonds'),
    ('hedge_fund',                  'hedge',        'fund',           'The hedge fund manager outperformed the benchmark'),
    ('bear_market',                 'bear',         'market',         'The bear market lasted for nearly eighteen months'),
    ('bull_market',                 'bull',         'market',         'The bull market drove prices to unprecedented levels'),
    ('credit_rating',               'credit',       'rating',         'The credit rating was downgraded after the earnings report'),
    ('tax_shelter',                 'tax',          'shelter',        "The tax shelter reduced the company's total liability"),
    ('venture_capital',             'venture',      'capital',        'The venture capital firm invested in early stage companies'),
    ('prime_rate',                  'prime',        'rate',           'The prime rate increased for the third consecutive quarter'),
    ('fiscal_policy',               'fiscal',       'policy',         'The fiscal policy change affected government spending levels'),
    ('trade_deficit',               'trade',        'deficit',        'The trade deficit widened to its largest level in years'),
]


def find_token_index(tokens, target):
    """
    Find the index of a target word in a list of tokens.
    Handles leading-space tokenization (e.g., ' screen' for 'screen')
    and subword splits (e.g., 'keyboard' -> ['Key', 'board']).

    For multi-token matches, returns the LAST subtoken index — that's
    where the composed representation lives after the model processes
    the subword sequence.

    Returns the index or None if not found.
    """
    target_lower = target.lower()

    # Pass 1: exact single-token match (stripped of whitespace)
    for i, tok in enumerate(tokens):
        if tok.strip().lower() == target_lower:
            return i

    # Pass 2: multi-token match — concatenate adjacent tokens
    for start in range(len(tokens)):
        concat = ""
        for end in range(start, len(tokens)):
            concat += tokens[end].strip().lower()
            if concat == target_lower:
                # Return the LAST token in the span
                return end
            if len(concat) > len(target_lower):
                break

    return None


def run_single_compound(model, compound_name, word1, word2, prompt, threshold=0.1):
    """
    Run binding analysis for a single compound pair.

    Returns list of dicts with layer, head, binding score for all heads
    (not just above threshold — threshold applied at analysis time).
    """
    tokens = model.to_str_tokens(prompt)

    # Find token indices
    idx1 = find_token_index(tokens, word1)
    idx2 = find_token_index(tokens, word2)

    if idx1 is None or idx2 is None:
        print(f"  WARNING: Could not find tokens for '{compound_name}'")
        print(f"    Looking for '{word1}' and '{word2}' in: {tokens}")
        return []

    # word2 attending to word1 (e.g., "reader" attending to "screen")
    target_idx = max(idx1, idx2)   # later token
    source_idx = min(idx1, idx2)   # earlier token

    logits, cache = model.run_with_cache(prompt)

    rows = []
    for layer in range(model.cfg.n_layers):
        attention = cache["pattern", layer]  # [batch, heads, seq, seq]
        for head in range(model.cfg.n_heads):
            attn = attention[0, head]  # [seq, seq]
            score = attn[target_idx, source_idx].item()
            rows.append({
                "compound": compound_name,
                "layer": layer,
                "head": head,
                "binding_score": round(score, 4),
                "word1": word1,
                "word2": word2,
                "prompt": prompt,
                "tokens": str(tokens),
                "word1_idx": source_idx,
                "word2_idx": target_idx,
            })

    return rows


def run_binding_sweep(model, model_name, project_root, compounds=None):
    """
    Run binding analysis for all compounds and save results.

    Args:
        model: A loaded TransformerLens model.
        model_name: Full model name (e.g. "EleutherAI/pythia-160m").
        project_root: Path to the project root directory.
        compounds: Optional list of (name, word1, word2, prompt) tuples.
                   Defaults to DEFAULT_COMPOUNDS.

    Returns:
        DataFrame with binding scores for all compounds × layers × heads.
    """
    if compounds is None:
        compounds = [
     'CONTROL',
     'ACCESSIBILITY',
     'MEDICAL',
     'LEGAL',
     'FINANCE'
]

    all_rows = []

    for compound_name, word1, word2, prompt in compounds:
        print(f"Running binding: {compound_name} (\"{prompt}\")")
        rows = run_single_compound(model, compound_name, word1, word2, prompt)
        all_rows.extend(rows)

    if not all_rows:
        print("WARNING: No binding data collected.")
        return pd.DataFrame()

    binding_df = pd.DataFrame(all_rows)
    binding_df["model"] = model_name

    # Save per-model CSV
    short_name = model_name.split('/')[-1]
    suite = 'pythia' if 'pythia' in short_name else 'gpt2'
    output_dir = Path(project_root) / 'results' / suite
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f'{short_name}-binding.csv'
    binding_df.to_csv(output_path, index=False)
    print(f"\nSaved {len(binding_df)} rows ({len(compounds)} compounds × "
          f"{model.cfg.n_layers} layers × {model.cfg.n_heads} heads) to {output_path}")

    # Print summary: top binding heads per compound
    print(f"\nTop binding heads per compound (threshold > 0.1):")
    for compound_name, _, _, _ in compounds:
        subset = binding_df[
            (binding_df['compound'] == compound_name) &
            (binding_df['binding_score'] > 0.1)
        ].sort_values('binding_score', ascending=False)
        if len(subset) > 0:
            top = subset.iloc[0]
            print(f"  {compound_name:25s} — L{int(top['layer']):2d}H{int(top['head']):2d} "
                  f"({top['binding_score']:.4f}), {len(subset)} heads above threshold")
        else:
            print(f"  {compound_name:25s} — no heads above threshold")

    return binding_df
