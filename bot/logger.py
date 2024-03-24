import logging
import os

logger = logging.getLogger()

file_handler = logging.FileHandler(os.path.join("app.log"))
formatter = logging.Formatter(
    fmt="%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - Line No : %(lineno)d - %(message)s",
    datefmt="%Y-%b-%d %I:%M:%S %p",
)
file_handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
