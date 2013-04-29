import sys

import pyinotify
import yaml

class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname

    def process_IN_DELETE(self, event):
        print "Deleting:", event.pathname

def read_settings(filename):
    with open(filename, 'rU') as f:
        settings = yaml.load(f.read())

    return settings['dirs'].keys()

if __name__ == "__main__":
    wm = pyinotify.WatchManager()
    handler = EventHandler()
    mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE

    notifier = pyinotify.Notifier(wm, handler)

    watch_dirs = read_settings(sys.argv[1])
    for directory in watch_dirs:
        wdd = wm.add_watch(directory, mask, rec=True)

    notifier.loop()

