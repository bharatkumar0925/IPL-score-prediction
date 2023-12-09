import pandas as pd
import numpy as np

path = "matches.csv"
data = pd.read_csv(path)
data['wickets'] = data.groupby(['id', 'current_innings'])['is_wicket'].cumsum().astype(int)
data['wickets_left'] = 10-data['wickets']
data.drop(['is_wicket'], axis=1, inplace=True)

over = data['over']
ball = data['ball']
current_score = data['current_score']
data['crr'] = (current_score*6/((over-1)*6+ball)).round(2)
data['over'] = data['over']-1

#print(data[['home_team', 'away_team', 'over', 'ball', 'balls_left', 'current_score', 'wickets', 'wickets_left']].head(200).to_string(index=False))
data.drop(['winner', 'runs', 'isBoundary', 'isWide', 'isNoball'], axis=1, inplace=True)
count = data['venue_name'].value_counts().reset_index()
count.columns = ['venue_name', 'count']

# Identify venues with counts less than 1000
venues_to_replace = count[(count['count'] < 1500) |
                           (count['venue_name'].isin(['Kingsmead, Durban', 'SuperSport Park, Centurion',
                                                     'The Wanderers Stadium, Johannesburg',
                                                     "St George's Park, Port Elizabeth",
                                                     'Newlands, Cape Town']))]['venue_name'].tolist()

# Replace those venues with "other"
data['venue_name'] = data['venue_name'].apply(lambda x: 'other' if x in venues_to_replace else x)

# Print the updated DataFrame
print(data['venue_name'].value_counts())
#print(data.info())
#print(data[['id', 'over', 'ball', 'current_score', 'crr']].head(10))
print(data.info())
data.to_csv('final_data.csv', index=False)
