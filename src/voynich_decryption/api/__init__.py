"""FastAPI REST API for Voynich Morphemic Decryption."""

from voynich_decryption.api.app import app
from voynich_decryption.api.routes import router
from voynich_decryption.api import schemas

__all__ = [
    "app",
    "router",
    "schemas",
]
