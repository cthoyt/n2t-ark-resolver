"""Implement an ARK metaresolver based on N2T.

1. Run this file with ``python n2t_arks.py``
2. Navigate to http://localhost:5000/ark:/53355/cl010277627
3. You get redirected to https://collections.louvre.fr/ark:/53355/cl010277627
"""

import pystow

import yaml
from curies import Converter, get_flask_app
import unittest

URL = "https://n2t.net/e/n2t_full_prefixes.yaml"
PROTOCOLS = {"https://", "http://", "ftp://"}


def get_prefix_map():
    """Get the prefix map from N2T, not including redundant ``ark:/`` in prefixes."""
    with pystow.ensure_open("n2t", url=URL) as file:
        records = yaml.safe_load(file)
    prefix_map = {}
    for key, record in records.items():
        redirect = record.get('redirect')
        if not redirect:
            continue
        if all(not redirect.startswith(protocol) for protocol in PROTOCOLS):
            continue
        if redirect.count('$id') != 1:
            continue
        if not redirect.endswith("$id"):
            continue
        if not key.startswith("ark:/"):
            continue
        prefix_map[key.removeprefix("ark:/")] = redirect.removesuffix("$id") + "/" + key.removeprefix("ark:/") + "/"

    return prefix_map


def get_app():
    """Get an ARK resolver app, noting that it uses a non-standard delimiter and URL prefix."""
    prefix_map = get_prefix_map()
    print(prefix_map)
    converter = Converter.from_prefix_map(prefix_map, delimiter="/")
    app = get_flask_app(converter, blueprint_kwargs=dict(url_prefix="/ark:"))
    return app


class TestApp(unittest.TestCase):
    """Tests for the ARK resolver."""

    def setUp(self) -> None:
        """Set up each test with an app."""
        self.app = get_app()

    def test_redirect(self):
        """Test redirecting properly"""
        curie = "53355/cl010277627"
        with self.app.test_client() as client:
            res = client.get(f"/ark:/{curie}", follow_redirects=False)
            self.assertEqual(302, res.status_code)


if __name__ == '__main__':
    get_app().run()
