def wrap_text(text: str, *, width: int = 80, padded: bool = False) -> str:
    lines = text.splitlines()

    for i, line in enumerate(lines):
        if len(line) > width:
            head, tail = line[:width], line[width:]
            lines[i] = head
            lines.insert(i + 1, tail)

    if padded:
        lines = [f"{ln: <{width}}" for ln in lines]

    return "\n".join(lines)
