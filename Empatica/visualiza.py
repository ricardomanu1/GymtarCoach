from datetime import datetime
import os
import csv
import matplotlib.pyplot as plt

def read_file(file):
    data = []
    with open(file, 'r') as archivo:
        lector_csv = csv.DictReader(archivo)
        for row in lector_csv:
            data.append(row)
    return data

def line_graph(file_name,title,y_parameter,y_label,start,end,data_serial):
    data = read_file(file_name)
    x = []
    y = []
    # Procesar los datos y almacenar los valores en las listas correspondientes
    for row in data:
        timestamp_iso = row['timestamp_iso']
        date = datetime.strptime(timestamp_iso, "%Y-%m-%dT%H:%M:%SZ")
        hour = date.hour + 2
        minute = date.minute
        y_data = row[y_parameter]
        if row['missing_value_reason'] != 'device_not_recording' and y_data:
            if hour >= start and hour <= end:
                x.append(hour + minute / 60)
                y.append(float(y_data))

    # Crear el gráfico de líneas
    fig, ax = plt.subplots()
    ax.step(x, y)

    # Configurar etiquetas y título del gráfico
    ax.set_title(title)
    ax.set_xlabel('Time (hours)')
    ax.set_ylabel(y_label)
    ax.set_xlim(start,end)
    ax.set_ylim(min(y)-1,max(y)+1)

    ruta_carpeta = 'Empatica/' +  data_serial + 'graph'

    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)

    fig.savefig(ruta_carpeta + '/' + title + '.png')

def Rutine_graph(id_serial,date,start,end):
    data_serial = id_serial + '_' + date + '_'

    ## Ratio de pulsaciones
    file_name = data_serial + 'pulse-rate.csv'
    y_parameter = 'pulse_rate_bpm'
    title = 'Ratio de pulsaciones 21-06-2023'
    y_label = 'BPM'
    line_graph(file_name,title,y_parameter,y_label,start,end,data_serial)

    ## Temperatura
    file_name = data_serial + 'temperature.csv'
    y_parameter = 'temperature_celsius'
    title = 'Temperatura Cº 21-06-2023'
    y_label = 'Celsius'
    line_graph(file_name,title,y_parameter,y_label,start,end,data_serial)

    ## EDA
    file_name =data_serial + 'eda.csv'
    y_parameter = 'eda_scl_usiemens'
    title = 'Respuesta galvánica de la piel 21-06-2023'
    y_label = 'EDA'
    line_graph(file_name,title,y_parameter,y_label,start,end,data_serial)

Rutine_graph('1-1-01','2023-06-21',12,14)