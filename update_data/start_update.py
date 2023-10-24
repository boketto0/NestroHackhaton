from update_data.roads import update_roads
from update_data.shopping_mall import update_shopping_malls
from update_data.parking_taxi_stand_train_station_transit_station import update_parking_taxi_stand_train_station_transit_stations
from update_data.gas_station import update_gas_stations
from update_data.car_dealer_rental_repair_wash import update_car_dealer_rental_repair_wash
from update_data.cafe_supermarket import update_cafe_supermarkets

from src.total_revenue import calculate_total_revenue
from src.propagate_clients import propagete_clients


def update_geo_data():
    """
    Функция `update_geo_data()` использует Google Maps API для обновления геоданных. Однако, рекомендуется не запускать
    эту функцию слишком часто, так как Google ограничивает количество запросов. В связи с этим, в коде функции включена
    задержка `time.sleep(0.2)` после каждого обращения к API, чтобы избежать проблем с ограничениями.

    Обновление геоданных может занять длительное время из-за ограничений Google и большого количества запросов,
    выполняемых функцией. Поэтому рекомендуется быть терпеливым при запуске этой функции.

    Код функции `update_geo_data()` включает вызов различных подфункций для обновления данных о дорогах, торговых
    центрах, парковках, такси, станциях поезда и транзитных станциях, заправочных станциях и автомобильных дилерских
    центрах. Эти подфункции содержат логику для получения данных через Google Maps API.
    В целом, эта функция представляет собой важный инструмент для обновления геоданных с использованием Google Maps API,
    но ее использование требует осторожности и учета ограничений API для избежания проблем и соблюдения правил
    использования."""

    update_roads()
    update_shopping_malls()
    update_parking_taxi_stand_train_station_transit_stations()
    update_gas_stations()
    update_car_dealer_rental_repair_wash()
    update_cafe_supermarkets()


def update_all_data():

    """ Выполнение update_geo_data() может занять до часа """
    # update_geo_data()   WARNING прежде чем раскоментировать функцию, прочитайте документацию к ней выше ^^.
    # propagete_clients()
    calculate_total_revenue()


