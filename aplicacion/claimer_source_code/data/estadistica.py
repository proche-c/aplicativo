    
import pandas as pd
from data.build import *
from data.out import *
from errores.errores import *
from tkinter import messagebox
import os

 
def estadistica(path, root):
    """
    Función que estructura y dirige la creación de una serie de data frames
    a partir de un archivo excel con información de la BBDD.
    Crea otron archivo excel que consta de dos hojas:
        - La primera muestra de forma clara, visual y formateada los datos de entrada
        procesados
        - La segunda muestra, también de forma clara y formateada una serie de datos 
        estadísticos obtenidos a partir de los datos de entrada. Por un lado muestra datos
        relevantes comercialmente, ya que reflejan qué productos resultan más rentables para 
        la correduría. Y por otro, resalta de manera visual las discrepancias entre la 
        información obtenida a partir de los datos de los recibos y la introducida manualmente 
        en Elevia referente a las comisiones de los productos
    """
    pd.options.mode.chained_assignment = None  # default='warn'

    edf = 0
    try:
        df = create_df_est(path) # Crea el data frame
    except Exception as e:
        tipo = type(e).__name__
        print("Error 40: " + tipo)
        e_40 = Error(tipo, "40")
        msg = "Error 40: " + tipo + ": " + e_40.msg_1 + e_40.msg_2
        messagebox.showinfo(message=msg, title="Warning", parent=root)
    else:
        edf = 1
    
    prod = 0
    if edf == 1:
        try:
            list_prod = create_list_prod(df) # Crea lista con la información de los productos
        except Exception as e:
            tipo = type(e).__name__
            print("Error 41: " + tipo)
            e_41 = Error(tipo, "41")
            msg = "Error 41: " + tipo + ": " + e_41.msg_1 + e_41.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            prod = 1
    
    comp = 0
    if prod == 1:
        try:
            complete_df(list_prod, df)  # Cálcula los campos que se añaden al data frame
        except Exception as e:
            tipo = type(e).__name__
            print("Error 42: " + tipo)
            e_42 = Error(tipo, "42")
            msg = "Error 42: " + tipo + ": " + e_42.msg_1 + e_42.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            comp = 1

    df_data = []
    daf = 0
    if comp == 1:
        try:
            # Se define la estructura de la tabla de datos a mostrar
            df_datos = df[['indice', 'Compañía', 'Producto', 'Prima neta', 'Com. prima neta', 
                'Com. correduría', 'Com. prima neta %', 'Com. correduría %', 'Sobrecomisión %', 'Com. año 1', 
                'Com. año 2', 'Com. año 3', 'Com. año 4', 'Com. año 5']]
            # Crea los data frame a exportar y los almacena un una lista
            df_data.append(df_datos)
            df1, df2, df3 = get_df_estadistica(df_datos, list_prod)
            df_data.append(df1)
            df_data.append(df2)
            df_data.append(df3)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 43: " + tipo)
            e_43 = Error(tipo, "43")
            msg = "Error 43: " + tipo + ": " + e_43.msg_1 + e_43.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            daf = 1

    path_est = "files/estadistica.xlsx"
    if daf == 1:
        try:
            writer = pd.ExcelWriter(path_est, engine='xlsxwriter')
            # Exporta a excel el data frame de los datos y le da formato
            exportar_datos(df_datos, writer, "Datos")
            # Exporta a excel el data frame de los datos estadísticos y le da formato 
            exportar_estadistica(df1, df2, df3, writer, "Resumen estadistico")
            writer.close()
        except Exception as e:
            tipo = type(e).__name__
            print("Error 44: " + tipo)
            e_44 = Error(tipo, "44")
            msg = "Error 44: " + tipo + ": " + e_44.msg_1 + e_44.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)

    return df_data
