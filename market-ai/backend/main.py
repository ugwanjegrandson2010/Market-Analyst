from fastapi import FastAPI

from app.services.api.market import router as market_router

app = FastAPI(
    title="Market AI",
    version="1.0.0",
 )

app.include_router(
        market_router,
        prefix = "/api"
)



