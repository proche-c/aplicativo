"""
El modulo cosesa contiene las funciones necesarias para la creación del dataframe
que trata las pólizas emitidas en clave cosesa cuyos recibos ya se han reclamado.
"""
import pandas as pd


def build_cosesa(df, cosesa):
    """
    Devuelve una lista anidada con los recibos de cosesa y las com a las que se reclamó..
    Parámetro df: es un data frame que se construye a partir de un hoja excel que
    contiene los datos de los recibos reclamados
    Parámetro cosesa: Es una lista anidada vacía. Es el valor que se devuelve
    """
    df['null'] = df['RECIBO2'].isna()

    # Para RECIBO, tomamos todas las filas (aunque COMISION pueda ser NaN)
    cosesa_main = df[['RECIBO', 'COMISION']].copy()
    # Reemplazamos NaN en COMISION por 0 para replicar comportamiento sin vectorizar
    cosesa_main['COMISION'] = cosesa_main['COMISION'].fillna(0)
    cosesa_main_list = cosesa_main.values.tolist()


    # Para RECIBO2 solo donde no es nulo, y tomamos COMISION igual con NaN a 0
    cosesa_secondary = df.loc[~df['null'], ['RECIBO2', 'COMISION']].copy()
    cosesa_secondary['COMISION'] = cosesa_secondary['COMISION'].fillna(0)
    cosesa_secondary_list = cosesa_secondary.values.tolist()


    # Unir ambas listas
    cosesa[:] = cosesa_main_list + cosesa_secondary_list

    return cosesa


def add_is_cosesa(df, cosesa):
    """
    Añade columnas indicando si un recibo ya fue reclamado a Cosesa y su comisión.
    """
    cosesa_df = pd.DataFrame(cosesa, columns=['Num. recibo', 'com. cosesa'])


    # Convertir a entero para eliminar decimales .0 y luego a string
    cosesa_df['Num. recibo'] = cosesa_df['Num. recibo'].astype(int).astype(str).str.strip()
    cosesa_df['com. cosesa'] = pd.to_numeric(cosesa_df['com. cosesa'], errors='coerce').fillna(0)

    df['Num. recibo'] = df['Num. recibo'].astype(str).str.strip()

    dup_count = cosesa_df['Num. recibo'].duplicated().sum()

    df = df.merge(cosesa_df, on='Num. recibo', how='left')

    df['com. cosesa'] = df['com. cosesa'].fillna(0.00)
    df['is cosesa'] = (df['com. cosesa'] > 0).astype(int)

    return df




