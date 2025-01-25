from fastapi import FastAPI
import uvicorn
from sqlalchemy import Column, Integer, String

from app.routers import news, summary
from app.database import engine, Base
from app import models

# Create all tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="AI based News Summary API",
    version="0.2",
    description="This is the API documentation for News Summary generating by AI.",
    contact={
        "name": "Md. Ziaul Hoque",
        "url": "https://growwithdata.net",
        "email": "www.mzhk@gmail.com",
    },
    redoc_url="/documentation",
    docs_url="/zia",
)

app.include_router(news.router)
app.include_router(summary.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the News Summary API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)
