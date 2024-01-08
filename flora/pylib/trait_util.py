def clean_trait(ent, replace):
    """Clean up simple traits."""
    frags = [replace.get(t.lower_, t.lower_) for t in ent if t.text not in "[]()"]
    return " ".join(frags)


def clear_tokens(ent):
    """Clear tokens in an entity."""
    for token in ent:
        token._.trait = None
        token._.flag = ""
        token._.term = ""
