import unittest
from utils.repository import *
from index import *

class RepositoryTests(unittest.TestCase):

    load_dotenv()
    API_KEY = os.environ.get('API_KEY')

    # There should be only one object inside the highscores.json
    # Otherwise the code won't work

    def test_fetch_highscores(self):
        # Test fetch_highscores function
        highscores = fetch_highscores(limit=5, sort="desc")
        self.assertIsInstance(highscores, list)
        self.assertGreaterEqual(len(highscores), 0)
        self.assertLessEqual(len(highscores), 5)

    def test_fetch_highscore(self):
        # Test fetch_highscore function
        player_data = fetch_highscore(1)
        self.assertIsInstance(player_data, dict)
        self.assertIn('id', player_data)
        self.assertIn('name', player_data)
        self.assertIn('highscore', player_data)

    def test_save_highscore(self):
        # Test save_highscore function
        save_highscore("John", 100)
        player_data = fetch_highscore(2)
        self.assertEqual(player_data['name'], 'John')
        self.assertEqual(player_data['highscore'], 100)

    def test_delete_highscore(self):
        #Test remove_highscore function
        remove_highscore(2)
        player_data = fetch_highscore(2)
        self.assertEqual(player_data, None)

    def test_save_highscore_with_invalid_input(self):
        # Test save_highscore function with invalid input
        with self.assertRaises(Exception):
            save_highscore("John", "invalid_score")

    def test_check_api_key(self):
        # Test case 1: Correct password
        pw = API_KEY
        assert check_api_key(pw) == True

        # Test case 2: Incorrect password
        pw = "wrong_password"
        assert check_api_key(pw) == False
    
    def test_get_highscores(self):
        # Test case 1: Correct API key
        with app.test_client() as client:
            response = client.get('/api/highscores?pw=' + API_KEY)
            assert response.status_code == 200

        # Test case 2: Incorrect API key
        with app.test_client() as client:
            response = client.get('/api/highscores?pw=wrong_password')
            assert response.status_code == 401

    def test_get_players_highscore(self):
        # Test case 1: Correct API key and existing player ID
        with app.test_client() as client:
            response = client.get('/api/highscores/1?pw=' + API_KEY)
            assert response.status_code == 200

        # Test case 2: Incorrect API key
        with app.test_client() as client:
            response = client.get('/api/highscores/1?pw=wrong_password')
            assert response.status_code == 401

        # Test case 3: Non-existing player ID
        with app.test_client() as client:
            response = client.get('/api/highscores/999?pw=' + API_KEY)
            assert response.status_code == 404

    def test_add_highscore(self):
    # Test case 1: Correct API key and valid data
        with app.test_client() as client:
            sent_data = {'name': 'chummy', 'overall_highscore': 100}
            response = client.post('/api/highscores?pw=' + API_KEY, data=json.dumps(sent_data), content_type='application/json')
            assert response.status_code == 201

        # Test case 2: Incorrect API key
        with app.test_client() as client:
            sent_data = {'name': 'dummy', 'overall_highscore': 100}
            response = client.post('/api/highscores?pw=wrong_password', data=json.dumps(sent_data), content_type='application/json')
            assert response.status_code == 401

        # Test case 3: Invalid data
        with app.test_client() as client:
            sent_data = {'name': 'd', 'overall_highscore': 100}
            response = client.post('/api/highscores?pw=' + API_KEY, data=json.dumps(sent_data), content_type='application/json')
            assert response.status_code == 400