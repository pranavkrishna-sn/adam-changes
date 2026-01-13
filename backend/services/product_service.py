import logging
from backend.models.product import Product
from backend.repositories.product_repository import ProductRepository
from backend.repositories.category_repository import CategoryRepository

logger = logging.getLogger("ecommerce")

class ProductService:
    def __init__(self, product_repo: ProductRepository, category_repo: CategoryRepository) -> None:
        self.product_repo = product_repo
        self.category_repo = category_repo

    def add_product(self, name: str, description: str, price: float, category_id: int, stock: int) -> Product:
        if price <= 0:
            raise ValueError("Product price must be a positive number")
        if not description.strip():
            raise ValueError("Product description cannot be empty")
        if self.product_repo.get_product_by_name(name):
            raise ValueError("Product name must be unique")
        if not self.category_repo.get_category(category_id):
            raise ValueError("Category not found")

        product = Product(
            name=name,
            description=description,
            price=price,
            category_id=category_id,
            stock=stock
        )
        created_product = self.product_repo.create_product(product)
        logger.info("Product '%s' added successfully", created_product.name)
        return created_product

    def list_all_products(self):
        return self.product_repo.list_products()