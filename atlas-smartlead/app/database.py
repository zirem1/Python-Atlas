import sqlite3
from config import Config


def get_db():
    """SQLite veritabanına bağlantı açar."""
    connection = sqlite3.connect(Config.DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Lead kayıtlarını tutacak tabloyu oluşturur."""
    connection = get_db()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                company TEXT,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()
    finally:
        connection.close()


def lead_ekle(name, email, company, message):
    """Yeni bir lead kaydını veritabanına ekler."""
    connection = get_db()

    try:
        cursor = connection.execute(
            """
            INSERT INTO leads (name, email, company, message)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, company, message),
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def tum_leadler():
    """Kayıtları en yeniden eskiye doğru getirir."""
    connection = get_db()

    try:
        rows = connection.execute(
            "SELECT * FROM leads ORDER BY created_at DESC, id DESC"
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()
