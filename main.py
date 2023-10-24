import pandas as pd
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from page_tablets.gas_station import gas_station_tables
from page_tablets.shopping_mall import shopping_malls_tables
from page_tablets.cafe_supermarket import cafe_supermarket_tables
from page_tablets.parking_taxistand_trainstation_transitstation import parking_taxistand_trainstation_transitstation_tables
from page_tablets.car_dealer_rental_repair_wash import car_dealer_rental_repair_wash_tables

from update_data.start_update import update_all_data
from update_data.traffic_daily import catch_traffic_now
#from apscheduler.schedulers.blocking import BlockingScheduler

app = FastAPI()


# Разрешение CORS для всех доменов
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {"message": "Greetings!"}


@app.get("/main")
async def main():
    # Указываем путь к файлу Excel
    file_path = 'data/clients/roads_rating.xlsx'

    # Читаем файл Excel и сохраняем данные в переменную df           uv(DataFrame)
    df = pd.read_excel(file_path)

    # Получаем колонки из DataFrame
    number_column = df.iloc[0:, 1]  # номер
    name_column = df.iloc[0:, 2]  # название
    origin_coords_column = df.iloc[0:, 3]  # coords start
    destination_coords_column = df.iloc[0:, 4]  # coords end
    rating_column = df.iloc[0:, 5]

    data = []
    counter = 0

    for i in range(len(number_column)):
        try:
            lat_start, lng_start = map(float, origin_coords_column.iloc[i].split(', '))
            lat_end, lng_end = map(float, destination_coords_column.iloc[i].split(', '))

            # if i in [0, 30, 43, 56, 78, 98, 108, 123, 134, 155] :
            data.append({
                "id": int(number_column.iloc[i]),
                "name": str(name_column.iloc[i]),
                "coordinates": [{
                    "lat": lat_start,
                    "lng": lng_start
                },
                    {
                        "lat": lat_end,
                        "lng": lng_end
                    }],
                "travelMode": "DRIVING",
                "rating": rating_column.iloc[i]})
        except:
            counter += 1
            pass

    print(counter)
    return data


@app.get("/road")
async def road_info(id):
    # Указываем путь к файлу Excel
    file_path = 'data/clients/road_best_place.xlsx'
    file_path2 = 'data/revenue/total_revenue.xlsx'

    # Читаем файл Excel и сохраняем данные в переменную df           uv(DataFrame)
    df = pd.read_excel(file_path)
    df2 = pd.read_excel(file_path2)

    # Получаем колонки из DataFrame
    number_column = df.iloc[0:, 2]  # номер
    name_column = df.iloc[0:, 3]  # название
    road_coords_column = df.iloc[0:, 6]  # coords start
    len_column = df.iloc[0:, 7]
    cities_column = df.iloc[0:, 8]
    nestro_column = df.iloc[0:, 9]
    malls_column = df.iloc[0:, 10]
    other_stations_column = df.iloc[0:, 11]
    car_service_column = df.iloc[0:, 12]
    parking_column = df.iloc[0:, 13]
    potential_column = df.iloc[0:, 14]
    best_place_column = df.iloc[0:, 15]
    clients_column = df.iloc[0:, 16]

    oil_revenue_column = df2.iloc[0:, 2]
    das_revenue_column = df2.iloc[0:, 3]

    for i in range(len(number_column)):
        if str(id) == str(number_column.iloc[i]):

            name = name_column.iloc[i]
            leng = len_column.iloc[i]
            road_coords = road_coords_column.iloc[i]
            cities = cities_column.iloc[i]
            nestro = nestro_column.iloc[i]
            malls = malls_column.iloc[i]
            other_stations = other_stations_column.iloc[i]
            potential = potential_column.iloc[i]
            best_place = best_place_column.iloc[i]
            car_service = car_service_column.iloc[i]
            parking = parking_column.iloc[i]
            clients = clients_column.iloc[i]
            oil_revenue = oil_revenue_column.iloc[i]
            das_revenue = das_revenue_column.iloc[i]
            total_revenue = oil_revenue_column.iloc[i] + das_revenue_column.iloc[i]

            dictionary = {
                "name": name,
                "road_coords": road_coords,
                "leng": leng,
                "cities": cities,
                "nestro": nestro,
                "malls": malls,
                "other_stations": other_stations,
                "potential": potential,
                "best_place": best_place,
                "car_service": car_service,
                "parking": parking,
                "clients": clients,
                "oil_revenue": oil_revenue,
                "das_revenue": das_revenue,
                "total_revenue": total_revenue
            }
            return dictionary

    return False


@app.get("/best_places")
async def best_places():
    # Указываем путь к файлу Excel
    file_path = 'data/clients/road_best_place.xlsx'
    file_path2 = 'data/revenue/total_revenue.xlsx'

    # Читаем файл Excel и сохраняем данные в переменную df           uv(DataFrame)
    df = pd.read_excel(file_path)
    df2 = pd.read_excel(file_path2)

    # Получаем колонки из DataFrame
    number_column = df.iloc[0:, 2]  # номер
    name_column = df.iloc[0:, 3]  # название
    road_coords_column = df.iloc[0:, 6]  # coords start
    len_column = df.iloc[0:, 7]
    cities_column = df.iloc[0:, 8]
    nestro_column = df.iloc[0:, 9]
    malls_column = df.iloc[0:, 10]
    other_stations_column = df.iloc[0:, 11]
    car_service_column = df.iloc[0:, 12]
    parking_column = df.iloc[0:, 13]
    potential_column = df.iloc[0:, 14]
    best_place_column = df.iloc[0:, 15]
    clients_column = df.iloc[0:, 16]

    oil_revenue_column = df2.iloc[0:, 2]
    das_revenue_column = df2.iloc[0:, 3]

    data_for_return = []
    norma = max(oil_revenue_column + das_revenue_column)
    print(norma)

    for i in range(len(number_column)):
        name = name_column.iloc[i]
        leng = len_column.iloc[i]
        road_coords = road_coords_column.iloc[i]
        cities = cities_column.iloc[i]
        nestro = nestro_column.iloc[i]
        malls = malls_column.iloc[i]
        other_stations = other_stations_column.iloc[i]
        potential = potential_column.iloc[i]
        best_place = best_place_column.iloc[i]
        car_service = car_service_column.iloc[i]
        parking = parking_column.iloc[i]
        clients = clients_column.iloc[i]
        oil_revenue = oil_revenue_column.iloc[i]
        das_revenue = das_revenue_column.iloc[i]
        total_revenue = oil_revenue_column.iloc[i] + das_revenue_column.iloc[i]
        print(best_place, total_revenue)
        if str(total_revenue) != "nan":
            dictionary = {
                # "name": name,
                # "road_coords": road_coords,
                # "leng": leng,
                # "cities": cities,
                # "nestro": nestro,
                # "malls": malls,
                # "other_stations": other_stations,
                # "potential": potential,
                "best_place": best_place,
                # "car_service": car_service,
                # "parking": parking,
                # "clients": clients,
                # "oil_revenue": oil_revenue,
                # "das_revenue": das_revenue,
                "total_revenue": total_revenue
            }
            data_for_return.append(dictionary)

    return sorted(data_for_return, key=lambda x: x['total_revenue'], reverse=True)



@app.get("/roads_dashboards")
async def road_info():
    # Указываем путь к файлу Excel
    file_path = 'data/clients/road_best_place.xlsx'
    file_path2 = 'data/revenue/total_revenue.xlsx'

    # Читаем файл Excel и сохраняем данные в переменную df           uv(DataFrame)
    df = pd.read_excel(file_path)
    df2 = pd.read_excel(file_path2)

    # Получаем колонки из DataFrame
    number_column = df.iloc[0:, 2]  # номер
    name_column = df.iloc[0:, 3]  # название
    potential_column = df.iloc[0:, 14]
    best_place_column = df.iloc[0:, 15]
    clients_column = df.iloc[0:, 16]

    oil_revenue_column = df2.iloc[0:, 2]
    das_revenue_column = df2.iloc[0:, 3]

    data_for_return = []

    for i in range(len(number_column)):
        number = number_column.iloc[i]
        name = name_column.iloc[i]
        best_place = best_place_column.iloc[i]
        clients = clients_column.iloc[i]
        oil_revenue = oil_revenue_column.iloc[i]
        das_revenue = das_revenue_column.iloc[i]

        dictionary = {
            "number": str(number),
            "name": name,
            "best_place": str(best_place),
            "clients": str(clients),
            "oil_revenue": str(oil_revenue),
            "das_revenue": str(das_revenue)
        }
        data_for_return.append(dictionary)

    return data_for_return


@app.get("/gas_station")
async def gas_station():
    return await gas_station_tables()


@app.get("/shopping_malls")
async def shopping_malls():
    return await shopping_malls_tables()


@app.get("/cafe_supermarket")
async def cafe_supermarket():
    return await cafe_supermarket_tables()


@app.get("/parking_taxistand_trainstation_transitstation")
async def parking_taxistand_trainstation_transitstation():
    return await parking_taxistand_trainstation_transitstation_tables()


@app.get("/car_dealer_rental_repair_wash")
async def car_dealer_rental_repair_wash():
    return await car_dealer_rental_repair_wash_tables()

  
if __name__ == '__main__':
    update_all_data()  # функция которая пересчитывает выручку и все данные с google maps api, прежде чем ее запустить, прочитайте описание к ней

    uvicorn.run(app)
    # Создаем объект планировщика
    #scheduler = BlockingScheduler()

    # Запускаем функцию каждый час
    #scheduler.add_job(catch_traffic_now, 'interval', minutes=1)

    # Запускаем планировщик для сбора трафика
    #scheduler.start()

