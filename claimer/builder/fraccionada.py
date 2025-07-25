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
    for i in range(len(df)):
        if df['Poliza.FormaPago'][i] ==  "Mensual":
            df['is_fraccionada'][i] = 1
            if (df['Poliza.Compania.Alias'][i] == "ZURICH" or df['Poliza.Compania.Alias'][i] == "ZURICH VIDA" or df['Poliza.Compania.Alias'][i] == "ZURICHVIDA"):
                df['Prima neta'][i] = 0.94 * df['Prima neta'][i]
                df['is_fraccionada_zurich'][i] = 1
        elif df['Poliza.FormaPago'][i] ==  "Trimestral":
            df['is_fraccionada'][i] = 1
            if (df['Poliza.Compania.Alias'][i] == "ZURICH" or df['Poliza.Compania.Alias'][i] == "ZURICH VIDA" or df['Poliza.Compania.Alias'][i] == "ZURICHVIDA"):
                df['Prima neta'][i] = 0.96 * df['Prima neta'][i]
                df['is_fraccionada_zurich'][i] = 1
        elif df['Poliza.FormaPago'][i] ==  "Semestral":
            df['is_fraccionada'][i] = 1
            if (df['Poliza.Compania.Alias'][i] == "ZURICH" or df['Poliza.Compania.Alias'][i] == "ZURICH VIDA" or df['Poliza.Compania.Alias'][i] == "ZURICHVIDA"):
                df['Prima neta'][i] = 0.98 * df['Prima neta'][i]
                df['is_fraccionada_zurich'][i] = 1
        elif df['Poliza.FormaPago'][i] ==  "Bimestral" or df['Poliza.FormaPago'][i] ==  "Cuatrimestral":
                df['is_fraccionada'][i] = 1