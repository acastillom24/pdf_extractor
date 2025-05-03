# 📦 PDF Extractor a Excel (Modelo 1 y 2)

Este programa permite cargar archivos PDF de dos formatos distintos ("Modelo 1" y "Modelo 2") y extraer los datos estructurados en tablas para exportarlos a Excel. También calcula la suma de columnas numéricas relevantes.

---

## 🖼 Interfaz

La aplicación cuenta con dos pestañas:

- **Modelo 1**: PDFs que contienen encabezados como `"UNITARIO UNIT. UNIT. CON CON DSCTO."`
- **Modelo 2**: PDFs con encabezados como `"SKU DESC CANT. PRECIO TOTAL"`

---

## 🚀 Instrucciones de uso

1. Ejecuta `main.py`.
2. En la interfaz, selecciona la pestaña correspondiente al modelo de tu PDF.
3. Haz clic en "Seleccionar PDF" y elige el archivo.
4. El programa mostrará la suma de totales extraídos y te permitirá guardar el archivo Excel.

---

## 📁 Estructura del Proyecto

pdf_extractor/  
├── main.py                     # Archivo principal que lanza la aplicación  
├── gui/  
│   └── app.py                  # Interfaz gráfica en Tkinter  
├── processor/  
│   ├── modelo1.py              # Lógica de extracción para Modelo 1  
│   ├── modelo2.py              # Lógica de extracción para Modelo 2  
│   └── common.py               # Funciones auxiliares comunes (opcional)  
└── utils/  
    └── file_dialogs.py         # Funciones reutilizables para seleccionar y guardar archivos  

---

## 📦 Instalación de dependencias

Primero, asegúrate de tener Python 3.10+ instalado.

Luego, instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

---

## 🛠 Generar ejecutable para Windows

Usa `pyinstaller` para generar un `.exe` ejecutable:

1. Instálalo si no lo tienes:

```bash
pip install -r requirements.txt
```

2. Desde la carpeta raíz (`pdf_extractor/`), ejecuta:

```bash
pyinstaller --noconfirm --onefile --windowed main.py
```
Esto generará una carpeta `dist/` con el ejecutable `main.exe` dentro.
