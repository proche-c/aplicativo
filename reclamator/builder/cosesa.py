
# Construye una lista anidada con los recibos de cosesa y las com a las que se reclamo
def build_cosesa(df, cosesa):
    length = len(df['RECIBO'])
    item = []
    for i in range(length):
        item = [df['RECIBO'][i], df['COMISION'][i]]
        cosesa.append(item)
    length = len(df['RECIBO2'])
    for i in range(length):
        #item = []
        item = [df['RECIBO2'][i], df['COMISION'][i]]
        cosesa.append(item)
    return cosesa

# Determina si es un recibo que por ser de cosesa ya se ha reclamado
def is_cosesa(df_num_rec, cosesa):
    for i in range(len(cosesa)):
        if (df_num_rec == cosesa[i][0]):
            return cosesa[i][1]
    return 0

# Añade la columna que determina si ya se ha reclamado como cosesa y que cantidad
def add_is_cosesa(df, cosesa):
    df['is cosesa'] = 0
    df['com. cosesa'] = 0
    for i in range(len(df)):
        com_c = is_cosesa(df['Num. recibo'][i], cosesa)
        if com_c > 0:
            df['is cosesa'][i] = 1
            df['com. cosesa'][i] = com_c
    return df