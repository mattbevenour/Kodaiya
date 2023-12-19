import pandas as pd
import numpy as np

from random import sample

from pyaml_env import parse_config
config = parse_config('config.yaml')
target_variable = config['target_variable']

def populate_games(num_games: int, playerbase: list, df: pd.DataFrame, players_per_team: int = 5) -> pd.DataFrame:
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
    rosters = generate_rosters(num_games, playerbase, 2 * players_per_team)

    # take rosters and assign players on roster to team 1
    # remaining 5 players will be assigned team 0
    for game_id in rosters.keys():
        home_team = rosters[game_id][:players_per_team]
        away_team = rosters[game_id][players_per_team:]
        for player in home_team:
          df.loc[df['game_id']==game_id, [f'{player}_team1']] = 1
        for player in away_team:
          df.loc[df['game_id']==game_id, [f'{player}_team0']] = 1
    
    # fill nulls
    for player in playerbase:
        df[f'{player}_team0'].fillna(0, inplace=True)
        df[f'{player}_team1'].fillna(0, inplace=True)
    
    # calculate each players' goal scoring per game
    df_scores = generate_goals(playerbase, df)

    # calculate score aggregate for each game
    df_scores_total = calc_game_score(playerbase, num_games, df_scores)

    # assign label, ties are not a victory
    df_scores_total[target_variable] = np.where(df_scores_total['score_difference'] > 0, 1, 0)
   
    # return complete game list
    return df_scores

def generate_rosters(x: int, p: list, num_sample: int = 5)-> dict:
    '''
    Generates teams of num_sample for team 1 for X games
    Players are chosen from from exhaustive list of players p
    '''
    return_dict ={}
    for y in range(1,x+1):
        return_dict[y]= sample(p,num_sample)
    return return_dict

def generate_goals(playerbase: list, df: pd.DataFrame) -> pd.DataFrame:
    for player in playerbase:
        df[f'{player}_goals']= np.where((df[f'{player}_team0'] == 0) & (df[f'{player}_team1'] == 0),
                                        0,
                                        np.random.randint(config['scoring_ranges_extended'][player][0],
                                                 config['scoring_ranges_extended'][player][1] +1,
                                                  len(df))
        )
    return df

def calc_game_score(playerbase: list, num_games: int, df: pd.DataFrame) -> pd.DataFrame:
    for x in range(1, num_games+1):
        team1_total = 0
        team0_total = 0
        for player in playerbase:
            if df.loc[df['game_id']==x, [f'{player}_team1']].values[0] == 1:
                team1_total = team1_total + df.loc[df['game_id'] ==x, [f'{player}_goals']].values[0]
            elif df.loc[df['game_id']==x, [f'{player}_team0']].values[0] == 1:
                team0_total = team0_total + df.loc[df['game_id'] ==x, [f'{player}_goals']].values[0]
        df.loc[df['game_id']==x, ['score_difference']] = int(team1_total - team0_total)
    return df