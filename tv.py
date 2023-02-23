import pywebostv.connection as tv_conn
import pywebostv.discovery as tv_disc
import getmac, wakeonlan
import file_store

store = {}

def connect():
    store = file_store.load_store()
    try:
        tv_host = store['host']
        client = tv_conn.WebOSClient(tv_host, secure=False)
        client.connect()
    except:
        hosts = tv_disc.discover("urn:schemas-upnp-org:device:MediaRenderer:1",
                        keyword="LG", hosts=True, retries=3)
        if len(hosts) == 0:
            raise Exception("No TV found!")

        tv_host = hosts[0]
        client = tv_conn.WebOSClient(tv_host, secure=False)
        client.connect()
        store['host'] = tv_host

    for status in client.register(store):
        if status == tv_conn.WebOSClient.PROMPTED:
            print("Please accept the connect on the TV!")
        elif status == tv_conn.WebOSClient.REGISTERED:
            print("Registration successful!")

    mac = getmac.get_mac_address(ip=tv_host, network_request=True)
    store['mac'] = mac

    file_store.save_store(store)
    return client

def turn_on():
    wakeonlan.send_magic_packet(store['mac'])