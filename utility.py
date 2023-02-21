import pandas as pd
import numpy as np

from random import sample

from pyaml_env import parse_config
config = parse_config('config.yaml')
target_variable = config['target_variable']

def populate_games(num_games: int, playerbase: list, df: pd.DataFrame) -> pd.DataFrame:
    '''
    Main game generation function

    assigns teams for each of $num_games games from list playerbase
    determines scores for all players participating in each game
    calculates score differential for each game
    determines, based on score differential, whether team 1 won
    '''
    # generate game IDs
    df['game_id'] = list(range(1,num_games+1))

    # generate dictionary for team rosters based on game ID
    rosters = generate_rosters(num_games, playerbase)

    # take rosters and assign players on roster to team 1
    # remaining 5 players will be assigned team 0
    for game_id in rosters.keys():
        home_team = rosters[game_id]
        for player in home_team:
          df.loc[df['game_id']==game_id, [f'{player}_team']] = 1
    
    # fill null teams with team 0
    for player in playerbase:
        df[f'{player}_team'].fillna(0, inplace=True)
    
    # calculate each players' goal scoring per game
    df_scores = generate_goals(playerbase, df)

    # calculate score aggregate for each game
    df_scores_total = calc_game_score(playerbase, num_games, df_scores)

    # assign label, ties are not a victory
    df_scores_total[target_variable] = np.where(df_scores_total['score_difference'] > 0, 1, 0)
   
    # return complete game list
    return df_scores

def generate_rosters(x: int, p: list)-> dict:
    '''
    Generates teams of 5 for team 1 for X games
    Players are chosen from from exhaustive list of players p
    '''
    return_dict ={}
    for y in range(1,x+1):
        return_dict[y]= sample(p,5)
    return return_dict

def generate_goals(playerbase: list, df: pd.DataFrame) -> pd.DataFrame:
    for player in playerbase:
        df[f'{player}_goals']= np.random.randint(config['scoring_ranges'][player][0],
                                                 config['scoring_ranges'][player][1] +1,
                                                  len(df))
    return df

def calc_game_score(playerbase: list, num_games: int, df: pd.DataFrame) -> pd.DataFrame:
    for x in range(1, num_games+1):
        team1_total = 0
        team0_total = 0
        for player in playerbase:
            if df.loc[df['game_id']==x, [f'{player}_team']].values[0] == 1:
                team1_total = team1_total + df.loc[df['game_id'] ==x, [f'{player}_goals']].values[0]
            else:
                team0_total = team0_total + df.loc[df['game_id'] ==x, [f'{player}_goals']].values[0]
        df.loc[df['game_id']==x, ['score_difference']] = int(team1_total - team0_total)
    return df