Series-Watcher
==============

Subscribe to TV series to be informed when a new episode is released

How to use
----------

You can create/update manually the database using `python manage.py populate`

You can also use cron to update it every hour: edit `series-watcher-cron.sh`
to set the VIRTUALENV to your own virtualenv. Then, symlink this script into
/etc/cron.hourly/ : `ln -s series-watcher-cron.sh /etc/cron.hourly`.
