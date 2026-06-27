"""
¿Alcanza el sueldo para la canasta básica en Ecuador? (2018–2026)
=================================================================
Compara el costo de la Canasta Familiar Básica (CFB) con el ingreso familiar
mensual del hogar tipo (4 miembros, 1,6 perceptores que ganan el salario básico)
en Ecuador, valores de enero de cada año.

El área sombreada muestra el excedente (verde) o el déficit (rojo) del ingreso
frente al costo de vivir.

Fuente: INEC — Índice de Precios al Consumidor (IPC), boletines técnicos de enero.

Uso:
    pip install pandas matplotlib
    python grafico.py
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


# === Rutas del proyecto =====================================================

BASE = Path(__file__).parent
DATA_PATH = BASE / "data" / "canasta_vs_ingreso.csv"
OUTPUT_DIR = BASE / "output"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# === Cargar y validar datos =================================================

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"No se encontró el archivo CSV:\n{DATA_PATH}\n\n"
        "La estructura esperada es:\n"
        "  proyecto/\n"
        "  ├── grafico.py\n"
        "  ├── data/canasta_vs_ingreso.csv\n"
        "  └── output/\n"
    )

d = pd.read_csv(DATA_PATH)

columnas_necesarias = {"anio", "canasta_basica_usd", "ingreso_familiar_usd"}
faltantes = columnas_necesarias - set(d.columns)
if faltantes:
    raise ValueError("Faltan columnas en el CSV: " + ", ".join(sorted(faltantes)))

d = d.sort_values("anio")
x = d["anio"]
canasta = d["canasta_basica_usd"]
ingreso = d["ingreso_familiar_usd"]


# === Estilo visual ==========================================================

RED = "#c8553d"          
BLUE = "#1f4e5f"         
GREEN = "#4a7c59"        
GREEN_FILL = "#dce8df"   
DEFICIT_FILL = "#f2dcd5" 

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 14,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#9aa0a6",
    "text.color": "#202124",
    "axes.labelcolor": "#202124",
    "xtick.color": "#5f6368",
    "ytick.color": "#5f6368",
    "savefig.dpi": 200,
})


# === Construcción del gráfico ===============================================

fig, ax = plt.subplots(figsize=(12, 7))

ax.fill_between(x, ingreso, canasta, where=(ingreso >= canasta),
                interpolate=True, color=GREEN_FILL, alpha=0.9, zorder=1)
ax.fill_between(x, ingreso, canasta, where=(ingreso < canasta),
                interpolate=True, color=DEFICIT_FILL, alpha=0.9, zorder=1)

ax.plot(x, canasta, color=RED, linewidth=3, zorder=3,
        label="Costo de la canasta básica")
ax.plot(x, ingreso, color=BLUE, linewidth=3, zorder=3,
        label="Ingreso familiar (1,6 perceptores)")

ax.scatter(x, canasta, s=45, color=RED, zorder=4, edgecolor="white", linewidth=1)
ax.scatter(x, ingreso, s=45, color=BLUE, zorder=4, edgecolor="white", linewidth=1)


# === Etiquetas y anotaciones ================================================

ax.annotate(f"${canasta.iloc[0]:,.0f}", (x.iloc[0], canasta.iloc[0]),
            textcoords="offset points", xytext=(-4, -20), ha="center",
            fontsize=12.5, fontweight="bold", color=RED)
ax.annotate(f"${ingreso.iloc[0]:,.0f}", (x.iloc[0], ingreso.iloc[0]),
            textcoords="offset points", xytext=(-4, 12), ha="center",
            fontsize=12.5, fontweight="bold", color=BLUE)
ax.annotate(f"${canasta.iloc[-1]:,.0f}", (x.iloc[-1], canasta.iloc[-1]),
            textcoords="offset points", xytext=(6, -18), ha="center",
            fontsize=12.5, fontweight="bold", color=RED)
ax.annotate(f"${ingreso.iloc[-1]:,.0f}", (x.iloc[-1], ingreso.iloc[-1]),
            textcoords="offset points", xytext=(6, 12), ha="center",
            fontsize=12.5, fontweight="bold", color=BLUE)
ax.annotate("Tras 2022 el ingreso\nse despega de la canasta",
            xy=(2023, 802), xytext=(2019.0, 815),
            fontsize=13, color=GREEN,
            arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.5))


# === Ejes, título y leyenda =================================================

ax.set_xticks(x)
ax.set_xticklabels(x, fontsize=12)
ax.tick_params(axis="y", labelsize=12)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"${v:,.0f}"))

ax.set_title("¿Alcanza el sueldo para la canasta básica en Ecuador?",
             fontsize=18, fontweight="bold", loc="left", pad=34)
ax.text(0, 1.02,
        "Costo de la Canasta Familiar Básica vs. ingreso del hogar tipo, 2018–2026",
        transform=ax.transAxes, fontsize=13, color="#5f6368")

ax.legend(loc="lower right", frameon=False, fontsize=12.5)
ax.margins(x=0.06)
ax.set_ylim(685, 915)

fig.text(0.02, 0.005,
         "Fuente: INEC – Índice de Precios al Consumidor (IPC), boletines técnicos de enero "
         "(datos oficiales). Elaboración propia, Ecuador Quantificado 2026.",
         fontsize=10, color="#80868b", ha="left")


# === Guardar resultados =====================================================

png_path = OUTPUT_DIR / "canasta_vs_ingreso.png"
svg_path = OUTPUT_DIR / "canasta_vs_ingreso.svg"

fig.savefig(png_path, bbox_inches="tight", facecolor="white")
fig.savefig(svg_path, bbox_inches="tight", facecolor="white")

print("Guardado correctamente:")
print(f"- {png_path}")
print(f"- {svg_path}")
