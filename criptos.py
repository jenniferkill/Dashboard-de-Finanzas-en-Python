import os
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

#Ruta estable del CSV
def ruta_csv_cripto():
    carpeta_proyecto = os.path.dirname(__file__)
    carpeta_data = os.path.join(carpeta_proyecto, "data")
    os.makedirs(carpeta_data, exist_ok=True)
    return os.path.join(carpeta_data, "criptos.csv")

#Descargar y devolver DataFrame
def get_top_100_coins() -> pd.DataFrame:
    url = "https://api.coingecko.com/api/v3/coins/markets"

    headers = {
        # Si un día querés, podés mover esto a variable de entorno.
        "x-cg-demo-api-key": "CG-ubVTXyBxsevcSKkpM14Y8qyo"
    }

    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": "false",
        "price_change_percentage": "24h,7d"
    }

    resp = requests.get(url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    return pd.DataFrame(data)

#asegurar números y quitar filas inválidas
def limpiar_df_cripto(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    cols_num = [
        "Precio (usd)",
        "Capi. de Mercado",
        "Rango de CM",
        "Minimo Historico(ATL)",
        "Maximo Historico(ATH)"
    ]

    # Convertir a numérico (lo que no se pueda -> NaN)
    df.loc[:, cols_num] = df.loc[:, cols_num].apply(pd.to_numeric, errors="coerce")
    return df
#Actualizar info
def actualizar_info_cripto() -> pd.DataFrame:
    df = get_top_100_coins()

    dfcriptos = df[
        ["symbol", "name", "current_price", "market_cap", "market_cap_rank", "atl", "ath"]
    ].copy()

    dfcriptos.columns = [
        "Simbolo",
        "Nombre",
        "Precio (usd)",
        "Capi. de Mercado",
        "Rango de CM",
        "Minimo Historico(ATL)",
        "Maximo Historico(ATH)"
    ]

    dfcriptos = limpiar_df_cripto(dfcriptos)

    ruta_csv = ruta_csv_cripto()
    dfcriptos.to_csv(ruta_csv, index=False, encoding="utf-8-sig")
    print(f"Se actualizó correctamente y se guardó en: {ruta_csv}")

    return dfcriptos

#Cargar CSV
def cargar_csv_cripto() -> pd.DataFrame:
    ruta_csv = ruta_csv_cripto()
    df = pd.read_csv(ruta_csv, encoding="utf-8-sig")

    # Asegurar limpieza por si el CSV quedó con strings
    df = limpiar_df_cripto(df)
    return df


# --------------------------------
######Graficos##########
# ---------------------------------

# Gráfico 1: barras horizontales de nombre por capitalización
def grafico_nombre_vs_capi(dfcriptos: pd.DataFrame, top_n: int = 20):
    df_top = dfcriptos.nlargest(top_n, "Capi. de Mercado").copy()

    fig = px.bar(
        df_top.sort_values("Capi. de Mercado"),
        x="Capi. de Mercado",
        y="Nombre",
        orientation="h",
        hover_data=["Simbolo", "Precio (usd)", "Rango de CM"],
        title=f"Top {top_n} criptomonedas por Capitalización de Mercado"
    )
    fig.update_layout(xaxis_title="Capitalización (USD)", yaxis_title="")
    fig.show()

# Gráfico 2: rango ATL-ATH + precio actual + métricas
def grafico_rango_atl_ath(dfcriptos: pd.DataFrame, top_n: int = 20):
    df_top = dfcriptos.nlargest(top_n, "Capi. de Mercado").copy()

    # Evitar divisiones por 0
    ath = df_top["Maximo Historico(ATH)"].replace(0, np.nan)
    atl = df_top["Minimo Historico(ATL)"].replace(0, np.nan)

    df_top["% bajo ATH"] = (ath - df_top["Precio (usd)"]) / ath * 100
    df_top["% desde ATL"] = (df_top["Precio (usd)"] - atl) / atl * 100

    # Orden visual
    df_top = df_top.sort_values("Precio (usd)")

    fig = go.Figure()

    # ATL markers
    fig.add_trace(go.Scatter(
        x=df_top["Minimo Historico(ATL)"],
        y=df_top["Nombre"],
        mode="markers",
        name="ATL",
        marker=dict(size=8),
        hovertemplate="<b>%{y}</b><br>ATL: %{x}<extra></extra>"
    ))

    # ATH markers
    fig.add_trace(go.Scatter(
        x=df_top["Maximo Historico(ATH)"],
        y=df_top["Nombre"],
        mode="markers",
        name="ATH",
        marker=dict(size=8),
        hovertemplate="<b>%{y}</b><br>ATH: %{x}<extra></extra>"
    ))

    # Segmentos ATL -> ATH
    for _, row in df_top.iterrows():
        fig.add_shape(
            type="line",
            x0=row["Minimo Historico(ATL)"],
            x1=row["Maximo Historico(ATH)"],
            y0=row["Nombre"],
            y1=row["Nombre"],
            xref="x",
            yref="y",
            line=dict(width=3)
        )

    # Precio actual con métricas
    customdata = np.stack([
        df_top["Minimo Historico(ATL)"],
        df_top["Maximo Historico(ATH)"],
        df_top["% bajo ATH"].fillna(np.nan),
        df_top["% desde ATL"].fillna(np.nan)
    ], axis=-1)

    fig.add_trace(go.Scatter(
        x=df_top["Precio (usd)"],
        y=df_top["Nombre"],
        mode="markers",
        name="Precio actual",
        marker=dict(size=10, symbol="circle"),
        customdata=customdata,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Precio: %{x}<br>"
            "ATL: %{customdata[0]}<br>"
            "ATH: %{customdata[1]}<br>"
            "% bajo ATH: %{customdata[2]:.2f}%<br>"
            "% desde ATL: %{customdata[3]:.2f}%"
            "<extra></extra>"
        )
    ))

    fig.update_xaxes(type="log", title="Precio (USD) - escala log (ATL–ATH y precio actual)")
    fig.update_layout(
        title=f"Precio actual dentro del rango histórico (Top {top_n} por Market Cap)",
        yaxis_title=""
    )
    fig.show()


def mostrar_data_cripto(dfcriptos: pd.DataFrame):
    print(dfcriptos)


