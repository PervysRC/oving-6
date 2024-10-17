import os
import matplotlib
matplotlib.use('TkAgg')  # Usa el backend TkAgg

import csv
from datetime import datetime
import matplotlib.pyplot as plt

# Función para leer datos desde el archivo de Sola (Formato específico)
def leer_datos_csv_sola(archivo):
    print(f"Intentando abrir el archivo: {archivo}")  # Imprimir la ruta que se está intentando abrir
    fechas = []
    temperaturas = []
    presiones = []
    
    if not os.path.isfile(archivo):
        print(f"Error: El archivo {archivo} no existe.")
        return fechas, temperaturas, presiones

    try:
        with open(archivo, newline='', encoding='utf-8') as csvfile:
            lector_csv = csv.reader(csvfile, delimiter=';')
            next(lector_csv)  # Saltar encabezado
            for fila in lector_csv:
                try:
                    fecha_str = fila[2]  # La fecha y hora están en la tercera columna
                    temperatura = float(fila[3].replace(',', '.'))  # Columna 4 para temperatura (Lufttemperatur)
                    presion = float(fila[4].replace(',', '.'))   # Columna 5 para presión (Lufttrykk i havnivå)
                    
                    # Parsear la fecha según el formato DD.MM.AAAA HH:MM
                    fecha = datetime.strptime(fecha_str, '%d.%m.%Y %H:%M')
                    
                    fechas.append(fecha)
                    temperaturas.append(temperatura)
                    presiones.append(presion)
                except (ValueError, IndexError):
                    continue  # Saltar líneas que no se puedan leer
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo}. Asegúrate de que la ruta sea correcta.")
    
    return fechas, temperaturas, presiones

# Función para leer datos desde el archivo de la estación local (Formato específico)
def leer_datos_csv_local(archivo):
    print(f"Intentando abrir el archivo: {archivo}")  # Imprimir la ruta que se está intentando abrir
    fechas = []
    temperaturas = []
    presiones = []
    
    if not os.path.isfile(archivo):
        print(f"Error: El archivo {archivo} no existe.")
        return fechas, temperaturas, presiones

    try:
        with open(archivo, newline='', encoding='utf-8') as csvfile:
            lector_csv = csv.reader(csvfile, delimiter=';')
            next(lector_csv)  # Saltar encabezado
            for fila in lector_csv:
                try:
                    fecha_str = fila[0]  # La fecha y hora están en la primera columna
                    temperatura = float(fila[4].replace(',', '.'))   # Columna 5 para temperatura
                    presion = float(fila[2].replace(',', '.')) * 10 # Columna 3 para presión (bar a hPa)
                    
                    # Parsear la fecha según el formato MM.DD.AAAA HH:MM
                    fecha = datetime.strptime(fecha_str, '%m.%d.%Y %H:%M')
                    
                    fechas.append(fecha)
                    temperaturas.append(temperatura)
                    presiones.append(presion)
                except (ValueError, IndexError):
                    continue  # Saltar líneas que no se puedan leer
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo}. Asegúrate de que la ruta sea correcta.")
    
    return fechas, temperaturas, presiones

# Rutas a los archivos
ruta_sola = r'C:\Users\pervy\OneDrive\Escritorio\prgrmacion\DAT120\oving 6\local_station.csv\temperatur_trykk_met_samme_rune_time_datasett.csv.txt'
ruta_local = r'C:\Users\pervy\OneDrive\Escritorio\prgrmacion\DAT120\oving 6\local_station.csv\trykk_og_temperaturlogg_rune_time.csv.txt'

# Cargar datos de la estación Sola
fechas_sola, temp_sola, pres_sola = leer_datos_csv_sola(ruta_sola)

# Cargar datos de la estación local
fechas_local, temp_local, pres_local = leer_datos_csv_local(ruta_local)

# Verificar si se cargaron los datos correctamente
if not fechas_sola or not fechas_local:
    print("No se pudieron cargar los datos. Por favor, verifica las rutas de los archivos.")
else:
    # Imprimir los datos para verificar que se hayan cargado correctamente
    print("Fechas Sola:", fechas_sola)
    print("Temperaturas Sola:", temp_sola)
    print("Presiones Sola:", pres_sola)

    print("Fechas Local:", fechas_local)
    print("Temperaturas Local:", temp_local)
    print("Presiones Local:", pres_local)

    # Establecer un estilo para la gráfica
    plt.style.use('ggplot')  # Cambia esto a un estilo disponible en tu instalación

    # Crear subplots para tener dos gráficos en una misma ventana
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))  # Dos gráficos, uno encima del otro

    # Graficar temperaturas en el primer gráfico (ax1)
    ax1.plot(fechas_sola, temp_sola, label='Temperatura Sola', color='blue', linewidth=2, marker='o', markersize=5)
    ax1.plot(fechas_local, temp_local, label='Temperatura Local', color='green', linewidth=2, marker='s', markersize=5)
    ax1.set_xlabel('Fecha y Hora', fontsize=14)
    ax1.set_ylabel('Temperatura (°C)', fontsize=14)
    ax1.set_title('Comparativa de Temperatura - Estación Sola vs Local', fontsize=16)
    ax1.legend(loc='upper left')
    ax1.grid(True)
    ax1.set_xticklabels(fechas_sola, rotation=45)

    # Graficar presiones en el segundo gráfico (ax2)
    ax2.plot(fechas_sola, pres_sola, label='Presión Sola', color='red', linewidth=2, marker='o', markersize=5)
    ax2.plot(fechas_local, pres_local, label='Presión Local', color='brown', linewidth=2, marker='s', markersize=5)
    ax2.set_xlabel('Fecha y Hora', fontsize=14)
    ax2.set_ylabel('Presión Atmosférica (hPa)', fontsize=14)
    ax2.set_title('Comparativa de Presión - Estación Sola vs Local', fontsize=16)
    ax2.legend(loc='upper left')
    ax2.grid(True)
    
    """ax2.set_xlim([min(fechas_sola + fechas_local), max(fechas_sola + fechas_local)])  # Limitar el tiempo a los datos disponibles
    ax2.set_ylim([min(min(pres_sola), min(pres_local)) * 0.98, max(max(pres_sola), max(pres_local)) *1.02])  # Ajustar los valores de presión para que no sean tan grandes"""
    
    
    ax2.set_xticklabels(fechas_sola, rotation=45)

    # Ajustar el layout para evitar superposición
    plt.tight_layout()
    plt.show()
