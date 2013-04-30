import yaml

# config will parse as:
#{
#        'watch_dirs': ['/tmp', '/tmp2', ],
#        'sync_dirs': {
#            '/sync/a': [
#                'Series Name',
#                ]
#        }
#}

class ConfigReader(object):
    def __init__(self, config_file):
        self.config = {}
        self._read(config_file)
        self._validate()

    def _read(self, filename):
        try:
            with open(filename, 'rU') as f:
                self.config = yaml.load(f.read())
        except:
            msg = "Could not read config file {0}".format(filename)
            raise configError(msg)

    def _validate(self):
        if not 'watch_dirs' in self.config:
            raise configError("No 'watch_dirs' specified in config")
        if not 'sync_dirs' in self.config:
            raise configError("No 'sync_dirs' specified in config")

    @property
    def watch_dirs(self):
        return self.config.get('watch_dirs')

    @property
    def sync_dirs(self):
        return self.config.get('sync_dirs')

class configError(Exception):
    pass
