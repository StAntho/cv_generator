def text_to_list(value: str) -> list[str]:
    if not value:
        return []
    return [
        line.strip()
        for line in value.splitlines()
        if line.strip()
    ]