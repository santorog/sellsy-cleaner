# Sellsy Cleaner

🤖 **AI-Powered Cleaning**: Uses OpenRouter and a LLM to clean or enrich data based on prompts.

**Sellsy Cleaner** is a Python tool designed to clean and process data—likely from Excel files—using AI models such as OpenAI through OpenRouter. 
It is tailored for integration with Sellsy CRM data, allowing enhanced data preparation and cleanup via intelligent prompts.

---

## Installation

```bash
git clone https://github.com/santorog/sellsy-cleaner.git
cd sellsy-cleaner
python -m venv venv
source venv/bin/activate 
pip install -r requirements.txt
```

---

## Usage

Update the `config.py` file and add a .env file with your API keys, IDs and Secrets.

To run the cleaner, from the project directory:

```bash
python main.py file.xlsx
```

---

## Requirements

- Python 3.8+
- Install required packages:

```bash
pip install -r requirements.txt
```

---

## License

MIT License.