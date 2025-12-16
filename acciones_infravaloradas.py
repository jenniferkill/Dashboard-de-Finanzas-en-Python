import pandas as pd

from Funciones import conexion_web, modificacion_tipo_datos
import plotly.express as px
import numpy as np
import os

# ---------- util ----------


def _ruta_csv():
    base_dir = os.path.dirname(__file__)  # evita lío con rutas en GUI
    carpeta = os.path.join(base_dir, "data")
    os.makedirs(carpeta, exist_ok=True)
    return os.path.join(carpeta, "acciones_infravaloradas.csv")


def actualizar_informacion_infra():
    url = "https://es.finance.yahoo.com/research-hub/screener/undervalued_growth_stocks/?start=0&count=100"
    tablas = conexion_web(url)
    df_raw = tablas[0]

    df = df_raw[['Symbol','Name','Precio (intradía)','Change','Change %','Volume','Market Cap','P/E Ratio (TTM)']].copy()
    df.columns = ['Simbolo','Nombre','Precio (intradía)','Cambio','Cambio %','Volumen','Capitalización de mercado','P/E Ratio (TTM)']

    # convertir tipos (incluyendo P/E)
    for col in ["Cambio %", "Volumen", "Capitalización de mercado", "P/E Ratio (TTM)"]:
        df[col] = df[col].apply(modificacion_tipo_datos)

    ruta = _ruta_csv()
    df.to_csv(ruta, index=False, encoding="utf-8-sig")
    print(f"Guardado/actualizado: {ruta}")

    return df


def cargar_csv_infra():
    ruta = _ruta_csv()
    return pd.read_csv(ruta, encoding="utf-8-sig")


#--------------------------------
######Graficos##########
#---------------------------------

def ranking_pe_masbajas(df_acciones_infra):
    df_top20 = df_acciones_infra.nsmallest(20, "P/E Ratio (TTM)")
    fig = px.bar(df_top20, x="Simbolo", y="P/E Ratio (TTM)",
                 title="Top 20 acciones infravaloradas por P/E Ratio más bajas",
                 text_auto=True)
    fig.show()


def pe_vs_cambio(df_acciones_infra):
    dfp = df_acciones_infra.dropna(subset=["P/E Ratio (TTM)", "Cambio %", "Capitalización de mercado"]).copy()
    dfp["rango"] = np.where(dfp["Cambio %"] >= 0, "Sube", "Baja")

    fig = px.scatter(dfp, x="P/E Ratio (TTM)", y="Cambio %",
                     color="rango", size="Capitalización de mercado",
                     hover_data=["Simbolo","Nombre","Precio (intradía)","Volumen"],
                     title="P/E vs Cambio % (detección de outliers)")
    fig.show()


