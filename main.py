"""main.py

This module is entry point into fast api application
"""

from fastapi import FastAPI, status, Depends, HTTPException
from sqlalchemy.orm import Session
from view_models import ProductRequestModel, ProductResponseModel
from database import Base, SessionLocal, engine
from schema import Product


# now ensure all the tables are created
Base.metadata.create_all(bind=engine)


# Get database
async def get_db():
    """
    This method gets the database connection
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# application object
app = FastAPI(
    title="Inventory Service",
    summary="Inventory Service for learning Fast API",
    version="1.0.0",
)


@app.post("/products", status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductRequestModel, db: Session = Depends(get_db)
) -> ProductResponseModel:
    """Ths api will create product"""
    # store the product in database
    db_product = Product(
        name=product.name,
        sku=product.sku,
        price=product.price,
        stock=product.stock,
        description=product.description,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    # generate a response
    return db_product


@app.delete("/products/{id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    """This method deletes the product based on id

    Args:
        product_id (int): product id
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: Not Found

    Returns:
        message
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted"}


@app.get("/products/")
async def get_products(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
) -> list[ProductResponseModel]:
    """This method returns products

    Args:
        skip (int, optional): _description_. Defaults to 0.
        limit (int, optional): _description_. Defaults to 10.
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        list[ProductResponseModel]: _description_
    """
    products = db.query(Product).offset(skip).limit(limit).all()
    return products


@app.get("/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductResponseModel:
    """This method returns the product by id

    Args:
        product_id (int): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        ProductResponseModel: _description_
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}")
async def update_product(
    product_id: int, product: ProductRequestModel, db: Session = Depends(get_db)
) -> ProductResponseModel:
    """This method updates the produc

    Args:
        product_id (int): _description_
        product (ProductRequestModel): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        ProductResponseModel: _description_
    """
    queried_product = db.query(Product).filter(Product.id == product_id).first()
    if queried_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    queried_product.name = product.name
    queried_product.price = product.price
    queried_product.stock = product.stock
    queried_product.sku = product.sku
    queried_product.description = product.description
    db.commit()
    db.refresh(queried_product)
    return queried_product
