import sys

from clients.openrouter_client import LLMDataCleaner
from clients.sellsy_client import SellsyClient
from data.excel_reader import batch_data_with_headers, read_excel


def main(file_path):
    data = read_excel(file_path)
    clean_and_push(data)


def clean_and_push(data):
    sellsy_client = SellsyClient()
    batch_cleaner = LLMDataCleaner()

    for batch in batch_data_with_headers(data, batch_size=50):
        contacts = batch_cleaner.clean(batch)
        push_contacts_sellsy(sellsy_client, contacts)


def push_contacts_sellsy(api_client, contacts):
    for contact in contacts:
        try:
            api_client.push_contact(contact)
            print(f"Pushed : {contact['email']}")
        except Exception as e:
            print(f"Error on {contact}: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <fichier_excel.xlsx>")
        sys.exit(1)
    main(sys.argv[1])
