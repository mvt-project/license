#!/usr/bin/env python3
"""Generates the GitHub Pages site from MVT License text files."""

import glob
import os
import re

VERSION_PAGE = """\
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>MVT License {version}</title>
    <style>
        body {{
            font-family: monospace;
            max-width: 80ch;
            margin: 0 auto;
            padding: 1em;
        }}
    </style>
</head>
<body>
<pre>{text}</pre>
</body>
</html>
"""

REDIRECT_PAGE = """\
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0;url=/{version}/">
    <title>MVT License</title>
</head>
<body>
    <p>Redirecting to <a href="/{version}/">MVT License {version}</a>...</p>
</body>
</html>
"""


def html_escape(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    out = "_site"
    os.makedirs(out, exist_ok=True)

    # Discover all versioned license files
    versions = []
    for path in glob.glob("MVT License *.txt"):
        m = re.match(r"MVT License (.+)\.txt", path)
        if m:
            versions.append((m.group(1), path))

    versions.sort(key=lambda v: [int(n) for n in v[0].split(".")])
    latest = versions[-1][0]

    # Generate a page for each version
    for version, path in versions:
        with open(path) as f:
            text = html_escape(f.read())
        version_dir = os.path.join(out, version)
        os.makedirs(version_dir, exist_ok=True)
        with open(os.path.join(version_dir, "index.html"), "w") as f:
            f.write(VERSION_PAGE.format(version=version, text=text))

    # Root redirects to latest version
    with open(os.path.join(out, "index.html"), "w") as f:
        f.write(REDIRECT_PAGE.format(version=latest))

    print(f"Built {len(versions)} version(s): {[v[0] for v in versions]}, latest: {latest}")


if __name__ == "__main__":
    main()
