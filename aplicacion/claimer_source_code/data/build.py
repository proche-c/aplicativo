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
        'Poliza.Producto.Com3', 'Poliza.Producto.Com4', 'Poliza.Producto.Com5']]
    col = ['Compañía', 'Producto', 'Prima neta', 'Com. prima neta', 'Com. correduría', 
        'Com. año 1', 'Com. año 2', 'Com. año 3', 'Com. año 4', 'Com. año 5']
    df.columns = col
    for i in range(len(df)):
        try:
            df['Prima neta'][i] = float(df['Prima neta'][i])
        except ValueError:
            df['Prima neta'][i] = 0
        try:
            df['Com. prima neta'][i] = float(df['Com. prima neta'][i])
        except ValueError:
            df['Com. prima neta'][i] = 0
        try:
            df['Com. correduría'][i] = float(df['Com. correduría'][i])
        except ValueError:
            df['Com. correduría'][i] = 0
    df['Prima neta'] = df['Prima neta'].astype(float)
    df['Com. prima neta'] = df['Com. prima neta'].astype(float)
    df['Com. correduría'] = df['Com. correduría'].astype(float)
    df['Prima neta'].fillna(0)
    df['Com. prima neta'].fillna(0)
    df['Com. correduría'].fillna(0)
    return df


def create_list_prod(df):
    """
    Crea una lista de tuplas de indice, compañía, producto y comisiones
    Toma los datos del archivo a analizar y elimina los duplicados
    toma como parametro el data frame creado y devuelve una lista de tuplas
    """
    l = []
    for i in range(len(df)):
        t = (df['Compañía'][i], df['Producto'][i], df['Com. año 1'][i], df['Com. año 2'][i], 
            df['Com. año 3'][i], df['Com. año 4'][i], df['Com. año 5'][i])
        l.append(t)
    l2 = []
    l2 = list(set(l))
    list_prod = []
    for i in range(len(l2)):
        t2 = (i, l2[i][0], l2[i][1], l2[i][2], l2[i][3], l2[i][4], l2[i][5], l2[i][6])
        list_prod.append(t2)
    return list_prod

def find_indice(list_prod, cia, prod, com1, com2, com3, com4, com5):
    """
    Relaciona los indices conforme los que se ha hecho el análisis estadístico con 
    sus correspondiente tupla en la lista de productos.
    Toma como parámetros:
        - list_prod: la lista de productos sin duplicados
        - Los datos de producto de cada registro del data frame
    """
    for i in range(len(list_prod)):
        if (list_prod[i][1] == cia and list_prod[i][2] == prod and list_prod[i][3] == com1 
        and list_prod[i][4] == com2 and list_prod[i][5] == com3 and 
        list_prod[i][6] == com4 and list_prod[i][7] == com5):
            break
    return list_prod[i]


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
    df['Com. prima neta %'] = 0.00
    df['Com. correduría %'] = 0.00
    df['Sobrecomisión %'] = 0.00
    for i in range(len(df)):
        tup = find_indice(list_prod, df['Compañía'][i], df['Producto'][i], df['Com. año 1'][i], 
            df['Com. año 2'][i], df['Com. año 3'][i], df['Com. año 4'][i], df['Com. año 5'][i]              )
        df['indice'][i] = tup[0]
        if df['Prima neta'][i] != 0:
            df['Com. prima neta %'][i] = (df['Com. prima neta'][i] / df['Prima neta'][i]).astype(float)
            df['Com. correduría %'][i] = (df['Com. correduría'][i] / df['Prima neta'][i])
            df['Sobrecomisión %'][i] = df['Com. correduría %'][i] - df['Com. prima neta %'][i]

