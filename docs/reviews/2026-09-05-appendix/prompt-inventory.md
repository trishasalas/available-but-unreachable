# Prompt inventory extracted for review


Verbatim prompt strings and existing expected judgments; no wording or coding criteria changed.


## Original batteries

### decl_screen_reader_001

```text
A screen reader is
```

Continuation limit: 100 tokens.

### decl_wcag_001

```text
WCAG stands for
```

Continuation limit: 100 tokens.

### decl_skip_link_001

```text
A skip link is
```

Continuation limit: 100 tokens.

### decl_alt_text_001

```text
The purpose of alt text is
```

Continuation limit: 100 tokens.

### decl_aria_001

```text
ARIA stands for
```

Continuation limit: 100 tokens.

### decl_focus_indicator_001

```text
A focus indicator is
```

Continuation limit: 100 tokens.

### decl_keyboard_nav_001

```text
Keyboard navigation allows
```

Continuation limit: 100 tokens.

### decl_color_contrast_001

```text
Color contrast is important because
```

Continuation limit: 100 tokens.

### decl_semantic_html_001

```text
Semantic HTML helps
```

Continuation limit: 100 tokens.

### decl_captions_001

```text
Closed captions are used for
```

Continuation limit: 100 tokens.

### eval_alt_text_001

```text
The following code is not accessible because it doesn't have what? <img src='photo.jpg'>
```

Continuation limit: 100 tokens.

### eval_div_onclick_001

```text
A <div> with onclick is not accessible because
```

Continuation limit: 100 tokens.

### eval_empty_link_001

```text
The accessibility problem with <a href='#'></a> is
```

Continuation limit: 100 tokens.

### eval_unlabeled_input_001

```text
<input type='text'> needs a
```

Continuation limit: 100 tokens.

### eval_click_here_001

```text
A button that only says 'Click here' is bad because
```

Continuation limit: 100 tokens.

## Additional declarative frequency probes

### decl_keyboard_interaction_001

```text
A keyboard interaction is
```

Continuation limit: 100 tokens.

### decl_section_heading_001

```text
A section heading is
```

Continuation limit: 100 tokens.

### decl_text_alternative_001

```text
A text alternative is
```

Continuation limit: 100 tokens.

### decl_audio_description_001

```text
An audio description is
```

Continuation limit: 100 tokens.

### decl_sign_language_001

```text
Sign language is
```

Continuation limit: 100 tokens.

### decl_sensory_characteristics_001

```text
Sensory characteristics are
```

Continuation limit: 100 tokens.

### decl_input_purpose_001

```text
An input purpose is
```

Continuation limit: 100 tokens.

### decl_target_size_001

```text
A target size is
```

Continuation limit: 100 tokens.

### decl_touch_target_001

```text
A touch target is
```

Continuation limit: 100 tokens.

### decl_drag_movement_001

```text
A drag movement is
```

Continuation limit: 100 tokens.

### decl_focus_appearance_001

```text
A focus appearance is
```

Continuation limit: 100 tokens.

### decl_consistent_help_001

```text
Consistent help is
```

Continuation limit: 100 tokens.

### decl_redundant_entry_001

```text
A redundant entry is
```

Continuation limit: 100 tokens.

### decl_accessible_authentication_001

```text
Accessible authentication is
```

Continuation limit: 100 tokens.

### decl_text_spacing_001

```text
Text spacing is
```

Continuation limit: 100 tokens.

### decl_status_message_001

```text
A status message is
```

Continuation limit: 100 tokens.

### decl_error_identification_001

```text
Error identification is
```

Continuation limit: 100 tokens.

### decl_pointer_cancellation_001

```text
Pointer cancellation is
```

Continuation limit: 100 tokens.

### decl_character_key_001

```text
A character key is
```

Continuation limit: 100 tokens.

### decl_accessibility_tree_001

```text
An accessibility tree is
```

Continuation limit: 100 tokens.

### decl_accessible_name_001

```text
An accessible name is
```

Continuation limit: 100 tokens.

### decl_accessible_description_001

```text
An accessible description is
```

Continuation limit: 100 tokens.

### decl_live_region_001

```text
A live region is
```

Continuation limit: 100 tokens.

### decl_tab_panel_001

```text
A tab panel is
```

Continuation limit: 100 tokens.

### decl_radio_group_001

```text
A radio group is
```

Continuation limit: 100 tokens.

### decl_tree_grid_001

```text
A tree grid is
```

Continuation limit: 100 tokens.

### decl_menu_bar_001

```text
A menu bar is
```

Continuation limit: 100 tokens.

### decl_tool_tip_001

```text
A tool tip is
```

Continuation limit: 100 tokens.

### decl_combo_box_001

```text
A combo box is
```

Continuation limit: 100 tokens.

### decl_semantic_markup_001

```text
Semantic markup is
```

Continuation limit: 100 tokens.

### decl_focus_management_001

```text
Focus management is
```

Continuation limit: 100 tokens.

### decl_reading_order_001

```text
Reading order is
```

Continuation limit: 100 tokens.

### decl_text_formatting_001

```text
Text formatting is
```

Continuation limit: 100 tokens.

### decl_form_field_001

```text
A form field is
```

Continuation limit: 100 tokens.

### decl_landmark_region_001

```text
A landmark region is
```

Continuation limit: 100 tokens.

### decl_low_vision_001

```text
Low vision is
```

Continuation limit: 100 tokens.

### decl_cognitive_disabilities_001

```text
Cognitive disabilities are
```

Continuation limit: 100 tokens.

### decl_universal_design_001

```text
Universal design is
```

Continuation limit: 100 tokens.

### decl_decorative_image_001

```text
A decorative image is
```

Continuation limit: 100 tokens.

### decl_informative_image_001

```text
An informative image is
```

Continuation limit: 100 tokens.

### decl_responsive_design_001

```text
Responsive design is
```

Continuation limit: 100 tokens.

## Frozen paired battery

### evalp_alt_text_primary_violation

```text
<h1>Heavy-Duty Dish Soap</h1><p>Tired of coming home to this?</p><img src='sink.jpg'><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: inaccessible because the image is missing an alt attribute or text alternative

### evalp_alt_text_primary_conformant

```text
<h1>Heavy-Duty Dish Soap</h1><p>Tired of coming home to this?</p><img src='sink.jpg' alt='Sink filled with dirty dishes'><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: accessible with respect to the image; does not invent a missing-alt problem

### evalp_captions_primary_violation

```text
<h2>Lecture 4: Cell Division</h2><video src='lecture.mp4' controls></video><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: inaccessible because the video has no captions or equivalent text alternative

### evalp_captions_primary_conformant

```text
<h2>Lecture 4: Cell Division</h2><video src='lecture.mp4' controls><track kind='captions' src='lecture.vtt' srclang='en' label='English'></video><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: accessible with respect to captions; does not claim captions are missing

### evalp_contrast_primary_violation

```text
<p style='color:#999999; background:#ffffff'>Read our full privacy policy.</p><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: inaccessible because the text contrast is insufficient

### evalp_contrast_primary_conformant

```text
<p style='color:#767676; background:#ffffff'>Read our full privacy policy.</p><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: accessible with respect to text contrast; does not claim the contrast is insufficient

### evalp_focus_indicator_primary_violation

```text
<button class='buy'>Buy now</button><style>.buy:focus { outline: none; }</style><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: inaccessible because keyboard focus has no visible indicator

### evalp_focus_indicator_primary_conformant

```text
<button class='buy'>Buy now</button><style>.buy:focus { outline: 3px solid #005fcc; outline-offset: 2px; }</style><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: accessible with respect to visible keyboard focus; does not claim the indicator is missing

### evalp_keyboard_navigation_primary_violation

```text
<form><label>First name <input name='first' tabindex='2'></label><label>Last name <input name='last' tabindex='1'></label><button type='submit' tabindex='3'>Submit</button></form><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: inaccessible because positive tabindex values override the natural document order; interactive elements should remain in source order rather than being manually numbered

### evalp_keyboard_navigation_primary_conformant

```text
<form><label>First name <input name='first'></label><label>Last name <input name='last'></label><button type='submit'>Submit</button></form><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: accessible with respect to tab order; native interactive elements need no tabindex and follow First name, Last name, then Submit in document order

### evalp_semantic_html_primary_violation

```text
<div class='heading'>Shipping information</div><p>Orders ship within two business days.</p><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: inaccessible because a visual heading is not marked up as a programmatic heading

### evalp_semantic_html_primary_conformant

```text
<h2>Shipping information</h2><p>Orders ship within two business days.</p><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: accessible with respect to heading semantics; does not claim the heading lacks structure

### evalp_skip_link_primary_violation

```text
A site repeats a 40-link navigation menu at the top of every page. A keyboard user must tab through all 40 links before reaching the main content, and the page provides no way to bypass the menu. Based only on this description, an accessibility reviewer should mark the page as
```

Continuation limit: 100 tokens.

Frozen expected judgment: inaccessible because repeated navigation cannot be bypassed

### evalp_skip_link_primary_conformant

```text
A site repeats a 40-link navigation menu at the top of every page. The first focusable element lets a keyboard user jump directly to the main content. Based only on this description, an accessibility reviewer should mark the page as
```

Continuation limit: 100 tokens.

Frozen expected judgment: accessible with respect to bypassing repeated navigation; does not claim a bypass is missing

### evalp_screen_reader_primary_violation

```text
<main aria-hidden='true'><h1>Order status</h1><p>Your order has shipped.</p></main><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: inaccessible because the main content is hidden from screen readers or the accessibility tree

### evalp_screen_reader_primary_conformant

```text
<main><h1>Order status</h1><p>Your order has shipped.</p></main><p>Based only on the code shown, an accessibility reviewer should mark this example as
```

Continuation limit: 100 tokens.

Frozen expected judgment: accessible with respect to screen-reader exposure; does not claim the main content is hidden

## Binding inventory

### screen_reader

Natural:
```text
A screen reader is
```

Uniform:
```text
A screen reader is
```

### alt_text

Natural:
```text
The purpose of alt text is
```

Uniform:
```text
A alt text is
```

### skip_link

Natural:
```text
A skip link is
```

Uniform:
```text
A skip link is
```

### color_contrast

Natural:
```text
Color contrast is important because
```

Uniform:
```text
A color contrast is
```

### keyboard_navigation

Natural:
```text
Keyboard navigation allows
```

Uniform:
```text
A keyboard navigation is
```

### closed_captions

Natural:
```text
Closed captions are used for
```

Uniform:
```text
A closed captions is
```

### focus_indicator

Natural:
```text
A focus indicator is
```

Uniform:
```text
A focus indicator is
```

### semantic_html

Natural:
```text
Semantic HTML helps
```

Uniform:
```text
A semantic HTML is
```

### form_label

Natural:
```text
A form label is
```

Uniform:
```text
A form label is
```

### link_text

Natural:
```text
Link text describes
```

Uniform:
```text
A link text is
```

### page_title

Natural:
```text
A page title describes
```

Uniform:
```text
A page title is
```

### keyboard_interaction

Natural:
```text
A keyboard interaction is
```

Uniform:
```text
A keyboard interaction is
```

### section_heading

Natural:
```text
A section heading is
```

Uniform:
```text
A section heading is
```

### text_alternative

Natural:
```text
A text alternative is
```

Uniform:
```text
A text alternative is
```

### audio_description

Natural:
```text
An audio description is
```

Uniform:
```text
A audio description is
```

### sign_language

Natural:
```text
Sign language is
```

Uniform:
```text
A sign language is
```

### sensory_characteristics

Natural:
```text
Sensory characteristics are
```

Uniform:
```text
A sensory characteristics is
```

### input_purpose

Natural:
```text
An input purpose is
```

Uniform:
```text
A input purpose is
```

### target_size

Natural:
```text
A target size is
```

Uniform:
```text
A target size is
```

### touch_target

Natural:
```text
A touch target is
```

Uniform:
```text
A touch target is
```

### drag_movement

Natural:
```text
A drag movement is
```

Uniform:
```text
A drag movement is
```

### focus_appearance

Natural:
```text
A focus appearance is
```

Uniform:
```text
A focus appearance is
```

### consistent_help

Natural:
```text
Consistent help is
```

Uniform:
```text
A consistent help is
```

### redundant_entry

Natural:
```text
A redundant entry is
```

Uniform:
```text
A redundant entry is
```

### accessible_authentication

Natural:
```text
Accessible authentication is
```

Uniform:
```text
A accessible authentication is
```

### text_spacing

Natural:
```text
Text spacing is
```

Uniform:
```text
A text spacing is
```

### status_message

Natural:
```text
A status message is
```

Uniform:
```text
A status message is
```

### error_identification

Natural:
```text
Error identification is
```

Uniform:
```text
A error identification is
```

### pointer_cancellation

Natural:
```text
Pointer cancellation is
```

Uniform:
```text
A pointer cancellation is
```

### character_key

Natural:
```text
A character key is
```

Uniform:
```text
A character key is
```

### accessibility_tree

Natural:
```text
An accessibility tree is
```

Uniform:
```text
A accessibility tree is
```

### accessible_name

Natural:
```text
An accessible name is
```

Uniform:
```text
A accessible name is
```

### accessible_description

Natural:
```text
An accessible description is
```

Uniform:
```text
A accessible description is
```

### live_region

Natural:
```text
A live region is
```

Uniform:
```text
A live region is
```

### tab_panel

Natural:
```text
A tab panel is
```

Uniform:
```text
A tab panel is
```

### radio_group

Natural:
```text
A radio group is
```

Uniform:
```text
A radio group is
```

### tree_grid

Natural:
```text
A tree grid is
```

Uniform:
```text
A tree grid is
```

### menu_bar

Natural:
```text
A menu bar is
```

Uniform:
```text
A menu bar is
```

### tool_tip

Natural:
```text
A tool tip is
```

Uniform:
```text
A tool tip is
```

### combo_box

Natural:
```text
A combo box is
```

Uniform:
```text
A combo box is
```

### semantic_markup

Natural:
```text
Semantic markup is
```

Uniform:
```text
A semantic markup is
```

### focus_management

Natural:
```text
Focus management is
```

Uniform:
```text
A focus management is
```

### reading_order

Natural:
```text
Reading order is
```

Uniform:
```text
A reading order is
```

### text_formatting

Natural:
```text
Text formatting is
```

Uniform:
```text
A text formatting is
```

### form_field

Natural:
```text
A form field is
```

Uniform:
```text
A form field is
```

### landmark_region

Natural:
```text
A landmark region is
```

Uniform:
```text
A landmark region is
```

### low_vision

Natural:
```text
Low vision is
```

Uniform:
```text
A low vision is
```

### cognitive_disabilities

Natural:
```text
Cognitive disabilities are
```

Uniform:
```text
A cognitive disabilities is
```

### universal_design

Natural:
```text
Universal design is
```

Uniform:
```text
A universal design is
```

### decorative_image

Natural:
```text
A decorative image is
```

Uniform:
```text
A decorative image is
```

### informative_image

Natural:
```text
An informative image is
```

Uniform:
```text
A informative image is
```

### responsive_design

Natural:
```text
Responsive design is
```

Uniform:
```text
A responsive design is
```

### empty_link

Natural:
```text
An empty link is
```

Uniform:
```text
A empty link is
```
