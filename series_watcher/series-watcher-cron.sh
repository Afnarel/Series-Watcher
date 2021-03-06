#!/bin/sh

# VIRTUALENV=/home/angel/.virtualenvs/series-watcher

SCRIPT=$(readlink -f $0)
SCRIPT_PATH=$(dirname $SCRIPT)
cd $SCRIPT_PATH

# . $VIRTUALENV/bin/activate

# python -u manage.py populate >> series-watcher.log 2>&1
python2 -u manage.py populate --settings=series_watcher.settings.production >> series-watcher.log 2>&1
