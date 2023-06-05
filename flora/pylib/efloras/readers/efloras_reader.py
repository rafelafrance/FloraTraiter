import csv
import re
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from itertools import product

from bs4 import BeautifulSoup
from plants.pylib.traits.part.part_action import PART_LABELS
from tqdm import tqdm

from efloras.pylib import const

TAXON_TITLE = "Accepted Name"

PARTS_SET = set(PART_LABELS)


@dataclass
class EflorasRow:
    family: str
    flora_id: int
    flora_name: str
    taxon: str
    taxon_id: int
    link: str
    path: str
    text: str
    traits: list[dict] = field(default_factory=list)


# Used to filter paragraphs in the source documents.
PARA_RE = f"({'|'.join(PART_LABELS)})"
PARA_RE = re.compile(PARA_RE, flags=re.IGNORECASE)


def reader(args, families):
    families_flora = get_family_flora_ids(args, families)
    flora_ids = get_flora_ids()

    # Build a filter for the taxon names
    genera = [g.lower() for g in args.genus] if args.genus else []
    genera = [r"\s".join(g.split()) for g in genera]
    genera = "|".join(genera)

    rows = []

    for family_name, flora_id in tqdm(families_flora):
        flora_id = int(flora_id)
        family = families[(family_name, flora_id)]
        taxa = get_family_tree(family)
        root = treatment_dir(flora_id, family["family"])
        for path in root.glob("*.html"):
            text = get_treatment(path)
            text = get_traits_para(text)
            taxon_id = get_taxon_id(path)

            # Must have a taxon name
            if not taxa.get(taxon_id):
                continue

            # Filter on the taxon name
            if genera and not re.search(genera, taxa[taxon_id], flags=re.IGNORECASE):
                continue

            rows.append(
                EflorasRow(
                    family=family["family"],
                    flora_id=flora_id,
                    flora_name=flora_ids[flora_id],
                    taxon=taxa[taxon_id],
                    taxon_id=taxon_id,
                    link=treatment_link(flora_id, taxon_id),
                    path=path,
                    text=text if text else "",
                )
            )

    return rows


def get_family_tree(family):
    """Get all taxa for the all the families."""
    taxa = {}
    dir_ = tree_dir(family["flora_id"], family["family"])
    for path in dir_.glob("*.html"):
        with open(path) as in_file:
            page = in_file.read()

        soup = BeautifulSoup(page, features="lxml")

        for link in soup.findAll("a", attrs={"title": TAXON_TITLE}):
            href = link.attrs["href"]
            taxon_id = get_taxon_id(href)
            taxa[taxon_id] = link.text

    return taxa


def get_treatment(path):
    """Get the taxon description page."""
    with open(path) as in_file:
        page = in_file.read()
    soup = BeautifulSoup(page, features="lxml")
    return soup.find(id="panelTaxonTreatment")


def get_traits_para(treatment):
    """Find the trait paragraph in the treatment."""
    if not treatment:
        return ""
    best = ""
    high = 0
    for para in treatment.find_all("p"):
        text = " ".join(para.get_text().split())
        unique = set(PARA_RE.findall(text))
        if len(unique) > high:
            best = " ".join(para.get_text().split())
            high = len(unique)
        if high >= 5:
            return best
    return best if high >= 4 else ""


def treatment_link(flora_id, taxon_id):
    """Build a link to the treatment page."""
    return (
        "http://www.efloras.org/florataxon.aspx?"
        rf"flora_id={flora_id}&taxon_id={taxon_id}"
    )


def get_families():
    """Get a list of all families in the eFloras catalog."""
    families = {}

    with open(const.EFLORAS_FAMILIES) as in_file:

        for family in csv.DictReader(in_file):

            times = {"created": "", "modified": "", "count": 0}

            path = (
                const.DATA_DIR / "eFloras" / f"{family['family']}_{family['flora_id']}"
            )

            if path.exists():
                times["count"] = len(list(path.glob("**/treatments/*.html")))
                if times["count"]:
                    stat = path.stat()
                    times["created"] = datetime.fromtimestamp(stat.st_ctime).strftime(
                        "%Y-%m-%d %H:%M"
                    )
                    times["modified"] = datetime.fromtimestamp(stat.st_mtime).strftime(
                        "%Y-%m-%d %H:%M"
                    )

            key = (family["family"].lower(), int(family["flora_id"]))
            families[key] = {**family, **times}

    return families


def get_flora_ids():
    """Get a list of flora IDs."""
    flora_ids = {}
    with open(const.EFLORAS_FAMILIES) as in_file:
        for family in csv.DictReader(in_file):
            flora_ids[int(family["flora_id"])] = family["flora_name"]
    return flora_ids


def get_family_flora_ids(args, families):
    """Get family and flora ID combinations."""
    return [c for c in product(args.family, args.flora_id) if c in families]


def get_taxon_id(href):
    """Given a link or file name return a taxon ID."""
    href = str(href)
    taxon_id_re = re.compile(r"taxon_id[=_](\d+)")
    return int(taxon_id_re.search(href)[1])


def treatment_dir(flora_id, family_name):
    return family_dir(flora_id, family_name) / "treatments"


def tree_dir(flora_id, family_name):
    return family_dir(flora_id, family_name) / "tree"


def family_dir(flora_id, family_name):
    """Build the family directory name."""
    taxon_dir = f"{family_name}_{flora_id}"
    return const.DATA_DIR / "eFloras" / taxon_dir
