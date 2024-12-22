import pywebostv.connection as tv_conn
import pywebostv.discovery as tv_disc
import pywebostv.controls as tv_cntl
import getmac
import wakeonlan
import file_store


class TV:
    def __init__(self):
        self._connected = False
        self._discovered = False
        self._store = file_store.load_store()

    def _discover(self):
        if 'host' in self._store:
            self._discovered = True
            return

        if self._discovered:
            return

        print('Discovering TV...')
        hosts = tv_disc.discover("urn:schemas-upnp-org:device:MediaRenderer:1",
                                 keyword="LG", hosts=True, retries=3)
        if len(hosts) == 0:
            raise Exception("No TV found!")
        tv_host = list(hosts)[0]
        self._store['host'] = tv_host
        tv_mac = getmac.get_mac_address(ip=tv_host, network_request=True)
        self._store['mac'] = tv_mac
        file_store.save_store(self._store)
        print(f"host: {tv_host}, mac: {tv_mac}")

        self._discovered = True

    def connect(self):
        self._discover()

        if self._connected:
            return

        print('Connecting to TV...')
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

        self._meida_ctl = tv_cntl.MediaControl(self._webos_client)
        self._tv_ctl = tv_cntl.TvControl(self._webos_client)
        self._system_ctl = tv_cntl.SystemControl(self._webos_client)
        self._application_ctl = tv_cntl.ApplicationControl(self._webos_client)
        self._input_ctl = tv_cntl.InputControl(self._webos_client)
        self._source_ctl = tv_cntl.SourceControl(self._webos_client)
        self._input_ctl.connect_input()

        self._connected = True

    def disconnect(self):
        if self._connected:
            self._webos_client.disconnect()
            self._connected = False

    def get_media_ctl(self):
        self.connect()
        return self._meida_ctl

    def get_tv_ctl(self):
        self.connect()
        return self._tv_ctl

    def get_system_ctl(self):
        self.connect()
        return self._system_ctl

    def get_application_ctl(self):
        self.connect()
        return self._application_ctl

    def get_input_ctl(self):
        self.connect()
        return self._input_ctl

    def get_source_ctl(self):
        self.connect()
        return self._source_ctl

    def popup(self, msg):
        self.connect()
        self._system_ctl.notify(msg)

    def close(self):
        self._input_ctl.disconnect_input()
        self._webos_client.close()

    def turn_on(self):
        if 'mac' not in self._store:
            raise Exception("TV host not found!")

        tv_mac = self._store['mac']
        print(f"Turning on TV at {tv_mac}...")
        wakeonlan.send_magic_packet(tv_mac)
        self.connect()
