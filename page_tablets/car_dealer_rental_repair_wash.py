import pandas as pd


async def car_dealer_rental_repair_wash_tables():
    # Указываем путь к файлу Excel
    file_path = 'data/origin/car_dealer_rental_repair_wash.xlsx'

    # Читаем файл Excel и сохраняем данные в переменную df           uv(DataFrame)
    df = pd.read_excel(file_path)

    # Получаем первую колонку из DataFrame
    name_column = df.iloc[0:, 0]
    lat_column = df.iloc[0:, 1]
    lon_column = df.iloc[0:, 2]
    rating_column = df.iloc[0:, 3]
    user_ratings_total_column = df.iloc[0:, 4]

    data = []

    for i in range(len(name_column)):
        if str(user_ratings_total_column.iloc[i]) == "nan" or str(rating_column.iloc[i]) == "nan":
            data.append({
                "name": name_column.iloc[i],
                "coordinates": str((lat_column.iloc[i], lon_column.iloc[i])),
                "rating": 0,
                "user_ratings_total": 0
            })

        else:
            data.append({
                "name": name_column.iloc[i],
                "coordinates": str((lat_column.iloc[i], lon_column.iloc[i])),
                "rating": float(rating_column.iloc[i]),
                "user_ratings_total": float(user_ratings_total_column.iloc[i])

            })

    return data