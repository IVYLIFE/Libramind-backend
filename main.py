from typing import Union
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

app = FastAPI()

# Set up simple logging
logging.basicConfig(
    filename="app.log",  # Log file name
    level=logging.INFO,  # Minimum log level to capture
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Route - /
@app.get("/")
def read_root():
    return {
        "status": "running",
        "message": "FastAPI server is up and healthy",
        "version": "1.0.0",
    }


# Route - /items/{item_id}
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    if item_id <= 0:
        raise HTTPException(status_code=400, detail="item_id must be positive integer")
    return {"item_id": item_id, "q": q}



# Catch-all route for 404 Not Found errors
@app.exception_handler(StarletteHTTPException)
async def not_found_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        logging.warning(f"Not Found: {request.method} {request.url}")

        return JSONResponse(
            status_code=404,
            content={
                "error": "Not Found",
                "detail": f"The requested resource '{request.url.path}' was not found.",
                "method": request.method,
                "path": request.url.path,
            },
        )
    # For other HTTP exceptions, use the default behavior
    return await app.default_exception_handler(request, exc)



# Global error handler for unexpected exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc)},
    )
