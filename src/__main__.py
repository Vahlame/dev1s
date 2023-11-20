import colorama
import os
import ctypes
import sys

is_admin = lambda: ctypes.windll.shell32.IsUserAnAdmin() != 0 if hasattr(ctypes.windll.shell32, "IsUserAnAdmin") else os.getuid() == 0
is_windows = lambda: True if os.name == 'nt' else False 
__BANNER__ = f""" {colorama.Fore.RED}
     _            _     
  __| | _____   _/ |___ 
 / _` |/ _ \\ \\ / / / __|
| (_| |  __/\\ V /| \\__ \\
 \\__,_|\\___| \\_/ |_|___/

            By Vahlame & uhemn
{colorama.Fore.RESET}"""

__MENU__ = """
1 - Desactivar servicios de telemetria
2 - Eliminar tareas programadas
3 - Establecer memoria de paginacion 
4 - Desactivar a cortana, noticias y anuncios
5 - Configurar CPU
6 - Todos 
7 - Salir

dev1s@windows -> """


def menu() -> None:
    opc = 0;
    while opc != 7:
       os.system("cls")
       print(__BANNER__)
       opc = int(input(__MENU__))

       


if __name__ == "__main__":
    if not is_windows():
        print("ocupas correr esto en un entorno windows")
        input("presiona enter para salir...")
        sys.exit(-1)
    elif not is_admin():
        print("ocupas administrador para correr este script")
        input("presiona enter para salir...")
        sys.exit(-1)

    menu()
    pass
