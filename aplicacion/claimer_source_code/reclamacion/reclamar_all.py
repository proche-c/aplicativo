from builder.fraccionada import *
from getter.input import *
from getter.output import *
from tkinter import messagebox
import os

def reclamar_all(path, path_cosesa, desv, referencia, root):
    """
    Función que crea los data frames que contienen la información de los
    recibos procesados, los clasifica, calcula las desvíaciones y determina
    si están correctamente pagados
    Toma como parámetros:
    - path: ruta en la que se encuentra el archivo a procesar
    - path_cosesa: ruta en la que se encuentra el archivo con los recibos reclamados de cosesa
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
    cos = 0
    try:
        df = create_df(path, 1) # creo df principal
    except Exception as e:
        tipo = type(e).__name__
        print("Error 20: " + tipo)
        e_20 = Error(tipo, "20")
        msg = "Error 20: " + tipo + ": " + e_20.msg_1 + e_20.msg_2
        messagebox.showinfo(message=msg, title="Warning", parent=root)
    else:
        claim = 1

    delcol = 0
    if claim == 1:
        try:
            eliminar_columnas(df)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 21: " + tipo)
            e_21 = Error(tipo, "21")
            msg = "Error 21: " + tipo + ": " + e_21.msg_1 + e_21.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            delcol = 1

    if delcol == 1:
        try:
            df_cosesa = create_df(path_cosesa, 0) # creo df de rec reclamados
        except Exception as e:
            tipo = type(e).__name__
            print("Error 22: " + tipo)
            e_22 = Error(tipo, "22")
            msg = "Error 22: " + tipo + ": " + e_22.msg_1 + e_22.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            cos = 1

    lista = 0
    if claim == 1 and cos == 1:
        try:
            cosesa = [] # Creo lista
            build_cosesa(df_cosesa, cosesa) # Y le añado num rec cosesa y com reclamada
        except Exception as e:
            tipo = type(e).__name__
            print("Error 23: " + tipo)
            e_23 = Error(tipo, "23")
            msg = "Error 23: " + tipo + ": " + e_23.msg_1 + e_23.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            lista = 1
   
    claim = 0
    if lista == 1:
        try:
            add_is_cosesa(df, cosesa) # Añado informacion al df ppal
        except Exception as e:
            tipo = type(e).__name__
            print("Error 24: " + tipo)
            e_24 = Error(tipo, "24")
            msg = "Error 24: " + tipo + ": " + e_24.msg_1 + e_24.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            claim = 1

    val = 0
    if claim == 1:
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
            print("Error 25: " + tipo)
            e_25 = Error(tipo, "25")
            msg = "Error 25: " + tipo + ": " + e_25.msg_1 + e_25.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            val = 1

    fracc = 0
    if val == 1:
        try:
            get_prima_fraccionada(df)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 26: " + tipo)
            e_26 = Error(tipo, "26")
            msg = "Error 26: " + tipo + ": " + e_26.msg_1 + e_26.msg_2
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
        except Exception as e:
            tipo = type(e).__name__
            print("Error 27: " + tipo)
            e_27 = Error(tipo, "27")
            msg = "Error 27: " + tipo + ": " + e_27.msg_1 + e_27.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            zmp = 1

    ccos = 0
    if zmp == 1:
        try: # Separo los recibos reclamados de cosesa
            df_rec_c = df[df['com. cosesa'] > 0]
            df_rec = df[df['com. cosesa'] == 0]
            length2 = len(df_rec_c)
            length.append(length2)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 28: " + tipo)
            e_28 = Error(tipo, "28")
            msg = "Error 28: " + tipo + ": " + e_28.msg_1 + e_28.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            ccos = 1

    red = 0
    if ccos == 1:
        try: # Separo los que tienen com reducida
            df_rec_a = df_rec[df_rec['Comision reducida'].isnull()==False]
            df_rec_r = df_rec[df_rec['Comision reducida'].isnull()==True]
            length3 = len(df_rec_a)
            length.append(length3)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 29: " + tipo)
            e_29 = Error(tipo, "29")
            msg = "Error 29: " + tipo + ": " + e_29.msg_1 + e_29.msg_2
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
            print("Error 210: " + tipo)
            e_210 = Error(tipo, "210")
            msg = "Error 210: " + tipo + ": " + e_210.msg_1 + e_210.msg_2
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
            print("Error 211: " + tipo)
            e_211 = Error(tipo, "211")
            msg = "Error 211: " + tipo + ": " + e_211.msg_1 + e_211.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            cred = 1

    diff = 0
    if cred == 1:
        try: # calculo la desv de la com teorica
            get_desv(df_rec_n, anomaly = 0)
            get_desv(df_rec_fr, anomaly = 0)
            get_desv(df_rec_c, anomaly = 1)
            get_desv(df_rec_a, anomaly = 2)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 212: " + tipo)
            e_212 = Error(tipo, "212")
            msg = "Error 212: " + tipo + ": " + e_212.msg_1 + e_212.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            diff = 1

    # Y calculo los que estan mal pagados de cada uno de los df (normales, cosesa, com. reducida)
    deb_1 = 0
    if diff == 1:
        try: # calculo los que estan mal pagados de los recibos normales y fraccionados
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
            print("Error 213: " + tipo)
            e_213 = Error(tipo, "213")
            msg = "Error 213: " + tipo + ": " + e_213.msg_1 + e_213.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            deb_1 = 1

    deb_2 = 0
    if deb_1 == 1:
        try: # calculo los que estan mal pagados de los recibos ya reclamados de cosesa
            df_rec_ok3 = df_rec_c[(df_rec_c['com_teorica'] - df_rec_c['com. cosesa'] * df_rec_c['Prima neta']) <= desv]
            df_rec_c = df_rec_c[(df_rec_c['com_teorica'] - df_rec_c['com. cosesa'] * df_rec_c['Prima neta']) > desv]
            length8 = len(df_rec_c)
            length.append(length8)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 214: " + tipo)
            e_214 = Error(tipo, "214")
            msg = "Error 214: " + tipo + ": " + e_214.msg_1 + e_214.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            deb_2 = 1

    deb_3 = 0
    if deb_2 == 1:
        try: # calculo los que estan mal pagados de los recibos con comision reducida
            if referencia == 1:
                df_rec_ok4 = df_rec_a[(df_rec_a['com_teorica'] * df_rec_a['com. red'] - df_rec_a['Comisión correduría']) <= desv]
                df_rec_a = df_rec_a[(df_rec_a['com_teorica'] * df_rec_a['com. red'] - df_rec_a['Comisión correduría']) > desv]
            elif referencia != 1:
                df_rec_ok4 = df_rec_a[(df_rec_a['Comision reducida'] == 'Referencia')]
                df_rec_a = df_rec_a[(df_rec_a['Comision reducida'] != 'Referencia')]
                df_rec_ok5 = df_rec_a[((df_rec_a['com_teorica'] * df_rec_a['com. red'] - df_rec_a['Comisión correduría']) <= desv)]
                df_rec_a = df_rec_a[(df_rec_a['com_teorica'] * df_rec_a['com. red'] - df_rec_a['Comisión correduría']) > desv]
            length9 = len(df_rec_a)
            length.append(length9)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 215: " + tipo)
            e_215 = Error(tipo, "215")
            msg = "Error 215: " + tipo + ": " + e_215.msg_1 + e_215.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            deb_3 = 1

    suma = []
    sum = 0
    if deb_3 == 1:
        try: # calculo la cantidades a regularizar y las meto en una lista
            suma_c = df_rec_c['Diferencia'].sum()
            suma_a = df_rec_a['Diferencia'].sum()
            suma_f = df_rec_f['Diferencia'].sum()
            suma_e = df_rec_e['Diferencia'].sum()
            suma.append(suma_e)
            suma.append(suma_f)
            suma.append(suma_a)
            suma.append(suma_c)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 216: " + tipo)
            e_216 = Error(tipo, "216")
            msg = "Error 216: " + tipo + ": " + e_216.msg_1 + e_216.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            sum = 1

    corr = 0
    if sum == 1:
        try:
            if referencia == 1: # junto los df de los recibos pagados correctamente
                df_rec_ok = pd.concat([df_rec_ok1, df_rec_ok2, df_rec_ok3, df_rec_ok4])
            else:
                df_rec_ok = pd.concat([df_rec_ok1, df_rec_ok2, df_rec_ok3, df_rec_ok4, df_rec_ok5])
        except Exception as e:
            tipo = type(e).__name__
            print("Error 217: " + tipo)
            e_217 = Error(tipo, "217")
            msg = "Error 217: " + tipo + ": " + e_217.msg_1 + e_217.msg_2
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
            df_rec_c['Poliza.FechaPrimerEfecto'] = df_rec_c['Poliza.FechaPrimerEfecto'].astype(str)
            df_rec_c['Fecha efecto'] = df_rec_c['Fecha efecto'].astype(str)
            df_rec_ok['Poliza.FechaPrimerEfecto'] = df_rec_ok['Poliza.FechaPrimerEfecto'].astype(str)
            df_rec_ok['Fecha efecto'] = df_rec_ok['Fecha efecto'].astype(str)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 218: " + tipo)
            e_218 = Error(tipo, "218")
            msg = "Error 218: " + tipo + ": " + e_218.msg_1 + e_218.msg_2
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
            col_co = ['Compañía', 'Producto', 'F. primer efecto', 'Nº de póliza', 
                       'Nº de recibo', 'Prima neta', 'Com. prima neta', 'Com. correduría', 
                       'F. de efecto', 'Situación', 'Estado', 'Com. año 1', 'Com. año 2', 
                       'Com. año 3', 'Com. año 4', 'Com. año 5', 'Forma de pago', 'Com. reclamada', 
                       'Com. año 6', 'Com. a aplicar', 'Com. teórica', 'Desviación']
            col_c = ['Compañía', 'Producto', 'F. primer efecto', 'Nº de póliza', 
                       'Nº de recibo', 'Prima neta', 'Com. prima neta', 'Com. correduría', 
                       'F. de efecto', 'Situación', 'Estado', 'Com. año 1', 'Com. año 2', 
                       'Com. año 3', 'Com. año 4', 'Com. año 5', 'Forma de pago', 'Com. reclamada', 
                       'Com. año 6', 'Com. a aplicar', 'Com. teórica', 'Desviación',  'Com. reducida']
            fix_columns_all(df_rec_e, col, 0)
            fix_columns_all(df_rec_f, col, 0)
            fix_columns_all(df_rec_a, col_r, 0)
            fix_columns_all(df_rec_c, col_co, 1)
            fix_columns_all(df_rec_ok, col_c, 1)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 219: " + tipo)
            e_219 = Error(tipo, "219")
            msg = "Error 219: " + tipo + ": " + e_219.msg_1 + e_219.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            adj = 1

    dfs = []
    dfl = 0
    if adj == 1:
        try: # Creo una lista para devolcer los dfs resultado
            dfs.append(df_rec_e)
            dfs.append(df_rec_f)
            dfs.append(df_rec_a)
            dfs.append(df_rec_c)
            dfs.append(df_rec_ok)
        except Exception as e:
            tipo = type(e).__name__
            print("Error 220: " + tipo)
            e_220 = Error(tipo, "220")
            msg = "Error 220: " + tipo + ": " + e_220.msg_1 + e_220.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            dfl = 1

    if dfl == 1:
        try: # exporto el resultado a hojas de excel
            writer = pd.ExcelWriter(path1, engine='xlsxwriter')
            exportar_resultado(df_rec_e, writer, "Normales", 0)
            exportar_resultado(df_rec_f, writer, "Fraccionadas", 0)
            exportar_resultado(df_rec_a, writer, "Comision reducida", 1)
            exportar_resultado(df_rec_c, writer, "Cosesa", 3)
            writer.close()
            writer = pd.ExcelWriter(path2, engine='xlsxwriter')
            exportar_resultado(df_rec_ok, writer, "Correctos", 4)
            writer.close()
        except Exception as e:
            tipo = type(e).__name__
            print("Error 221: " + tipo)
            e_221 = Error(tipo, "221")
            msg = "Error 221: " + tipo + ": " + e_221.msg_1 + e_221.msg_2
            messagebox.showinfo(message=msg, title="Warning", parent=root)
        else:
            result = 1

    return (length, suma, dfs, result)
