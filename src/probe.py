"""Linear probing: does the model geometrically encode a concept, even when it
can't generate it?

A linear probe trains a logistic regression classifier on residual stream
activations at each layer, using contrastive prompt pairs (target concept vs
control). Probe accuracy above chance at a given layer means the concept
exists as a separable direction in the model's representation space at that
depth — independent of whether it can be decoded into output.

This answers a different question than the logit lens or decomposition tools:
  - Logit lens asks: "what token would the model predict if it stopped here?"
  - Decomposition asks: "which components are voting for the target token?"
  - Linear probe asks: "is this concept geometrically present in the residual
    stream, even if it can't be retrieved?"

## Why this matters for the accessibility emergence work

The Pythia behavioral paper found that screen reader / alt text / skip link
emerge at 2.8B parameters. But "emerge" there means behavioral — the model
starts generating correct completions. A probe can show whether the knowledge
exists geometrically in smaller models *before* the behavioral threshold,
which would mean the 2.8B threshold is a retrieval problem, not an encoding
problem.

Expected patterns:
  - If concept is not encoded: probe accuracy ≈ 50% (chance) across all layers
  - If encoded but inaccessible: accuracy rises in middle layers, falls again
    (geometry exists but isn't connected to the output path)
  - If encoded and accessible: accuracy rises and stays high into late layers

## Usage

    from transformer_lens import HookedTransformer
    from src.models import load_model
    from src.probe import linear_probe, print_probe_results

    model, info = load_model("gpt2-medium")

    target_prompts = [
        "A screen reader is software that reads",
        "Screen readers allow blind users to",
        "The screen reader announces the",
    ]
    control_prompts = [
        "A text editor is software that edits",
        "Word processors allow users to type",
        "The browser renders the",
    ]

    df = linear_probe(model, target_prompts, control_prompts)
    print_probe_results(df)

## Notes on prompt set size

Logistic regression needs enough samples to generalize. With small prompt sets
(the default for accessibility research), use cross_validate=True to get more
reliable accuracy estimates via k-fold cross-validation rather than a single
train/test split. With 6 prompts per class, 3-fold CV is the minimum that
makes sense.

Activations are extracted at the last token position by default. For prompts
that vary in length this may not be the most informative position — consider
padding prompts to equal length or testing specific token positions.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from transformer_lens import HookedTransformer


def _extract_activations(
    model: HookedTransformer,
    prompts: list[str],
    position: int = -1,
) -> np.ndarray:
    """Extract residual stream activations for a list of prompts.

    Args:
        model: A loaded HookedTransformer.
        prompts: List of prompt strings.
        position: Token position to extract from. Default -1 (last token).

    Returns:
        Array of shape (n_prompts, n_layers, d_model).
    """
    all_activations = []

    for prompt in prompts:
        _, cache = model.run_with_cache(
            prompt,
            names_filter=lambda name: name.startswith("resid_post"),
        )

        # Shape: (n_layers, d_model)
        layers = [
            cache["resid_post", layer][0, position].detach().cpu().numpy()
            for layer in range(model.cfg.n_layers)
        ]
        all_activations.append(layers)

    # Shape: (n_prompts, n_layers, d_model)
    return np.array(all_activations)


def linear_probe(
    model: HookedTransformer,
    target_prompts: list[str],
    control_prompts: list[str],
    position: int = -1,
    cross_validate: bool = True,
    cv_folds: int = 3,
    test_size: float = 0.2,
    random_state: int = 42,
) -> pd.DataFrame:
    """Train a linear probe at each layer to detect concept presence.

    Extracts residual stream activations for target and control prompts,
    then trains a logistic regression classifier at each layer. Probe
    accuracy above chance (0.5) indicates the concept is geometrically
    separable at that layer.

    Args:
        model: A loaded HookedTransformer.
        target_prompts: Prompts containing the concept of interest.
        control_prompts: Structurally similar prompts without the concept.
            Should match target_prompts in length and syntactic structure
            as closely as possible — you want to isolate the concept, not
            sentence structure.
        position: Token position to extract activations from.
            Default -1 (last token).
        cross_validate: If True, use k-fold cross-validation for accuracy
            estimates. Recommended for small prompt sets (< 20 per class).
            If False, uses a single train/test split.
        cv_folds: Number of folds for cross-validation. Default 3.
            With small datasets, 3 is the practical minimum.
        test_size: Fraction of data for test set when cross_validate=False.
            Default 0.2.
        random_state: Random seed for reproducibility. Default 42.

    Returns:
        DataFrame with columns:
            layer       — layer index (0-indexed)
            accuracy    — mean probe accuracy (0.0–1.0)
            std         — standard deviation across CV folds (or 0 if no CV)
            n_target    — number of target prompts
            n_control   — number of control prompts

        DataFrame.attrs contains model metadata and probe configuration.

    Notes:
        Activations are standardized (zero mean, unit variance) per layer
        before fitting. This is important — residual stream magnitudes vary
        significantly across layers and would otherwise bias the classifier.
    """
    n_target = len(target_prompts)
    n_control = len(control_prompts)

    # Extract activations: (n_prompts, n_layers, d_model)
    target_acts = _extract_activations(model, target_prompts, position)
    control_acts = _extract_activations(model, control_prompts, position)

    # Labels: 1 for target, 0 for control
    labels = np.array([1] * n_target + [0] * n_control)

    rows = []
    for layer in range(model.cfg.n_layers):
        # Shape: (n_prompts, d_model)
        X = np.concatenate([
            target_acts[:, layer, :],
            control_acts[:, layer, :],
        ], axis=0)

        # Standardize — residual stream scale varies across layers
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        clf = LogisticRegression(
            max_iter=1000,
            random_state=random_state,
            solver="lbfgs",
        )

        if cross_validate:
            scores = cross_val_score(clf, X_scaled, labels, cv=cv_folds)
            accuracy = scores.mean()
            std = scores.std()
        else:
            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, labels,
                test_size=test_size,
                random_state=random_state,
            )
            clf.fit(X_train, y_train)
            accuracy = clf.score(X_test, y_test)
            std = 0.0

        rows.append({
            "layer": layer,
            "accuracy": accuracy,
            "std": std,
            "n_target": n_target,
            "n_control": n_control,
        })

    df = pd.DataFrame(rows)
    df.attrs["model"] = model.cfg.model_name
    df.attrs["n_layers"] = model.cfg.n_layers
    df.attrs["position"] = position
    df.attrs["cross_validate"] = cross_validate
    df.attrs["cv_folds"] = cv_folds if cross_validate else None
    df.attrs["random_state"] = random_state

    return df


def print_probe_results(df: pd.DataFrame) -> None:
    """Pretty-print probe accuracy by layer."""
    attrs = df.attrs
    print(f"Model: {attrs.get('model', '?')}")
    print(f"Prompts: {df['n_target'].iloc[0]} target / "
          f"{df['n_control'].iloc[0]} control")
    cv = attrs.get("cross_validate", False)
    if cv:
        print(f"Method: {attrs.get('cv_folds', '?')}-fold cross-validation")
    else:
        print("Method: single train/test split")
    print()
    print(f"{'Layer':<8} {'Accuracy':<12} {'±Std':<10} {'Signal'}")
    print("-" * 45)
    for _, row in df.iterrows():
        bar = "█" * int(row["accuracy"] * 20)
        std_str = f"±{row['std']:.3f}" if row["std"] > 0 else "—"
        print(f"{row['layer']:<8} {row['accuracy']:<12.3f} "
              f"{std_str:<10} {bar}")


def summarize_probe(df: pd.DataFrame) -> dict:
    """Quick summary of probe results.

    Returns dict with:
        peak_layer      — layer with highest probe accuracy
        peak_accuracy   — accuracy at peak layer
        mean_accuracy   — mean accuracy across all layers
        above_chance    — number of layers with accuracy > 0.6
        encoding_pattern — rough characterization:
            "not_encoded"   — mean accuracy near chance throughout
            "early"         — peak in first third of layers
            "middle"        — peak in middle third
            "late"          — peak in final third
            "sustained"     — high accuracy maintained across many layers
    """
    peak_idx = df["accuracy"].idxmax()
    peak_layer = int(df.loc[peak_idx, "layer"])
    peak_accuracy = df.loc[peak_idx, "accuracy"]
    mean_accuracy = df["accuracy"].mean()
    above_chance = int((df["accuracy"] > 0.6).sum())
    n_layers = len(df)

    if mean_accuracy < 0.55:
        pattern = "not_encoded"
    elif above_chance > n_layers * 0.5:
        pattern = "sustained"
    elif peak_layer < n_layers // 3:
        pattern = "early"
    elif peak_layer < (n_layers * 2) // 3:
        pattern = "middle"
    else:
        pattern = "late"

    return {
        "peak_layer": peak_layer,
        "peak_accuracy": peak_accuracy,
        "mean_accuracy": mean_accuracy,
        "above_chance": above_chance,
        "encoding_pattern": pattern,
    }
