"""Motor de detecção da Regis.

    from motor.detectar import detectar
    resultado = detectar("dados")
"""

from .detectar import detectar  # noqa: F401

__all__ = ["detectar"]
