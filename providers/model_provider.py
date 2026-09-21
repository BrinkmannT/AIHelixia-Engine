"""
AIHelixia Intelligence Engine
Model Provider
Version: 0.4.3
"""

from __future__ import annotations

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class ModelProvider:
    """
    Zentrale Schnittstelle zwischen der AIHelixia Engine
    und dem verwendeten Sprachmodell.

    Unterstützte Modi:
    - auto
    - cpu
    - cuda

    V0.4.3:
    - explizite Device-Konfiguration
    - Cloud-GPU-Unterstützung über CUDA
    - lokale CPU-Unterstützung
    - keine Änderung an der restlichen Engine notwendig
    """

    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-0.5B-Instruct",
        device: str = "auto",
    ) -> None:

        self.model_name = model_name

        if device not in {
            "auto",
            "cpu",
            "cuda",
        }:
            raise ValueError(
                "device muss 'auto', 'cpu' oder 'cuda' sein."
            )

        self.requested_device = device

        self.device = self._resolve_device(
            device
        )

        self.tokenizer = None
        self.model = None

        self.status = "created"

    @staticmethod
    def _resolve_device(
        device: str,
    ) -> str:
        """
        Bestimmt das tatsächlich verwendete Gerät.
        """

        if device == "cpu":
            return "cpu"

        if device == "cuda":
            if not torch.cuda.is_available():
                raise RuntimeError(
                    "CUDA wurde angefordert, ist aber "
                    "auf diesem System nicht verfügbar."
                )

            return "cuda"

        if torch.cuda.is_available():
            return "cuda"

        return "cpu"

    def load(self) -> dict[str, str]:
        """
        Lädt Tokenizer und Modell.
        """

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name
        )

        if self.device == "cuda":
            self.model = (
                AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float16,
                ).to("cuda")
            )

        else:
            self.model = (
                AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float32,
                ).to("cpu")
            )

        self.model.eval()

        self.status = "loaded"

        return self.get_status()

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 64,
    ) -> str:
        """
        Erzeugt eine Antwort des Modells.
        """

        if self.model is None or self.tokenizer is None:
            raise RuntimeError(
                "ModelProvider ist nicht geladen. "
                "Bitte zuerst load() aufrufen."
            )

        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
            )

        new_tokens = outputs[0][
            inputs["input_ids"].shape[1]:
        ]

        response = self.tokenizer.decode(
            new_tokens,
            skip_special_tokens=True,
        )

        return response.strip()

    def get_status(self) -> dict[str, str]:
        """
        Gibt den aktuellen Status des Model Providers zurück.
        """

        return {
            "model": self.model_name,
            "requested_device": self.requested_device,
            "device": self.device,
            "status": self.status,
        }