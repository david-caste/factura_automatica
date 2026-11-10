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

    color_primario = (0.10, 0.18, 0.29)
    color_acento = (0.08, 0.58, 0.55)
    color_texto = (0.16, 0.22, 0.29)
    color_secundario = (0.38, 0.45, 0.53)
    color_borde = (0.83, 0.87, 0.90)
    color_fondo = (0.95, 0.97, 0.98)

    encabezado_y = pagina_alto - margen - 82
    pdf.setFillColorRGB(*color_primario)
    pdf.roundRect(
        margen,
        encabezado_y,
        contenido_ancho,
        82,
        8,
        stroke=0,
        fill=1,
    )
    pdf.setFillColorRGB(*color_acento)
    pdf.roundRect(
        margen,
        encabezado_y,
        7,
        82,
        3,
        stroke=0,
        fill=1,
    )
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(margen + 22, encabezado_y + 47, "FACTURA")
    pdf.setFillColorRGB(0.80, 0.87, 0.91)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(margen + 23, encabezado_y + 29, "COMPROBANTE DE VENTA")

    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawRightString(
        pagina_ancho - margen - 18,
        encabezado_y + 51,
        f"N.º {numero}",
    )
    pdf.setFillColorRGB(0.80, 0.87, 0.91)
    pdf.setFont("Helvetica", 9)
    pdf.drawRightString(
        pagina_ancho - margen - 18,
        encabezado_y + 31,
        f"FECHA  {date.today():%d/%m/%Y}",
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
    cliente_y = encabezado_y - 14 - alto_cliente
    cliente_top = cliente_y + alto_cliente
    cabecera_cliente_y = cliente_top - alto_encabezado

    pdf.setFillColorRGB(*color_fondo)
    pdf.roundRect(
        margen,
        cliente_y,
        contenido_ancho,
        alto_cliente,
        7,
        stroke=0,
        fill=1,
    )
    pdf.setFillColorRGB(*color_primario)
    pdf.roundRect(
        margen,
        cabecera_cliente_y,
        contenido_ancho,
        alto_encabezado,
        7,
        stroke=0,
        fill=1,
    )
    pdf.rect(
        margen,
        cabecera_cliente_y,
        contenido_ancho,
        alto_encabezado / 2,
        stroke=0,
        fill=1,
    )
    pdf.setStrokeColorRGB(*color_borde)
    pdf.roundRect(
        margen,
        cliente_y,
        contenido_ancho,
        alto_cliente,
        7,
        stroke=1,
        fill=0,
    )
    pdf.setFillColorRGB(*color_acento)
    pdf.circle(margen + 14, cabecera_cliente_y + alto_encabezado / 2, 3, stroke=0, fill=1)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(margen + 25, cabecera_cliente_y + 9, "DATOS DEL CLIENTE")
    pdf.line(
        margen,
        cabecera_cliente_y,
        margen + contenido_ancho,
        cabecera_cliente_y,
    )
    pdf.setStrokeColorRGB(*color_borde)
    cursor_y = cabecera_cliente_y
    for indice, (izquierda, derecha, alto_fila) in enumerate(filas):
        fila_abajo = cursor_y - alto_fila
        if indice % 2 == 0:
            pdf.setFillColorRGB(1, 1, 1)
            pdf.rect(
                margen + 1,
                fila_abajo,
                contenido_ancho - 2,
                alto_fila,
                stroke=0,
                fill=1,
            )
        for columna, (etiqueta, lineas, ancho_etiqueta) in enumerate(
            (
                (*izquierda, ancho_etiqueta_izquierda),
                (*derecha, ancho_etiqueta_derecha),
            )
        ):
            columna_x = margen + columna * columna_ancho
            bloque_alto = len(lineas) * alto_linea
            texto_y = cursor_y - (alto_fila - bloque_alto) / 2 - 9
            pdf.setFillColorRGB(*color_secundario)
            pdf.setFont("Helvetica-Bold", 8)
            pdf.drawString(columna_x + 8, texto_y, f"{etiqueta}:")
            pdf.setFillColorRGB(*color_texto)
            pdf.setFont("Helvetica", 10)
            for linea_indice, linea in enumerate(lineas):
                pdf.drawString(
                    columna_x + ancho_etiqueta,
                    texto_y - linea_indice * alto_linea,
                    linea,
                )
        cursor_y -= alto_fila
        if indice < len(filas) - 1:
            pdf.setStrokeColorRGB(*color_borde)
            pdf.line(margen, cursor_y, margen + columna_ancho, cursor_y)
            pdf.line(
                margen + columna_ancho,
                cursor_y,
                margen + contenido_ancho,
                cursor_y,
            )

    pdf.setStrokeColorRGB(*color_borde)
    pdf.line(
        margen + columna_ancho,
        cliente_y,
        margen + columna_ancho,
        cabecera_cliente_y,
    )

    alto_pago = 82
    pago_y = cliente_y - 16 - alto_pago
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
    pdf.setFillColorRGB(*color_fondo)
    pdf.roundRect(
        margen,
        pago_y,
        contenido_ancho,
        alto_pago,
        7,
        stroke=0,
        fill=1,
    )
    monto_x = margen + sum(anchos_columnas[:-1])
    pdf.setFillColorRGB(*color_primario)
    pdf.roundRect(
        monto_x,
        pago_y,
        anchos_columnas[-1],
        alto_pago,
        7,
        stroke=0,
        fill=1,
    )
    pdf.rect(
        monto_x,
        pago_y,
        8,
        alto_pago,
        stroke=0,
        fill=1,
    )
    pdf.setStrokeColorRGB(*color_borde)
    pdf.roundRect(
        margen,
        pago_y,
        contenido_ancho,
        alto_pago,
        7,
        stroke=1,
        fill=0,
    )
    x = margen
    for indice, (ancho, etiqueta, valor) in enumerate(
        zip(anchos_columnas, etiquetas_pago, valores_pago)
    ):
        if indice:
            pdf.setStrokeColorRGB(
                *(color_acento if indice == len(anchos_columnas) - 1 else color_borde)
            )
            pdf.line(x, pago_y + 10, x, pago_y + alto_pago - 10)
        if indice == len(anchos_columnas) - 1:
            pdf.setFillColorRGB(0.80, 0.87, 0.91)
            pdf.setFont("Helvetica-Bold", 8)
            pdf.drawString(x + 12, pago_y + 55, etiqueta)
            pdf.setFillColorRGB(1, 1, 1)
            pdf.setFont("Helvetica-Bold", 13)
            pdf.drawString(x + 12, pago_y + 29, valor)
        else:
            pdf.setFillColorRGB(*color_secundario)
            pdf.setFont("Helvetica-Bold", 8)
            pdf.drawString(x + 10, pago_y + 54, etiqueta)
            pdf.setFillColorRGB(*color_texto)
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(x + 10, pago_y + 30, valor)
        x += ancho

    pdf.save()
    return str(ruta)
