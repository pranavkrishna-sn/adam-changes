from fastapi import APIRouter, HTTPException, Header, status
from backend.config.settings import Settings
from backend.repositories.product_repository import ProductRepository
from backend.services.product_update_service import ProductUpdateService

router = APIRouter()
settings = Settings()
repository = ProductRepository(db_path="database/ecommerce.db")
service = ProductUpdateService(repository=repository)

def verify_admin(api_key: str | None) -> None:
    if not api_key or api_key != settings.admin_api_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin authorization required")

@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    name: str,
    description: str,
    price: float,
    stock: int,
    x_api_key: str | None = Header(default=None)
) -> dict:
    verify_admin(x_api_key)
    try:
        updated_product = service.update_product_details(product_id, name, description, price, stock)
        return {"message": "Product updated successfully", "product": updated_product.dict()}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))