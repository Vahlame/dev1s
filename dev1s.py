import subprocess
import re
import os 
import sys 
import winreg

if os.name != 'nt':
    print("solo windows soportado")
    sys.exit(-1)

a = " SE NECESITA CORRER-EJECUTAR COMO ADMINISTRADOR mediante elpresente mensaje se le informa el siguiente script desactivara varios servicios de windows con tal de mejorar el rendimiento de su PC,entre los cuales va incluido en su totalidad la telemtria y servicios obsoletos para hoy dia, al escribir (SI) "
def politicas_y_terminos(aceptacion):
    if (aceptacion == "SI" ):
       print("ha aceptado los terminos, el script se ejecutara enseguida")
       
    else:
        print("no ha aceptado los terminos el script se cerrara y no se ejecutara")        
choice = input(a)
politicas_y_terminos(choice)

def disable_windows_defender():
    try:
        registry_path = r"SOFTWARE\Policies\Microsoft\Windows Defender"
        key_handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, registry_path, 0, winreg.KEY_SET_VALUE)
        value_name = "DisableAntiSpyware"
        value_data = 1
        winreg.SetValueEx(key_handle, value_name, 0, winreg.REG_DWORD, value_data)
        winreg.CloseKey(key_handle)
        print("Windows Defender ha sido desactivado correctamente.")
    except Exception as e:
        print(f"Error al desactivar Windows Defender: {e}")
disable_windows_defender()

def Servicios_telemetria ():
      Commands = [
        "sc stop XboxNetApiSvc >nul & sc config XboxNetApiSvc start=disabled",
        "sc stop XblGameSave >nul & sc config XblGameSave start=disabled",
        "sc stop XblAuthManager >nul & sc config XblAuthManager start=disabled",
        "sc stop XboxGipSvc >nul & sc config XboxGipSvc start=disabled",
        "reg add \"HKLM\\System\\CurrentControlSet\\Services\\WpnUserService\" /v \"Start\" /t REG_DWORD /d \"4\" /f",
        "sc stop Spectrum >nul & sc config Spectrum start=disabled",
        "sc stop MixedRealityOpenXRSvc >nul & sc config MixedRealityOpenXRSvc start=disabled",
        "sc stop WbioSrvc >nul & sc config WbioSrvc start=disabled",
        "sc config TokenBroker start= disabled",
        "sc config WalletService start= disabled",
        "sc config SensorService start= disabled",
        "sc config TroubleshootingSvc start= disabled",
        "sc config PcaSvc start= disabled",
        "sc config wercplsupport start= disabled",
        "sc config PhoneSvc start= disabled",
        "sc config WpcMonSvc start= disabled",
        "sc config uhssvc start= disabled",
        "sc config ClickToRunSvc start= disabled",
        "sc config edgeupdatem start= disabled",
        "sc config edgeupdate start= disabled",
        "sc config MicrosoftEdgeElevationService start= disabled",
        "sc config diagnosticshub.standardcollector.service start= disabled",
        "sc config gupdatem start= disabled",
        "sc config gupdate start= disabled",
        "sc config GoogleChromeElevationService start= disabled",
        "sc config MapsBroker start= disabled",
        "sc config Fax start= disabled",
        "sc config BcastDVRUserService_5be19 start= disabled",
        "sc config BcastDVRUserService_10c515 start= disabled",
        "sc config lfsvc start= disabled",
        "sc config GoogleChromeElevationService start= disabled",
        "net stop HomeGroupListener",
        "sc config HomeGroupListener start= disabled",
        "net stop HomeGroupProvider",
        "sc config HomeGroupProvider start= disabled",
        "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\StorageSense\\Parameters\\StoragePolicy\" /v \"01\" /t REG_DWORD /d \"0\" /f"
     ]
      co = 0
      for Command in Commands:
        result = subprocess.run(['powershell', Command], shell=True, capture_output=True, text=True)
        print(result.stdout)
        co = co + 1
        if(co < 35):
            print (f"parte {str(co)} de 35")
        else:
            print("listo")
Servicios_telemetria ()
print("fase 1 lista")

def eliminar_tareas_programadas():
      comando_eliminar_tareas = "schtasks /delete /tn * /f"
    
      try:
        subprocess.run(['powershell',comando_eliminar_tareas], shell=True, capture_output=True, text=True, check=True)
        print("Todas las tareas programadas han sido eliminadas.")
      except subprocess.CalledProcessError as e:
        print(f"Error al eliminar las tareas programadas: {str(e)}")
eliminar_tareas_programadas()
print("fase 2 lista")

def desactivar_cortana_noticias_anuncios():
      comandos = [
        "reg add \"HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Search\" /v \"AllowCortana\" /t REG_DWORD /d 0 /f",
        "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Feeds\" /v \"ShellFeedsTaskbarViewMode\" /t REG_DWORD /d 2 /f",
        "reg add \"HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\AdvertisingInfo\" /v \"Enabled\" /t REG_DWORD /d 0 /f"
     ]
    
      for comando in comandos:
        try:
            subprocess.run(['powershell',comando], shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando '{comando}': {str(e)}")
desactivar_cortana_noticias_anuncios()
print("fase 3 lista")

def establecer_memoria_paginacion():
    
       comando_ram = 'wmic MemoryChip get Capacity'
    
       try:
        resultado = subprocess.run(['powershell',comando_ram], shell=True, check=True, capture_output=True, text=True)
        total_ram_gb = sum(int(mo.group()) for mo in re.finditer(r'\d+', resultado.stdout)) // (1024**3)
        print(f"Tu sistema tiene {total_ram_gb} GB de RAM.")
        
        x = total_ram_gb
        comando_paginacion = f'wmic pagefileset where name="C:\\\\pagefile.sys" set InitialSize={1500},MaximumSize={1024*x}'
        subprocess.run(comando_paginacion, shell=True, check=True)
        print(f"El tamaño de la memoria de paginación se ha establecido a 1024-{1024*x}.")
       except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar los comandos: {str(e)}")
establecer_memoria_paginacion()
print("fase 4 lista")

def configurar_cpu_antivirus():
      comandos = [
        "Get-MpPreference | Select ScanAvgCPULoadFactor",
        "Set-MpPreference -ScanAvgCPULoadFactor 10",
        "gpupdate /force"
     ]
    
      for comando in comandos:
        try:
            subprocess.run(["powershell", "-Command", comando], shell=True, capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error al ejecutar el comando '{comando}': {str(e)}")
configurar_cpu_antivirus()
print("fase 5 lista")

print("listo, se puede cerrar")
