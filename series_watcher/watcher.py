import os

from flexget.utils.titles import SeriesParser
import pyinotify


class EventHandler(pyinotify.ProcessEvent):
    def __init__(self, config):
        self.config = config

    def process_IN_CREATE(self, event):
        print "Creating:", event.pathname

        for sync_dir, series in self.config.sync_dirs.iteritems():
            for series_name in series:
                series = SeriesParser(series_name)
                filename = os.path.basename(event.pathname)
                series.parse(filename)

                if series.valid:
                    print "Match: ", series
                    # TODO: Trigger callback

    def process_IN_DELETE(self, event):
        print "Deleting:", event.pathname

