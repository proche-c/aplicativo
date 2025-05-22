from builder.fraccionada import *
from getter.input import *
from getter.output import *
from tkinter import messagebox
import os

def reclamar(path, desv, referencia, root):
    """
    Función que crea los data frames que contienen la información de los
    recibos procesados, los clasifica, calcula las desvíaciones y determina
    si están correctamente pagados
    Toma como parámetros:
    - path: ruta en la que se encuentra el archivo a procesar
    - desv: desviación a partir de la que se consideran los recibos erróneos
    - referencia: obtiene un parámetro introducido por el usuario y que indica cómo se han de consideran las pólizas por las que se
    percibe una comisión por debajo de la comisión por tabla pero no se tiene la certeza de que s ehaya pactado una
    comisión reducida.
    - Si su valor es 1, se considerará que la póliza tiene la comisión que se indica en la tabla de comisiones
    - Si su valor es 0, se considerará que las pólizas tienen pactada una comisión reducida y por lo tanto, el 
    recibo es correcto
    """
    pd.options.mode.chained_assignment = None  # default='warn'
    result = 0
    claim = 0
    try:
        df = create_df(path, 1) # creo df principal
    except Exception as e:
        tipo = type(e).__name__
        print("Error 10: " + tipo)
        e_10 = Error(tipo, "10")
        msg = "Error 10: " + tipo + ": " + e_10.msg_1 + e_10.msg_2
        messagebox.showinfo(message=msg, title="Warning", parent=root)
    else:
        claim = 1
    
    delcol = 0
    if claim == 1:
        try:
            eliminar_columnas(df)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 11: " + tipo)
            e_11 = Error(tipo, "11")
            msg = "Error 11: " + tipo + ": " + e_11.msg_1 + e_11.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            delcol = 1

    val = 0
    if delcol == 1:
        try:
            for i in range(len(df)):
                try:
                    df['Prima neta'][i] = float(df['Prima neta'][i])
                except ValueError:
                    df['Prima neta'][i] = 0
                try:
                    df['Comisión prima neta'][i] = float(df['Comisión prima neta'][i])
                except ValueError:
                    df['Comisión prima neta'][i] = 0
                try:
                    df['Comisión correduría'][i] = float(df['Comisión correduría'][i])
                except ValueError:
                    df['Comisión correduría'][i] = 0
            df['Prima neta'] = df['Prima neta'].astype(float)
            df['Comisión prima neta'] = df['Comisión prima neta'].astype(float)
            df['Comisión correduría'] = df['Comisión correduría'].astype(float)
            df['Prima neta'].fillna(0)
            df['Comisión prima neta'].fillna(0)
            df['Comisión correduría'].fillna(0)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 12: " + tipo)
            e_12 = Error(tipo, "12")
            msg = "Error 12: " + tipo + ": " + e_12.msg_1 + e_12.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            val = 1

    fracc = 0
    if val == 1:
        try:
            get_prima_fraccionada(df)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 13: " + tipo)
            e_13 = Error(tipo, "13")
            msg = "Error 13: " + tipo + ": " + e_13.msg_1 + e_13.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            fracc = 1
   
    length = [] # Creo una lista para guardar las length
    zmp = 0
    if fracc == 1:
        try:
            get_com(df) # Calculo com a aplicar en % y com teorica a cobrar en Euros
            length1 = len(df)
            length.append(length1)
            length2 = 0
            length.append(length2)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 14: " + tipo)
            e_14 = Error(tipo, "14")
            msg = "Error 14: " + tipo + ": " + e_14.msg_1 + e_14.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            zmp = 1

    red = 0
    if zmp == 1:
        try: # Separo los que tienen com reducida
            df_rec_a = df[df['Comision reducida'].isnull()==False]
            df_rec_r = df[df['Comision reducida'].isnull()==True]
            length3 = len(df_rec_a)
            length.append(length3)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 15: " + tipo)
            e_15 = Error(tipo, "15")
            msg = "Error 15: " + tipo + ": " + e_15.msg_1 + e_15.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            red = 1

    fc = 0
    if red == 1:
        try: # Separo las polizas fraccionadas
            df_rec_fr = df_rec_r[df_rec_r['is_fraccionada_zurich'] == 1]
            df_rec_n = df_rec_r[df_rec_r['is_fraccionada_zurich'] == 0]
            length4 = len(df_rec_n)
            length5 = len(df_rec_fr)
            length.append(length4)
            length.append(length5)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 16: " + tipo)
            e_16 = Error(tipo, "16")
            msg = "Error 16: " + tipo + ": " + e_16.msg_1 + e_16.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            fc = 1

    cred = 0
    if fc == 1:
        try: # calculo la comision reducida en porcentaje
            fix_index(df_rec_a)
            get_comision_r(df_rec_a)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 17: " + tipo)
            e_17 = Error(tipo, "16")
            msg = "Error 17: " + tipo + ": " + e_17.msg_1 + e_17.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            cred = 1

    diff = 0
    if cred == 1:
        try: # calculo la desv entre com teorica y cobrada
            get_desv(df_rec_n, anomaly = 0)
            get_desv(df_rec_fr, anomaly = 0)
            get_desv(df_rec_a, anomaly = 2)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 18: " + tipo)
            e_18 = Error(tipo, "18")
            msg = "Error 18: " + tipo + ": " + e_18.msg_1 + e_18.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            diff = 1

    # Y calculo los que estan mal pagados de cada uno de los df (normales y com. reducida)
    deb_1 = 0
    if diff == 1:
        try: # calculo los que estan mal pagados de los recibos normales y separo
            df_rec_ok1 = df_rec_n[(df_rec_n['com_teorica'] - df_rec_n['Comisión correduría']) <= desv]
            df_rec_e = df_rec_n[(df_rec_n['com_teorica'] - df_rec_n['Comisión correduría']) > desv]
            df_rec_ok2 = df_rec_fr[(df_rec_fr['com_teorica'] - df_rec_fr['Comisión correduría']) <= desv]
            df_rec_f = df_rec_fr[(df_rec_fr['com_teorica'] - df_rec_fr['Comisión correduría']) > desv]
            length6 = len(df_rec_e)
            length.append(length6)
            length7 = len(df_rec_f)
            length.append(length7)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 19: " + tipo)
            e_19 = Error(tipo, "19")
            msg = "Error 19: " + tipo + ": " + e_19.msg_1 + e_19.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            deb_1 = 1

    deb_2 = 0
    if deb_1 == 1:
        try: # calculo los que estan mal pagados de los recibos con comision reducida y separo
            if referencia == 1:
                df_rec_ok3 = df_rec_a[(df_rec_a['com_teorica'] * df_rec_a['com. red'] - df_rec_a['Comisión correduría']) <= desv]
                df_rec_a = df_rec_a[(df_rec_a['com_teorica'] * df_rec_a['com. red'] - df_rec_a['Comisión correduría']) > desv]
            elif referencia != 1:
                df_rec_ok3 = df_rec_a[(df_rec_a['Comision reducida'] == 'Referencia')]
                df_rec_a = df_rec_a[(df_rec_a['Comision reducida'] != 'Referencia')]
                df_rec_ok4 = df_rec_a[((df_rec_a['com_teorica'] * df_rec_a['com. red'] - df_rec_a['Comisión correduría']) <= desv)]
                df_rec_a = df_rec_a[(df_rec_a['com_teorica'] * df_rec_a['com. red'] - df_rec_a['Comisión correduría']) > desv]
            length8 = 0
            length.append(length8)
            length9 = len(df_rec_a)
            length.append(length9)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 110: " + tipo)
            e_110 = Error(tipo, "110")
            msg = "Error 110: " + tipo + ": " + e_110.msg_1 + e_110.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            deb_2 = 1

    suma = [] # Creo una lista para meter las cantidades a regularizar
    sum = 0
    if deb_2 == 1:
        try: # calculo la cantidades a regularizar y las meto en una lista
            suma_c = 0
            suma_a = df_rec_a['Diferencia'].sum()
            suma_f = df_rec_f['Diferencia'].sum()
            suma_e = df_rec_e['Diferencia'].sum()
            suma.append(suma_e)
            suma.append(suma_f)
            suma.append(suma_a)
            suma.append(suma_c)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 111: " + tipo)
            e_111 = Error(tipo, "111")
            msg = "Error 111: " + tipo + ": " + e_111.msg_1 + e_111.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            sum = 1

    corr = 0
    if sum == 1:
        try:
            if referencia == 1: # junto los df de los recibos pagados correctamente
                df_rec_ok = pd.concat([df_rec_ok1, df_rec_ok3, df_rec_ok2])
            else:
                df_rec_ok = pd.concat([df_rec_ok1, df_rec_ok3, df_rec_ok4, df_rec_ok2])
        except Exception as e:
            tipo = type(e).__name__
            print("Error 112: " + tipo)
            e_112 = Error(tipo, "112")
            msg = "Error 112: " + tipo + ": " + e_112.msg_1 + e_112.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            corr = 1

    if corr == 1:
        try:  # Arreglo las fechas para que se muestren bien en el excel   
            df_rec_e['Poliza.FechaPrimerEfecto'] = df_rec_e['Poliza.FechaPrimerEfecto'].astype(str)
            df_rec_e['Fecha efecto'] = df_rec_e['Fecha efecto'].astype(str)
            df_rec_f['Poliza.FechaPrimerEfecto'] = df_rec_f['Poliza.FechaPrimerEfecto'].astype(str)
            df_rec_f['Fecha efecto'] = df_rec_f['Fecha efecto'].astype(str)
            df_rec_a['Poliza.FechaPrimerEfecto'] = df_rec_a['Poliza.FechaPrimerEfecto'].astype(str)
            df_rec_a['Fecha efecto'] = df_rec_a['Fecha efecto'].astype(str)
            df_rec_ok['Poliza.FechaPrimerEfecto'] = df_rec_ok['Poliza.FechaPrimerEfecto'].astype(str)
            df_rec_ok['Fecha efecto'] = df_rec_ok['Fecha efecto'].astype(str)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 113: " + tipo)
            e_113 = Error(tipo, "113")
            msg = "Error 113: " + tipo + ": " + e_113.msg_1 + e_113.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)

    paths = []  # Creo una lista para devolver las rutas de los archivos creados
    path1 = "files/erroneos.xlsx"
    path2 = "files/correctos.xlsx"
    paths.append(path1)
    paths.append(path2)

    adj = 0
    if corr == 1:
        try: # elimina las columnas que no se necesita mostrar
            col = ['Compañía', 'Producto', 'F. primer efecto', 'Nº de póliza', 
                       'Nº de recibo', 'Prima neta', 'Com. prima neta', 'Com. correduría', 
                       'F. de efecto', 'Situación', 'Estado', 'Com. año 1', 'Com. año 2', 
                       'Com. año 3', 'Com. año 4', 'Com. año 5', 'Forma de pago', 'Com. año 6', 
                       'Com. a aplicar', 'Com. teórica', 'Desviación']
            col_r = ['Compañía', 'Producto', 'F. primer efecto', 'Nº de póliza', 
                       'Nº de recibo', 'Prima neta', 'Com. prima neta', 'Com. correduría', 
                       'F. de efecto', 'Situación', 'Estado', 'Com. año 1', 'Com. año 2', 
                       'Com. año 3', 'Com. año 4', 'Com. año 5', 'Forma de pago', 'Com. año 6', 
                       'Com. a aplicar', 'Com. teórica', 'Com. reducida', 'Desviación']
            col_c = ['Compañía', 'Producto', 'F. primer efecto', 'Nº de póliza', 
                       'Nº de recibo', 'Prima neta', 'Com. prima neta', 'Com. correduría', 
                       'F. de efecto', 'Situación', 'Estado', 'Com. año 1', 'Com. año 2', 
                       'Com. año 3', 'Com. año 4', 'Com. año 5', 'Forma de pago', 'Com. año 6', 
                       'Com. a aplicar', 'Com. teórica', 'Desviación',  'Com. reducida']
            fix_columns(df_rec_e, col)
            fix_columns(df_rec_f, col)
            fix_columns(df_rec_a, col_r)
            fix_columns(df_rec_ok, col_c)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 114: " + tipo)
            e_114 = Error(tipo, "114")
            msg = "Error 114: " + tipo + ": " + e_114.msg_1 + e_114.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            adj = 1

    dfs = [] # Creo una lista para devolcer los dfs resultado
    dfl = 0
    if adj == 1:
        try:
            dfs.append(df_rec_e)
            dfs.append(df_rec_f)
            dfs.append(df_rec_a)
            dfs.append(df_rec_ok)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 115: " + tipo)
            e_115 = Error(tipo, "115")
            msg = "Error 115: " + tipo + ": " + e_115.msg_1 + e_115.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            dfl = 1

    if dfl == 1:
        try: # exporto el resultado a hojas de excel
            writer = pd.ExcelWriter(path1, engine='xlsxwriter')
            exportar_resultado(df_rec_e, writer, "Normales", 0)
            exportar_resultado(df_rec_f, writer, "Fraccionadas", 0)
            exportar_resultado(df_rec_a, writer, "Comision reducida", 1)
            writer.close()
            writer = pd.ExcelWriter(path2, engine='xlsxwriter')
            exportar_resultado(df_rec_ok, writer, "Correctos", 2)
            writer.close()
        except Exception as e:
            tipo = type(e).__name__
            print("Error 116: " + tipo)
            e_116 = Error(tipo, "116")
            msg = "Error 116: " + tipo + ": " + e_116.msg_1 + e_116.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            result = 1

    return (length, suma, dfs, result)