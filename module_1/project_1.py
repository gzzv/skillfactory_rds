# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 20:21:50 2020

@author: Ildar
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from itertools import combinations


data = pd.read_csv('C:\\Python_test\\movie_bd_v5.xls')


# Предобработка
answers = {}
data['profit'] = data.revenue - data.budget

def sep_func(data, column):
    
    data[column] = data[column].map(lambda x: x.split('|'))
    data = data.explode(column)
    
    return data
   

# 1. У какого фильма из списка самый большой бюджет?
answers['1'] = 'Pirates of the Caribbean: On Stranger Tides (tt1298650)'
data[data.budget == data.budget.max()][['original_title', 'imdb_id', 'budget']]
# +


# 2. Какой из фильмов самый длительный (в минутах)?
answers['2'] = 'Gods and Generals (tt0279111)'
data[data.runtime == data.runtime.max()][['original_title', 'imdb_id', 'runtime']]
# +


# 3. Какой из фильмов самый короткий (в минутах)?
answers['3'] = 'Winnie the Pooh (tt1449283)'
data[data.runtime == data.runtime.min()][['original_title', 'imdb_id', 'runtime']]
# +


# 4. Какова средняя длительность фильмов?
answers['4'] = '110'
data['runtime'].mean()
# +


# 5. Каково медианное значение длительности фильмов?
answers['5'] = '107'
data['runtime'].median()
# +


# 6. Какой самый прибыльный фильм?
answers['6'] = 'Avatar (tt0499549)'
data[data.profit == data.profit.max()][['original_title', 'imdb_id', 'profit']]
# +


# 7. Какой фильм самый убыточный?
answers['7'] = 'The Lone Ranger (tt1210819)'
data[data.profit == data.profit.min()][['original_title', 'imdb_id', 'profit']]
# +


# 8. У скольких фильмов из датасета объем сборов оказался выше бюджета?
answers['8'] = '1478'
len(data[data.profit >0])
# +


# 9. Какой фильм оказался самым кассовым в 2008 году?
answers['9'] = 'The Dark Knight (tt0468569)'
data_9 = data[data.release_year == 2008]
data_9[data_9.profit == data_9.profit.max()][['original_title', 'imdb_id', 'profit']]
# +


# 10. Самый убыточный фильм за период с 2012 по 2014 годы (включительно)?
answers['10'] = 'The Lone Ranger (tt1210819)'
data[(data.release_year <= 2014) & (data.release_year >= 2012) & 
     (data.profit == data.profit.min())][['original_title', 'imdb_id', 'profit']]
# +


# 11. Какого жанра фильмов больше всего?
answers['11'] = 'Drama'
count_dict = {}
for genre in 'Action Adventure Drama Comedy Thriller'.split():
    count_dict[genre] = len(data[data.genres.str.contains(genre)])
# +


# 12. Фильмы какого жанра чаще всего становятся прибыльными?
answers['12'] = 'Drama'
Counter(data['genres'].str.cat(sep = '|').split('|')).most_common()
# +


# 13. У какого режиссера самые большие суммарные кассовые сбооры?
answers['13'] = 'Peter Jackson'
data.groupby(['director'])['revenue'].sum().sort_values(ascending=False)
# +


# 14. Какой режисер снял больше всего фильмов в стиле Action?
answers['14'] = 'Robert Rodriguez'
data_14 = data[data.genres.str.contains('Action', na = False)]
Counter(data_14['director'].str.cat(sep = '|').split('|')).most_common()
# +


# 15. Фильмы с каким актером принесли самые высокие кассовые сборы в 2012 году?
answers['15'] = 'Chris Hemsworth'
data_15 = data[data.release_year == 2012]
data_15 = sep_func(data_15, 'cast').groupby('cast')['revenue'].sum().sort_values(ascending=False)
# +


# 16. Какой актер снялся в большем количестве высокобюджетных фильмов?
answers['16'] = 'Matt Damon'
data_16 = data[data.budget > data.budget.mean()]
data_16 = sep_func(data_16, 'cast')['cast'].value_counts()
# +


# 17. В фильмах какого жанра больше всего снимался Nicolas Cage?
answers['17'] = 'Action'
data_17 = data[data.cast.str.contains('Nicolas Cage', na = False)]
data_17 = sep_func(data_17, 'genres')['genres'].value_counts()
# +


# 18. Самый убыточный фильм от Paramount Pictures
answers['18'] = 'K-19: The Widowmaker (tt0267626)'
data_18 = data[data.production_companies.str.contains('Paramount Pictures')]
data_18[data_18.profit == data_18.profit.min()][['original_title', 'imdb_id', 'profit']]
# +


# 19. Какой год стал самым успешным по суммарным кассовым сборам?
answers['19'] = '2015'
data.groupby(['release_year'])['revenue'].sum().sort_values(ascending=False)
# +


# 20. Какой самый прибыльный год для студии Warner Bros?
answers['20'] = '2014'
data_20 = data[data.production_companies.str.contains('Warner Bros')]
data_20.groupby(['release_year'])['profit'].sum().sort_values(ascending=False)
# +

# 21. В каком месяце за все годы суммарно вышло больше всего фильмов?
answers['21'] = 'Сентябрь'
data_21 = data.copy()
data_21['release_date'] = data_21['release_date'].map(lambda x: x.split('/'))
data_21['month'] = data_21['release_date'].map(lambda x: x[0])
data_21['month'].value_counts()
# +

# 22. Сколько суммарно вышло фильмов летом? (за июнь, июль, август)
answers['22'] = '450'
data_22 = data.copy()
data_22['release_date'] = data_22['release_date'].map(lambda x: x.split('/'))
data_22['month'] = data_22['release_date'].map(lambda x: x[0])
len(data_22[data_22['month'].isin(['6', '7', '8'])])
# +


# 23. Для какого режиссера зима – самое продуктивное время года? 
answers['23'] = 'Peter Jackson'
data_23 = data.copy()
data_23['release_date'] =data_23['release_date'].map(lambda x: x.split('/'))
data_23['month'] = data_23['release_date'].map(lambda x: x[0])
data_23 = data_23[data_23['month'].isin(['1', '2', '12'])]
data_23 = sep_func(data_23, 'director')['director'].value_counts()
# +


# 24. Какая студия дает самые длинные названия своим фильмам по количеству символов?
answers['24'] = 'Four By Two Productions'
data_24 = data.copy()
data_24['title_len'] = data_24['original_title'].map(lambda x: len(x))
data_24 = sep_func(data_24, 'production_companies')
data_24.groupby(['production_companies'])['title_len'].mean().sort_values(ascending=False)
# +


# 25. Описание фильмов какой студии в среднем самые длинные по количеству слов?
answers['25'] = 'Midnight Picture Show'
data_25 = data.copy()
data_25 = sep_func(data_25, 'production_companies')
data_25['overview_len'] = data_25['overview'].map(lambda x: len(x.split()))
data_25.groupby(['production_companies'])['overview_len'].mean().sort_values(ascending=False)
# +


# 26. Какие фильмы входят в 1 процент лучших по рейтингу?
answers['26'] = 'Inside Out, The Dark Knight, 12 Years a Slave'
data_26 = data[data.vote_average > data.quantile(0.99)['vote_average']]['original_title']
# +


# 27. Какие актеры чаще всего снимаются в одном фильме вместе?
answers['27'] = 'Daniel Radcliffe, Rupert Grint'
data_27 = pd.DataFrame(data['cast'].map(lambda x: x.split('|')))
data_27['pairs'] = data_27['cast'].map(lambda x: list(combinations(x, 2)))
Counter(data_27.explode('pairs')['pairs']).most_common(10)
# +


# Submission