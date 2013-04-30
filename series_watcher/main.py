import sys
from optparse import OptionParser

import pyinotify

from config import ConfigReader
from watcher import EventHandler

usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-c", "--config",
                  metavar="FILE", help="write output to FILE")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage: %s config.yml" % sys.argv[0]
        sys.exit(1)

    config = ConfigReader(sys.argv[1])

    wm = pyinotify.WatchManager()
    handler = EventHandler(config)
    mask = pyinotify.IN_CREATE | pyinotify.IN_DELETE

    notifier = pyinotify.Notifier(wm, handler)

    for directory in config.watch_dirs:
        wdd = wm.add_watch(directory, mask, rec=True)

    # TODO: Slow down polling, every minute should be fine
    notifier.loop()

