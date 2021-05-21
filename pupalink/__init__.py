from importlib import metadata

__version__ = metadata.version(__name__)

from .downloader import Session

__all__ = ["Session"]
