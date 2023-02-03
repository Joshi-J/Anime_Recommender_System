import pandas as pd

REVIEW_FILEPATH = r'Anime_Recommender_System\reviews.csv'

review_df = pd.read_csv(REVIEW_FILEPATH)
# print(review_df.tail)
# print(review_df.columns)
print(review_df[review_df["username"].str.contains("username", na = False)])  
