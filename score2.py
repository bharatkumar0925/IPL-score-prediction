import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report, r2_score, mean_squared_error
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor, GradientBoostingRegressor
import warnings
import pickle
warnings.filterwarnings('ignore')
data = pd.read_csv('final_data.csv')
cat_col = list(data.select_dtypes(['object', 'category']))
data = data.astype({'id': 'int32', **{col: 'category' for col in cat_col}})
data.drop(['over', 'ball', 'balls_left'], axis=1, inplace=True)



# Apply OneHotEncoder using ColumnTransformer
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(sparse=False, dtype='bool'), cat_col)
    ],
    remainder='passthrough'
)

data = data.astype({'current_score': 'int16', 'id': 'int32', 'season': 'int16', 'crr': 'float32', 'score': 'int16', 'wickets': 'int8', 'wickets_left': 'int8'})


X = data.drop('score', axis=1)
y = data['score']
our_data = data.query('id==1304047')

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(
    n_estimators=100,
    max_samples=0.7,
    max_features=15,
    n_jobs=-1, random_state=42, oob_score=True)
pipe = Pipeline([
    ('preprocessor', preprocessor),
    ('model', model)
])
#cv = cross_val_score(model, X_train, y_train, cv=5, scoring='r2', n_jobs=-1)
pipe.fit(X_train, y_train)

oob_score = pipe.named_steps['model'].oob_score_

#with open('score_prediction.pkl', 'wb') as model_file:
#    pickle.dump(pipe, model_file)

y_pred = pipe.predict(X_test).round(0).astype(int)
print(r2_score(y_pred, y_test)*100)
print(mean_squared_error(y_pred, y_test))
print(oob_score*100)
#print(round(cv.mean()*(100), 3))
df = our_data.drop('score', axis=1)
prediction = pipe.predict(df).round(0).astype(int)

our_data['predicted'] = prediction
print(our_data[['current_score', 'wickets', 'score', 'predicted']].to_string(index=False))

temp = pd.DataFrame({
    'id': [2498010]*10,
    'toss_won': ['KKR']*10,
    'decision': ['BOWL FIRST']*10,
    'venue_name': ['Punjab Cricket Association IS Bindra Stadium, Mohali, Chandigarh']*10,
    'season': [2023]*10,
    'home_team': ['PBKS']*10,
    'away_team': ['KKR']*10,
    'current_innings': ['PBKS']*10,
    'innings_id': [1]*10,
    'over': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
    'current_score': [23, 36, 56, 79, 100, 121, 142, 153, 168, 191],
    'wickets': [1, 1, 1, 1, 1, 2, 3, 4, 5, 5]
})

temp['wickets_left'] = (10-temp['wickets'])
temp['crr'] = (temp['current_score']/temp['over']).round(2)
temp = temp.drop(['over'], axis=1)
prediction = pipe.predict(temp).round(0).astype(int)
temp['prediction'] = prediction

print(temp[['current_score', 'prediction']].to_string(index=False))


