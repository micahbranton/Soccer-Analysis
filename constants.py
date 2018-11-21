# =============================================================================
#          File: constants.py
#        Author: Andre Brener
#       Created: 22 Aug 2017
# Last Modified: 21 Nov 2018
#   Description: description
# =============================================================================
from datetime import date

COMPETITION_DICT = {
    'primera_division': 'arg.1',
    'copa_argentina': 'arg.copa',
    'copa_libertadores': 'conmebol.libertadores',
    'copa_sudamericana': 'conmebol.sudamericana',
    'recopa_sudamericana': 'conmebol.recopa',
    'world_cup': 'fifa.world',
    'confederations_cup': 'fifa.confederations',
    'europa_league': 'uefa.europa',
    'champions_league': 'uefa.champions',
}

COMPETITION = 'primera_division'

START_DATE = date(2017, 8, 27)
END_DATE = date(2017, 8, 28)
