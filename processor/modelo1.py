import pdfplumber
import pandas as pd
import re

def procesar_pdf_modelo1(filepath):
    with pdfplumber.open(filepath) as pdf:
        raw_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())

    start_marker = "UNITARIO UNIT. UNIT. CON CON DSCTO."
    end_marker = "NOTA: OPERACION SUJETA A PERCEPCION DEL IGV"
    start = raw_text.find(start_marker)
    end = raw_text.find(end_marker)
    data_block = raw_text[start:end]
    data_block = re.sub(r"UNITARIO UNIT. UNIT. CON CON DSCTO.*?\n", "", data_block)

    lines = [line.strip() for line in data_block.splitlines() if line.strip()]
    rows = []
    i = 0
    while i < len(lines):
        if re.match(r"^\d+\s", lines[i]):
            add = 1
            cant, text = lines[i].split(" ", 1)
            code = re.search(r'\b(\d{8,9})\b', text).group(1)
            desc, prices = text.split(code)
            desc = desc.strip()
            prices = prices.strip().split()
            if lines[i + 1].startswith("LOTE"):
                desc += " " + lines[i + 1]
                add = 2
            rows.append([
                cant,
                desc,
                code,
                prices[0],
                prices[1],
                prices[2],
                prices[3]
            ])
            i += add
        else:
            i += 1

    df = pd.DataFrame(rows, columns=[
        "CANT",
        "DESCRIPCION",
        "CODIGO VTA.",
        "PRECIO DE VENTA UNITARIO",
        "VALOR VENTA CAT. UNIT.",
        "VALOR VENTA CAT. UNIT. CON",
        "VALOR VENTA CAT. CON DSCTO."
    ])
    df["CANT"] = df["CANT"].astype(int)
    for col in df.columns[3:]:
        df[col] = df[col].astype(float)
    return df
