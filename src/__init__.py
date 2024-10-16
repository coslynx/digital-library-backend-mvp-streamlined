from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from src.config.settings import settings
from src.infrastructure.api.dependencies.database import get_db
from src.infrastructure.api.v1.routes.books import router as books_router
from src.infrastructure.api.v1.routes.users import router as users_router
from src.infrastructure.api.v1.routes.auth import router as auth_router

app = FastAPI(
    title="Streamlined Digital Library Backend",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(books_router, prefix="/api/v1/books")
app.include_router(users_router, prefix="/api/v1/users")
app.include_router(auth_router, prefix="/api/v1/auth")

# Serve static files for frontend integration
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup():
    # Initialize database connection on startup
    await get_db() 

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Streamlined Digital Library Backend</title>
        </head>
        <body>
            <h1>Welcome to the Streamlined Digital Library Backend!</h1>
            <p>This API powers the digital library platform.</p>
            <p>Explore the documentation at <a href="/api/v1/docs">API Documentation</a>.</p>
        </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)