"""
Accuracy coding for elicitation experiment responses.

Each response is coded as 'correct', 'partial', or 'incorrect' based on
whether it captures the accessibility-relevant meaning of the concept.

Coding criteria are documented inline. These rules are the methodology —
changes to coding criteria must be documented in DECISIONS.md.

Usage:
    from src.accuracy_coding import code_response
    df['accuracy'] = df.apply(
        lambda r: code_response(r['prompt_type'], r['concept'], r['prompt'], r['output']),
        axis=1
    )
"""


# ===========================================================================
# n=49 EXPANSION — coding doctrine (authored blind 2026-07-02/03; translated
# from docs/findings/criteria_authoring.csv per criteria-handoff-2026-07-03.md)
#
# CODING DOCTRINE (verbatim from DECISIONS.md 2026-07-03; governs the 41 new
# declarative rules below — Trisha's semantics, mechanical translation only):
#   1. LATERAL confusion (wrong mirror: AD<->captions, decorative<->informative,
#      semantic-web-for-semantic-markup) -> INCORRECT.
#   2. VERTICAL confusion (instance-for-umbrella: alt-text-for-text-alternative;
#      tab-for-tabpanel; name-collapse on description) -> PARTIAL.
#   3. SYNONYM pairs (target_size <-> touch_target) -> cross-definition NODS.
#   4. MECHANISM-FOR-CONCEPT (attribute-as-the-thing) — severity is PER-ROW:
#      where the mechanism constitutes the concept (aria-live for live region)
#      -> nods; where the mechanism is categorically different plumbing
#      (aria-describedby for accessible description, per 2026-07-03 veto)
#      -> INCORRECT.
#   5. TRENCH COAT (compound restated with a modal verb: "help should be
#      consistent") -> circular -> INCORRECT. tc always loses.
#
# Translation convention (matches the original 8's house pattern):
#   - correct requires the DISTINGUISHING content markers, not the compound
#     tokens alone — so circular / trench-coat restatements fail by omission
#     (they carry the compound words but not the distinguishing markers),
#     implementing doctrine plank 5 without a separate circular detector.
#   - lateral / wrong-domain traps flagged in the worksheet's incorrect_markers
#     become negative guards (cf. the original focus_indicator 'camera' guard).
#   - degenerate repetition is flagged separately by _is_degenerate() in
#     gap_analysis.py (feeds the degenerate tables, not accuracy).
#
# Sense policy: Option A (general technical sense counts as correct) + per-
# response sense recording — see observe_sense() below. All 41 criteria are now
# authored, so PENDING_CRITERIA is empty; the guard remains as a documented
# no-op. Regression guard: the original concepts' coded outputs are byte-
# identical before/after (verified 2026-07-03).
# ===========================================================================

PENDING_CRITERIA = set()  # all 41 expansion criteria authored 2026-07-03


def _has(text, *subs):
    """True if any substring in *subs appears in text (text pre-lowercased)."""
    return any(s in text for s in subs)


# ---------------------------------------------------------------------------
# Sense recording (Option A + dual analysis; DECISIONS 2026-07-02/03)
#
# Per-response sense_observed in {a11y, generic}: a11y if the response carries
# any GLOBAL a11y marker OR any of the compound-specific markers authored in the
# worksheet's `a11y_sense_markers` column. Common markers are hoisted to the
# global list; the per-compound dict supplies the additions. Feeds the dual
# Spearman (all rows / a11y-sense-only).
# ---------------------------------------------------------------------------

GLOBAL_A11Y_MARKERS = (
    'screen reader', 'assistive', 'wcag', 'announce', 'blind',
    'low vision', 'keyboard-only', 'aria', 'alt text',
)

# Compound-specific additions (from criteria_authoring.csv `a11y_sense_markers`,
# minus tokens already in the global list; normalized to lowercase substrings).
A11Y_SENSE_MARKERS = {
    'keyboard interaction': ('focus indicator', 'motor'),
    'section heading': ('navigate by headings', 'heading level', 'skipped level'),
    'text alternative': ('non-text',),
    'audio description': (),  # fully covered by global (blind/low vision/screen reader/assistive/wcag)
    'sign language': ('interpret', 'deaf', 'media', 'video', 'provided', 'aaa'),
    'sensory characteristics': ('color blind', 'colour blind'),
    'input purpose': ('autocomplete', 'autofill', 'programmatically determinable', 'cognitive'),
    'target size': ('motor', 'touch', 'tremor', '24px', 'spacing'),
    'touch target': ('motor', 'mobile', 'finger', '24px', 'spacing'),
    'drag movement': ('motor', 'tremor', 'single pointer', 'alternative'),
    'focus appearance': ('keyboard', 'focus indicator', 'contrast', ':focus'),
    'consistent help': ('cognitive', 'find help', 'relative order'),
    'redundant entry': ('cognitive', 'memory', 'auto-populate', 'fatigue'),
    'accessible authentication': ('cognitive', 'memory', 'password manager', 'paste', 'passkey'),
    'text spacing': ('dyslexia', 'cognitive', 'user stylesheet', 'readability'),
    'status message': ('aria-live', 'role=status', 'focus'),
    'error identification': ('color alone', 'form validation'),
    'pointer cancellation': ('motor', 'tremor', 'accidental activation', 'up event'),
    'character key': ('speech input', 'voice control', 'accidental activation', 'remap'),
    'accessibility tree': ('assistive technology', 'role', 'exposed', 'platform accessibility'),
    'accessible name': ('accname', 'label'),
    'accessible description': ('supplementary', 'hint'),
    'live region': ('aria-live', 'polite', 'assertive', 'role=status', 'role=alert'),
    'tab panel': ('role=tabpanel', 'aria-controls', 'aria-labelledby', 'keyboard', 'arrow keys'),
    'radio group': ('fieldset', 'legend', 'role=radiogroup', 'arrow keys'),
    'tree grid': ('role=treegrid', 'aria-expanded', 'aria-level', 'arrow keys'),
    'menu bar': ('role=menubar', 'aria-orientation', 'arrow keys', 'keyboard'),
    'tool tip': ('focus', 'keyboard', 'role=tooltip', 'aria-describedby', 'dismissible', '1.4.13'),
    'combo box': ('role=combobox', 'aria-expanded', 'aria-activedescendant', 'autocomplete', 'keyboard'),
    'landmark region': ('navigate', 'jump between', 'role=', 'landmark', 'rotor'),
    'semantic markup': ('accessibility tree', 'role', 'machine-readable', 'native semantics'),
    'focus management': ('keyboard', 'focus trap', 'return focus', 'tabindex', 'spa'),
    'reading order': ('dom order', 'source order', 'flexbox order', '1.3.2'),
    'text formatting': ('strong', 'markup not appearance', 'real lists', 'semantic'),
    'form field': ('label', 'required', 'error', 'autocomplete'),
    'low vision': ('magnif', 'zoom', 'contrast', 'large text'),
    'cognitive disabilities': ('plain language', 'cognitive load', 'memory', 'coga'),
    'universal design': ('disability', 'accessibility', 'inclusive design', 'curb cut'),
    'decorative image': ('alt=""', "alt=''", 'empty alt', 'null alt', 'role=presentation', 'hidden from'),
    'informative image': ('describe', 'non-text'),
    'responsive design': ('reflow', 'zoom', '1.4.10', 'magnification'),
}


def observe_sense(concept, output):
    """Return 'a11y' if the response shows an accessibility-specific sense,
    else 'generic'. a11y iff any GLOBAL_A11Y_MARKER or any compound-specific
    marker appears. Applies uniformly to every response (Option A + recording).
    """
    text = str(output).lower()
    if _has(text, *GLOBAL_A11Y_MARKERS):
        return 'a11y'
    extra = A11Y_SENSE_MARKERS.get(str(concept).strip().lower(), ())
    if extra and _has(text, *extra):
        return 'a11y'
    return 'generic'


def code_response(prompt_type, concept, prompt, output):
    """
    Route to the appropriate coding function based on prompt type.
    Returns: 'correct' | 'partial' | 'incorrect'
    """
    # Guard: expansion compounds return 'uncoded' until their criteria are
    # authored (see PENDING_CRITERIA below). Without this guard they would
    # fall through code_declarative's rules.get() miss and be silently coded
    # 'incorrect' — a wall of fake never_emerges. Remove each concept from
    # PENDING_CRITERIA as its criteria land.
    if concept in PENDING_CRITERIA:
        return 'uncoded'

    if prompt_type == 'declarative':
        return code_declarative(concept, output)
    elif prompt_type == 'evaluative':
        return code_evaluative(concept, prompt, output)
    elif prompt_type == 'control':
        return code_control(concept, prompt, output)
    elif prompt_type == 'completion':
        return code_completion(concept, prompt, output)
    elif prompt_type == 'validation':
        return code_validation(concept, prompt, output)
    elif prompt_type == 'hypothesis':
        return code_hypothesis(concept, prompt, output)
    else:
        return 'uncoded'


def code_declarative(concept, output):
    """
    Code declarative (cloze) responses.

    Criteria: Does the completion capture the accessibility-relevant
    meaning of the concept?
      - correct:   captures the core meaning a practitioner would recognize
      - partial:   touches the right domain but misses the key point
      - incorrect: wrong domain, circular, degenerate, or nonsensical
    """
    output = str(output).lower()

    rules = {
        'screen reader': {
            # correct: must indicate it reads/speaks text or content aloud,
            # or mention assistive use for blind/low-vision users
            'correct': (
                'reads text' in output or
                'reads aloud' in output or
                'reads the text' in output or
                'reads content' in output or
                'reads the content' in output or
                'converts it into speech' in output
            ),
            # partial: mentions screen + reading but doesn't capture the
            # assistive technology meaning (e.g. "view a screen")
            'partial': 'screen' in output and 'read' in output,
        },
        'WCAG': {
            # correct: must expand to Web Content Accessibility Guidelines
            'correct': 'web content accessibility' in output,
            # partial: mentions accessibility or web content but wrong expansion
            'partial': 'accessibility' in output or 'web content' in output,
        },
        'skip link': {
            # correct: must indicate skipping/jumping over navigation to
            # reach main content or a specific section
            'correct': (
                ('skip' in output or 'jump' in output) and
                ('navigation' in output or 'main content' in output or
                 'section' in output or 'specific location' in output)
            ),
            # partial: gets the "not part of main" idea but misses the
            # skip-to-content function
            'partial': (
                'link' in output and
                'not a link' not in output and
                ('not part' in output or 'not displayed' in output)
            ),
        },
        'alt text': {
            # correct: must mention describing an image
            'correct': 'description' in output and 'image' in output,
            # partial: mentions description or text+image but doesn't
            # connect them clearly
            'partial': (
                'description' in output or
                ('text' in output and ('image' in output or 'alt' in output))
            ),
        },
        'ARIA': {
            # correct: must be "Accessible Rich Internet Applications"
            # No partial — it's an acronym, you either know it or you don't
            'correct': 'accessible rich internet' in output,
            'partial': False,
        },
        'focus indicator': {
            # correct: must relate to showing which element has keyboard
            # focus or is currently active — NOT camera focus
            'correct': (
                'focus' in output and
                ('visible' in output or 'keyboard' in output or
                 'element' in output or 'current' in output) and
                'camera' not in output and
                'beam' not in output and
                'laser' not in output
            ),
            # partial: mentions focus in a potentially relevant way but
            # doesn't connect to keyboard/interaction context
            'partial': (
                'focus' in output and
                'camera' not in output and
                'beam' not in output and
                'laser' not in output
            ),
        },
        'keyboard navigation': {
            # correct: must relate to navigating a website/page via keyboard
            'correct': (
                'navigate' in output and
                ('web' in output or 'site' in output or 'page' in output)
            ),
            # partial: mentions navigation but not web-specific
            'partial': 'navigate' in output or 'navigation' in output,
        },
        'color contrast': {
            # correct: must relate to distinguishing/perceiving/reading
            # colors — the visual accessibility connection
            'correct': (
                ('readab' in output or 'distinguish' in output or
                 'perceiv' in output or 'see the diff' in output) and
                'color' in output
            ),
            # partial: mentions color but doesn't connect to perception
            'partial': 'color' in output,
        },
        'semantic HTML': {
            # correct: must capture meaning/structure conveyed through HTML
            'correct': (
                'meaning' in output or
                ('structure' in output and 'html' in output)
            ),
            # partial: mentions HTML or semantic but doesn't connect them
            'partial': 'html' in output or 'semantic' in output,
        },
        'captions': {
            # correct: must connect captions to video/audio content AND
            # text/description purpose or deaf/hearing users
            'correct': (
                ('video' in output or 'audio' in output) and
                ('text' in output or 'description' in output or
                 'deaf' in output or 'hearing' in output)
            ),
            # partial: mentions video/audio but doesn't connect to
            # accessibility purpose
            'partial': 'video' in output or 'audio' in output,
        },
        # S5 — captions naming fix (DECISIONS 2026-07-03). The declarative
        # captions data uses concept 'captions' (handled above); 'closed
        # captions' appears only as control. This alias closes the DANGEROUS
        # CELL defensively: if a declarative 'closed captions' row ever appears
        # it codes by the same rule instead of falling through to 'incorrect'.
        # No current declarative row has this concept, so it is a no-op on the
        # existing data (regression-neutral).
        'closed captions': {
            'correct': (
                ('video' in output or 'audio' in output) and
                ('text' in output or 'description' in output or
                 'deaf' in output or 'hearing' in output)
            ),
            'partial': 'video' in output or 'audio' in output,
        },

        # ================================================================
        # n=49 EXPANSION — 41 declarative rules (translated from
        # docs/findings/criteria_authoring.csv; doctrine block at module top).
        # correct = distinguishing markers; partial = right-neighborhood-thin;
        # else incorrect (absorbs wrong-domain / circular / trench-coat).
        # ================================================================

        'keyboard interaction': {
            # correct: operating/navigating via keys/tab, not mere typing
            'correct': (
                _has(output, 'navigat', 'operate', 'operating', 'arrow key',
                     'without a mouse', 'without using a mouse', 'keyboard-only',
                     'move through', 'activat', 'tabbing', 'tab key',
                     'pressing tab') and
                not _has(output, 'piano', 'music', 'instrument', 'song')
            ),
            # partial: generic keyboard/typing use, no operate/navigate content
            'partial': (_has(output, 'keyboard', 'keystroke', 'typ', 'press') and
                        not _has(output, 'piano', 'music', 'instrument')),
        },
        'section heading': {
            # correct: heading that organizes structure / section / levels
            'correct': (
                _has(output, 'section', 'structur', 'organiz', 'hierarch',
                     'heading level', 'h1', 'h2', 'h3', 'level') and
                not _has(output, 'newspaper', 'magazine', 'headline of')
            ),
            # partial: title/label/visual-only framing, no structure content
            'partial': (_has(output, 'head', 'title', 'label', 'bold text',
                             'big text') and
                        not _has(output, 'newspaper', 'magazine')),
        },
        'text alternative': {
            # correct: umbrella — equivalent text for non-text content generally
            'correct': (
                _has(output, 'equivalent', 'serves the same', 'same purpose',
                     'in place of', 'replacement', 'text version', 'substitute',
                     'stand in') and
                _has(output, 'non-text', 'nontext', 'audio', 'video', 'media',
                     'control')
            ),
            # partial: alt-text-only (images) — vertical, too narrow
            'partial': (_has(output, 'image', 'picture', 'alt') and
                        _has(output, 'text', 'describ', 'equivalent',
                             'alternative')),
        },
        'audio description': {
            # correct: describes VISUAL content of video; not captions/inverted
            'correct': (
                _has(output, 'describ', 'narrat', 'explain') and
                _has(output, 'visual', 'on-screen', 'on screen', 'scene',
                     'action', 'what is happening', "what's happening", 'see ',
                     'seeing', 'sighted') and
                not _has(output, 'caption', 'subtitle', 'dialogue', 'transcri',
                         'deaf', 'hard of hearing', 'hearing', 'sound', 'music')
            ),
            # partial: added narration/audio track, no describing-visual content
            'partial': (
                _has(output, 'narrat', 'audio track', 'voice-over', 'voiceover',
                     'soundtrack', 'extra audio', 'additional audio') and
                _has(output, 'video', 'media', 'film') and
                not _has(output, 'caption', 'subtitle', 'dialogue', 'deaf')
            ),
        },
        'sign language': {
            # correct: gestural/visual language for communication / interpret
            'correct': (
                _has(output, 'deaf', 'interpret', 'gestur', 'hand', 'manual',
                     'communicat', 'visual language') and
                not _has(output, 'road sign', 'traffic sign', 'street sign',
                         'signage', 'warning sign', 'sign up', 'sign in')
            ),
            # partial: signing/gestures with no communication/language content
            'partial': (_has(output, 'gestur', 'hand', 'signing', 'signed') and
                        not _has(output, 'road sign', 'traffic sign', 'signage')),
        },
        'sensory characteristics': {
            # correct: instructions must not rely SOLELY on sensory traits
            'correct': (
                _has(output, 'shape', 'color', 'colour', 'size', 'location',
                     'position', 'orientation', 'sound') and
                _has(output, 'instruction', 'rely', 'solely', 'alone', 'only',
                     'not only', 'more than') and
                not _has(output, 'taste', 'smell', 'texture', 'aroma', 'flavou',
                         'food', 'sensory evaluation')
            ),
            # partial: names sensory traits in a UI context, no don't-rely point
            'partial': (
                _has(output, 'shape', 'color', 'colour', 'size', 'location',
                     'orientation', 'sensory', 'perceiv') and
                not _has(output, 'taste', 'smell', 'flavou', 'food')
            ),
        },
        'input purpose': {
            # correct: field purpose made programmatically determinable
            'correct': (
                _has(output, 'programmatically', 'machine-readable',
                     'machine readable', 'autocomplete', 'autofill') and
                _has(output, 'input', 'field', 'form', 'collect', 'purpose')
            ),
            # partial: fields-have-purposes / label-only (human-readable)
            'partial': _has(output, 'label', 'collect', 'information', 'name',
                            'email', 'address', 'autofill', 'form field'),
        },
        'target size': {
            # correct: interactive target large enough to activate (touch/motor)
            'correct': (
                _has(output, 'button', 'link', 'control', 'interactive',
                     'clickable', 'tappable') and
                _has(output, 'large enough', 'big enough', 'minimum', '24',
                     'activate', 'tap', 'touch', 'click') and
                not _has(output, 'archery', 'shooting', 'marketing', 'dartboard',
                         'bullseye')
            ),
            # partial: size-of-elements framing, no interactive/activation
            'partial': (_has(output, 'size', 'area', 'dimension', 'pixel') and
                        not _has(output, 'archery', 'shooting')),
        },
        'touch target': {
            # correct: tappable area large enough for reliable touch activation
            'correct': (
                _has(output, 'button', 'link', 'control', 'interactive',
                     'tappable', 'clickable') and
                _has(output, 'large enough', 'big enough', 'minimum', '24', '44',
                     '48', 'tap', 'touch', 'finger', 'activate') and
                not _has(output, 'touchscreen hardware', 'game', 'gaming',
                         'sensor')
            ),
            # partial: area/region framing, no interactive/activation content
            'partial': (_has(output, 'area', 'region', 'size', 'tap', 'touch',
                             'finger') and
                        not _has(output, 'game', 'gaming', 'sensor')),
        },
        'drag movement': {
            # correct: draggable functionality must have a non-drag alternative
            'correct': (
                _has(output, 'drag') and
                _has(output, 'alternative', 'without', 'single pointer',
                     'single-pointer', 'click', 'tap', 'another way',
                     'other than') and
                not _has(output, 'drag racing', 'drag coefficient', 'drag force',
                         'aerodynamic')
            ),
            # partial: dragging-moves-things, no alternative-required content
            'partial': (
                _has(output, 'drag', 'slider', 'reorder', 'drag-and-drop',
                     'drag and drop') and
                not _has(output, 'drag racing', 'drag coefficient', 'aerodynamic')
            ),
        },
        'focus appearance': {
            # correct: visible focus indicator quality for keyboard users
            'correct': (
                _has(output, 'focus') and
                _has(output, 'indicator', 'outline', 'ring', 'highlight',
                     'border', 'visible', 'visibility') and
                _has(output, 'keyboard', 'contrast', 'where', 'current',
                     'which element', 'active element', 'tab') and
                not _has(output, 'camera', 'photograph', 'lens', 'blur',
                         'sharpness')
            ),
            # partial: how-focus-looks, no keyboard/indicator purpose
            'partial': (
                _has(output, 'focus') and
                _has(output, 'indicator', 'outline', 'ring', 'highlight',
                     'visible', 'look') and
                not _has(output, 'camera', 'photograph', 'lens')
            ),
        },
        'consistent help': {
            # correct: help in the SAME relative location across pages
            'correct': (
                _has(output, 'help', 'contact', 'chat', 'faq', 'support') and
                _has(output, 'same location', 'same place', 'same order',
                     'same position', 'relative order', 'across pages',
                     'every page', 'multiple pages', 'each page',
                     'consistent location', 'same spot')
            ),
            # partial: help-is-available/findable, no cross-page placement rule
            'partial': (
                _has(output, 'help', 'contact', 'chat', 'faq', 'support') and
                _has(output, 'find', 'available', 'easy', 'locate', 'access')
            ),
        },
        'redundant entry': {
            # correct: don't require retyping already-entered info
            'correct': (
                (_has(output, 'already entered', 'previously entered',
                      'already provided', 'already typed', 'already filled') or
                 (_has(output, 'retype', 're-enter', 'reenter', 're-type',
                       'enter again', 'type again', 'repeat') and
                  _has(output, 'information', 'data', 'details', 'form',
                       'field'))) and
                not _has(output, 'database', 'duplicate record', 'deduplicat',
                         'redundant data')
            ),
            # partial: don't-repeat-yourself, no mechanism/same-process scope
            'partial': (
                _has(output, 'repeat', 'again', 're-enter', 'retype',
                     'same information', 'twice') and
                not _has(output, 'database', 'deduplicat')
            ),
        },
        'accessible authentication': {
            # correct: auth without memory/cognitive burden (paste/manager/etc.)
            'correct': (
                _has(output, 'authenticat', 'login', 'log in', 'sign in',
                     'sign-in', 'password', 'credential') and
                _has(output, 'paste', 'copy', 'password manager', 'captcha',
                     'passkey', 'memoriz', 'memory', 'cognitive', 'remember',
                     'transcrib') and
                not _has(output, 'more secure', 'harder to', 'stronger security',
                         '2fa only')
            ),
            # partial: auth-mechanics only, no accessibility modifier
            'partial': (
                _has(output, 'authenticat', 'login', 'log in', 'sign in',
                     'password', 'credential', 'identity', '2fa', 'oauth',
                     'verify') and
                not _has(output, 'more secure', 'harder', 'stronger security',
                         'robust security', 'prevent unauthorized',
                         'protect against hacker')
            ),
        },
        'text spacing': {
            # correct: user can adjust/override spacing (survivability)
            'correct': (
                _has(output, 'spacing', 'line height', 'line-height',
                     'letter-spacing', 'word-spacing', 'paragraph') and
                _has(output, 'adjust', 'override', 'increase', 'change', 'user',
                     'custom', 'browser') and
                not _has(output, 'kerning', 'aesthetic', 'leading for')
            ),
            # partial: names spacing properties, no override-survivability
            'partial': _has(output, 'spacing', 'line height', 'letter', 'word',
                            'paragraph', 'kerning', 'leading'),
        },
        'status message': {
            # correct: message about state/result/progress in the UI (toast ok)
            'correct': (
                _has(output, 'notification', 'toast', 'alert', 'message',
                     'status') and
                _has(output, 'success', 'progress', 'result', 'error', 'state',
                     'update', 'inform', 'convey', 'confirm', 'feedback') and
                not _has(output, 'http', '404', '200', '500', 'status code',
                         'response code', 'social media', 'server status',
                         'uptime')
            ),
            # partial: information-shown-to-user, no state/result/notification
            'partial': (
                _has(output, 'message', 'inform', 'display', 'shown', 'user') and
                not _has(output, 'http', 'status code', '404', '200')
            ),
        },
        'error identification': {
            # correct: which field is in error, described in text (the pointing)
            'correct': (
                _has(output, 'error') and
                _has(output, 'field', 'input', 'which', 'identif', 'locate',
                     'point', 'where', 'what went wrong') and
                _has(output, 'text', 'describ', 'explain', 'message', 'tell',
                     'inform') and
                not _has(output, 'stack trace', 'exception', 'debug', 'compiler',
                         'error code', 'bug ')
            ),
            # partial: generic show-an-error-message (misses field/text pointing)
            'partial': (
                _has(output, 'error') and
                _has(output, 'message', 'show', 'display', 'tell', 'inform',
                     'alert') and
                not _has(output, 'stack trace', 'exception', 'debug', 'compiler')
            ),
        },
        'pointer cancellation': {
            # correct: pointer actions abortable mid-gesture (up-event/move-off)
            'correct': (
                _has(output, 'cancel', 'abort', 'undo', 'stop') and
                _has(output, 'up event', 'up-event', 'release', 'let go',
                     'letting go', 'before releas', 'move away', 'move off',
                     'slide off', 'drag away', 'down event', 'down-event') and
                not _has(output, 'null pointer', 'memory', 'dereference', 'c++',
                         'pointer variable', 'malloc')
            ),
            # partial: pointer-actions-general, no cancel-mid-gesture mechanism
            'partial': (
                _has(output, 'pointer', 'touch', 'click', 'tap') and
                _has(output, 'cancel', 'abort', 'accidental', 'undo',
                     'mistake') and
                not _has(output, 'null pointer', 'memory', 'dereference', 'c++')
            ),
        },
        'character key': {
            # correct: single-char shortcut with remap / turn-off / focus-only
            'correct': (
                _has(output, 'shortcut', 'single key', 'single character',
                     'single-key', 'single-character', 'one-key',
                     'keyboard shortcut') and
                _has(output, 'remap', 'reassign', 'rebind', 'turn off',
                     'disable', 'only when focused', 'on focus', 'customize') and
                not _has(output, 'cipher', 'cryptograph', 'encryption',
                         'protagonist', 'story', 'novel', 'ascii')
            ),
            # partial: shortcuts-exist, none of the three mitigations
            'partial': (
                _has(output, 'shortcut', 'single key', 'keyboard shortcut',
                     'single character') and
                not _has(output, 'cipher', 'cryptograph', 'protagonist', 'story')
            ),
        },
        'accessibility tree': {
            # correct: DOM-derived structure exposed to assistive technology
            'correct': (
                _has(output, 'dom', 'browser', 'derived', 'built from',
                     'parallel', 'representation') and
                _has(output, 'assistive', 'screen reader', 'exposed', 'exposes',
                     'accessibility api', 'role', 'state', 'propert') and
                not _has(output, 'binary tree', 'decision tree', 'file system',
                         'directory', 'family tree')
            ),
            # partial: DOM-adjacent without AT consumer, or AT without structure
            'partial': (
                _has(output, 'dom', 'tree', 'structure', 'role', 'node') and
                not _has(output, 'binary tree', 'decision tree', 'family tree',
                         'file system')
            ),
        },
        'accessible name': {
            # correct: what the element is CALLED, computed/announced by AT
            'correct': (
                _has(output, 'announce', 'computed', 'comput', 'aria-label',
                     'labelledby', 'accname', 'screen reader', 'assistive',
                     'identif') and
                _has(output, 'name', 'label', 'called') and
                not _has(output, 'variable name', 'file name', 'filename',
                         'naming convention', 'username', 'domain name')
            ),
            # partial: label-framing without the computed/announced-by-AT layer
            'partial': (
                _has(output, 'label', 'called', 'identif', 'announce',
                     'title') and
                not _has(output, 'variable name', 'file name', 'filename',
                         'username')
            ),
        },
        'accessible description': {
            # correct: supplementary text BEYOND the name (elaborates)
            # aria-describedby is NOT a correct marker (2026-07-03 veto)
            'correct': (
                _has(output, 'supplementary', 'additional', 'extra', 'context',
                     'hint', 'beyond the name', 'after the name',
                     'more information', 'further') and
                _has(output, 'describ', 'description', 'announce', 'convey',
                     'screen reader', 'assistive', 'read')
            ),
            # partial: description framing, thin — but describedby-as-answer is
            # incorrect (veto), so it is excluded from partial too
            'partial': (
                _has(output, 'describ', 'description', 'context', 'detail',
                     'information') and
                not _has(output, 'aria-describedby', 'describedby')
            ),
        },
        'live region': {
            # correct: dynamic area whose changes are announced without focus
            'correct': (
                _has(output, 'update', 'change', 'dynamic', 'new content',
                     'refresh', 'content that') and
                _has(output, 'announce', 'read aloud', 'notified',
                     'screen reader', 'assistive', 'aria-live', 'without focus',
                     'without moving focus') and
                not _has(output, 'live broadcast', 'live coverage', 'live stream',
                         'geographic', 'region of a country', 'live tv')
            ),
            # partial: dynamic-content framing, no announcement/AT content
            'partial': (
                _has(output, 'update', 'change', 'dynamic', 'region', 'area') and
                not _has(output, 'broadcast', 'geographic', 'country',
                         'live stream', 'live tv')
            ),
        },
        'tab panel': {
            # correct: content container shown for its selected/associated tab
            'correct': (
                _has(output, 'panel', 'content', 'container') and
                'tab' in output and
                _has(output, 'select', 'active', 'associated', 'shown',
                     'displayed', 'one at a time', 'switch', 'when')
            ),
            # partial: defines the TAB not the PANEL, or no association content
            'partial': _has(output, 'tab', 'panel'),
        },
        'radio group': {
            # correct: mutually-exclusive option set (the exclusivity)
            'correct': (
                _has(output, 'radio') and
                _has(output, 'mutually exclusive', 'only one', 'one at a time',
                     'one option', 'deselect', 'exclusive', 'select one') and
                not _has(output, 'radio station', 'fm radio', 'am radio',
                         'radio broadcast', 'radio signal', 'radio wave',
                         'walkie')
            ),
            # partial: radio-buttons-grouped, no mutual-exclusivity semantics
            'partial': (
                _has(output, 'radio') and
                _has(output, 'group', 'button', 'options', 'set') and
                not _has(output, 'radio station', 'broadcast', 'radio wave',
                         'fm ', 'am radio')
            ),
        },
        'tree grid': {
            # correct: BOTH halves — a data TABLE (not the echoed 'grid') whose
            # ROWS expand/collapse HIERARCHICALLY (not the echoed 'tree' token).
            # Guards the arboreal "grid of trees" + ML (decision tree / grid
            # search) attractors. tree_grid predicted never_emerges.
            'correct': (
                _has(output, 'table', 'rows and columns', 'data table',
                     'spreadsheet', 'column', 'tabular') and
                _has(output, 'expand', 'collaps', 'hierarch', 'nested',
                     'parent-child', 'parent and child', 'expandable row') and
                not _has(output, 'decision tree', 'grid search',
                         'machine learning', 'optimization', 'electrical grid',
                         'power grid', 'grid of trees', 'forest', 'orchard')
            ),
            # partial: half the hybrid — a treeview/hierarchy half OR a table
            # half, via distinguishing tokens (not the echoed compound words)
            'partial': (
                (_has(output, 'treeview', 'tree view', 'tree-like', 'hierarch',
                      'nested', 'expand', 'collaps', 'parent-child') or
                 _has(output, 'table', 'rows and columns', 'data table',
                      'spreadsheet', 'column', 'tabular')) and
                not _has(output, 'decision tree', 'grid search', 'power grid',
                         'electrical grid', 'grid of trees', 'forest', 'orchard',
                         'machine learning')
            ),
        },
        'menu bar': {
            # correct: strip/container of menus (Option A poster child — generic
            # GUI sense nods)
            'correct': (
                _has(output, 'menu') and
                _has(output, 'bar', 'strip', 'container', 'submenu', 'dropdown',
                     'drop-down', 'command', 'file', 'edit', 'view', 'toolbar',
                     'application', 'navigation') and
                not _has(output, 'restaurant', 'food menu', 'dinner', 'waiter')
            ),
            # partial: menus-exist, no bar/container-of-menus structure
            'partial': (_has(output, 'menu') and
                        not _has(output, 'restaurant', 'food menu', 'dinner')),
        },
        'tool tip': {
            # correct: popup with supplementary text on hover OR focus (hover-
            # only still correct under Option A)
            'correct': (
                (_has(output, 'tooltip', 'popup', 'pop-up', 'bubble',
                      'small box') or
                 _has(output, 'hover', 'mouse over')) and
                _has(output, 'text', 'information', 'hint', 'description',
                     'extra', 'additional', 'brief', 'context', 'label',
                     'appears') and
                not _has(output, 'physical tool', 'tip of a tool', 'screwdriver',
                         'hammer')
            ),
            # partial: popup framing with no supplementary-text purpose
            'partial': (
                _has(output, 'tooltip', 'popup', 'pop-up', 'bubble', 'hover') and
                not _has(output, 'physical tool', 'tip of a tool')
            ),
        },
        'combo box': {
            # correct: text input COMBINED with a popup list (the combination)
            'correct': (
                (_has(output, 'text') and
                 _has(output, 'input', 'field', 'type', 'typing', 'enter')) and
                _has(output, 'list', 'dropdown', 'drop-down', 'listbox',
                     'options', 'suggestions', 'popup') and
                not _has(output, 'combo meal', 'combination lock', 'combo deal',
                         'padlock')
            ),
            # partial: plain-dropdown (select-only) — named half the machine
            'partial': (
                _has(output, 'dropdown', 'drop-down', 'list', 'select',
                     'options', 'choose', 'box') and
                not _has(output, 'combo meal', 'combination lock')
            ),
        },
        'semantic markup': {
            # correct: elements chosen for MEANING not appearance
            'correct': (
                _has(output, 'meaning', 'semantic', 'purpose', 'machine-readable',
                     'convey') and
                _has(output, 'element', 'tag', 'html', 'button', 'nav',
                     'heading', 'markup') and
                not _has(output, 'semantic web', 'rdf', 'ontolog', 'sparql',
                         'linked data', 'nlp', 'natural language',
                         'word embedding')
            ),
            # partial: elements-have-meaning, no meaning-vs-appearance contrast
            'partial': (
                _has(output, 'html', 'element', 'tag', 'markup', 'semantic') and
                not _has(output, 'semantic web', 'rdf', 'ontolog', 'nlp',
                         'natural language')
            ),
        },
        'focus management': {
            # correct: deliberately MOVING focus on context changes
            'correct': (
                _has(output, 'focus') and
                _has(output, 'move', 'moving', 'send', 'sent', 'place', 'set ',
                     'return', 'shift', 'bring', 'trap', 'tabindex') and
                _has(output, 'dialog', 'modal', 'route', 'page change',
                     'dynamic', 'component', 'element', 'open', 'close',
                     'navigat') and
                not _has(output, 'concentration', 'productivity', 'deep work',
                         'distraction', 'pay attention', 'stay focused',
                         'mental focus', 'mindful')
            ),
            # partial: focus-exists / keyboard-nav-general, no deliberate-move
            'partial': (
                _has(output, 'focus') and
                not _has(output, 'concentration', 'productivity', 'deep work',
                         'distraction', 'mindful', 'camera')
            ),
        },
        'reading order': {
            # correct: linear sequence content is read in (generic sense passes)
            'correct': (
                _has(output, 'order', 'sequence', 'sequential') and
                _has(output, 'read', 'reading', 'content', 'linear', 'in order',
                     'follow', 'logical', 'top to bottom', 'left to right') and
                not _has(output, 'sort order', 'alphabetical order',
                         'religious order', 'sorting', 'database order')
            ),
            # partial: order-of-things, no reading/content connection
            'partial': (
                _has(output, 'order', 'sequence') and
                not _has(output, 'sort order', 'religious order', 'alphabetical')
            ),
        },
        'text formatting': {
            # correct: visual presentation/styling of text (generic nods — flat)
            'correct': (
                _has(output, 'bold', 'italic', 'underline', 'font', 'size',
                     'color', 'colour', 'align', 'style', 'heading',
                     'presentation', 'appearance', 'markup') and
                not _has(output, 'file format', '.txt', '.docx', '.pdf',
                         'plain text file', 'file type', 'document format')
            ),
            # partial: styling-exists framing so thin it names nothing
            'partial': (
                _has(output, 'format', 'style', 'appearance') and
                not _has(output, 'file format', '.txt', '.docx')
            ),
        },
        'form field': {
            # correct: interactive input element collecting data (generic nods)
            'correct': (
                _has(output, 'input', 'field', 'control', 'text box', 'textbox',
                     'checkbox', 'dropdown', 'drop-down', 'select', 'textarea',
                     'radio') and
                _has(output, 'form', 'enter', 'collect', 'fill', 'user', 'data',
                     'information', 'type') and
                not _has(output, 'database field', 'database record',
                         'farm field', 'field of study', 'magnetic field',
                         'electric field', 'football field')
            ),
            # partial: forms-exist framing with no input-element content
            'partial': (
                _has(output, 'form', 'field', 'input') and
                not _has(output, 'database field', 'farm field',
                         'magnetic field', 'field of study')
            ),
        },
        'landmark region': {
            # correct: named/typed structural regions of a page
            'correct': (
                _has(output, 'landmark', 'region', 'area', 'section') and
                _has(output, 'main', 'nav', 'header', 'banner', 'footer',
                     'contentinfo', 'complementary', 'aside', 'search',
                     'structur', 'role', 'named', 'part of the page') and
                not _has(output, 'monument', 'eiffel', 'statue', 'tourist',
                         'geographic', 'point of interest', 'historic')
            ),
            # partial: generic sections-of-a-page, no named/typed-region content
            'partial': (
                _has(output, 'region', 'area', 'section', 'part of the page',
                     'structure') and
                not _has(output, 'monument', 'eiffel', 'tourist', 'geographic',
                         'landmark of a city', 'historic')
            ),
        },
        'low vision': {
            # correct: partial sight — beyond correction, short of blindness
            'correct': (
                _has(output, 'vision', 'sight', 'visual', 'see', 'eyesight') and
                _has(output, 'impair', 'loss', 'reduced', 'partial', 'limited',
                     'poor', 'difficulty', 'not fully correct', 'glasses',
                     'not blind', 'not completely blind', 'some vision',
                     'remaining vision') and
                not _has(output, 'low visibility', 'foggy', 'photograph',
                         'camera', 'weather', 'driving condition')
            ),
            # partial: vision-problems, no distinct-from-blindness/correction
            'partial': (
                _has(output, 'vision', 'sight', 'visual', 'eye') and
                not _has(output, 'low visibility', 'foggy', 'weather',
                         'photograph')
            ),
        },
        'cognitive disabilities': {
            # correct: conditions affecting cognition (population term)
            'correct': (
                _has(output, 'cognit', 'memory', 'attention', 'comprehen',
                     'learning', 'processing', 'understand', 'think',
                     'reasoning', 'intellectual', 'dementia', 'adhd', 'dyslex',
                     'autism') and
                _has(output, 'disab', 'impair', 'condition', 'difficult',
                     'affect', 'challenge', 'limit')
            ),
            # partial: mental-illness conflation (RATIFIED partial 2026-07-03),
            # or disability-general with no cognition content
            'partial': (
                _has(output, 'mental illness', 'mental health', 'depression',
                     'anxiety', 'psychiatric', 'bipolar', 'schizophren') or
                _has(output, 'disab', 'impair', 'condition')
            ),
        },
        'universal design': {
            # correct: design for everyone FROM THE START (anti-retrofit)
            'correct': (
                _has(output, 'curb cut') or
                (_has(output, 'everyone', 'all users', 'all people',
                      'widest range', 'regardless', 'any ability',
                      'all abilities') and
                 _has(output, 'from the start', 'from the beginning', 'built in',
                      'built-in', 'upfront', 'not added later',
                      'rather than retrofit', 'not retrofit',
                      'designed for all'))
            ),
            # partial: design-for-everyone, no from-the-start/anti-retrofit
            'partial': _has(output, 'everyone', 'all users', 'all people',
                            'accessible to all', 'regardless', 'inclusive'),
        },
        'decorative image': {
            # correct: no-information image; removability test; empty alt
            'correct': (
                ((_has(output, 'no information', 'no meaning', 'no content',
                       'not convey', "doesn't convey", 'does not convey',
                       'purely decorat', 'purely aesthetic', 'purely visual',
                       'only for decoration', 'just decoration', 'decorative') and
                  not _has(output, 'convey information', 'conveys information',
                           'needs alt', 'requires alt', 'meaningful')) or
                 (_has(output, 'remov') and
                  _has(output, 'unaffected', 'no loss', 'still understand',
                       'without losing', 'no information is lost', 'same')) or
                 _has(output, 'alt=""', "alt=''", 'empty alt', 'null alt',
                      'blank alt')) and
                not _has(output, 'home decor', 'home décor', 'interior design',
                         'decorating a room', 'picture of decorations')
            ),
            # partial: aesthetic/decoration framing, no no-info/removability
            'partial': (
                _has(output, 'decorat', 'aesthetic', 'visual') and
                not _has(output, 'home decor', 'interior design')
            ),
        },
        'informative image': {
            # correct: BINARY — must mention alt text / "text alternative" (GATE,
            # 2026-07-03 veto); mirror-confusion (decorative) excluded
            'correct': (
                _has(output, 'alt text', 'alt attribute', 'alternative text',
                     'text alternative', 'alt=') and
                not _has(output, 'decorative', 'empty alt', 'alt=""',
                         'no alt text', 'purely aesthetic', 'no information')
            ),
            # no partial zone — veto made this row correct-or-incorrect
            'partial': False,
        },
        'responsive design': {
            # correct: adapts to screen/device (generic web-dev sense nods).
            # 'responsive' echoes the prompt, so the SCREEN/DEVICE content is
            # the real discriminator; guard the performance ('responds fast')
            # sense. ('responsive' != 'respond' as a substring — both listed.)
            'correct': (
                _has(output, 'responsive', 'adapt', 'adjust', 'change',
                     'resize', 'fluid', 'flexible', 'respond') and
                _has(output, 'screen size', 'screen', 'viewport', 'device',
                     'mobile', 'desktop', 'tablet', 'window size',
                     'different size', 'various size', 'any device',
                     'breakpoint', 'media quer') and
                not _has(output, 'responds quickly', 'fast response',
                         'response time', 'quick to respond', 'low latency',
                         'loads fast')
            ),
            # partial: design-that-adapts, no screen/device content
            'partial': (
                _has(output, 'adapt', 'adjust', 'flexible', 'fluid') and
                not _has(output, 'response time', 'fast response', 'low latency')
            ),
        },
    }

    r = rules.get(concept, {})
    if r.get('correct', False):
        return 'correct'
    if r.get('partial', False):
        return 'partial'
    return 'incorrect'


def code_evaluative(concept, prompt, output):
    """
    Code evaluative (code review) responses.

    Criteria: Does the model correctly identify the accessibility problem
    in the code snippet?
      - correct:   identifies the specific accessibility issue
      - partial:   identifies something is wrong but misattributes the cause
      - incorrect: fails to identify the issue or gives unrelated output
    """
    output = str(output).lower()
    prompt = str(prompt).lower()

    # <img src='photo.jpg'> — missing alt attribute
    if 'img' in prompt and "doesn't have" in prompt:
        if 'alt' in output and ('missing' in output or 'attribute' in output or 'text' in output):
            return 'correct'
        return 'incorrect'

    # <div> with onclick — should be a button/link, not semantically interactive
    if 'div' in prompt and 'onclick' in prompt:
        if ('button' in output or 'semantic' in output or
                'keyboard' in output or 'focusable' in output or
                'role' in output or 'not a form control' in output):
            return 'correct'
        if 'not a link' in output or 'not a valid' in output:
            return 'partial'
        return 'incorrect'

    # <a href='#'></a> — empty link, no text content
    if "a href='#'></a>" in prompt:
        if 'empty' in output or 'no text' in output or 'no content' in output:
            return 'correct'
        if 'not clear' in output or 'not accessible' in output:
            return 'partial'
        return 'incorrect'

    # <input type='text'> — needs a label
    if "input type='text'" in prompt:
        if 'label' in output or 'aria-label' in output:
            return 'correct'
        if 'value' in output or 'name' in output:
            return 'partial'
        return 'incorrect'

    # Button saying 'Click here' — not descriptive
    if 'click here' in prompt:
        if ('descriptive' in output or 'what it does' in output or
                'not clear' in output or "doesn't tell" in output or
                'what to click' in output):
            return 'correct'
        return 'incorrect'

    return 'incorrect'


def code_control(concept, prompt, output):
    """
    Code control (bicycle) responses.

    Criteria: Does the model demonstrate general evaluative reasoning
    on common-knowledge topics?
      - correct:   logically sound reasoning about the topic
      - partial:   touches the right idea but circular or vague
      - incorrect: wrong, nonsensical, or contradicts the premise
    """
    output = str(output).lower()
    prompt = str(prompt).lower()

    if 'bicycle' in prompt and ('brakes' in prompt or 'safe' in prompt):
        if ('stop' in output or 'injury' in output or 'crash' in output or
                'accident' in output or 'danger' in output):
            return 'correct'
        if 'not safe' in output and 'not safe' in prompt:
            return 'partial'  # circular
        return 'incorrect'

    if 'bicycle' in prompt and 'helmet' in prompt:
        if ('head' in output or 'injury' in output or 'struck' in output or
                'hit' in output or 'protect' in output):
            return 'correct'
        return 'incorrect'

    if 'bicycle' in prompt and 'used for' in prompt:
        if 'transport' in output or 'travel' in output or 'exercise' in output:
            return 'correct'
        return 'incorrect'

    # Definitional bicycle probes ("What is a bicycle?", "Explain bicycles...")
    if 'bicycle' in prompt and ('what is' in prompt or 'explain' in prompt):
        if ('wheel' in output or 'pedal' in output or 'ride' in output or
                'ridden' in output or 'vehicle' in output or 'transport' in output or
                'two-wheel' in output or 'cycle' in output):
            return 'correct'
        return 'incorrect'

    # Non-bicycle "control" rows are accessibility-concept probes (closed
    # captions / color contrast / page title) across varied templates (cloze,
    # question, instruction, evaluative, scenario). They are graded for
    # conceptual correctness — NOT used as the reasoning baseline (that is the
    # bicycle control). See DECISIONS.md.
    if concept == 'closed captions':
        if (('text' in output or 'subtitle' in output or 'word' in output or
             'read' in output or 'transcri' in output) and
                ('audio' in output or 'video' in output or 'sound' in output or
                 'spoken' in output or 'speech' in output or 'deaf' in output or
                 'hearing' in output or 'dialog' in output)):
            return 'correct'
        if ('caption' in output or 'subtitle' in output or
                'video' in output or 'audio' in output):
            return 'partial'
        return 'incorrect'

    if concept == 'color contrast':
        if (('distinguish' in output or 'difference between' in output or
             'see the diff' in output or 'readab' in output or
             'perceiv' in output or 'legib' in output) and 'color' in output):
            return 'correct'
        if 'color' in output or 'contrast' in output:
            return 'partial'
        return 'incorrect'

    if concept == 'page title':
        if (('describe' in output or 'identif' in output or 'summar' in output or
             'content' in output or 'topic' in output or 'tab' in output or
             'name of' in output) and
                ('page' in output or 'document' in output or 'site' in output or
                 'window' in output)):
            return 'correct'
        if 'page' in output or 'title' in output:
            return 'partial'
        return 'incorrect'

    return 'uncoded'


def code_validation(concept, prompt, output):
    """
    Code validation responses — held-out diagnostic and acronym probes
    (concepts: ARIA, HTML, alt text, screen reader; templates: direct_question,
    instruction, socratic, cloze). Routes by prompt content.

      - correct:   expands the acronym / names the missing attribute / explains
                   the screen-reader failure
      - partial:   right domain, wrong specifics
      - incorrect: fails to identify it
    """
    out = str(output).lower()
    p = str(prompt).lower()

    # Acronym expansion ("ARIA stands for", "HTML stands for")
    if 'stands for' in p:
        if 'aria' in p:
            if 'accessible rich internet' in out:
                return 'correct'
            return 'partial' if ('accessible' in out or 'accessibility' in out) else 'incorrect'
        if 'html' in p:
            if 'hypertext markup' in out or 'hyper text markup' in out:
                return 'correct'
            return 'partial' if ('markup' in out or 'hypertext' in out) else 'incorrect'

    # Screen-reader-failure reasoning ("...Why would it fail to describe <img>?")
    if 'screen reader' in p and ('fail' in p or 'why' in p):
        if ('text alternative' in out or 'no text' in out or 'no description' in out or
                'cannot read' in out or "can't read" in out or
                ('alt' in out and ('no ' in out or 'missing' in out or
                                    'without' in out or "n't" in out))):
            return 'correct'
        return 'incorrect'

    # Missing-attribute diagnosis on an <img> (alt text)
    if 'img' in p and ('missing' in p or "doesn't have" in p or 'attribute' in p):
        if 'alt' in out and ('missing' in out or 'attribute' in out or
                             'text' in out or 'description' in out):
            return 'correct'
        return 'incorrect'

    return 'incorrect'


def code_hypothesis(concept, prompt, output):
    """
    Code hypothesis responses — diagnostic alt-text probes (templates:
    direct_question, error_correction, socratic).

      - correct:   names/adds the missing alt attribute, or explains the failure
      - partial:   mentions alt without the diagnostic point
      - incorrect: fails to identify it
    """
    import re
    out = str(output).lower()
    p = str(prompt).lower()

    # "Correct the following inaccessible code: <img ...>" — expects alt=
    if 'correct' in p and 'img' in p:
        if re.search(r'alt\s*=', out):
            return 'correct'
        if 'alt' in out and ('attribute' in out or 'text' in out):
            return 'partial'
        return 'incorrect'

    # Screen-reader-failure reasoning
    if 'screen reader' in p and ('fail' in p or 'why' in p):
        if ('text alternative' in out or 'no text' in out or 'no description' in out or
                ('alt' in out and ('no ' in out or 'missing' in out or
                                    'without' in out or "n't" in out))):
            return 'correct'
        return 'incorrect'

    # "What specific attribute is missing ... <img>?"
    if 'img' in p and ('missing' in p or 'attribute' in p):
        if 'alt' in out and ('missing' in out or 'attribute' in out or
                             'text' in out or 'description' in out):
            return 'correct'
        return 'incorrect'

    return 'incorrect'


def code_completion(concept, prompt, output):
    """
    Code completion (few-shot / bare HTML) responses.

    Criteria: did the model emit the structurally-correct continuation —
    i.e. pattern-match the syntax — regardless of whether it can *define*
    the concept? This grades syntactic competence, which is the substrate
    for the "completion paradox": a model can produce alt="..." in context
    at scales where it cannot say what alt text is.

      - correct:   emits the expected attribute/element with non-empty content
      - partial:   emits the right attribute/element but empty or malformed
      - incorrect: does not produce the expected pattern

    Note: 'page title' and 'script' are syntactic controls — they have no
    declarative counterpart and serve as a baseline for pure pattern-matching.
    """
    import re
    out = str(output)
    low = out.lower()
    c = str(concept).strip().lower()

    if c == 'alt text':
        # expected continuation of `<img src="photo.jpg"` is ` alt="...">`
        if re.search(r'alt\s*=\s*["\'][^"\']+["\']', out):
            return 'correct'
        if re.search(r'alt\s*=\s*["\']\s*["\']', out) or 'alt=' in low:
            return 'partial'
        return 'incorrect'

    if c in ('captions', 'closed captions'):
        # expected continuation adds <track kind="captions" ...>
        if 'track' in low and 'caption' in low:
            return 'correct'
        if 'track' in low or 'caption' in low:
            return 'partial'
        return 'incorrect'

    if c == 'page title':
        # expected continuation produces a non-empty <title>...</title>
        if re.search(r'<title>\s*[^<\s][^<]*', out, re.I):
            return 'correct'
        if '<title>' in low:
            return 'partial'
        return 'incorrect'

    if c == 'script':
        # expected continuation produces a src="..." or closes the tag
        if re.search(r'src\s*=\s*["\'][^"\']+["\']', out):
            return 'correct'
        if 'src=' in low or '</script>' in low:
            return 'partial'
        return 'incorrect'

    return 'uncoded'
