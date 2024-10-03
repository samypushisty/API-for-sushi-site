from fastapi.exceptions import HTTPException
from sqlalchemy import insert, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query
from auth.jwt_functions import JwtInfo
from data_base import get_session
from models.models import Basket, Food, Set, UsersHistory
from fastapi import Request


product_rout = APIRouter(
    prefix="/commands/product",
    tags=["usercomands"]
)





