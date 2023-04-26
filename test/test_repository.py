import unittest
from utils.repository import *

class RepositoryTests(unittest.TestCase):

    def test_fetch_highscores(self):
        """
        Test case for fetch_highscores function.

        Test fetch_highscores function with limit=5 and sort="desc".
        """
        # Test fetch_highscores function
        highscores = fetch_highscores(limit=5, sort="desc")
        self.assertIsInstance(highscores, list)
        self.assertGreaterEqual(len(highscores), 0)
        self.assertLessEqual(len(highscores), 5)

    def test_fetch_highscore(self):
        """
        Test case for fetch_highscore function.

        Test fetch_highscore function with player ID 1.
        """
        # Test fetch_highscore function
        player_data = fetch_highscore(1)
        self.assertIsInstance(player_data, dict)
        self.assertIn('id', player_data)
        self.assertIn('name', player_data)
        self.assertIn('highscore', player_data)

    def test_save_highscore(self):
        """
        Test case for save_highscore function.

        Test save_highscore function with name="John" and highscore=100.
        """
        # Test save_highscore function
        save_highscore("John", 100)
        player_data = fetch_highscore(2)
        self.assertEqual(player_data['name'], 'John')
        self.assertEqual(player_data['highscore'], 100)

    def test_remove_highscore(self):
        """
        Test case for remove_highscore function.

        Test remove_highscore function with player ID 2.
        """
        #Test remove_highscore function
        remove_highscore(2)
        player_data = fetch_highscore(2)
        self.assertEqual(player_data, None)

    def test_save_highscore_with_invalid_input(self):
        """
        Test case for save_highscore function with invalid input.

        Test save_highscore function with name="John" and highscore="invalid_score".
        Expects an exception to be raised.
        """
        # Test save_highscore function with invalid input
        with self.assertRaises(Exception):
            save_highscore("John", "invalid_score")