import csv
import pandas as pd
import json
import numpy as np
import requests

# Bring in Data from data.csv
# remove dancability columns becasue all values are null delete ",," in csv file
with open('data.csv', 'r') as f:
    data = list(csv.reader(f, delimiter=','))
    data = np.array(data) # convert to numpy array
print(data)
# convert to pandas dataframe

dataframe = pd.DataFrame(data=data[1:,0:],    # values
                  columns=data[0,0:])  # 1st row as the column names
#print out all the column names
print(dataframe.columns)
#print(dataframe.head(5))


#years = dataframe['year'].unique()
#print(years)
# Calculate most frequent genres by year (split if multiple)

def get_genres(df):
    try:
        df['genres'] = df['genres'].str.replace('[', '')
        df['genres'] = df['genres'].str.replace(']', '')
        df['genres'] = df['genres'].str.replace(' ', '')
        df['genres'] = df['genres'].str.split(',')
        return df
    except:
        print(df)
        return df

# Calculate weights of genres by year
def get_genre_representation(df):
    ## initialize all 'year_genre_dict' columns
    year_genre_dict = {}
    #years = df['year'].unique()
    if df is None:
        return
    
    # add all list of genres to year_genre_dict
    
    years = df['year'].unique()
    #print(years)
    for year in years:
        year_genre_dict[year] = {}
        df_year = df[df['year'] == year]
        albums = df_year['album'].unique()
        for album in albums:
            df_album = df_year[df_year['album'] == album]
            for genre in df_album['genres'].iloc[0]:
                if genre not in year_genre_dict[year]:
                    year_genre_dict[year][genre] = 0
                #print(len(df_album['genres'].iloc[0]))
                year_genre_dict[year][genre] += 1 / len(df_album['genres'].iloc[0])
    # normalize weights
    for year in year_genre_dict:
        total = 0
        for genre in year_genre_dict[year]:
            total += year_genre_dict[year][genre]
        for genre in year_genre_dict[year]:
            year_genre_dict[year][genre] = year_genre_dict[year][genre] / total
    #print(year_genre_dict["2021"])
    return year_genre_dict
    

            
    ## normalize weights

def calculate_genre_weights(df):
    year_genre_dict = get_genre_representation(df)
    #print(year_genre_dict)
    if df is None:
        return
    else:
        for row in df.iterrows():
            year = row[1]['year']
            #print(year)
            genres = row[1]['genres']
            #print(genres)
            total = 0
            for genre in genres:
                if genre in year_genre_dict[year]:
                    total += year_genre_dict[year][genre] 
                else: 
                    year_genre_dict[year][genre] = 1 / len(genres)
                    total += year_genre_dict[year][genre] 
                #print(total)
            df.loc[row[0], 'genre_weights'] = total 
            #print(df.loc[row[0], 'genre_weights'])
        #print(df)
        return df
    

# Calculate the average of all features per year saled by album rank and genre weights

def normalize_all_features(df):
    if df is None:
        return
    features = ['acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'tempo', 'key', 'mode', 'time_signature', 'duration']
    try:
        for row in df.iterrows():
            for feature in features:
                ## Normalize feature 0-1
                df.loc[row[0], feature] = (df.loc[row[0], feature] - df[feature].min()) / (df[feature].max() - df[feature].min())
        return df
    except:
        return df

def calculate_feature_averages(df):
    if df is None:
        return
    features = ['acousticness',  'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence', 'tempo', 'key', 'mode', 'time_signature', 'duration']
    average_features = {}
    
    years = df['year'].unique()
    #try:
    average_features = {year : {} for year in years}
    for year in average_features:
        df_year = df[df['year'] == year]
            #print(average_features)
        for feature in features:
            array = df_year[feature].to_numpy()
            for i in range(len(array)):
                if array[i] == '':
                    array[i] = 0
                else: 
                    array[i] = float(array[i])
            arr_mean = np.mean(array)
            average_features[year][feature] = arr_mean
        #print(average_features)
    return average_features
    #except:
    #    for year in range(2015, 2023):
    #        average_features[year] = {}
    #        for feature in features:
    #            average_features[year][feature] = 0
    #    #print(average_features["2021"])
    #    return average_features

def init_normal(df):
    df = get_genres(df)
    df = calculate_genre_weights(df)
    df = normalize_all_features(df)
    return df

def get_average_features(df):
    average_features = calculate_feature_averages(df)
    return average_features 

def get_song_closeness(df):
    average_features = get_average_features(df)
    #print(average_features)
    for index, row in df.iterrows():
        #print(row)
        year = row['year']
        song_closeness = 0
        df.loc[index, 'song_closeness'] = 0
        for feature in average_features[year]:
            #print(feature)
            if df.loc[index, feature] == '':
                df.loc[index, feature] = 0
            song_closeness += abs(float(df.loc[index, feature]) - float(average_features[year][feature])) 
        #print(song_closeness)
        #print(df.loc[index, 'genre_weights'])
        df.loc[index, 'song_closeness'] = 1 / (201 - float(df.loc[index, 'rank']))**2 * song_closeness / float(df.loc[index, 'genre_weights'])   
        #print(df.loc[index, 'song_closeness'])
    return df

def return_top_song_by_year(df):
    ### Order df by song closeness
    df = df.sort_values(by=['song_closeness'])
    #print(df.head(5))
    ### Get top song by year
    top_songs = {}
    years = df['year'].unique()
    #print(years)
    for year in years:
        df_year = df[df['year'] == year]
        top_songs[year] = df_year.iloc[0]['track_name'] + " by " + df_year.iloc[0]['artist_name']
    return top_songs

def get_top_songs(df):  
    df = init_normal(df)
    #print(df.head(5))
    df = get_song_closeness(df)
    #print(df.head(5))
    top_songs = return_top_song_by_year(df)
    #print(top_songs)
    return top_songs

#print(get_top_songs(dataframe))

def dump_top5_to_json(df):
    df = init_normal(df)
    df = get_song_closeness(df)
    # Sort the DataFrame by 'year' and 'song_closeness'
    df_sorted = df.sort_values(by=['year', 'song_closeness'], ascending=[True, False])

    # Group the DataFrame by 'year' and get the top 5 entries for each group
    top_songs_by_year = df_sorted.groupby('year').head(5)

    # Convert the grouped DataFrame to a dictionary of JSON objects
    json_data = {
        year: group[['track_name','artist_name', 'song_closeness']].to_dict(orient='records')
        for year, group in top_songs_by_year.groupby('year')
    }

    # Write the JSON data to separate files for each year
    for year, data in json_data.items():
        filename = f'top5_songs_{year}.json'
        with open(filename, 'w') as f:
            f.write(pd.Series(data).to_json(orient='records', lines=True))

    return json_data

def write_top_songs_to_json(df, output_filename):
    df = init_normal(df)
    #print(df.head(5))
    df = get_song_closeness(df)
    # Order df by song closeness
    df = df.sort_values(by=['song_closeness'])

    # Get top 5 songs by year
    top_songs_by_year = {}
    years = df['year'].unique()
    
    for year in years:
        df_year = df[df['year'] == year]
        top_songs_by_year[year] = [
            df_year.iloc[i]['track_name'] + " by " + df_year.iloc[i]['artist_name']
            for i in range(min(5, len(df_year)))
        ]
    
    # Write the top songs by year to a JSON file
    with open(output_filename, 'w') as json_file:
        json.dump(top_songs_by_year, json_file, indent=4)

#output_filename = 'top_songs_by_year.json'
#write_top_songs_to_json(dataframe, output_filename)
#print(f"JSON data written to {output_filename}")

def get_song_data(song_id, headers):
    url = f'https://api.spotify.com/v1/tracks/{song_id}'
    response = requests.get(url, headers=headers)
    json_response = response.json()
    return json_response


def write_song_data_to_json(output_filename, headers):
    dataframe = pd.DataFrame(data=data[1:,0:],    # values
                  columns=data[0,0:])  # 1st row as the column names
    dataframe = init_normal(dataframe)
    #print(df.head(5))
    dataframe = get_song_closeness(dataframe)
    # Order df by song closeness
    dataframe = dataframe.sort_values(by=['song_closeness'])

    # Get top 5 songs by year
    top_songs_all_data = {}
    years = dataframe['year'].unique()
    
    for year in years:
        df_year = dataframe[dataframe['year'] == year]
        top_songs_all_data[year] = [
            get_song_data(df_year.iloc[i]['track_id'], headers)
            for i in range(min(5, len(df_year)))
        ]
    
    # Write the top songs by year to a JSON file
    with open(output_filename, 'w') as json_file:
        json.dump(top_songs_all_data, json_file, indent=4)