from __future__ import annotations

import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        if data and data.strip():
            self.parts.append(data.strip())

    def text(self) -> str:
        return "\n".join(self.parts)


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    return text


def read_txt(path: str | Path) -> str:
    path = Path(path)
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "gbk"):
        try:
            return clean_text(path.read_text(encoding=encoding, errors="ignore"))
        except UnicodeDecodeError:
            continue
    return clean_text(path.read_text(errors="ignore"))


def read_epub(path: str | Path) -> str:
    path = Path(path)
    chunks: list[str] = []
    with zipfile.ZipFile(path, "r") as archive:
        for name in archive.namelist():
            lower = name.lower()
            if not lower.endswith((".xhtml", ".html", ".htm")):
                continue
            raw = archive.read(name).decode("utf-8", errors="ignore")
            parser = _HTMLTextExtractor()
            parser.feed(raw)
            chunks.append(parser.text())
    return clean_text("\n".join(chunks))


def read_novel(path: str | Path) -> str:
    suffix = Path(path).suffix.lower()
    if suffix == ".epub":
        return read_epub(path)
    if suffix == ".txt":
        return read_txt(path)
    raise ValueError("Pixian only supports .txt and .epub files.")
