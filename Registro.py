import serial
import pandas as pd
from datetime import datetime
import os

# Ajusta este puerto al tuyo (en Windows suele ser COM3 o COM4)
arduino = serial.Serial('COM9', 9600, timeout=1)

archivo_excel = 'registros_rfid.xlsx'

# Si ya existe el Excel, lo carga; si no, lo crea vacío
if os.path.exists(archivo_excel):
    df = pd.read_excel(archivo_excel)
else:
    df = pd.DataFrame(columns=['UID', 'Usuario', 'Hora'])

print("Esperando datos desde Arduino...")

while True:
    try:
        linea = arduino.readline().decode('utf-8').strip()
        if linea:
            print("Recibido:", linea)

            if linea.startswith("UID:"):
                partes = linea.split(" - ")
                uid = partes[0].replace("UID:", "").strip()
                usuario = partes[1] if len(partes) > 1 else "Desconocido"
                hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                nuevo_registro = {'UID': uid, 'Usuario': usuario, 'Hora': hora}
                df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
                df.to_excel(archivo_excel, index=False)

                print(f"Registro guardado: {usuario} ({uid}) - {hora}")

    except KeyboardInterrupt:
        print("\nPrograma detenido manualmente.")
        break
    except Exception as e:
        print("Error:", e)