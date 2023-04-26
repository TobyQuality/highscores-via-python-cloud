from flask import *
from json import *
from dotenv import load_dotenv
import os
import bcrypt
from utils.repository import *
from utils.validator import *

app = Flask(__name__)

# loading the .env file containing the api key for the app
load_dotenv()
# accessing the api key
API_KEY = os.environ.get('API_KEY')

# this method is used to check the validity of the password
# sent with requests to the backend
def check_api_key(pw):
    """
    Check the validity of the password sent with requests to the backend.

    Args:
        pw (str): The password string to be checked.

    Returns:
        bool: True if the password is valid, False otherwise.

    Raises:
        None
    """
    # hashing the API_KEY that has been turned to bytes array
    # with randomly generated salt
    hash = bcrypt.hashpw(API_KEY.encode('utf-8'), bcrypt.gensalt())
    # checking password received as parameter with api key
    result = bcrypt.checkpw(pw.encode('utf-8'), hash)
    # returned values are boolean type
    return True if result else False

@app.route("/")
def root():
    """
    Route for the root URL ("/").

    Returns:
        str: A string with a greeting message.

    Raises:
        None
    """
    return "<h1>:)</h1>"

@app.route("/api/highscores")
def get_highscores():
    """
    Route for getting highscores via API.

    Returns:
        Response: A Flask Response object containing highscores data or an error message.

    Raises:
        None
    """
    pw = request.args.get("pw")
    if (check_api_key(pw) == False):
        return make_response(jsonify("You are unauthorized"), 401)
    highscores = jsonify(fetch_highscores())
    return make_response(highscores, 200)

@app.route('/api/highscores/<int:the_id>')
def get_players_highscore(the_id):
    """
    Route for getting a specific player's highscore via API.

    Args:
        the_id (int): The ID of the player.

    Returns:
        Response: A Flask Response object containing the player's highscore data or an error message.

    Raises:
        NotFound: If the player with the given ID is not found.
    """
    pw = request.args.get("pw")
    if (check_api_key(pw) == False):
        return make_response(jsonify("You are unauthorized"), 401)
    players_data = fetch_highscore(the_id)
    if players_data != None:
        # if player with id given as argument is found,
        # then a new dict object will be created,
        # which contains only id, name and overall highscore
        # from the data
        return make_response(jsonify(players_data), 200)
    else:
        abort(404)

# This method is used for posting a player's highscore in
# one of the four levels of the game
@app.route("/api/highscores", methods=['POST'])
def add_highscore():
    """
    Route for adding a player's highscore via API.

    Returns:
        Response: A Flask Response object indicating success or failure of the request.

    Raises:
        None
    """
    pw = request.args.get("pw")
    if (check_api_key(pw) == False):
        return make_response(jsonify("You are unauthorized"), 401)
    # the data sent via post request is e.g. {'name': 'dummy', 'overall_highscore': 100}
    sent_data = json.loads(request.data)
    if validate_name(sent_data['player_name']) != True:
        return make_response("Name must be be at least 3 characters and max 20 characters long", 400)
    save_highscore(sent_data['player_name'], sent_data['overall_highscore'])
    return make_response("", 201)

@app.route('/api/highscores/<int:the_id>', methods=['DELETE'])
def delete_highscore(the_id):
    """
    Deletes a highscore entry for a player with the given ID.

    Args:
        the_id (int): The ID of the player whose highscore is to be deleted.

    Returns:
        Response: A Flask response object with a 204 status code on successful deletion,
        or a response object with 404 status code if the player ID is not found.
    """
    pw = request.args.get("pw")
    if (check_api_key(pw) == False):
        return make_response(jsonify("You are unauthorized"), 401)
    # Before deletion, it has to be made sure that
    # the id of a player exists. Otherwise, a response
    # with status code 404 will be sent
    player_data = fetch_highscore(the_id)
    if player_data == None:
        return make_response("", 404)
    remove_highscore(the_id)
    return make_response("", 204)

@app.route('/highscores')
def show_highscores():
    """
    Renders the highscores page with optional sorting and limiting options.

    Returns:
        Response: A Flask response object containing the rendered highscores page
        with optional sorting and limiting options applied.
    """
    # The highscore page doesn't need password
    limit = 100
    sort = "desc"
    if request.args.get("sort") != None:
        sort = request.args.get("sort")
    if request.args.get("limit") != None:
        limit = int(request.args.get("limit"))
    highscores = fetch_highscores(limit, sort)
    return render_template("highscores.html", highscores=highscores)
    
if __name__ == "__main__":
    app.run(debug=True)