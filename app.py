import pywebostv.connection as tv_conn
# import pywebostv.controls as tv_cntl
# import pywebostv.discovery as tv_disc

from flask import Flask
from blueprints.input import input_bp

app = Flask(__name__)

def connect_tv():
    store = {'client_key': '5c930e4b77788374d70f42ab7d6f5685'}
    # hosts = tv_disc.discover("urn:schemas-upnp-org:device:MediaRenderer:1",
    #                    keyword="LG", hosts=True, retries=3)
    # print(hosts)
    # client = tv_conn.WebOSClient.discover()[0] # Use discover(secure=True) for newer models.
    client = tv_conn.WebOSClient('192.168.219.181', secure=False)
    client.connect()
    for status in client.register(store):
        if status == tv_conn.WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")
        elif status == tv_conn.WebOSClient.REGISTERED:
            print("Registration successful!")
    return client

# ---

tv_client = connect_tv()

app.register_blueprint(input_bp)

if __name__ == '__main__':
    app.run() # :5000
