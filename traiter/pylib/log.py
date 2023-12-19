"""Common logging functions."""
import logging
import sys
from os.path import basename
from os.path import splitext


def setup_logger(level=logging.INFO):
    """Setup the logger."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def module_name() -> str:
    """Get the current module name."""
    return splitext(basename(sys.argv[0]))[0]


def started() -> None:
    """Log the program start time."""
    setup_logger()
    logging.info("=" * 80)
    logging.info("%s started", module_name())


def finished() -> None:
    """Log the program end time."""
    logging.info("%s finished", module_name())
