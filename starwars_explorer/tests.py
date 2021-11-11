from django.test import TestCase

# Create your tests here.
from utils.tools import download_dataset, get_aggregated_data
from django.conf import settings
from django.urls import reverse
from .models import Metadata

import datetime
import os


class DownloadTests(TestCase):
    def test_download_succeeds(self):
        dataset_path = download_dataset(settings.DATA_PATH)
        exists = os.path.exists(dataset_path)
        self.assertIs(exists, True)
        size = os.path.getsize(dataset_path)
        self.assertGreater(size, 0)
        os.remove(dataset_path)


class AggregateTests(TestCase):
    def test_aggregate_succeeds(self):
        dataset_path = download_dataset(settings.DATA_PATH)
        rows = get_aggregated_data(
            settings.DATA_PATH, dataset_path.name, keys=["homeworld"]
        )
        self.assertEqual(len(rows), 50)
        os.remove(dataset_path)


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

    def test_collection_contains_Luke_and_Obi(self):
        dataset_path = download_dataset(settings.DATA_PATH)
        self._create_metadata(dataset_path.name)
        response = self.client.get(
            "/starwars_explorer/collections/" + dataset_path.name + "/"
        )
        self.assertContains(response, "Luke")
        self.assertContains(response, "Obi")
        os.remove(dataset_path)

class AggregateView(TestCase):
    def _create_metadata(self, filename):
        return Metadata.objects.create(
            filename=filename, download_date=datetime.datetime.now()
        )

    def test_succeeds(self):
        dataset_path = download_dataset(settings.DATA_PATH)
        self._create_metadata(dataset_path.name)
        response = self.client.get(
            "/starwars_explorer/collections/aggregate/" + dataset_path.name + "/"
        )
        self.assertContains(response, "homeworld")
        os.remove(dataset_path)