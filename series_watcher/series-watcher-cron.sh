#!/bin/sh

VIRTUALENV=/home/afnarel/.virtualenvs/series-watcher

SCRIPT=$(readlink -f $0)
SCRIPT_PATH=$(dirname $SCRIPT)
cd $SCRIPT_PATH

. $VIRTUALENV/bin/activate

python -u manage.py populate >> series-watcher.log
