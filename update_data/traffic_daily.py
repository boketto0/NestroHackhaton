import json
from datetime import datetime

import pandas as pd
import googlemaps
from apscheduler.schedulers.blocking import BlockingScheduler


# Вставьте ваш API-ключ Google Maps
api_key = "AIzaSyCjgcE4I9N0VYO9nTA2XHBgaoeM6Glnzww"

# Создайте клиент Google Maps
gmaps = googlemaps.Client(key=api_key)


def traffic_coef(start_point, end_point):
    # Получите информацию о загруженности дороги между двумя точками
    directions_result = gmaps.directions(start_point, end_point, departure_time="now", traffic_model="best_guess")
    pretty_json = json.dumps(directions_result, indent=4)

    # Получите значение коэффициента загруженности дороги
    time_without = directions_result[0]['legs'][0]['duration_in_traffic']['value']
    time_with = directions_result[0]['legs'][0]['duration']['value']

    k = time_without / time_with

    # Возвращаем значение коэффициента загруженности дороги
    return k


def catch_traffic_now():
    """
    Функция catch_traffic_now работает на платформе Replit в течение 24 часов. Она собирает 24 коэффициента
    загруженности дорог с помощью Google Maps API. Затем эти коэффициенты суммируются и умножаются на среднее количество
    полос на исследуемом участке дороги .
    Далее данные относительно трафика за 2016 год используются для нормирования полученных значений и получается
    файл 'traffic_daily.xlsx'. Таким образом, данные о трафике актуализируются и улучшаются. Этот процесс может быть
    постоянным, что позволяет постепенно расширять и улучшать датасет о трафике."""

    time = str(datetime.now().strftime("%Y-%m-%d %H:%M"))

    # Указываем путь к файлу Excel
    file_path = 'data/origin/replit.xlsx'

    # Читаем файл Excel и сохраняем данные в переменную df (DataFrame)
    df = pd.read_excel(file_path)

    # Получаем первую колонку из DataFrame
    number_column = df.iloc[0:, 0]  # номер
    name_column = df.iloc[0:, 1]  # название
    origin_coords_column = df.iloc[0:, 2]  # coords start
    destination_coords_column = df.iloc[0:, 3]  # coords end

    number = []
    name = []
    coefs = []

    for i in range(len(number_column)):
        lat_start, lng_start = map(float, origin_coords_column.iloc[i].split(','))
        lat_end, lng_end = map(float, destination_coords_column.iloc[i].split(','))
        k = traffic_coef(start_point=(lat_start, lng_start), end_point=(lat_end, lng_end))
        number.append(number_column.iloc[i])
        name.append(name_column.iloc[i])
        coefs.append(k)


    # Создаем новый DataFrame с первой колонкой
    new_df = pd.DataFrame({'Номер': number,
                           'Название': name,
                           'Коэфф': coefs})

    # Сохраняем новый DataFrame в файл Excel
    new_file_path = f'data/origin/coefs_trafic{time}.xlsx'
    new_df.to_excel(new_file_path, index=False)

    print(f'Новая таблица успешно создана и сохранена в файле {new_file_path}.')

