import pandas as pd
from builder.regular import *
from builder.cosesa import *
from builder.reducida import *
from getter.getters import *

pd.options.mode.chained_assignment = None  # default='warn'

path = "archivos/caz.xlsx"
path_cosesa = "archivos/Cosesa_2017.xlsx"
desv = 0.5
referencia = 0  #indica si se reclaman las de ref (1) o no (0)

# Creo el dataframe de los recibos
df = create_df(path, 1)

# Creo el dataframe de los recibos Cosesa reclamados
df_cosesa = create_df(path_cosesa, 0)

# Creo una lista anidada con los recibos de cosesa y la com reclamada
cosesa = []
build_cosesa(df_cosesa, cosesa)

# Añado esa informacion al dataframe de recibos
add_is_cosesa(df, cosesa)

# Calculo la com a aplicar y lo que se deberia haber cobrado
get_com(df)

# Separo los recibos reclamados de cosesa
df_rec_c = df[df['com. cosesa'] > 0]
df_rec = df[df['com. cosesa'] == 0]

# Separo los que tienen com reducida
df_rec_a = df_rec[df_rec['Comision reducida'].isnull()==False]
df_rec_n = df_rec[df_rec['Comision reducida'].isnull()==True]

# Y calculo los que estan mal pagados de cada uno de los dt (normales, cosesa, com. reducida)
df_rec_ok1 = df_rec_n[(df_rec_n['com_teorica'] - df_rec_n['Comisión correduría']) <= desv]
df_rec_e = df_rec_n[(df_rec_n['com_teorica'] - df_rec_n['Comisión correduría']) > desv]
df_rec_e = df_rec_e[(df_rec_e['Prima neta'] > 0)]

df_rec_ok2 = df_rec_c[(df_rec_c['com_teorica'] - df_rec_c['com. cosesa'] * df_rec_c['Prima neta']) <= desv]
df_rec_c = df_rec_c[(df_rec_c['com_teorica'] - df_rec_c['com. cosesa'] * df_rec_c['Prima neta']) > desv]
df_rec_c = df_rec_c[(df_rec_c['Prima neta'] > 0)]

fix_index(df_rec_a,'cod')
get_comision_r(df_rec_a)
if referencia == 1:
    df_rec_ok3 = df_rec_a[(df_rec_a['com_teorica'] * df_rec_a['com. red'] - df_rec_a['Comisión correduría']) <= desv]
    df_rec_a = df_rec_a[(df_rec_a['com_teorica'] * df_rec_a['com. red'] - df_rec_a['Comisión correduría']) > desv]
elif referencia != 1:
    df_rec_ok3 = df_rec_a[(df_rec_a['Comision reducida'] == 'Referencia')]
    df_rec_a = df_rec_a[(df_rec_a['Comision reducida'] != 'Referencia')]
    df_rec_ok4 = df_rec_a[((df_rec_a['com_teorica'] * df_rec_a['com. red'] - df_rec_a['Comisión correduría']) <= desv)]
    df_rec_a = df_rec_a[(df_rec_a['com_teorica'] * df_rec_a['com. red'] - df_rec_a['Comisión correduría']) > desv]

LO ARREGLO MAÑANA!!!!!!!!!!!



get_desv(df_rec_e, anomaly = 0)
get_desv(df_rec_c, anomaly = 1)
get_desv(df_rec_a, anomaly = 2)

# Creo la columna com. red en ok2 y ok1
df_rec_ok1['com. red'] = 1 
df_rec_ok2['com. red'] = 1

df_rec_ok = pd.concat([df_rec_ok1, df_rec_ok2, df_rec_ok3])

# # Arreglo las fechas para que se muestren bien en el excel
df_rec_e['Poliza.FechaPrimerEfecto'] = df_rec_e['Poliza.FechaPrimerEfecto'].astype(str)
df_rec_e['Fecha efecto'] = df_rec_e['Fecha efecto'].astype(str)
df_rec_a['Poliza.FechaPrimerEfecto'] = df_rec_a['Poliza.FechaPrimerEfecto'].astype(str)
df_rec_a['Fecha efecto'] = df_rec_a['Fecha efecto'].astype(str)
df_rec_c['Poliza.FechaPrimerEfecto'] = df_rec_a['Poliza.FechaPrimerEfecto'].astype(str)
df_rec_c['Fecha efecto'] = df_rec_a['Fecha efecto'].astype(str)
df_rec_ok['Poliza.FechaPrimerEfecto'] = df_rec_ok['Poliza.FechaPrimerEfecto'].astype(str)
df_rec_ok['Fecha efecto'] = df_rec_ok['Fecha efecto'].astype(str)

with pd.ExcelWriter("archivos/resultado.xlsx") as writer:
    df_rec_e.to_excel(writer, sheet_name="Normales", index = False)
    df_rec_a.to_excel(writer, sheet_name="Comision reducida", index = False)
    df_rec_c.to_excel(writer, sheet_name="Cosesa", index = False)

with pd.ExcelWriter("archivos/correctos.xlsx") as writer:
    df_rec_ok.to_excel(writer, sheet_name="Correctos", index = False)

print("ACABA EL PROGRAMA")g