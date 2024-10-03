from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from auth.check_commands import check_value, check_mail
from auth.hash_password import hash_password
from auth.jwt_functions import JwtInfo
from models.models import Users
from sqlalchemy import select
from fastapi import APIRouter, Depends
from data_base import get_session
from fastapi import Request, Query


userrouter = APIRouter(
    prefix="/user",
    tags=["user"]
)


@userrouter.get("/showinfo")
async def showinfo(request: Request,
                   session: AsyncSession = Depends(get_session)):
    jwt_info = JwtInfo(request.cookies.get("jwt"))
    try:
        if jwt_info.valid:

            query_set = select(Users).filter(Users.id == jwt_info.id)
            user = await session.execute(query_set)
            user = user.scalars().all()
            return user
        else:
            return HTTPException(status_code=500, detail=jwt_info.info_except)
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()


@userrouter.get("/aviability")
async def aviability(value: str,
                     arg: str = Query(
                                    None,
                                    title="attribute",
                                    description="email, number, username"),
                     session: AsyncSession = Depends(get_session)):
    try:
        if arg in ["email", "number", "username"]:
            print(1)
            return await check_value(session=session, argument=arg, value=value)
        else:
            return HTTPException(status_code=500, detail="you have not permission")
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()


@userrouter.post("/changeinfo")
async def changeinfo(request: Request, value: str, attribute: str = Query(
                                    None,
                                    title="attribute",
                                    description="email, addresses, number, username"),
                     session: AsyncSession = Depends(get_session)):
    jwt_info = JwtInfo(request.cookies.get("jwt"))
    if attribute == "password":
        value = hash_password(value)

    try:
        if attribute in ["email", "addresses", "number", "username"]:
            if jwt_info.valid:
                query = select(Users).filter(Users.id == jwt_info.id)
                user = await session.execute(query)
                user = user.scalars().first()
                setattr(user, attribute, value)
                await session.commit()
            else:
                return HTTPException(status_code=500, detail=jwt_info.info_except)
        else:
            return HTTPException(status_code=500, detail="wrong attribute")
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()


@userrouter.post("/changepassword")
async def change_password(email: str, password: str,
                          session: AsyncSession = Depends(get_session)):
    password = hash_password(password)
    try:
        permission = await check_mail(session=session, email=email)
        if permission:
            query = select(Users).filter(Users.email == email)
            user = await session.execute(query)
            user = user.scalars().first()
            user.password = password
            await session.commit()
    except Exception as e:
        print(e)
        return HTTPException(status_code=500, detail="something went wrong")
    finally:
        await session.close()
