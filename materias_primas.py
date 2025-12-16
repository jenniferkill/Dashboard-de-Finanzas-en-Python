import os
import re
import numpy as np
import pandas as pd
import plotly.express as px
from Funciones import conexion_web, modificacion_tipo_datos


# materias primas
# Ruta  del CSV
def ruta_csv_mp():
    carpeta_proyecto = os.path.dirname(__file__)
    carpeta_data = os.path.join(carpeta_proyecto, "data")
    os.makedirs(carpeta_data, exist_ok=True)
    return os.path.join(carpeta_data, "materias_primas.csv")


def limpiar_df_mp(df_mp: pd.DataFrame) -> pd.DataFrame:
    """Convierte columnas clave a numérico para que nlargest y gráficos funcionen."""
    df_mp = df_mp.copy()

    cols = ["Precio", "% Cambio", "Volumen", "Posiciones en abierto"]
    for c in cols:
        if c in df_mp.columns:
            df_mp[c] = df_mp[c].apply(modificacion_tipo_datos)

    return df_mp

#  Actualizar info (descargar + limpiar + guardar CSV)
def actualizar_informacion_mp():
    url_mp = "https://es.finance.yahoo.com/mercados/materias-primas/"

    tablas_mp = conexion_web(url_mp)
    df = tablas_mp[0]

    df_mp = df[
        ["Symbol", "Name", "Price", "Change", "Change %", "Volume", "Posiciones en abierto"]
    ].copy()

    df_mp.columns = ["Simbolos", "Nombre", "Precio", "Cambio", "% Cambio", "Volumen", "Posiciones en abierto"]

    # Convertir tipos numéricos (importante para top 10 por volumen)
    df_mp = limpiar_df_mp(df_mp)

    ruta_csv = ruta_csv_mp()
    df_mp.to_csv(ruta_csv, index=False, encoding="utf-8-sig")
    print(f"Se actualizó correctamente y se guardó en: {ruta_csv}")

    return df_mp
#  Cargar CSV
# -------------------------------------------------
def cargar_csv_mp():
    ruta_csv = ruta_csv_mp()
    df_mp = pd.read_csv(ruta_csv, encoding="utf-8-sig")

    # Asegurar tipos numéricos aunque el CSV venga con strings
    df_mp = limpiar_df_mp(df_mp)
    return df_mp


#--------GRaficos--------#
#Nombre vs Cambio top 10 de volumen
def graficos_top10(df_mp: pd.DataFrame):
    # si hay NaN en Volumen, nlargest no explota pero conviene filtrar
    dfp = df_mp.dropna(subset=["Volumen"]).copy()
    df_top10 = dfp.nlargest(10, "Volumen")

    fig = px.bar(
        df_top10,
        x="Nombre",
        y="Volumen",
        title="Top 10 Materias Primas por Volumen",
        labels={"Nombre": "Materias Primas"},
        width=1600,
        height=800
    )
    fig.show()
    return fig
#Nombre vs Cambio todas las materias primas
def graficos_todas(df_mp: pd.DataFrame):
    fig = px.histogram(
        df_mp,
        x="Nombre",
        y="Volumen",
        title="Todas las Materias Primas",
        labels={"Nombre": "Materias Primas"},
        width=1600,
        height=800
    )
    fig.show()
    return fig


def mostrar_data_mp(df_mp: pd.DataFrame, n: int = 21):
    print(df_mp.head(n))


