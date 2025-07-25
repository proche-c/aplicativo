"""
Este módulo contiene las funciones que obtienen los datos necesarios para clasificar los 
registros y las funciones que guardan una copia temporal de los resultados obtenidos
"""

from getter.input import *
from getter.exexcel import *
from errores.errores import *
from data.out import *
from tkinter import filedialog
from tkinter import messagebox


def get_desv(df, anomaly):
    """
    Ajusta los indices del data frama tras una separación y calcula la diferencia 
    entre la comisión que se debería haber cobrado de acuerdo a las condiciones 
    del producto y la póliza y la que se ha cobrado.
    Toma como parametros de entrada:
        - df: data frame de recibos a procesar
        - anomaly: este parámetro indica si las pólizas tienen una casúistica especial.
        Su valor es 0, si la póliza no presenta anomalías; 1, si se trata de una 
        póliza emitida con clave cosesa y cuyo recibo ya fue reclamado; 2, si se ha 
        pactado una comisión reducida en esa póliza
    """
    fix_index(df)
    get_dif(df, anomaly)


def get_dif(df_recibos, anomaly):
    """
    Calcula la diferencia 
    entre la comisión que se debería haber cobrado de acuerdo a las condiciones 
    del producto y la póliza y la que se ha cobrado.
    Toma como parametros de entrada:
        - df: data frame de recibos a procesar
        - anomaly: este parámetro indica si las pólizas tienen una casúistica especial.
        Su valor es 0, si la póliza no presenta anomalías; 1, si se trata de una 
        póliza emitida con clave cosesa y cuyo recibo ya fue reclamado; 2, si se ha 
        pactado una comisión reducida en esa póliza
    """
    df_recibos['Diferencia'] = 0.00
    for i in range(len(df_recibos)):
        if anomaly == 0:
            df_recibos['Diferencia'][i] = df_recibos['com_teorica'][i] - df_recibos['Comisión correduría'][i]
        elif anomaly == 1:
            df_recibos['Diferencia'][i] = df_recibos['com_teorica'][i] - df_recibos['com. cosesa'][i] * df_recibos['Prima neta'][i]
        elif anomaly == 2:
            df_recibos['Diferencia'][i] = df_recibos['com_teorica'][i] * df_recibos['com. red'][i] - df_recibos['Comisión correduría'][i]


def save_r_1(dfs):
    """Guarda una copia del archivo excel 'Resultado' en la ruta que el usuario indica"""
    idir = 'files'
    your_file = filedialog.asksaveasfilename(initialdir=idir, defaultextension='xlsx')  # Me devuelve la ruta absoluta
    try:
        if len(dfs) == 5:
            writer = pd.ExcelWriter(your_file, engine='xlsxwriter')
            exportar_resultado(dfs[0], writer, "Normales", 0)
            exportar_resultado(dfs[1], writer, "Fraccionadas", 0)
            exportar_resultado(dfs[2], writer, "Comision reducida", 1)
            exportar_resultado(dfs[3], writer, "Cosesa", 3)
            writer.close()
        elif len(dfs) == 4:
            writer = pd.ExcelWriter(your_file, engine='xlsxwriter')
            exportar_resultado(dfs[0], writer, "Normales", 0)
            exportar_resultado(dfs[1], writer, "Fraccionadas", 0)
            exportar_resultado(dfs[2], writer, "Comision reducida", 1)
            writer.close()
    except Exception as e:
        tipo = type(e).__name__
        print("Error 30: " + tipo)
        e_30 = Error(tipo, "30")
        msg = "Error 30: " + tipo + ": " + e_30.msg_1 + e_30.msg_2
        messagebox.showinfo(message=msg, title="Warning")
    finally:
        return your_file


def save_r_2(dfs):
    """
    Guarda una copia del archivo excel 'Correctos' en la ruta que el usuario indica
    """
    idir = 'files'
    your_file = filedialog.asksaveasfilename(initialdir=idir, defaultextension='xlsx')
    try:
        if len(dfs) == 5:
            writer = pd.ExcelWriter(your_file, engine='xlsxwriter')
            exportar_resultado(dfs[4], writer, "Correctos", 4)
            writer.close()
        elif len(dfs) == 4:
            writer = pd.ExcelWriter(your_file, engine='xlsxwriter')
            exportar_resultado(dfs[3], writer, "Correctos", 2)
            writer.close()
    except Exception as e:
        tipo = type(e).__name__
        print("Error 31: " + tipo)
        e_31 = Error(tipo, "31")
        msg = "Error 31: " + tipo + ": " + e_31.msg_1 + e_31.msg_2
        messagebox.showinfo(message=msg, title="Warning")
    finally:
        return your_file
    

def save_est(df_data):
    """
    Guarda una copia del archivo excel 'Estadistica' en la ruta que el usuario indica
    """
    idir = 'files'
    your_file_e = filedialog.asksaveasfilename(initialdir=idir, defaultextension='xlsx')
    try:  
        writer = pd.ExcelWriter(your_file_e, engine='xlsxwriter')
        exportar_datos(df_data[0], writer, "Datos")
        exportar_estadistica(df_data[1], df_data[2], df_data[3], writer, "Resumen estadistico")
        writer.close()
    except Exception as e:
        tipo = type(e).__name__
        print("Error 32: " + tipo)
        e_32 = Error(tipo, "32")
        msg = "Error 32: " + tipo + ": " + e_32.msg_1 + e_32.msg_2
        messagebox.showinfo(message=msg, title="Warning")
    finally:
        return your_file_e