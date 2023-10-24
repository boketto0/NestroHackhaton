import googlemaps
import polyline
import pandas as pd


def update_roads():
    # Вставьте ваш API-ключ Google Maps
    api_key = 'AIzaSyBDKQ4aPOVR7rxRgl2ut_vZTJjJBCBCbEs'

    # Создайте экземпляр клиента Google Maps
    gmaps = googlemaps.Client(key=api_key)

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
    origin_coords = []
    destination_coords = []
    roads_coords = []

    for i in range(len(number_column)):
        origin_str = origin_coords_column.iloc[i]
        destination_str = destination_coords_column.iloc[i]

        # Разделяем строку по запятой и преобразуем каждую часть в число
        latitude_origin, longitude_origin = map(float, origin_str.split(','))
        latitude_destination, longitude_destination = map(float, destination_str.split(','))

        origin = (latitude_origin, longitude_origin)
        destination = (latitude_destination, longitude_destination)

        directions_result = gmaps.directions(origin, destination, mode="driving")
        d = directions_result[0]['legs'][0]['steps'][0]['polyline']['points']  # 'polyline'
        t = polyline.decode(d, 5)
        number.append(number_column.iloc[i])
        name.append(name_column.iloc[i])
        origin_coords.append(origin_coords_column.iloc[i])
        destination_coords.append(destination_coords_column.iloc[i])
        print(t)
        roads_coords.append(t)

    # Создаем новый DataFrame с первой колонкой
    new_df = pd.DataFrame({'Номер': number,
                           'Название': name,
                           'origin_coords': origin_coords,
                           'destination_coords': destination_coords,
                           'roads_coords': roads_coords})

    # Сохраняем новый DataFrame в файл Excel
    new_file_path = 'data/origin/roads.xlsx'
    new_df.to_excel(new_file_path, index=False)

    print(f'Новая таблица успешно создана и сохранена в файле {new_file_path}.')



