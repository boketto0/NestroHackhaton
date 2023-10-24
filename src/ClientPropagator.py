import pandas as pd
import src.data_for_clients as data


class ClientPropagator:
    """Класс, предсказывающий количество клиентов АЗС"""

    def __init__(self, potential=None):
        """Potential -- pd.Series с раннее рассчитанным потенциалом для каждой дороги, если такой есть"""
        # Список настраиваемых параметров
        self.client_traffic_ratio = 0.02  # доля заправок с трафика
        self.pop_coef = 1e7  # коэффициент населения
        self.nestro_stat_coef = -1e4  # коэффициент АЗС Nestro
        self.stat_coef = 1e5  # коэффициент других АЗС
        self.shopping_mall_coef = 1e5  # коэффициент торговых центров
        self.car_service_coef = 1e3
        self.parkings_coef = 1e3
        self.point_diameter_ratio = 0.05  #
        self.roads_potential = potential

        # Если нет уже посчитанного потенциала, то расчет идет заново
        if self.roads_potential is None:
            self.total_pot = {}
            for ind, road in data.roads_df.iterrows():
                print(ind)
                pot = 0
                try:
                    l = road['len'] / len(eval(road['roads_coords']))
                    for point in eval(road['roads_coords']):
                        pot += self.calc_potential(road['Номер'], point[0], point[1])
                    self.total_pot[road['Номер']] = pot * l
                except:
                    self.total_pot[road['Номер']] = None

            # Сохранение данных в таблицу для возможного повторного использования
            roads_and_potential = data.roads_df.copy()
            roads_and_potential['potential'] = pd.Series(self.total_pot.values())
            roads_and_potential.to_excel('data/clients/roads_potential.xlsx')

    def calc_population_potential(self, road_ind, lat, lon):
        """Расчет потенциала от населения"""
        pot = 0
        for c in data.roads_df[data.roads_df['Номер'] == road_ind].iloc[0]['cities']:
            city = data.cities_df[data.cities_df['City'] == c].iloc[0]
            l2 = 0.001 + ((city['lat'] - lat) ** 2 + (city['lon'] - lon) ** 2) * 6400 ** 2
            pot += self.pop_coef * city['ratio'] / l2
        return pot

    def calc_nestro_station_potential(self, road_ind, lat, lon):
        """Расчет отталкивающего потенциала от АЗС Nestro"""
        pot = 0
        for ns in data.roads_df[data.roads_df['Номер'] == road_ind].iloc[0]['nestro_stations']:
            station = data.nestro_stations_df[data.nestro_stations_df['lat'] == ns].iloc[0]
            l2 = 0.001 + ((station['lat'] - lat) ** 2 + (station['lon'] - lon) ** 2) * 6400 ** 2
            pot += self.nestro_stat_coef / l2
        return pot

    def calc_shopping_mall_potential(self, road_ind, lat, lon):
        """Расчет потенциала от ТЦ"""
        pot = 0
        for sm in data.roads_df[data.roads_df['Номер'] == road_ind].iloc[0]['shopping_malls']:
            sh_mall = data.shopping_malls_df[data.shopping_malls_df['lat'] == sm].iloc[0]
            l2 = 0.001 + ((sh_mall['lat'] - lat) ** 2 + (sh_mall['lon'] - lon) ** 2) * 6400 ** 2

            pot += self.shopping_mall_coef * sh_mall['rating'] * sh_mall['user_ratings_total'] / 1000 / l2
        return pot

    """Расчет потенциала от других АЗС"""

    def calc_station_potential(self, road_ind, lat, lon):
        """Расчет потенциала от АЗС других станций"""
        pot = 0
        for s in data.roads_df[data.roads_df['Номер'] == road_ind].iloc[0]['other_stations']:
            try:
                l2 = 0.001 + ((s['lat'] - lat) ** 2 + (s['lon'] - lon) ** 2) * 6400 ** 2
                pot += self.stat_coef / l2
            except:
                pass
        return pot

    def calc_car_service_potential(self, road_ind, lat, lon):
        """Расчет потенциала от АЗС других станций"""
        pot = 0
        for s in data.roads_df[data.roads_df['Номер'] == road_ind].iloc[0]['car_services']:
            try:
                l2 = 0.001 + ((s['lat'] - lat) ** 2 + (s['lon'] - lon) ** 2) * 6400 ** 2
                pot += self.car_service_coef * s['rating'] * s['user_ratings_total'] / 1000 / l2
            except:
                pass
        return pot

    def calc_parking_potential(self, road_ind, lat, lon):
        """Расчет потенциала от АЗС других станций"""
        pot = 0
        for p in data.roads_df[data.roads_df['Номер'] == road_ind].iloc[0]['parkings']:
            try:
                l2 = 0.001 + ((p['lat'] - lat) ** 2 + (p['lon'] - lon) ** 2) * 6400 ** 2
                pot += self.parkings_coef * p['rating'] * p['user_ratings_total'] / 1000 / l2
            except:
                pass
        return pot

    """Вычисление полного потенциала точки"""

    def calc_potential(self, road_ind, lat, lon):
        return 1 + self.calc_population_potential(road_ind, lat, lon) + \
            self.calc_nestro_station_potential(road_ind, lat, lon) + self.calc_station_potential(
                road_ind, lat, lon) + self.calc_parking_potential(road_ind, lat, lon) + \
            self.calc_car_service_potential(road_ind, lat, lon)

    def linear_transform(self, x, a, b, A, B):
        """Линейно переводит промежуток (a, b) в (A, B)"""
        if a == b: return 0
        return (B * a - A * b) / (a - b) + (A - B) / (a - b) * x

    def propagate(self, road_ind, lat, lon):
        """Предсказывает количество клиентов"""
        road = data.roads_df[data.roads_df['Номер'] == road_ind]
        clients = self.client_traffic_ratio * data.traffic_df[data.traffic_df['Номер'] == road_ind].iloc[0][
            'Авто в день']
        pot = self.calc_potential(road_ind, lat, lon)
        total_pot = self.roads_potential.iloc[road.index[0]] if self.roads_potential is not None \
            else self.total_pot[road_ind] if self.total_pot[road_ind] > 0 else 1
        return pot * self.point_diameter_ratio * road['len'].iloc[0] / total_pot

    def find_places(self, road_ind):
        """Оценивает каждую точку на дороге"""
        points = {}
        try:
            road = data.roads_df[data.roads_df['Номер'] == road_ind].iloc[0]
            for point in eval(road['roads_coords']):
                points[tuple(point)] = self.propagate(road_ind, point[0], point[1])
            return {
                i: self.linear_transform(j, min(points.values()), max(points.values()), 0,
                                         1) * self.client_traffic_ratio *
                   data.traffic_df[data.traffic_df['Номер'] == road_ind].iloc[0]['Авто в день'] for i, j in
                points.items()}
        except:
            return {}

    def best_place(self, road_ind):
        try:
            places = self.find_places(road_ind)
            key = list(places.keys())[list(places.values()).index(max(places.values()))]
            return key, places[key]
        except:
            return None, None

