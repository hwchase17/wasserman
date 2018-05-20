import cgi
import json
from datetime import datetime

import pandas as pd
import requests as _requests

import api_constants as provider
from constants import SEASON_TYPES
from helpers import year_to_year_string
from sql.sql_helpers import update_database


def _get_db_name_from_measure_type(_measure_type):
    '''Consistent mapping of measure type to database name for seasons stats'''
    return 'season_{}'.format(_measure_type.lower())


def _get_season_stats(measure_type, year, season_type):
    '''Get raw season stats directly from NBA.com api'''
    year_id = year_to_year_string(year)
    api_params = provider.get_season_stats_api_params(measure_type, year_id, season_type)
    pull_url = cgi.urlparse.urljoin(provider.BASE_URL, provider.SEASON_SUMMARY_STATS_URL)
    response = _requests.get(pull_url, params=api_params, headers=provider.HEADER_DATA)
    data = json.loads(response.content)
    df = pd.DataFrame(data['resultSets'][0]['rowSet'])
    df.columns = data['resultSets'][0]['headers']
    return df


def _prep_df_for_database(df, year, season_type):
    '''Do various preprocessing steps to make df database friendly'''
    df.columns = map(unicode.lower, df.columns)
    df['year'] = year
    df['season'] = season_type
    df['update_time'] = datetime.now()
    return df


def update_season_stats_for_single_year(year):
    '''Update season stats databases for single year'''
    for measure_type in provider.SUMMARY_STATS_TYPES:
        all_df = []
        for season_type in SEASON_TYPES:
            _raw_data = _get_season_stats(measure_type, year, season_type)
            df = _prep_df_for_database(_raw_data, year, season_type)
            all_df.append(df)
        all_df = pd.concat(all_df)
        db_name = _get_db_name_from_measure_type(measure_type)
        update_database(db_name, all_df)


def update_season_stats_for_many_years(start_year, end_year):
    '''Update season stats databases for a list of years'''
    for year in range(start_year, end_year + 1):
        update_season_stats_for_single_year(year)
