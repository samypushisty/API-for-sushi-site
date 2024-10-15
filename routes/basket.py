from typing import Union

from fastapi.exceptions import HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query

from auth.converter import RequestAnswer
from auth.jwt_functions import JwtInfo, validation
from database import get_session
from models.models import Basket, Food, Set, UsersHistory

basket_rout = APIRouter(
    prefix="/commands/basket",
    tags=["usercomands"]
)


@basket_rout.post("/addfood")
async def add_food_to_basket(food_id: int, session: AsyncSession = Depends(get_session),
                             type_food: str = Query(
                                 None,
                                 title="Type of food",
                                 description="Choose from food, set"),
                             jwt_info: Union[JwtInfo, HTTPException] = Depends(validation)):
    tables = {"food": Food, "set": Set}
    try:
        query_set = select(tables[type_food]).filter(tables[type_food].id == food_id)
        food = await session.execute(query_set)
        food = food.scalars().first()
        if food:
            price = food.price
            stmt = insert(Basket).values({
                "user_id": jwt_info.id,
                "food_id": food_id,
                "type": type_food,
                "price": price
            })
            await session.execute(stmt)
            await session.commit()
        else:
            return HTTPException(status_code=500, detail="food is not be")
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")


@basket_rout.get("/show")
async def watch_basket(session: AsyncSession = Depends(get_session),
                       jwt_info: Union[JwtInfo, HTTPException] = Depends(validation)):
    query_set = select(Basket).filter(Basket.user_id == jwt_info.id)
    food = await session.execute(query_set)
    food = food.scalars().all()
    return RequestAnswer(detail=food, status_code=200)


@basket_rout.delete("/product")
async def delete_product_from_basket(id: int, session: AsyncSession = Depends(get_session),
                                     jwt_info: Union[JwtInfo, HTTPException] = Depends(validation)):
    query_set = delete(Basket).filter(Basket.id == id).filter(Basket.user_id == jwt_info.id)
    await session.execute(query_set)
    await session.commit()


@basket_rout.post("/buy")
async def buy(address: str, session: AsyncSession = Depends(get_session),
              jwt_info: Union[JwtInfo, HTTPException] = Depends(validation)):
    try:
        query_set = select(Basket).filter(Basket.user_id == jwt_info.id)
        food = await session.execute(query_set)
        food = food.scalars().all()
        if food:
            result = {
                "user_id": jwt_info.id,
                "list_food": "",
                "list_set": "",
                "total_price": 0,
                "address": address
            }
            for i in food:
                result["list_" + i.type] += " " + str(i.food_id)
                result["total_price"] += i.price
            stmt = insert(UsersHistory).values(result)
            await session.execute(stmt)
            await session.commit()
            query_del = delete(Basket).filter(Basket.user_id == jwt_info.id)
            await session.execute(query_del)
            await session.commit()
        else:
            return HTTPException(status_code=500, detail="food is not be")
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")


@basket_rout.get("/history")
async def watch_history(session: AsyncSession = Depends(get_session),
                        jwt_info: Union[JwtInfo, HTTPException] = Depends(validation)):
    query_set = select(UsersHistory).filter(UsersHistory.user_id == jwt_info.id)
    result = await session.execute(query_set)
    result = result.scalars().all()
    return RequestAnswer(detail=result, status_code=200)
