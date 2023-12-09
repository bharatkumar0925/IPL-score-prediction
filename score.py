import pandas as pd
import numpy as np

path1 = r"C:\Users\BHARAT\Desktop\my files\data sets\iplData3\all_season_details.csv"
path2 = r"C:\Users\BHARAT\Desktop\my files\data sets\iplData3\all_season_summary.csv"
detail_data = pd.read_csv(path1, usecols=list(range(1, 15))+[36])
detail_data.drop(['match_name', 'shortText'], axis=1, inplace=True)
summary_data = pd.read_csv(path2, usecols=[1, 7, 8, 9, 10, 13, 14, 18])
summary_data = summary_data.replace({
    'Dr DY Patil Sports Academy, Mumbai': 'Dr DY Patil Sports Academy, Navi Mumbai',
    'KXIP': 'PBKS', 'GL': 'RR', 'RPS': 'CSK'})
detail_data = detail_data.replace({'KXIP': 'PBKS', 'GL': 'RR', 'RPS': 'CSK'})
#first_inning = summary_data.groupby('id')['1st_inning_score'].apply(lambda x: x.str.split('/').str.get(0).fillna(-1).astype(int)).reset_index(drop=True, level=1)
#second_inning = summary_data.groupby('id')['2nd_inning_score'].apply(lambda x: x.str.split('/').str.get(0)).fillna(-1).astype(int).reset_index(drop=True, level=1)
summary_data.drop(['1st_inning_score', '2nd_inning_score'], axis=1, inplace=True)


detail_data['is_wicket'] = detail_data['wkt_batsman_name'].notnull().astype(int)
detail_data.drop('wkt_batsman_name', axis=1, inplace=True)
#print(summary_data['target'].describe())
detail_data = detail_data.query('home_team != ["Kochi", "PWI"] and away_team != ["Kochi", "PWI"]')
summary_data = summary_data.query('result != "No result" and result!="Match abandoned without a ball bowled"')
expanded_data = summary_data.merge(detail_data, left_on='id', right_on='match_id')
expanded_data.drop(['result', 'match_id'], axis=1, inplace=True)
#expanded_data = expanded_data.merge(first_inning, on='id')
expanded_data['current_score'] = expanded_data.groupby(['id', 'innings_id'])['runs'].cumsum()
expanded_data['balls_left'] = (126-(expanded_data['over']*6+expanded_data['ball']))
expanded_data['score'] = expanded_data.groupby(['id', 'innings_id'])['current_score'].transform('last')
#print(expanded_data.columns)
print(expanded_data.head(130).to_string())
#expanded_data = expanded_data.sample(frac=1)
print(expanded_data.info())


#expanded_data.to_csv('matches.csv', index=False)
print(expanded_data.shape)
#print(expanded_data.info())
