from criptos import (
    actualizar_info_cripto,
    cargar_csv_cripto,
    grafico_nombre_vs_capi,
    grafico_rango_atl_ath,
    mostrar_data_cripto
)

from materias_primas import (
    actualizar_informacion_mp,
    cargar_csv_mp,
    graficos_todas,
    graficos_top10,
    mostrar_data_mp
)

from acciones_infravaloradas import (
    actualizar_informacion_infra,
    cargar_csv_infra,
    ranking_pe_masbajas,
    pe_vs_cambio,
    mostrar_data_infra
)


def pedir_entero(mensaje: str):
    valor = input(mensaje).strip()
    try:
        return int(valor)
    except ValueError:
        return None


def pedir_opcion(titulo: str, opciones: dict[int, str]) -> int:
    while True:
        print("\n" + titulo)
        for k in sorted(opciones):
            print(f"{k} - {opciones[k]}")

        op = pedir_entero("Ingrese opción: ")
        if op is not None and op in opciones:
            return op

        print("Opción inválida. Intente nuevamente.")


# -----------------------------
# SUBMENÚ CRIPTOS
# -----------------------------
def submenu_cripto():
    df_cripto = None

    while True:
        op = pedir_opcion(
            "CRIPTOMONEDAS",
            {
                1: "Actualizar información",
                2: "Cargar CSV",
                3: "Gráfico nombre vs capitalización",
                4: "Gráfico rango ATL y ATH",
                5: "Revisar información completa",
                0: "Volver"
            }
        )

        if op == 0:
            break

        if op == 1:
            df_cripto = actualizar_info_cripto()

        elif op == 2:
            try:
                df_cripto = cargar_csv_cripto()
                print("CSV cargado correctamente.")
            except FileNotFoundError:
                print("No existe el CSV. Primero usá 'Actualizar información'.")

        elif op == 3:
            if df_cripto is None:
                try:
                    df_cripto = cargar_csv_cripto()
                except FileNotFoundError:
                    print("No hay datos. Actualizá primero.")
                    continue
            grafico_nombre_vs_capi(df_cripto, top_n=20)

        elif op == 4:
            if df_cripto is None:
                try:
                    df_cripto = cargar_csv_cripto()
                except FileNotFoundError:
                    print("No hay datos. Actualizá primero.")
                    continue
            grafico_rango_atl_ath(df_cripto, top_n=20)

        elif op == 5:
            if df_cripto is None:
                try:
                    df_cripto = cargar_csv_cripto()
                except FileNotFoundError:
                    print("No hay datos. Actualizá primero.")
                    continue
            mostrar_data_cripto(df_cripto)


# -----------------------------
# SUBMENÚ MATERIAS PRIMAS
# -----------------------------
def submenu_materias_primas():
    df_mp = None

    while True:
        op = pedir_opcion(
            "MATERIAS PRIMAS",
            {
                1: "Actualizar información",
                2: "Cargar CSV",
                3: "Gráfico de todas las materias primas",
                4: "Gráfico Top 10 materias primas",
                5: "Revisar información completa",
                0: "Volver"
            }
        )

        if op == 0:
            break

        if op == 1:
            df_mp = actualizar_informacion_mp()

        elif op == 2:
            try:
                df_mp = cargar_csv_mp()
                print("CSV cargado correctamente.")
            except FileNotFoundError:
                print("No existe el CSV. Primero usá 'Actualizar información'.")

        elif op == 3:
            if df_mp is None:
                try:
                    df_mp = cargar_csv_mp()
                except FileNotFoundError:
                    print("No hay datos. Actualizá primero.")
                    continue
            graficos_todas(df_mp)

        elif op == 4:
            if df_mp is None:
                try:
                    df_mp = cargar_csv_mp()
                except FileNotFoundError:
                    print("No hay datos. Actualizá primero.")
                    continue
            graficos_top10(df_mp)

        elif op == 5:
            if df_mp is None:
                try:
                    df_mp = cargar_csv_mp()
                except FileNotFoundError:
                    print("No hay datos. Actualizá primero.")
                    continue
            mostrar_data_mp(df_mp)


# -----------------------------
# SUBMENÚ ACCIONES INFRA
# -----------------------------
def submenu_infravaloradas():
    df_infra = None

    while True:
        op = pedir_opcion(
            "ACCIONES INFRAVALORADAS",
            {
                1: "Actualizar información",
                2: "Cargar CSV",
                3: "Ranking P/E más bajas",
                4: "P/E vs Cambio",
                5: "Revisar información completa",
                0: "Volver"
            }
        )

        if op == 0:
            break

        if op == 1:
            df_infra = actualizar_informacion_infra()

        elif op == 2:
            try:
                df_infra = cargar_csv_infra()
                print("CSV cargado correctamente.")
            except FileNotFoundError:
                print("No existe el CSV. Primero usá 'Actualizar información'.")

        elif op == 3:
            if df_infra is None:
                try:
                    df_infra = cargar_csv_infra()
                except FileNotFoundError:
                    print("No hay datos. Actualizá primero.")
                    continue
            ranking_pe_masbajas(df_infra)

        elif op == 4:
            if df_infra is None:
                try:
                    df_infra = cargar_csv_infra()
                except FileNotFoundError:
                    print("No hay datos. Actualizá primero.")
                    continue
            pe_vs_cambio(df_infra)

        elif op == 5:
            if df_infra is None:
                try:
                    df_infra = cargar_csv_infra()
                except FileNotFoundError:
                    print("No hay datos. Actualizá primero.")
                    continue
            mostrar_data_infra(df_infra)


def main():
    while True:
        op = pedir_opcion(
            "MENÚ PRINCIPAL",
            {
                1: "Información de criptomonedas",
                2: "Información de materias primas",
                3: "Información de acciones infravaloradas",
                4: "Salir"
            }
        )

        if op == 4:
            print("Saliendo del programa...")
            break
        elif op == 1:
            submenu_cripto()
        elif op == 2:
            submenu_materias_primas()
        elif op == 3:
            submenu_infravaloradas()


if __name__ == "__main__":
    main()