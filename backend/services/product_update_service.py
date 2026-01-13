import logging
from backend.models.product import Product
from backend.repositories.product_repository import ProductRepository

logger = logging.getLogger("ecommerce")

class ProductUpdateService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def update_product_details(self, product_id: int, name: str, description: str, price: float, stock: int) -> Product:
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive numeric value")

        existing_product = self.repository.get_product_by_id(product_id)
        if not existing_product:
            raise ValueError("Product not found")

        if not description.strip():
            raise ValueError("Product description cannot be empty or removed")

        updated_product = self.repository.update_product(
            product_id=product_id,
            name=name.strip(),
            description=description.strip(),
            price=price,
            stock=stock
        )
        logger.info("Admin updated product %s (%s)", updated_product.name, updated_product.id)
        return updated_product