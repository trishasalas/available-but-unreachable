"""Model loading and memory management for TransformerLens experiments.

Handles GPT-2 and Pythia model families with automatic device detection
and memory cleanup between model swaps on memory-constrained hardware.
"""
import warnings
# Suppress all warnings
warnings.filterwarnings('ignore')

# Or specifically for TransformerLens/HuggingFace warnings:
warnings.filterwarnings('ignore', category=UserWarning, module='transformer_lens')

import gc
from dataclasses import dataclass
from typing import Optional


import torch
from transformer_lens import HookedTransformer


@dataclass
class ModelInfo:
    """Metadata about a loaded model for comparison tables."""
    name: str
    family: str  # "gpt2" or "pythia"
    n_layers: int
    n_heads: int
    d_model: int
    d_mlp: int
    architecture: str  # "sequential" or "parallel"


# Architecture reference for cross-model comparison
GPT2_MODELS = {
    "gpt2":        {"layers": 12, "d_model": 768,  "d_mlp": 3072, "heads": 12},
    "gpt2-medium": {"layers": 24, "d_model": 1024, "d_mlp": 4096, "heads": 16},
    "gpt2-large":  {"layers": 36, "d_model": 1280, "d_mlp": 5120, "heads": 20},
    "gpt2-xl":     {"layers": 48, "d_model": 1600, "d_mlp": 6400, "heads": 25},
}

PYTHIA_MODELS = {
    "pythia-410m":         {"layers": 24, "d_model": 1024, "d_mlp": 4096, "heads": 16},
    "pythia-1b":           {"layers": 16, "d_model": 2048, "d_mlp": 8192, "heads": 8},
    "pythia-1.4b":         {"layers": 24, "d_model": 2048, "d_mlp": 8192, "heads": 16},
    "pythia-2.8b":         {"layers": 32, "d_model": 2560, "d_mlp": 10240, "heads": 32},
    "pythia-410m-deduped":  {"layers": 24, "d_model": 1024, "d_mlp": 4096, "heads": 16},
    "pythia-1b-deduped":    {"layers": 16, "d_model": 2048, "d_mlp": 8192, "heads": 8},
    "pythia-1.4b-deduped":  {"layers": 24, "d_model": 2048, "d_mlp": 8192, "heads": 16},
    "pythia-2.8b-deduped":  {"layers": 32, "d_model": 2560, "d_mlp": 10240, "heads": 32},
}


def _detect_device() -> str:
    """Pick the best available device."""
    if torch.cuda.is_available():
        return "cuda"
    if torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def _clear_memory(device: str) -> None:
    """Free GPU/MPS memory. Call between model loads."""
    gc.collect()
    if device == "cuda":
        torch.cuda.empty_cache()
    elif device == "mps":
        torch.mps.empty_cache()


def _model_family(name: str) -> str:
    """Determine model family from name."""
    if name.startswith("gpt2"):
        return "gpt2"
    if name.startswith("pythia"):
        return "pythia"
    raise ValueError(f"Unknown model family for '{name}'")


def _architecture_type(name: str) -> str:
    """GPT-2 is sequential attn+MLP, Pythia is parallel."""
    family = _model_family(name)
    return "sequential" if family == "gpt2" else "parallel"


def load_model(name: str, device: Optional[str] = None) -> tuple[HookedTransformer, ModelInfo]:
    """Load a model and return it with metadata.

    Args:
        name: Model name as TransformerLens expects it.
              GPT-2:  "gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl"
              Pythia: "pythia-410m", "pythia-1b-deduped", etc.
        device: Force a specific device. Auto-detects if None.

    Returns:
        (model, info) tuple.
    """
    if device is None:
        device = _detect_device()

    model = HookedTransformer.from_pretrained(name, device=device)

    info = ModelInfo(
        name=name,
        family=_model_family(name),
        n_layers=model.cfg.n_layers,
        n_heads=model.cfg.n_heads,
        d_model=model.cfg.d_model,
        d_mlp=model.cfg.d_mlp,
        architecture=_architecture_type(name),
    )

    print(f"Loaded {name} on {device}")
    print(f"  {info.n_layers} layers | {info.n_heads} heads | "
          f"d_model={info.d_model} | d_mlp={info.d_mlp} | "
          f"{info.architecture} attn+MLP")

    return model, info


def unload(model: HookedTransformer) -> None:
    """Delete a model and free memory.

    Usage:
        model, info = load_model("gpt2-medium")
        # ... do work ...
        unload(model)
    """
    device = str(model.cfg.device)
    del model
    _clear_memory(device)
    print("Model unloaded, memory cleared")
