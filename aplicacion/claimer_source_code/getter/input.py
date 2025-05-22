"""
El módulo input contiene las funciones que modifican el data frame inicial y la función que 
gestiona la creación de los campos necesarios para el procesamiento de los recibos
"""

from builder.regular import *
from builder.cosesa import *
from builder.reducida import *
import pandas as pd
import re

def create_df(path, header):
    """
    Crea el DataFrame inicial a partir del archivo excel introducido.
    Los parametros de entrada son:
        - path: es la ruta del archivo excel que contiene los datos a cargar en el 
        data frame creado.
        - header: indica la fila cuyos valores se quieren tomar como 
        cabecera del data frame que se crea
    """
    if header > 0:
        df = pd.read_excel(path, header=header)
    else:
        df = pd.read_excel(path)
    return df


def eliminar_columnas(df):
    """
    Elimina las columnas sin etiquetar, en este caso, las columnas llamadas 
    'Unnamed' que corresponden con la especificación de la moneda utilizada
    """
    rem = []
    for i in range(len(df.columns)):
        c = df.columns[i]
        control = re.search('Unnamed:', c)
        if control is not None:
            rem.append(i)
    if len(rem) > 0:
        i = 0
        for j in rem:
            df.drop(df.columns[j - i], axis=1, inplace=True)
            i = i + 1


def fix_index(df):
    """
    Arregla los indices. Se usa despues de eliminar alguna fila para evitar errores.
    Toma como parámetro el data frame cuyos indices se han de corregir
    """
    ind = range(len(df))
    df['cod'] = ind
    df.set_index('cod', inplace=True)


def get_com(df):
    """
    Añade al dataframe los campos que indican la comision del sexto año,
    la comision que debe aplicarse en porcentaje y la comision teorica
    que se deberia haber cobrado en euros
    """
    fix_index(df)
    add_Com6(df)
    get_comision_a(df)
    get_comision_t(df)

