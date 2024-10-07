

from fastapi import FastAPI
from routes.auth import authrouter
from routes.favorite_list import favorite_list_rout
from starlette.middleware.cors import CORSMiddleware
from routes.basket import basket_rout
import uvicorn

from routes.produt import product_rout
from routes.user import userrouter

app = FastAPI(
    title="Trading App"
)
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