from plants.pylib.writers import csv_writer as base_writer


class CsvWriter(base_writer.CsvWriter):
    first = """ taxon """.split()

    def format_row(self, row):
        csv_row = {"taxon": row.taxon}

        return self.row_builder(row, csv_row)
