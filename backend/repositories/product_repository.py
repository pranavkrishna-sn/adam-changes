import sqlite3
import logging
from typing import Optional, List
from backend.models.product import Product

logger = logging.getLogger("ecommerce")

class ProductRepository:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def create_product(self, product: Product) -> Product:
        query = """
        INSERT INTO products (name, description, price, category_id, stock, created_at, updated_at, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(query, (
                    product.name,
                    product.description,
                    product.price,
                    product.category_id,
                    product.stock,
                    product.created_at,
                    product.updated_at,
                    product.is_active
                ))
                conn.commit()
                product.id = cursor.lastrowid
            logger.info("New product created: %s", product.name)
            return product
        except sqlite3.IntegrityError:
            logger.error("Product creation failed: name '%s' already exists", product.name)
            raise ValueError("Product with this name already exists")

    def get_product_by_name(self, name: str) -> Optional[Product]:
        query = """
        SELECT id, name, description, price, category_id, stock, created_at, updated_at, is_active
        FROM products WHERE name = ?
        """
        with self._get_connection() as conn:
            row = conn.execute(query, (name,)).fetchone()
            if not row:
                return None
            return Product(
                id=row[0], name=row[1], description=row[2], price=row[3],
                category_id=row[4], stock=row[5], created_at=row[6],
                updated_at=row[7], is_active=bool(row[8])
            )

    def list_products(self) -> List[Product]:
        query = """
        SELECT id, name, description, price, category_id, stock, created_at, updated_at, is_active
        FROM products WHERE is_active = 1
        """
        with self._get_connection() as conn:
            results = conn.execute(query).fetchall()
            return [Product(
                id=row[0], name=row[1], description=row[2], price=row[3],
                category_id=row[4], stock=row[5], created_at=row[6],
                updated_at=row[7], is_active=bool(row[8])
            ) for row in results]