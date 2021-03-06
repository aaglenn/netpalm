import napalm

class naplm:

    def __init__(self, **kwargs):
        self.connection_args = kwargs.get('connection_args', False)
        #convert the netmiko naming format to the native napalm format
        driver_lookup = {"arista_eos":"eos","juniper":"junos","cisco_xr":"iosxr", "nxos":"nxos", "cisco_nxos_ssh":"nxos_ssh", "cisco_ios":"ios"}
        self.driver = driver_lookup[self.connection_args.get('device_type', False)]
        self.connection_args["hostname"] = self.connection_args.pop("host")
        del self.connection_args["device_type"]

    def connect(self):
        try:
            driver = napalm.get_network_driver(self.driver)
            napalmses = driver(**self.connection_args)
            return napalmses
        except Exception as e:
            return str(e)

    def sendcommand(self, session=False, command=False):
        try:
            session.open()
            response = session.cli(command)
            result = {}
            for command in response:
                result[command] = response[command].split('\n')
            return result
        except Exception as e:
            return str(e)

    def config(self, session=False, command=False):
        try:
            if type(command) == list:
                napalmconfig = ""
                for comm in command:
                    napalmconfig += comm + "\n"
            else:
                napalmconfig = command
            session.open()
            session.load_merge_candidate(config=napalmconfig)
            diff = session.compare_config()
            response = session.commit_config()
            result = {}
            result["changes"] = diff.split('\n')
            return result
        except Exception as e:
            return str(e)

    def logout(self, session):
        try:
            response = session.close()
            return response
        except Exception as e:
            return str(e)
