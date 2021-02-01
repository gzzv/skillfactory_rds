# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 20:45:45 2021

@author: Ildar
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_selection import f_classif, mutual_info_classif
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import confusion_matrix, auc, roc_auc_score, roc_curve
from sklearn.metrics import recall_score, precision_score, f1_score, log_loss
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA


# Инициализация функций
def fill_by_dist(x):
    """Функция для заполнения пропусков в соответствии с распределнием значений"""
    isnull = x.isnull()
    sample = x.dropna().sample(isnull.sum(), replace=True).values
    output = x.loc[isnull] = sample
    return output

def fill_by_mode(x):
    """Фукция для заполнения пропусков модой"""
    return x.fillna(x.mode()[0])


# Загрузка данных
test = pd.read_csv('test.csv', encoding = 'ISO-8859-1', low_memory = False)
train = pd.read_csv('train.csv', encoding = 'ISO-8859-1', low_memory = False)
sample_submission = pd.read_csv('sample_submission.csv', encoding = 'ISO-8859-1', 
                                low_memory = False)
RANDOM_SEED = 42


# Объединение тестовых и тренировочных данных для совместной обработки
train['sample'] = 1 # пометим тренировочные данные
test['sample'] = 0 # пометим тестовые данные
test['default'] = 0 # в тестовые данные добавим целевой признак
data = test.append(train, sort=False).reset_index(drop=True) # объеденим данные


# Заполнение пропусков
data.isnull().sum()
fill_by_dist(data['education'])


# Добавление новых фичей
data['app_date'] = pd.to_datetime(data['app_date'])
data['app_date'] = (pd.to_datetime('today') - data['app_date']).dt.days
data['bki_req_to_age'] = data['bki_request_cnt']/data['age']
data['bki_to_date'] = data['score_bki']/data['app_date']
data['age_2'] = data['age']**2
data['age_to_date'] = data['age']/data['app_date']
data['app_date3'] = data['app_date']**3


# Создание списков с именами колонок для дальнейшей обработки
bin_cols = ['sex', 'car', 'car_type', 'foreign_passport', 'good_work']
cat_cols = ['education', 'home_address', 'work_address', 'sna', 'first_time', 
            'region_rating']
num_cols = ['app_date', 'age', 'decline_app_cnt', 'score_bki', 'bki_request_cnt', 
            'income', 'bki_req_to_age', 'bki_to_date', 'age_2', 'age_to_date', 
            'app_date3']


# Удаление выбросов
for i in num_cols:
    plt.figure()
    sns.boxplot(x=data['default'], y=data[i], data=data)
    plt.title(i)
    plt.show()


# Логарифмирование некоторых признаков
data['age'] = np.log(data['age'])
data['decline_app_cnt'] = np.log(data['decline_app_cnt']+1)
data['bki_request_cnt'] = np.log(data['bki_request_cnt']+1)
data['income'] = np.log(data['income']+1)
data['bki_req_to_age'] = np.log(data['bki_req_to_age']+1)
data['app_date'] = np.log(data['app_date'])


# Преобразование бинарных признаков с помощью label encoder
label_encoder = LabelEncoder()
for column in bin_cols:
    data[column] = label_encoder.fit_transform(data[column])


# Преобразование признака 'education' с помощью ordinal encoder
ordinal_encoder = OrdinalEncoder(categories=[data['education'].value_counts().index])
data[['education']] = ordinal_encoder.fit_transform(data[['education']])


# Преобразование категориальных признаков с помощью one hot encoder
one_hot_encoder = OneHotEncoder(sparse = False)
X_cat = one_hot_encoder.fit_transform(data[cat_cols].values)
X_cat = pd.DataFrame(X_cat, columns = one_hot_encoder.get_feature_names())


# Нормализация числовых признаков
X_num = StandardScaler().fit_transform(data[num_cols])
X_num = pd.DataFrame(X_num, columns = num_cols)


# Объединение в один DataFrame
df = pd.concat([data['client_id'].reset_index(drop=True), X_num, 
                data[bin_cols].reset_index(drop=True), X_cat, 
                data['default'].reset_index(drop=True), 
                data['sample'].reset_index(drop=True)], axis=1)


# Снижение дисбаланса выборки
sns.countplot(train['default'])


# Подготовка данных к машинному обучению
df_train = df.query('sample == 1').drop(['sample'], axis=1)
df_test = df.query('sample == 0').drop(['sample'], axis=1)
X = df_train.drop(['client_id', 'default'], axis=1)
y = df_train['default']


# Снижение размерности
pca = PCA(n_components=37, random_state=RANDOM_SEED)
X = pca.fit_transform(X)

# Разделение на тренировочные и валидационные данные
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=RANDOM_SEED, 
                                                    shuffle=True)


# Обучение модели
model = LogisticRegression(penalty='l2', C=1, max_iter=800)
model.fit(X_train, y_train)


# Оценка точности предсказаний
probs = model.predict_proba(X_test)
y_pred = model.predict(X_test)

probs = probs[:, 1]

fpr, tpr, threshold = roc_curve(y_test, probs)
roc_auc = roc_auc_score(y_test, probs)
f1 = f1_score(y_test, y_pred)
acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)


# Визуализация ROC AUC
plt.figure()
plt.plot([0, 1], label='Baseline', linestyle='--')
plt.plot(fpr, tpr, label='Regression')
plt.title('Logistic Regression ROC AUC = %0.3f' % roc_auc)
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')
plt.legend(loc='lower right')
plt.show()
print(roc_auc)


# Подготовка submission
X_sub = df_test.drop(['client_id', 'default'], axis=1)
X_sub = pca.fit_transform(X_sub)
predict_submission = model.predict_proba(X_sub)
predict_submission[:, 1]