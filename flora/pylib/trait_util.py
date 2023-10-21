def clean_trait(ent, replace):
    """Clean up simple traits."""
    frags = []
    for token in ent:
        if token.text not in "[]()":
            frags.append(replace.get(token.lower_, token.lower_))
    return " ".join(frags)
