"""
Configuración compartida de pytest para todos los tests de la API.
Crea una base de datos SQLite en memoria, exclusiva para los tests,
y la inyecta en la app en lugar de la base de datos real (sensorhub.db).
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db import Base, get_db
from app.main import app

# URL especial de SQLite: crea la base de datos solo en memoria RAM, nunca en disco.
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

# StaticPool mantiene UNA sola conexión compartida durante todo el test,
# necesario porque una base en memoria desaparece si se cierra la conexión.
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_test_database():
    """Crea las tablas antes de cada test y las borra al terminar, para que
    ningún test vea datos dejados por otro test anterior.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    """Reemplaza la sesión de base de datos real por la de pruebas."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Le dice a FastAPI: "cada vez que alguien pida get_db, dale esta versión de prueba".
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def db_session():
    """Sesión de base de datos de prueba, para tests que instancian
    repositorios/servicios directamente (sin pasar por HTTP).
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()