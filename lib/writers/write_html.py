"""Write the traiter output to an HTML file."""

from lib.writers.write_base import WriteBase


class WriteHtml(WriteBase):
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""

    def header(self):
        """Output the report header."""

    def row(self):
        """Output a report row."""

    def cell(self):
        """Output a report cell."""

    def footer(self):
        """Output the report footer."""
