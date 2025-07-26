"""
Este módulo contiene las funciones que crean el data frame a partir del cual 
se construyen los data frame de datos estadísticos
"""

import pandas as pd


def create_df_est(path):
    """
    Crea el data frame con los datos estadisticos que se han considerado
    relevantes tanto para su visualización como para extraer datos
    de negocio que ayuden a las métricas
    Recibe como parámetro la ruta donde se encuentra el archivo con datos
    a analizar
    """
    df_i = pd.read_excel(path, header=1)
    
    df = df_i[['Poliza.Compania.Alias', 'Producto', 'Prima neta', 'Comisión prima neta', 
               'Comisión correduría', 'Poliza.Producto.Com1', 'Poliza.Producto.Com2', 
               'Poliza.Producto.Com3', 'Poliza.Producto.Com4', 'Poliza.Producto.Com5']].copy()
    
    df.columns = ['Compañía', 'Producto', 'Prima neta', 'Com. prima neta', 'Com. correduría',
                  'Com. año 1', 'Com. año 2', 'Com. año 3', 'Com. año 4', 'Com. año 5']

    # Convertimos columnas numéricas con errores a 0 si no se pueden convertir
    for col in ['Prima neta', 'Com. prima neta', 'Com. correduría']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    return df


def create_list_prod(df):
    """
    Crea una lista de tuplas de indice, compañía, producto y comisiones
    Toma los datos del archivo a analizar y elimina los duplicados
    toma como parametro el data frame creado y devuelve una lista de tuplas
    """
    cols = ['Compañía', 'Producto', 'Com. año 1', 'Com. año 2', 'Com. año 3', 'Com. año 4', 'Com. año 5']
    df_unique = df[cols].drop_duplicates().reset_index(drop=True)
    df_unique.insert(0, 'indice', df_unique.index)
    list_prod = list(df_unique.itertuples(index=False, name=None))
    return list_prod

def find_indice(list_prod, cia, prod, com1, com2, com3, com4, com5):
    """
    Relaciona los indices conforme los que se ha hecho el análisis estadístico con 
    sus correspondiente tupla en la lista de productos.
    Toma como parámetros:
        - list_prod: la lista de productos sin duplicados
        - Los datos de producto de cada registro del data frame
    """
    for tup in list_prod:
        if tup[1:] == (cia, prod, com1, com2, com3, com4, com5):
            return tup
    return None


def complete_df(list_prod, df):
    """
    Crea un indice único asociado a cada par de valores producto-compañía y que
    se utiliza como referencia de los cálculos estadísticos con el fín de evitar
    la contaminación de datos que pueda derivarse de posibles duplicidades en los
    nombres de los productos.
    Recibe como parametros una lista de tuplas con los datos relevantes de cada
    producto y el data frame
    """
    df['indice'] = -1

    df_map = pd.DataFrame(list_prod, columns=['indice', 'Compañía', 'Producto', 
                                               'Com. año 1', 'Com. año 2', 'Com. año 3', 
                                               'Com. año 4', 'Com. año 5'])

    df = df.merge(df_map, on=['Compañía', 'Producto', 'Com. año 1', 'Com. año 2', 
                              'Com. año 3', 'Com. año 4', 'Com. año 5'], how='left', suffixes=('', '_map'))

    # Renombra correctamente y elimina el antiguo
    if 'indice_map' in df.columns:
        df.drop(columns=['indice'], inplace=True)
        df.rename(columns={'indice_map': 'indice'}, inplace=True)

    # Calcula los porcentajes
    df['Com. prima neta %'] = (df['Com. prima neta'] / df['Prima neta']).fillna(0)
    df['Com. correduría %'] = (df['Com. correduría'] / df['Prima neta']).fillna(0)
    df['Sobrecomisión %'] = df['Com. correduría %'] - df['Com. prima neta %']

    return df

