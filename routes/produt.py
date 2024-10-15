from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query
from fastapi.responses import FileResponse
from auth.converter import RequestAnswer, tojson
from database import get_session
from models.models import Food, Set, FoodInSet

redis = {
    "set": [],
    "sushi": [],
    "drink": [],
    "sauce": []
}


async def reload_book_bd_id(session: AsyncSession):
    global redis
    for i in ["sushi", "drink", "sauce"]:
        query = select(Food.id).filter(Food.type == i)
        result = await session.execute(query)
        redis[i] = result.scalars().all()
    query = select(Set.id)
    result = await session.execute(query)
    redis["set"] = result.scalars().all()
    for i in redis:
        print(redis[i])


product_rout = APIRouter(
    prefix="/commands/product",
    tags=["product"]
)


@product_rout.get("/food")
async def food_get(food_id: int, session: AsyncSession = Depends(get_session)):
    query_set = select(Food).filter(Food.id == food_id)
    food = await session.execute(query_set)
    food = food.scalars().first()
    if food:
        return RequestAnswer(detail=food, status_code=200)
    else:
        return RequestAnswer(detail="None id", status_code=200)


@product_rout.get("/set")
async def sushi_set_get(set_id: int, session: AsyncSession = Depends(get_session)):
    query_set = select(Set).filter(Set.id == set_id)
    sushi_set = await session.execute(query_set)
    sushi_set = sushi_set.scalars().first()
    if sushi_set:
        sushi_set = tojson(sushi_set)
        query_food_in_set = select(FoodInSet.food_id).filter(FoodInSet.set_id == set_id)
        food_in_set = await session.execute(query_food_in_set)
        sushi_set["food_in_set"] = food_in_set.scalars().all()
        return RequestAnswer(detail=sushi_set, status_code=200)
    else:
        return RequestAnswer(detail="None id", status_code=200)


@product_rout.get("/upload_image")
async def upload_image(food_id: int, type_food: str):
    try:
        file_path = f"images/{type_food+"_"+str(food_id)+".jpg"}"
        return FileResponse(file_path, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")


@product_rout.get("/foods/{page}")
async def eight_food(page: int,
                     type_food: str = Query(None,
                                            title="Type of food",
                                            description="Choose from sushi, drink, sauce"),
                     session: AsyncSession = Depends(get_session)):
    tables = {"set": Set, "sushi": Food, "drink": Food, "sauce": Food}
    if page * 8 - 8 < len(redis[type_food]):
        if page * 8 < len(redis[type_food]):
            first_id = page * 8 - 8
            last_id = page * 8 - 1
        else:
            first_id = page * 8 - 8
            last_id = len(redis[type_food]) - 1

        print(redis[type_food][first_id:last_id+1])
        query = select(tables[type_food]).filter(tables[type_food].id.in_(redis[type_food][first_id:last_id+1]))
        result = await session.execute(query)
        result = result.scalars().all()
        return RequestAnswer(detail=result, status_code=200)
    else:
        return RequestAnswer(detail="page not found", status_code=200)
