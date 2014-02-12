Series-Watcher
==============

Subscribe to TV series to be informed when a new episode is released

How to use
----------

You can create/update manually the database using `python manage.py populate`

You can also use cron to update it every hour: edit `series-watcher-cron.sh`
to set the VIRTUALENV to your own virtualenv. Then, symlink this script into
/etc/cron.hourly/ : `ln -s series-watcher-cron.sh /etc/cron.hourly`.

Make sure that the cron daemon is running.

On ArchLinux with systemctl (replace 'cronie' with 'dcron' if needed):
  * `systemctl is-active cronie` to check if it is running
  * `systemctl start cronie` to start it during this session
  * `systemctl enable cronie` to start it automatically at each boot
  * `systemctl is-enabled cronie` to check if it is enabled
