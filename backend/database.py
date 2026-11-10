import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

required_settings = ("DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME")
missing_settings = [name for name in required_settings if not os.getenv(name)]
if missing_settings:
    raise RuntimeError(
        "Faltan variables de configuración de la base de datos: "
        + ", ".join(missing_settings)
    )

try:
    database_port = int(os.environ["DB_PORT"])
except ValueError as exc:
    raise ValueError("DB_PORT debe ser un número entero entre 1 y 65535") from exc
if not 1 <= database_port <= 65535:
    raise ValueError("DB_PORT debe ser un número entero entre 1 y 65535")

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=database_port,
    database=os.environ["DB_NAME"],
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)