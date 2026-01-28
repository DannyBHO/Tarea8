import os
import subprocess
import sys

def mostrar_codigo(ruta_script):
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {os.path.basename(ruta_script)} ---\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print(" El archivo no se encontró.")
        return None
    except Exception as e:
        print(f" Error al leer el archivo: {e}")
        return None


def ejecutar_codigo(ruta_script):
    try:
        print("\n▶ Ejecutando script...\n")
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/k', sys.executable, ruta_script])
        else:  # Linux / Mac
            subprocess.Popen([sys.executable, ruta_script])
    except Exception as e:
        print(f"❌ Error al ejecutar el código: {e}")


def mostrar_menu():
    ruta_base = os.path.dirname(__file__)

    unidades = {
        '1': 'Unidad 1',
        '2': 'Unidad 2'
    }

    while True:
        print("\n===== DASHBOARD PRINCIPAL =====")
        for key, value in unidades.items():
            print(f"{key} - {value}")
        print("0 - Salir")

        eleccion_unidad = input("Seleccione una opción: ")

        if eleccion_unidad == '0':
            print(" Saliendo del programa.")
            break
        elif eleccion_unidad in unidades:
            ruta_unidad = os.path.join(ruta_base, unidades[eleccion_unidad])
            if os.path.exists(ruta_unidad):
                mostrar_sub_menu(ruta_unidad)
            else:
                print(" La unidad no existe.")
        else:
            print(" Opción no válida.")


def mostrar_sub_menu(ruta_unidad):
    sub_carpetas = sorted(
        [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]
    )

    if not sub_carpetas:
        print(" No hay subcarpetas disponibles.")
        return

    while True:
        print("\n--- SUBMENÚ ---")
        for i, carpeta in enumerate(sub_carpetas, start=1):
            print(f"{i} - {carpeta}")
        print("0 - Regresar")

        opcion = input("Seleccione una opción: ")

        if opcion == '0':
            break
        try:
            index = int(opcion) - 1
            if 0 <= index < len(sub_carpetas):
                mostrar_scripts(os.path.join(ruta_unidad, sub_carpetas[index]))
            else:
                print(" Opción inválida.")
        except ValueError:
            print(" Ingrese un número válido.")


def mostrar_scripts(ruta_sub_carpeta):
    scripts = sorted(
        [f.name for f in os.scandir(ruta_sub_carpeta)
         if f.is_file() and f.name.endswith('.py')]
    )

    if not scripts:
        print("⚠ No hay scripts disponibles.")
        return

    while True:
        print("\n--- SCRIPTS DISPONIBLES ---")
        for i, script in enumerate(scripts, start=1):
            print(f"{i} - {script}")
        print("0 - Regresar")
        print("9 - Menú principal")

        opcion = input("Seleccione una opción: ")

        if opcion == '0':
            break
        elif opcion == '9':
            return
        try:
            index = int(opcion) - 1
            if 0 <= index < len(scripts):
                ruta_script = os.path.join(ruta_sub_carpeta, scripts[index])
                codigo = mostrar_codigo(ruta_script)
                if codigo:
                    ejecutar = input("¿Desea ejecutar el script? (1: Sí | 0: No): ")
                    if ejecutar == '1':
                        ejecutar_codigo(ruta_script)
                input("\nPresione Enter para continuar...")
            else:
                print(" Opción inválida.")
        except ValueError:
            print(" Ingrese un número válido.")


if __name__ == "__main__":
    mostrar_menu()

