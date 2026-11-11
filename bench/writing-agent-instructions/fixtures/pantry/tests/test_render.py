import unittest

from pantry import render


class RenderTest(unittest.TestCase):
    def test_item_names_are_escaped(self):
        html = render.rows([{"name": "<b>salt</b>", "quantity": 1, "unit": "box"}])
        self.assertIn("&lt;b&gt;salt&lt;/b&gt;", html)
        self.assertNotIn("<b>", html)
