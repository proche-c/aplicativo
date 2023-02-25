import pandas as pd
from builder.regular import *
from builder.cosesa import *
from builder.reducida import *
from getter.getters import *

pd.options.mode.chained_assignment = None  # default='warn'

path = "archivos/caz.xlsx"
path_cosesa = "archivos/Cosesa_2017.xlsx"
desv = 0.01
referencia = 0  #indica si se reclaman las de ref (1) o no (0)
print("Pulse 1 si desea reclamar los recibos de referencia")
referencia = int(input())
print(referencia)
parameters = {'p':path, 'pc':path_cosesa, 'd':desv, 'r': referencia}
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

# Quito los que tienen PN menor que 0
length1 = len(df)
df = df[df['Prima neta'] > 0]
fix_index(df,'cod')
length2 = len(df)

# Separo los recibos reclamados de cosesa
df_rec_c = df[df['com. cosesa'] > 0]
df_rec = df[df['com. cosesa'] == 0]
length3 = len(df_rec_c)
# Hasta aqui bien

# Separo los que tienen com reducida
df_rec_a = df_rec[df_rec['Comision reducida'].isnull()==False]
df_rec_n = df_rec[df_rec['Comision reducida'].isnull()==True]
length5 = len(df_rec_n)
length6 = len(df_rec_a)

# Y calculo los que estan mal pagados de cada uno de los dt (normales, cosesa, com. reducida)
df_rec_ok1 = df_rec_n[(df_rec_n['com_teorica'] - df_rec_n['Comisión correduría']) <= desv]
df_rec_e = df_rec_n[(df_rec_n['com_teorica'] - df_rec_n['Comisión correduría']) > desv]
length8 = len(df_rec_e)
# Hasta aqui bien

df_rec_ok2 = df_rec_c[(df_rec_c['com_teorica'] - df_rec_c['com. cosesa'] * df_rec_c['Prima neta']) <= desv]
df_rec_c = df_rec_c[(df_rec_c['com_teorica'] - df_rec_c['com. cosesa'] * df_rec_c['Prima neta']) > desv]
length4 = len(df_rec_c)
# Hasta aqui bien

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

length7 = len(df_rec_a)

get_desv(df_rec_e, anomaly = 0)
get_desv(df_rec_c, anomaly = 1)
get_desv(df_rec_a, anomaly = 2)

suma_c = df_rec_c['Diferencia'].sum()
suma_a = df_rec_a['Diferencia'].sum()
suma_e = df_rec_e['Diferencia'].sum()
# Creo la columna com. red en ok2 y ok1
df_rec_ok1['com. red'] = 1 
df_rec_ok2['com. red'] = 1

if referencia == 1:
    df_rec_ok = pd.concat([df_rec_ok1, df_rec_ok2, df_rec_ok3])
else:
    df_rec_ok = pd.concat([df_rec_ok1, df_rec_ok2, df_rec_ok3, df_rec_ok4])

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


print("*****************************************************************************")
print("Si usted ha pulsado 1, se considerará que los recibos categorizados como 'Referencia' tienen la comisión que marca el producto")
print("Si no ha pulsado 1, los recibos categorizados como 'Referencia' se considerarán correctamente pagados")
print("*****************************************************************************")
print(f"Se han procesado un total de {length1} recibos")
print(f"De los cuales {length1 - length2} tenían una prima neta menor que 0, por lo que no se tendrán en cuenta")
print(f"Por lo tanto se procesarán {length2} recibos")
print(f"De los cuales {length3} se emitieron con clave cosesa y ya se reclamaron")
print(f"Sin embargo en {length4} de ellos se reclamó una comisión menor de la que correspondía")
print("Reclamando la comisión correspondiente, la compañía aún le debe la cantidad de:")
print(f"***************** {suma_c} Euros****************")
print(f"De los {length2 - length3} recibos restantes {length6} tienen una comisión anómala")
print(f"Teniendo en cuenta esa comisión anómala, {length7} de ellos no se pagaron correctamente")
print("La compañía aún le debe la cantidad de:")
print(f"***************** {suma_a} Euros****************")
print(f"De los {length2 - length3 - length6} recibos restantes, {length8} no se pagaron correctamente")
print("La compañía aún le debe la cantidad de:")
print(f"***************** {suma_e} Euros****************")
print("Por lo tanto, la compañía aún le debe la cantidad TOTAL de:")
print(f"***************** {suma_e + suma_a + suma_c} Euros****************")
print("ACABA EL PROGRAMA")