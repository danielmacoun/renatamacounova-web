"""Read-only validation of the static site; run from the repository root."""

import json
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

import html5lib
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ORIGIN = "https://renatamacounova.cz"


def site_pages():
    return sorted(p for p in ROOT.rglob("*.html")
                  if not any(part.startswith(".") for part in p.relative_to(ROOT).parts))


def route(path):
    name = path.relative_to(ROOT).as_posix()
    return "/" + (name[:-10] if name.endswith("index.html") else name)


def local_target(source, value):
    url = urlsplit(value)
    if url.scheme not in ("", "http", "https"):
        return None
    if url.netloc and url.netloc != urlsplit(ORIGIN).netloc:
        return None
    name = unquote(url.path)
    if not name:
        target = source
    elif name.startswith("/") or url.netloc:
        target = ROOT / name.lstrip("/")
    else:
        target = source.parent / name
    target = target.resolve()
    if not target.is_relative_to(ROOT):
        raise ValueError("path escapes site root")
    if target.is_dir():
        target /= "index.html"
    return target, unquote(url.fragment)


def validate():
    errors, documents, ids = [], {}, {}

    def fail(path, message):
        errors.append(f"{path.relative_to(ROOT)}: {message}")

    for path in site_pages():
        parser = html5lib.HTMLParser(namespaceHTMLElements=False)
        doc = parser.parse(path.read_text(encoding="utf-8"))
        documents[path] = doc
        for position, code, details in parser.errors:
            fail(path, f"HTML {position}: {code} {details}")
        if doc.get("lang") != "cs":
            fail(path, 'expected html lang="cs"')
        page_ids = [el.get("id") for el in doc.iter() if el.get("id")]
        if len(page_ids) != len(set(page_ids)):
            fail(path, "duplicate element IDs")
        ids[path] = set(page_ids)
        title = doc.findall("./head/title")
        if len(title) != 1 or not "".join(title[0].itertext()).strip():
            fail(path, "missing or duplicate title")
        if len(doc.findall(".//h1")) != 1:
            fail(path, "expected exactly one h1")
        metas = doc.findall("./head/meta")
        for attr, key in [("name", "description"), ("name", "viewport"),
                          ("property", "og:title"), ("property", "og:description"),
                          ("property", "og:url"), ("property", "og:type")]:
            matches = [el.get("content", "").strip() for el in metas if el.get(attr) == key]
            if len(matches) != 1 or not matches[0]:
                fail(path, f"missing, empty or duplicate {key}")
        if not any(el.get("charset", "").lower() == "utf-8" for el in metas):
            fail(path, "missing UTF-8 charset")
        canonical = [el.get("href") for el in doc.findall("./head/link")
                     if "canonical" in el.get("rel", "").split()]
        expected = ORIGIN + route(path)
        if canonical != [expected]:
            fail(path, f"canonical must be {expected}")
        if [el.get("content") for el in metas if el.get("property") == "og:url"] != [expected]:
            fail(path, "og:url must match canonical")
        for script in doc.findall(".//script"):
            if script.get("type") == "application/ld+json":
                try:
                    json.loads(script.text or "")
                except ValueError as error:
                    fail(path, f"invalid JSON-LD: {error}")

    if not documents:
        errors.append("No HTML pages found")
    for path, doc in documents.items():
        for el in doc.iter():
            if el.tag == "img" and "alt" not in el.attrib:
                fail(path, "image missing alt attribute")
            for attribute in ("href", "src", "poster"):
                value = el.get(attribute)
                if value is None:
                    continue
                if not value.strip():
                    fail(path, f"empty {attribute}")
                    continue
                try:
                    result = local_target(path, value)
                    if result is None:
                        continue
                    target, fragment = result
                    if not target.is_file():
                        fail(path, f"missing local file: {value}")
                    elif fragment and target in ids and fragment not in ids[target]:
                        fail(path, f"missing anchor: {value}")
                except ValueError as error:
                    fail(path, f"invalid URL {value}: {error}")

    for path in (ROOT / "assets" / "img").rglob("*"):
        if path.suffix.lower() in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif"):
            try:
                with Image.open(path) as picture:
                    picture.verify()
            except Exception as error:
                fail(path, f"unreadable image: {error}")
    try:
        sitemap = ET.parse(ROOT / "sitemap.xml")
        locations = [el.text for el in sitemap.findall(".//{*}loc")]
        expected = {ORIGIN + route(path) for path in documents}
        if set(locations) != expected or len(locations) != len(set(locations)):
            errors.append("sitemap.xml: URLs must match all HTML pages without duplicates")
    except (OSError, ET.ParseError) as error:
        errors.append(f"sitemap.xml: {error}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"PASS: {len(documents)} HTML pages, metadata, internal links, anchors, images and sitemap")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
