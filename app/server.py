from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


from app.utils import error_response
from app.api import books, student


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


@app.get("/")
def root():
    return {
        "status": "ok",
        "version": "1.0.0",
        "title": "LibraMind",
        "description": "Welcome to the Book Management API",
    }




# Custom HTTPException override
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail if exc.detail else "An HTTP error occurred"
    return error_response(
        status_code=exc.status_code,
        detail=detail
    )

# Request validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print("Validation exception occurred")
    print(exc)

    detail = [
        {
            "fieldname": error['loc'][-1], 
            "msg": error['msg']
        }
        for error in exc.errors()
    ]
    return error_response(
        message="Validation Error",
        status_code=422,
        detail=detail
    )

# Catch-all fallback
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    print("Unhandled exception occurred")
    print(exc)
    return error_response(
        status_code=500,
        detail=str(exc)
    )
