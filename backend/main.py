from fastapi import FastAPI
from api.routes import router as api_router
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/resume", StaticFiles(directory="public"), name="resumes")

# Include your API routes
app.include_router(api_router, prefix="/api")

# Optionally, add CORS middleware if your frontend is separate
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)