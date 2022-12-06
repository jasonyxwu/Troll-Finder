import re
# import numpy as np
import pandas as pd
# plotting
# import seaborn as sns
# from wordcloud import WordCloud
import nltk

try:
    nltk.download('wordnet', download_dir='/opt/python/current/app')
    nltk.download('wordnet', download_dir='/opt/python/current/app')
    nltk.download('punkt', download_dir='/opt/python/current/app')


except:
    nltk.download('wordnet')
    nltk.download('omw-1.4')
    nltk.download('punkt')
import sklearn
from sklearn.linear_model import LogisticRegression
import pickle
import os



class Model:
  def __init__(self):
    self.emojis = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad', 
          ':-(': 'sad', ':-<': 'sad', ':P': 'raspberry', ':O': 'surprised',
          ':-@': 'shocked', ':@': 'shocked',':-$': 'confused', ':\\': 'annoyed', 
          ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy',
          '@@': 'eyeroll', ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused',
          '<(-_-)>': 'robot', 'd[-_-]b': 'dj', ":'-)": 'sadsmile', ';)': 'wink', 
          ';-)': 'wink', 'O:-)': 'angel','O*-)': 'angel','(:-D': 'gossip', '=^.^=': 'cat'}
    self.stopwords = [['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]]

  def pre_process(self, textdata):
    processedText = []
    
    # Create Lemmatizer and Stemmer.
    wordLemm = nltk.stem.WordNetLemmatizer()
    
    # Defining regex patterns.
    urlPattern        = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    userPattern       = '@[^\s]+'
    alphaPattern      = "[^a-zA-Z0-9]"
    # sequencePattern   = r"(.)\1\1+"
    # seqReplacePattern = r"\1\1"
    
    for tweet in textdata:
        
        tweet = tweet.lower()
        # Remove all URls
        tweet = re.sub(urlPattern,' ',tweet)
        # Replace all emojis.
        for emoji in self.emojis.keys():
            tweet = tweet.replace(emoji, self.emojis[emoji])        
        # Remove @Username
        tweet = re.sub(userPattern,' ', tweet)        
        # Replace all non alphabets.
        tweet = re.sub(alphaPattern, ' ', tweet)

        # Lemmatizing the word.
        tweetwords = ''
        for word in tweet.split():
          # Remove stopwords and shortwords before stemming
          if  len(word)>1 and word not in self.stopwords:   
              word = wordLemm.lemmatize(word)
              tweetwords += (word+' ')
          
        processedText.append(tweetwords)
        
    return processedText

  def load_models(self):
    # Load the vectoriser.
    file = open('vectoriser-ngram-(1,2)-feature-1000.pickle', 'rb')
    self.vectoriser = pickle.load(file)
    file.close()

    # Load the LR Model.
    file = open('sentiment-lr-2.pickle', 'rb')
    self.lr_model = pickle.load(file)
    file.close()

  def predict(self, text):
    # Predict the sentiment
    textdata = self.vectoriser.transform(self.pre_process(text))
    sentiment = self.lr_model.predict(textdata)
    
    ## Make a list of text with sentiment.
    # data = []
    # for text, pred in zip(text, sentiment):
    #     data.append((text,pred))
        
    # # Convert the list into a Pandas DataFrame.
    # df = pd.DataFrame(data, columns = ['text','sentiment'])
    # df = df.replace([0,1], ["Negative","Positive"])
    return sentiment