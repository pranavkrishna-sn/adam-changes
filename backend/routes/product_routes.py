from fastapi import APIRouter, HTTPException, status
from backend.config.settings import Settings
from backend.repositories.product_repository import ProductRepository
from backend.repositories.category_repository import CategoryRepository
from backend.services.product_service import ProductService

router = APIRouter()
settings = Settings()
product_repo = ProductRepository(db_path="database/ecommerce.db")
category_repo = CategoryRepository(db_path="database/ecommerce.db")
service = ProductService(product_repo, category_repo)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_product(name: str, description: str, price: float, category_id: int, stock: int = 0):
    try:
        product = service.add_product(name, description, price, category_id, stock)
        return {"message": "Product added successfully", "product": product.dict()}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", status_code=status.HTTP_200_OK)
async def list_products():
    products = service.list_all_products()
    return {"products": [p.dict() for p in products]}