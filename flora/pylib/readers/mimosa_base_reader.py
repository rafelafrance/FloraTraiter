from collections import defaultdict
from collections import namedtuple

from .. import pipeline
from .. import sentence_pipeline

TraitsInText = namedtuple("TraitsInText", "text traits")
TraitsByTaxon = namedtuple("TraitsByTaxon", "taxon traits")


class TraitsInTextList:
    def __init__(self, text_traits):
        self.traits = [TraitsInText(t[0], t[1]) for t in text_traits]

    def __iter__(self):
        yield from self.traits


class TraitsByTaxonList:
    def __init__(self, taxon_traits):
        self.split_multi_taxa(taxon_traits)
        self.traits = dict(sorted(taxon_traits.items(), key=lambda t: t[0]))
        self.traits = [TraitsByTaxon(k, v) for k, v in taxon_traits.items()]

    def __iter__(self):
        yield from self.traits

    @staticmethod
    def split_multi_taxa(taxon_traits):
        new_traits = defaultdict(list)
        for taxa, traits in taxon_traits.items():
            if isinstance(taxa, tuple):
                for name in taxa:
                    new_traits[name] += traits
            else:
                new_traits[taxa] += traits
        return new_traits


class BaseReader:
    def __init__(self, args):
        self.lines = self.read_lines(args.in_text, args.limit)
        self.nlp = pipeline.build()
        self.sent_nlp = sentence_pipeline.pipeline()
        self.text_traits = []
        self.taxon_traits = defaultdict(list)

    def read(self):
        raise NotImplementedError()

    @staticmethod
    def read_lines(in_text, limit):
        with open(in_text, encoding="utf_8") as in_file:
            lines = in_file.readlines()

        if limit:
            lines = lines[:limit]

        return lines

    def finish(self):
        return TraitsInTextList(self.text_traits), TraitsByTaxonList(self.taxon_traits)
