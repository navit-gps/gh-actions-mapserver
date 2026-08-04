#!/usr/bin/env python3
"""Compare two extracted navit binfile tile directories semantically.

Parses each member as a stream of item_bin records:
  len(i32, in 4-byte words, excluding itself) type(i32) clen(i32)
  coords: clen words, attrs: rest, each attr = len(i32) type(i32) data
Canonical form: (item_type, coords, sorted attrs). Compares per-member
multisets, reporting items only in old / only in new.
"""
import struct
import sys
import zipfile
from collections import Counter
from pathlib import Path


def parse_items(data):
    items = []
    off = 0
    while off < len(data):
        (ilen,) = struct.unpack_from("<i", data, off)
        end = off + 4 + ilen * 4
        (itype,) = struct.unpack_from("<i", data, off + 4)
        (clen,) = struct.unpack_from("<i", data, off + 8)
        coords = data[off + 12 : off + 12 + clen * 4]
        attrs = []
        aoff = off + 12 + clen * 4
        while aoff < end:
            (alen,) = struct.unpack_from("<i", data, aoff)
            (atype,) = struct.unpack_from("<i", data, aoff + 4)
            attrs.append((atype, data[aoff + 8 : aoff + 4 + alen * 4]))
            aoff += 4 + alen * 4
        items.append((itype, coords, tuple(sorted(attrs))))
        off = end
    return items


class Source:
    """Reads binfile members either from an extracted dir or straight from the
    .bin zip. Streaming from the zip avoids needing disk for large maps."""

    def __init__(self, path):
        p = Path(path)
        self.zf = None if p.is_dir() else zipfile.ZipFile(p)
        self.dir = p if p.is_dir() else None

    def names(self):
        return sorted(f.name for f in self.dir.iterdir()) if self.dir else sorted(self.zf.namelist())

    def read(self, name):
        return (self.dir / name).read_bytes() if self.dir else self.zf.read(name)


def main(old_path, new_path):
    old_src, new_src = Source(old_path), Source(new_path)
    old_names, new_names = old_src.names(), new_src.names()
    bad = 0
    if old_names != new_names:
        only_old = set(old_names) - set(new_names)
        only_new = set(new_names) - set(old_names)
        print(f"MEMBER LISTS DIFFER: {len(only_old)} only-old {sorted(only_old)[:5]}, "
              f"{len(only_new)} only-new {sorted(only_new)[:5]}")
        bad += 1
    for name in old_names:
        if name not in set(new_names):
            continue
        old = Counter(parse_items(old_src.read(name)))
        new = Counter(parse_items(new_src.read(name)))
        if old == new:
            continue
        bad += 1
        print(f"=== {name}: {sum((old - new).values())} only-old, {sum((new - old).values())} only-new")
        for item, n in list((old - new).items())[:3]:
            print(f"  old only x{n}: type=0x{item[0]:x} ncoord={len(item[1])//4} attrs={[(hex(t), v[:40]) for t, v in item[2]]}")
        for item, n in list((new - old).items())[:3]:
            print(f"  new only x{n}: type=0x{item[0]:x} ncoord={len(item[1])//4} attrs={[(hex(t), v[:40]) for t, v in item[2]]}")
    print(f"{bad} members differ semantically" if bad
          else f"ALL {len(old_names)} MEMBERS SEMANTICALLY IDENTICAL (modulo item/attr order)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
