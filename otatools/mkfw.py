#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple firmware packager tool.
"""

import argparse
import cbor
import zlib
import hashlib
import subprocess
import os
from datetime import datetime as DT
from dateutil.parser import parse as dt_parse
from dateutil.tz import tzlocal
from os.path import basename


def main():
    def dflt_build_date():
        v = os.environ.get("BUILD_DATE")
        if v:
            return dt_parse(v)
        else:
            return DT.now(tz=tzlocal())

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--outfile", metavar="OUTFILE", type=argparse.FileType("wb"), required=True, help="Output file")
    parser.add_argument("--no-compress", action="store_true", help="Do not compress images")

    meta = parser.add_argument_group("Metadata")
    meta.add_argument("--desc", help="Description")
    meta.add_argument("-b", "--board", required=True, help="Board ID")
    meta.add_argument("-d", "--build-date", type=dt_parse, default=dflt_build_date(), help="Build date")
    meta_scm_excl = meta.add_mutually_exclusive_group(required=True)
    meta_scm_excl.add_argument("-vr", "--ver-rev", nargs=2, metavar=('VER', 'REV'), help="Version and SCM revision strings")
    meta_scm_excl.add_argument("--git-identity", action="store_true", help="Get revision and version from GIT SCM")

    # unfortunately it can't help parse flags like this: "-n abc.bin file.bin -a 0x00800000 file2.bin" to:
    # <group #1: name=abc.bin srcfile=file.bin>
    # <group #2: load_addr=0x00800000 srcfile=file2.bin>
    srcgroup = parser.add_argument_group("Source file arguments")
    srcgroup.add_argument("-n", "--name", action="append", help="Image name (e.g. firmware.bin)")
    srcgroup.add_argument("-a", "--load-addr", metavar="ADDR", type=lambda x: int(x, base=0), action="append", help="Image load address")
    srcgroup.add_argument("--dfu-alt", metavar="N", type=int, action="append", help="DFU Alternate setting")
    srcgroup.add_argument("infile", metavar="INFILE", type=argparse.FileType("rb"), nargs="+", help="Source file(s)")

    args = parser.parse_args()

    # I found bug in _cbor.so: don't encode Tag 0 (ver 0.1.25)
    # https://bitbucket.org/bodhisnarkva/cbor/issues/11/failed-to-encode-tag-0-invalid-negative

    if args.git_identity:
        p = subprocess.Popen(["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE)
        rev_parse, err = p.communicate()

        p = subprocess.Popen(["git", "describe", "--always", "--dirty"], stdout=subprocess.PIPE)
        describe, err = p.communicate()

        ver, rev = describe.decode().strip(), rev_parse.decode().strip()
    else:
        ver, rev = args.ver_rev

    image_meta = {
        'description': args.desc or '',
        'build_date': cbor.Tag(0, args.build_date.isoformat()),
        'version': ver,
        'revision': rev,
        'board': args.board,
    }

    images = {}

    def getindex(lst, idx, default=None):
        if lst and len(lst) > idx:
            return lst[idx]
        else:
            return default

    for i, src in enumerate(args.infile):
        name = getindex(args.name, i, basename(src.name))
        addr = getindex(args.load_addr, i)
        dalt = getindex(args.dfu_alt, i)

        image = {}
        if addr is not None: image['load_address'] = addr
        if dalt is not None: image['dfu_alt'] = dalt

        with src as fd:
            buffer = bytes(fd.read())

            hasher = hashlib.sha1()
            hasher.update(buffer)

            image['size'] = len(buffer)
            image['sha1sum'] = bytes(hasher.digest())

            # less effective if data to random, but usual case use compressed
            deflated_buffer = bytes(zlib.compress(buffer, 9))
            if len(buffer) > len(deflated_buffer) and not args.no_compress:
                # Tag: 'z' * 100 + 22 -> zipped, base64 repr
                image['image'] = cbor.Tag(12222, deflated_buffer)
            else:
                image['image'] = buffer

        images[name] = image

    with args.outfile as fd:
        # In version 1.0.0 Tag(0) bug fixed.
        cbor.dump(
            ("OTAFWv1", image_meta, images),
            fd)


if __name__ == "__main__":
    main()
