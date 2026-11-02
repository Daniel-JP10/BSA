"""Minimal read-only .xlsx reader, standard library only.

Spreadsheets from outside are untrusted. Nothing in them is executed, XML that declares a DOCTYPE
or an ENTITY is refused, and every part has a size limit.
"""
import re
import xml.etree.ElementTree as ET
import zipfile

MAX_PART = 20_000_000
NS = {
    "m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "p": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def _parse(z: zipfile.ZipFile, name: str) -> ET.Element:
    if z.getinfo(name).file_size > MAX_PART:
        raise ValueError(f"{name} is too large")
    data = z.read(name)
    if re.search(rb"<!(DOCTYPE|ENTITY)", data, re.I):
        raise ValueError(f"{name} declares a DOCTYPE or ENTITY")
    return ET.fromstring(data)


def _column(reference: str) -> int:
    number = 0
    for letter in re.match(r"[A-Z]+", reference).group(0):
        number = number * 26 + ord(letter) - 64
    return number - 1


def _text(element: ET.Element) -> str:
    return "".join(t.text or "" for t in element.iter("{%s}t" % NS["m"]))


def read_book(source) -> dict[str, list[list]]:
    """Sheet name -> rows. `source` is a path or a binary file object. Missing cells are None."""
    z = zipfile.ZipFile(source)
    strings = []
    if "xl/sharedStrings.xml" in z.namelist():
        strings = [_text(si) for si in _parse(z, "xl/sharedStrings.xml").findall("m:si", NS)]
    targets = {r.get("Id"): r.get("Target") for r in _parse(z, "xl/_rels/workbook.xml.rels").findall("p:Relationship", NS)}
    book = {}
    for sheet in _parse(z, "xl/workbook.xml").find("m:sheets", NS):
        target = targets[sheet.get("{%s}id" % NS["r"])].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        rows = []
        for row in _parse(z, target).iter("{%s}row" % NS["m"]):
            cells = {}
            for cell in row.findall("m:c", NS):
                kind, value = cell.get("t"), cell.find("m:v", NS)
                if kind == "s" and value is not None:
                    content = strings[int(value.text)]
                elif kind == "inlineStr":
                    content = _text(cell)
                elif value is not None:
                    content = value.text
                    if kind not in ("str", "b", "e"):
                        try:
                            number = float(content)
                            content = int(number) if number == int(number) else number
                        except ValueError:
                            pass
                else:
                    content = None
                cells[_column(cell.get("r"))] = content
            rows.append([cells.get(i) for i in range(max(cells) + 1)] if cells else [])
        book[sheet.get("name")] = rows
    return book
