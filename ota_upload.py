#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File uploader tool for OTA server.

Wery simple remote server accept http form and store file on the disk.
"""

import argparse
import requests
import os, sys
from datetime import datetime as DT
from dateutil.tz import tzlocal
from dateutil.parser import parse as dt_parse
from os.path import basename


def main():
    def env(name, default=None):
        return os.environ.get(name, default)

    def envreq(name):
        v = env(name)
        return {"required": v is None, "default": v}

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=argparse.FileType("rb"), help="File to send")
    parser.add_argument("-s", "--server", default=env("OTA_SERVER", "http://localhost:8081"), help="Form url")
    parser.add_argument("-r", "--repo", help="Project repository", **envreq("OTA_REPO"))
    parser.add_argument("-p", "--key", help="Repositopy passkey", **envreq("OTA_KEY"))
    parser.add_argument("--rev", required=True, help="SCM revision")
    parser.add_argument("--tag", help="SCM tag (version)")
    parser.add_argument("-d", "--build-date", type=dt_parse, default=DT.now(tz=tzlocal()), help="Build date")
    parser.add_argument("-t", "--file-type", help="File type (for index)")

    args = parser.parse_args()

    post = {
        "project": args.repo,
        "key": args.key,
        "rev": args.rev,
        # go time.Time do not recognize other types than returned by `date --iso-8601=s`
        # datetime.isoformat() to precise.
        "build_date": args.build_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "file_type": args.file_type,
    }

    if args.tag:
        post['tag'] = args.tag

    r = requests.post(args.server,
                      headers={
                          "user-agent": "otauploader",
                      },
                      data=post,
                      files={
                          "file": args.file,
                      },
                      timeout=1.0)

    print(r.text)
    if r.status_code != 200:
        sys.exit(1)

if __name__ == "__main__":
    main()
