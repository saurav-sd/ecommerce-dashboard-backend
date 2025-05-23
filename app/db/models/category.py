from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True, unique=True)
    description = Column(String(255), nullable=True)

    products = relationship("Product", back_populates="category")

