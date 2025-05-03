from tkinter import filedialog

def select_pdf_file():
    return filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])

def save_excel_file():
    return filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
