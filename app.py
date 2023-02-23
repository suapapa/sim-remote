import tv
from flask import Flask
from handler import tv_bp, tv_key_bp, tv_src_bp, tv_audio_bp

app = Flask(__name__)
tv_client = tv.connect()
app.register_blueprint(tv_bp)
app.register_blueprint(tv_key_bp)
app.register_blueprint(tv_src_bp)
app.register_blueprint(tv_audio_bp)

if __name__ == '__main__':
    app.run() # :5000
