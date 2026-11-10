import unicodedata

import pandas as pd

from .config import IVA
from .pdf_generator import crear_pdf


def _normalizar_columna(nombre):
    nombre = unicodedata.normalize("NFKD", str(nombre))
    nombre = nombre.encode("ascii", "ignore").decode("ascii")
    return "_".join(nombre.strip().lower().split())


def _obtener_dato(datos, *nombres):
    for nombre in nombres:
        valor = datos.get(nombre)
        if valor is not None and not pd.isna(valor):
            return str(valor).strip()
    return ""


def procesar_factura(row, consecutivo):

    subtotal = row["cantidad"] * row["valor_unitario"]
    iva = subtotal * IVA
    total = subtotal + iva

    numero = f"FAC-{consecutivo}"

    datos = {
        _normalizar_columna(nombre): valor
        for nombre, valor in row.items()
    }

    pdf = crear_pdf(
        numero=numero,
        cliente=_obtener_dato(datos, "cliente", "nombre"),
        total=total,
        cantidad=row["cantidad"],
        valor_unitario=row["valor_unitario"],
        cedula=_obtener_dato(datos, "cedula"),
        telefono=_obtener_dato(datos, "telefono"),
        correo=_obtener_dato(datos, "correo", "email"),
        ciudad=_obtener_dato(datos, "ciudad"),
        direccion=_obtener_dato(datos, "direccion"),
        modo_pago=_obtener_dato(
            datos,
            "modo_de_pago",
            "forma_de_pago",
            "modo_pago",
            "forma_pago",
        ),
    )

    return numero, pdf