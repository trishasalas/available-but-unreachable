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


def code_response(prompt_type, concept, prompt, output):
    """
    Route to the appropriate coding function based on prompt type.
    Returns: 'correct' | 'partial' | 'incorrect'
    """
    if prompt_type == 'declarative':
        return code_declarative(concept, output)
    elif prompt_type == 'evaluative':
        return code_evaluative(concept, prompt, output)
    elif prompt_type == 'control':
        return code_control(concept, prompt, output)
    elif prompt_type == 'completion':
        return code_completion(concept, prompt, output)
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

    return 'uncoded'


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
