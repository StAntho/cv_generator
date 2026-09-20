from fastapi import FastAPI
from routers import all_routers
from contextlib import asynccontextmanager
from db.database import create_db_and_tables

from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

## Initialisation de l'app FastAPI
app = FastAPI(lifespan=lifespan)

for router in all_routers: 
    app.include_router(router)