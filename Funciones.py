import time
from io import StringIO

import pandas as pd
import requests
import numpy as np
import re


def conexion_web(url, timeout=30, max_retries=2, pause=1.0):
    """
    Descarga una página web y devuelve las tablas con pandas.read_html()

    - timeout: segundos máximos de espera por request
    - max_retries: cantidad de reintentos si falla
    - pause: pausa (segundos) entre reintentos
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    }

    ultimo_error = None

    for intento in range(max_retries + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()

            html = StringIO(resp.text)
            tablas = pd.read_html(html)
            return tablas

        except requests.exceptions.RequestException as e:
            ultimo_error = e
            # Si todavía quedan reintentos, esperamos y reintentamos
            if intento < max_retries:
                time.sleep(pause)
            else:
                # Ya no quedan reintentos
                raise

        except ValueError as e:
            # pandas.read_html lanza ValueError si no encuentra tablas
            raise ValueError(f"No se encontraron tablas HTML en: {url}") from e

def  modificacion_tipo_datos(x):
    """
    Convierte cosas como:
    - '1.234,56' -> 1234.56
    - '+2,3%' -> 2.3
    - '1,2K' / '3,4M' / '5,6MM' -> números
    - 'N/A', '-', '—' -> NaN
    """
    if pd.isna(x):
        return np.nan

    s = str(x).strip().replace("\xa0", "").replace(" ", "")
    if s in {"", "-", "—", "N/A"}:
        return np.nan

    s = s.replace("+", "").replace("%", "")

    # normalizar separadores (coma decimal)
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")

    mult = 1.0
    if s.endswith("T"):
        mult = 1e12; s = s[:-1]
    elif s.endswith("MM"):
        mult = 1e9; s = s[:-1]
    elif s.endswith("M"):
        mult = 1e6; s = s[:-1]
    elif s.endswith("K"):
        mult = 1e3; s = s[:-1]

    s = re.sub(r"[^0-9\.\-]", "", s)

    try:
        return float(s) * mult
    except ValueError:
        return np.nan
