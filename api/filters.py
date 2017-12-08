from rest_framework.filters import FilterSet

from .models import Station, Metering


class StationFilterSet(FilterSet):
    class Meta:
        model = Station
        fields = {
            'name': ['exact', 'icontains'],
            'is_in_test_mode': ['exact'],
            'country': ['exact', 'icontains'],
            'state': ['exact', 'icontains'],
            'county': ['exact', 'icontains'],
            'community': ['exact', 'icontains'],
            'city': ['exact', 'icontains'],
            'district': ['exact', 'icontains'],
            'owner': ['exact'],
            'created': ['lte', 'gte'],
            'updated': ['lte', 'gte'],
        }


class MeteringFilterSet(FilterSet):
    class Meta:
        model = Metering
        fields = {
            'created': ['lte', 'gte'],
            'station': ['exact'],
        }
