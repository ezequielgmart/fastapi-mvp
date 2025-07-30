# src/main.py
from fastapi import FastAPI
from src.features.authors import route as authors_routes

app = FastAPI(
    title="Mi API de Autores",
    description="Una API para gestionar autores y libros.",
    version="1.0.0",
)

app.include_router(
    authors_routes.router,
    prefix="/authors",
    tags=["Authors"]
)

@app.get("/")
async def read_root():
    return {"message": "¡Bienvenido a la API!"}

# Para ejecutar tu aplicación: uvicorn src.main:app --reload