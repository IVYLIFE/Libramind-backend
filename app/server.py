from fastapi import FastAPI
from app.api import books, student, issue


def create_app() -> FastAPI:
    app = FastAPI(
        title="LibraMind",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    return app


app = create_app()

app.include_router(books.router)
app.include_router(student.router)
app.include_router(issue.router)


@app.get("/")
def root():
    return {
        "status": "ok",
        "version": "1.0.0",
        "description": "Book Management API",
        "message": "Welcome to the Book Management API",
    }
