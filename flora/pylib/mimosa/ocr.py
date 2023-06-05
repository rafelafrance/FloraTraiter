import pytesseract


class EngineConfig:
    char_blacklist = "¥€£¢$«»®©™§{}|~”"
    tess_lang = "eng"
    tess_config = " ".join(
        [
            f"-l {tess_lang}",
            f"-c tessedit_char_blacklist='{char_blacklist}'",
        ]
    )


def tesseract_engine(image) -> list[dict]:
    df = pytesseract.image_to_data(
        image, config=EngineConfig.tess_config, output_type="data.frame"
    )

    df = df.loc[df.conf > 0]

    if df.shape[0] > 0:
        df.text = df.text.astype(str)
        df.text = df.text.str.strip()
        df.conf /= 100.0
        df["right"] = df.left + df.width
        df["bottom"] = df.top + df.height
    else:
        df["right"] = None
        df["bottom"] = None

    df = df.loc[:, ["conf", "left", "top", "right", "bottom", "text"]]

    results = df.to_dict("records")
    return results
