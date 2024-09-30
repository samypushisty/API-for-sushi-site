

from fastapi import FastAPI
from routes.auth import authrouter
from routes.favorite_list import favorite_list_rout
from routes.basket import basket_rout

app = FastAPI(
    title="Trading App"
)


app.include_router(authrouter)
app.include_router(favorite_list_rout)
app.include_router(basket_rout)
