import sqlite3, datetime
from ..dependencies import get_db_path

class LinkDAO:
    def __init__(self):
        self.db_path = get_db_path()
        self._init_db()

    def _init_db(self):
        with self._get_connection() as con:
            con.cursor().execute("""CREATE TABLE IF NOT EXISTS links(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                original_url VARCHAR(100),
                short_alias VARCHAR(50) UNIQUE,
                clicks INTEGER,
                created_at DATE
            )""")
            con.commit()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    #crud
    def create_link(self, original_url, short_alias):
        with self._get_connection() as con:
            con.cursor().execute("""INSERT INTO links(original_url, short_alias, clicks, created_at)
                VALUES (?, ?, ?, ?)
            """, (str(original_url), short_alias, 0, datetime.datetime.now().strftime("%Y-%m-%d")))
            con.commit()

    def get_all_links(self):
        with self._get_connection() as con:
            res = con.cursor().execute("SELECT * FROM links").fetchall()
            print(res)
            links = []
            for l in res:
                links.append({
                    "id": l[0],
                    "original_url": l[1],
                    "short_alias": l[2],
                    "clicks": l[3],
                    "created_at": l[4]
                })
            return links
    
    def get_link_by_id(self, id):
        with self._get_connection() as con:
            con.cursor().execute("SELECT * FROM links WHERE id = ?", (id,))
            return con.cursor().fetchone()

    def delete_by_id(self,id):
        with self._get_connection() as con:
            con.cursor().execute("DELETE FROM links WHERE id = ?", (id,))
            con.commit()

    def get_url_by_alias(self, short_alias: str):
        with self._get_connection() as con:
            res = con.cursor().execute("SELECT original_url, clicks FROM links WHERE short_alias = ?", (short_alias,)).fetchone()
            
            if res is None:
                return None

            return res
            
    def update_clicks(self, clicks, short_alias):
        with self._get_connection() as con:
            con.cursor().execute("UPDATE links SET clicks = ? WHERE short_alias = ?", (int(clicks) + 1, short_alias))
            con.commit()