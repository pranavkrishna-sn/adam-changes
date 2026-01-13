import sqlite3
import logging
from typing import Optional
from backend.models.category import Category

logger = logging.getLogger("ecommerce")

class CategoryRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_category(self, category_id: int) -> Optional[Category]:
        query = "SELECT id, name, description, created_at, updated_at FROM categories WHERE id = ?"
        with self._get_connection() as conn:
            row = conn.execute(query, (category_id,)).fetchone()
            if not row:
                return None
            return Category(id=row[0], name=row[1], description=row[2], created_at=row[3], updated_at=row[4])