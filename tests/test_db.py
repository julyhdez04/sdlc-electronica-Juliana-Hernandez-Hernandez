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


