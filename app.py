from flask import Flask
from blueprints.input import input_bp
import tv

app = Flask(__name__)
tv_client = tv.connect()
app.register_blueprint(input_bp)

if __name__ == '__main__':
    app.run() # :5000
