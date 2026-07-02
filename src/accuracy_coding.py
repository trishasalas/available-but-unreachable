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


# ---------------------------------------------------------------------------
# n=49 EXPANSION — criteria pending (2026-07-01)
#
# The 41 compounds below have elicitation runs but NO coding criteria yet.
# They are guarded in code_response() to return 'uncoded' until authored.
#
# Authoring workflow (see docs/findings/coding-criteria-draft.md):
#   1. Author criteria in the worksheet, frequency_table.csv CLOSED.
#   2. Decide the sense policy ONCE (worksheet, Option A/B) — several of
#      these have dominant non-a11y senses (menu bar, sign language, …).
#   3. Add each concept's rules to code_declarative's `rules` dict using the
#      existing house pattern (correct-markers + partial-markers), and REMOVE
#      it from PENDING_CRITERIA in the same commit.
#   4. DECISIONS.md entry (2026-06-28 policy) with the commit hash.
#   5. Regression guard: the original 8 compounds' rows in
#      per_concept_trajectories.csv must be byte-identical before/after.
#
# Naming note: concept strings below are GUESSES at the space-separated form
# (frequency_table.csv uses underscores; its `concept` column maps e.g.
# closed_captions -> "captions"). VERIFY each against the actual `concept`
# values in the new elicitation CSVs before trusting the guard — a mismatch
# here silently re-opens the fall-through-to-'incorrect' hazard.
# ---------------------------------------------------------------------------

PENDING_CRITERIA = {
    # WCAG success-criterion terms
    'input purpose', 'target size', 'touch target', 'drag movement',
    'focus appearance', 'consistent help', 'redundant entry',
    'accessible authentication', 'text spacing', 'status message',
    'error identification', 'pointer cancellation', 'character key',
    'sensory characteristics',
    # ARIA / assistive-tech terms
    'accessibility tree', 'accessible name', 'accessible description',
    'live region', 'tab panel', 'radio group', 'tree grid', 'menu bar',
    'tool tip', 'combo box', 'landmark region',
    # practice / content terms
    'keyboard interaction', 'section heading', 'text alternative',
    'audio description', 'sign language', 'semantic markup',
    'focus management', 'reading order', 'text formatting', 'form field',
    'low vision', 'cognitive disabilities', 'universal design',
    'decorative image', 'informative image', 'responsive design',
}


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
