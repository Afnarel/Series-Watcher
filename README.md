Series-Watcher
==============

About
-----

Subscribe to TV series to be informed when a new episode is released.

This project has been initiated on February 8, 2014.

It is a Django web application, which includes a manage.py command to crawl
the http://stream-tv.me/ website.

Setup
-----

### How to start the web interface

  * Use pip to install the dependencies: `pip install -r requirements.txt`
  * Create the database: `python manage.py syncdb`
  * Use whatever server you want:
    * Using the Django development server (not suitable for production):
        `python manage.py runserver`
    * Using [gunicorn](http://gunicorn.org/) (you will need to serve static
      files separately):
        `gunicorn_django /path/to/series_watcher/settings.py`

### How to create and update the database

You can create/update manually the database using `python manage.py populate`

You can also use cron to update it every hour: edit `series-watcher-cron.sh`
to set the VIRTUALENV to your own virtualenv. Then, symlink this script into
/etc/cron.hourly/ : `ln -s series-watcher-cron.sh /etc/cron.hourly`.
If this does not work, run `crontab -e` (as root) and add the following at the
end:
~~~
SHELL=/bin/bash
@hourly /etc/cron.hourly/series-watcher-cron.sh
~~~


Make sure that the cron daemon is running.
On ArchLinux with systemctl (replace 'cronie' with 'dcron' if needed):
  * `systemctl is-active cronie` to check if it is running
  * `systemctl start cronie` to start it during this session
  * `systemctl enable cronie` to start it automatically at each boot
  * `systemctl is-enabled cronie` to check if it is enabled

On Ubuntu:
  * `sudo service cron start` to start cron (it is already started at boot)

Author
------

François CHAPUIS - [Afnarel](http://afnarel.com/)

License
-------

This project is distributed under the terms of the [Creative Commons
CC-BY-SA](http://creativecommons.org/licenses/by-sa/4.0/legalcode) license

Contributing
------------

This is more a tool developed selfishly for my own usage than an actual
community project.
Still, if you wish to contribute some code, you are welcome to submit pull requests.
