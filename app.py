import webostv
import sys
from flask import Flask, current_app
from handler import tv_bp, tv_key_bp, tv_src_bp, tv_audio_bp, tv_app_bp

app = Flask(__name__)

with app.app_context():
    current_app.tv = webostv.TV()
    # current_app.tv_client, current_app.tv_mac = tv.connect()

app.register_blueprint(tv_bp)
app.register_blueprint(tv_key_bp)
app.register_blueprint(tv_src_bp)
app.register_blueprint(tv_audio_bp)
app.register_blueprint(tv_app_bp)


@app.errorhandler(Exception)
def handle_exception(e):
    print(f"Caught an exception: {e}")
    sys.exit(-1)


if __name__ == '__main__':
    try:
        app.run()  # :5000
    except Exception as e:
        print(f"Caught an exception on main: {e}")
        sys.exit(-1)
