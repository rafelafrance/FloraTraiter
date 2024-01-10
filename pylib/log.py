import logging
import sys
from pathlib import Path


def setup_logger(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def module_name() -> str:
    return Path(sys.argv[0]).name


def started() -> None:
    setup_logger()
    logging.info("=" * 80)
    logging.info("%s started", module_name())


def finished() -> None:
    logging.info("%s finished", module_name())
