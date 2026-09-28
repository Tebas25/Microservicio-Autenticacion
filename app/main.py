from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.db.session import init_engine
from app.api.v1.routers import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_engine()
    yield


app = FastAPI(
    title="Auth Service - Bartender Robótico",
    description="Microservicio emisor de JWT y validación de usuarios",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Auth Service en línea. Guardia listo."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
