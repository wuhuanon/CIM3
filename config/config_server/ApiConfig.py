
import configparser
import os

current_path = os.getcwd()
PATH = os.path.join(current_path, "config.ini")
# PATH = "../config.ini"
class ConfigFile(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, path=PATH):
        self.path = path
        try:
            self.configFile = configparser.RawConfigParser(allow_no_value=True)
            self.configFile.read(self.path)
        except Exception as e:
            import traceback
            traceback.print_exc()

    def get(self, session, name, default=None):
        try:
            if self.configFile.has_section(session):

                return self.configFile.get(session, name)
            else:
                return default

        except Exception as e:
            if default:
                return default
            else:
                if default is None:
                    import traceback
                    traceback.print_exc()
                else:
                    return ''
        finally:
            pass

    def set(self, session, name, value):
        try:
            if not self.configFile.has_section(session):
                self.configFile.add_section(session)

            self.configFile.set(session, name, value)

        except Exception as e:
            import traceback
            traceback.print_exc()
        finally:
            pass

    def save(self):
        with open(self.path, 'wb') as configfile:
            self.configFile.write(configfile)

config = ConfigFile()
if __name__ == "__main__":
    # config = ConfigFile()
    print(config.get("IpAddress", 'port'))
    print(config.get("IpAddress", 'address'))