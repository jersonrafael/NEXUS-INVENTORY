from flask import Flask
from bson.json_util import dumps
from flask_cors import CORS


#APP
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
# @cross_origin(origins=['http://localhost:3000'])
def response():
    message = 'Hello World'
    return message

@app.route('/home',methods=['GET'])
def home():
    # message = 'HOME'
    json_response = dumps({'message':'Hola'})
    return json_response    
# RUN APP
if __name__ == "__main__":
    app.run(debug=True)