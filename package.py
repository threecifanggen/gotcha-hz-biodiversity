"""Package all the useful markdown files into the 'build' directory.
"""
import typing as t
from pathlib import Path
import re

CONTENT_TOTAL = False

_PATTERN_LIST: list[str] = [
    r"!\[.*?\]\(.*?\)",
]


def search_dir() -> t.Generator[Path, None, None]:
    """
    Search the 'content' directory recursively and yield all the Path objects of the markdown files.

    Yields:
        Path: The Path object of each markdown file found in the 'content' directory.
    """
    return Path("content").glob("**/*.md")


def clear_build() -> None:
    """
    Clears the contents of the 'build' directory.
    """
    for p in Path("build").glob("*"):
        p.unlink()


def process_content(content_text: str) -> str:
    """
    Process the content text by removing certain characters.

    Args:
        content_text (str): The content text to process

    Returns:
        str: The processed content text
    """
    res_text = (
        content_text.replace("[[", "")
        .replace("]]", "")
        .replace(" #", "")
        .replace(" @", "")
    )
    for pattern in _PATTERN_LIST:
        res_text = re.sub(pattern, "", res_text)
    return res_text


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
