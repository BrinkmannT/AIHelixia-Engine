"""
AIHelixia Intelligence Engine
Model Provider
Version: 0.1.1
"""

from __future__ import annotations

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class ModelProvider:
    """
    Zentrale Schnittstelle zwischen der AIHelixia Engine
    und dem verwendeten Sprachmodell.
    """

    def __init__(
        self,
        model_name: str = "Qwen/Qwen2.5-0.5B-Instruct",
    ) -> None:

        self.model_name = model_name

        self.device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.tokenizer = None
        self.model = None

        self.status = "created"

    def load(self) -> dict[str, str]:
        """Lädt Tokenizer und Modell."""

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16
            if self.device == "cuda"
            else torch.float32,
            device_map=self.device,
        )

        self.status = "loaded"

        return self.get_status()

    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 64,
    ) -> str:
        """Erzeugt eine Antwort des Modells."""

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
        """Gibt den Status des Model Providers zurück."""

        return {
            "model": self.model_name,
            "device": self.device,
            "status": self.status,
        }

