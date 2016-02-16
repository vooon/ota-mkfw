#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Firmware flasher tool.
Require dfu-util program.
"""

import argparse
import cbor
import zlib
import hashlib
import subprocess
import tempfile
from datetime import datetime as DT
from dateutil.parser import parse as dt_parse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("infile", metavar="FILE", type=argparse.FileType('rb'), help=".ofw firmware file")
    parser.add_argument("--sudo", action="store_true", help="Require root access for dfu-util")
    parser.add_argument("--leave", action="store_true", help="Flash and ask device to leave DFU mode")
    parser.add_argument("-d", "--dfu-args", action="append", help="dfu-util arguments")

    args = parser.parse_args()

    print args

    tag0 = cbor.ClassTag(0, DT, None, decode_function=dt_parse)
    tag12222 = cbor.ClassTag(12222, bytes, None, decode_function=zlib.decompress)

    tm = cbor.TagMapper(class_tags=[tag0, tag12222], raise_on_unknown_tag=True)
    root = tm.load(args.infile)

    if not isinstance(root, list):
        raise Exception("Unknown file structure.")

    if root[0] != "OTAFWv1":
        raise Exception("Unknown file magic")

    _, image_meta, images = root

    print("Matadata:")
    print("  Board ID: %s" % image_meta['board'])
    print("  Version: %s" % image_meta['version'])
    print("  Revision: %s" % image_meta['revision'])
    print("  Build Date: %s" % image_meta['build_date'])
    print("")

    if "firmware.bin" not in images:
        raise Exception("No firmware.bin")

    image = images["firmware.bin"]
    if "load_address" not in image:
        raise Exception("Load address not set!")
    if "dfu_alt" not in image:
        raise Exception("DFU Alternate setting not set!")

    image_bin = image['image']
    if image['size'] != len(image_bin):
        raise Exception("Image size error")

    sha1sum = image.get('sha1sum')
    if sha1sum:
        hasher = hashlib.sha1()
        hasher.update(image_bin)
        sum = hasher.digest()

        if sum != sha1sum:
            raise Exception("SHA1 sum not match!")

    with tempfile.NamedTemporaryFile(prefix="firmware-", suffix=".bin", mode="wb") as tfd:
        tfd.write(image_bin)
        tfd.file.flush()

        cmd = ["dfu-util",
               "--alt", str(image['dfu_alt']),
               "--dfuse-address", ('0x%08X:leave' if args.leave else '0x%08X') % image['load_address'],
               "--download", tfd.name]

        if args.dfu_args:
            for s in args.dfu_args:
                cmd += s.split()

        if args.sudo:
            cmd = ['sudo'] + cmd

        print("Exec: " + " ".join(cmd))
        proc = subprocess.Popen(cmd)
        proc.communicate()


if __name__ == "__main__":
    main()
