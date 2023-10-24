import numpy as np
import pandas as pd

data_clients = pd.read_excel("../data/clients/road_best_place.xlsx")

size = data_clients.shape[0]
mean_cars = 0.86
cars55 = mean_cars * np.ones(size) + np.random.normal(loc=0., scale=0.04, size=size)
cars5_12 = np.abs(np.ones(size) - cars55) * 0.65
cars12_16 = np.abs(np.ones(size) - cars55) * 0.3
cars16 = np.abs(np.ones(size) - cars55) * 0.05

#traffic
data_traffic = pd.DataFrame(data={'< 5,5 m': cars55, '5,5 - 12 m': cars5_12,
                                  '12 - 16,5 m': cars12_16, '> 16,5 m': cars16})
data_traffic.to_excel("../data/origin/cars_length_procent.xlsx")


gas95 = 1.5  # euro/litre
gasDiesel = 1.48


data_fuel = pd.DataFrame(data={'95, euro': np.random.normal(loc=gas95, scale=0.05, size=size),
                               'Diesel, euro': np.random.normal(loc=gasDiesel, scale=0.05, size=size)})

data_fuel.to_excel("../data/origin/fuel.xlsx")

das_average_bill = 6.5
data_das = pd.DataFrame(data={'средний чек на ДАС в районе':
                                  das_average_bill * np.ones(size) + np.random.normal(loc=0., scale=2, size=size)})
data_das.to_excel("../data/origin/das.xlsx")
