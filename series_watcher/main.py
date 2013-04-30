import sys
from optparse import OptionParser

import pyinotify

from config import ConfigReader
from watcher import EventHandler

def main():
    usage = "Usage: %prog [options]"
    parser = OptionParser()
    parser.add_option("-c", "--config",
                      dest="config",
                      metavar="FILE",
                      help="Use config in FILE")
    (options, args) = parser.parse_args()

    if not options.config:
        parser.print_help()
        sys.exit(1)

    config = ConfigReader(options.config)

    wm = pyinotify.WatchManager()
    handler = EventHandler(config)
    mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE

    notifier = pyinotify.Notifier(wm, handler)

    for directory in config.watch_dirs:
        wdd = wm.add_watch(directory, mask, rec=True)

    # TODO: Slow down polling, every minute should be fine
    notifier.loop()

if __name__ == "__main__":
    main()
