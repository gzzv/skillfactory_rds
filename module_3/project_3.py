# -*- coding: utf-8 -*-
"""
Created on Tue Dec 29 18:56:51 2020

@author: Ildar
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestRegressor  
from sklearn import metrics
import matplotlib.pyplot as plt
from ast import literal_eval


def reviews_interval(row):
    '''Определение интервала между отзывами'''
    
    if len(row[1]) < 2:
        return 0
    else:
        return abs((pd.to_datetime(row[1][1]) - pd.to_datetime(row[1][0])).days)
 

def last_review(row):
    '''Количество дней до последнего отзыва'''
    
    if len(row[1]) < 1:
        return 0
    else:
        return abs(today - max(list(map(lambda x: pd.to_datetime(x), row[1])))).days


def reviews_length(row):
    '''Расчет средней длины отзыва'''
    
    if len(row[0]) < 1:
        return 0
    elif pd.isna(row[0][0]):
        return 0
    elif len(row[0]) == 1:
        return len(row[0][0])
    elif pd.isna(row[0][1]):
        return 0
    else:
        return (len(row[0][0]) + len(row[0][1]))/2


def price_level(price):
    '''Кодировка по ценовой категории'''
    
    if price == '$':
        return 1
    elif price == '$$$$':
        return 3
    else:
        return 2

    
def div_by_ranking(row):
    '''One-Hot Encoding по значению признака 'Ranking'''
    
    if row >= 11000:
        return 0
    else:
        return 1


random_seed = 42
data = pd.read_csv('main_task.csv')


# Добавление столбцов с указанием наличия пропусков для переменных с пропусками
data['Number_of_Reviews_isNAN'] = pd.isna(data['Number of Reviews']).astype('uint8')
data['Price Range_isNAN'] = pd.isna(data['Price Range']).astype('uint8')
data['Cuisine Style_isNAN'] = pd.isna(data['Cuisine Style']).astype('uint8')


# Замена Nan на 0
data['Number of Reviews'].fillna(0, inplace=True)
# Замена Nan на наиболее часто встречаюшееся значение
data['Price Range'] = data['Price Range'].replace({np.nan: data['Price Range'].value_counts().index[0]})
# Замена Nan на 'European'
data['Cuisine Style'] = data['Cuisine Style'].replace({np.nan: '[\'European\']'})
# Замена Nan на '[[], []]'
data['Reviews'].fillna('[[], []]', inplace=True)


# Преобразование переменной 'Cuisine Style'
data['Cuisine Style'] = data['Cuisine Style'].apply(lambda x: literal_eval(x))


# Добавление переменной 'Number of Cuisine' (количество представленных кухонь)
data['Number of Cuisine'] = data['Cuisine Style'].apply(lambda x: len(x))


# Добавление столбца с количеством ресторанов, входящих в сеть
chain = data['Restaurant_id'].value_counts()
data['Chain'] = data['Restaurant_id'].apply(lambda x: chain[x])


# Преобразование переменной 'Reviews' 
data['Reviews'] = data['Reviews'].apply(lambda x: literal_eval(x.replace('nan', 'None')))


#  Добавление 'Reviews Length'(длина отзыва)
data['Reviews Length'] = data['Reviews'].apply(reviews_length)


# Суммарное количество отзывов всех ресторанов в городе
reviews_in_city = data.groupby(['City'])['Number of Reviews'].sum().sort_values(ascending=False)
data['Reviews in City'] = data['City'].apply(lambda x: reviews_in_city[x])


#  Добавление 'Last Review', 'Reviews interval'
today = pd.to_datetime('today').normalize()
data['Last Review'] = data['Reviews'].apply(last_review)
data['Reviews interval'] = data['Reviews'].apply(reviews_interval)


# Добавление столбца с количеством конкурентов в городе, в котором находится ресторан
city = data['City'].value_counts()
data['Restaurant in city'] = data['City'].apply(lambda x: city[x])


# Столбец с уникальными id (понадобится для определения количества конкурентов в городе с подобной кухней)
data['Unique id'] = np.arange(len(data))


# Добавление признака со средним количеством конкурентов в городе с подобной кухней
competitors = data[['Unique id', 'City', 'Cuisine Style']].explode('Cuisine Style',
                                                                   ignore_index=True)
pivot_data = pd.pivot_table(competitors, index = ['City'], 
                            columns = ['Cuisine Style'], aggfunc = 'count', 
                            fill_value = 0)
pivot_data.columns = list(pivot_data.columns.map(lambda x: x[1]))

count = 0
competitors['Сompetitors'] = 0
for index, row in competitors.iterrows():
    competitors['Сompetitors'][index] = pivot_data[row['Cuisine Style']][row['City']]
    count +=1    
data = data.merge(competitors.groupby(['Unique id']).agg(Avg_Сompetitors=('Сompetitors', 'mean')), 
                  left_on='Unique id', right_on='Unique id')


# Нормализуем 'Ranking' по ресторанам в городе
data['Ranking Norm'] = data['Ranking'] / data['Restaurant in city']


# 'Ranking' к количеству ресторанов в сети
data['Ranking to Chain'] = data['Ranking'] / data['Chain']


# 'Ranking' к количеству отзывов (в городе и суммарно)
data['Ranking to Reviews'] = data['Ranking'] / data['Reviews in City']
data['Ranking to Reviews1'] = data['Ranking'] / data['Number of Reviews']
data['Ranking to Reviews1'] = data['Ranking to Reviews1'].replace({np.inf: 0})


# id ресторана
data['ID_TA'] = data['ID_TA'].apply(lambda x: int(x[1:]))


# One-Hot Encoding по значению признака 'Ranking
data['Divide by Ranking'] = data['Ranking'].apply(div_by_ranking)


# One-Hot Encoding по городам
data = pd.get_dummies(data, columns=['City'])


# Label Encoding по ценовой категории   
data['Price level'] = data['Price Range'].apply(price_level)


# Удаление лишних столбцов
data = data.drop(['Restaurant_id', 'URL_TA', 'Unique id', 'Cuisine Style', 
                  'Price Range', 'Reviews', 'Restaurant in city', 'Ranking'], axis=1)


cor_matrix = data.corr()
#%%
y = data['Rating']
x = data.drop(['Rating'], axis=1)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2) 

regr = RandomForestRegressor(n_estimators=100, verbose=1, n_jobs=-1, random_state=random_seed)   
regr.fit(x_train, y_train)    
y_pred = regr.predict(x_test)  
print('MAE:', metrics.mean_absolute_error(y_test, y_pred)) 

plt.rcParams['figure.figsize'] = (10,10)
feat_importances = pd.Series(regr.feature_importances_, index=x.columns)
feat_importances.nlargest(15).plot(kind='barh')