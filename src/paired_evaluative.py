"""Validation, frozen coding, and analysis for the paired evaluative battery.

This module does not run models. It keeps the new paired estimator separate
from ``src.gap_analysis`` and never writes the historical ``*_gap.csv`` files.

The coding rules below are authored against the approved prompts and synthetic
responses only. Do not change them after the battery freeze in response to
model output; any later amendment needs a dated decision and a full recode.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Callable, Mapping

import pandas as pd
import yaml


CONCEPTS = (
    "screen reader",
    "skip link",
    "alt text",
    "focus indicator",
    "keyboard navigation",
    "color contrast",
    "semantic HTML",
    "closed captions",
)

DECLARATIVE_PROMPTS = {
    "screen reader": "decl_screen_reader_001",
    "skip link": "decl_skip_link_001",
    "alt text": "decl_alt_text_001",
    "focus indicator": "decl_focus_indicator_001",
    "keyboard navigation": "decl_keyboard_nav_001",
    "color contrast": "decl_color_contrast_001",
    "semantic HTML": "decl_semantic_html_001",
    "closed captions": "decl_captions_001",
}

MODEL_META = {
    "pythia-160m": ("pythia", "160M"),
    "pythia-410m": ("pythia", "410M"),
    "pythia-1b": ("pythia", "1B"),
    "pythia-2.8b": ("pythia", "2.8B"),
    "pythia-6.9b": ("pythia", "6.9B"),
    "pythia-12b": ("pythia", "12B"),
    "gpt2": ("gpt2", "124M"),
    "gpt2-medium": ("gpt2", "355M"),
    "gpt2-large": ("gpt2", "774M"),
    "gpt2-xl": ("gpt2", "1.5B"),
    "OLMo-2-0425-1B": ("olmo", "1B"),
    "OLMo-2-1124-7B": ("olmo", "7B"),
    "OLMo-2-1124-13B": ("olmo", "13B"),
}

PILOT_MODELS = frozenset({"pythia-2.8b"})
REQUIRED_ITEM_FIELDS = frozenset({
    "prompt_id",
    "pair_id",
    "concept",
    "prompt_type",
    "template_type",
    "polarity",
    "paired_with",
    "prompt",
    "expected",
    "max_tokens",
})


def load_battery(path: str | Path) -> dict:
    """Load a paired-battery YAML document."""
    with Path(path).open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict) or not isinstance(data.get("prompts"), list):
        raise ValueError("paired battery must be a mapping with a prompts list")
    return data


def validate_battery(
    battery: Mapping,
    declarative_path: str | Path | None = None,
) -> None:
    """Raise ``ValueError`` if the approved 8 × 2 structure is not intact."""
    prompts = list(battery.get("prompts", []))
    errors: list[str] = []

    if len(prompts) != 16:
        errors.append(f"expected 16 prompts, found {len(prompts)}")

    prompt_ids = [item.get("prompt_id") for item in prompts]
    if len(set(prompt_ids)) != len(prompt_ids):
        errors.append("prompt_id values are not unique")

    for item in prompts:
        missing = REQUIRED_ITEM_FIELDS - set(item)
        if missing:
            errors.append(
                f"{item.get('prompt_id', '<missing id>')} missing fields {sorted(missing)}"
            )
        if item.get("prompt_type") != "evaluative_paired":
            errors.append(f"{item.get('prompt_id')} has wrong prompt_type")
        if item.get("template_type") != "neutral_review":
            errors.append(f"{item.get('prompt_id')} has wrong template_type")
        if item.get("polarity") not in {"violation", "conformant"}:
            errors.append(f"{item.get('prompt_id')} has invalid polarity")
        if item.get("max_tokens") != 100:
            errors.append(f"{item.get('prompt_id')} must use max_tokens=100")

    found_concepts = {item.get("concept") for item in prompts}
    if found_concepts != set(CONCEPTS):
        errors.append(
            f"concept set differs: missing={sorted(set(CONCEPTS) - found_concepts)}, "
            f"extra={sorted(found_concepts - set(CONCEPTS))}"
        )

    pair_counts = Counter((item.get("concept"), item.get("polarity")) for item in prompts)
    for concept in CONCEPTS:
        for polarity in ("violation", "conformant"):
            if pair_counts[(concept, polarity)] != 1:
                errors.append(
                    f"{concept!r} must have exactly one {polarity} item; "
                    f"found {pair_counts[(concept, polarity)]}"
                )
        pair_ids = {item.get("pair_id") for item in prompts if item.get("concept") == concept}
        if len(pair_ids) != 1:
            errors.append(f"{concept!r} must have one shared pair_id")
        paired_with = {
            item.get("paired_with") for item in prompts if item.get("concept") == concept
        }
        if paired_with != {DECLARATIVE_PROMPTS[concept]}:
            errors.append(f"{concept!r} maps to the wrong declarative prompt")

    metadata = battery.get("metadata", {})
    if metadata.get("primary_scoring") != "both_polarities_must_be_correct":
        errors.append("metadata primary_scoring does not match the approved rule")
    if set(metadata.get("pilot_models", [])) != set(PILOT_MODELS):
        errors.append("metadata pilot_models does not match the approved pilot split")

    if declarative_path is not None:
        with Path(declarative_path).open(encoding="utf-8") as handle:
            declarative = yaml.safe_load(handle)
        decl_map = {
            item["prompt_id"]: item["concept"]
            for item in declarative.get("prompts", [])
            if item.get("prompt_type") == "declarative"
        }
        for concept, prompt_id in DECLARATIVE_PROMPTS.items():
            if decl_map.get(prompt_id) != concept:
                errors.append(
                    f"declarative mapping mismatch for {concept!r}: "
                    f"{prompt_id!r} -> {decl_map.get(prompt_id)!r}"
                )

    if errors:
        raise ValueError("paired battery validation failed:\n- " + "\n- ".join(errors))


def _has(text: str, *needles: str) -> bool:
    return any(needle in text for needle in needles)


def _missing_language(text: str) -> bool:
    return _has(
        text,
        "missing",
        "lacks",
        "lack of",
        "without",
        "does not have",
        "doesn't have",
        "no alt",
        "no caption",
        "not provided",
        "absent",
    )


def _alt_reason(text: str) -> bool:
    target = _has(text, "alt text", "alt attribute", "alternative text", "text alternative")
    return target and _missing_language(text)


def _captions_reason(text: str) -> bool:
    return "caption" in text and _missing_language(text)


def _contrast_reason(text: str) -> bool:
    return "contrast" in text and _has(
        text,
        "insufficient",
        "too low",
        "low contrast",
        "poor contrast",
        "not enough",
        "hard to read",
        "difficult to read",
        "2.85",
        "below 4.5",
        "fails",
    )


def _focus_reason(text: str) -> bool:
    target = "focus" in text and _has(text, "outline", "indicator", "visible", "visibility")
    missing = _has(
        text,
        "none",
        "missing",
        "no visible",
        "not visible",
        "removed",
        "suppressed",
        "without",
        "lack",
    )
    return target and missing


def _keyboard_reason(text: str) -> bool:
    explicit = "tabindex" in text and _has(
        text,
        "positive",
        "greater than zero",
        "> 0",
        "override",
        "manual",
        "numbered",
        "source order",
        "document order",
        "natural order",
    )
    order = _has(text, "tab order", "focus order") and _has(
        text,
        "wrong",
        "incorrect",
        "illogical",
        "out of order",
        "does not follow",
        "doesn't follow",
        "last name",
    )
    return explicit or order


def _semantic_reason(text: str) -> bool:
    target = "heading" in text and _has(
        text,
        "div",
        "h2",
        "semantic",
        "programmatic",
        "structure",
        "screen reader",
    )
    fault = _has(
        text,
        "not marked",
        "not semantic",
        "not a heading",
        "lacks",
        "missing",
        "does not convey",
        "doesn't convey",
        "not exposed",
        "only visual",
        "visually",
        "instead of",
    )
    return target and fault


def _skip_reason(text: str) -> bool:
    return (
        "bypass" in text
        or (_has(text, "skip", "jump") and _has(text, "navigation", "menu", "main content"))
        or (_has(text, "tab through", "tab past") and _has(text, "40", "navigation", "menu"))
    ) and _has(
        text,
        "no ",
        "not ",
        "without",
        "missing",
        "must",
        "cannot",
        "can't",
        "every",
        "all 40",
    )


def _screen_reader_reason(text: str) -> bool:
    return (
        "aria-hidden" in text
        or "accessibility tree" in text
        or _has(text, "screen reader", "assistive technology")
    ) and _has(
        text,
        "hidden",
        "removed",
        "not available",
        "unavailable",
        "cannot access",
        "can't access",
        "not exposed",
        "excluded",
        "ignored",
    )


REASON_RULES: dict[str, Callable[[str], bool]] = {
    "alt text": _alt_reason,
    "closed captions": _captions_reason,
    "color contrast": _contrast_reason,
    "focus indicator": _focus_reason,
    "keyboard navigation": _keyboard_reason,
    "semantic HTML": _semantic_reason,
    "skip link": _skip_reason,
    "screen reader": _screen_reader_reason,
}


def _stance(text: str) -> str:
    """Return positive, negative, or unknown accessibility classification."""
    if _has(text, "not inaccessible", "no accessibility issue", "no accessibility problem"):
        return "positive"
    if _has(
        text,
        "inaccessible",
        "not accessible",
        "non-accessible",
        "nonaccessible",
        "non-compliant",
        "noncompliant",
        "fails",
        "failure",
        "violation",
    ):
        return "negative"
    if _has(text, "accessible", "conformant", "compliant", "passes"):
        return "positive"
    return "unknown"


def _is_degenerate(text: str) -> bool:
    words = text.split()
    for width in (1, 2, 3, 4):
        for start in range(len(words) - 3 * width + 1):
            phrase = words[start : start + width]
            if (
                words[start + width : start + 2 * width] == phrase
                and words[start + 2 * width : start + 3 * width] == phrase
            ):
                return True
    return False


def code_paired_response(item: Mapping, output: object) -> str:
    """Code one response using its frozen battery item metadata."""
    text = " ".join(str(output).lower().split())
    if not text or _is_degenerate(text):
        return "incorrect"

    polarity = item["polarity"]
    stance = _stance(text)

    if polarity == "conformant":
        if stance == "negative":
            return "incorrect"
        reason = REASON_RULES[item["concept"]](text)
        contradiction = reason and _has(text, "but", "however", "although", "yet")
        if stance == "positive" and contradiction:
            return "incorrect"
        if stance == "positive":
            return "correct"
        return "partial"

    if polarity != "violation":
        raise ValueError(f"unknown polarity {polarity!r}")

    if stance == "positive":
        return "incorrect"
    reason = REASON_RULES[item["concept"]](text)
    if stance == "negative" and reason:
        return "correct"
    if stance == "negative" or reason:
        return "partial"
    return "incorrect"


def code_result_frame(
    results: pd.DataFrame,
    battery: Mapping,
    require_all_models: bool = False,
) -> pd.DataFrame:
    """Attach frozen item metadata and code a complete set of model results."""
    required = {"prompt_id", "output", "model"}
    missing = required - set(results.columns)
    if missing:
        raise ValueError(f"paired results missing columns {sorted(missing)}")

    prompts = pd.DataFrame(battery["prompts"])
    expected_ids = set(prompts["prompt_id"])
    frames = []

    if require_all_models:
        found_models = {_model_key(value) for value in results["model"]}
        expected_models = set(MODEL_META)
        if found_models != expected_models:
            raise ValueError(
                "paired analysis requires all 13 frozen models; "
                f"missing={sorted(expected_models - found_models)}, "
                f"extra={sorted(found_models - expected_models)}"
            )

    for model, group in results.groupby("model", sort=False):
        ids = set(group["prompt_id"])
        if ids != expected_ids or len(group) != len(prompts):
            raise ValueError(
                f"{model}: incomplete paired result set; "
                f"missing={sorted(expected_ids - ids)}, extra={sorted(ids - expected_ids)}, "
                f"rows={len(group)}"
            )
        if group["prompt_id"].duplicated().any():
            raise ValueError(f"{model}: duplicate prompt_id rows")
        frames.append(group)

    complete = pd.concat(frames, ignore_index=True)
    metadata_columns = [
        "prompt_id",
        "pair_id",
        "concept",
        "polarity",
        "paired_with",
        "expected",
    ]
    result_metadata = {"concept", "polarity", "pair_id", "paired_with", "expected"}
    complete = complete.drop(columns=[c for c in result_metadata if c in complete.columns])
    coded = complete.merge(
        prompts[metadata_columns], on="prompt_id", how="left", validate="many_to_one"
    )
    item_lookup = {item["prompt_id"]: item for item in battery["prompts"]}
    coded["accuracy"] = coded.apply(
        lambda row: code_paired_response(item_lookup[row["prompt_id"]], row["output"]),
        axis=1,
    )
    coded["strict_score"] = coded["accuracy"].map(
        {"correct": 1, "partial": 0, "incorrect": 0}
    )
    coded["weighted_score"] = coded["accuracy"].map(
        {"correct": 1.0, "partial": 0.5, "incorrect": 0.0}
    )
    return _fill_model_metadata(coded)


def _model_key(value: object) -> str:
    return str(value).rstrip("/").split("/")[-1]


def _fill_model_metadata(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["model_key"] = result["model"].map(_model_key)
    unknown = sorted(set(result["model_key"]) - set(MODEL_META))
    if unknown:
        raise ValueError(f"unknown paired model names: {unknown}")

    expected_suite = result["model_key"].map(lambda key: MODEL_META[key][0])
    expected_scale = result["model_key"].map(lambda key: MODEL_META[key][1])
    if "suite" in result and not (result["suite"].astype(str) == expected_suite).all():
        raise ValueError("saved suite disagrees with frozen model metadata")
    if "scale" in result and not (result["scale"].astype(str) == expected_scale).all():
        raise ValueError("saved scale disagrees with frozen model metadata")
    result["suite"] = expected_suite
    result["scale"] = expected_scale
    result["is_pilot"] = result["model_key"].isin(PILOT_MODELS)
    result["confirmatory"] = ~result["is_pilot"]
    return result


def aggregate_pairs(coded: pd.DataFrame) -> pd.DataFrame:
    """Reduce two item rows to one strict evaluative result per model × concept."""
    rows = []
    keys = ["model", "model_key", "suite", "scale", "is_pilot", "confirmatory", "concept", "pair_id"]
    for key, group in coded.groupby(keys, sort=False, dropna=False):
        polarity_counts = Counter(group["polarity"])
        if len(group) != 2 or polarity_counts != {"violation": 1, "conformant": 1}:
            raise ValueError(f"{key}: expected exactly one row per polarity")
        by_polarity = group.set_index("polarity")
        violation = by_polarity.loc["violation"]
        conformant = by_polarity.loc["conformant"]
        row = dict(zip(keys, key))
        row.update({
            "violation_accuracy": violation["accuracy"],
            "conformant_accuracy": conformant["accuracy"],
            "violation_correct": bool(violation["accuracy"] == "correct"),
            "conformant_correct": bool(conformant["accuracy"] == "correct"),
            "evaluative_pass": bool(
                violation["accuracy"] == "correct"
                and conformant["accuracy"] == "correct"
            ),
            "strict_item_mean": float(group["strict_score"].mean()),
            "weighted_item_mean": float(group["weighted_score"].mean()),
        })
        rows.append(row)
    return pd.DataFrame(rows)


def load_declarative_long(project_root: str | Path) -> pd.DataFrame:
    """Load the existing original-concept declarative tables in long form."""
    project_root = Path(project_root)
    frames = []
    for suite in ("pythia", "gpt2", "olmo"):
        path = project_root / "results" / "analysis" / f"{suite}_declarative.csv"
        table = pd.read_csv(path)
        long = table.melt(id_vars="concept", var_name="scale", value_name="declarative_accuracy")
        long["suite"] = suite
        long["concept_key"] = long["concept"].map(_concept_key)
        frames.append(long[["suite", "scale", "concept_key", "declarative_accuracy"]])
    result = pd.concat(frames, ignore_index=True)
    if result.duplicated(["suite", "scale", "concept_key"]).any():
        raise ValueError("declarative table contains duplicate suite × scale × concept cells")
    return result


def _concept_key(value: object) -> str:
    return str(value).strip().lower().replace(" ", "_")


def build_gap_cells(pairs: pd.DataFrame, declarative: pd.DataFrame) -> pd.DataFrame:
    """Join strict evaluative pairs to the same concepts' declarative outcomes."""
    result = pairs.copy()
    result["concept_key"] = result["concept"].map(_concept_key)
    result = result.merge(
        declarative,
        on=["suite", "scale", "concept_key"],
        how="left",
        validate="many_to_one",
    )
    if result["declarative_accuracy"].isna().any():
        missing = result.loc[
            result["declarative_accuracy"].isna(), ["suite", "scale", "concept"]
        ].drop_duplicates()
        raise ValueError(f"paired cells missing declarative outcomes:\n{missing}")

    result["declarative_pass"] = result["declarative_accuracy"].eq("correct")
    result["gap_cell"] = result["declarative_pass"] & ~result["evaluative_pass"]
    result["cell_state"] = result.apply(_cell_state, axis=1)
    return result


def _cell_state(row: pd.Series) -> str:
    if row["declarative_pass"] and row["evaluative_pass"]:
        return "declarative_and_evaluative_pass"
    if row["declarative_pass"]:
        return "declarative_pass_evaluative_fail"
    if row["evaluative_pass"]:
        return "declarative_fail_evaluative_pass"
    return "declarative_and_evaluative_fail"


def summarize_gap(cells: pd.DataFrame) -> pd.DataFrame:
    """Produce per-model summaries with explicit primary denominators."""
    rows = []
    keys = ["model", "model_key", "suite", "scale", "is_pilot", "confirmatory"]
    for key, group in cells.groupby(keys, sort=False, dropna=False):
        declarative_passes = int(group["declarative_pass"].sum())
        gap_cells = int(group["gap_cell"].sum())
        evaluative_passes = int(group["evaluative_pass"].sum())
        states = Counter(group["cell_state"])
        row = dict(zip(keys, key))
        row.update({
            "n_concepts": int(len(group)),
            "declarative_passes": declarative_passes,
            "evaluative_pair_passes": evaluative_passes,
            "gap_cells": gap_cells,
            "gap_given_declarative_numerator": gap_cells,
            "gap_given_declarative_denominator": declarative_passes,
            "gap_given_declarative_pct": (
                round(gap_cells / declarative_passes * 100, 1)
                if declarative_passes
                else pd.NA
            ),
            "declarative_pass_pct": round(declarative_passes / len(group) * 100, 1),
            "evaluative_pass_pct": round(evaluative_passes / len(group) * 100, 1),
            "paired_gap_pct_pts": round(
                (declarative_passes - evaluative_passes) / len(group) * 100, 1
            ),
            "declarative_and_evaluative_pass": states["declarative_and_evaluative_pass"],
            "declarative_pass_evaluative_fail": states["declarative_pass_evaluative_fail"],
            "declarative_fail_evaluative_pass": states["declarative_fail_evaluative_pass"],
            "declarative_and_evaluative_fail": states["declarative_and_evaluative_fail"],
        })
        rows.append(row)
    return pd.DataFrame(rows)


def load_saved_results(project_root: str | Path) -> pd.DataFrame:
    """Load only dedicated paired-battery CSVs."""
    root = Path(project_root) / "results" / "evaluative_paired"
    paths = sorted(root.glob("*/*/*-evaluative-paired.csv"))
    if not paths:
        raise FileNotFoundError(f"no paired result CSVs found under {root}")
    return pd.concat((pd.read_csv(path) for path in paths), ignore_index=True)


def run_paired_analysis(
    project_root: str | Path,
    battery_path: str | Path | None = None,
) -> dict[str, pd.DataFrame]:
    """Code saved outputs and write the three preregistered analysis tables."""
    project_root = Path(project_root)
    if battery_path is None:
        battery_path = project_root / "data" / "evaluative_paired.yaml"
    battery = load_battery(battery_path)
    validate_battery(battery, project_root / "data" / "accessibility.yaml")

    item_coded = code_result_frame(
        load_saved_results(project_root), battery, require_all_models=True
    )
    pairs = aggregate_pairs(item_coded)
    cells = build_gap_cells(pairs, load_declarative_long(project_root))
    summary = summarize_gap(cells)

    output_dir = project_root / "results" / "analysis"
    output_dir.mkdir(parents=True, exist_ok=True)
    item_coded.to_csv(output_dir / "paired_item_coded.csv", index=False)
    cells.to_csv(output_dir / "paired_gap_cells.csv", index=False)
    summary.to_csv(output_dir / "paired_gap_summary.csv", index=False)
    return {"item_coded": item_coded, "cells": cells, "summary": summary}
