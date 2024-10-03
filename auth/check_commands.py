from fastapi.exceptions import HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from auth.jwt_functions import JwtInfo
from data_base import get_session
from models.models import Users
from fastapi import Request
import asyncio


async def check_value(session: AsyncSession, argument: str, value: str):
    try:
        query = select(Users).filter(getattr(Users, argument) == value)
        value = await session.execute(query)
        value = value.scalars().first()
        return bool(value)
    except Exception as e:
        print(e)
        return False


async def check_mail(session: AsyncSession, email: str):
    try:
        if await check_value(session=session, argument="email", value=email):
            await asyncio.sleep(10)
            # отправка сообщения на email
            return True
    except Exception as e:
        print(e)
        return False