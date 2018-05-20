import sys
sys.path.append('/Users/hchase/wasserman')

from constants import YEAR
from nba_season_stats import update_season_stats_for_single_year

update_season_stats_for_single_year(YEAR)
