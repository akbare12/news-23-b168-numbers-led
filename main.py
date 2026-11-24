#!/usr/bin/env python3
"""main.py — news-23 b168 numbers-led entry generator (stdlib only, no PIL).

Reads the entry PNG next to this file, validates it strictly (PNG signature,
IHDR 1024x1024, bit depth 8, colour type 2/6, zero compression/filter/
interlace, per-chunk CRCs, non-empty IDAT payload, IEND last with no trailing
data, size bounds, pinned sha256/size), then writes a byte-identical copy to
$MAKEFUN_OUTPUT_DIR/entry.png (default: ./out/entry.png).

Guards: refuses an empty MAKEFUN_OUTPUT_DIR, an output dir inside this repo,
an output path that is an existing file, or an output that would overwrite
the source image.
"""
import hashlib
import os
import struct
import sys
import zlib

EXPECTED_SHA256 = "4626a1b86f6d0b85770d624e9b6ddee9aa07b4904c9a379051dfd9ed0439c476"
EXPECTED_SIZE = 142187

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
MIN_SIZE = 10000
MAX_SIZE = 1024 * 1024


def fail(msg):
    print(f"main.py: error: {msg}", file=sys.stderr)
    sys.exit(1)


def parse_png(data):
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        fail("bad PNG signature")
    pos = 8
    first = True
    idat_total = 0
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            fail("truncated chunk header")
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + length > len(data):
            fail(f"truncated chunk {ctype!r}")
        chunk_data = data[pos + 8:pos + 8 + length]
        (crc_stored,) = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])
        crc_calc = zlib.crc32(ctype + chunk_data) & 0xFFFFFFFF
        if crc_calc != crc_stored:
            fail(f"CRC mismatch in chunk {ctype!r}")
        if first:
            if ctype != b"IHDR" or length != 13:
                fail("first chunk must be a 13-byte IHDR")
            w, h, depth, ctype_id, comp, filt, inter = struct.unpack(
                ">IIBBBBB", chunk_data)
            if (w, h) != (1024, 1024):
                fail(f"bad dimensions {w}x{h}, expected 1024x1024")
            if depth != 8:
                fail(f"bad bit depth {depth}, expected 8")
            if ctype_id not in (2, 6):
                fail(f"bad colour type {ctype_id}, expected 2 or 6")
            if comp != 0 or filt != 0 or inter != 0:
                fail("compression/filter/interlace must all be 0")
            first = False
        if ctype == b"IDAT":
            if length == 0:
                fail("empty IDAT chunk")
            idat_total += length
        if ctype == b"IEND":
            if length != 0:
                fail("IEND must be 0 bytes")
            if pos + 12 + length != len(data):
                fail("trailing data after IEND")
            seen_iend = True
            pos += 12 + length
            break
        pos += 12 + length
    if first:
        fail("no IHDR chunk found")
    if not seen_iend:
        fail("no IEND chunk found")
    if idat_total < 1000:
        fail(f"IDAT payload too small: {idat_total} bytes")
    return idat_total


def main():
    if not os.path.isfile(SOURCE):
        fail(f"source image missing: {SOURCE}")
    with open(SOURCE, "rb") as f:
        data = f.read()
    if len(data) < MIN_SIZE:
        fail(f"image too small: {len(data)} bytes")
    if len(data) > MAX_SIZE:
        fail(f"image too large: {len(data)} bytes (>1 MiB)")
    parse_png(data)
    sha = hashlib.sha256(data).hexdigest()
    if EXPECTED_SHA256 != "PLACEHOLDER" and sha != EXPECTED_SHA256:
        fail(f"sha256 mismatch: got {sha}")
    if EXPECTED_SIZE and len(data) != EXPECTED_SIZE:
        fail(f"size mismatch: got {len(data)}, expected {EXPECTED_SIZE}")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is empty")
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir_abs = os.path.abspath(out_dir)
    if os.path.isfile(out_dir_abs):
        fail(f"MAKEFUN_OUTPUT_DIR is a file: {out_dir_abs}")
    if os.path.commonpath([out_dir_abs, repo_dir]) == repo_dir:
        fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    out_path = os.path.join(out_dir_abs, "entry.png")
    if os.path.abspath(out_path) == os.path.abspath(SOURCE):
        fail("output would overwrite the source image")
    os.makedirs(out_dir_abs, exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(data)
    with open(out_path, "rb") as f:
        written = f.read()
    if written != data:
        fail("re-read output is not byte-identical to source")
    print(f"main.py: wrote {out_path} ({len(data)} bytes, sha256 {sha})")


if __name__ == "__main__":
    main()
