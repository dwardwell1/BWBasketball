import json
import requests

api_key = 'bf680b61288fa7d775ca603ec2c246ae'


# First get a list of in-season sports
sports_response = requests.get('https://api.the-odds-api.com/v3/sports', params={
    'api_key': api_key
})

sports_json = json.loads(sports_response.text)

if not sports_json['success']:
    print(
        'There was a problem with the sports request:',
        sports_json['msg']
    )

else:
    print()
    print(
        'Successfully got {} sports'.format(len(sports_json['data'])),
        'Here\'s the first sport:'
    )
    print(sports_json['data'][0])


odds_response = requests.get('https://api.the-odds-api.com/v3/odds', params={
    'api_key': api_key,
    'sport': 'basketball_nba',
    'region': 'us',  # uk | us | eu | au
    'mkt': 'h2h'  # h2h | spreads | totals
})

odds_json = json.loads(odds_response.text)
if not odds_json['success']:
    print(
        'There was a problem with the odds request:',
        odds_json['msg']
    )

else:
    # odds_json['data'] contains a list of live and
    #   upcoming events and odds for different bookmakers.
    # Events are ordered by start time (live events are first)
    print()
    print(
        'Successfully got {} events'.format(len(odds_json['data'])),
        'Here\'s the first event:'
    )
    print(odds_json['data'][0])

    # Check your usage
    print()
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])

example_return = {'id': 'e3173597dbefed391dd1ff8ba2b060ff',
                  'sport_key': 'basketball_nba',
                  'sport_nice': 'NBA',
                  'teams': ['Charlotte Hornets', 'Detroit Pistons'],
                  'commence_time': 1615507800,
                  'home_team': 'Charlotte Hornets',
                  'sites': [{'site_key': 'fanduel',
                             'site_nice': 'FanDuel',
                             'last_update': 1615457586,
                             'odds': {'h2h': [1.42, 2.98]}},
                            {'site_key': 'betfair',
                             'site_nice': 'Betfair',
                             'last_update': 1615457434,
                             'odds': {'h2h': [1.42, 3.0], 'h2h_lay': [1.5, 3.4]}},
                            {'site_key': 'betmgm',
                             'site_nice': 'BetMGM',
                             'last_update': 1615457636,
                             'odds': {'h2h': [1.44, 2.9]}},
                            {'site_key': 'sugarhouse',
                             'site_nice': 'SugarHouse',
                             'last_update': 1615457597,
                             'odds': {'h2h': [1.43, 2.88]}},
                            {'site_key': 'betrivers',
                             'site_nice': 'BetRivers',
                             'last_update': 1615457629,
                             'odds': {'h2h': [1.43, 2.88]}},
                            {'site_key': 'unibet',
                             'site_nice': 'Unibet',
                             'last_update': 1615457425,
                             'odds': {'h2h': [1.43, 2.88]}},
                            {'site_key': 'draftkings',
                             'site_nice': 'DraftKings',
                             'last_update': 1615457681,
                             'odds': {'h2h': [1.43, 2.88]}},
                            {'site_key': 'foxbet',
                             'site_nice': 'FOX Bet',
                             'last_update': 1615457481,
                             'odds': {'h2h': [1.4, 2.9]}},
                            {'site_key': 'pointsbetus',
                             'site_nice': 'PointsBet (US)',
                             'last_update': 1615457541,
                             'odds': {'h2h': [1.43, 2.85]}}],
                  'sites_count': 9}

""" Notes 

    for games in odds_json['data']:
       ...:     if 'Boston' in games['teams']:
       ...:         print(games) doesn't work, why is that?
       ok I found looking for full 'Boston Celtics' Does work, just not single word

     """
