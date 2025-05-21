from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    description: str | None = None

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: str | None = None
    description: str | None = None

class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True # This allows the model to work with ORM objects