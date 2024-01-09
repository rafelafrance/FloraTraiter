from spacy.language import Language

DEBUG_TOKENS = "debug_tokens"
DEBUG_ENTITIES = "debug_entities"

# So we don't have to come up with new names all the time
DEBUG_COUNT = 0  # Used to rename debug pipes


def tokens(nlp, **kwargs) -> str:
    """Automatically set up a pipe to print token information."""
    global DEBUG_COUNT
    DEBUG_COUNT += 1
    name = f"debug_tokens_{DEBUG_COUNT}"
    nlp.add_pipe(DEBUG_TOKENS, name=name, **kwargs)
    return name


def ents(nlp, **kwargs) -> str:
    """Automatically set up a pipe to print entity information."""
    global DEBUG_COUNT
    DEBUG_COUNT += 1
    name = f"debug_entities_{DEBUG_COUNT}"
    nlp.add_pipe(DEBUG_ENTITIES, name=name, **kwargs)
    return name


@Language.factory(DEBUG_TOKENS)
class DebugTokens:
    def __init__(self, nlp: Language, name: str):
        self.nlp = nlp
        self.name = name

    def __call__(self, doc):
        print("=" * 80)
        print(self.name)
        print(f'{"entity type":<20} {"flag":10} {"pos":6} {"term":<20} token')
        print(f'{"-----------":<20} {"----":10} {"---":6} {"----":<20} -----')
        for token in doc:
            print(
                f"{token.ent_type_:<20} {token._.flag:10} {token.pos_:6} "
                f"{token._.term:<20} {token}",
            )
        print()
        return doc


@Language.factory(DEBUG_ENTITIES)
class DebugEntities:
    def __init__(self, nlp: Language, name: str):
        self.nlp = nlp
        self.name = name

    def __call__(self, doc):
        print("=" * 80)
        print(self.name)
        for ent in doc.ents:
            print(f"{ent.label_:<20} {ent}")
            # print(f'{" " * 20} delete={ent._.delete}')
            print(f'{" " * 20} {ent._.trait}\n')
        print()
        return doc
