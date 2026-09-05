import unittest
import pandas as pd
from src.effective_binding_validation import validate_binding_output


class BindingOutputValidationTests(unittest.TestCase):
    def setUp(self):
        self.cases = [dict(name='keyboard_navigation', word1='keyboard', word2='navigation',
                           prompt='Keyboard navigation allows')]
        self.frame = pd.DataFrame([dict(compound='keyboard_navigation', layer=l, head=h,
            model='gpt2-medium', prompt_condition='uniform', prompt='A keyboard navigation is',
            word1='keyboard', word2='navigation', attention_weight=.2, ov_write_norm=1.,
            weighted_ov_norm=.2, relative_weighted_ov_norm=.1, target_residual_norm=2.)
            for l in range(2) for h in range(2)])

    def check_frame(self, frame):
        validate_binding_output(frame, self.cases, 'gpt2-medium', 'uniform', 2, 2)

    def test_valid_run(self):
        self.check_frame(self.frame)

    def test_natural_output_with_uniform_label_is_rejected(self):
        frame = self.frame.assign(prompt='Keyboard navigation allows')
        with self.assertRaisesRegex(ValueError, 'saved prompt'):
            self.check_frame(frame)

    def test_missing_and_duplicate_heads_are_rejected(self):
        for frame in [self.frame.iloc[:-1], pd.concat([self.frame.iloc[:-1], self.frame.iloc[[0]]])]:
            with self.assertRaises(ValueError):
                self.check_frame(frame)

    def test_nonfinite_measurement_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'finite'):
            self.check_frame(self.frame.assign(ov_write_norm=float('inf')))

    def test_stale_model_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Model'):
            self.check_frame(self.frame.assign(model='gpt2-large'))
