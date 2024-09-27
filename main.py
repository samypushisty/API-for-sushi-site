

from fastapi import FastAPI
from authroutes import authrouter
from interfacerouts import interfacerouter

app = FastAPI(
    title="Trading App"
)


app.include_router(authrouter)
app.include_router(interfacerouter)