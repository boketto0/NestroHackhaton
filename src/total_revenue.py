"""
Модуль рассчитывает среднюю прибыль на заправке
"""
import pandas as pd
import numpy as np


def calculate_fuel_revenue(clients_data_file_path="data/clients/road_best_place.xlsx",
                            data_traffic_file_path="data/origin/cars_length_procent.xlsx",
                            data_fuel_file_path="data/origin/fuel.xlsx",
                            data_output_file="data/revenue/total_revenue.xlsx"):
    """
        Функция рассчитывает прибыль заправок от реализации топлива

        Args:
            clients_data_file_path (str): путь к excel файлу с данными о количестве клиентов на заправке.
                'Номер' - номер дороги
                'Название' - название дороги,
                'clients' - кол-во клиентов на заправке.

            data_traffic_file_path (str):
                '< 5,5 m', '5,5 - 12 m', '12 - 16,5 m', '> 16,5 m' - трафик на дороге
                по соответствующим длинам кузова в процентах.

            data_fuel_file_path (str):
                '95, euro', 'Deisel, euro' - стоимость 95 бензина и дизеля в евро для каждой заправки.

            data_output_file (str):
             путь к excel файлу с выходными данными


        Returns:
            запись в файл данные с прибылью для всех предоставленных заправок
    """
    # чтение данных
    data = pd.read_excel(clients_data_file_path)
    data_traffic = pd.read_excel(data_traffic_file_path)
    data_fuel = pd.read_excel(data_fuel_file_path)

    # расчет типов машин клиентов на завправках
    data['< 5,5 m'] = np.int32(data_traffic['< 5,5 m'] * data['clients'])
    data['5,5 - 12 m'] = np.int32(data_traffic['5,5 - 12 m'] * data['clients'])
    data['12 - 16,5 m'] = np.int32(data_traffic['12 - 16,5 m'] * data['clients'])
    data['> 16,5 m'] = np.int32(data_traffic['> 16,5 m'] * data['clients'])

    # средний обьем бака авто с разной длиной кузова
    tankV55 = 45
    tankV5_12 = 75
    tankV12_16 = 250
    tankV16 = 1000

    # расчет прибыли
    # от реализации топлива
    revenue = ((data['< 5,5 m'] * tankV55 + data['5,5 - 12 m'] * tankV5_12) * data_fuel['95, euro'] +
                    (data['12 - 16,5 m'] * tankV12_16 + data['> 16,5 m'] * tankV16) * data_fuel['Diesel, euro'])*0.9

    data_output = pd.DataFrame()
    data_output['Номер'] = data['Номер']
    data_output['Название'] = data['Название']
    data_output['Доход от реализации топлива, евро'] = revenue

    data_output.to_excel(data_output_file, index=False)


def calculate_DAS_revenue(clients_data_file_path="data/clients/road_best_place.xlsx",
                          best_place_data_file_path="data/clients/road_best_place.xlsx",
                          supemarket_cafe_data_file_path="data/origin/cafe_supermarket.xlsx",
                          data_das_file_path="data/origin/das.xlsx",
                          data_output_file="data/revenue/total_revenue.xlsx"):
    """
        Функция рассчитывает прибыль заправок от ДАС
    Args:
        clients_data_file_path: путь к excel файлу с данными о количестве клиентов на заправке.
        best_place_data_file_path: путь к excel файлу с данными о расположении заправок
        supemarket_cafe_data_file_path: путь к excel файлу с данными о расположении супермаркетов и кафе конкурентов
        data_das_file_path: путь к excel файлу с данными о средней прибыли от ДАС в этом районе
        data_output_file: путь к excel файлу с выходными данными
    Returns:

    """

    data = pd.read_excel(clients_data_file_path)
    data_supermarket_cafe = pd.read_excel(supemarket_cafe_data_file_path)
    data_best_place = pd.read_excel(best_place_data_file_path)
    data_das = pd.read_excel(data_das_file_path)
    data_total_rev = pd.read_excel(data_output_file)

    data_best_place['best_place'] = data_best_place['best_place'].apply(
        lambda x: tuple(float(i) for i in x.strip("()").split(", ")) if isinstance(x, str) else (0, 0))

    r_distance = 3 #km - радиус, внутри которого учитываем конкурентов
    rating_max = 5 # максимальный рейтинг магазина/кафешки
    param_model = 2
    feedback_n = max(data_supermarket_cafe['user_ratings_total'])

    shopping_malls_cafe = []  # список магазинов и кафешек рядом с каждой заправкой
    best_place_lat = data_best_place['best_place'].apply(lambda x: x[0] if isinstance(x, tuple) else 0)
    best_place_lon = data_best_place['best_place'].apply(lambda x: x[1] if isinstance(x, tuple) else 0)

    for ind, place in data_best_place.iterrows():
        shopping_malls_cafe.append(data_supermarket_cafe[(data_supermarket_cafe['lat'] - place['best_place'][0])**2 +
                                                         (data_supermarket_cafe['lon'] - place['best_place'][1])**2 < r_distance / 6400.]['name'].values)

    probability = []
    for station_num in range(len(shopping_malls_cafe)):
        sum = 0
        num = len(shopping_malls_cafe[station_num])
        for cafe_name in shopping_malls_cafe[station_num]:
            cafe = data_supermarket_cafe.loc[data_supermarket_cafe['name'] == cafe_name]
            l_norm = 6400. * ((best_place_lat[station_num] - cafe['lat'])**2 + (best_place_lon[station_num] - cafe['lon'])**2) / r_distance
            l_norm = l_norm.iloc[0]
            rating_norm = (cafe['rating'] / rating_max).iloc[0]
            feedback_norm = (cafe['user_ratings_total'] / feedback_n).iloc[0]
            sum += rating_norm * feedback_norm / l_norm
        if num:
            sum = sum / num

        probability.append(1 - sum)

    probability = np.array(probability)
    probability[probability <= 0.] = 0.1
    probability[probability >= 1.] = 0.9

    revenue = param_model * probability * data['clients'] * data_das['средний чек на ДАС в районе']


    data_total_rev['Доход от ДАС, евро'] = revenue

    data_total_rev.to_excel(data_output_file, index=False)


def calculate_fuel_revenue_Nestro(clients_data_file_path="data/clients/NestroStations.xlsx",
                           data_traffic_file_path="data/origin/cars_length_procent_NestroStations.xlsx",
                           data_fuel_file_path="data/origin/fuel_NestroStations.xlsx",
                           data_output_file="data/revenue/total_revenue_NestroStations.xlsx"):
    """
        Функция рассчитывает прибыль заправок от реализации топлива для существующих заправок Nestro

        Args:
            clients_data_file_path (str): путь к excel файлу с данными о количестве клиентов на заправке.
                'Номер' - номер дороги
                'Название' - название дороги,
                'clients' - кол-во клиентов на заправке.

            data_traffic_file_path (str):
                '< 5,5 m', '5,5 - 12 m', '12 - 16,5 m', '> 16,5 m' - трафик на дороге
                по соответствующим длинам кузова в процентах.

            data_fuel_file_path (str):
                '95, euro', 'Deisel, euro' - стоимость 95 бензина и дизеля в евро для каждой заправки.

            data_output_file (str):
             путь к excel файлу с выходными данными


        Returns:
            запись в файл данные с прибылью для всех предоставленных заправок
    """
    # чтение данных
    data = pd.read_excel(clients_data_file_path)
    data_traffic = pd.read_excel(data_traffic_file_path)
    data_fuel = pd.read_excel(data_fuel_file_path)

    # расчет типов машин клиентов на завправках
    data['< 5,5 m'] = np.int32(data_traffic['< 5,5 m'] * data['clients'])
    data['5,5 - 12 m'] = np.int32(data_traffic['5,5 - 12 m'] * data['clients'])
    data['12 - 16,5 m'] = np.int32(data_traffic['12 - 16,5 m'] * data['clients'])
    data['> 16,5 m'] = np.int32(data_traffic['> 16,5 m'] * data['clients'])

    # средний обьем бака авто с разной длиной кузова
    tankV55 = 45
    tankV5_12 = 75
    tankV12_16 = 250
    tankV16 = 1000

    # расчет прибыли
    # от реализации топлива
    revenue = ((data['< 5,5 m'] * tankV55 + data['5,5 - 12 m'] * tankV5_12) * data_fuel['95, euro'] +
                    (data['12 - 16,5 m'] * tankV12_16 + data['> 16,5 m'] * tankV16) * data_fuel['Diesel, euro'])*0.9

    data_output = pd.DataFrame()
    data_output['Номер'] = data['Номер']
    data_output['Название'] = data['Название']
    data_output['Доход от реализации топлива, евро'] = revenue

    data_output.to_excel(data_output_file, index=False)


def calculate_DAS_revenue_Nestro(clients_data_file_path="data/clients/NestroStations.xlsx",
                          best_place_data_file_path="data/clients/NestroStations.xlsx",
                          supemarket_cafe_data_file_path="data/origin/cafe_supermarket.xlsx",
                          data_das_file_path="data/origin/das_NestroStations.xlsx",
                          data_output_file="data/revenue/total_revenue_NestroStations.xlsx"):
    """
        Функция рассчитывает прибыль заправок от ДАС для существующих заправок Nestro
    Args:
        clients_data_file_path: путь к excel файлу с данными о количестве клиентов на заправке.
        best_place_data_file_path: путь к excel файлу с данными о расположении заправок
        supemarket_cafe_data_file_path: путь к excel файлу с данными о расположении супермаркетов и кафе конкурентов
        data_das_file_path: путь к excel файлу с данными о средней прибыли от ДАС в этом районе
        data_output_file: путь к excel файлу с выходными данными
    Returns:

    """

    data = pd.read_excel(clients_data_file_path)
    data_supermarket_cafe = pd.read_excel(supemarket_cafe_data_file_path)
    data_best_place = pd.read_excel(best_place_data_file_path)
    data_das = pd.read_excel(data_das_file_path)
    data_total_rev = pd.read_excel(data_output_file)

    # data_best_place['best_place'] = data_best_place['best_place'].apply(
    #     lambda x: tuple(float(i) for i in x.strip("()").split(", ")) if isinstance(x, str) else (0, 0))

    data_best_place['best_place'] = data_best_place[['lat', 'lon']].apply(tuple, axis=1)

    r_distance = 3 #km - радиус, внутри которого учитываем конкурентов
    rating_max = 5 # максимальный рейтинг магазина/кафешки
    param_model = 2
    feedback_n = max(data_supermarket_cafe['user_ratings_total'])

    shopping_malls_cafe = []  # список магазинов и кафешек рядом с каждой заправкой
    best_place_lat = data_best_place['best_place'].apply(lambda x: x[0] if isinstance(x, tuple) else 0)
    best_place_lon = data_best_place['best_place'].apply(lambda x: x[1] if isinstance(x, tuple) else 0)

    for ind, place in data_best_place.iterrows():
        shopping_malls_cafe.append(data_supermarket_cafe[(data_supermarket_cafe['lat'] - place['best_place'][0])**2 +
                                                         (data_supermarket_cafe['lon'] - place['best_place'][1])**2 < r_distance / 6400.]['name'].values)

    probability = []
    for station_num in range(len(shopping_malls_cafe)):
        sum = 0
        num = len(shopping_malls_cafe[station_num])
        for cafe_name in shopping_malls_cafe[station_num]:
            cafe = data_supermarket_cafe.loc[data_supermarket_cafe['name'] == cafe_name]
            l_norm = 6400. * ((best_place_lat[station_num] - cafe['lat'])**2 + (best_place_lon[station_num] - cafe['lon'])**2) / r_distance
            l_norm = l_norm.iloc[0]
            rating_norm = (cafe['rating'] / rating_max).iloc[0]
            feedback_norm = (cafe['user_ratings_total'] / feedback_n).iloc[0]
            sum += rating_norm * feedback_norm / l_norm
        if num:
            sum = sum / num

        probability.append(1 - sum)

    probability = np.array(probability)
    probability[probability <= 0.] = 0.1
    probability[probability >= 1.] = 0.9

    revenue = param_model * probability * data['clients'] * data_das['средний чек на ДАС в районе']


    data_total_rev['Доход от ДАС, евро'] = revenue

    data_total_rev['lat'] = data_best_place['lat']
    data_total_rev['lon'] = data_best_place['lon']

    data_total_rev.to_excel(data_output_file, index=False)


def calculate_total_revenue():
    """
        Функция запуска расчета прибыли заправки
    """
    calculate_fuel_revenue()
    calculate_DAS_revenue()

    calculate_fuel_revenue_Nestro()
    calculate_DAS_revenue_Nestro()
