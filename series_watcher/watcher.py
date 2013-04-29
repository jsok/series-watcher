import os
import sys

from flexget.utils.titles import SeriesParser
import pyinotify
import yaml

# Format should match:
# SETTINGS =
#{
#        'watch_dirs': ['/tmp', '/tmp2', ],
#        'sync_dirs': {
#            '/sync/a': [
#                'Series Name',
#                ]
#        }
#}
SETTINGS = {}

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname

        for sync_dir, series in SETTINGS['sync_dirs'].iteritems():
            for series_name in series:
                series = SeriesParser(series_name)
                filename = os.path.basename(event.pathname)
                series.parse(filename)

                if series.valid:
                    print "Match: ", series
                    # TODO: Trigger callback

    def process_IN_DELETE(self, event):
        print "Deleting:", event.pathname

def read_settings(filename):
    try:
        with open(filename, 'rU') as f:
            settings = yaml.load(f.read())
    except:
        return None
    return settings

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s settings.yml" % sys.argv[0]
        sys.exit(1)

    SETTINGS = read_settings(sys.argv[1])
    if not SETTINGS:
        print "Invalid settings file"
        sys.exit(1)

    wm = pyinotify.WatchManager()
    handler = EventHandler()
    mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE

    notifier = pyinotify.Notifier(wm, handler)

    for directory in SETTINGS['watch_dirs']:
        wdd = wm.add_watch(directory, mask, rec=True)

    # TODO: Slow down polling, every minute should be fine
    notifier.loop()

