import pandas as pd

from src.ClientPropagator import ClientPropagator

import src.data_for_clients as data



def propagete_clients():
    CL = ClientPropagator(data.roads_df['potential'])
    # CL = ClientPropagator()
    best_places = []
    clients = []
    for ind, road in data.roads_df.iterrows():
        best_place, client = CL.best_place(road['Номер'])
        best_places.append(best_place)
        clients.append(client)

    road_best_place_df = data.roads_df.copy()
    road_best_place_df['best_place'] = pd.Series(best_places)
    road_best_place_df['clients'] = pd.Series(clients)
    road_best_place_df.to_excel('data/clients/road_best_place.xlsx')

    roads_rating = pd.DataFrame()
    roads_rating['Номер'] = data.roads_df['Номер']
    roads_rating['Название'] = data.roads_df['Название']
    roads_rating['origin_coords'] = data.roads_df['origin_coords']
    roads_rating['destination_coords'] = data.roads_df['destination_coords']
    roads_rating['rating'] = data.traffic_df['Авто в день'] / data.traffic_df['Авто в день'].max()
    roads_rating.to_excel('data/clients/roads_rating.xlsx')

