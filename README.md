# AutoFactura

## Instalación y ejecución

Desde la carpeta del proyecto, activa un entorno Python e instala las dependencias:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

La API queda disponible en `http://127.0.0.1:8000`; la documentación interactiva
está en `http://127.0.0.1:8000/docs`.

## Generar y descargar facturas

El endpoint `POST /cargar-excel` recibe un archivo `.xlsx` con las columnas
`cliente`, `cantidad` y `valor_unitario`. No se envían correos.
También puede incluir `cedula`, `telefono`, `correo`, `ciudad`, `direccion` y
`modo_pago` (o `forma_pago`). Estos campos se imprimen en la factura cuando
están presentes. La hoja puede usar encabezados con mayúsculas o tildes; por
ejemplo, `Cedula`, `Ciudad` y `Direccion`.
El PDF muestra la cantidad y el valor unitario, y calcula el monto total con el
IVA configurado. La fecha corresponde al día en que se genera el PDF. Conserva
la cédula como texto en Excel para no perder ceros iniciales.

La respuesta incluye la lista de facturas generadas y la ruta de descarga de cada
PDF. También puedes abrir cada enlace `/pdfs/<archivo>.pdf` desde el navegador.
Los archivos quedan guardados individualmente en la carpeta `pdfs/`; las
facturas nuevas usan consecutivos disponibles y no reemplazan las anteriores.

Si el servidor SMTP responde `535 5.7.3 Authentication unsuccessful`, Microsoft
365 está rechazando las credenciales o la autenticación SMTP del buzón o de la
organización está deshabilitada. Revisa esa configuración con el administrador
de Microsoft 365; no compartas la contraseña en reportes o registros.
