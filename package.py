from pathlib import Path
import typing as t


def search_dir():
    return Path("content").glob("**/*.md")


def package(paths: t.Generator[Path, None, None]):
    content_total = ""
    for p in paths:
        print(p)
        content = (
            p.read_text(encoding="utf-8")
            .replace("[[", "")
            .replace("]]", "")
            .replace(" #", "")
            .replace(" @", "")
        )
        content_total += "\n" + content
        (Path() / "build" / p.name).write_text(content, encoding="utf-8")
    return content_total


if __name__ == "__main__":
    paths = search_dir()
    content = package(paths)
    (Path() / "build" / "content.md").write_text(content, encoding="utf-8")
