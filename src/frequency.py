"""
Corpus frequency — compound inventory and Infini-gram plumbing.

This module holds only what a reviewer would not ask about: the compound
inventory, the Infini-gram HTTP call with its retry/backoff, and per-suite
table I/O with schema validation.

It deliberately does NOT hold the mechanism. The query loop, the -1 sentinel
screen, the conditional-probability and PMI computations, and the correlation
itself live in readable cells in notebooks/frequency-{pythia,gpt2,olmo}.ipynb.
The test for where a line belongs: if a reviewer asked "how did you compute
this," a notebook should answer it without opening a module.

It also does NOT compute a Spearman. The pre-registered estimator has exactly
one implementation, src/dual_spearman.py, per DECISIONS 2026-07-03. A second
one lived here until 2026-08-09 and wrote its results to spearman_summary.csv
— the same path dual_spearman writes as PRIMARY — so the file under the
authoritative name held whichever estimator ran last.

Usage (from notebook):
    from src.frequency import (
        COMPOUNDS, FAILED_COUNT,
        query_infinigram, save_suite_frequency_table,
    )

    CORPUS_INDEX = "v4_piletrain_llama"        # named as a literal, not looked up
    ...                                        # query loop lives in the notebook
    save_suite_frequency_table(freq_df, PROJECT_ROOT, "pythia", CORPUS_INDEX)

Removed 2026-08-09 (zero external consumers; see git history):
    build_frequency_table         -> mechanism, now inline in the notebooks
    frequency_accuracy_correlation-> duplicate estimator, use dual_spearman
    run_frequency_analysis        -> wrote both colliding global filenames
    save_frequency_results        -> unused, stale output path
"""

import time
from pathlib import Path

import pandas as pd
import requests


# --------------------------------------------------------------------------- #
# Compound inventory                                                           #
# --------------------------------------------------------------------------- #
# Aligned with binding.py DEFAULT_COMPOUNDS and per_concept_trajectories.csv.
# Each entry: (concept_name, word1, word2, prompt)
# word1 and word2 are the compound components for frequency queries.
COMPOUNDS = [
    # ── Original compounds (with trajectory data) ────────────────────
    ("screen_reader",              "screen",      "reader",          "A screen reader is"),
    ("alt_text",                   "alt",         "text",            "The purpose of alt text is"),
    ("skip_link",                  "skip",        "link",            "A skip link is"),
    ("color_contrast",             "color",       "contrast",        "Color contrast is important because"),
    ("keyboard_navigation",        "keyboard",    "navigation",      "Keyboard navigation allows"),
    ("focus_indicator",            "focus",       "indicator",       "A focus indicator is"),
    ("semantic_html",              "semantic",    "HTML",            "Semantic HTML helps"),
    ("closed_captions",            "closed",      "captions",        "Closed captions display"),

    # ── Original domain pairs ───────────────────────────────────────
    ("keyboard_interaction",       "keyboard",    "interaction",     "My friend uses keyboard interaction to navigate a web site"),
    ("section_heading",            "section",     "heading",         "Web pages should have a section heading"),
    ("text_alternative",           "text",        "alternative",     "Provide a text alternative for non-text content"),
    ("audio_description",          "audio",       "description",     "There should be an audio description for prerecorded video content"),
    ("sign_language",              "sign",        "language",        "Sign language interpretation should be provided"),
    ("sensory_characteristics",    "sensory",     "characteristics", "You should not rely on sensory characteristics only to convey meaning"),
    ("input_purpose",              "input",       "purpose",         "Input purpose should be determined programmatically"),

    # ── WCAG compounds ──────────────────────────────────────────────
    ("target_size",                "target",      "size",            "The target size must be large enough to activate easily"),
    ("touch_target",               "touch",       "target",          "A touch target should be at least 24 pixels wide"),
    ("drag_movement",              "drag",        "movement",        "Any drag movement must have a single pointer alternative"),
    ("focus_appearance",           "focus",       "appearance",      "The focus appearance should meet minimum contrast requirements"),
    ("consistent_help",            "consistent",  "help",            "WCAG Guidelines require consistent help so users can find help completing tasks"),
    ("redundant_entry",            "redundant",   "entry",           "Forms should avoid redundant entry in the same session"),
    ("accessible_authentication",  "accessible",  "authentication",  "Websites need accessible authentication that does not rely on memory"),
    ("text_spacing",               "text",        "spacing",         "Text spacing can be adjusted without loss of content"),
    ("status_message",             "status",      "message",         "A status message should be announced without receiving focus"),
    ("error_identification",       "error",       "identification",  "Error identification must describe the problem in text"),
    ("pointer_cancellation",       "pointer",     "cancellation",    "The pointer cancellation feature allows users to abort clicks"),
    ("character_key",              "character",   "key",             "Character key shortcuts must be remappable by the user"),

    # ── MDN / ARIA compounds ────────────────────────────────────────
    ("accessibility_tree",         "accessibility", "tree",          "The accessibility tree exposes content to assistive technology"),
    ("accessible_name",            "accessible",  "name",            "An accessible name identifies an element for screen readers"),
    ("accessible_description",     "accessible",  "description",     "An accessible description provides additional context for users"),
    ("live_region",                "live",        "region",          "A live region announces dynamic content changes automatically"),
    ("tab_panel",                  "tab",         "panel",           "Each tab panel contains content for its associated tab"),
    ("radio_group",                "radio",       "group",           "A radio group contains mutually exclusive options"),
    ("tree_grid",                  "tree",        "grid",            "A tree grid combines a tree view with a data table"),
    ("menu_bar",                   "menu",        "bar",             "The menu bar provides top level navigation for the application"),
    ("tool_tip",                   "tool",        "tip",             "A tool tip provides additional information on hover"),
    ("combo_box",                  "combo",       "box",             "A combo box combines a text input with a dropdown list"),
    ("semantic_markup",            "semantic",    "markup",          "Authors should use semantic markup to convey meaning"),
    ("focus_management",           "focus",       "management",      "Focus management is critical for single page applications"),
    ("reading_order",              "reading",     "order",           "Reading order must match the visual layout of the page"),

    # ── Additional accessibility compounds ──────────────────────────
    ("text_formatting",            "text",        "formatting",      "Text formatting should not be the only way to convey meaning"),
    ("form_field",                 "form",        "field",           "Every form field must have a visible label"),
    ("landmark_region",            "landmark",    "region",          "A landmark region helps users navigate to major sections"),
    ("low_vision",                 "low",         "vision",          "People with low vision may need larger text and higher contrast"),
    ("cognitive_disabilities",     "cognitive",   "disabilities",    "Users with cognitive disabilities may need simpler language"),
    ("universal_design",           "universal",   "design",          "Universal design benefits all users regardless of ability"),
    ("decorative_image",           "decorative",  "image",           "A decorative image should have an empty alt attribute"),
    ("informative_image",          "informative", "image",           "An informative image must have meaningful alt text"),
    ("responsive_design",          "responsive",  "design",          "Modern responsive design should maintain accessibility at all sizes"),
    ("form_label",                 "form",        "label",           "A form label is"),
    ("link_text",                  "link",        "text",            "Link text describes"),
    ("page_title",                 "page",        "title",           "A page title describes"),
    ("empty_link",                 "empty",       "link",            "An empty link is"),
]

# --------------------------------------------------------------------------- #
# Domain comparison compounds                                                 #
# --------------------------------------------------------------------------- #
# control/legal/medical/finance compounds sourced from thatDangCircuit's
# final_*_pairs.py. NOT part of the default frequency run — Section 5's
# frequency-vs-trajectory analysis uses the accessibility set only. Kept here
# (not deleted) so the cross-domain version is one call away: pass these to
# build_frequency_table(compounds=COMPOUNDS + DOMAIN_COMPOUNDS). Their domains
# are already in COMPOUND_DOMAINS below.
DOMAIN_COMPOUNDS = [
    # ══ Control compounds (final_control_pairs.py) ════════════════════════
    # ── Original 8 ────────────────────────────────────────────────────
    ('blue_sky',                    'blue',         'sky',            'I like to look at the blue sky'),
    ('cold_water',                  'cold',         'water',          'She drank a glass of cold water'),
    ('ice_cream',                   'ice',          'cream',          'My favorite ice cream is chocolate'),
    ('life_jacket',                 'life',         'jacket',         'We took a life jacket on the boat'),
    ('tea_cup',                     'tea',          'cup',            'My tea cup is pink'),
    ('living_room',                 'living',       'room',           'Our house has a formal living room'),
    ('roller_coaster',              'roller',       'coaster',        'The roller coaster is my favorite ride'),
    ('school_bus',                  'school',       'bus',            'The school bus is yellow'),
    # ── Food and drink ────────────────────────────────────────────────
    ('grilled_cheese',              'grilled',      'cheese',         'She ordered a grilled cheese from the menu'),
    ('peanut_butter',               'peanut',       'butter',         'We need to buy peanut butter at the store'),
    ('hot_chocolate',               'hot',          'chocolate',      'He put whipped cream on his hot chocolate'),
    ('apple_pie',                   'apple',        'pie',            'The apple pie was still warm from the oven'),
    ('orange_juice',                'orange',       'juice',          'She drinks orange juice every morning'),
    ('baked_beans',                 'baked',        'beans',          'We had baked beans with dinner last night'),
    # ── Nature and weather ────────────────────────────────────────────
    ('palm_tree',                   'palm',         'tree',           'The palm tree swayed gently in the breeze'),
    ('thunder_storm',               'thunder',      'storm',          'A thunder storm rolled in from the west'),
    ('coral_reef',                  'coral',        'reef',           'The coral reef is home to many fish'),
    ('shooting_star',               'shooting',     'star',           'We watched the shooting star cross the sky'),
    ('mountain_lion',               'mountain',     'lion',           'The mountain lion was spotted near the trail'),
    ('tidal_wave',                  'tidal',        'wave',           'A tidal wave warning was issued for the coast'),
    # ── Home and everyday objects ─────────────────────────────────────
    ('dining_table',                'dining',       'table',          'The dining table seats six people comfortably'),
    ('car_keys',                    'car',          'keys',           'He left his car keys on the counter'),
    ('washing_machine',             'washing',      'machine',        'The washing machine is making a strange noise'),
    ('bath_towels',                 'bath',         'towels',         'She bought new bath towels for the guest room'),
    ('alarm_clock',                 'alarm',        'clock',          'The alarm clock went off at six in the morning'),
    ('light_bulb',                  'light',        'bulb',           'He replaced the light bulb in the hallway'),
    # ── Places and travel ─────────────────────────────────────────────
    ('post_office',                 'post',         'office',         'The post office closes at five on weekdays'),
    ('parking_lot',                 'parking',      'lot',            'We parked in the parking lot behind the building'),
    ('train_station',               'train',        'station',        'The train station is two blocks from here'),
    ('fire_station',                'fire',         'station',        'She works at the fire station downtown'),
    ('swimming_pool',               'swimming',     'pool',           'The swimming pool is open during the summer'),
    ('coffee_shop',                 'coffee',       'shop',           'They met at the coffee shop on the corner'),
    # ── Technology and general ────────────────────────────────────────
    ('hard_drive',                  'hard',         'drive',          'The hard drive stores all of your files'),
    ('operating_system',            'operating',    'system',         'She updated her operating system last night'),
    ('search_engine',               'search',       'engine',         'The search engine returned millions of results'),
    ('user_name',                   'user',         'name',           'He forgot his user name for the website'),
    ('power_supply',                'power',        'supply',         'The power supply was disconnected during the storm'),
    ('data_base',                   'data',         'base',           'A data base stores information in structured tables'),
    # ── Body and health ───────────────────────────────────────────────
    ('sore_throat',                 'sore',         'throat',         'She has a sore throat from the cold weather'),
    ('blood_pressure',              'blood',        'pressure',       'The blood pressure reading was perfectly normal'),
    ('collar_bone',                 'collar',       'bone',           'He broke his collar bone playing football'),
    ('heart_rate',                  'heart',        'rate',           'The heart rate monitor beeped steadily'),
    ('dental_appointment',          'dental',       'appointment',    'She scheduled a dental appointment for Tuesday'),
    ('waiting_room',                'waiting',      'room',           'The waiting room was full of patients'),

    # ══ Legal compounds (final_legal_pairs.py) ════════════════════════════
    # ── Constitutional ────────────────────────────────────────────────
    ('due_process',                 'due',          'process',        'The due process clause protects individual rights'),
    ('equal_protection',            'equal',        'protection',     'The equal protection argument was central to the case'),
    ('commerce_clause',             'commerce',     'clause',         'The commerce clause limits state regulatory power'),
    ('fifth_amendment',             'fifth',        'amendment',      'The fifth amendment protects against self incrimination'),
    ('free_speech',                 'free',         'speech',         'The free speech doctrine applies to public forums'),
    # ── Tort ──────────────────────────────────────────────────────────
    ('strict_liability',            'strict',       'liability',      'The strict liability standard applied to the manufacturer'),
    ('punitive_damages',            'punitive',     'damages',        'The punitive damages award exceeded ten million dollars'),
    ('sovereign_immunity',          'sovereign',    'immunity',       'The sovereign immunity doctrine shielded the government'),
    # ── Criminal ──────────────────────────────────────────────────────
    ('grand_indictment',            'grand',        'indictment',     'The grand indictment was handed down by the jury'),
    ('guilty_plea',                 'guilty',       'plea',           'A guilty plea was entered in exchange for reduced charges'),
    ('excessive_bail',              'excessive',    'bail',           'The excessive bail amount was challenged on appeal'),
    ('felony_conviction',           'felony',       'conviction',     'The felony conviction carried a mandatory minimum sentence'),
    ('conditional_parole',          'conditional',  'parole',         'The conditional parole required regular check ins'),
    ('joint_custody',               'joint',        'custody',        'The joint custody arrangement was approved by the court'),
    # ── Contract ──────────────────────────────────────────────────────
    ('material_breach',             'material',     'breach',         'The material breach voided the entire agreement'),
    ('adequate_consideration',      'adequate',     'consideration',  'The adequate consideration requirement was not satisfied'),
    ('arbitration_clause',          'arbitration',  'clause',         'The arbitration clause required disputes be settled privately'),
    ('specific_performance',        'specific',     'performance',    'The specific performance remedy was granted by the court'),
    # ── Procedure ─────────────────────────────────────────────────────
    ('preliminary_injunction',      'preliminary',  'injunction',     'The preliminary injunction halted construction immediately'),
    ('oral_deposition',             'oral',         'deposition',     'The oral deposition lasted more than six hours'),
    ('personal_jurisdiction',       'personal',     'jurisdiction',   'The personal jurisdiction question was raised early'),
    ('electronic_discovery',        'electronic',   'discovery',      'The electronic discovery process produced thousands of documents'),
    ('summary_motion',              'summary',      'motion',         'A summary motion was filed to dismiss the case'),
    ('proper_venue',                'proper',       'venue',          'The proper venue for the trial was disputed'),
    # ── IP/Corporate ──────────────────────────────────────────────────
    ('patent_infringement',         'patent',       'infringement',   'The patent infringement suit was filed in federal court'),
    ('articles_incorporation',      'articles',     'incorporation',  'The articles incorporation were filed with the state'),
    ('hostile_merger',              'hostile',      'merger',         'The hostile merger attempt was blocked by the board'),
    # ── Statutory ─────────────────────────────────────────────────────
    ('statute_limitations',         'statute',      'limitations',    'The statute limitations period had already expired'),
    ('legal_standing',              'legal',        'standing',       'The legal standing requirement must be met before filing'),
    ('binding_precedent',           'binding',      'precedent',      'The binding precedent from the higher court controlled'),
    ('judicial_review',             'judicial',     'review',         'The judicial review process examined the agency decision'),
    # ── Replacements (for Latin/long-word compounds lost to tokenization) ───
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

    # ══ Medical compounds (final_medical_pairs.py) ════════════════════════
    # blood_pressure and heart_rate live in the control set above (skipped here).
    # ── Vitals ────────────────────────────────────────────────────────
    ('oxygen_saturation',           'oxygen',       'saturation',     'The oxygen saturation dropped below normal levels'),
    ('body_temperature',            'body',         'temperature',    'His body temperature was checked every four hours'),
    # ── Lab/Diagnostics ───────────────────────────────────────────────
    ('platelet_count',              'platelet',     'count',          'The platelet count was dangerously low'),
    ('metabolic_panel',             'metabolic',    'panel',          'A metabolic panel revealed elevated liver enzymes'),
    ('bacterial_infection',         'bacterial',    'infection',      'The blood culture confirmed a bacterial infection'),
    # ── Imaging ───────────────────────────────────────────────────────
    ('magnetic_resonance',          'magnetic',     'resonance',      'The magnetic resonance scan showed no abnormalities'),
    # ── Conditions ────────────────────────────────────────────────────
    ('multiple_sclerosis',          'multiple',     'sclerosis',      'Multiple sclerosis affects the central nervous system'),
    # ── Oncology ──────────────────────────────────────────────────────
    ('complete_remission',          'complete',     'remission',      'The patient achieved complete remission after treatment'),
    # ── Surgical ──────────────────────────────────────────────────────
    ('bowel_resection',             'bowel',        'resection',      'The bowel resection was completed without complications'),
    ('organ_transplant',            'organ',        'transplant',     'An organ transplant requires lifelong medication'),
    # ── Pharmacology ──────────────────────────────────────────────────
    ('therapeutic_dosage',          'therapeutic',  'dosage',         'The therapeutic dosage was adjusted based on lab results'),
    ('drug_interaction',            'drug',         'interaction',    'A drug interaction caused an unexpected side effect'),
    ('antibiotic_resistance',       'antibiotic',   'resistance',     'The antibiotic resistance made treatment more difficult'),
    ('gastrointestinal_absorption', 'gastrointestinal', 'absorption',     'The gastrointestinal absorption rate varied between patients'),
    # ── Anatomy ───────────────────────────────────────────────────────
    ('respiratory_tract',           'respiratory',  'tract',          'The respiratory tract was inflamed from the infection'),
    ('cerebral_cortex',             'cerebral',     'cortex',         'The cerebral cortex processes sensory information'),
    # ── Clinical Practice ─────────────────────────────────────────────
    ('informed_consent',            'informed',     'consent',        'The informed consent form was signed before the procedure'),
    ('clinical_trial',              'clinical',     'trial',          'The clinical trial enrolled five hundred participants'),
    # ── Replacements (common medical terms, clean tokenization) ───────
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

    # ══ Finance compounds (final_finance_pairs.py) ════════════════════════
    # ── Accounting ────────────────────────────────────────────────────
    ('cash_flow',                   'cash',         'flow',           'The cash flow statement showed positive operating results'),
    ('balance_sheet',               'balance',      'sheet',          'The balance sheet reflected total assets and liabilities'),
    ('journal_entry',               'journal',      'entry',          'Each journal entry must have equal debits and credits'),
    ('accelerated_depreciation',    'accelerated',  'depreciation',   'The accelerated depreciation method reduced taxable income'),
    ('impairment_goodwill',         'impairment',   'goodwill',       'The impairment goodwill charge reduced reported earnings'),
    # ── Fixed Income ──────────────────────────────────────────────────
    ('yield_maturity',              'yield',        'maturity',       'The yield maturity calculation determined the bond value'),
    ('bond_coupon',                 'bond',         'coupon',         'The bond coupon payment arrives every six months'),
    ('credit_spread',               'credit',       'spread',         'The credit spread widened during the market downturn'),
    ('modified_duration',           'modified',     'duration',       'The modified duration measure estimates interest rate risk'),
    # ── Derivatives ───────────────────────────────────────────────────
    ('interest_swap',               'interest',     'swap',           'An interest swap exchanges fixed for floating payments'),
    ('call_option',                 'call',         'option',         'A call option gives the right to buy at a set price'),
    ('commodity_futures',           'commodity',    'futures',        'The commodity futures contract expires next month'),
    ('currency_hedge',              'currency',     'hedge',          'A currency hedge protects against exchange rate movements'),
    ('implied_volatility',          'implied',      'volatility',     'The implied volatility rose sharply before the announcement'),
    ('zero_collar',                 'zero',         'collar',         'A zero collar strategy caps both gains and losses'),
    # ── Equities ──────────────────────────────────────────────────────
    ('diluted_earnings',            'diluted',      'earnings',       'The diluted earnings per share declined this quarter'),
    ('price_ratio',                 'price',        'ratio',          'The price ratio suggested the stock was overvalued'),
    ('preferred_dividend',          'preferred',    'dividend',       'The preferred dividend was paid before common shareholders'),
    # ── Corporate Finance ─────────────────────────────────────────────
    ('financial_leverage',          'financial',    'leverage',       'The financial leverage ratio exceeded industry standards'),
    ('debt_covenant',               'debt',         'covenant',       'The debt covenant restricted additional borrowing'),
    ('capital_structure',           'capital',      'structure',      'The capital structure included both equity and debt'),
    ('due_diligence',               'due',          'diligence',      'The due diligence review uncovered several risk factors'),
    ('public_offering',             'public',       'offering',       'The public offering raised two billion in new capital'),
    # ── Markets ───────────────────────────────────────────────────────
    ('market_liquidity',            'market',       'liquidity',      'The market liquidity dried up during the crisis'),
    ('trade_settlement',            'trade',        'settlement',     'The trade settlement occurs two days after execution'),
    ('central_clearing',            'central',      'clearing',       'The central clearing house guaranteed all transactions'),
    ('maintenance_margin',          'maintenance',  'margin',         'The maintenance margin requirement triggered a call'),
    # ── Banking/Regulation ────────────────────────────────────────────
    ('regulatory_compliance',       'regulatory',   'compliance',     'The regulatory compliance department reviewed the filing'),
    ('money_laundering',            'money',        'laundering',     'The money laundering investigation lasted several years'),
    # ── Portfolio/Risk ────────────────────────────────────────────────
    ('asset_allocation',            'asset',        'allocation',     'The asset allocation strategy balanced growth and income'),
    ('systemic_risk',               'systemic',     'risk',           'The systemic risk assessment flagged several vulnerabilities'),
    ('stress_test',                 'stress',       'test',           'The stress test revealed weakness in the loan portfolio'),
    ('credit_default',              'credit',       'default',        'The credit default probability increased dramatically'),
    # ── Replacements (for compounds lost to tokenization) ─────────────
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

# Single-word concepts — excluded from compound frequency analysis.
# These don't have bigrams and require different treatment.
# Can be analyzed separately if needed.
SINGLE_CONCEPTS = [
    ("WCAG",                "WCAG",     None,        "WCAG stands for"),
    ("ARIA",                "ARIA",     None,        "ARIA stands for"),
]


# --------------------------------------------------------------------------- #
# Compound → domain map                                                        #
# --------------------------------------------------------------------------- #
# Every compound in COMPOUNDS tagged with its domain. Accessibility is the test
# domain; control/legal/medical/finance are the comparison domains sourced from
# thatDangCircuit's final_*_pairs.py. blood_pressure and heart_rate appear in
# both the control and medical sets — they're tagged "control" (kept once).
COMPOUND_DOMAINS = {
    # ── Accessibility (test domain) ──
    "screen_reader":                "accessibility",
    "alt_text":                     "accessibility",
    "skip_link":                    "accessibility",
    "color_contrast":               "accessibility",
    "keyboard_navigation":          "accessibility",
    "focus_indicator":              "accessibility",
    "semantic_html":                "accessibility",
    "closed_captions":              "accessibility",
    "keyboard_interaction":         "accessibility",
    "section_heading":              "accessibility",
    "text_alternative":             "accessibility",
    "audio_description":            "accessibility",
    "sign_language":                "accessibility",
    "sensory_characteristics":      "accessibility",
    "input_purpose":                "accessibility",
    "target_size":                  "accessibility",
    "touch_target":                 "accessibility",
    "drag_movement":                "accessibility",
    "focus_appearance":             "accessibility",
    "consistent_help":              "accessibility",
    "redundant_entry":              "accessibility",
    "accessible_authentication":    "accessibility",
    "text_spacing":                 "accessibility",
    "status_message":               "accessibility",
    "error_identification":         "accessibility",
    "pointer_cancellation":         "accessibility",
    "character_key":                "accessibility",
    "accessibility_tree":           "accessibility",
    "accessible_name":              "accessibility",
    "accessible_description":       "accessibility",
    "live_region":                  "accessibility",
    "tab_panel":                    "accessibility",
    "radio_group":                  "accessibility",
    "tree_grid":                    "accessibility",
    "menu_bar":                     "accessibility",
    "tool_tip":                     "accessibility",
    "combo_box":                    "accessibility",
    "semantic_markup":              "accessibility",
    "focus_management":             "accessibility",
    "reading_order":                "accessibility",
    "text_formatting":              "accessibility",
    "form_field":                   "accessibility",
    "landmark_region":              "accessibility",
    "low_vision":                   "accessibility",
    "cognitive_disabilities":       "accessibility",
    "universal_design":             "accessibility",
    "decorative_image":             "accessibility",
    "informative_image":            "accessibility",
    "responsive_design":            "accessibility",
    "form_label":                   "accessibility",
    "link_text":                    "accessibility",
    "page_title":                   "accessibility",
    "empty_link":                   "accessibility",
    # ── Control ──
    "blue_sky":                     "control",
    "cold_water":                   "control",
    "ice_cream":                    "control",
    "life_jacket":                  "control",
    "tea_cup":                      "control",
    "living_room":                  "control",
    "roller_coaster":               "control",
    "school_bus":                   "control",
    "grilled_cheese":               "control",
    "peanut_butter":                "control",
    "hot_chocolate":                "control",
    "apple_pie":                    "control",
    "orange_juice":                 "control",
    "baked_beans":                  "control",
    "palm_tree":                    "control",
    "thunder_storm":                "control",
    "coral_reef":                   "control",
    "shooting_star":                "control",
    "mountain_lion":                "control",
    "tidal_wave":                   "control",
    "dining_table":                 "control",
    "car_keys":                     "control",
    "washing_machine":              "control",
    "bath_towels":                  "control",
    "alarm_clock":                  "control",
    "light_bulb":                   "control",
    "post_office":                  "control",
    "parking_lot":                  "control",
    "train_station":                "control",
    "fire_station":                 "control",
    "swimming_pool":                "control",
    "coffee_shop":                  "control",
    "hard_drive":                   "control",
    "operating_system":             "control",
    "search_engine":                "control",
    "user_name":                    "control",
    "power_supply":                 "control",
    "data_base":                    "control",
    "sore_throat":                  "control",
    "blood_pressure":               "control",
    "collar_bone":                  "control",
    "heart_rate":                   "control",
    "dental_appointment":           "control",
    "waiting_room":                 "control",
    # ── Legal ──
    "due_process":                  "legal",
    "equal_protection":             "legal",
    "commerce_clause":              "legal",
    "fifth_amendment":              "legal",
    "free_speech":                  "legal",
    "strict_liability":             "legal",
    "punitive_damages":             "legal",
    "sovereign_immunity":           "legal",
    "grand_indictment":             "legal",
    "guilty_plea":                  "legal",
    "excessive_bail":               "legal",
    "felony_conviction":            "legal",
    "conditional_parole":           "legal",
    "joint_custody":                "legal",
    "material_breach":              "legal",
    "adequate_consideration":       "legal",
    "arbitration_clause":           "legal",
    "specific_performance":         "legal",
    "preliminary_injunction":       "legal",
    "oral_deposition":              "legal",
    "personal_jurisdiction":        "legal",
    "electronic_discovery":         "legal",
    "summary_motion":               "legal",
    "proper_venue":                 "legal",
    "patent_infringement":          "legal",
    "articles_incorporation":       "legal",
    "hostile_merger":               "legal",
    "statute_limitations":          "legal",
    "legal_standing":               "legal",
    "binding_precedent":            "legal",
    "judicial_review":              "legal",
    "civil_lawsuit":                "legal",
    "criminal_record":              "legal",
    "search_warrant":               "legal",
    "plea_bargain":                 "legal",
    "witness_testimony":            "legal",
    "expert_witness":               "legal",
    "court_order":                  "legal",
    "bench_trial":                  "legal",
    "jury_verdict":                 "legal",
    "class_action":                 "legal",
    "double_jeopardy":              "legal",
    "probable_cause":               "legal",
    "restraining_order":            "legal",
    # ── Medical ──
    "oxygen_saturation":            "medical",
    "body_temperature":             "medical",
    "platelet_count":               "medical",
    "metabolic_panel":              "medical",
    "bacterial_infection":          "medical",
    "magnetic_resonance":           "medical",
    "multiple_sclerosis":           "medical",
    "complete_remission":           "medical",
    "bowel_resection":              "medical",
    "organ_transplant":             "medical",
    "therapeutic_dosage":           "medical",
    "drug_interaction":             "medical",
    "antibiotic_resistance":        "medical",
    "gastrointestinal_absorption":  "medical",
    "respiratory_tract":            "medical",
    "cerebral_cortex":              "medical",
    "informed_consent":             "medical",
    "clinical_trial":               "medical",
    "nerve_damage":                 "medical",
    "chest_pain":                   "medical",
    "bone_marrow":                  "medical",
    "brain_stem":                   "medical",
    "birth_defect":                 "medical",
    "wound_care":                   "medical",
    "pain_management":              "medical",
    "blood_clot":                   "medical",
    "tumor_growth":                 "medical",
    "joint_replacement":            "medical",
    "immune_response":              "medical",
    "viral_infection":              "medical",
    "chronic_pain":                 "medical",
    "mental_health":                "medical",
    "spinal_cord":                  "medical",
    "scar_tissue":                  "medical",
    "fluid_retention":              "medical",
    "sleep_apnea":                  "medical",
    "muscle_spasm":                 "medical",
    "breast_cancer":                "medical",
    "lung_cancer":                  "medical",
    "skin_graft":                   "medical",
    "stem_cell":                    "medical",
    "side_effect":                  "medical",
    # ── Finance ──
    "cash_flow":                    "finance",
    "balance_sheet":                "finance",
    "journal_entry":                "finance",
    "accelerated_depreciation":     "finance",
    "impairment_goodwill":          "finance",
    "yield_maturity":               "finance",
    "bond_coupon":                  "finance",
    "credit_spread":                "finance",
    "modified_duration":            "finance",
    "interest_swap":                "finance",
    "call_option":                  "finance",
    "commodity_futures":            "finance",
    "currency_hedge":               "finance",
    "implied_volatility":           "finance",
    "zero_collar":                  "finance",
    "diluted_earnings":             "finance",
    "price_ratio":                  "finance",
    "preferred_dividend":           "finance",
    "financial_leverage":           "finance",
    "debt_covenant":                "finance",
    "capital_structure":            "finance",
    "due_diligence":                "finance",
    "public_offering":              "finance",
    "market_liquidity":             "finance",
    "trade_settlement":             "finance",
    "central_clearing":             "finance",
    "maintenance_margin":           "finance",
    "regulatory_compliance":        "finance",
    "money_laundering":             "finance",
    "asset_allocation":             "finance",
    "systemic_risk":                "finance",
    "stress_test":                  "finance",
    "credit_default":               "finance",
    "stock_market":                 "finance",
    "mutual_fund":                  "finance",
    "hedge_fund":                   "finance",
    "bear_market":                  "finance",
    "bull_market":                  "finance",
    "credit_rating":                "finance",
    "tax_shelter":                  "finance",
    "venture_capital":              "finance",
    "prime_rate":                   "finance",
    "fiscal_policy":                "finance",
    "trade_deficit":                "finance",
}


# --------------------------------------------------------------------------- #
# Infini-gram API                                                              #
# --------------------------------------------------------------------------- #
INFINIGRAM_API = "https://api.infini-gram.io/"

# Corpus indices, for reference only. These are deliberately NOT defaults, and
# there is deliberately no suite -> index mapping in this module:
#
#   v4_piletrain_llama       Pile-train, Llama-2 tokenizer, 380B tokens.
#                            pythia (exact — Pile is the training corpus)
#                            gpt2   (proxy — WebText is not public)
#   v4_olmo-mix-1124_llama   OLMo-Mix-1124, Llama-2 tokenizer.
#                            olmo   (exact)
#
# Each frequency notebook names its index as a literal in its first cells, so
# the corpus that produced a number is visible in the notebook that produced
# it. Audit finding A4 is what a lookup table costs: the primary path consulted
# the dict correctly and the robustness paths did not, and four contradictory
# OLMo rho values ended up on disk with no way to tell them apart.

#: Infini-gram returns this as a count when a lookup fails after all retries.
#: It is never a real count. Screen it to NaN before it reaches any statistic —
#: it is not caught by dropna(), and as the smallest value it would take the
#: bottom rank in a Spearman.
FAILED_COUNT = -1


def query_infinigram(ngram, index, retries=5, delay=2.0):
    """Query Infini-gram for the count of an n-gram in a corpus.

    Args:
        ngram: string to count (e.g. "skip link", "screen reader").
            Case-sensitive. Tokenized by Infini-gram server-side.
        index: corpus index. REQUIRED — there is no default on purpose. A
            default here is how a robustness path silently used Pile counts
            for OLMo (A4); with none, forgetting it raises at the call site.
        retries: number of retry attempts on failure.
        delay: seconds between retries.

    Returns:
        dict with keys: ngram, count, approx, tokens, latency_ms.
        On failure after retries: count=FAILED_COUNT (-1) and an error key.

    Note: the Pile-train index uses the Llama-2 tokenizer, not Pythia's
    GPT-NeoX tokenizer. For regular English words this doesn't affect
    counts. For acronyms (WCAG, ARIA) or unusual tokens, verify that
    the tokenization shown in the response matches expectations.
    """
    payload = {
        "index": index,
        "query_type": "count",
        "query": ngram,
    }

    for attempt in range(retries):
        try:
            resp = requests.post(INFINIGRAM_API, json=payload, timeout=30)

            # Rate limited — back off and retry
            if resp.status_code == 403:
                wait = delay * (2 ** attempt)
                print(f"  Rate limited on '{ngram}', waiting {wait:.0f}s (attempt {attempt + 1}/{retries})")
                time.sleep(wait)
                continue

            resp.raise_for_status()
            data = resp.json()

            if "error" in data:
                print(f"  API error for '{ngram}': {data['error']}")
                return {"ngram": ngram, "count": FAILED_COUNT, "error": data["error"]}

            return {
                "ngram": ngram,
                "count": data["count"],
                "approx": data.get("approx", False),
                "tokens": data.get("tokens", []),
                "latency_ms": round(data.get("latency", 0), 1),
            }
        except Exception as e:
            if attempt < retries - 1:
                print(f"  Retry {attempt + 1}/{retries} for '{ngram}': {e}")
                time.sleep(delay)
            else:
                print(f"  Failed after {retries} attempts for '{ngram}': {e}")
                return {"ngram": ngram, "count": FAILED_COUNT, "error": str(e)}

    # All retries exhausted by persistent rate-limiting (403). Degrade like the
    # exception path above — return the sentinel so the caller records a miss
    # and moves on, instead of returning None and crashing.
    print(f"  Rate limited out after {retries} attempts for '{ngram}'")
    return {"ngram": ngram, "count": FAILED_COUNT, "error": "rate_limited"}


# --------------------------------------------------------------------------- #
# Per-suite table I/O                                                          #
# --------------------------------------------------------------------------- #
# One suite, one file, one writer. The frequency notebooks are the only
# writers; src/dual_spearman.py is the only reader. Nothing writes a global
# results/frequency/frequency_table.csv any more — that file is a frozen Pile
# artifact (see its sibling frequency_table.README.md) and a pipeline that can
# overwrite a frozen artifact makes it not frozen.

FREQUENCY_TABLE_COLUMNS = [
    "compound", "domain", "word1", "word2",
    "bigram_count", "word1_count", "word2_count",
    "conditional_prob", "pmi", "corpus_index",
]

COUNT_COLUMNS = ["bigram_count", "word1_count", "word2_count"]


def suite_frequency_table_path(project_root, suite):
    """Canonical path for a suite's frequency table."""
    return (Path(project_root) / "results" / "frequency" / suite /
            f"{suite}_frequency_table.csv")


def save_suite_frequency_table(freq_df, project_root, suite, index):
    """Write results/frequency/{suite}/{suite}_frequency_table.csv.

    Plumbing only — schema validation, provenance stamping, file I/O. The
    query loop and the FAILED_COUNT screen live in the notebook, where a
    reviewer can read them.

    Stamps every row with `corpus_index` so provenance is recoverable from the
    artifact rather than from the notebook that produced it.

    Args:
        freq_df: DataFrame with at least the non-provenance columns of
            FREQUENCY_TABLE_COLUMNS. Failed lookups must already be NaN.
        project_root: path to the tmlr repo root.
        suite: 'pythia' | 'gpt2' | 'olmo'.
        index: the Infini-gram index this table was queried against.

    Returns:
        Path to the written file.

    Raises:
        ValueError: if required columns are missing, or if a negative count
            survived — which means the FAILED_COUNT screen was skipped.
    """
    df = freq_df.copy()
    df["corpus_index"] = index

    missing = [c for c in FREQUENCY_TABLE_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"{suite}: frequency table missing columns {missing}")
    df = df[FREQUENCY_TABLE_COLUMNS]

    # A negative count here means the notebook did not screen FAILED_COUNT.
    # Fail loudly rather than writing a -1 that a later Spearman would rank.
    for col in COUNT_COLUMNS:
        n_bad = int((df[col] < 0).sum())
        if n_bad:
            raise ValueError(
                f"{suite}: {n_bad} negative value(s) in {col} — the "
                f"Infini-gram {FAILED_COUNT} sentinel reached save unscreened")

    out = suite_frequency_table_path(project_root, suite)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False, lineterminator="\n")

    n_screened = int(df["bigram_count"].isna().sum())
    print(f"{suite}: wrote {len(df)} rows -> {out}")
    print(f"{suite}: corpus_index = {index}")
    print(f"{suite}: {n_screened} row(s) have no usable bigram count")
    return out


def load_suite_frequency_table(project_root, suite):
    """Read a suite's frequency table and the corpus index it records.

    Args:
        project_root: path to the tmlr repo root.
        suite: 'pythia' | 'gpt2' | 'olmo'.

    Returns:
        (df, corpus_index) — the table, and the single index string it carries.

    Raises:
        FileNotFoundError: if the suite has no table yet.
        ValueError: if the table carries more than one corpus_index, which
            would mean two corpora were merged into one set of x-values.
    """
    path = suite_frequency_table_path(project_root, suite)
    if not path.exists():
        raise FileNotFoundError(
            f"{suite}: no per-suite frequency table at {path}. "
            f"Run notebooks/frequency-{suite}.ipynb first.")

    df = pd.read_csv(path)
    found = sorted(df["corpus_index"].dropna().unique())
    if len(found) != 1:
        raise ValueError(
            f"{suite}: expected exactly one corpus_index in {path}, "
            f"found {found}")
    return df, found[0]
