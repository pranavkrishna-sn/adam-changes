import pytest
from backend.models.product import Product
from backend.models.category import Category
from backend.services.product_service import ProductService
from backend.repositories.product_repository import ProductRepository
from backend.repositories.category_repository import CategoryRepository

class InMemoryProductRepo(ProductRepository):
    def __init__(self):
        self.products = {}

    def create_product(self, product: Product) -> Product:
        if product.name in self.products:
            raise ValueError("Product with this name already exists")
        product.id = len(self.products) + 1
        self.products[product.name] = product
        return product

    def get_product_by_name(self, name: str):
        return self.products.get(name)

    def list_products(self):
        return list(self.products.values())

class InMemoryCategoryRepo(CategoryRepository):
    def __init__(self):
        self.categories = {1: Category(id=1, name="Electronics", description="Devices")}

    def get_category(self, category_id: int):
        return self.categories.get(category_id)

@pytest.fixture
def product_service():
    product_repo = InMemoryProductRepo()
    category_repo = InMemoryCategoryRepo()
    return ProductService(product_repo, category_repo)

def test_add_product_success(product_service):
    product = product_service.add_product("Phone", "Smartphone with 6GB RAM", 699.99, 1, 10)
    assert product.name == "Phone"
    assert product.price == 699.99

def test_duplicate_product_name(product_service):
    product_service.add_product("Laptop", "Gaming laptop", 1200.0, 1, 5)
    with pytest.raises(ValueError):
        product_service.add_product("Laptop", "Business laptop", 1300.0, 1, 5)

def test_invalid_price(product_service):
    with pytest.raises(ValueError):
        product_service.add_product("Watch", "Smart Watch", -10.0, 1, 3)

def test_missing_category(product_service):
    with pytest.raises(ValueError):
        product_service.add_product("TV", "OLED Smart TV", 1800.0, 99, 3)