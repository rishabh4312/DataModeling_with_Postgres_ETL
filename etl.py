from typing import Callable
from psycopg2.extensions import connection, cursor

import os
import glob
import pandas as pd

from db import get_connection

from sql_queries import (
    songplay_table_insert,
    user_table_insert,
    song_table_insert,
    artist_table_insert,
    time_table_insert,
    song_select
)

# Paths for the files to process in ETL
song_file_path = "C:/Users/Rishabh/Desktop/Preperation2020/Udacity - Data Engineer/Project-1/data/song_data"
log_file_path = "C:/Users/Rishabh/Desktop/Preperation2020/Udacity - Data Engineer/Project-1/data/log_data"


def process_song_file(cur: cursor, filepath: str) -> None:
    """
    process a given song file and load to database

    """

    #read song file
    df = pd.read_json(filepath, lines = True)

    #insert song record from this into song table
    song_columns = ['song_id', 'title', 'artist_id', 'year', 'duration']
    song_data = df[song_columns].values[0].tolist()
    cur.execute(song_table_insert,song_data)

    #insert artist record into artist table
    artist_columns = ['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']
    artist_data = df[artist_columns].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)

def process_log_file(cur: cursor, filepath: str) -> None:
    """
    process a given log file and load to database

    """

    # read a log file into a dataframe
    df = pd.read_json(filepath, lines = True)

    # filter records on Next action
    df = df[df['page']=='NextSong']

    # insert records into time table
    t = pd.to_datetime(df['ts'], unit = 'ms')
    time_data = [[x, x.hour, x.day, x.week, x.month, x.year, x.dayofweek] for x in t]
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(time_data, columns = column_labels)

    for i,row in time_df.iterrows():
         cur.execute(time_table_insert, list(row))

    # insert users records
    users_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates()

    for i,row in users_df.iterrows():
        cur.execute(user_table_insert, row)
    
    # insert songplay records

    for index,row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, [row.song, row.artist, row.length])
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None,None
        
        #insert songplay record
        songplay_data = [pd.to_datetime(row.ts), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent]
        cur.execute(songplay_table_insert, songplay_data)
    
def process_data(cur: cursor, conn: connection, filepath: str, func: Callable) -> None:
    """
    will process each data file in a given filepath using func

    """

    #get all files matching exstension from directory
    all_files=[]
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,"*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))
    
    # get total number of files
    num_files = len(all_files)
    print(f"{num_files} found in {filepath}")

    # iterate over files and process
    for i,datafile in enumerate(all_files,1):
        func(cur, datafile)
        conn.commit()
        print(f"{i}/{num_files} files processed.")

def main():
    """
    Sparkify ETL pipeline

    """

    #get reusable database connection
    conn, cur = get_connection()

    #process song and log data

    process_data(cur, conn, song_file_path, func=process_song_file)
    process_data(cur, conn, filepath=log_file_path, func=process_log_file)

    #close database connections
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()



    



