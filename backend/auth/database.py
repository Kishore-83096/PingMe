import psycopg

from config import DATABASE_URL


def check_database_connection():
    """
    Checks whether PingMe can successfully connect to Neon PostgreSQL.

    SELECT 1 is used because we only need to verify the database
    connection at this stage.
    """
    try:
        with psycopg.connect(
            DATABASE_URL,
            connect_timeout=5,
        ) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return True

    except psycopg.Error:
        return False