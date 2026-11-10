import pandas as pd

def cargar_excel(ruta):
    return pd.read_excel(ruta, dtype=object)