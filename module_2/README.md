# module_2
## Задача проекта 
  Изучение и проведение разведоватьельного анализа данных, получение навыков по обработке данных, построению графиков, отбора параметров модели

## Описание данных
  Исходный датасет содержит данные об условиях жизни и обучения, родителях и успеваемости по математике учащихся в возрасте от 15 до 22.
  
## Этапы работы
  - **Очистка данных от пустых ячеек**
    
    Загруженные данные содержат ячейки со значением 'nan' для количественных (int64 и float) и номинативных (object) переменных. 
    Для очистки этих ячеек применялась функция, которая заменяет 'nan' на 'None' для номинативных переменны и заменяет 'nan' на наиболее часто встречающееся значение для   количественных переменных.
  
  - **Удаление выбросов количественных переменных**
    
    Некоторые количественные переменные содержат выбросы:
    
    * age
    
    ![age hist](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_age.png/)
    
    * Fedu
    
    ![Fedu hist](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_Fedu.png/)
    
    * absences
    
    ![absences hist](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_absences.png/)
    
    
    Выбросы в этих переменных можно выявить и удалить с помощью квартилей и межквартильного размаха.
  
  - **Корреляционный анализ**
  
  Построим матрицу корреляций для количественных переменных
  
  ![corr matrix](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_corr_matrix.png/)
  
  Из матрицы видно, что переменные 'studytime' и 'studytime, granular' коррелируют между собой. Поэтому можно удалить переменную 'studytime, granular'. Также глядя на матрицу можно сделать вывод, 
  что переменные 'traveltime', 'famrel', 'freetime' мало коррелируют с оценкой по математике. Эти переменные можно не включать в итоговую таблицу для дальнейшего использования в построении модели.  
  
  - **Выявление номинативных переменных, влияющих на оценку по математике**
  
  Среди номинативных переменных только 'Pstatus', 'Mjob', 'Fjob', 'reason' имеют более 2 уникальных значений.
  
  Анализ графиков boxplot и pointplot, а также критерия Стьюдента номинативных переменных показал, что переменные 'sex' (p = 0.027), 'address' (p = 0.009), 'Mjob' (p = 0.001),
'paid' (p = 0.039), 'higher' (p = 0.0004), 'romantic (p = 0.007)' оказывают наибольшее влияние на переменную 'score'

  * sex
  
  ![sex boxplot](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_sex.png/)
  ![sex pointplot](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_sex_pointplot.png/)
  
  * address
  
  ![address boxplot](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_address.png/)
  ![address pointplot](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_address_pointplot.png/)
  
  * Mjob
  
  ![Mjob boxplot](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_Mjob.png/)
  ![Mjob pointplot](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_Mjob_pointplot.png/)
  
  * paid
  
  ![paid boxplot](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_paid.png/)
  ![paid pointplot](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_paid_pointplot.png/)
  
  * higher
  
  ![higher boxplot](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_higherpng/)
  ![higher pointplot](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_higher_pointplot.png/)
  
  * romantic
  
  ![romantic boxplot](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_romantic.png/)
  ![romantic pointplot](https://github.com/gzzv/skillfactory_rds/raw/master/screenshots/module_2_romantic_pointplot.png/)
  
  - **Выводы**
  
  Разведовательный анализ данных об условиях жизни учащихся покзал, что не все переменные оказывают значимое влияние на оценку по математике. Список самых важных переменных, 
  которые решено оставить для дальнейшего использования: 'sex', 'address', 'Mjob', 'paid', 'higher', 'romantic', 'age', 'health', 'absences', 'Medu', 'goout', 'failures',
 'Fedu', 'studytime', 'score'

### Вопросы саморефлексии:
1. Какова была ваша роль в команде?

  Я работал над проектом один

2. Какой частью своей работы вы остались особенно довольны?

  Изучил способы оценки статистических различий по критерию Стьюдента, возможность графического изображения этой значимости с помощью seaborn.pointplot()

3. Что не получилось сделать так, как хотелось? Над чем ещё стоит поработать?

  Считаю, что глобально получилось сделать проект как ожидал, в будущем стоит изучить способы уменьшения числа количественных параметров модели

4. Что интересного и полезного вы узнали в этом модуле?

  Способы очистки данных от выбросов, оценки статистических различий

5. Что является вашим главным результатом при прохождении этого проекта?

  Подкрепление полученных ранее навыков по работе с библиотекой pandas, использование библиотеки seaborn для построение графиков

6. Какие навыки вы уже можете применить в текущей деятельности?

  Навык предобработки данных, нахождения выбросов, нулевых и пустых ячеек, оценки статистически обоснованных различий по критерию Стьюдента

7. Планируете ли вы дополнительно изучать материалы по теме проекта?

  Обязательно
