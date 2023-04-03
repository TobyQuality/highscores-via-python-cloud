from flask import *
from json import *
from utils.repository import *

app = Flask(__name__)

@app.route("/")
def root():
    return "<h1>hello</h1>"

@app.route("/api/highscores")
def get_highscores():
    highscores = jsonify(fetch_highscores())
    return make_response(highscores, 200)

@app.route('/api/highscores/<int:the_id>')
def get_players_highscore(the_id):
    players_data = fetch_player_data(the_id)
    if players_data != None:
        # if player with id given as argument is found,
        # then a new dict object will be created,
        # which contains only id, name and overall highscore
        # from the data
        return make_response(jsonify({"name": players_data['name'], 
                                      "highscore": players_data['highscore']}), 200)
    else:
        abort(404)

# This method is used for posting a player's highscore in
# one of the four levels of the game
@app.route("/api/highscores", methods=['POST'])
def add_highscore():
    # the data sent via post request is e.g. {'id': 1, 'name': 'dummy', 'level': 1, 'score': 100}
    sent_data = json.loads(request.data)
    # first we have to make sure that the score that's being sent
    # is greater than the current highscore of the level. First the player data is fetched
    players_data = fetch_player_data(sent_data['id'])
    # the player's new level score has to be measured against the current level highscore
    level_highscore = players_data['level_highscores'][sent_data['level'] - 1][str(sent_data['level'])]
    # if the new score is greater, then it will be saved in the json file
    if sent_data['score'] > level_highscore:
        save_highscore(sent_data['name'], sent_data['level'], sent_data['score'])
        return make_response("", 201)
    else:
        # even if the score didn't update, a status code 200 is sent to
        # inform that the sent information was handled
        return make_response("", 200)

# the delete method is used for deleting all scores,
# including level highscores and the overall highscore of all levels
@app.route('/api/highscores/<int:the_id>', methods=['DELETE'])
def delete_customer(the_id):
    # Before deletion, it has to be made sure that
    # the id of a player exists. Otherwise, a response
    # with status code 404 will be sent
    player_data = fetch_player_data(the_id)
    if player_data == None:
        return make_response("", 404)
    else:
        delete_score_by_id(the_id)
        return make_response("", 204)
    
@app.route('/api/new_player', methods=['POST'])
def create_new_account():
    # the request should contain json object with two properties
    # "name" and "email" and their values
    sent_data = json.loads(request.data)
    # first we need to make sure that the username is unique
    players_list = json.loads(read_database())
    for player_data in players_list:
        if player_data['name'] == sent_data['name']:
            return make_response("", 409)
    # if username is unique, new player data can be constructed
    id = len(players_list) + 1
    new_player = {"id": id, "name": sent_data['name'], "email": sent_data['email'], "level_highscores": [0, 0, 0, 0], "highscore": 0}
    add_new_player(new_player)
    # the new player info is sent back to the game
    return make_response(jsonify(new_player), 200)

@app.route('/highscores')
def show_highscores():
    highscores = fetch_highscores()
    return render_template("highscores.html", highscores=highscores)

if __name__ == "__main__":
    app.run(debug=True)