import unittest
import requests
import json
from dotenv import load_dotenv
import os

class TestHighscoresAPI(unittest.TestCase):

    load_dotenv()

    API_KEY = os.environ.get('API_KEY')

    API_URL = "http://localhost:5000/api/highscores"

    def test_get_highscores(self):
        # Test getting highscores via API
        response = requests.get(self.API_URL + "?pw=" + self.API_KEY)
        self.assertEqual(response.status_code, 200)

    def test_get_players_highscore(self):
        # Test getting a specific player's highscore via API
        response = requests.get(self.API_URL + "/1?pw=" + self.API_KEY)
        self.assertEqual(response.status_code, 200)

    #def test_add_highscore(self):
        # Test adding a player's highscore via API
        #headers = {'Content-type': 'application/json'}
        #data = json.dumps({'player_name': 'John Doe', 'overall_highscore': 100})
        #response = requests.post(self.API_URL + "?pw=API_KEY", headers=headers, data=data)
        #self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()