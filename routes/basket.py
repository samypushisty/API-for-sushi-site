from fastapi.exceptions import HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query
from auth.jwt_functions import JwtInfo
from data_base import get_session
from models.models import Basket, Food, Set, UsersHistory
from fastapi import Request


basket_rout = APIRouter(
    prefix="/commands/basket",
    tags=["usercomands"]
)


@basket_rout.post("/addfood")
async def add_food_to_basket(food_id: int, request: Request, session: AsyncSession = Depends(get_session),
                                type_food: str = Query(
                                    None,
                                    title="Type of food",
                                    description="Choose from food, set")):
    jwt_info = JwtInfo(request.cookies.get("jwt"))
    tables = {"food": Food, "set": Set}
    try:
        if jwt_info.valid:
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
                return price
            else:
                return HTTPException(status_code=500, detail="food is not be")
        else:
            return HTTPException(status_code=500, detail=jwt_info.info_except)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()


@basket_rout.get("/show")
async def watch_basket(request: Request, session: AsyncSession = Depends(get_session)):
    jwt_info = JwtInfo(request.cookies.get("jwt"))
    try:
        if jwt_info.valid:

            query_set = select(Basket).filter(Basket.user_id == jwt_info.id)
            food = await session.execute(query_set)
            food = food.scalars().all()
            return food
        else:
            return HTTPException(status_code=500, detail=jwt_info.info_except)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()


@basket_rout.delete("/product")
async def delete_product_from_basket(id: int, request: Request, session: AsyncSession = Depends(get_session)):
    jwt_info = JwtInfo(request.cookies.get("jwt"))
    try:
        if jwt_info.valid:
            query_set = delete(Basket).filter(Basket.id == id)
            await session.execute(query_set)
            await session.commit()
            return "product delete"
        else:
            return HTTPException(status_code=500, detail=jwt_info.info_except)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()


@basket_rout.post("/buy")
async def buy(request: Request, session: AsyncSession = Depends(get_session)):
    jwt_info = JwtInfo(request.cookies.get("jwt"))
    try:
        if jwt_info.valid:
            query_set = select(Basket).filter(Basket.user_id == jwt_info.id)
            food = await session.execute(query_set)
            food = food.scalars().all()
            if food:
                result = {
                    "user_id": jwt_info.id,
                    "list_food": "",
                    "list_set": "",
                    "total_price": 0
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
        else:
            return HTTPException(status_code=500, detail=jwt_info.info_except)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()


@basket_rout.get("/history")
async def watch_history(request: Request, session: AsyncSession = Depends(get_session)):
    jwt_info = JwtInfo(request.cookies.get("jwt"))
    try:
        if jwt_info.valid:
            query_set = select(UsersHistory).filter(UsersHistory.user_id == jwt_info.id)
            result = await session.execute(query_set)
            result = result.scalars().all()
            return result
        else:
            return HTTPException(status_code=500, detail=jwt_info.info_except)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()
