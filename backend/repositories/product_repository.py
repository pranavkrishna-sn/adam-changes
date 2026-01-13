import sqlite3
import logging
from typing import Optional
from backend.models.product import Product

logger = logging.getLogger("ecommerce")

class ProductRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        query = """
        SELECT id, name, description, price, category_id, stock, created_at, updated_at, is_active
        FROM products WHERE id = ?
        """
        with self._get_connection() as conn:
            row = conn.execute(query, (product_id,)).fetchone()
            if not row:
                return None
            return Product(
                id=row[0],
                name=row[1],
                description=row[2],
                price=row[3],
                category_id=row[4],
                stock=row[5],
                created_at=row[6],
                updated_at=row[7],
                is_active=bool(row[8])
            )

    def update_product(self, product_id: int, name: str, description: str, price: float, stock: int) -> Product:
        query = """
        UPDATE products
        SET name = ?, description = ?, price = ?, stock = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (name, description, price, stock, product_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise ValueError("Product not found")
        logger.info("Product %s updated successfully", product_id)
        return self.get_product_by_id(product_id)