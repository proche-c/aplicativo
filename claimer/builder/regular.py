"""
El modulo regular contiene la funcion necesaria para la creación del dataframe
que trata las pólizas sin anomalías.
"""


def get_comision_a(df_recibos):
    """Obtiene la comision que se debe aplicar segun la antiguedad de la poliza"""
    df_recibos['com_aplicada'] = 0.00
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


def add_Com6(df_recibos):
    """Añade la com del 6º año para el Zurich Motor Pack"""
    df_recibos['Poliza.Producto.Com6'] = 0.00
    for i in range(len(df_recibos)):
        if df_recibos.loc[:,'Producto'][0:][i] == 'ZURICH MOTOR PACK(1ª CAT)':
            df_recibos['Poliza.Producto.Com6'][i] = df_recibos['Poliza.Producto.Com5'][i] + 0.01
        elif df_recibos.loc[:,'Producto'][0:][i] == 'ZURICH MOTOR PACK(2ª CAT)':
            df_recibos['Poliza.Producto.Com6'][i] = df_recibos['Poliza.Producto.Com5'][i] + 0.01
        elif df_recibos.loc[:,'Producto'][0:][i] == 'ZURICH MOTOR PACK(3ª CAT)':
            df_recibos['Poliza.Producto.Com6'][i] = df_recibos['Poliza.Producto.Com5'][i] + 0.01
        else:
            df_recibos['Poliza.Producto.Com6'][i] = df_recibos['Poliza.Producto.Com5'][i]

    
def get_comision_t(df_recibos):
    """Calcula la comision que se debe cobrar segun fecha y producto"""
    df_recibos['com_teorica'] = 0.00
    for i in range(len(df_recibos)):
        if df_recibos['Prima neta'][i] != 0:
            df_recibos['com_teorica'][i] = df_recibos['com_aplicada'][i] * df_recibos['Prima neta'][i]


