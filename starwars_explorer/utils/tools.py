import requests
import petl as etl
import pandas as pd
import uuid
from pathlib import Path
import csv


def download_dataset(data_path):
    """Download new dataset from swapi

    Args:
        data_path ([str]): path where new dataset should be downloaded.

    Returns:
        [Path]: Path object leading to the new dataset.
    """
    all_planets = set()
    all_characters = []
    keys_list = [
        "homeworld",
        "gender",
        "mass",
        "height",
        "hair_color",
        "skin_color",
        "eye_color",
        "birth_year",
        "name",
    ]
    for i in range(1, 10):
        r = requests.get(f"https://swapi.dev/api/people/?page={i}")
        data = r.json()
        results = data["results"]

        for result in results:
            filtered_result = {key: result[key] for key in keys_list}
            planet_num = filtered_result["homeworld"].split("/")[-2]
            filtered_result["homeworld"] = planet_num
            all_planets.add(planet_num)
            all_characters.append(filtered_result)

    planet_dict = {}
    index = 1
    for i in range(1, 10):
        r = requests.get(f"https://swapi.dev/api/planets/?page={i}")
        data = r.json()
        results = data.get("results")
        if not results:
            break
        for result in results:
            name = result["name"]
            planet_dict[index] = name
            index += 1

    for character in all_characters:
        character["homeworld"] = planet_dict[int(character["homeworld"])]
    file_name = str(uuid.uuid4()) + ".csv"
    ch_file = Path(data_path) / file_name

    with open(ch_file, "w", newline="") as output_file:
        dict_writer = csv.DictWriter(output_file, keys_list)
        dict_writer.writeheader()
        dict_writer.writerows(all_characters)
    return ch_file


def get_aggregated_data(data_path, file_name, keys):
    """get_aggregated_data

        aggregate data from the dataset using keys,
        to determine which columns to use to aggregate data.

    Args:
        data_path ([str]): path leading the directory where datasets
            are stored.

        file_name ([str]): file name.
        keys ([List]): list of columns

    Returns:
        [List]: rows of new aggregated table
    """
    file_path = Path(data_path) / file_name
    df_characters = pd.read_csv(file_path)
    df_characters.gender = df_characters.gender.fillna("unknown")

    table = etl.fromdataframe(df_characters)

    if keys:
        if len(keys) == 1:
            keys = keys[0]
        aggregated_table = etl.aggregate(table, key=keys, aggregation=len)
        rows = aggregated_table.enumerate()
        rows = [list(row[1]) for row in rows]
        return rows
    return None
