"""
main
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from src.config.constants import APP_CONTEXT_PATH, APP_CONTEXT_PATH_v2
from src.versions.v1 import main as v1_route
from src.versions.v1 import internal as v1_route_internal
from src.config.env import get_settings
from src.lib.redis import redis_cache
from fastapi.middleware.gzip import GZipMiddleware

config = get_settings()


app = FastAPI(
    title="E-Commerce Backend API",
    description="This application will serve APIs for E-Commerce web application",
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await redis_cache.init_cache()
    yield
    # Shutdown
    await redis_cache.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include version routers
app.include_router(v1_route.api_router, prefix=APP_CONTEXT_PATH)
app.include_router(v1_route_internal.api_router, prefix=APP_CONTEXT_PATH_v2)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)