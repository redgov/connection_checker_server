from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import groups


app = FastAPI()

app.include_router(groups.router)
