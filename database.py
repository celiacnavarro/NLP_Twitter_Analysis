import snscrape.modules.twitter as sntwitter
import pandas as pd
from sqlalchemy import create_engine
import pymysql

from utils import functions
#Webscrapping de los tweets

#Definir las fechas
start_date = '2022-11-21'
end_date = '2023-03-07'

query = '@TheBridge_Tech since:{} until:{}'.format(start_date, end_date)
tweets = functions.scrape_tweets(query)

# Convertir la lista de tweets en un dataframe
tweets_df = pd.DataFrame(tweets, columns=['id', 'text', 'date', 'author_id', 'author_name', 'author_username', 'retweets', 'replies', 'likes', 'quotes'])

#Dataframe de los tweets
df_tweets = pd.DataFrame(columns=['id', 'text', 'date', 'author_id', 'retweets_count', 'replies_count', 'likes_count', 'quotes_count'])
df_tweets['id'] = tweets_df['id']
df_tweets['text'] = tweets_df['text']
df_tweets['date'] = tweets_df['date']
df_tweets['author_id'] = tweets_df['author_id']
df_tweets['retweets_count'] = tweets_df['retweets']
df_tweets['replies_count'] = tweets_df['replies']
df_tweets['likes_count'] = tweets_df['likes']
df_tweets['quotes_count'] = tweets_df['quotes']

#Dataframe de los users
df_users = tweets_df.loc[:, 'author_id':'author_username']
df_users.drop_duplicates(inplace=True)

# Base de datos en AWS

#Credenciales AWS
username = "tu_username"
password = "tu_password"
host = "tu_host" 
port = "tu_puerto"

#Conexión DB
db = pymysql.connect(host = host,
                     user = username,
                     password = password,
                     cursorclass = pymysql.cursors.DictCursor
)
cursor = db.cursor()

#Seleccionar base de datos
use_db = ''' USE tweets_database'''
cursor.execute(use_db)
#Crear base de datos
create_db = '''CREATE DATABASE tweets_database'''
cursor.execute(create_db)
# Crear las tablas en la base de datos
cursor.execute('''
        CREATE TABLE tweets (
        id bigint PRIMARY KEY,
        text text,
        date timestamp,
        author_id bigint,
        retweets_count int,
        replies_count int,
        likes_count int,
        quotes_count int
        )
    ''')
cursor.execute('''
        CREATE TABLE users (
        author_id bigint PRIMARY KEY,
        author_name text,
        author_username text
        )
    ''')

# Crear sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(user = username, pw = password, host = host, db = 'tweets_database'))
# engine = create_engine("mysql+pymysql://my_user:my_password@my_host/my_database")

# Cargar los dataframes en las tablas correspondientes
df_tweets.to_sql(name='tweets', con=engine, if_exists= 'append', index=False)
df_users.to_sql(name='users', con=engine, if_exists= 'append', index=False)
db.commit()
db.close()

df_tweets.to_csv('data/tweets.csv')
df_users.to_csv('data/users.csv')