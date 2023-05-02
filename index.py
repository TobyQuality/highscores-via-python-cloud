from flask import *
from json import *
from dotenv import load_dotenv
import os
import bcrypt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import tempfile

app = Flask(__name__)

# loading the .env file
load_dotenv()

#!!!!
# Most of the code concerning Firebase
# is based on the code of Jussi Pohjolainen (pohjus at Github)
#!!!!

# read firebase env
# create new variable to render.com named firebase whose
# content is a json file from firebase
json_str = os.environ.get('firebase')

# save the content of the env to a temp file
with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
    f.write(str(json_str))
    temp_path = f.name

# read json file
cred = credentials.Certificate(temp_path)

# create env to render.com named bucket, whose content is
# e.g.: mydatabase-38cf0.appspot.com
firebase_admin.initialize_app(cred, {
    'storageBucket': os.environ.get('bucket')
})
bucket = storage.bucket()

# accessing the api key used as password with requests to the server
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

def fetch_highscores_from_firebase():
    blob = bucket.blob('highscores.json')
    content = blob.download_as_string().decode('utf-8')
    highscores = json.loads(content)
    return highscores

def fetch_a_highscore_based_on_id(id, highscores):
    highscore = None
    for data in highscores:
        if data['id'] == id:
            highscore = data
            break
    return highscore

def upload_to_firebase(content, content_type="application/json"):
    blob = bucket.blob('highscores.json')
    blob.upload_from_string(content, content_type)

def validate_name(name):
    """
    Validates a name string.

    Args:
        name (str): The name string to be validated.

    Returns:
        bool: True if the name is valid, False otherwise.

    Raises:
        None

    Example:
        >>> validate_name("John Doe")
        True
        >>> validate_name("A")
        False
        >>> validate_name("This is a very long name")
        False
    """
    if len(name) > 20 or 2 > len(name):
        return False
    return True

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
    highscores = fetch_highscores_from_firebase()
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
    highscore = fetch_a_highscore_based_on_id(the_id, fetch_highscores_from_firebase())
    if highscore != None:
        return make_response(jsonify(highscore), 200)
    else:
        return make_response(jsonify({'message': 'Player not found.'}), 404)

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
    # the data sent via post request is e.g. {'player_name': 'dummy', 'overall_highscore': 100}
    received_data = json.loads(request.data)
    if validate_name(received_data['player_name']) != True:
        return make_response("Name must be be at least 3 characters and max 20 characters long", 400)
    highscores = fetch_highscores_from_firebase()
    # create id for highscore
    # new highscore id is initially array length + 1
    id = len(highscores) + 1
    # check if there is a duplicate id
    duplicate = True
    while duplicate:
        player_data = fetch_a_highscore_based_on_id(id, highscores)
        if player_data != None:
            id = id + 1
        else:
            duplicate = False
    new_highscore = {"id": id, "name": received_data['player_name'], "highscore": received_data['overall_highscore']}
    # append new highscore to highscores list and jsonify it
    highscores.append(new_highscore)
    highscores_json = json.dumps(highscores)
    # Upload the updated highscores file to Firebase Storage
    upload_to_firebase(content = highscores_json)
    return make_response(jsonify({'message': 'Highscore added successfully!'}), 201)

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
    highscores = fetch_highscores_from_firebase()
    player_data = fetch_a_highscore_based_on_id(the_id, highscores)
    if player_data == None:
        return make_response("", 404)
    for i in range(len(highscores)):
        if highscores[i]['id'] == the_id:
            highscores.pop(i)
            break
    highscores_json = json.dumps(highscores)
    # Upload the updated highscores file to Firebase Storage
    upload_to_firebase(content = highscores_json)
    return make_response("", 204)

@app.route('/highscores')
def show_highscores():
    """
    Renders the highscores page with optional sorting and limiting options.

    Returns:
        Response: A Flask response object containing the rendered highscores page
        with optional sorting and limiting options applied.
    """
    # check, if there is a sort attribute with request
    limit = 0
    sort = ""
    if request.args.get("sort") != None:
        sort = request.args.get("sort")
    # check, if there is a limit attribute with request
    if request.args.get("limit") != None:
        limit = int(request.args.get("limit"))
    #  check, if limit is within 1-100 range, else defaults to 100
    if limit > 100 or limit <= 0:
        limit = 100
    # if sort is not "none", "asc", or "desc", then it will be "desc"
    # by default, meaning the highscores list will be shown in descending order,
    # meaning highest score is first, and so on.
    if sort != "desc":
        if sort != "asc":
            if sort != "none":
                sort = "desc"
    # download highscores from firebase
    highscores = fetch_highscores_from_firebase()
    # this variable determines whether the max range of list objects
    # is the limit or length of the list, dependent on whether the limit
    # is greater than the length of the list or not
    max_range = len(highscores) if limit > len(highscores) else limit
    # a list containing dicts will be returned
    returned_highscores = []
    if sort == "none":
        for i in range(0, max_range):
            returned_highscores.append(highscores[i])
    if sort == "asc":
        sorted_highscores = sorted(highscores, key=lambda d: d['highscore'])
        for i in range(0, max_range):
            returned_highscores.append(sorted_highscores[i])
        return highscores
    if sort == "desc":
        sorted_highscores = sorted(highscores, key=lambda d: d['highscore'], reverse=True)
        for i in range(0, max_range):
            returned_highscores.append(sorted_highscores[i])
    return render_template("highscores.html", highscores=returned_highscores)
    
if __name__ == "__main__":
    app.run(debug=True)