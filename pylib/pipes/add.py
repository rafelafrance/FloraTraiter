from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path

from spacy.language import Language

from traiter.pylib import term_util
from traiter.pylib.pattern_compiler import ACCUMULATOR, Compiler
from traiter.pylib.pipes import (
    cleanup,
    debug,
    link,
    merge_selected,
    phrase,
    trait,
)


def term_pipe(
    nlp,
    *,
    name: str,
    path: Path | list[Path],
    default_labels: dict[str, str] | None = None,
):
    default_labels = default_labels if default_labels else {}
    paths = path if isinstance(path, Iterable) else [path]

    # Gather terms and make sure they have the needed fields
    by_attr = defaultdict(list)
    replaces = defaultdict(dict)

    for path in paths:
        terms = term_util.read_terms(path)
        for term in terms:
            label = term.get("label", default_labels.get(path.stem))
            pattern = {"label": label, "pattern": term["pattern"]}
            attr = term.get("attr", "lower").upper()
            by_attr[attr].append(pattern)
            if replace := term.get("replace"):
                replaces[attr][term["pattern"]] = replace

    # Add a pipe for each phrase matcher attribute
    with nlp.select_pipes(enable="tokenizer"):
        for attr, patterns in by_attr.items():
            name = f"{name}_{attr.lower()}"
            config = {
                "patterns": patterns,
                "replace": replaces[attr],
                "attr": attr,
            }
            nlp.add_pipe(phrase.PHRASE_PIPE, name=name, config=config)


def trait_pipe(
    nlp,
    *,
    name: str,
    compiler: list[Compiler] | Compiler,
    keep: list[str] | None = None,
    overwrite: list[str] | None = None,
    merge: list[str] | None = None,
):
    keep = keep if keep is not None else ACCUMULATOR.keep
    compilers = compiler if isinstance(compiler, Iterable) else [compiler]
    merge = merge if merge else []
    patterns = defaultdict(list)
    dispatch = {}
    relabel = {}

    for comp in compilers:
        comp.compile()
        patterns[comp.label] += comp.patterns

        if comp.on_match:
            dispatch[comp.label] = comp.on_match

        if comp.id:
            relabel[comp.label] = comp.id

    config = {
        "patterns": patterns,
        "dispatch": dispatch,
        "relabel": relabel,
        "keep": keep,
        "overwrite": overwrite,
    }
    nlp.add_pipe(trait.ADD_TRAITS, name=name, config=config)

    if merge:
        name = f"{name}_merge"
        config = {"labels": merge}
        nlp.add_pipe(merge_selected.MERGE_SELECTED, name=name, config=config)


def cleanup_pipe(nlp: Language, *, name: str, delete=None):
    if delete:
        delete = delete if isinstance(delete, list) else [delete]
        ACCUMULATOR.delete(delete)

    config = {"keep": ACCUMULATOR.keep}
    nlp.add_pipe(cleanup.CLEANUP_TRAITS, name=name, config=config)


def custom_pipe(
    nlp: Language,
    registered: str,
    name: str = "",
    config: dict | None = None,
):
    config = config if config else {}
    name = name if name else registered
    nlp.add_pipe(registered, name=name, config=config)


def debug_tokens(nlp: Language):
    debug.tokens(nlp)


def debug_ents(nlp: Language):
    debug.ents(nlp)


def link_pipe(
    nlp,
    *,
    compiler,
    name,
    parents,
    children,
    weights=None,
    reverse_weights=None,
    max_links=None,
    differ=None,
):
    compiler.compile()
    patterns = [
        {"label": compiler.label, "pattern": p, "id": compiler.id}
        for p in compiler.patterns
    ]
    config = {
        "patterns": patterns,
        "parents": parents,
        "children": children,
    }
    if weights is not None:
        config["weights"] = weights
    if reverse_weights is not None:
        config["reverse_weights"] = reverse_weights
    if max_links is not None:
        config["max_links"] = max_links
    if differ is not None:
        config["differ"] = differ
    nlp.add_pipe(link.LINK_TRAITS, name=name, config=config)
