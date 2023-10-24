import time
import pandas as pd
import googlemaps
import requests


def is_in_bosnia(lat, lng):
    gmaps = googlemaps.Client(key="AIzaSyCjgcE4I9N0VYO9nTA2XHBgaoeM6Glnzww")  # Замените YOUR_API_KEY на ваш ключ API Google Maps

    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))

    for result in reverse_geocode_result:
        for component in result['address_components']:
            if 'country' in component['types'] and component['long_name'] == 'Bosnia and Herzegovina':
                return True

    return True


def get_car_dealer_rental_repair_wash(adress: str, LAT: list):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": adress,
        "radius": 50000,
        "type": ["car_dealer", "car_rental", "car_repair", "car_wash"],
        "key": "AIzaSyCjgcE4I9N0VYO9nTA2XHBgaoeM6Glnzww"
    }

    response = requests.get(url, params=params)
    car_dealer_rental_repair_wash = []

    data = response.json()

    for result in data['results']:
        name = result['name']
        lat = result['geometry']['location']['lat']
        lng = result['geometry']['location']['lng']
        try:
            rating = result['rating']
            user_ratings_total = result['user_ratings_total']
        except:
            rating = None
            user_ratings_total = None

        if is_in_bosnia(lat=lat, lng=lng) and rating is not None and (lat, lng) not in LAT:
            LAT.append((lat, lng))
            car_dealer_rental_repair_wash.append(
                {'name': name, 'lat': lat, 'lng': lng, 'rating': rating, 'user_ratings_total': user_ratings_total})

    counter = 0
    # Обработайте ответ API и извлеките координаты и названия заправок
    while 'next_page_token' in data and counter < 5:
        counter+=1
        time.sleep(0.2)
        next_page_token = data['next_page_token']
        params = {
            "key": "AIzaSyCjgcE4I9N0VYO9nTA2XHBgaoeM6Glnzww",
            'pagetoken': next_page_token,
        }

        response = requests.get(url, params=params)
        data = response.json()

        for result in data['results']:
            name = result['name']
            lat = result['geometry']['location']['lat']
            lng = result['geometry']['location']['lng']
            try:
                rating = result['rating']
                user_ratings_total = result['user_ratings_total']
            except:
                rating = None
                user_ratings_total = None

            #проверяем условие точки
            if is_in_bosnia(lat=lat, lng=lng) and rating is not None and user_ratings_total > 5 and (lat, lng) not in LAT:
                LAT.append((lat, lng))
                car_dealer_rental_repair_wash.append(
                    {'name': name, 'lat': lat, 'lng': lng, 'rating': rating, 'user_ratings_total': user_ratings_total})

    return [car_dealer_rental_repair_wash, LAT]


# Вызовите функцию для получения списка заправок
def update_car_dealer_rental_repair_wash():
    # Указываем путь к файлу Excel
    file_path_lat = 'data/origin/latlonNestroStations.xlsx'

    # Читаем файл Excel и сохраняем данные в переменную df           uv(DataFrame)
    df_lat = pd.read_excel(file_path_lat)

    # Получаем колонки из DataFrame
    lat_column = df_lat.iloc[0:, 2]  # lat
    lon_column = df_lat.iloc[0:, 3]  # lon

    # формируем список для прогона
    list_adress = []
    for i in range(len(lat_column)):
        list_adress.append(str(lat_column.iloc[i]) + ", " + str(lon_column.iloc[i]))

    #list_adress = ['43.842315, 18.254834', '45.052381, 17.307831', '44.622637, 17.370599', '44.320866, 16.937977', '44.419015, 17.048408', '44.872041, 17.332149', '44.489545, 16.923317', '44.821766, 17.196404', '45.096755, 17.513176', '44.903194, 17.29847', '44.768788, 19.225582', '44.739508, 19.180843', '44.784767, 17.204405', '44.652869, 19.242527', '44.814907, 19.268933', '44.692531, 19.031705', '44.631771, 18.842966', '44.371438, 19.101828', '44.409277, 19.12412', '44.291826, 18.845654', '44.185632, 19.332315', '44.116629, 19.289541', '44.183461, 18.946396', '43.161633, 18.542569', '44.174384, 19.07561', '45.134846, 17.996191', '45.147398, 18.003667', '44.728593, 18.088819', '44.727753, 18.091505', '44.9713, 18.2765', '44.957807, 18.30811', '44.91386, 18.640417', '44.633948, 18.362347', '44.985448, 17.941826', '44.775561, 17.206755', '44.862286, 17.669804', '44.620661, 17.854182', '44.607583, 17.850869', '45.053925, 18.478658', '43.814066, 18.575143', '43.85079, 18.538614', '43.851092, 18.538386', '43.825851, 18.370387', '43.91808, 18.767319', '43.812846, 18.997463', '44.77922, 17.196727', '43.789731, 19.292382', '43.611036, 19.367466', '43.557375, 19.073298', '44.094532, 18.95662', '43.932621, 18.790917', '43.691413, 19.087637', '44.979719, 16.714964', '45.178908, 16.80244', '44.979176, 16.720097', '45.048762, 16.385818', '44.746573, 17.155061', '45.221632, 16.52349', '44.851895, 16.676274', '44.972935, 16.834951', '45.207291, 16.877914', '43.256243, 18.116985', '42.948048, 18.09414', '43.497547, 18.767348', '43.51, 18.644094', '42.873076, 18.424401', '42.709961, 18.346192', '44.774165, 17.181917', '42.701798, 18.348586', '43.511809, 18.77906', '44.814064, 18.552236', '44.108284, 17.431352', '44.556493, 18.693714', '44.127732, 17.886227', '44.638782, 17.973634', '43.839405, 17.174661', '44.72436, 18.201796', '44.629198, 18.560672', '44.811729, 17.21171', '44.784175, 18.515896', '43.39385, 17.86903', '45.143649, 17.255218', '44.9090978, 17.0225537', '45.1766639, 16.7949789', '44.7613835, 19.2060944', '43.9295946, 18.3317267', '44.6336947, 17.9756766', '44.828841, 17.209831']
    #list_adress = ['43.842315, 18.254834', '43.842315, 18.254834', '45.052381, 17.307831']
    lat = []
    car_dealer_rental_repair_washes = []

    for adress in list_adress:
        car_dealer_rental_repair_wash_result = get_car_dealer_rental_repair_wash(adress, lat)
        lat = car_dealer_rental_repair_wash_result[1]
        car_dealer_rental_repair_washes.extend(car_dealer_rental_repair_wash_result[0])
        print("len", len(car_dealer_rental_repair_washes))


    name = []
    latt = []
    lngg = []
    ratingg = []
    user_rat = []

    for diction in car_dealer_rental_repair_washes:
        name.append(diction['name'])
        latt.append(diction['lat'])
        lngg.append(diction['lng'])
        ratingg.append(diction['rating'])
        user_rat.append(diction['user_ratings_total'])


    # Создаем новый DataFrame с первой колонкой
    new_df = pd.DataFrame({'name': name,
                           'lat': latt,
                           'lon': lngg,
                           'rating': ratingg,
                           'user_ratings_total': user_rat})

    # Сохраняем новый DataFrame в файл Excel
    new_file_path = 'data/origin/car_dealer_rental_repair_wash.xlsx'
    new_df.to_excel(new_file_path, index=False)

    print(f'Новая таблица успешно создана и сохранена в файле {new_file_path}.')

