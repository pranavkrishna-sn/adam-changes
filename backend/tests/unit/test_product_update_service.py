import pytest
from backend.models.product import Product
from backend.services.product_update_service import ProductUpdateService
from backend.repositories.product_repository import ProductRepository

class InMemoryRepo(ProductRepository):
    def __init__(self):
        self.products = {
            1: Product(id=1, name="Laptop", description="Gaming Laptop", price=1200.0, category_id=1, stock=5)
        }

    def get_product_by_id(self, product_id: int):
        return self.products.get(product_id)

    def update_product(self, product_id: int, name: str, description: str, price: float, stock: int):
        product = self.products.get(product_id)
        if not product:
            raise ValueError("Product not found")
        product.name = name
        product.description = description
        product.price = price
        product.stock = stock
        self.products[product_id] = product
        return product

@pytest.fixture
def service():
    repo = InMemoryRepo()
    return ProductUpdateService(repository=repo)

def test_successful_product_update(service):
    product = service.update_product_details(1, "Laptop Pro", "Updated Laptop", 1300.0, 10)
    assert product.name == "Laptop Pro"
    assert product.price == 1300.0

def test_invalid_price_raises_error(service):
    with pytest.raises(ValueError):
        service.update_product_details(1, "Laptop Pro", "Updated Laptop", -5.0, 10)

def test_empty_description_is_not_allowed(service):
    with pytest.raises(ValueError):
        service.update_product_details(1, "Laptop Pro", "", 1300.0, 10)

def test_nonexistent_product_raises_error(service):
    with pytest.raises(ValueError):
        service.update_product_details(99, "Tablet", "New tablet", 300.0, 4)