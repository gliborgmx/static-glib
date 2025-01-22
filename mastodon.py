#!/usr/bin/env python3

import requests
import uuid
import os
import sys
import re
from typing import Optional

MESSAGE = '¡Hemos publicado un nuevo texto!'
BASE_BLOG_URL = 'https://glib.org.mx/'
BASE_URL = 'https://floss.social/api/v1/statuses'

URI='urn:ietf:wg:oauth:2.0:oob'

META_RE = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+)\s*=\s*"(?P<value>.*)"$')
BEGIN_RE = re.compile(r'^\+{3}(\s.*)?')
END_RE = re.compile(r'^(\+{3}|\.{3})(\s.*)?')

ACCESS_TOKEN = ""

def publish(meta: dict) -> bool:
    # https://docs.joinmastodon.org/methods/statuses/#headers
    headers: dict = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Idempotency-Key": str(uuid.uuid4()),
    }

    try:
        # https://docs.joinmastodon.org/methods/statuses/#form-data-parameters
        form_data: dict = {
            "status": f"{MESSAGE}\n\n{meta['title'][0]}\n\n{BASE_BLOG_URL}{meta['slug'][0]}",
            "visibility": "public",
            "language": "es",
        }
    except KeyError as e:
        return False

    response = requests.post(BASE_URL, headers=headers, data=form_data)
    if response.status_code == requests.codes.ok:
        return 0

    print(f"Request error: {response.text}")
    return -1

def get_meta(fname: str) -> Optional[dict]:
    meta: dict[str, list[str]] = {}
    with open(fname) as fn:
        line = next(fn).strip()
        if BEGIN_RE.match(line):
            while line:
                line = next(fn).strip()
                if END_RE.match(line):
                    return meta
                else:
                    m1 = META_RE.match(line)
                    if m1:
                        key = m1.group('key').lower().strip()
                        value = m1.group('value').strip()
                        try:
                            meta[key].append(value)
                        except KeyError:
                            meta[key] = [value]
    return None

def process(fname: str) -> int:
    meta = get_meta(fname)
    if meta and publish(meta):
        return 0
    return -1

def main() -> int:
    try:
        global ACCESS_TOKEN
        ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
    except KeyError as e:
        return -1

    if len(sys.argv) == 2:
        return process(sys.argv[1])
    return -1

if __name__ == '__main__':
    sys.exit(main())
