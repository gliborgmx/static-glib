#!/usr/bin/env python3

"""Publish a Tooth given an MD file"""

from typing import Optional

import os
import re
import sys
import uuid
import requests

MESSAGE = '¡Hemos publicado un nuevo texto!'
BASE_BLOG_URL = 'https://glib.org.mx/'
BASE_URL = 'https://floss.social/api/v1/statuses'

URI = 'urn:ietf:wg:oauth:2.0:oob'

META_RE = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+)\s*=\s*"(?P<value>.*)"$')
BEGIN_RE = re.compile(r'^\+{3}(\s.*)?')
END_RE = re.compile(r'^(\+{3}|\.{3})(\s.*)?')

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')


def publish(meta: dict) -> bool:
    """HTTP post message to mastodon server with message to publish"""
    # https://docs.joinmastodon.org/methods/statuses/#headers
    headers: dict = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Idempotency-Key": str(uuid.uuid4()),
    }

    try:
        status = f"{MESSAGE}\n\n{meta['title'][0]}\n\n"\
            f"{BASE_BLOG_URL}{meta['slug'][0]}"
    except LookupError:
        print("meta doesn't contain title or slug")
        return False

    # https://docs.joinmastodon.org/methods/statuses/#form-data-parameters
    form_data: dict = {
        "status": status,
        "visibility": "public",
        "language": "es",
    }

    try:
        if meta['draft'] and \
           meta['draft'][0] in ['true', 'True', 'yes', 'Yes', '1']:
            print(f"article {meta['slug'][0]} is a draft")
            return True
    except LookupError:
        pass

    response = requests.post(BASE_URL,
                             headers=headers,
                             data=form_data,
                             timeout=5)
    if response.status_code == requests.codes.ok:  # pylint: disable=no-member
        return True

    print(f"Request error: {response.text}")
    return False


def get_meta(fname: str) -> Optional[dict]:
    """Gets meta information of the post"""
    meta: dict[str, list[str]] = {}
    with open(fname, encoding="utf-8") as fn:
        line = next(fn).strip()
        if BEGIN_RE.match(line):
            while line:
                line = next(fn).strip()
                if END_RE.match(line):
                    return meta

                m1 = META_RE.match(line)
                if m1:
                    key = m1.group('key').lower().strip()
                    value = m1.group('value').strip()
                    try:
                        meta[key].append(value)
                    except LookupError:
                        meta[key] = [value]

    print(f"No metada data found in {fname}")
    return None


def process(fname: str) -> int:
    """Gets article's meta and publish the link in mastodon"""
    meta = get_meta(fname)
    if meta and publish(meta):
        return 0
    print('Unknown error')
    return -1


def main() -> int:
    """Main function"""
    if ACCESS_TOKEN and len(sys.argv) == 2:
        return process(sys.argv[1])
    print('No access token or missing parameter')
    return -1


if __name__ == '__main__':
    sys.exit(main())
