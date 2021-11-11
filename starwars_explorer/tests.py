from django.test import TestCase

# Create your tests here.
from utils.tools import get_aggregated_data, SwapiClient
from django.conf import settings
from .models import Metadata

import datetime
import os
from unittest.mock import MagicMock
from pathlib import Path

class SwapiClientTest(TestCase):
    def setUp(self):
        DATA_PATH = "/data/"
        self.client = SwapiClient(DATA_PATH, ["homeworld", "name"])

    def test__filter_planet_numbers(self):
        characters = self.client._filter_planet_numbers(
            characters=[{"name": "Luke", "homeworld": 1}], planet_dict={1: "Tatooine"}
        )
        self.assertEqual(characters[0]["homeworld"], "Tatooine")

    def test__save_dataset(self):
        characters = [{"name": "Leia Oregana"}, {"name": "Luke Skywalker"}]
        self.client._save_dataset("./1234.csv", characters)
        self.assertEqual(os.path.exists("./1234.csv"), True)
        os.remove("./1234.csv")


class AggregateTests(TestCase):
    def setUp(self):
        DATA_PATH = "/data/"
        self.client = SwapiClient(DATA_PATH, ["homeworld", "name", "gender"])
        characters = [
            {"name": "Leia Oregana", "homeworld": "Tatooine", "gender": "female"},
            {"name": "Luke Skywalker", "homeworld": "Tatooine", "gender": "male"},
        ]
        self.client._save_dataset("./1234.csv", characters)

    def test_aggregate_succeeds(self):
        rows = get_aggregated_data("./", "1234.csv", keys=["homeworld"])
        self.assertEqual(len(rows), 2)


class CollectionsViewTests(TestCase):
    def _create_metadata(self):
        return Metadata.objects.create(
            filename="1234.csv", download_date=datetime.datetime.now()
        )

    def test_no_collections(self):
        response = self.client.get("/starwars_explorer/collections/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, ".csv")

    def test_one_collection(self):
        metadata = self._create_metadata()
        response = self.client.get("/starwars_explorer/collections/")
        self.assertContains(response, "1234.csv")


class CollectionDetail(TestCase):
    def _create_metadata(self, filename):
        return Metadata.objects.create(
            filename=filename, download_date=datetime.datetime.now()
        )

    def setUp(self):
        self.DATA_PATH = Path(settings.DATA_PATH)
        self.swapi_client = SwapiClient(self.DATA_PATH, ["homeworld", "name", "gender"])
        characters = [
            {"name": "Leia Oregana", "homeworld": "Tatooine", "gender": "female"},
            {"name": "Luke Skywalker", "homeworld": "Tatooine", "gender": "male"},
        ]
        self.swapi_client._save_dataset(self.DATA_PATH / "1234.csv", characters)

    def test_collection_contains_Luke(self): 
        self._create_metadata("1234.csv")
        response = self.client.get(
            "/starwars_explorer/collections/1234.csv/"
        )
        self.assertContains(response, "Luke")

    def tearDown(self):
        os.remove(self.DATA_PATH / "1234.csv")

class AggregateView(TestCase):
    def setUp(self):
        self.DATA_PATH = Path(settings.DATA_PATH)
        self.swapi_client = SwapiClient(self.DATA_PATH, ["homeworld", "name", "gender"])
        characters = [
            {"name": "Leia Oregana", "homeworld": "Tatooine", "gender": "female"},
            {"name": "Luke Skywalker", "homeworld": "Tatooine", "gender": "male"},
        ]
        self.swapi_client._save_dataset(self.DATA_PATH / "1234.csv", characters)

    def _create_metadata(self, filename):
        return Metadata.objects.create(
            filename=filename, download_date=datetime.datetime.now()
        )

    def test_succeeds(self):
        
        self._create_metadata("1234.csv")
        response = self.client.get(
            "/starwars_explorer/collections/aggregate/1234.csv/"
        )
        self.assertContains(response, "homeworld")
