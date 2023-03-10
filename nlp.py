import pandas as pd
import pickle
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
from googletrans import Translator

from utils import functions

# Abrir el modelo
with open('model/sentiment_model', "rb") as archivo_entrada:
    model = pickle.load(archivo_entrada)
tweets = pd.read_csv('data/tweets.csv')

# Traducir los tweets que no están en castellano
tweets['text_trans'] = tweets['text'].apply(functions.translate_tweet)

df = functions.nlp_clean(tweets, 'text_trans', 'spanish')

# Predicciones
predictions = model.predict(df['text_trans'])
df.loc[:,'pred_bin'] = pd.Series(predictions)

# Predicciones de probabilidad
predictions = model.predict_proba(df['text_trans'])
# Obtener la probabilidad de la clase positiva y negativa
pos_probs = predictions[:, 1]
neg_probs = predictions[:, 0]
# Agregar las columnas de predicción al dataframe original
df['polarity_pos'] = pos_probs
df['polarity_neg'] = neg_probs

# Guardar las predicciones
df.to_csv('data/predictions.csv')

# Crear el pie chart
colors = ['yellowgreen', 'lightskyblue']
explode = (0, 0.1)  
plt.pie(df['pred_bin'].value_counts(), labels=['Negativas', 'Positivas'], colors=colors, startangle=0, counterclock=False, explode=explode, shadow=True, autopct='%1.1f%%', labeldistance=1.15, wedgeprops = { 'linewidth' : 3, 'edgecolor' : 'white' })
# Establecer el título
plt.title('Porcentaje de predicciones de análisis de sentimiento')
# Mostrar el gráfico
plt.savefig('img/pred_percentage.png')
plt.show()

# Gráfico de la predicción probabilística
plt.hist(x=df['polarity_pos'], bins=13, color='coral',
                            alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Porcentaje')
plt.ylabel('Frecuencia')
plt.title('Predicción probabilística positiva')
plt.savefig('img/pred_proba.png')

# Variables más importantes del modelo

# Obtener todos los coeficientes
coeficients = model.named_steps['cls'].coef_[0]
# Obtener los nombres de las características (palabras) del CountVectorizer
feature_names = model.named_steps['vect'].vocabulary_
# Crear un diccionario con los coeficientes y las características
# Montar un diccionario con palabra -> coeficiente
feature_to_coef = {
    word: coef for word, coef in zip(
        feature_names, coeficients
    )
}

for best_positive in sorted(
    feature_to_coef.items(), 
    key=lambda x: x[1], 
    reverse=True)[:5]:
    print(best_positive)
    
print('################################')
for best_negative in sorted(
    feature_to_coef.items(), 
    key=lambda x: x[1])[:5]:
    print(best_negative)
    

# Palabras más frecuentes en los tweets positivos y negativos
functions.plot_ngrams(df, 'pred_bin', 'text_trans', 1)

# Guardar dataframe procesado
df.to_csv('data/tweets_cleaned.csv')
