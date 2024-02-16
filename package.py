import typing as t
from pathlib import Path

CONTENT_TOTAL = False


def search_dir() -> t.Generator[Path, None, None]:
    return Path("content").glob("**/*.md")


def clear_build() -> None:
    """
    Clears the contents of the 'build' directory.
    """
    for p in Path("build").glob("*"):
        p.unlink()


def package(
    paths: t.Generator[Path, None, None],
) -> str:
    """
    This function takes a generator of Path objects, reads the text from each path,
    checks if the text contains "docs: true", and if so, it removes certain characters
    from the text and saves it to a new file in the "build" directory with the same filename.
    The modified content from all files is also accumulated and returned as a single string.

    Args:
        paths (t.Generator[Path, None, None]): A generator of Path objects

    Returns:
        str: The modified content from all files that contained "docs: true"
    """
    content_total = ""
    for p in paths:
        print(p)
        raw_content = p.read_text(encoding="utf8")
        if "docs: true" in raw_content:
            content = (
                raw_content.replace("[[", "")
                .replace("]]", "")
                .replace(" #", "")
                .replace(" @", "")
            )
            content_total += "\n" + content
            (Path() / "build" / p.name).write_text(content, encoding="utf8")
    return content_total


if __name__ == "__main__":
    paths = search_dir()
    clear_build()
    content = package(paths)
    if CONTENT_TOTAL:
        (Path() / "build" / "content.md").write_text(content, encoding="utf-8")
