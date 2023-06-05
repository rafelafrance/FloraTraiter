from plants.pylib.writers import csv_writer as base_writer


class CsvWriter(base_writer.CsvWriter):
    first = """ family flora_id flora_name taxon taxon_id link path """.split()

    def format_row(self, row):
        csv_row = {
            "family": row.family,
            "flora_id": row.flora_id,
            "flora_name": row.flora_name,
            "taxon": row.taxon,
            "taxon_id": row.taxon_id,
            "link": row.link,
            "path": row.path,
        }

        return self.row_builder(row, csv_row)
