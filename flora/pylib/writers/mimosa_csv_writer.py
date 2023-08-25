from .base_csv_writer import BaseCsvWriter


class CsvWriter(BaseCsvWriter):
    first = """ taxon """.split()

    def format_row(self, row):
        csv_row = {"taxon": row.taxon}

        return self.row_builder(row, csv_row)
