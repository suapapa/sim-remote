import tv
from flask import Flask, current_app
from handler import tv_bp, tv_key_bp, tv_src_bp, tv_audio_bp, tv_app_bp

app = Flask(__name__)

with app.app_context():
    current_app.tv_client, current_app.tv_mac = tv.connect()

app.register_blueprint(tv_bp)
app.register_blueprint(tv_key_bp)
app.register_blueprint(tv_src_bp)
app.register_blueprint(tv_audio_bp)
app.register_blueprint(tv_app_bp)

if __name__ == '__main__':
    app.run()  # :5000
