import os
import urllib

from constants import IMAGE_TEMPLATE


def year_to_year_string(year):
    '''Transform a year (YYYY) to a year string (YYYY-YY)'''
    last_two_digits = str(year % 100 + 1).zfill(2)
    return '{}-{}'.format(year, last_two_digits)


def _get_path_to_headshot(player_id):
    '''Get path to headshot'''
    return 'player_headshots/{}.png'.format(player_id)


def populate_path_to_headshot(year, player_id, force_populate=False):
    '''Return a path to a player headshot, scraping from web if desired/needed'''
    path = _get_path_to_headshot(player_id)
    if force_populate or not os.path.isfile(path):
        web_url = IMAGE_TEMPLATE.format(year=year, player=player_id)
        urllib.urlretrieve(web_url, path)
    return path
