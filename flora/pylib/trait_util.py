def clean_trait(ent, replace):
    """Clean up simple traits."""
    frags = []
    for token in ent:
        if token.text not in "[]()":
            frags.append(replace.get(token.lower_, token.lower_))
    return " ".join(frags)


def clear_tokens(ent):
    """Clear tokens in an entity."""
    for token in ent:
        token._.trait = None
        token._.flag = ""
        token._.term = ""
