import json
import os

def open_file(char):
    """
    Open highscores.json file with a given character, which defines the crud-operation (read, write etc.).
    Args:
        char (str): Character representing the crud-operation to be performed on the file ("r" for read, "w" for write, etc.)
    Returns:
        file: File object representing the opened file.
    """
    # in order to reach highscores.json file from folder that is up by one step
    # in the directory, we first have to locate the current folder location of repository.py
    # with os.path.dirname(__file__)
    current_folder = os.path.dirname(__file__)
    # with os.path.join we can find highscores.py with current folder as one argument,
    # ".." as second, which indicates going up the directory by one step,
    # then the file name of highscores as the last argument.
    # Now we have established the relative path to highscores.json
    highscores_file_path = os.path.join(current_folder, '..', 'highscores.json')
    f = open(highscores_file_path, char)
    return f

# This method is used for reading the database, returning
# the content of the file in a string form
def read_database():
    """
    Read the content of the highscores.json file and return it as a string.
    Returns:
        str: Content of the highscores.json file.
    """
    f = open_file("r")
    content = f.read()
    f.close()
    return content

def fetch_highscores(limit = 100, sort="none"):
    """
    Fetch the highscores from the highscores.json file.
    Args:
        limit (int, optional): Maximum number of highscores to fetch. Defaults to 100.
        sort (str, optional): Sorting order for highscores ("asc", "desc", or "none"). Defaults to "none".
    Returns:
        list: List of dictionaries containing player names and highscores.
    Raises:
        Exception: If limit is not an integer.
    """
    if type(limit) != int:
        raise Exception("give int")
    # 100 is the default limit
    if limit > 100 or limit <= 0:
        limit = 100
    # if sort is not "none", "asc", or "desc", then it will be "none"
    # by default
    if sort != "none":
        if sort != "asc":
            if sort != "desc":
                sort= "none"
    #print(sort)
    highscores = []
    # the loads function converts json to a python object,
    # in this case to a list
    content = json.loads(read_database())
    # this variable determines whether the max range of list objects
    # is the limit or length of the list, dependent on whether the limit
    # is greater than the length of the list or not
    max_range = len(content) if limit > len(content) else limit
    # we want to return a list of dicts, 
    # with each dict object containing only name and highscore
    if sort == "none":
        for i in range(0, max_range):
            player_and_highscore = {}
            player_and_highscore['player'] = content[i]['name']
            player_and_highscore['highscore'] = content[i]['highscore']
            highscores.append(player_and_highscore)
        return highscores
    if sort == "asc":
        sorted_highscores = sorted(content, key=lambda d: d['highscore'])
        for i in range(0, max_range):
            player_and_highscore = {}
            player_and_highscore['player'] = sorted_highscores[i]['name']
            player_and_highscore['highscore'] = sorted_highscores[i]['highscore']
            highscores.append(player_and_highscore)
        return highscores
    if sort == "desc":
        sorted_highscores = sorted(content, key=lambda d: d['highscore'], reverse=True)
        for i in range(0, max_range):
            player_and_highscore = {}
            player_and_highscore['player'] = sorted_highscores[i]['name']
            player_and_highscore['highscore'] = sorted_highscores[i]['highscore']
            highscores.append(player_and_highscore)
        return highscores

def fetch_player_data(id):
    """
    Fetch the highscores from the highscores.json file.
    Args:
        limit (int, optional): Maximum number of highscores to fetch. Defaults to 100.
        sort (str, optional): Sorting order for highscores ("asc", "desc", or "none"). Defaults to "none".
    Returns:
        list: List of dictionaries containing player names and highscores.
    Raises:
        Exception: If limit is not an integer.
    """
    if type(id) != int:
        raise Exception("Give integer type of id")
    # if player data remains as none
    # it will be dealt with in index.py
    # with an appropriate response
    player_data = None
    content = json.loads(read_database())
    for data in content:
        if data['id'] == id:
            player_data = data
            break
    return player_data

def save_highscore(name, level, level_highscore):
    """
    This function saves the highscore for a specific player and level in the database.
    
    Args:
        name (str): The name of the player.
        level (int): The level number for which the highscore is being updated.
        level_highscore (int): The highscore to be saved for the given level.
        
    Returns:
        None
    """
    content = json.loads(read_database())
    for data in content:
        # the highscore of the player given as argument will be modified.
        # The variable 'content' is a list containing dicts. It has a property called
        # 'name' which is needed to find the highscores tied to the player's name,
        # contained in a list named 'level_highscores'
        if data['name'] == name:
            # once the player is found, the index of the list 'level_highscores' 
            # is determined by level number minus one due to list index starting from 0.
            data['level_highscores'][level - 1] = level_highscore
            # after level highscore has been updated,
            # the overall highscore of all levels, contained in the property
            # 'highscore', has to be updated.
            highscore = 0
            for i in range(len(data['level_highscores'])):
                highscore += data['level_highscores'][i]
            data['highscore'] = highscore
            break
    # Once out of the for loop, overwriting the json file can proceed
    # The list data inside variable 'content' has to be stringified before
    # writing its content to highscores.json file.
    f = open_file("w")
    f.write(json.dumps(content))
    f.close()

def delete_score_by_id(id):
    """
    This function deletes the highscore and level highscores for a specific player by ID in the database.
    
    Args:
        id (int): The ID of the player whose highscore and level highscores are to be deleted.
        
    Returns:
        None
    """
    if type(id) != int:
        raise Exception('Give integer type of id')
    player_data = fetch_player_data(id)
    player_data['highscore'] = 0
    for i in range(len(player_data['level_highscores'])):
        player_data['level_highscores'][i] = 0
    player_data_list = json.loads(read_database())
    for i in range(len(player_data_list)):
        if player_data_list[i]['id'] == id:
            player_data_list[i] = player_data
            break
    f = open_file("w")
    f.write(json.dumps(player_data_list))
    f.close()

def add_new_player(dict_object):
    """
    This function adds a new player to the database with the given player data as a dictionary.
    
    Args:
        dict_object (dict): A dictionary containing the player data to be added to the database.
        
    Returns:
        None
    """
    if type(dict_object) != dict:
        raise Exception("Give a dict object as parameter")
    content = json.loads(read_database())
    content.append(dict_object)
    f = open_file("w")
    json.dump(content, f)
    f.close()

def main():
    print("main function is used for testing the module's methods")
    # print(read_database())
    # print(fetch_player_data(1))
    # delete_score_by_id(1)
    print(fetch_highscores(sort="desc"))

if __name__ == "__main__":
    main()