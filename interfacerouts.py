from fastapi.exceptions import HTTPException
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query
from auth.jwt_functions import JwtInfo
from data_base import get_session
from models.models import UsersFavoriteFood, UsersFavoriteSet
from fastapi import Request

interfacerouter = APIRouter(
    prefix="/commands",
    tags=["usercomands"]
)


@interfacerouter.post("/addfoodtofavoritelist")
async def addbooktofavoritelist(food_id: int, request: Request, session: AsyncSession = Depends(get_session),
                                type_food: str = Query(
                                    None,
                                    title="Type of food",
                                    description="Choose from food, set")):
    jwt_info = JwtInfo(request.cookies.get("jwt"))
    tables = {"food": UsersFavoriteFood, "set": UsersFavoriteSet}
    if jwt_info.valid:
        try:
            stmt = insert(tables[type_food]).values({
                "user_id": jwt_info.id,
                type_food + "_id": food_id,
            })
            await session.execute(stmt)
            await session.commit()
        except:
            return HTTPException(status_code=500, detail="food or user is not be")
    else:
        return HTTPException(status_code=500, detail=jwt_info.info_except)
