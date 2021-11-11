from django.http import HttpResponse
from django.template import loader
from .utils.tools import download_dataset, get_aggregated_data
from .models import Metadata
import datetime
import pytz
from pathlib import Path
from django.shortcuts import redirect
from django.conf import settings

import pandas as pd
import logging

logger = logging.getLogger(__name__)


def get_collections(request):
    template = loader.get_template("collections.html")

    collections_list = Metadata.objects.all()
    context = {"collections_list": collections_list}
    return HttpResponse(template.render(context, request))


def detail(request, file_name):
    context = {}

    if Metadata.objects.filter(filename=file_name).count() == 0:
        return HttpResponse(status=404)

    file_path = Path(settings.DATA_PATH) / file_name
    try:
        characters_df = pd.read_csv(file_path)
    except FileNotFoundError:
        return HttpResponse(status=404)

    characters_list = characters_df.to_dict("records")
    context = {
        "file_name": file_name,
        "characters_list": characters_list,
    }
    template = loader.get_template("collection_detail.html")
    return HttpResponse(template.render(context, request))


def fetch_new(request):
    try:
        dataset_path = download_dataset(settings.DATA_PATH)
        metaobject = Metadata.objects.create(
            filename=dataset_path.name, download_date=datetime.datetime.now(pytz.utc)
        )
        metaobject.save()
    except Exception as e:
        logger.error(e)
        logger.error("Failed to downlad new dataset.")
        return HttpResponse(status=500)
    return redirect("/starwars_explorer/collections")


def aggregate(request, file_name):
    if Metadata.objects.filter(filename=file_name).count() == 0:
        return HttpResponse(status=404)

    context = {}
    aggregate_by = {}
    valid_keys = ["homeworld", "mass", "height", "gender"]
    for key in valid_keys:
        if request.GET.get(key) == "on":
            aggregate_by[key] = True

    keys = [str(key) for key in aggregate_by]
    rows = get_aggregated_data(settings.DATA_PATH, file_name, keys)
    if rows:
        context["rows"] = rows

    context["aggregate_by"] = aggregate_by
    context["file_name"] = file_name
    template = loader.get_template("aggregator.html")
    return HttpResponse(template.render(context, request))
