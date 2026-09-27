from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Auth Service - Bartender Robótico",
    description="Microservicio emisor de JWT y validación de usuarios",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Auth Service en línea. Guardia listo."}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
