def obj_diff(a: dict[str, int] | None, b: dict[str, int]) -> dict[str, int]:
    if a:
        return {k: v for k, v in b.items() if a[k] != v}
    return b
