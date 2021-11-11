from django.urls import path
from .views import get_collections, detail, fetch_new, aggregate


app_name = "starwars_app"
urlpatterns = [
    path("collections/", get_collections, name="collections"),
    path("collections/<str:file_name>/", detail, name="detail"),
    path("collections/fetch", fetch_new, name="fetch"),
    path("collections/aggregate/<str:file_name>/", aggregate, name="aggregate"),
]
