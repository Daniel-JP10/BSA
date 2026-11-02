import io
import sys
import unittest
import zipfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from bsa import xlsx  # noqa: E402

WORKBOOK = ('<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>{sheets}</sheets></workbook>')
RELS = '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{rels}</Relationships>'
SHEET = '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>{rows}</sheetData></worksheet>'


def make_xlsx(book: dict[str, list[list]], prefix: str = "") -> bytes:
    """A minimal workbook. Text is stored inline, numbers as numbers, None as a missing cell."""
    sheets, rels, parts = "", "", {}
    for index, (name, table) in enumerate(book.items(), 1):
        sheets += f'<sheet name="{name}" sheetId="{index}" r:id="rId{index}"/>'
        rels += f'<Relationship Id="rId{index}" Target="worksheets/sheet{index}.xml"/>'
        rows = ""
        for number, values in enumerate(table, 1):
            cells = ""
            for column, value in enumerate(values):
                ref = f"{chr(65 + column)}{number}"
                if value is None:
                    continue
                cells += (f'<c r="{ref}"><v>{value}</v></c>' if isinstance(value, (int, float))
                          else f'<c r="{ref}" t="inlineStr"><is><t>{value}</t></is></c>')
            rows += f'<row r="{number}">{cells}</row>'
        parts[f"xl/worksheets/sheet{index}.xml"] = prefix + SHEET.format(rows=rows)
    parts["xl/workbook.xml"] = WORKBOOK.format(sheets=sheets)
    parts["xl/_rels/workbook.xml.rels"] = RELS.format(rels=rels)
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w") as z:
        for name, text in parts.items():
            z.writestr(name, text)
    return out.getvalue()


class Reader(unittest.TestCase):
    def test_round_trip(self):
        book = {"First": [["a", "b"], ["x", 3]], "Second": [["only"]]}
        self.assertEqual(xlsx.read_book(io.BytesIO(make_xlsx(book))), book)

    def test_missing_cells_are_none(self):
        data = make_xlsx({"S": [["a", None, "c"], [1, 2.5, None]]})
        self.assertEqual(xlsx.read_book(io.BytesIO(data))["S"], [["a", None, "c"], [1, 2.5]])

    def test_doctype_is_refused(self):
        data = make_xlsx({"S": [["a"]]}, prefix='<!DOCTYPE x [<!ENTITY e "boom">]>')
        with self.assertRaises(ValueError):
            xlsx.read_book(io.BytesIO(data))

    def test_entity_is_refused(self):
        data = make_xlsx({"S": [["a"]]}, prefix='<!ENTITY e "boom">')
        with self.assertRaises(ValueError):
            xlsx.read_book(io.BytesIO(data))

    def test_oversized_parts_are_refused(self):
        with mock.patch.object(xlsx, "MAX_PART", 10), self.assertRaises(ValueError):
            xlsx.read_book(io.BytesIO(make_xlsx({"S": [["a"]]})))

    def test_not_a_spreadsheet(self):
        with self.assertRaises(zipfile.BadZipFile):
            xlsx.read_book(io.BytesIO(b"not a zip"))


if __name__ == "__main__":
    unittest.main()
