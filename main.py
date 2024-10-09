from fastapi import FastAPI

from data_base import get_session
from routes.auth import authrouter
from routes.favorite_list import favorite_list_rout
from starlette.middleware.cors import CORSMiddleware
from routes.basket import basket_rout
import uvicorn
from sqlalchemy.ext.asyncio import AsyncSession
from routes.produt import product_rout, reload_book_bd_id
from routes.user import userrouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


app = FastAPI(
    title="Trading App"
)


async def startup_event():
    async for session in get_session():
        await reload_book_bd_id(session=session)

app.add_event_handler("startup", startup_event)





origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(authrouter)
app.include_router(userrouter)
app.include_router(product_rout)
app.include_router(favorite_list_rout)
app.include_router(basket_rout)



if __name__ == "__main__":
    uvicorn.run(
        "main:app", reload=True, port=8000
    )