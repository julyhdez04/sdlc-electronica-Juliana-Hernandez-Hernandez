from app.db import get_db


def test_get_db_yields_and_closes_session():
    """Ejercita get_db() directamente como generador, para cubrir tanto
    el yield de la sesión como el finally que la cierra. No modifica
    ningún dato: solo abre y cierra la conexión.
    """
    generator = get_db()

    db = next(generator)
    assert db is not None

    # Al agotar el generador, se dispara el bloque finally (db.close()).
    try:
        next(generator)
    except StopIteration:
        pass

def test_get_database_url_postgres_legacy(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgres://user:pass@localhost/db")
    from app.db import get_database_url
    assert get_database_url() == "postgresql+psycopg://user:pass@localhost/db"


def test_get_database_url_postgresql_sin_driver(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost/db")
    from app.db import get_database_url
    assert get_database_url() == "postgresql+psycopg://user:pass@localhost/db"


