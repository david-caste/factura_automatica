import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from .excel_processor import cargar_excel
from .invoice_service import procesar_factura

PROJECT_ROOT = Path(__file__).resolve().parents[1]

UPLOADS_DIR = PROJECT_ROOT / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

PDFS_DIR = PROJECT_ROOT / "pdfs"
PDFS_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="AutoFactura",
    description="Transforma un archivo Excel en facturas PDF.",
)


@app.get("/", include_in_schema=False)
def inicio():
    return {"mensaje": "AutoFactura funcionando"}


@app.post("/cargar-excel", summary="Convertir Excel a PDF")
async def cargar_archivo(archivo: UploadFile = File(...)):

    if (
        not archivo.filename
        or Path(archivo.filename).suffix.lower() != ".xlsx"
    ):
        raise HTTPException(
            status_code=400,
            detail="Debes subir un archivo .xlsx"
        )

    # Evita conflictos por nombres repetidos
    nombre_archivo = f"{uuid4()}_{Path(archivo.filename).name}"
    ruta = UPLOADS_DIR / nombre_archivo

    with open(ruta, "wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    df = cargar_excel(ruta)

    required_columns = {
        "cliente",
        "cantidad",
        "valor_unitario"
    }

    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=(
                "Faltan columnas requeridas: "
                + ", ".join(sorted(missing_columns))
            ),
        )

    consecutivo = 1000
    facturas = []

    for _, row in df.iterrows():

        while (PDFS_DIR / f"FAC-{consecutivo}.pdf").exists():
            consecutivo += 1

        numero, pdf = procesar_factura(
            row,
            consecutivo
        )

        facturas.append(
            {
                "numero": numero,
                "archivo": Path(pdf).name,
                "descarga": f"/pdfs/{Path(pdf).name}"
            }
        )

        consecutivo += 1

    return {
        "estado": "procesado",
        "facturas": facturas
    }


@app.get("/pdfs/{filename}", include_in_schema=False)
def descargar_pdf(filename: str):

    ruta = (PDFS_DIR / filename).resolve()

    if (
        Path(filename).name != filename
        or ruta.parent != PDFS_DIR.resolve()
        or ruta.suffix.lower() != ".pdf"
    ):
        raise HTTPException(
            status_code=404,
            detail="PDF no encontrado"
        )

    if not ruta.exists():
        raise HTTPException(
            status_code=404,
            detail="PDF no encontrado"
        )

    return FileResponse(
        path=ruta,
        media_type="application/pdf",
        filename=ruta.name
    )