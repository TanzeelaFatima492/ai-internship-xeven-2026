from pydantic import BaseModel, field_validator
from typing import List

class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool
    tags: List[str]

    @field_validator('price')
    @classmethod
    def check_price(cls, v):
        if v < 0:
            raise ValueError("Price must be >= 0")
        return v


# ✅ TEST DATA (THIS PRODUCES OUTPUT)
p = Product(
    id=1,
    name="Laptop",
    price=999.99,
    in_stock=True,
    tags=["electronics", "computer"]
)

print(p)
print(p.model_dump())   # JSON-like output