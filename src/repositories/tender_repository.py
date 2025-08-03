import sqlite3
from typing import List, Dict
from src.config import DB_PATH


class TenderRepository:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS tenders (
                        number TEXT PRIMARY KEY,
                        link TEXT,
                        goods_description TEXT,
                        organizer TEXT,
                        publish_date TEXT,
                        end_date TEXT
                    )
                """)
                conn.commit()
        except Exception as e:
            raise RuntimeError(f"Ошибка при инициализации базы данных: {e}")

    def save_tenders(self, tenders: List[Dict]):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                for t in tenders:
                    try:
                        cur.execute(
                            """
                            INSERT OR IGNORE INTO tenders 
                            (number, link, goods_description, organizer, publish_date, end_date)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """,
                            (t['number'], t['link'], t['goods_description'], t['organizer'], t['publish_date'], t['end_date'])
                        )
                    except Exception as e:
                        raise RuntimeError(f"Ошибка при сохранении тендера {t.get('number')}: {e}")
                conn.commit()
        except Exception as e:
            raise RuntimeError(f"Ошибка при сохранении тендеров в БД: {e}")

    def get_all_tenders(self) -> List[Dict]:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cur = conn.cursor()
                cur.execute("SELECT number, link, goods_description, organizer, publish_date, end_date FROM tenders")
                rows = cur.fetchall()
                return [
                    {
                        "number": r[0],
                        "link": r[1],
                        "goods_description": r[2],
                        "organizer": r[3],
                        "publish_date": r[4],
                        "end_date": r[5],
                    }
                    for r in rows
                ]
        except Exception as e:
            raise RuntimeError(f"Ошибка при чтении тендеров из БД: {e}")
