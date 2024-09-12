from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from .schemas.item import Item, ItemCreate
from .schemas.category import Category, CategoryCreate
from .models.category import Base
from .controllers import crud
from .database import engine, get_db

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/categories/", response_model=Category)
async def create_categoria(categoria: CategoryCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_categoria(db, categoria)

@app.get("/categories/", response_model=list[Category])
async def read_categories(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_categories(db, skip=skip, limit=limit)

@app.get("/categories/{categoria_id}", response_model=Category)
async def read_category(categoria_id: int, db: AsyncSession = Depends(get_db)):
    categoria = await crud.get_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Category not found")
    return categoria

@app.put("/categories/{categoria_id}", response_model=Category)
async def update_category(categoria_id: int, categoria_update: CategoryCreate, db: AsyncSession = Depends(get_db)):
    categoria = await crud.update_categoria(db, categoria_id, categoria_update)
    if not categoria:
        raise HTTPException(status_code=404, detail="Category not found")
    return categoria

@app.post("/items/", response_model=Item)
async def create_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_item(db, item)

@app.get("/items/", response_model=list[Item])
async def read_itens(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_itens(db, skip=skip, limit=limit)


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, item_update: ItemCreate, db: AsyncSession = Depends(get_db)):
    item = await crud.update_item(db, item_id, item_update)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/categories/{categoria_id}", response_model=Category)
async def delete_categoria(categoria_id: int, db: AsyncSession = Depends(get_db)):
    categoria = await crud.delete_categoria(db, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Category not found")
    return categoria

@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await crud.delete_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item