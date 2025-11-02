from typing import Dict, Any, List

from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel


class LoraExecutor:
    def __init__(self, base_model: str, lora_path: str, temperature: float = 0.3, max_tokens: int = 512):
        self.base_model_id = base_model
        self.lora_path = lora_path
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.tokenizer = AutoTokenizer.from_pretrained(base_model)
        base = AutoModelForCausalLM.from_pretrained(base_model)
        self.model = PeftModel.from_pretrained(base, lora_path)

    def generate(self, prompt: str, context_snippets: List[str] | None = None) -> str:
        context_text = "\n\n".join(context_snippets or [])
        full_prompt = f"{context_text}\n\n{prompt}" if context_text else prompt
        inputs = self.tokenizer(full_prompt, return_tensors='pt')
        output = self.model.generate(**inputs, max_new_tokens=self.max_tokens, do_sample=self.temperature > 0.0, temperature=self.temperature)
        return self.tokenizer.decode(output[0], skip_special_tokens=True)

