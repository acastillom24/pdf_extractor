import tkinter as tk
from tkinter import messagebox, ttk

from processor.modelo1 import procesar_pdf_modelo1
from processor.modelo2 import procesar_pdf_modelo2
from utils.file_dialogs import save_excel_file, select_pdf_file


class PDFExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Extractor de Datos PDF a Excel")
        self.root.geometry("600x400")

        self.dfs = {1: None, 2: None}  # Cada modelo tiene su propio DataFrame
        self.text_summaries = {}      # Cada pestaña tiene su Text separado

        self.tab_control = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Modelo 1')
        self.tab_control.add(self.tab2, text='Modelo 2')
        self.tab_control.pack(expand=1, fill="both")

        self.create_tab_content(self.tab1, 1)
        self.create_tab_content(self.tab2, 2)

    def create_tab_content(self, tab, modelo):
        ttk.Label(tab, text=f"Seleccione un PDF del Modelo {modelo}").pack(pady=10)

        btn_frame = ttk.Frame(tab)
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="Seleccionar PDF", command=lambda: self.handle_file(modelo)).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Descargar Excel", command=lambda: self.save_excel(modelo)).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Reiniciar", command=lambda: self.reset_ui(modelo)).grid(row=0, column=2, padx=5)

        text_summary = tk.Text(tab, height=10, width=70, state='disabled')
        text_summary.pack(pady=10)
        self.text_summaries[modelo] = text_summary  # Guardar referencia por modelo

    def handle_file(self, modelo):
        filepath = select_pdf_file()
        if not filepath:
            return

        try:
            if modelo == 1:
                self.dfs[modelo] = procesar_pdf_modelo1(filepath)
            else:
                self.dfs[modelo] = procesar_pdf_modelo2(filepath)

            total_sum = self.dfs[modelo].select_dtypes(include='number').sum()
            self.display_summary(modelo, total_sum)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_summary(self, modelo, total_sum):
        text_widget = self.text_summaries[modelo]
        text_widget.configure(state='normal')
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, "Resumen de totales:\n")
        text_widget.insert(tk.END, total_sum.to_string())
        text_widget.configure(state='disabled')

    def save_excel(self, modelo):
        df = self.dfs.get(modelo)
        if df is None:
            messagebox.showwarning("Aviso", "Primero debe procesar un PDF.")
            return
        output_path = save_excel_file()
        if output_path:
            df.to_excel(output_path, index=False)
            messagebox.showinfo("Éxito", f"Archivo guardado en:\n{output_path}")

    def reset_ui(self, modelo):
        self.dfs[modelo] = None
        text_widget = self.text_summaries[modelo]
        text_widget.configure(state='normal')
        text_widget.delete("1.0", tk.END)
        text_widget.configure(state='disabled')


def run_app():
    root = tk.Tk()
    app = PDFExtractorApp(root)
    root.mainloop()
