from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text, inspect
from contextlib import asynccontextmanager

import logging
import logging.config

from app.database import Base, engine
from app.utils import error_response
from app.api import books, students
# from app.logging_config import LOGGING_CONFIG


# logging.config.dictConfig(LOGGING_CONFIG)
# logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("\n\n\n✅ Database connection established at startup.\n\n\n")
            # logger.info("Database connection successful at startup.")
    except Exception as e:
        print(f"❌ Database connection failed at startup: {e}")
        # logger.error("Database connection failed at startup.", exc_info=e)
        raise RuntimeError(f"Startup DB connection failed: {e}")
    
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="LibraMind",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        # lifespan=lifespan,
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(books.router)
    app.include_router(students.router)

    return app

app = create_app()



# =============================================
# Health Check Endpoints
# =============================================


@app.get("/")
def root():
    return {
        "status": "ok",
        "version": "1.0.0",
        "title": "LibraMind",
        "description": "Welcome to the Book Management API",
    }



@app.get("/db-check")
def db_check():
    try:
        with Session(engine) as session:
            # 1. Get DB version
            version_result = session.execute(text("SELECT version()"))
            version_str = version_result.scalar()

            # 2. Get current DB name
            dbname_result = session.execute(text("SELECT current_database()"))
            db_name = dbname_result.scalar()
            

            # 3. List tables in current schema (Postgres specific)
            inspector = inspect(engine)
            tables = inspector.get_table_names()

            db_details = {
                "version" : version_str,
                "tables"  : tables
            }

            return {
                "status": "ok",
                "message": "Database connection successful.",
                "database_name": db_name,
                "database_details": db_details
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
    


# =============================================
# Global Exception Handlers
# =============================================

# Custom HTTPException override
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    detail = exc.detail if exc.detail else "An HTTP error occurred"
    # logging.warning(f"❌ HTTP Exception : Not Found: {request.method} {request.url}")
    return error_response(
        status_code=exc.status_code,
        detail=detail
    )

# Request validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    detail = [
        {
            "fieldname": error['loc'][-1], 
            "msg": error['msg']
        }
        for error in exc.errors()
    ]
    return error_response(
        status_code=422,
        detail=detail
    )

# Catch-all fallback
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    # logging.error(f"❌ Unhandled exception: {exc}", exc_info=True)
    return error_response(
        status_code=500,
        detail=str(exc)
    )


# =====================================================================