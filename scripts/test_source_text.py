#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Tests for scripts/source-text (red-first, offline, deterministic).

All fixture text is deliberately fake ("widgets"): no real statistics here.
"""

import contextlib
import gzip
import importlib.machinery
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "source-text"

SNAPSHOT = "https://web.archive.org/web/20200102030405/https://example.org/a.html"
RAW_SNAPSHOT = "https://web.archive.org/web/20200102030405id_/https://example.org/a.html"
OTHER_CAPTURE = "https://web.archive.org/web/20210607080910id_/http://example.org/a.html"


def load_module():
    """Import scripts/source-text (no .py suffix) as a module."""
    loader = importlib.machinery.SourceFileLoader("source_text", str(SCRIPT))
    spec = importlib.util.spec_from_loader("source_text", loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


class FakeResponse:
    """Stands in for the object urllib.request.urlopen returns."""

    def __init__(self, body: bytes, headers: dict | None = None, url: str = RAW_SNAPSHOT):
        self._body = body
        self.headers = headers or {}
        self._url = url
        self.status = 200

    def read(self) -> bytes:
        return self._body

    def geturl(self) -> str:
        return self._url

    def __enter__(self):
        return self

    def __exit__(self, *exc) -> bool:
        return False


def build_minimal_pdf(text: str | None) -> bytes:
    """Create a minimal valid single-page PDF containing `text` (or blank if None)."""
    objects: list[bytes] = []
    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    objects.append(b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")

    if text is not None:
        escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream = f"BT /F1 12 Tf 72 720 Td ({escaped}) Tj ET\n".encode("ascii")
        objects.append(
            b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n"
        )
        objects.append(
            b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n"
        )
        objects.append(
            f"5 0 obj\n<< /Length {len(stream)} >>\nstream\n".encode("ascii")
            + stream
            + b"endstream\nendobj\n"
        )
    else:
        objects.append(
            b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n"
        )

    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(out))
        out.extend(obj)

    xref_pos = len(out)
    out.extend(f"xref\n0 {len(offsets)}\n".encode("ascii"))
    out.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode("ascii"))

    out.extend(
        f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\n"
        f"startxref\n{xref_pos}\n%%EOF\n".encode("ascii")
    )
    return bytes(out)


class CliTests(unittest.TestCase):
    """Runs the script as a subprocess, the way agents and checks call it."""

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(SCRIPT), *args],
            capture_output=True,
            text=True,
            check=False,
        )

    def run_on_file(self, data: bytes, suffix: str, *extra: str) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile("wb", suffix=suffix, delete=False) as tmp:
            tmp.write(data)
            tmp_path = tmp.name
        try:
            return self.run_cli("--file", tmp_path, *extra)
        finally:
            os.unlink(tmp_path)

    def test_script_exists_and_is_executable(self) -> None:
        self.assertTrue(SCRIPT.is_file(), f"Missing {SCRIPT}")
        self.assertTrue(os.access(SCRIPT, os.X_OK), f"{SCRIPT} is not executable")

    def test_rejects_missing_argument(self) -> None:
        res = self.run_cli()
        self.assertEqual(res.returncode, 2)
        self.assertIn("usage", res.stderr.lower())

    def test_rejects_non_wayback_url(self) -> None:
        res = self.run_cli("https://example.org/report.html")
        self.assertEqual(res.returncode, 2)
        self.assertIn("web.archive.org", res.stderr.lower())

    def test_rejects_truncated_timestamp(self) -> None:
        res = self.run_cli("--print-url", "https://web.archive.org/web/2020/https://example.org/a.html")
        self.assertEqual(res.returncode, 2)
        self.assertIn("14-digit", res.stderr)

    def test_wayback_url_rewritten_to_raw_id_modifier(self) -> None:
        res = self.run_cli("--print-url", SNAPSHOT)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(res.stdout.strip(), RAW_SNAPSHOT)

    def test_wayback_url_preserves_existing_id_modifier(self) -> None:
        res = self.run_cli("--print-url", RAW_SNAPSHOT)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(res.stdout.strip(), RAW_SNAPSHOT)

    def test_missing_file_is_a_usage_error(self) -> None:
        res = self.run_cli("--file", "/nonexistent/widget.html")
        self.assertEqual(res.returncode, 2)

    def test_extracts_html_text_without_scripts_or_styles(self) -> None:
        html = (
            "<!doctype html><html><head><title>Widget Report</title>"
            "<style>.x { color: red; }</style>"
            "<script>var secret = 999;</script></head>"
            "<body><h1>Widget Output</h1>"
            "<p>Widget output reached 12% in 1999 &amp; rose slightly.</p>"
            "<noscript>ignored</noscript>"
            "<table><tr><th>Year</th><th>Widgets</th></tr>"
            "<tr><td>1999</td><td>34 000</td></tr></table>"
            "</body></html>"
        )
        res = self.run_on_file(html.encode("utf-8"), ".html")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("Widget Output", res.stdout)
        self.assertIn("Widget output reached 12% in 1999 & rose slightly.", res.stdout)
        self.assertIn("34 000", res.stdout)
        self.assertNotIn("secret", res.stdout)
        self.assertNotIn("color: red", res.stdout)
        self.assertNotIn("ignored", res.stdout)

    def test_reads_charset_from_meta_tag(self) -> None:
        page = (
            b'<html><head><meta charset="iso-8859-1"></head>'
            b"<body><p>Gr\xfc\xdfe aus dem Widgetb\xfcro</p></body></html>"
        )
        res = self.run_on_file(page, ".html")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("Grüße aus dem Widgetbüro", res.stdout)
        self.assertNotIn("\ufffd", res.stdout)

    def test_undecodable_text_fails_loudly(self) -> None:
        page = b"<html><body><p>Widgetcaf\xe9</p></body></html>"
        res = self.run_on_file(page, ".html")
        self.assertEqual(res.returncode, 1)
        self.assertIn("--encoding", res.stderr)
        self.assertEqual(res.stdout, "")

    def test_encoding_override(self) -> None:
        page = b"<html><body><p>Widgetcaf\xe9</p></body></html>"
        res = self.run_on_file(page, ".html", "--encoding", "cp1252")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("Widgetcafé", res.stdout)

    def test_normalises_invisible_characters_but_keeps_superscripts(self) -> None:
        page = (
            "<html><body><p>34&nbsp;000 widgets; wid&shy;get; 5\u202f000 m²; "
            "zero\u200bwidth</p></body></html>"
        ).encode("utf-8")
        res = self.run_on_file(page, ".html")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("34 000 widgets; widget; 5 000 m²; zerowidth", res.stdout)

    def test_extracts_pdf_text_via_pdftotext(self) -> None:
        res = self.run_on_file(build_minimal_pdf("Sample widget text for extraction."), ".pdf")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("Sample widget text for extraction.", res.stdout)

    def test_fails_on_empty_or_scanned_pdf(self) -> None:
        res = self.run_on_file(build_minimal_pdf(None), ".pdf")
        self.assertEqual(res.returncode, 1)
        self.assertIn("no extractable text", res.stderr.lower())


class FetchTests(unittest.TestCase):
    """Exercises the network path with urlopen replaced; nothing leaves the machine."""

    PAGE = b"<html><body><p>Widget page body</p></body></html>"

    def setUp(self) -> None:
        self.mod = load_module()

    def run_main(self, *argv: str, response=None, error=None) -> tuple[int, str, str]:
        def fake_urlopen(*_args, **_kwargs):
            if error is not None:
                raise error
            return response

        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(self.mod.urllib.request, "urlopen", fake_urlopen), \
                contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = self.mod.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_gzip_encoded_capture_is_decompressed(self) -> None:
        response = FakeResponse(
            gzip.compress(self.PAGE),
            {"Content-Encoding": "gzip", "Content-Type": "text/html; charset=UTF-8"},
        )
        code, out, err = self.run_main(SNAPSHOT, response=response)
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "Widget page body\n")

    def test_gzip_body_without_header_is_decompressed(self) -> None:
        response = FakeResponse(gzip.compress(self.PAGE), {"Content-Type": "text/html"})
        code, out, err = self.run_main(SNAPSHOT, response=response)
        self.assertEqual(code, 0, err)
        self.assertEqual(out, "Widget page body\n")

    def test_unsupported_content_encoding_fails(self) -> None:
        response = FakeResponse(b"\x00\x01", {"Content-Encoding": "br"})
        code, out, err = self.run_main(SNAPSHOT, response=response)
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("br", err)

    def test_redirect_to_another_capture_fails_and_names_it(self) -> None:
        response = FakeResponse(self.PAGE, {"Content-Type": "text/html"}, url=OTHER_CAPTURE)
        code, out, err = self.run_main(SNAPSHOT, response=response)
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn(OTHER_CAPTURE, err)

    def test_network_failure_is_inconclusive(self) -> None:
        code, out, err = self.run_main(SNAPSHOT, error=urllib.error.URLError("connection refused"))
        self.assertEqual(code, 3)
        self.assertEqual(out, "")
        self.assertIn("inconclusive", err.lower())

    def test_timeout_is_inconclusive(self) -> None:
        code, _out, _err = self.run_main(SNAPSHOT, error=TimeoutError("timed out"))
        self.assertEqual(code, 3)

    def test_server_error_is_inconclusive(self) -> None:
        error = urllib.error.HTTPError(RAW_SNAPSHOT, 503, "Service Unavailable", {}, None)
        code, _out, _err = self.run_main(SNAPSHOT, error=error)
        self.assertEqual(code, 3)

    def test_missing_snapshot_is_a_source_error(self) -> None:
        error = urllib.error.HTTPError(RAW_SNAPSHOT, 404, "Not Found", {}, None)
        code, _out, err = self.run_main(SNAPSHOT, error=error)
        self.assertEqual(code, 1)
        self.assertIn("404", err)


class NormaliseTextTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mod = load_module()

    def test_keeps_page_breaks_and_drops_blank_lines(self) -> None:
        text = "page  one\n\n  line two \n\fpage\u00a0two\n"
        self.assertEqual(self.mod.normalise_text(text), "page one\nline two\n\fpage two\n")

    def test_composes_to_nfc_without_compatibility_folding(self) -> None:
        self.assertEqual(self.mod.normalise_text("u\u0308 10\u2076"), "\u00fc 10\u2076\n")


if __name__ == "__main__":
    unittest.main()
