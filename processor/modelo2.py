import pdfplumber
import pandas as pd
import re

def procesar_pdf_modelo2(filepath):
    with pdfplumber.open(filepath) as pdf:
        raw_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    start_marker = "SKU DESC CANT. PRECIO TOTAL"
    end_marker = "Sub-Total:"
    start = raw_text.find(start_marker)
    end = raw_text.find(end_marker)
    data_block = raw_text[start:end]
    data_block = re.sub(r"SKU DESC CANT. PRECIO TOTAL.*?\n", "", data_block)
    lines = [line.strip() for line in data_block.splitlines() if line.strip()]

    rows = []
    i = 0
    while i < len(lines):
        if re.match(r"^\d+\s", lines[i]):
            add = 1
            sku_match = re.search(r'\b(\d{9})\b', lines[i])
            if sku_match:
                add = 3
                sku = sku_match.group(1)
                desc = lines[i + 1]
                prices = lines[i + 2].split()
                rows.append([
                    sku,
                    desc,
                    prices[0],
                    prices[1],
                    prices[2]
                ])
            i += add
        else:
            i += 1

    df = pd.DataFrame(rows, columns=[
        "SKU", "DESCRIPCION", "CANT", "PRECIO", "TOTAL"
    ])
    for col in ["CANT", "PRECIO", "TOTAL"]:
        df[col] = df[col].astype(float)
    return df
