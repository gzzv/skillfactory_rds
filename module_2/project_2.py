# -*- coding: utf-8 -*-

# Описание и выводы по проекту находятся в файле README

# Импорт требуемых библиотек

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.stats import ttest_ind

# Подготовка функций

def clean_func(data):
    """Функция для замены значения ячеек 'nan' на 'None' для столбцов типа 'object'
    и на наиболее часто встречающееся значение для столбцов типа 'int' и 'float'"""
    
    clear_data = pd.DataFrame()
    for col in data.iteritems():
        if col[1].dtypes == 'object':
            temp_s = col[1].where(pd.notnull(col[1]), None)
            clear_data = pd.concat([clear_data, temp_s], axis=1)
        else:
            temp_s = col[1].replace({np.nan: col[1].value_counts().index[0]})
            clear_data = pd.concat([clear_data, temp_s], axis=1)
            
    return clear_data


def get_distplot(data, column):
    """Функция для создания графиков distplot"""
    
    fig, ax = plt.subplots(figsize = (8, 4))
    sns.distplot(data[column])
    plt.show()
 
    
def anomaly_del_func(data):
    """Функция для удаления выбросов. 
    Возвращает маску, с помощью которой можно удалить выбросы"""
    
    iqr = data.quantile(0.75) - data.quantile(0.25)
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    mask = data.between(q1 - 1.5*iqr, q3 + 1.5*iqr)
    
    return mask

    
def get_boxplot(data, column):
    """Функция для создания графиков boxplot"""
    
    fig, ax = plt.subplots(figsize = (8, 4))
    sns.boxplot(x = column, y = 'score', data = data, ax=ax)
    plt.xticks(rotation = 45)
    plt.show()


def get_pointplot(data, column):
    """Функция для создания графиков pointplot"""
    
    fig, ax = plt.subplots(figsize = (6, 3))
    sns.pointplot(x = column, y = 'score', data = data, capsize = 0.2)
    plt.show()
    

def get_stat_dif(data, column):
    """Функция для расчета p_value критерия Стьюдента
    Печатает имена колонок со статистически значимыми различиями, 
    p_value для этих колонок, возвращает сами колонки"""
    
    col = data[column].value_counts().index
    combinations_all = list(combinations(col, 2))
    for comb in combinations_all:
        if ttest_ind(data[data[column] == comb[0]].score,
                     data[data[column] == comb[1]].score).pvalue \
            <= 0.05/len(combinations_all):
            print('Найдены статистически значимые различия для колонки', column)
            print('p =', ttest_ind(data[data[column] == comb[0]].score, 
                                       data[data[column] == comb[1]].score).pvalue)
            return column
            break
   
            
# Чтение и очистка датасета от пустых ячеек и выбросов

study_data = pd.read_csv("C:\\Python_test\\stud_math.xls")
study_data = clean_func(study_data)

study_data = study_data[anomaly_del_func(study_data.age)]
study_data = study_data[anomaly_del_func(study_data.Fedu)]
study_data = study_data[anomaly_del_func(study_data.absences)]


# Создание списков с именами столбцов разных типов
columns_list = study_data.columns
quant_columns_list = []
nom_columns_list = []

for item in columns_list:
    if study_data[item].dtype != 'object':
        quant_columns_list.append(item)
    else:
        nom_columns_list.append(item)


# Печать гистограмм для количественных столбцов
for col in quant_columns_list:
    get_distplot(study_data, col)

    
# Печать матрицы корреляций
plt.figure(figsize = (16,6))
sns.heatmap(study_data.corr(), annot = True, cmap = 'coolwarm', linewidths = 0.5)


# Удаление коррелирующих переменных
study_data.drop(['studytime, granular'], inplace = True, axis = 1)


# Печать уникальных значений для номинативных переменных
for item in nom_columns_list:
    count_info = study_data[item].value_counts()
    print(count_info)


# Печать boxplot и pointplot для номинативных переменных
for col in nom_columns_list:
    get_boxplot(study_data, col)
    
for col in nom_columns_list:
    get_pointplot(study_data, col)


# Проверка на статистическую значимость по критерию Стьюдента номинативных переменных
# Формирование списка с именами переменных для использования в построении модели
output_columns = []
for col in nom_columns_list:
    output_columns.append(get_stat_dif(study_data, col))

output_columns = list(filter(None, output_columns)) 
output_columns = output_columns + quant_columns_list


# Датасет для дальнейшего построения модели
study_data_for_model = study_data[output_columns]
