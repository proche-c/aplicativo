import re

# Parsea los valores de com. reducida y los transforma todos a flotantes
def get_comision_r(df):
    df['com. red'] = 1
    for i in range(len(df)):
        if type(df['Comision reducida'][i]) is float:
            df['com. red'][i] = df['Comision reducida'][i]
        if type(df['Comision reducida'][i]) is str:
            ref = re.search('Referencia', df['Comision reducida'][i])
            if ref is None:
                com = re.search('%', df['Comision reducida'][i])
                if com is not None:
                    end = com.start()
                    df['com. red'][i] = float(df['Comision reducida'][i][0:end]) / 100