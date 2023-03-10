import sntwitter
import re
import nltk
from googletrans import Translator
import plotly.graph_objs as go
from plotly import tools
from collections import defaultdict
import pandas as pd
import plotly.offline as py
from wordcloud import STOPWORDS


def scrape_tweets(query):
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(query).get_items():
        if tweet.user.username != 'TheBridge_Tech':
            tweet_id = tweet.id
            text = tweet.rawContent
            date = tweet.date.strftime('%Y-%m-%d %H:%M:%S')
            author_id = tweet.user.id
            author_name = tweet.user.displayname
            author_username = tweet.user.username
            retweets = tweet.retweetCount
            replies = tweet.replyCount
            likes = tweet.likeCount
            quotes = tweet.quoteCount
            tweets.append([tweet_id, text, date, author_id, author_name, author_username, retweets, replies, likes, quotes])
    return tweets

def nlp_clean(df, column, language):

    #Borramos los missing values
    df.dropna(inplace=True)
    
    # Eliminamos los duplicados
    df.drop_duplicates(inplace=True)

    #Eliminamos menciones
    df[column] = df[column].str.replace(r'\s*@\w+', '', regex=True)

    #Eliminamos signos de puntuación y pasamos a minúsculas
    signos = re.compile("(\.)|(\;)|(\:)|(\¡)|(\#)|(\!)|(\?)|(\¿)|(\@)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")

    def signs_tweets(tweet):
        return signos.sub('', tweet.lower())

    df[column] = df[column].apply(signs_tweets)
    
    #Eliminamos los emojis
    df.astype(str).apply(lambda x: x.str.encode('ascii', 'ignore').str.decode('ascii'))

    #Eliminamos links
    def remove_links(df):
        return " ".join([' ' if ('http') in word else word for word in df.split()])
    
    df[column] = df[column].apply(remove_links)

    #Eliminamos stopwords
    stopwords_lang = stopwords.words(language)
    def remove_stopwords(df):
        return " ".join([word for word in df.split() if word not in stopwords_lang])
    
    df[column] = df[column].apply(remove_stopwords)

    #Guardamos los datos procesados
    final_df = df[[column]]
    return final_df

def translate_tweet(tweet):
    translator = Translator()
    if translator.detect(tweet).lang == 'eu':
        return translator.translate(tweet, src='eu', dest='es').text
    else:
        return tweet

def plot_ngrams(df, target:str, text:str, n_gram:int):

    df1 = df[df[target] ==1]
    df0 = df[df[target] ==0]
    ## custom function for ngram generation ##
    def generate_ngrams(text, n_gram):
        token = [token for token in text.lower().split(" ") if token != "" if token not in STOPWORDS]
        ngrams = zip(*[token[i:] for i in range(n_gram)])
        return [" ".join(ngram) for ngram in ngrams]
    ## custom function for horizontal bar chart ##
    def horizontal_bar_chart(df, color):
        trace = go.Bar(
            y=df["word"].values[::-1],
            x=df["wordcount"].values[::-1],
            showlegend=False,
            orientation='h',
            marker=dict(
                color=color,
            ),
        )
        return trace

    ## Get the bar chart from text with label 0 ##
    freq_dict = defaultdict(int)
    for sent in df0[text]:
        for word in generate_ngrams(sent, n_gram):
            freq_dict[word] += 1
    fd_sorted = pd.DataFrame(sorted(freq_dict.items(), key=lambda x: x[1])[::-1])
    fd_sorted.columns = ["word", "wordcount"]
    trace0 = horizontal_bar_chart(fd_sorted.head(50), 'blue')

    ## Get the bar chart from text with label 1 ##
    freq_dict = defaultdict(int)
    for sent in df1[text]:
        for word in generate_ngrams(sent, n_gram):
            freq_dict[word] += 1
    fd_sorted = pd.DataFrame(sorted(freq_dict.items(), key=lambda x: x[1])[::-1])
    fd_sorted.columns = ["word", "wordcount"]
    trace1 = horizontal_bar_chart(fd_sorted.head(50), 'blue')

    # Creating two subplots
    fig = tools.make_subplots(rows=1, cols=2, vertical_spacing=0.04,
                          subplot_titles=["Palabras frecuentes en tweets negativos", 
                                          "Palabras frecuentes en tweets positivos"])
    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 2)
    fig['layout'].update(height=1200, width=900, paper_bgcolor='rgb(233,233,233)', title="Word Count Plots")
    fig.write_image("img/plot_ngrams.png")
    py.iplot(fig, filename='word-plots')
