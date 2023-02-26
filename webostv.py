import pywebostv.connection as tv_conn
import pywebostv.discovery as tv_disc
import pywebostv.controls as tv_cntl
import getmac
import wakeonlan
import file_store

class TV:
    def __init__(self):
        self._store = file_store.load_store()

    def discover(self):
        hosts = tv_disc.discover("urn:schemas-upnp-org:device:MediaRenderer:1",
                                    keyword="LG", hosts=True, retries=3)
        if len(hosts) == 0:
            raise Exception("No TV found!")
        tv_host = list(hosts)[0]
        tv_mac = getmac.get_mac_address(ip=tv_host, network_request=True)
        self._store['host'] = tv_host
        self._store['mac'] = tv_mac
        file_store.save_store(self._store)

    def connect(self):
        if 'host' not in self._store:
            raise Exception("TV host not found!")
        
        store = self._store
        tv_host = store['host']
        self._webos_client = tv_conn.WebOSClient(tv_host, secure=False)
        self._webos_client.connect()

        for status in self._webos_client.register(store):
            if status == tv_conn.WebOSClient.PROMPTED:
                print("Please accept the connect on the TV!")
            elif status == tv_conn.WebOSClient.REGISTERED:
                print("Registration successful!")

        print(store)
        file_store.save_store(store)

        self.meida_ctl = tv_cntl.MediaControl(self._webos_client)
        self.tv_ctl = tv_cntl.TvControl(self._webos_client)
        self.system_ctl = tv_cntl.SystemControl(self._webos_client)
        self.application_ctl = tv_cntl.ApplicationControl(self._webos_client)
        self.input_ctl = tv_cntl.InputControl(self._webos_client)
        self.source_ctl = tv_cntl.SourceControl(self._webos_client)
        self.input_ctl.connect_input()

    def close(self):
        self._input_ctl.disconnect_input()
        self._webos_client.close()

    def turn_on(self):
        if 'host' not in self._store:
            raise Exception("TV host not found!")

        tv_host = self._store['host']
        mac = getmac.get_mac_address(ip=tv_host, network_request=True)
        print(f"Turning on TV at {mac}...")
        wakeonlan.send_magic_packet(mac)

    def popup(self, msg):
        self.tv_ctl.notify(msg)
