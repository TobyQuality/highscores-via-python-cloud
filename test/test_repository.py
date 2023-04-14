import os
import unittest
from unittest.mock import mock_open, patch
from utils.repository import open_file, read_database, fetch_highscores, fetch_player_data

class TestRepositoryFunctions(unittest.TestCase):

    def test_open_file(self):
        # Mocking the open function using mock_open
        m = mock_open()
        with patch('builtins.open', m):
            # Call the function with 'r' argument
            open_file('r')
            # Assert that open was called with the correct arguments
            m.assert_called_once_with(os.path.join('..', 'highscores.json'), 'r')

    def test_read_database(self):
        # Mocking the read_file function and its return value
        with patch('utils.repository.read_file') as mock_read_file:
            mock_read_file.return_value = '{"name": "John", "highscore": 100}'
            result = read_database()
            # Assert that the mocked read_file function was called
            mock_read_file.assert_called_once()
            # Assert that the result is correct
            self.assertEqual(result, '{"name": "John", "highscore": 100}')

    def test_fetch_highscores(self):
        # Mocking the read_database function and its return value
        with patch('utils.repository.read_database') as mock_read_database:
            mock_read_database.return_value = '[{"name": "John", "highscore": 100}, {"name": "Alice", "highscore": 90}]'
            # Test case 1: Sort by none
            result = fetch_highscores(limit=2, sort='none')
            expected = [{'player': 'John', 'highscore': 100}, {'player': 'Alice', 'highscore': 90}]
            self.assertEqual(result, expected)

            # Test case 2: Sort by asc
            result = fetch_highscores(limit=2, sort='asc')
            expected = [{'player': 'Alice', 'highscore': 90}, {'player': 'John', 'highscore': 100}]
            self.assertEqual(result, expected)

            # Test case 3: Sort by desc
            result = fetch_highscores(limit=2, sort='desc')
            expected = [{'player': 'John', 'highscore': 100}, {'player': 'Alice', 'highscore': 90}]
            self.assertEqual(result, expected)

    def test_fetch_player_data(self):
        # Mocking the read_database function and its return value
        with patch('utils.repository.read_database') as mock_read_database:
            mock_read_database.return_value = '[{"id": 1, "name": "John", "highscore": 100}, {"id": 2, "name": "Alice", "highscore": 90}]'
            # Test case 1: Existing player
            result = fetch_player_data(id=1)
            expected = {"id": 1, "name": "John", "highscore": 100}
            self.assertEqual(result, expected)

            # Test case 2: Non-existing player
            result = fetch_player_data(id=3)
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
