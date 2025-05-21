import pandas as pd


def read_excel(path):
    df = pd.read_excel(path)
    headers = list(df.columns)
    rows = df.values.tolist()
    return {"headers": headers, "rows": rows}


def batch_data_with_headers(data, batch_size):
    if not data or "headers" not in data or "rows" not in data:
        return

    headers = data["headers"]
    rows = data["rows"]

    for i in range(0, len(rows), batch_size):
        batch_rows = rows[i : i + batch_size]
        yield headers, batch_rows
