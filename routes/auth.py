from datetime import timedelta

from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from auth.check_commands import check_value
from auth.converter import RequestAnswer
from auth.hash_password import hash_password, check_password
from auth.jwt_functions import create_jwt
from models.models import Users
from datafunctions import naive_utcnow
from sqlalchemy import insert, select
from fastapi import APIRouter, Depends, Response
from models.schemes import User, UserSignIn
from database import get_session


authrouter = APIRouter(
    prefix="/auth",
    tags=["registration"]
)


@authrouter.post("/registration")
async def registration(
        user: User,
        session: AsyncSession = Depends(get_session)):
    try:
        user = user.dict()
        user["registered_at"] = naive_utcnow()
        user["password"] = hash_password(user["password"])
        stmt = insert(Users).values(**user)
        await session.execute(stmt)
        await session.commit()
    except:
        return HTTPException(status_code=500, detail="emeil or username or number is be")



@authrouter.post("/signin")
async def signin(user_sign_in: UserSignIn,
                 response: Response,
                 session: AsyncSession = Depends(get_session)):
    token_expiration = timedelta(minutes=30)
    query = select(Users).where(Users.email == user_sign_in.email)
    user_information = await session.execute(query)
    user_information = user_information.scalars().first()
    if user_information:
        if check_password(user_information.password, user_sign_in.password):
            response.set_cookie(
                key="jwt",
                value=create_jwt(user_information.username, user_information.id),
                httponly=True,
                secure=True,
                samesite="None",
                max_age=int(token_expiration.total_seconds()),
                expires=int(token_expiration.total_seconds()),
            )
        else:
            return HTTPException(status_code=500, detail="invalid passport")
    else:
        return HTTPException(status_code=500, detail="invalid email")
