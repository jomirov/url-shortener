from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import links

app = FastAPI()

app.include_router(links.router)

app.add_middleware(CORSMiddleware)