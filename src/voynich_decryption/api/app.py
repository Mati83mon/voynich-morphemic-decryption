"""FastAPI application for Voynich Morphemic Decryption API."""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from voynich_decryption.__version__ import __version__
from voynich_decryption.api.routes import router
from voynich_decryption.api.schemas import ErrorResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for FastAPI application.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("=" * 70)
    logger.info("Starting Voynich Morphemic Decryption API")
    logger.info(f"Version: {__version__}")
    logger.info("=" * 70)

    yield

    # Shutdown
    logger.info("=" * 70)
    logger.info("Shutting down Voynich Morphemic Decryption API")
    logger.info("=" * 70)


# Create FastAPI application
app = FastAPI(
    title="Voynich Morphemic Decryption API",
    description="""
    Advanced morphemic analysis API for the Voynich Manuscript.

    This API provides endpoints for:
    - Morphemic decomposition of Voynich words
    - Statistical validation of analysis results
    - Batch processing of vocabularies
    - Word-by-word analysis

    ## Features

    * **Morphemic Analysis**: Decompose words into constituent morphemes
    * **Statistical Validation**: Chi-square tests and distribution analysis
    * **Batch Processing**: Analyze entire vocabularies at once
    * **Caching**: Efficient caching for improved performance
    * **Type Safety**: Full Pydantic validation for all endpoints

    ## Authentication

    Currently no authentication required. Future versions may include API key authentication.

    ## Rate Limiting

    No rate limiting currently implemented. Use responsibly.
    """,
    version=__version__,
    contact={
        "name": "Mateusz Piesiak",
        "email": "mateuszpiesiak1990@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle request validation errors."""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error=True,
            message="Request validation failed",
            detail=str(exc.errors()),
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error=True,
            message="Internal server error",
            detail=str(exc),
        ).model_dump(),
    )


# Include routers
app.include_router(router, prefix="/api/v1", tags=["analysis"])


# Custom middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests."""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"{request.method} {request.url.path} - {response.status_code}")
    return response


if __name__ == "__main__":
    import uvicorn

    # Run the application
    uvicorn.run(
        "voynich_decryption.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
