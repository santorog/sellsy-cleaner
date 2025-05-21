import json
import os
from string import Template

from openai import OpenAI

from config import AppConfig


def clean_batch(batch):
    headers, rows = batch

    with open("prompts/cleaning_prompt.txt", "r", encoding="utf-8") as file:
        prompt_template = Template(file.read())

    data = {"headers": headers, "rows": rows}

    batch_json = json.dumps(data, ensure_ascii=False, indent=2)
    prompt = prompt_template.substitute(batch=f"```json\n{batch_json}\n```")

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model=AppConfig.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=AppConfig.OPENAI_TEMPERATURE,
    )
    raw_output = response.choices[0].message.content

    try:
        return json.loads(raw_output)
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON parsing failed: {e}")
        print("[DEBUG] Raw output received:")
        print(raw_output)
        return []
