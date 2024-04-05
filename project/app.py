from application import create_app
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == "__main__":
    PORT = os.environ.get('PORT_DEV', 5000)
    DEBUG = os.environ.get('FLASK_DEBUG', 'True') == 'True'
    HOST = os.environ.get('HOST_DEV', '127.0.0.1')
    app = create_app()

    app.run(host=HOST, port=int(PORT), debug=DEBUG)
