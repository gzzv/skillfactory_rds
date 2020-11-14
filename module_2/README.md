# module_2
## Задача проекта 
  Изучение и проведение разведоватьельного анализа данных, получение навыков по обработке данных, построению графиков, отбора параметров модели

## Описание данных
  Исходный датасет содержит данные об условиях жизни и обучения, родителях и успеваемости по математике учащихся в возрасте от 15 до 22.
  
## Этапы работы
  - Загрузка требуемых библиотек
  ```sh
  import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.stats import ttest_ind
```

  - Подготовка функций для обработки данных
    ```sh
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
```
  


- Вопросы саморефлексии:
1. Какова была ваша роль в команде?
Я работал над проектом один
2. Какой частью своей работы вы остались особенно довольны?
Изучил способы оценки статистических различий по критерию Стьюдента, возможность графического изображения этой значимости с помощью seaborn.pointplot()
3. Что не получилось сделать так, как хотелось? Над чем ещё стоит поработать?
Считаю, что глобально получилось сделать проект как ожидал, в будущем стоит изучить способы уменьшения числа количественных параметров модели
4. Что интересного и полезного вы узнали в этом модуле?
Способы очистки данных от выбросов, оценки статистических различий
5. Что является вашим главным результатом при прохождении этого проекта?
Подкрепление полыченных ранее навыков по работе с библиотекой pandas, применение возможностей библиотеки seaborn для построение графиков
6. Какие навыки вы уже можете применить в текущей деятельности?
Навык предобработки данных, нахождения выбросов, нулевых и пустых ячеек, оценки статистически обоснованных различий по критерию Стьюдента
7. Планируете ли вы дополнительно изучать материалы по теме проекта?
Обязательно
