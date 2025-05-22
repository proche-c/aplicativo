"""
El modulo cosesa contiene las funciones necesarias para la creación del dataframe
que trata las pólizas emitidas en clave cosesa cuyos recibos ya se han reclamado.
"""
import pandas as pd


def build_cosesa(df, cosesa):
    """
    Construye una lista anidada con los recibos de cosesa y las com a las que se reclamó..
    Parámetro df: es un data frame que se construye a partir de un hoja excel que
    contiene los datos de los recibos reclamados
    Parámetro cosesa: Es una lista anidada vacía. Es el vslor que se devuelve
    """
    df['null'] = pd.isna(df['RECIBO2'])
    length = len(df['RECIBO'])
    item = []
    for i in range(length):
        item = [df['RECIBO'][i], df['COMISION'][i]]
        cosesa.append(item)
    length = len(df['RECIBO2'])
    for i in range(length):
        if df['null'][i] == False:
            item = [df['RECIBO2'][i], df['COMISION'][i]]
            cosesa.append(item)
    return cosesa


def is_cosesa(df_num_rec, cosesa):
    """
    Determina si es un recibo que por ser de cosesa ya se ha reclamado.
    Busca cada recibo del data frame en la lista anidada cosesa
    Valores de retorno: 0 si no se ha reclamado; comision reclamada si se ha hecho
    """
    for i in range(len(cosesa)):
        if (df_num_rec == cosesa[i][0]):
            return cosesa[i][1]
    return 0


def add_is_cosesa(df, cosesa):
    """
    Añade la columna que determina si ya se ha reclamado como cosesa y que cantidad
    Crea en el data frame de recibos los campos:
    is_cosesa: 1 si está reclamado; 0 si no lo está
    com. cosesa: comisión reclamada si se ha reclamado; 0 si no
    """
    df['is cosesa'] = 0
    df['com. cosesa'] = 0.00
    for i in range(len(df)):
        com_c = is_cosesa(df['Num. recibo'][i], cosesa)
        if com_c > 0:
            df['is cosesa'][i] = 1
            df['com. cosesa'][i] = com_c
    return df

