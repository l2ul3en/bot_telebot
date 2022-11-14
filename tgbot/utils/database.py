"""
    Conexión a PostgreSQL con Python
    Ejemplo de CRUD evitando inyecciones SQL
"""
import psycopg2, json
import tgbot.config as config

class Database:
    def __init__(self):
        self._file = open(config.FILE_DB)
        cred = json.load(self._file)
        self._conn = psycopg2.connect(**cred)

    def get_conn (self):
        return self._conn

    def __del__(self):
        print('Eliminando conexion')
        self._file.close()
        self._conn.close()


if __name__ == '__main__':
    db = Database()
    cursor = db.get_conn().cursor()
    cursor.execute("select * from users")
    for data in cursor.fetchall():
        print(data)
    