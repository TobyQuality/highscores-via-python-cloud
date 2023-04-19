from flask import *
from json import *
from dotenv import load_dotenv
import os
import bcrypt
from utils.repository import *

app = Flask(__name__)

# loading the .env file containing the api key for the app
load_dotenv()
# accessing the api key
API_KEY = os.environ.get('API_KEY')

# this method is used to check the validity of the password
# sent with requests to the backend
def check_api_key(pw):
    if type(pw) != str:
        raise Exception("Give password as string object")
    # hashing the API_KEY that has been turned to bytes array
    # with randomly generated salt
    hash = bcrypt.hashpw(API_KEY.encode('utf-8'), bcrypt.gensalt())
    # checking password received as parameter with api key
    result = bcrypt.checkpw(pw.encode('utf-8'), hash)
    # returned values are boolean type
    return True if result else False

@app.route("/")
def root():
    return "<h1>hello</h1>"

@app.route("/api/highscores")
def get_highscores():
    pw = request.args.get("pw")
    if (check_api_key(pw) == False):
        return make_response(jsonify("You are unauthorized"), 401)
    highscores = jsonify(fetch_highscores())
    return make_response(highscores, 200)

@app.route('/api/highscores/<int:the_id>')
def get_players_highscore(the_id):
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
    pw = request.args.get("pw")
    if (check_api_key(pw) == False):
        return make_response(jsonify("You are unauthorized"), 401)
    # the data sent via post request is e.g. {'name': 'dummy', 'overall_highscore': 100}
    sent_data = json.loads(request.data)
    save_highscore(sent_data['name'], sent_data['overall_highscore'])
    return make_response("", 201)

@app.route('/api/highscores/<int:the_id>', methods=['DELETE'])
def delete_highscore(the_id):
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
    # The highscore page doesn't need password
    limit = 100
    sort = "none"
    if request.args.get("sort") != None:
        sort = request.args.get("sort")
    if request.args.get("limit") != None:
        limit = int(request.args.get("limit"))
    highscores = fetch_highscores(limit, sort)
    return render_template("highscores.html", highscores=highscores)
    
if __name__ == "__main__":
    app.run(debug=True)