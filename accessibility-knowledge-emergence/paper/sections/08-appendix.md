\newpage

## Appendix A

### 1. Declarative Prompts

All declarative experiments used completion-style prompts. Models were
given the prompt prefix and generated a continuation.

- A screen reader is
- WCAG stands for
- A skip link is
- The purpose of alt text is
- ARIA stands for
- A focus indicator is
- Keyboard navigation allows
- Color contrast is important because
- Semantic HTML helps
- Captions are used for

### 2. Evaluative Prompts

Evaluative experiments used zero-shot code completion prompts.

- The following code is not accessible because it doesn't have what?
  `<img src='photo.jpg'>`
- A `<div>` with onclick is not accessible because
- The accessibility problem with `<a href='#'></a>` is
- `<input type='text'>` needs a
- A button that only says 'Click here' is bad because

\newpage

### 3. Perplexity Pairs

Each pair consists of a correct and incorrect definition. Perplexity was
computed for each sentence independently. Values below 1.0 on the
preference ratio indicate the model finds the wrong definition more
natural.

| Concept |       Correct      |      Incorrect      |
| ---------- | ---------------- | --------------- |
| screen  reader | A screen reader is software that reads text aloud for blind users. | A screen reader is a device for viewing screens.       |
| alt text | The purpose of alt text is to provide a textual description of an image for people with visual disabilities. | The purpose of alt text is to make images load faster. |
| skip link | A skip link is a navigation aid that allows keyboard users to bypass repetitive content. | A skip link is a broken hyperlink that does not load.                                                       |


\newpage

## Appendix B

### Model Architectures

All experiments used base (non-instruction-tuned) model checkpoints.

#### Pythia Scaling Suite

\smallskip

Architecture: parallel attention + MLP blocks.

**Table 2**

| Model | Layers | Heads | d_model | d_mlp |
|-------|-------|-------|-------|-------|
| 160M | 12 | 12 | 768 | 3,072 |
| 410M | 24 | 16 | 1,024 | 4,096 |
| 1B | 16 | 8 | 2,048 | 8,192 |
| 2.8B | 32 | 32 | 2,560 | 10,240 |
| 6.9B | 32 | 32 |4,096 | 16,384 |
| 12B | 36 | 40 | 5,120 | 20,480 |

#### GPT-2 Model Family

\smallskip

Architecture: sequential attention + MLP blocks.

**Table 3**

| Model | Layers | Heads | d_model | d_mlp |
|-------|-------|-------|-------|-------|
| Small (117M) | 12 | 12 | 768 | 3,072 |
| Medium (406M)| 24 | 16 | 1,024 | 4,096 |
| Large (838M) | 36 | 20 | 1,280 | 5,120 |
| XL (1.5B) | 48 | 25 | 1,600 | 6,400 |

\newpage

## Appendix C

### 1. Completion Prompts

- **Alt text - Few Shot:** \
  `<img src="icons/home.png" alt="Home">`\
  `<img src="icons/mail.png" alt="Inbox">`\
  `<img src="photo.jpg`
- **Alt Text - Bare:** \
  `<img src="photo.jpg"`
- **Closed Captions - Few Shot:** \
  `<video src="intro.mp4">`\
  `<track kind="captions" src="intro.vtt"></video>`\
  `<video src="demo.mp4"><track kind="captions" src="demo.vtt"></video>`\
  `<video src="lecture.mp4">`
- **Closed Captions - Bare:** \
  `<video src="lecture.mp4">`
- **Page Title - Few Shot:** \
  `<html><head><title>About Us</title></head>`\
  `<html><head><title>Contact</title></head>`\
  `<html><head>`
- **Page Title - Bare:** \
  `<html><head><meta charset="utf-8">`
- **Script Source - Bare (control):** \
  `<script`
- **Script Source - Few Shot (control):** \
  `<script src="utils.js"></script>`\
  `<script src="main.js"></script>`\
  `<script src="`

### 2. Hypothesis Driven Prompts

- **Direct Question:** \
  Look at this HTML: `<img src='portrait.jpg'>`.\
  What specific attribute is missing to make it accessible?\
  **Expected Failure:** Model repeats the tag or provides a generic
  definition of images rather than 'alt text'.
- **Error Correction:** \
  Correct the following inaccessible code: `<img src='logo.png'>`.\
  **Expected Failure:** Model completes the line with more attributes
  (like width or height) but ignores the alt attribute.
- **Negative Constraint (Socratic)**\
  A screen reader is software that reads text aloud.\
  Why would a screen reader fail to describe this tag:\
  `<img src='chart.svg'>`?\
  **Expected Failure:** Despite the 'screen reader' anchor (which is
  deeply bound at 2.8B), the model cannot link the concept to the lack
  of an alt attribute.

### 3. Validation Prompts

- **Direct Completion:** \
  The following code is not accessible because it doesn't have what?
  `<img src='photo.jpg'>`?\
  **Expected Behavior:** Stalls or repeats prompt despite correctly
  defining 'alt text' elsewhere.
- **Instructional Correction:** \
  What accessibility attribute is missing from this HTML:
  `<img src='photo.jpg'>`?\
  **Expected Behavior:** Failure to answer 'alt text'.
- **Functional Socratic:\**
  A screen reader is software that reads text aloud. Why would it fail
  to describe `<img src='photo.jpg'>`?\
  **Expected Behavior:** Model fails to link the 'screen reader'
  definition to the missing 'alt' attribute."
- **Fluent Confabulation (Control):\**
  ARIA stands for\
  **Expected Behavior:** Produces confident but incorrect expansions.
- **Fluent Confabulation (Control):\**
  HTML stands for\
  **Expected Behavior:** Produces confident but incorrect expansions.
