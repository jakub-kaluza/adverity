import requests
import petl as etl
import pandas as pd
import uuid
from pathlib import Path
import csv
import logging

logger = logging.getLogger(__name__)


class SwapiClient():
    def __init__(self, data_path, used_keys):
        self.keys_list = used_keys
        self.data_path = data_path
        self.num_pages = 10

    def get_all_characters(self):
        all_characters = []
        pertinent_planets = set()
        for i in range(1, self.num_pages):
            try:
                request_url = f"https://swapi.dev/api/people/?page={i}"
                r = requests.get(request_url)
                data = r.json()
                results = data["results"]

                for result in results:
                    filtered_result = {key: result[key] for key in self.keys_list}
                    planet_num = filtered_result["homeworld"].split("/")[-2]
                    filtered_result["homeworld"] = planet_num
                    pertinent_planets.add(planet_num)
                    all_characters.append(filtered_result)
            except Exception as exception:
                logger.error("Something went wrong during reqest to %s", request_url)
                raise exception
        return all_characters

    def get_all_planets(self):
        planet_dict = {}
        index = 1
        for i in range(1, self.num_pages):
            request_url = f"https://swapi.dev/api/planets/?page={i}"
            try:
                r = requests.get(request_url)
                data = r.json()
                results = data.get("results")
                if not results:
                    break
                for result in results:
                    name = result["name"]
                    planet_dict[index] = name
                    index += 1
            except Exception as exception:
                logger.error("Something went wrong during reqest to %s", request_url)
                raise exception
        return planet_dict

    def _filter_planet_numbers(self, characters, planet_dict):
        for character in characters:
            character["homeworld"] = planet_dict[int(character["homeworld"])]
        return characters
    
    def _save_dataset(self, file_name, characters):
        try:
            with open(file_name, "w", newline="") as output_file:
                dict_writer = csv.DictWriter(output_file, self.keys_list)
                dict_writer.writeheader()
                dict_writer.writerows(characters)
        except OSError as oserror:
            logger.error("Could not write file")
            raise oserror 

    def download_dataset(self):
        all_characters = self.get_all_characters()
        all_planets = self.get_all_planets()
        all_characters = self._filter_planet_numbers(all_characters, all_planets)
        file_name = str(uuid.uuid4()) + ".csv"
        dataset_path = Path(self.data_path) / file_name
        self._save_dataset(dataset_path, all_characters)
        return dataset_path


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
