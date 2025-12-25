from loguru import logger

logger.add("logs/pipeline.log", rotation="10 MB", retention=5)

__all__ = ["logger"]
