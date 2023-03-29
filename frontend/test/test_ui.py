import unittest

import ui


# python3 -m unittest test.test_ui


class TestUi(unittest.TestCase):

    def test_get_title(self):
        self.assertEqual(ui.get_title(), "Battleship")
