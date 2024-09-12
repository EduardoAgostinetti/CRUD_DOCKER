from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.category import Category
from ..schemas.category import CategoryCreate
from ..models.item import Item
from ..schemas.item import ItemCreate


async def get_categoria(db: AsyncSession, categoria_id: int):
    result = await db.execute(select(Category).filter(Category.id == categoria_id))
    return result.scalars().first()

async def create_categoria(db: AsyncSession, categoria: CategoryCreate):
    db_categoria = Category(**categoria.dict())
    db.add(db_categoria)
    await db.commit()
    await db.refresh(db_categoria)
    return db_categoria

async def update_categoria(db: AsyncSession, categoria_id: int, categoria_update: CategoryCreate):
    # Buscar a categoria existente
    result = await db.execute(select(Category).filter(Category.id == categoria_id))
    categoria = result.scalars().first()
    
    if not categoria:
        return None
    
    # Atualizar os campos da categoria
    for key, value in categoria_update.dict().items():
        setattr(categoria, key, value)
    
    # Salvar as alterações
    db.add(categoria)
    await db.commit()
    await db.refresh(categoria)
    
    return categoria

async def create_item(db: AsyncSession, item: ItemCreate):
    db_item = Item(**item.dict())
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

async def get_itens(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return result.scalars().all()

async def get_item(db: AsyncSession, item_id: int):
    result = await db.execute(select(Item).filter(Item.id == item_id))
    return result.scalars().first()

async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Category).offset(skip).limit(limit))
    return result.scalars().all()

async def update_item(db: AsyncSession, item_id: int, item_update: ItemCreate):
    # Buscar o item existente
    result = await db.execute(select(Item).filter(Item.id == item_id))
    item = result.scalars().first()
    
    if not item:
        return None
    
    # Atualizar os campos do item
    for key, value in item_update.dict().items():
        setattr(item, key, value)
    
    # Salvar as alterações
    db.add(item)
    await db.commit()
    await db.refresh(item)
    
    return item

async def delete_categoria(db: AsyncSession, categoria_id: int):
    async with db.begin():
        try:
            # Buscar a categoria existente
            result = await db.execute(select(Category).filter(Category.id == categoria_id))
            categoria = result.scalars().first()
            if not categoria:
                return None
            # Deletar a categoria
            await db.delete(categoria)
            await db.commit()
            return categoria
        except NoResultFound:
            return None

async def delete_item(db: AsyncSession, item_id: int):
    async with db.begin():
        try:
            # Buscar o item existente
            result = await db.execute(select(Item).filter(Item.id == item_id))
            item = result.scalars().first()
            if not item:
                return None
            # Deletar o item
            await db.delete(item)
            await db.commit()
            return item
        except NoResultFound:
            return None