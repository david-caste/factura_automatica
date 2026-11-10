from datetime import date
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

PDFS_DIR = Path(__file__).resolve().parents[1] / "pdfs"
PDFS_DIR.mkdir(parents=True, exist_ok=True)


def crear_pdf(
    numero,
    cliente,
    total,
    cantidad="",
    valor_unitario="",
    cedula="",
    telefono="",
    correo="",
    ciudad="",
    direccion="",
    modo_pago="",
):
    ruta = PDFS_DIR / f"{numero}.pdf"
    pagina_ancho, pagina_alto = letter
    margen = 42
    contenido_ancho = pagina_ancho - margen * 2
    pdf = canvas.Canvas(str(ruta), pagesize=letter)
    pdf.setTitle(f"Factura {numero}")

    pdf.setFillColorRGB(0.12, 0.17, 0.21)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawCentredString(pagina_ancho / 2, pagina_alto - 58, "FACTURA")
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(margen, pagina_alto - 82, f"Número de factura: {numero}")
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(
        pagina_ancho - margen,
        pagina_alto - 82,
        f"Fecha: {date.today():%d/%m/%Y}",
    )

    columna_ancho = contenido_ancho / 2
    ancho_etiqueta_izquierda = 62
    ancho_etiqueta_derecha = 70
    alto_encabezado = 28
    alto_linea = 12
    filas = []
    datos_izquierda = [
        ("NOMBRE", cliente),
        ("CÉDULA", cedula),
        ("TELÉFONO", telefono),
    ]
    datos_derecha = [
        ("CORREO", correo),
        ("CIUDAD", ciudad),
        ("DIRECCIÓN", direccion),
    ]
    for (etiqueta_izquierda, valor_izquierda), (
        etiqueta_derecha,
        valor_derecha,
    ) in zip(datos_izquierda, datos_derecha):
        linea_izquierda = simpleSplit(
            str(valor_izquierda or ""),
            "Helvetica",
            10,
            columna_ancho - ancho_etiqueta_izquierda - 16,
        ) or [""]
        linea_derecha = simpleSplit(
            str(valor_derecha or ""),
            "Helvetica",
            10,
            columna_ancho - ancho_etiqueta_derecha - 16,
        ) or [""]
        alto_fila = max(
            24,
            max(len(linea_izquierda), len(linea_derecha)) * alto_linea + 8,
        )
        filas.append(
            (
                (etiqueta_izquierda, linea_izquierda),
                (etiqueta_derecha, linea_derecha),
                alto_fila,
            )
        )

    alto_cliente = alto_encabezado + sum(fila[2] for fila in filas)
    cliente_y = pagina_alto - 100 - alto_cliente

    pdf.setStrokeColorRGB(0.25, 0.31, 0.36)
    pdf.setFillColorRGB(0.12, 0.17, 0.21)
    pdf.rect(margen, cliente_y, contenido_ancho, alto_cliente, stroke=1, fill=0)
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawCentredString(pagina_ancho / 2, cliente_y + alto_cliente - 19, "DATOS DEL CLIENTE")
    pdf.line(
        margen,
        cliente_y + alto_cliente - alto_encabezado,
        margen + contenido_ancho,
        cliente_y + alto_cliente - alto_encabezado,
    )
    pdf.line(
        margen + columna_ancho,
        cliente_y,
        margen + columna_ancho,
        cliente_y + alto_cliente - alto_encabezado,
    )

    cursor_y = cliente_y + alto_cliente - alto_encabezado
    for indice, (izquierda, derecha, alto_fila) in enumerate(filas):
        for columna, (etiqueta, lineas, ancho_etiqueta) in enumerate(
            (
                (*izquierda, ancho_etiqueta_izquierda),
                (*derecha, ancho_etiqueta_derecha),
            )
        ):
            columna_x = margen + columna * columna_ancho
            bloque_alto = len(lineas) * alto_linea
            texto_y = cursor_y - (alto_fila - bloque_alto) / 2 - 9
            pdf.setFont("Helvetica-Bold", 9)
            pdf.drawString(columna_x + 8, texto_y, f"{etiqueta}:")
            pdf.setFont("Helvetica", 10)
            for linea_indice, linea in enumerate(lineas):
                pdf.drawString(
                    columna_x + ancho_etiqueta,
                    texto_y - linea_indice * alto_linea,
                    linea,
                )
        cursor_y -= alto_fila
        if indice < len(filas) - 1:
            pdf.line(margen, cursor_y, margen + columna_ancho, cursor_y)
            pdf.line(
                margen + columna_ancho,
                cursor_y,
                margen + contenido_ancho,
                cursor_y,
            )

    alto_pago = 74
    pago_y = cliente_y - 18 - alto_pago
    pdf.rect(margen, pago_y, contenido_ancho, alto_pago, stroke=1, fill=0)
    anchos_columnas = [
        contenido_ancho * 0.34,
        contenido_ancho * 0.16,
        contenido_ancho * 0.25,
        contenido_ancho * 0.25,
    ]
    etiquetas_pago = [
        "MODO DE PAGO",
        "CANTIDAD",
        "VALOR UNITARIO",
        "MONTO",
    ]
    valores_pago = [
        str(modo_pago or ""),
        str(cantidad),
        f"$ {valor_unitario:,.2f}",
        f"$ {total:,.2f}",
    ]
    x = margen
    for indice, (ancho, etiqueta, valor) in enumerate(
        zip(anchos_columnas, etiquetas_pago, valores_pago)
    ):
        if indice:
            pdf.line(x, pago_y, x, pago_y + alto_pago)
        pdf.setFont("Helvetica-Bold", 8)
        pdf.drawString(x + 8, pago_y + 48, etiqueta)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(x + 8, pago_y + 24, valor)
        x += ancho

    pdf.save()
    return str(ruta)
