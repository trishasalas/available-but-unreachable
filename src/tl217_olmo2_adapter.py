"""OLMo 2 adapter for TransformerLens 2.17.0.

This module keeps the installed TransformerLens 2.17.0 implementation intact for
all previously supported architectures and adds a conditional OLMo 2 path.

Target dependency versions:
    transformer_lens == 2.17.0
    transformers == 4.57.6

The adapter supports the base OLMo 2 models whose number of KV heads equals the
number of query heads, including allenai/OLMo-2-0425-1B and
allenai/OLMo-2-1124-7B.
"""

from __future__ import annotations

import gc
import math
from importlib.metadata import version
from typing import Optional, Union

import einops
import torch
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer

from transformer_lens import HookedTransformer
from transformer_lens.HookedTransformerConfig import HookedTransformerConfig
from transformer_lens.components.abstract_attention import AbstractAttention
from transformer_lens.components.rms_norm import RMSNorm
from transformer_lens.components.transformer_block import TransformerBlock
from transformer_lens.utils import repeat_along_head_dimension


_EXPECTED_TL_VERSION = "2.18.0"
_EXPECTED_TRANSFORMERS_VERSION = "4.57.6"
_OLMO2_ARCH = "Olmo2ForCausalLM"


def _check_versions() -> None:
    tl_version = version("transformer_lens")
    hf_version = version("transformers")
    if tl_version != _EXPECTED_TL_VERSION:
        raise RuntimeError(
            f"This adapter targets transformer_lens=={_EXPECTED_TL_VERSION}; "
            f"found {tl_version}. Restart the runtime after installing the pinned version."
        )
    if hf_version != _EXPECTED_TRANSFORMERS_VERSION:
        raise RuntimeError(
            f"This adapter targets transformers=={_EXPECTED_TRANSFORMERS_VERSION}; "
            f"found {hf_version}. Restart the runtime after installing the pinned version."
        )


def patch_tl217_for_olmo2() -> None:
    """Install architecture-conditional OLMo 2 forward paths.

    Existing TL2.17 architectures delegate to their original methods unchanged.
    Calling this function more than once is safe.
    """

    _check_versions()

    if not hasattr(AbstractAttention, "_olmo2_original_calculate_qkv_matrices"):
        AbstractAttention._olmo2_original_calculate_qkv_matrices = (  # type: ignore[attr-defined]
            AbstractAttention.calculate_qkv_matrices
        )

        def calculate_qkv_matrices_olmo2(self, query_input, key_input, value_input):
            original = AbstractAttention._olmo2_original_calculate_qkv_matrices  # type: ignore[attr-defined]
            q, k, v = original(self, query_input, key_input, value_input)

            if self.cfg.original_architecture != _OLMO2_ARCH:
                return q, k, v

            if self.q_norm is None or self.k_norm is None:
                raise RuntimeError("OLMo 2 full-projection Q/K norms were not installed.")

            q_heads = q.shape[2]
            k_heads = k.shape[2]

            q = einops.rearrange(
                self.q_norm(
                    einops.rearrange(
                        q,
                        "batch pos head d_head -> batch pos (head d_head)",
                    )
                ),
                "batch pos (head d_head) -> batch pos head d_head",
                head=q_heads,
            )
            k = einops.rearrange(
                self.k_norm(
                    einops.rearrange(
                        k,
                        "batch pos head d_head -> batch pos (head d_head)",
                    )
                ),
                "batch pos (head d_head) -> batch pos head d_head",
                head=k_heads,
            )
            return q, k, v

        AbstractAttention.calculate_qkv_matrices = calculate_qkv_matrices_olmo2

    if not hasattr(TransformerBlock, "_olmo2_original_forward"):
        TransformerBlock._olmo2_original_forward = TransformerBlock.forward  # type: ignore[attr-defined]

        def forward_olmo2(
            self,
            resid_pre,
            shortformer_pos_embed=None,
            past_kv_cache_entry=None,
            attention_mask=None,
        ):
            original = TransformerBlock._olmo2_original_forward  # type: ignore[attr-defined]
            if self.cfg.original_architecture != _OLMO2_ARCH:
                return original(
                    self,
                    resid_pre,
                    shortformer_pos_embed=shortformer_pos_embed,
                    past_kv_cache_entry=past_kv_cache_entry,
                    attention_mask=attention_mask,
                )

            if shortformer_pos_embed is not None:
                raise RuntimeError("OLMo 2 does not use Shortformer positional embeddings.")
            if self.cfg.attn_only or self.cfg.parallel_attn_mlp:
                raise RuntimeError("Unexpected OLMo 2 block configuration.")

            resid_pre = self.hook_resid_pre(resid_pre)

            if self.cfg.use_attn_in or self.cfg.use_split_qkv_input:
                attn_in = resid_pre
            else:
                attn_in = resid_pre

            if self.cfg.use_attn_in:
                attn_in = self.hook_attn_in(
                    repeat_along_head_dimension(resid_pre, n_heads=self.cfg.n_heads)
                )

            if self.cfg.use_split_qkv_input:
                n_kv_heads = (
                    self.cfg.n_key_value_heads
                    if self.cfg.n_key_value_heads is not None
                    and not self.cfg.ungroup_grouped_query_attention
                    else self.cfg.n_heads
                )
                query_input = self.hook_q_input(
                    repeat_along_head_dimension(resid_pre, n_heads=self.cfg.n_heads)
                )
                key_input = self.hook_k_input(
                    repeat_along_head_dimension(resid_pre, n_heads=n_kv_heads)
                )
                value_input = self.hook_v_input(
                    repeat_along_head_dimension(resid_pre, n_heads=n_kv_heads)
                )
            else:
                query_input = attn_in
                key_input = attn_in
                value_input = attn_in

            # OLMo 2 attention reads the raw residual stream. Its RMSNorm is
            # applied to the attention branch output before residual addition.
            attn_out = self.attn(
                query_input=query_input,
                key_input=key_input,
                value_input=value_input,
                past_kv_cache_entry=past_kv_cache_entry,
                attention_mask=attention_mask,
            )
            attn_out = self.hook_attn_out(attn_out)
            attn_out = self.ln1(attn_out)

            if resid_pre.device != attn_out.device:
                resid_pre = resid_pre.to(attn_out.device)

            resid_mid = self.hook_resid_mid(resid_pre + attn_out)
            mlp_in = (
                resid_mid
                if not self.cfg.use_hook_mlp_in
                else self.hook_mlp_in(resid_mid.clone())
            )

            # OLMo 2 MLP also reads the raw residual stream and normalizes the
            # branch output before residual addition.
            mlp_out = self.apply_mlp(mlp_in)
            mlp_out = self.ln2(mlp_out)
            return self.hook_resid_post(resid_mid + mlp_out)

        TransformerBlock.forward = forward_olmo2


def _make_tl_config(hf_config, model_name: str, device: str, dtype: torch.dtype):
    architecture = hf_config.architectures[0] if hf_config.architectures else None
    if architecture != _OLMO2_ARCH:
        raise ValueError(
            f"Expected architecture {_OLMO2_ARCH}, found {architecture!r} for {model_name}."
        )
    if hf_config.num_key_value_heads != hf_config.num_attention_heads:
        raise NotImplementedError(
            "This TL2.17 adapter currently supports OLMo 2 checkpoints with "
            "num_key_value_heads == num_attention_heads."
        )

    d_head = hf_config.hidden_size // hf_config.num_attention_heads
    return HookedTransformerConfig(
        n_layers=hf_config.num_hidden_layers,
        d_model=hf_config.hidden_size,
        n_ctx=hf_config.max_position_embeddings,
        d_head=d_head,
        n_heads=hf_config.num_attention_heads,
        d_mlp=hf_config.intermediate_size,
        d_vocab=hf_config.vocab_size,
        d_vocab_out=hf_config.vocab_size,
        act_fn=hf_config.hidden_act,
        eps=hf_config.rms_norm_eps,
        initializer_range=hf_config.initializer_range,
        normalization_type="RMS",
        positional_embedding_type="rotary",
        rotary_dim=d_head,
        rotary_base=hf_config.rope_theta,
        rotary_adjacent_pairs=False,
        use_attn_scale=True,
        attn_scale=math.sqrt(d_head),
        gated_mlp=True,
        original_architecture=_OLMO2_ARCH,
        model_name=model_name,
        tokenizer_name=model_name,
        default_prepend_bos=True,
        tie_word_embeddings=hf_config.tie_word_embeddings,
        n_key_value_heads=None,
        use_qk_norm=False,
        init_weights=False,
        dtype=dtype,
        device=device,
    )


def _convert_olmo2_weights(hf_model, model: HookedTransformer) -> dict[str, torch.Tensor]:
    cfg = model.cfg
    state_dict: dict[str, torch.Tensor] = {
        "embed.W_E": hf_model.model.embed_tokens.weight.detach(),
    }

    for layer_index, layer in enumerate(hf_model.model.layers):
        q_weight = layer.self_attn.q_proj.weight.detach()
        k_weight = layer.self_attn.k_proj.weight.detach()
        v_weight = layer.self_attn.v_proj.weight.detach()
        o_weight = layer.self_attn.o_proj.weight.detach()

        state_dict[f"blocks.{layer_index}.attn.W_Q"] = einops.rearrange(
            q_weight, "(head d_head) d_model -> head d_model d_head", head=cfg.n_heads
        )
        state_dict[f"blocks.{layer_index}.attn.W_K"] = einops.rearrange(
            k_weight, "(head d_head) d_model -> head d_model d_head", head=cfg.n_heads
        )
        state_dict[f"blocks.{layer_index}.attn.W_V"] = einops.rearrange(
            v_weight, "(head d_head) d_model -> head d_model d_head", head=cfg.n_heads
        )
        state_dict[f"blocks.{layer_index}.attn.W_O"] = einops.rearrange(
            o_weight, "d_model (head d_head) -> head d_head d_model", head=cfg.n_heads
        )

        state_dict[f"blocks.{layer_index}.attn.b_Q"] = torch.zeros(
            cfg.n_heads, cfg.d_head, dtype=cfg.dtype
        )
        state_dict[f"blocks.{layer_index}.attn.b_K"] = torch.zeros(
            cfg.n_heads, cfg.d_head, dtype=cfg.dtype
        )
        state_dict[f"blocks.{layer_index}.attn.b_V"] = torch.zeros(
            cfg.n_heads, cfg.d_head, dtype=cfg.dtype
        )
        state_dict[f"blocks.{layer_index}.attn.b_O"] = torch.zeros(
            cfg.d_model, dtype=cfg.dtype
        )

        state_dict[f"blocks.{layer_index}.attn.q_norm.w"] = (
            layer.self_attn.q_norm.weight.detach()
        )
        state_dict[f"blocks.{layer_index}.attn.k_norm.w"] = (
            layer.self_attn.k_norm.weight.detach()
        )
        state_dict[f"blocks.{layer_index}.ln1.w"] = (
            layer.post_attention_layernorm.weight.detach()
        )
        state_dict[f"blocks.{layer_index}.ln2.w"] = (
            layer.post_feedforward_layernorm.weight.detach()
        )

        state_dict[f"blocks.{layer_index}.mlp.W_gate"] = (
            layer.mlp.gate_proj.weight.detach().T
        )
        state_dict[f"blocks.{layer_index}.mlp.W_in"] = (
            layer.mlp.up_proj.weight.detach().T
        )
        state_dict[f"blocks.{layer_index}.mlp.W_out"] = (
            layer.mlp.down_proj.weight.detach().T
        )
        state_dict[f"blocks.{layer_index}.mlp.b_in"] = torch.zeros(
            cfg.d_mlp, dtype=cfg.dtype
        )
        state_dict[f"blocks.{layer_index}.mlp.b_out"] = torch.zeros(
            cfg.d_model, dtype=cfg.dtype
        )

    state_dict["ln_final.w"] = hf_model.model.norm.weight.detach()
    state_dict["unembed.W_U"] = hf_model.lm_head.weight.detach().T
    state_dict["unembed.b_U"] = torch.zeros(cfg.d_vocab_out, dtype=cfg.dtype)
    return state_dict


def load_olmo2_tl217(
    model_name: str = "allenai/OLMo-2-0425-1B",
    *,
    device: Optional[Union[str, torch.device]] = None,
    dtype: torch.dtype = torch.float32,
    revision: Optional[str] = None,
    center_unembed: bool = True,
    validate_prompt: Optional[str] = "An image without alt text is not accessible because",
) -> HookedTransformer:
    """Load OLMo 2 into the TL2.17 HookedTransformer implementation.

    This intentionally does not fold RMSNorm or center residual-writing weights.
    Those TL2 transformations are not valid for OLMo 2's post-norm branches.
    Centering the unembedding is retained by default because it preserves the
    softmax distribution and argmax while matching TL2's normal coordinate
    convention.
    """

    patch_tl217_for_olmo2()

    target_device = str(
        device if device is not None else ("cuda" if torch.cuda.is_available() else "cpu")
    )

    hf_config = AutoConfig.from_pretrained(model_name, revision=revision)
    cfg = _make_tl_config(hf_config, model_name, target_device, dtype)
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        revision=revision,
        add_bos_token=True,
        use_fast=True,
    )

    hf_device = target_device if target_device.startswith("cuda") else "cpu"
    hf_model = AutoModelForCausalLM.from_pretrained(
        model_name,
        revision=revision,
        torch_dtype=dtype,
        attn_implementation="eager",
        low_cpu_mem_usage=True,
    ).to(hf_device)
    hf_model.eval()

    model = HookedTransformer(
        cfg,
        tokenizer=tokenizer,
        move_to_device=False,
        default_padding_side="right",
    )

    # OLMo 2 normalizes the full concatenated Q/K projection, not each head
    # independently. TL2.17's built-in use_qk_norm normalizes per head, so these
    # full-width modules are installed explicitly.
    for block in model.blocks:
        block.attn.q_norm = RMSNorm(cfg, length=cfg.d_model)
        block.attn.k_norm = RMSNorm(cfg, length=cfg.d_model)
    model.setup()

    converted = _convert_olmo2_weights(hf_model, model)
    expected_parameters = set(dict(model.named_parameters()))
    converted_parameters = set(converted)
    missing = sorted(expected_parameters - converted_parameters)
    unexpected = sorted(converted_parameters - expected_parameters)
    if missing or unexpected:
        raise RuntimeError(
            "Converted state dict does not match the TL model. "
            f"Missing parameters: {missing}; unexpected parameters: {unexpected}"
        )

    model.load_state_dict(converted, strict=False)
    del converted

    if center_unembed:
        with torch.no_grad():
            model.unembed.W_U.sub_(model.unembed.W_U.mean(dim=-1, keepdim=True))

    reference_logits = None
    validation_tokens = None
    if validate_prompt is not None:
        validation_tokens = model.to_tokens(validate_prompt)
        with torch.no_grad():
            reference_logits = hf_model(
                validation_tokens.to(hf_device),
                use_cache=False,
            ).logits.float().cpu().detach().clone()
        if center_unembed:
            reference_logits.sub_(reference_logits.mean(dim=-1, keepdim=True))

    del hf_model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    model.move_model_modules_to_device()
    model.eval()

    if reference_logits is not None and validation_tokens is not None:
        with torch.no_grad():
            tl_logits = model(
                validation_tokens.to(target_device),
                return_type="logits",
            ).float().cpu().detach().clone()

        difference = tl_logits - reference_logits
        top1_match = torch.equal(tl_logits.argmax(-1), reference_logits.argmax(-1))
        print("OLMo 2 TL2.17 validation")
        print(f"  max |logit difference|:  {difference.abs().max().item():.6g}")
        print(f"  mean |logit difference|: {difference.abs().mean().item():.6g}")
        print(f"  top-1 match at every position: {top1_match}")
        if not top1_match:
            raise RuntimeError(
                "The TL2.17 adapter and native Hugging Face OLMo 2 disagree on top-1 tokens. "
                "Do not use this model for experiments until the mismatch is resolved."
            )

    print(f"Loaded pretrained model {model_name} into TransformerLens 2.17.0")
    return model
