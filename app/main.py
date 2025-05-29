from fastapi import FastAPI
from app.api.endpoints.items import router as items_router
from app.api.endpoints.users import router as users_router
import logging

logging.basicConfig(
    level=logging.INFO,  # or DEBUG for more verbosity
    format="[%(asctime)s %(levelname)s %(name)s: %(message)s]"
)

logger = logging.getLogger("Test application")


app = FastAPI()

app.include_router(items_router, prefix="/items", tags=["items"])
app.include_router(users_router, prefix="/users", tags=["users"])

logger.info("FastAPI application started.")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application!"}