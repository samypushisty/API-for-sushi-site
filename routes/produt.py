from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from auth.converter import RequestAnswer, tojson
from data_base import get_session
from models.models import Food, Set, FoodInSet



product_rout = APIRouter(
    prefix="/commands/product",
    tags=["product"]
)


@product_rout.get("/food")
async def food_get(food_id: int, session: AsyncSession = Depends(get_session)):
    try:
        query_set = select(Food).filter(Food.id == food_id)
        food = await session.execute(query_set)
        food = food.scalars().first()
        print("vlad")
        return RequestAnswer(detail=food, status_code=200)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()


@product_rout.get("/set")
async def sushi_set_get(set_id: int, session: AsyncSession = Depends(get_session)):
    try:
        query_set = select(Set).filter(Set.id == set_id)
        sushi_set = await session.execute(query_set)
        sushi_set = tojson(sushi_set.scalars().first())
        query_food_in_set = select(FoodInSet.food_id).filter(FoodInSet.set_id == set_id)
        food_in_set = await session.execute(query_food_in_set)
        sushi_set["food_in_set"] = food_in_set.scalars().all()
        return RequestAnswer(detail=sushi_set, status_code=200)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()


@product_rout.get("/upload_image")
async def upload_image(food_id: int, type_food: str):
    try:
        file_path = f"images/{type_food+"_"+str(food_id)+".jpg"}"
         # Алекс нужен хеш удОли headers={"Cache-Control": "no-cache, no-store, must-revalidate"
        print("upload")
        return FileResponse(file_path, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")