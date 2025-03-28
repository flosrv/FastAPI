from fastapi import FastAPI, HTTPException
from models import books_models
from routes.routes import book_endpoint
import logging

# Configuration des logs
logging.basicConfig(level=logging.DEBUG)

version = "v1"


# Initialisation de l'application FastAPI
app = FastAPI(
    title="Bookly",
    description="A REST API for a book review web service",
    version=version
    )

# Log de l'initialisation de l'API
logging.info(f"Initializing Bookly API - version {version}")

# Inclusion du routeur
try:
    app.include_router(book_endpoint, prefix=f"/api/{version}/books", tags=["books"])
    logging.info("Successfully included the 'book_endpoint' router.")
except Exception as e:
    logging.error(f"Failed to include the 'book_endpoint' router: {e}")
    raise HTTPException(status_code=500, detail="Failed to include router")

# Root endpoint - un point de terminaison de base pour tester
# @app.get("/")
# async def root():
#     try:
#         logging.debug("Root endpoint accessed.")
#         return {"message": "Welcome to the Bookly API!"}
#     except Exception as e:
#         logging.error(f"Error in root endpoint: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# Log de démarrage de l'application
logging.info(f"Application {version} started successfully.")
