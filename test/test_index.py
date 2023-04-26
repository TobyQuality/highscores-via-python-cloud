from dotenv import load_dotenv    
from index import *
import unittest

class RepositoryTests(unittest.TestCase):

    load_dotenv()
    API_KEY = os.environ.get('API_KEY')

    def test_check_api_key(self):
        """
        Test case for checking API key validation.

        Test case 1: Correct password
        Test case 2: Incorrect password
        """
        # Test case 1: Correct password
        pw = API_KEY
        assert check_api_key(pw) == True

        # Test case 2: Incorrect password
        pw = "wrong_password"
        assert check_api_key(pw) == False
    
    def test_get_highscores(self):
        """
        Test case for getting highscores API endpoint.

        Test case 1: Correct API key
        Test case 2: Incorrect API key
        """
        # Test case 1: Correct API key
        with app.test_client() as client:
            response = client.get('/api/highscores?pw=' + API_KEY)
            assert response.status_code == 200

        # Test case 2: Incorrect API key
        with app.test_client() as client:
            response = client.get('/api/highscores?pw=wrong_password')
            assert response.status_code == 401

    def test_get_players_highscore(self):
        """
        Test case for getting player's highscore API endpoint.

        Test case 1: Correct API key and existing player ID
        Test case 2: Incorrect API key
        Test case 3: Non-existing player ID
        """
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
        """
        Test case for adding highscore API endpoint.

        Test case 1: Correct API key and valid data
        Test case 2: Incorrect API key
        Test case 3: Invalid data
        """
        # Test case 1: Correct API key and valid data
        with app.test_client() as client:
            sent_data = {'player_name': 'chummy', 'overall_highscore': 100}
            response = client.post('/api/highscores?pw=' + API_KEY, data=json.dumps(sent_data), content_type='application/json')
            assert response.status_code == 201

        # Test case 2: Incorrect API key
        with app.test_client() as client:
            sent_data = {'player_name': 'dummy', 'overall_highscore': 100}
            response = client.post('/api/highscores?pw=wrong_password', data=json.dumps(sent_data), content_type='application/json')
            assert response.status_code == 401

        # Test case 3: Invalid data
        with app.test_client() as client:
            sent_data = {'player_name': 'd', 'overall_highscore': 100}
            response = client.post('/api/highscores?pw=' + API_KEY, data=json.dumps(sent_data), content_type='application/json')
            assert response.status_code == 400
    
    def test_delete_highscore(self):
        """
        Test case for deleting a highscore API endpoint.

        Test case 1: Correct API key and existing highscore ID
        """
        with app.test_client() as client:
            response = client.delete('/api/highscores/2?pw=' + API_KEY)
            assert response.status_code == 204