"""Synthetic tests for the paired evaluative battery.

These examples are authored fixtures, not model outputs. They freeze what the
mechanical rubric means before the confirmatory runs.
"""

from pathlib import Path
import unittest

import pandas as pd

from src.paired_evaluative import (
    aggregate_pairs,
    build_gap_cells,
    code_paired_response,
    code_result_frame,
    load_battery,
    summarize_gap,
    validate_battery,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BATTERY_PATH = PROJECT_ROOT / "data" / "evaluative_paired.yaml"
DECLARATIVE_PATH = PROJECT_ROOT / "data" / "accessibility.yaml"


VIOLATION_CORRECT = {
    "alt text": "inaccessible because the image is missing an alt attribute",
    "closed captions": "inaccessible because captions are missing from the video",
    "color contrast": "inaccessible because the text contrast is too low",
    "focus indicator": "inaccessible because the visible focus outline was removed",
    "keyboard navigation": (
        "inaccessible because positive tabindex values override the natural document order"
    ),
    "semantic HTML": (
        "inaccessible because the div is only visually a heading and is not marked "
        "as a programmatic heading"
    ),
    "skip link": "inaccessible because there is no way to bypass the repeated navigation",
    "screen reader": (
        "inaccessible because aria-hidden removes the main content from the accessibility tree"
    ),
}


class BatteryValidationTests(unittest.TestCase):
    def test_approved_proposal_has_exact_structure(self):
        battery = load_battery(BATTERY_PATH)
        validate_battery(battery, DECLARATIVE_PATH)
        self.assertEqual(len(battery["prompts"]), 16)


class FrozenCodingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.battery = load_battery(BATTERY_PATH)

    def test_each_violation_rule_accepts_specific_failure(self):
        for item in self.battery["prompts"]:
            if item["polarity"] != "violation":
                continue
            with self.subTest(concept=item["concept"]):
                self.assertEqual(
                    code_paired_response(item, VIOLATION_CORRECT[item["concept"]]),
                    "correct",
                )

    def test_generic_inaccessible_is_partial_on_violation(self):
        for item in self.battery["prompts"]:
            if item["polarity"] != "violation":
                continue
            with self.subTest(concept=item["concept"]):
                self.assertEqual(
                    code_paired_response(item, "inaccessible because something is wrong"),
                    "partial",
                )

    def test_accessible_is_incorrect_on_violation(self):
        for item in self.battery["prompts"]:
            if item["polarity"] != "violation":
                continue
            with self.subTest(concept=item["concept"]):
                self.assertEqual(code_paired_response(item, "accessible"), "incorrect")

    def test_accessible_is_correct_on_conformant(self):
        for item in self.battery["prompts"]:
            if item["polarity"] != "conformant":
                continue
            with self.subTest(concept=item["concept"]):
                self.assertEqual(
                    code_paired_response(item, "accessible based on the code shown"),
                    "correct",
                )

    def test_inaccessible_is_incorrect_on_conformant(self):
        for item in self.battery["prompts"]:
            if item["polarity"] != "conformant":
                continue
            with self.subTest(concept=item["concept"]):
                self.assertEqual(
                    code_paired_response(item, "inaccessible because it fails accessibility"),
                    "incorrect",
                )

    def test_accessible_but_asserting_target_fault_is_incorrect_on_conformant(self):
        item = next(
            item
            for item in self.battery["prompts"]
            if item["concept"] == "alt text" and item["polarity"] == "conformant"
        )
        self.assertEqual(
            code_paired_response(
                item,
                "accessible, but the image is missing an alt attribute",
            ),
            "incorrect",
        )

    def test_unclear_conformant_response_is_partial(self):
        item = next(
            item for item in self.battery["prompts"] if item["polarity"] == "conformant"
        )
        self.assertEqual(code_paired_response(item, "the code contains an image"), "partial")

    def test_degenerate_response_is_incorrect(self):
        item = self.battery["prompts"][0]
        self.assertEqual(
            code_paired_response(item, "accessible accessible accessible"),
            "incorrect",
        )


class AggregationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.battery = load_battery(BATTERY_PATH)

    def _complete_synthetic_results(self):
        rows = []
        for item in self.battery["prompts"]:
            output = (
                VIOLATION_CORRECT[item["concept"]]
                if item["polarity"] == "violation"
                else "accessible based on the code shown"
            )
            rows.append({
                "prompt_id": item["prompt_id"],
                "output": output,
                "model": "pythia-160m",
            })
        # One concept demonstrates the gap: declarative correct, violation wrong.
        for row in rows:
            if row["prompt_id"] == "evalp_alt_text_primary_violation":
                row["output"] = "accessible"
        return pd.DataFrame(rows)

    def test_pair_pass_requires_both_polarities(self):
        coded = code_result_frame(self._complete_synthetic_results(), self.battery)
        pairs = aggregate_pairs(coded)
        alt = pairs[pairs["concept"] == "alt text"].iloc[0]
        captions = pairs[pairs["concept"] == "closed captions"].iloc[0]
        self.assertFalse(bool(alt["evaluative_pass"]))
        self.assertTrue(bool(captions["evaluative_pass"]))
        self.assertEqual(len(pairs), 8)

    def test_gap_summary_prints_conditional_denominator(self):
        coded = code_result_frame(self._complete_synthetic_results(), self.battery)
        pairs = aggregate_pairs(coded)
        declarative = pd.DataFrame({
            "suite": ["pythia"] * 8,
            "scale": ["160M"] * 8,
            "concept_key": [concept.lower().replace(" ", "_") for concept in VIOLATION_CORRECT],
            "declarative_accuracy": ["correct"] * 8,
        })
        cells = build_gap_cells(pairs, declarative)
        summary = summarize_gap(cells).iloc[0]
        self.assertEqual(int(summary["gap_given_declarative_numerator"]), 1)
        self.assertEqual(int(summary["gap_given_declarative_denominator"]), 8)
        self.assertEqual(float(summary["gap_given_declarative_pct"]), 12.5)
        self.assertEqual(int(cells["gap_cell"].sum()), 1)

    def test_incomplete_model_output_is_rejected(self):
        incomplete = self._complete_synthetic_results().iloc[:-1]
        with self.assertRaisesRegex(ValueError, "incomplete paired result set"):
            code_result_frame(incomplete, self.battery)


if __name__ == "__main__":
    unittest.main()
