"""
The algorithms for linking traits to the taxon they describe can get involved.
This simple-minded reader associates traits with a taxon by proximity to the nearest
trait mentioned. That is, it will link a trait to the nearest taxon that precedes it
in the text. There is a radius parameter that will stop linking traits and assign the
trait to "Unknown" once the sentence count passes the threshold.
"""
from .mimosa_base_reader import BaseReader


class ProximityReader(BaseReader):
    def __init__(self, args):
        super().__init__(args)
        self.taxon_distance = args.taxon_distance

    def read(self):
        taxon = "Unknown"
        countdown = 0

        for ln in self.lines:
            ln = ln.strip()
            doc = self.nlp(ln)

            traits = []

            for ent in doc.ents:
                trait = ent._.trait

                if trait["trait"] == "taxon":
                    taxon = trait["taxon"]
                    taxon = tuple(taxon) if isinstance(taxon, list) else taxon
                    countdown = self.taxon_distance
                elif trait["trait"] != "taxon":
                    trait["taxon"] = taxon
                    self.taxon_traits[taxon].append(trait)

                traits.append(trait)

            self.text_traits.append((ln, traits))

            countdown -= 1
            if countdown <= 0:
                taxon = "Unknown"

        return self.finish()
