"""
El modulo fraccionada contiene las funciones necesarias para la creación del dataframe
que trata las pólizas fraccionadas de Zurich cuya prima neta requiere un ajuste para 
el cálculo de la comisión.
"""

def get_prima_fraccionada(df):
    """
    Realiza el ajuste a los datos de Prima neta de la BBDD para que el resultado se aproxime
    al cálculo que Zurich realiza. El factor de conversión es un cáculo aproximado
    """
    df['is_fraccionada'] = 0
    df['is_fraccionada_zurich'] = 0

    formas_fraccionadas = ["Mensual", "Trimestral", "Semestral", "Bimestral", "Cuatrimestral"]
    df['is_fraccionada'] = df['Poliza.FormaPago'].isin(formas_fraccionadas).astype(int)

    es_zurich = df['Poliza.Compania.Alias'].isin(["ZURICH", "ZURICH VIDA", "ZURICHVIDA"])

    df.loc[es_zurich & (df['Poliza.FormaPago'] == "Mensual"), 'Prima neta'] *= 0.94
    df.loc[es_zurich & (df['Poliza.FormaPago'] == "Trimestral"), 'Prima neta'] *= 0.96
    df.loc[es_zurich & (df['Poliza.FormaPago'] == "Semestral"), 'Prima neta'] *= 0.98

    df.loc[es_zurich & df['Poliza.FormaPago'].isin(["Mensual", "Trimestral", "Semestral"]), 'is_fraccionada_zurich'] = 1
