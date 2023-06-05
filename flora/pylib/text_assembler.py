"""Convert structured in table-like formats into text in sentences & paragraphs."""
from dataclasses import dataclass
from dataclasses import field


@dataclass
class Word:
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    word: str


@dataclass
class Line:
    words: list[Word] = field(default_factory=list)

    @property
    def text(self):
        return " ".join(w.word for w in self.words)

    @property
    def top(self):
        return min(w.y_min for w in self.words)


@dataclass
class Page:
    no: int = 0
    width: float = 0.0
    height: float = 0.0
    words: list[Word] = field(default_factory=list)
    lines: list[Line] = field(default_factory=list)


def page_flow(args, page, lines):
    flow, col1, col2 = [], [], []
    center = page.width // 2
    gap_left = center - args.gap_radius
    gap_right = center + args.gap_radius
    for line in lines:
        split = find_column_split(line, args.gap_min, gap_left, gap_right)

        # Found a column gutter
        if split >= 0:
            col1.append(Line(line.words[:split]))
            col2.append(Line(line.words[split:]))

        # Found a left-side widow
        elif line.words[-1].x_max <= center:
            col1.append(line)

        # Found a right-side widow
        elif line.words[0].x_min >= center:
            col2.append(line)

        # This line spans both columns, so re-flow the columns
        else:
            flow += col1
            flow += col2
            flow.append(line)
            col1, col2 = [], []

    flow += col1
    flow += col2

    return flow


def find_column_split(line, gap_min, gap_left, gap_right):
    splits = []
    for i, (prev, curr) in enumerate(zip(line.words[:-1], line.words[1:]), 1):
        split = curr.x_min - prev.x_max
        x_min = max(prev.x_max, gap_left)
        x_max = min(curr.x_min, gap_right)
        inter = max(0.0, x_max - x_min)
        if split >= gap_min and inter > 0.0:
            splits.append((split, i))
    splits = sorted(splits, reverse=True)
    return splits[0][1] if splits else -1


def find_lines(page, vert_overlap=0.3):
    lines = []

    for word in page.words:
        overlap = [(find_overlap(ln, word), ln) for ln in lines]
        overlap = sorted(overlap, key=lambda o: -o[0])

        if overlap and overlap[0][0] > vert_overlap:
            line = overlap[0][1]
            line.words.append(word)
        else:
            line = Line()
            line.words.append(word)
            lines.append(line)

    lines = sorted(lines, key=lambda ln: ln.top)
    return lines


def find_overlap(line, word, eps=1):
    """Find the vertical overlap between a line and the word bounding box.

    This is a fraction of the smallest height of the line & word bounding box.
    """
    last = line.words[-1]  # If line.words is empty then we have a bigger problem
    min_height = min(last.y_max - last.y_min, word.y_max - word.y_min)
    y_min = max(last.y_min, word.y_min)
    y_max = min(last.y_max, word.y_max)
    inter = max(0, y_max - y_min)
    return inter / (min_height + eps)
