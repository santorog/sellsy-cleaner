import json
import os
from string import Template

import requests

import config
from config import AppConfig


class LLMDataCleaner:
    def __init__(self, prompt_path="prompts/cleaning_prompt.txt"):
        self.prompt_path = prompt_path
        self.model = AppConfig.OPENROUTER_MODEL
        self.temperature = AppConfig.TEMPERATURE
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    def _load_prompt_template(self):
        try:
            with open(self.prompt_path, "r", encoding="utf-8") as file:
                return Template(file.read())
        except FileNotFoundError:
            raise RuntimeError(f"Prompt file not found at {self.prompt_path}")

    def _prepare_prompt(self, headers, rows):
        template = self._load_prompt_template()
        data_json = json.dumps(
            {"headers": headers, "rows": rows}, ensure_ascii=False, indent=2
        )
        return template.substitute(batch=f"```json\n{data_json}\n```")

    def _send_request(self, prompt):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        response = requests.post(self.api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def clean(self, data):
        headers, rows = data
        prompt = self._prepare_prompt(headers, rows)

        try:
            raw_output = self._send_request(prompt)
        except Exception as e:
            print(f"[ERROR] API call failed: {e}")
            return []

        try:
            return json.loads(raw_output)
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON parsing failed: {e}")
            print("[DEBUG] Raw output received:")
            print(raw_output)
            return []
