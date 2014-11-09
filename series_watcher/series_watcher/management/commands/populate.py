# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from series_watcher.models import Series, Season, Episode
from django.core.exceptions import ObjectDoesNotExist

from bs4 import BeautifulSoup
import re
from time import strftime
from socket import error as socket_error
from httplib import BadStatusLine
from traceback import format_exc
from django.conf import settings
import urllib2


class Command(BaseCommand):

    def log(self, text=""):
        if text:
            t = strftime('%Y-%m-%d %X ')
            self.stdout.write(t + text + "\n")
        else:
            self.stdout.write("\n")

    def getParsedData(self, url):
        try:
            request = urllib2.Request(url)
            opener = urllib2.build_opener()
            request.add_header('User-Agent', "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")
            page = opener.open(request)  # .read()
            # page = urlopen(url)
        except (urllib2.URLError, socket_error, BadStatusLine) as e:
            s = "Error for URL {0}:\n\t{1}: {2}".format(
                url, e.errno, e.strerror)
            self.log(s)
            raise CommandError('URL %s does not respond' % url)
        except:
            self.log(format_exc())
        return BeautifulSoup(page.read())

    def createOrUpdateSeries(self):
        html = self.getParsedData(settings.STREAMTV_URL)
        regex = "%s/watch" % settings.BASE_REGEX
        series = html.findAll('a', href=re.compile(regex))

        #self.getInfosAboutSeries(
        #    "%s/watch-misfits-online/" % settings.BASE_REGEX)
        for s in series:
            if not s.text.startswith('Watch '):
                try:
                    self.getInfosAboutSeries(s.get('href'))
                except:
                    continue

    def getInfosAboutSeries(self, url, full_update=False):
        """
            If something changed on the website,
            let's update the database (and log
            the change)
            The way to identify a series is its URL
        """

        # Parse the data about the series
        html = self.getParsedData(url)

        # Get the series name from URL (url_keyword)
        regex = "%s/watch-(.*)-online.*" % settings.BASE_REGEX
        p = re.compile(regex)
        m = p.match(url)
        try:
            url_keyword = m.group(1)
        except AttributeError:
            # self.log('Could not get series name from url %s' % url)
            regex2 = "%s/watch-(.*)/" % settings.BASE_REGEX
            p = re.compile(regex2)
            m = p.match(url)
            try:
                url_keyword = m.group(1)
            except AttributeError:
                self.log('Could not get series name from url %s' % url)

        # Test if the series exists. If it doesn't, create
        # one with just a URL and a URL keyword
        try:
            _series = Series.objects.get(url_keyword=url_keyword)
            is_new = False
        except ObjectDoesNotExist:
            _series = Series.objects.create(url=url, url_keyword=url_keyword)
            is_new = True
        # _series, is_new = Series.objects.get_or_create(url=url)

        # If the series has just been created (or if we want to
        # perform a complete update), we need to fill in the
        # basic data about it
        name = ''
        if is_new or full_update:
            self.log("Series '" + url + "' has been added to the database")

            # Name
            title = html.find('div', class_='title').h2.text
            try:
                p = re.compile('Watch (.*) Online')
                m = p.match(title)
                name = m.group(1)
                print name
            except AttributeError:
                p = re.compile('Watch (.*)')
                m = p.match(title)
                name = m.group(1)
                print name

            _series.name = name

            entry = html.find('div', class_='entry').findAll('p')[:3]
            # Synopsis
            for p in entry:
                if p.find('a', text=name+' Streaming'):
                    p.find('a', text=name+' Streaming').extract()
                    _series.synopsis = p.text

            for p in entry:
                if ('Genre' in p.text) and ('External Link' in p.text) \
                        and ('Release date' in p.text):

                    # Imdb
                    imdb = p.find('a')
                    if imdb:
                        _series.imdb = imdb.get('href')
                    metadata = p.text.split('\n')
                    for meta in metadata:
                        # Genre
                        if 'Genre' in meta:
                            _series.genre = meta.split(':')[1].strip()
                        # Release date
                        elif 'Release date' in meta:
                            _series.release_date = meta.split(':')[1].strip()

            # Photo
            for p in entry:
                photo = p.find('img', alt='Watch ' + name + ' Online')
                if photo:
                    _series.photo = photo.get('src')

        _series.save()

        # Check the episodes
        # If this is a quick check, check the number
        # of episodes
        # In case of a complete update or if the series has
        # just been created, process the whole list
        season_nb = 1
        ep_nb = 0
        for ul in html.findAll('ul'):
            season_tag = ul.find_previous('strong')
            if season_tag and season_tag.text == 'Season ' + str(season_nb):
                _season, new_season = Season.objects.get_or_create(
                    number=season_nb,
                    series=_series)
                for ep_tag in ul.findAll('a'):
                    ep_url = ep_tag.get('href')
                    if not ep_url:
                        ep_url = '#'
                    ep_text = ep_tag.text

                    # Patch a problem of unclosed unordered list...
                    regexp = ".*Season (\d*) .*"
                    p = re.compile(regexp)
                    m = p.match(ep_text)
                    if m is not None:
                        _season, new_season = Season.objects.get_or_create(
                            number=int(m.group(1)),
                            series=_series)
                    # End of the patch

                    regexp = u".*pisode ((\d|-)+)"
                    #regexp = u".*Episode (\S*)"
                    p = re.compile(regexp)
                    m = p.match(ep_text)
                    if m is None:
                        #self.log("Special ===> " + ep_text.encode('utf-8'))
                        ep_real_nb = str(ep_nb) + u'–' + 'spe'
                    else:
                        ep_real_nb = m.group(1)

                    if '-' in ep_real_nb:
                        ep_nb = int(ep_real_nb.split('-')[0])
                    elif u'–' in ep_real_nb:
                        ep_nb = int(ep_real_nb.split(u'–')[0])
                    else:
                        ep_nb = int(ep_real_nb)

                    if u'–' in ep_text:
                        ep_name = ep_text.split(u'–')[1].strip()
                    else:
                        ep_name = ''

                    episode, new_episode = Episode.objects.get_or_create(
                        name=ep_name,
                        real_number=ep_real_nb,
                        number=ep_nb,
                        season=_season,
                        url=ep_url)

                    if new_episode:
                        self.log(unicode(episode).encode('utf-8'))
                        # For each user who subscribed to the series
                        # inform him that a new episode is out
                        for u in _series.subscribers.all():
                            episode.watchers.add(u)

                        # if ep_text.encode('utf-8').strip() != unicode(
                        #         episode).encode('utf-8'):
                        #     self.log("Episode: " + ep_text.encode('utf-8'))
                        #     self.log("stored in DB as: " + unicode(
                        #         episode).encode('utf-8'))
                        #     self.log()

                season_nb += 1

    def handle(self, *args, **options):
        self.log("Starting check")
        self.createOrUpdateSeries()
        self.log("Check finished")

        #self.stdout.write(str(User.objects.count()))
