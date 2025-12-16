import threading
import traceback

import pandas as pd
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, ttk

import criptos
import materias_primas
import acciones_infravaloradas


def cargar_en_treeview(tree: ttk.Treeview, df: pd.DataFrame):
    tree.delete(*tree.get_children())

    if df is None or df.empty:
        tree["columns"] = []
        return

    cols = list(df.columns)
    tree["columns"] = cols
    tree["show"] = "headings"

    for c in cols:
        tree.heading(c, text=c)
        tree.column(c, width=160, anchor=W)

    max_rows = 200
    for _, row in df.head(max_rows).iterrows():
        tree.insert("", END, values=[row[c] for c in cols])


def ejecutar_en_thread(root, lbl_status, tarea, al_final=None):
    def worker():
        try:
            resultado = tarea()
            if al_final:
                root.after(0, lambda: al_final(resultado))
            root.after(0, lambda: lbl_status.config(text="Listo."))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("Error", f"Ocurrió un error:\n{e}"))
            root.after(0, lambda: lbl_status.config(text="Error. Mirá el traceback en consola."))
            print("TRACEBACK:\n", traceback.format_exc())

    lbl_status.config(text="Cargando...")
    threading.Thread(target=worker, daemon=True).start()


def construir_pestania(root, notebook, titulo,
                      on_actualizar,
                      on_graf1=None, txt_graf1="Gráfico 1",
                      on_graf2=None, txt_graf2="Gráfico 2"):
    """Crea una pestaña SOLO con Actualizar + gráficos (sin botón Cargar CSV)."""
    frame = tb.Frame(notebook, padding=10)
    notebook.add(frame, text=titulo)

    barra = tb.Frame(frame)
    barra.pack(fill=X, pady=(0, 10))

    lbl_status = tb.Label(barra, text="Listo.")
    lbl_status.pack(side=RIGHT)

    tb.Button(
        barra, text="Actualizar", bootstyle=INFO,
        command=lambda: on_actualizar(lbl_status)
    ).pack(side=LEFT, padx=(0, 8))

    if on_graf1:
        tb.Button(barra, text=txt_graf1, bootstyle=SUCCESS,
                  command=on_graf1).pack(side=LEFT, padx=(0, 8))

    if on_graf2:
        tb.Button(barra, text=txt_graf2, bootstyle=SUCCESS,
                  command=on_graf2).pack(side=LEFT, padx=(0, 8))

    cont_tabla = tb.Frame(frame)
    cont_tabla.pack(fill=BOTH, expand=True)

    tree = ttk.Treeview(cont_tabla)
    tree.pack(side=LEFT, fill=BOTH, expand=True)

    scroll_y = ttk.Scrollbar(cont_tabla, orient=VERTICAL, command=tree.yview)
    scroll_y.pack(side=RIGHT, fill=Y)
    tree.configure(yscrollcommand=scroll_y.set)

    return tree


def main():
    root = tb.Window(themename="cyborg")
    root.title("Dashboard simple - Finanzas (ttkbootstrap)")
    root.geometry("1200x700")

    notebook = tb.Notebook(root)
    notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)

    barra_inferior = tb.Frame(root, padding=(10, 0, 10, 10))
    barra_inferior.pack(fill=X)
    tb.Button(
        barra_inferior,
        text="Salir",
        bootstyle="warning-outline",
        command=root.destroy
    ).pack(side=RIGHT)

    # IMPORTANTE: arrancan en None
    data_actual = {"cripto": None, "mp": None, "infra": None}

    # -------------------------
    # PESTAÑA CRIPTOS
    # -------------------------
    def cripto_actualizar(lbl):
        ejecutar_en_thread(
            root, lbl,
            tarea=lambda: criptos.actualizar_info_cripto(),
            al_final=lambda df: (data_actual.__setitem__("cripto", df),
                                cargar_en_treeview(tree_cripto, df)),
        )

    def cripto_graf1():
        df = data_actual["cripto"]
        if df is None or df.empty:
            messagebox.showinfo("Info", "No hay datos cargados. Presioná 'Actualizar'.")
            return
        criptos.grafico_nombre_vs_capi(df, top_n=20)

    def cripto_graf2():
        df = data_actual["cripto"]
        if df is None or df.empty:
            messagebox.showinfo("Info", "No hay datos cargados. Presioná 'Actualizar'.")
            return
        criptos.grafico_rango_atl_ath(df, top_n=20)

    tree_cripto = construir_pestania(
        root, notebook, "Criptos",
        on_actualizar=cripto_actualizar,
        on_graf1=cripto_graf1, txt_graf1="Top 20 por Cap.",
        on_graf2=cripto_graf2, txt_graf2="Rango ATL/ATH"
    )

    # -------------------------
    # PESTAÑA MATERIAS PRIMAS
    # -------------------------
    def mp_actualizar(lbl):
        ejecutar_en_thread(
            root, lbl,
            tarea=lambda: materias_primas.actualizar_informacion_mp(),
            al_final=lambda df: (data_actual.__setitem__("mp", df),
                                cargar_en_treeview(tree_mp, df)),
        )

    def mp_graf1():
        df = data_actual["mp"]
        if df is None or df.empty:
            messagebox.showinfo("Info", "No hay datos cargados. Presioná 'Actualizar'.")
            return
        materias_primas.graficos_top10(df)

    def mp_graf2():
        df = data_actual["mp"]
        if df is None or df.empty:
            messagebox.showinfo("Info", "No hay datos cargados. Presioná 'Actualizar'.")
            return
        materias_primas.graficos_todas(df)

    tree_mp = construir_pestania(
        root, notebook, "Materias primas",
        on_actualizar=mp_actualizar,
        on_graf1=mp_graf1, txt_graf1="Top 10 Volumen",
        on_graf2=mp_graf2, txt_graf2="Todas"
    )

    # -------------------------
    # PESTAÑA ACCIONES INFRA
    # -------------------------
    def infra_actualizar(lbl):
        ejecutar_en_thread(
            root, lbl,
            tarea=lambda: acciones_infravaloradas.actualizar_informacion_infra(),
            al_final=lambda df: (data_actual.__setitem__("infra", df),
                                cargar_en_treeview(tree_infra, df)),
        )

    def infra_graf1():
        df = data_actual["infra"]
        if df is None or df.empty:
            messagebox.showinfo("Info", "No hay datos cargados. Presioná 'Actualizar'.")
            return
        acciones_infravaloradas.ranking_pe_masbajas(df)

    def infra_graf2():
        df = data_actual["infra"]
        if df is None or df.empty:
            messagebox.showinfo("Info", "No hay datos cargados. Presioná 'Actualizar'.")
            return
        acciones_infravaloradas.pe_vs_cambio(df)

    tree_infra = construir_pestania(
        root, notebook, "Acciones infravaloradas",
        on_actualizar=infra_actualizar,
        on_graf1=infra_graf1, txt_graf1="Ranking P/E bajas",
        on_graf2=infra_graf2, txt_graf2="P/E vs Cambio"
    )

    # -------------------------
    # CARGA AUTOMÁTICA AL INICIAR (si existen los CSV)
    # -------------------------
    try:
        df = criptos.cargar_csv_cripto()
        data_actual["cripto"] = df
        cargar_en_treeview(tree_cripto, df)
    except FileNotFoundError:
        pass

    try:
        df = materias_primas.cargar_csv_mp()
        data_actual["mp"] = df
        cargar_en_treeview(tree_mp, df)
    except FileNotFoundError:
        pass

    try:
        df = acciones_infravaloradas.cargar_csv_infra()
        data_actual["infra"] = df
        cargar_en_treeview(tree_infra, df)
    except FileNotFoundError:
        pass

    root.mainloop()


if __name__ == "__main__":
    main()
