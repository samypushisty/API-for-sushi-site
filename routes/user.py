from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from auth.check_commands import check_value, check_mail
from auth.converter import RequestAnswer
from auth.hash_password import hash_password
from auth.jwt_functions import JwtInfo, validation
from models.models import Users
from sqlalchemy import select
from fastapi import APIRouter, Depends
from database import get_session
from fastapi import Query
from typing import Union


userrouter = APIRouter(
    prefix="/user",
    tags=["user"]
)


@userrouter.get("/showinfo")
async def showinfo(session: AsyncSession = Depends(get_session),
                   jwt_info: Union[JwtInfo, HTTPException] = Depends(validation)):

    query_set = select(Users).filter(Users.id == jwt_info.id)
    user = await session.execute(query_set)
    user = user.scalars().first()
    return RequestAnswer(detail=user, status_code=200)



@userrouter.get("/aviability")
async def aviability(value: str,
                     arg: str = Query(
                                    None,
                                    title="attribute",
                                    description="email, number, username"),
                     session: AsyncSession = Depends(get_session)):
    if arg in ["email", "number", "username"]:
        result = await check_value(session=session, argument=arg, value=value)
        return RequestAnswer(detail=result, status_code=200)
    else:
        return HTTPException(status_code=500, detail="you have not permission")


@userrouter.post("/changeinfo")
async def changeinfo(value: str, attribute: str = Query(
                                    None,
                                    title="attribute",
                                    description="email, addresses, number, username"),
                     session: AsyncSession = Depends(get_session),
                     jwt_info: Union[JwtInfo, HTTPException] = Depends(validation)):
    valid_attributes = ["email", "addresses", "number", "username"]
    if attribute in valid_attributes:
        if await check_value(session=session, value=value, argument=attribute):
            return RequestAnswer(detail="wrong value", status_code=200)
        query = select(Users).filter(Users.id == jwt_info.id)
        user = await session.execute(query)
        user = user.scalars().first()
        setattr(user, attribute, value)
        await session.commit()
    else:
        return HTTPException(status_code=500, detail="wrong attribute")


@userrouter.post("/changepassword")
async def change_password(email: str, password: str,
                          session: AsyncSession = Depends(get_session)):
    password = hash_password(password)
    permission = await check_mail(session=session, email=email)
    if permission:
        query = select(Users).filter(Users.email == email)
        user = await session.execute(query)
        user = user.scalars().first()
        user.password = password
        await session.commit()

