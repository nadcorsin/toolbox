# -*- coding: UTF-8 -*-
# Copyright (C) 2018 Jean Bizot <jean@styckr.io>
""" Main lib for toolbox Project
"""

from os.path import split
import pandas as pd
import datetime

pd.set_option('display.width', 200)


def __init__(self):
    # Find the absolute path for the root dir (04-Decision-Science)
    # Uses __file__ as absolute path anchor
    # root_dir = os.path.dirname(os.path.dirname(__file__))
    return self
def punctuation_remover(self, text):
    # function that removes punctuation from a given text
    import string
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text
def to_lowercase(self, text):
    # function that makes all text lowercase
    return text.lower()
def num_remover(self, text):
    # removes numbers from a given text
    text = ''.join(char for char in text if not char.isdigit())
    return text
def stopword_remover(self, text):
    # removes stopwords from given text and returns text as list of words
    # imports
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    # english stopwords stored in variable stop_words
    stop_words = set(stopwords.words('english'))
    # splits text into list of words
    word_tokens = word_tokenize(text)
    # removes stopwords from text
    text_list = [word for word in word_tokens if not word in stop_words]
    # returns list of non-stopwords
    return text_list
def lemmatizer(self, text_list):
    # replaces words in text by their root
    # imports
    from nltk.stem import WordNetLemmatizer
    # instance
    lemmatizer = WordNetLemmatizer()
    # replaces each word in list by its root word
    text_list = [lemmatizer.lemmatize(word) for word in text_list]
    # returns list of each word rooted
    return text_list
def list_concat(self, text_list):
    # converts list of words back into string
    text = ' '.join(text_list)
    return text
def preprocessor(self, df_series):
    # complete preprocess with all functions above
    df_series = df_series.apply(punctuation_remover)
    df_series = df_series.apply(to_lowercase)
    df_series = df_series.apply(num_remover)
    df_series = df_series.apply(stopword_remover)
    df_series = df_series.apply(lemmatizer)
    df_series = df_series.apply(list_concat)
    return df_series
def hello():
    print('hello')

def clean_data(data):
    """ clean data
    """
    # Remove columns starts with vote
    cols = [x for x in data.columns if x.find('vote') >= 0]
    data.drop(cols, axis=1, inplace=True)
    # Remove special characteres from columns
    data.loc[:, 'civility'] = data['civility'].replace('\.', '', regex=True)
    # Calculate Age from day of birth
    actual_year = datetime.datetime.now().year
    data.loc[:, 'Year_Month'] = pd.to_datetime(data.birthdate)
    data.loc[:, 'Age'] = actual_year - data['Year_Month'].dt.year
    # Uppercase variable to avoid duplicates
    data.loc[:, 'city'] = data['city'].str.upper()
    # Take 2 first digits, 2700 -> 02700 so first two are region
    data.loc[:, 'postal_code'] = data.postal_code.str.zfill(5).str[0:2]
    # Remove columns with more than 50% of nans
    cnans = data.shape[0] / 2
    data = data.dropna(thresh=cnans, axis=1)
    # Remove rows with more than 50% of nans
    rnans = data.shape[1] / 2
    data = data.dropna(thresh=rnans, axis=0)
    # Discretize based on quantiles
    data.loc[:, 'duration'] = pd.qcut(data['surveyduration'], 10)
    # Discretize based on values
    data.loc[:, 'Age'] = pd.cut(data['Age'], 10)
    # Rename columns
    data.rename(columns={'q1': 'Frequency'}, inplace=True)
    # Transform type of columns
    data.loc[:, 'Frequency'] = data['Frequency'].astype(int)
    # Rename values in rows
    drows = {1: 'Manytimes', 2: 'Onetimebyday', 3: '5/6timesforweek',
             4: '4timesforweek', 5: '1/3timesforweek', 6: '1timeformonth',
             7: '1/trimestre', 8: 'Less', 9: 'Never'}
    data.loc[:, 'Frequency'] = data['Frequency'].map(drows)
    return data


if __name__ == '__main__':
    # For introspections purpose to quickly get this functions on ipython
    import toolbox
    folder_source, _ = split(toolbox.__file__)
    df = pd.read_csv('{}/data/data.csv.gz'.format(folder_source))
    clean_data = clean_data(df)
    print(' dataframe cleaned')
