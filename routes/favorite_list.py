from typing import Union

from fastapi.exceptions import HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query

from auth.converter import RequestAnswer
from auth.jwt_functions import JwtInfo, validation
from database import get_session
from models.models import UsersFavoriteFood, UsersFavoriteSet, Set, Food
from fastapi import Request


favorite_list_rout = APIRouter(
    prefix="/commands/favoritelist",
    tags=["usercomands"]
)


@favorite_list_rout.post("/add")
async def add_food_to_favorite_list(food_id: int, session: AsyncSession = Depends(get_session),
                                    type_food: str = Query(
                                    None,
                                    title="Type of food",
                                    description="Choose from food, set"),
                                    jwt_info: Union[JwtInfo, HTTPException] = Depends(validation)):
    tables = {"food": UsersFavoriteFood, "set": UsersFavoriteSet}
    try:
        stmt = insert(tables[type_food]).values({
            "user_id": jwt_info.id,
            type_food + "_id": food_id,
        })
        await session.execute(stmt)
        await session.commit()
    except:
        return HTTPException(status_code=500, detail="food or user is not be")


@favorite_list_rout.get("/show")
async def watch_list(session: AsyncSession = Depends(get_session),
                     jwt_info: Union[JwtInfo, HTTPException] = Depends(validation)):
    query_set = select(UsersFavoriteSet.set_id).filter(UsersFavoriteSet.user_id == jwt_info.id)
    list_set = await session.execute(query_set)
    list_set = list_set.scalars().all()

    query_set = select(Set).filter(Set.id.in_(list_set))
    list_set = await session.execute(query_set)
    list_set = list_set.scalars().all()

    query_food = select(UsersFavoriteFood.food_id).filter(UsersFavoriteFood.user_id == jwt_info.id)
    list_food = await session.execute(query_food)
    list_food = list_food.scalars().all()

    query_food = select(Food).filter(Food.id.in_(list_food))
    list_food = await session.execute(query_food)
    list_food = list_food.scalars().all()

    return RequestAnswer(detail=list_set + list_food, status_code=200)


@favorite_list_rout.delete("/product")
async def delete_product_from_favorite_list(food_id: int, session: AsyncSession = Depends(get_session),
                                            type_food: str = Query(
                                                None,
                                                title="Type of food",
                                                description="Choose from food, set"),
                                            jwt_info: Union[JwtInfo, HTTPException] = Depends(validation)):
    tables = {"food": UsersFavoriteFood, "set": UsersFavoriteSet}
    parametres = {"food": UsersFavoriteFood.food_id, "set": UsersFavoriteSet.set_id}

    query_set = delete(tables[type_food]).filter(parametres[type_food] == food_id).filter(tables[type_food].user_id == jwt_info.id)
    await session.execute(query_set)
    await session.commit()
