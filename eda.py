import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from nltk.corpus import stopwords
import numpy as np
from wordcloud import WordCloud

from utils import functions

# Conexión a la database

#Credenciales AWS
username = "tu_username"
password = "tu_password"
host = "tu_host" 
port = "tu_puerto"

db = pymysql.connect(host = host,
                     user = username,
                     password = password,
                     cursorclass = pymysql.cursors.DictCursor
)
cursor = db.cursor()

# ¿Cuál es el tweet con mayor repercusión social?
sql = '''SELECT * 
FROM tweets 
ORDER BY retweets_count
DESC LIMIT 1;'''
cursor.execute(sql)
mi_tabla = cursor.fetchall()
mi_tabla

# ¿Cuál es el usuario que más menciona a la escuela?
sql = '''SELECT author_id, COUNT(*) AS count
FROM tweets 
GROUP BY author_id
ORDER BY count
DESC LIMIT 1;'''
cursor.execute(sql)
mi_tabla = cursor.fetchall()
mi_tabla

sql = '''SELECT author_name
FROM users
WHERE author_id = 702077405045899264'''
cursor.execute(sql)
mi_tabla = cursor.fetchall()
mi_tabla

# ¿En qué mes se concentra el mayor número de tweets?
sql = '''SELECT MONTH(date) AS month, COUNT(*) AS num_tweets 
FROM tweets 
GROUP BY month 
ORDER BY num_tweets DESC '''
cursor.execute(sql)
mi_tabla = cursor.fetchall()
mi_tabla

# datos
data = [{'month': 11, 'num_tweets': 33},
        {'month': 12, 'num_tweets': 34},
        {'month': 1, 'num_tweets': 67},
        {'month': 2, 'num_tweets': 27},
        {'month': 3, 'num_tweets': 14}]

# Crear listas separadas para el mes y el número de tweets
months = [d['month'] for d in data]
num_tweets = [d['num_tweets'] for d in data]

# Crear una lista de nombres de los meses en orden
month_names = ['Noviembre', 'Diciembre', 'Enero', 'Febrero', 'Marzo']

# Crear el gráfico de tarta
#colors = ['#fa7e1e', '#feda75', '#4f5bd5', '#962fbf', '#d62976']
colors = ['gold', 'yellowgreen', 'coral', 'lightskyblue', 'mediumorchid']
explode = (0, 0, 0.1, 0, 0)  # explode 1st slice

plt.pie(num_tweets, labels=month_names, colors=colors, startangle=0, counterclock=False, explode=explode, shadow=True, autopct='%1.1f%%', labeldistance=1.15, wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })

# Establecer el título
plt.title('Porcentaje de tweets por mes')

# Mostrar el gráfico
#plt.axis('equal')

plt.savefig('img/groupby_month.png')
plt.show()


# ¿Qué palabras son más frecuentes?
tweets = pd.read_csv('data/tweets.csv')
clean_df = functions.nlp_clean(tweets, 'text', 'spanish')
#Wordcloud 
wordcloud = WordCloud(background_color='white', collocations=False,
                max_words = 200, max_font_size = 80, 
                 width=800, height=400)

plt.figure(figsize=(12, 12))
wordcloud.generate(' '.join(clean_df['text']))
plt.grid(visible=False)
plt.title('Palabras más frecuentes en las menciones a @TheBridge_Tech', fontsize=16, pad=40)
plt.imshow(wordcloud);
wordcloud.to_file('img/wordcloud.png')

# ¿Qué tipo de correlación matemática encuentras entre las métricas públicas?
# Extraer las métricas públicas
metrics = tweets.loc[:,'retweets_count':'quotes_count']

# Crear el heatmap de correlación
fig, ax = plt.subplots()
sns.heatmap(metrics.corr(), annot=True, cmap='Blues', ax=ax)

# Cambiar los nombres de los xticks
ax.set_xticklabels(['Retweets', 'Replies', 'Likes', 'Quotes'])
ax.set_yticklabels(['Retweets', 'Replies', 'Likes', 'Quotes'])

# Establecer el título del gráfico
ax.set_title('Correlación entre las métricas públicas de los tweets', pad=30, loc= 'center')

fig.tight_layout()
plt.savefig('img/correlations.png')
plt.show()


# Distribución de la longitud de los tweets
lengths = []
for index, i in enumerate(tweets['text']):
    lengths.append(len(i))

tweets['length'] = lengths
plt.hist(x=tweets['length'], bins=20, color='mediumslateblue',
                            alpha=0.8, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Número de caracteres')
plt.ylabel('Frecuencia')
plt.title('Distribución de la longitud de los tweets', pad=20)
plt.savefig('img/length_tweets.png')

db.close()