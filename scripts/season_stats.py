import os
os.chdir('/c/Users/hchase/wasserman')

from constants import YEAR
from season_stats import update_season_stats_for_single_year

update_season_stats_for_single_year(YEAR)