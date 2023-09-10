from app import app
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    app.run(port=os.getenv('port'),host='192.168.1.42' ,debug=True)