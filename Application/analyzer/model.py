import re
# import numpy as np
import pandas as pd
# plotting
# import seaborn as sns
# from wordcloud import WordCloud
# # nltk
import nltk

import sklearn
from nltk.corpus import stopwords
from sklearn.linear_model import LogisticRegression
import pickle

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('punkt')

emojis = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad', 
          ':-(': 'sad', ':-<': 'sad', ':P': 'raspberry', ':O': 'surprised',
          ':-@': 'shocked', ':@': 'shocked',':-$': 'confused', ':\\': 'annoyed', 
          ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy',
          '@@': 'eyeroll', ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused',
          '<(-_-)>': 'robot', 'd[-_-]b': 'dj', ":'-)": 'sadsmile', ';)': 'wink', 
          ';-)': 'wink', 'O:-)': 'angel','O*-)': 'angel','(:-D': 'gossip', '=^.^=': 'cat'}

def pre_process(textdata):
    processedText = []
    
    # Create Lemmatizer and Stemmer.
    wordLemm = nltk.stem.WordNetLemmatizer()
    
    # Defining regex patterns.
    urlPattern        = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    userPattern       = '@[^\s]+'
    alphaPattern      = "[^a-zA-Z0-9]"
    sequencePattern   = r"(.)\1\1+"
    seqReplacePattern = r"\1\1"
    
    for tweet in textdata:
        tweet = tweet.lower()
        
        # Remove all URls
        tweet = re.sub(urlPattern,' ',tweet)
        # Replace all emojis.
        for emoji in emojis.keys():
            tweet = tweet.replace(emoji, emojis[emoji])        
        # Remove @Username
        tweet = re.sub(userPattern,' ', tweet)        
        # Replace all non alphabets.
        tweet = re.sub(alphaPattern, ' ', tweet)
        
 
        stop_words = set(stopwords.words('english'))

        # Lemmatizing the word.
        tweetwords = ''
        for word in tweet.split():
          # Remove stopwords and shortwords before stemming
          if  len(word)>1 and word not in stop_words:   
              word = wordLemm.lemmatize(word)
              tweetwords += (word+' ')
          
        processedText.append(tweetwords)
        
    return processedText
def load_models():
    
    # Load the vectoriser.
    file = open('vectoriser-ngram-(1,2)-feature-1000.pickle', 'rb')
    vectoriser = pickle.load(file)
    file.close()
    # Load the LR Model.
    file = open('sentiment-lr-2.pickle', 'rb')
    lr_model = pickle.load(file)
    file.close()
    
    return vectoriser, lr_model

def predict(vectoriser, model, text):
    # Predict the sentiment
    textdata = vectoriser.transform(pre_process(text))
    sentiment = model.predict(textdata)
    
    # Make a list of text with sentiment.
    data = []
    for text, pred in zip(text, sentiment):
        data.append((text,pred))
        
    # Convert the list into a Pandas DataFrame.
    df = pd.DataFrame(data, columns = ['text','sentiment'])
    df = df.replace([0,1], ["Negative","Positive"])
    return df

if __name__=="__main__":
    # Loading the models.
    vectoriser, lr_model = load_models()
    
    # Text to classify should be in a list.
    text = ["It's really fine.. Noting impressive"]
    
    df = predict(vectoriser, lr_model, text)
    print(df.head())