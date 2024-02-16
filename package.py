from pathlib import Path
import typing as t

CONTENT_TOTAL = False

def search_dir():
    return Path("content").glob("**/*.md")

def clear_build():
    for p in Path("build").glob("*"):
        p.unlink()

def package(paths: t.Generator[Path, None, None]):
    content_total = ""
    for p in paths:
        print(p)
        raw_content = p.read_text(encoding="utf-8")
        if "docs: true" in raw_content:
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
    clear_build()
    content = package(paths)
    if CONTENT_TOTAL:
        (Path() / "build" / "content.md").write_text(content, encoding="utf-8")
