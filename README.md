# Highscores for Risky Cargo game

This project has been done to implement the saving and storing highscores for the game Risky Cargo. The game has been produced as part of IT studies in Tampere University of Applied Sciences.

# Author

Topias Laatu

# Screenshots

![Alt text](/risky_cargo_highscores.png "The website containing the player highscores")

# Tech/framework used

The highscore functions are implemented in Python programming language and the server is running on Flask environment. Gunicorn is used for deploying the app in cloud environment in Render.com. Bcrypt is used for giving a password protection for the http/https requests.

# Installation and running

Provide step by step series of examples and explanations about how to get a development env running. Example:

To run this app:

1. Go to a folder where you want to install the app.

2. Open command console and write down the path to the folder.

3. Use this command: 'git clone https://github.com/TobyQuality/highscores-via-python-cloud.git'

4. After the file has been downloaded completely, go to the folder 'highscores-via-python-cloud' (the root directory) with your command console

5. Type the command 'python index.py' (provided you have python installed)

6. Create .env file to your root directory. Inside key value pair in this fashion: API_KEY: "somepassword". Note that API_KEY is without quotation marks and the value, in this case 'somepassword' HAS TO HAVE quotation marks. You can give value you like. It works as the password for the http/https requests.

7. You are good to go! In folder 'test' is a file called 'test.http' where you can specify the requests you make to the server running in your localhost. Remember always to use password attribute like this:  get http://127.0.0.1:5000/api/highscores?pw=secret 

To save your highscores to the cloud environment of the game, you need to wait until the game is finished and downloadable in Google Play store.

# API implementation

API is deployed to cloud and can be accessed using following url:

- https://risky-cargo-highscores.onrender.com/api

# Screencast

[![Screencast](https://youtu.be/tui9hdY9XlI)