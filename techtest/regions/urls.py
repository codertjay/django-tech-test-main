from django.urls import path

from techtest.regions.views import RegionsListView, RegionView

app_name = 'regions'
urlpatterns = [
    path("", RegionsListView.as_view(), name="regions-list"),
    path("<int:region_id>/", RegionView.as_view(), name="region"),
]
