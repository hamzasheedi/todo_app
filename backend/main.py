from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from .routes import auth, tasks
from .database import create_db_and_tables

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Todo API",
    description="API for the multi-user todo application",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Todo API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Include routes
app.include_router(auth.router)
app.include_router(tasks.router, prefix="/api/{user_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)