# Import Libraries
import requests
import pandas as pd
import time

ANIME_FILEPATH = r'Anime_Recommender_System\anime.csv'
REVIEW_FILEPATH = r'Anime_Recommender_System\reviews.csv'

def get_anime(df):
  # Make API Call
  initial_response = requests.get("https://api.jikan.moe/v4/anime?page=0&type=tv&status=complete").json()
  max_pages = initial_response["pagination"]["last_visible_page"]
  time.sleep(0.5)

  for page in range(1, max_pages+1):
    response = requests.get(f"https://api.jikan.moe/v4/anime?page={page}&type=tv&status=complete").json()
    time.sleep(1)
    anime_data = response["data"]
    for anime in anime_data:
      anime_id = anime["mal_id"]
      anime_name = anime["title"]
      anime_name_eng = anime["title_english"]
      num_episodes = anime["episodes"]
      start_date = anime["aired"]["from"]
      end_date = anime["aired"]["to"]
      duration = anime["duration"]
      rating = anime["rating"]
      score = anime["score"]
      rank = anime["rank"]
      synopsis = anime["synopsis"]
      genres = [genre["name"] for genre in anime["genres"]]
      demographics = [demo["name"] for demo in anime["demographics"]]

      df = df.append({"MAL_ID" : anime_id,
                 "anime_name" : anime_name,
                 "anime_name_eng" : anime_name_eng,
                 "num_episodes" : num_episodes,
                 "start_date" : start_date,
                 "end_date" : end_date,
                 "duration" : duration,
                 "rating" : rating,
                 "score" : score,
                 "rank" : rank,
                 "synopsis" : synopsis,
                 "genres" : genres,
                 "demographics" : demographics},
                 ignore_index=True)
  return df

refresh = True
if refresh:
  anime_df = pd.DataFrame(columns=["MAL_ID", "anime_name", "anime_name_eng", "num_episodes", "start_date", "end_date", "duration", "rating", "score", "rank", "synopsis", "genres", "demographics"])

  anime_df = get_anime(anime_df)
  anime_df.to_csv(ANIME_FILEPATH, index=False, columns=anime_df.columns)
else:
  anime_df = pd.read_csv(ANIME_FILEPATH)

review_df = pd.DataFrame(columns=["username", "MAL_ID", "score", "review"])

anime_with_score_df = anime_df[anime_df.score.notnull()]
anime_id = anime_with_score_df["MAL_ID"]
max_index = list(anime_id.items())[-1][0]

review_df.to_csv(REVIEW_FILEPATH, index=False)
for index, anime in anime_id.items():
  for page in range(1, 50):
    start_time = time.time()
    response = requests.get(f"https://api.jikan.moe/v4/anime/{anime}/reviews?page={page}")
    end_time = time.time()
    duration_time = end_time - start_time
    if duration_time < 1:
      time.sleep(1-duration_time)
    if response.status_code == 400 or "status" in response.json():
      break
    review_json = response.json()
    
    review_data = review_json["data"]
    for review in review_data:
      user_name = review["user"]["username"]
      score = review["score"]
      review_desc = review["review"]


      new_review_df = pd.DataFrame({"username" : user_name,
                  "MAL_ID" : anime,
                  "score" : score,
                  "review" : review_desc}, index=[0])
      
      new_review_df.to_csv(REVIEW_FILEPATH, index=False, mode='a', header=False)
    print(f"{anime}_{page}")
    print(f"{index/max_index*100}_%")
   

