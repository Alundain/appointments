from flask import Flask 

app = Flask(__name__)

app.secret_key="secretKey" # se necesita para la sesión
