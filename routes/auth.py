from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from auth.hash_password import hash_password, check_password
from auth.jwt_functions import create_jwt
from models.models import Users
from datafunctions import naive_utcnow
from sqlalchemy import insert, select
from fastapi import APIRouter, Depends, Response
from models.schemes import User, UserSignIn
from data_base import get_session



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
        query = select(Users).where(Users.email == user["email"])
        try:
            await session.execute(query)
        except:
            return HTTPException(status_code=500, detail="email be is")
        query = select(Users).where(Users.username == user["username"])
        try:
            await session.execute(query)
        except:
            return HTTPException(status_code=500, detail="username be is")
    finally:
        await session.close()


@authrouter.post("/signin")
async def signin(user_sign_in: UserSignIn,
                 response: Response,
                 session: AsyncSession = Depends(get_session)):
    try:
        query = select(Users).where(Users.email == user_sign_in.email)
        user_information = await session.execute(query)
        user_information = user_information.scalars().first()
        if user_information:
            if check_password(user_information.password, user_sign_in.password):
                response.set_cookie(key="jwt", value=create_jwt(user_information.username, user_information.id))
                return "jwt in cookie"
            else:
                return HTTPException(status_code=500, detail="invalid passport")
        else:
            return HTTPException(status_code=500, detail="invalid email")
    except:
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        print(type(session))
        await session.close()

