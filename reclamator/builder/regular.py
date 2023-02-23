from datetime import datetime
import pandas as pd

# Crea el DataFrame
def create_df(path, header):
    if header > 0:
        df = pd.read_excel(path, header=header)
    else:
        df = pd.read_excel(path)
    return df

# Arregla los indices. Se usa despues de eliminar alguna fila para evitar errores
def fix_index(df, cod):
    ind = range(len(df))
    df[cod] = ind
    df.set_index(cod, inplace=True)

# Obtiene la comision que se debe aplicar segun la antiguedad de la poliza
def get_comision_a(df_recibos):
    df_recibos['com_aplicada'] = 0
    for i in range(len(df_recibos)):
        date_1 = df_recibos['Fecha efecto'][i]
        date_2 = df_recibos['Poliza.FechaPrimerEfecto'][i]
        if date_1.year == date_2.year or (date_1.year == date_2.year + 1 and date_1.month < date_2.month):
            df_recibos['com_aplicada'][i] = df_recibos['Poliza.Producto.Com1'][i]
        elif (date_1.year == date_2.year + 1 and date_1.month >= date_2.month) or (date_1.year == date_2.year + 2 and date_1.month < date_2.month):
            df_recibos['com_aplicada'][i] = df_recibos['Poliza.Producto.Com2'][i]
        elif (date_1.year == date_2.year + 2 and date_1.month >= date_2.month) or (date_1.year == date_2.year + 3 and date_1.month < date_2.month):
            df_recibos['com_aplicada'][i] = df_recibos['Poliza.Producto.Com3'][i]
        elif (date_1.year == date_2.year + 3 and date_1.month >= date_2.month) or (date_1.year == date_2.year + 4 and date_1.month < date_2.month):
            df_recibos['com_aplicada'][i] = df_recibos['Poliza.Producto.Com4'][i]
        elif (date_1.year == date_2.year + 4 and date_1.month >= date_2.month) or (date_1.year == date_2.year + 5 and date_1.month < date_2.month):
            df_recibos['com_aplicada'][i] = df_recibos['Poliza.Producto.Com5'][i]
        else:
            df_recibos['com_aplicada'][i] = df_recibos['Poliza.Producto.Com6'][i]

# Añade la com del 6º año para el Zurich Motor Pack
def add_Com6(df_recibos):
    df_recibos['Poliza.Producto.Com6'] = 0
    for i in range(len(df_recibos)):
        if df_recibos.loc[:,'Producto'][0:][i] == 'ZURICH MOTOR PACK(1ª CAT)':
            df_recibos['Poliza.Producto.Com6'][i] = df_recibos['Poliza.Producto.Com5'][i] + 0.01
        elif df_recibos.loc[:,'Producto'][0:][i] == 'ZURICH MOTOR PACK(2ª CAT)':
            df_recibos['Poliza.Producto.Com6'][i] = df_recibos['Poliza.Producto.Com5'][i] + 0.01
        elif df_recibos.loc[:,'Producto'][0:][i] == 'ZURICH MOTOR PACK(3ª CAT)':
            df_recibos['Poliza.Producto.Com6'][i] = df_recibos['Poliza.Producto.Com5'][i] + 0.01
        else:
            df_recibos['Poliza.Producto.Com6'][i] = df_recibos['Poliza.Producto.Com5'][i]

# Calcula la comision que se debe cobrar segun fecha y producto    
def get_comision_t(df_recibos):
    df_recibos['com_teorica'] = 0
    for i in range(len(df_recibos)):
        df_recibos['com_teorica'][i] = df_recibos['com_aplicada'][i] * df_recibos['Prima neta'][i]

# Calcula la diferencia entre la com cobrada y la que se deberia haber cobrado
def get_dif(df_recibos, anomaly):
    df_recibos['Diferencia'] = 0
    for i in range(len(df_recibos)):
        if anomaly == 0:
            df_recibos['Diferencia'][i] = df_recibos['com_teorica'][i] - df_recibos['Comisión correduría'][i]
        elif anomaly == 1:
            df_recibos['Diferencia'][i] = df_recibos['com_teorica'][i] - df_recibos['com. cosesa'][i] * df_recibos['Prima neta'][i]
        elif anomaly == 2:
            df_recibos['Diferencia'][i] = df_recibos['com_teorica'][i] * df_recibos['com. red'][i] - df_recibos['Comisión correduría'][i]
