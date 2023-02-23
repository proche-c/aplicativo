from builder.regular import *
from builder.cosesa import *
from builder.reducida import *

def get_com(df):
    fix_index(df,'cod')
    add_Com6(df)
    get_comision_a(df)
    get_comision_t(df)

def get_desv(df, anomaly):
    fix_index(df,'cod')
    get_dif(df, anomaly)