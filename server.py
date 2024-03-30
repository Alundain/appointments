from flask_app import app 

# importacion controlladores 
from flask_app.controllers import users
from flask_app.controllers import appointments


if __name__ == "__main__":
    app.run(debug=True, port=8080)