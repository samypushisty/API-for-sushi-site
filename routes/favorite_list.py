from fastapi.exceptions import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query
from auth.jwt_functions import JwtInfo
from data_base import get_session
from models.models import UsersFavoriteFood, UsersFavoriteSet
from fastapi import Request


favorite_list_rout = APIRouter(
    prefix="/commands/favoritelist",
    tags=["usercomands"]
)


@favorite_list_rout.post("/add")
async def addbooktofavoritelist(food_id: int, request: Request, session: AsyncSession = Depends(get_session),
                                type_food: str = Query(
                                    None,
                                    title="Type of food",
                                    description="Choose from food, set")):
    jwt_info = JwtInfo(request.cookies.get("jwt"))
    tables = {"food": UsersFavoriteFood, "set": UsersFavoriteSet}
    try:
        if jwt_info.valid:
            stmt = insert(tables[type_food]).values({
                "user_id": jwt_info.id,
                type_food + "_id": food_id,
            })
            await session.execute(stmt)
            await session.commit()
        else:
            return HTTPException(status_code=500, detail=jwt_info.info_except)
    except:
        return HTTPException(status_code=500, detail="food or user is not be")
    finally:
        await session.close()


@favorite_list_rout.get("/show")
async def watch_book(request: Request, session: AsyncSession = Depends(get_session)):
    jwt_info = JwtInfo(request.cookies.get("jwt"))
    try:
        if jwt_info.valid:
            query_set = select(UsersFavoriteSet.set_id).filter(UsersFavoriteSet.user_id == jwt_info.id)
            list_set = await session.execute(query_set)
            list_set = list_set.scalars().all()
            query_food = select(UsersFavoriteFood.food_id).filter(UsersFavoriteFood.user_id == jwt_info.id)
            list_food = await session.execute(query_food)
            list_food = list_food.scalars().all()
            result = {
                "sets": list_set,
                "foods": list_food
                      }
            return result
        else:
            return HTTPException(status_code=500, detail=jwt_info.info_except)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()
