import logging
import sys
from pathlib import Path


def setup_logger(file_name=None) -> None:
    logging.basicConfig(
        filename=file_name,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def module_name() -> str:
    return Path(sys.argv[0]).stem


def started(file_name=None) -> None:
    setup_logger(file_name)
    logging.info("=" * 80)
    msg = f"{module_name()} started"
    logging.info(msg)


def finished() -> None:
    msg = f"{module_name()} finished"
    logging.info(msg)
