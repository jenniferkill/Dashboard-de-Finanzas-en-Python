README - Dashboard de Finanzas en Python (GUI + CLI)
==================================================

Aplicación en Python para consultar, guardar y visualizar datos financieros de:
- Criptomonedas (API CoinGecko)
- Materias primas (Yahoo Finance – scraping)
- Acciones infravaloradas (Yahoo Finance Screener – scraping)

Incluye:
- Interfaz gráfica (ttkbootstrap) con pestañas
- Menú por consola (CLI)
- Guardado automático en CSV para reutilizar datos sin volver a descargar
- Carga automática al iniciar (si ya existen los CSV)


1) Características principales
-----------------------------
- Descarga datos desde fuentes públicas
- Convierte los datos a pandas.DataFrame
- Limpia y tipifica valores numéricos (%, K/M/B, N/A, etc.)
- Guarda resultados en data/*.csv
- Genera gráficos interactivos con Plotly
- GUI que no se congela usando threading
- Carga automática al iniciar si existen los CSV


2) Estructura del proyecto
--------------------------
Estructura recomendada:

proyecto_finanzas/
├── app_gui.py                          # GUI (ttkbootstrap)
├── main.py                             # Menú por consola (CLI)
├── Funciones.py                        # Funciones comunes (scraping)
├── criptos.py                          # API CoinGecko + CSV + gráficos
├── materias_primas.py                  # Yahoo scraping + CSV + gráficos
├── acciones_infravaloradas.py          # Yahoo screener + CSV + gráficos
└── data/
    ├── criptos.csv
    ├── materias_primas.csv
    └── acciones_infravaloradas.csv

Nota: la carpeta data/ se crea automáticamente si no existe.


3) Requisitos
-------------
- Python 3.10+ (recomendado)

Ejemplo de requirements.txt mínimo:

pandas
numpy
requests
plotly
ttkbootstrap
lxml
beautifulsoup4
html5lib


4) Instalación (Windows)
------------------------

4.1 Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate

4.2 Instalar dependencias
python -m pip install -r requirements.txt

4.3 Verificación (opcional)
python -c "import pandas, numpy, requests, plotly, ttkbootstrap; print('OK')"


5) Ejecución
------------

5.1 Ejecutar la GUI
python app_gui.py

Qué hace al abrir:
- Intenta cargar automáticamente data/criptos.csv, data/materias_primas.csv y data/acciones_infravaloradas.csv
- Si existen, los muestra directamente en cada pestaña
- Si no existen, se deben generar con el botón "Actualizar"

5.2 Ejecutar el menú por consola (CLI)
python main.py


6) Uso de la GUI
----------------
Cada pestaña representa un conjunto de datos:
- Criptos
- Materias primas
- Acciones infravaloradas

Botones típicos:
- Actualizar: descarga datos, limpia, guarda CSV y muestra la tabla
- Gráfico 1 / Gráfico 2: abre gráficos Plotly (en ventana/navegador externo)
- Salir: cierra la aplicación

Nota: Plotly abre los gráficos fuera de la app. Es normal y esperado.


7) Módulos y responsabilidades
------------------------------

7.1 Funciones.py
- conexion_web(url): descarga HTML y extrae tablas con pandas.read_html

7.2 criptos.py
Funciones principales:
- actualizar_info_cripto(): consume API CoinGecko, limpia, guarda data/criptos.csv
- cargar_csv_cripto(): carga el CSV
- grafico_nombre_vs_capi(df, top_n=20)
- grafico_rango_atl_ath(df, top_n=20)

7.3 materias_primas.py
Funciones principales:
- actualizar_informacion_mp(): scraping Yahoo, limpieza, guarda data/materias_primas.csv
- cargar_csv_mp(): carga el CSV
- graficos_top10(df)
- graficos_todas(df)

7.4 acciones_infravaloradas.py
Funciones principales:
- actualizar_informacion_infra(): scraping screener Yahoo, limpieza, guarda data/acciones_infravaloradas.csv
- cargar_csv_infra(): carga el CSV
- ranking_pe_masbajas(df)
- pe_vs_cambio(df)


8) Errores comunes y solución
-----------------------------

8.1 "No me toma las librerías instaladas"
Normalmente estás ejecutando con el Python global y no con el entorno virtual.
Verificá:
where python
python -c "import sys; print(sys.executable)"
python -m pip -V

Ejecutá siempre desde el entorno:
.venv\Scripts\activate
python app_gui.py

8.2 "CSV no encontrado"
Aparece si se intenta cargar datos y el CSV todavía no existe.
Solución: presionar "Actualizar" al menos una vez para generar el CSV.

8.3 Yahoo no devuelve tablas
Puede pasar por cambios en el HTML o restricciones.
Solución: reintentar más tarde y asegurarse de tener instalados:
- lxml
- beautifulsoup4
- html5lib


9) Mejoras futuras (ideas)
--------------------------
- Guardar histórico por fecha en lugar de sobrescribir CSV
- Agregar más métricas: variación 7d/30d, medias móviles, alertas
- Exportar reportes automáticos (Excel/PDF)
- Embebido de gráficos dentro de la GUI (más avanzado)


10) Autor
---------
Jennifer Paola Coral Reina 
Proyecto académico / portfolio (Python + Ciencia de Datos + Finanzas)
