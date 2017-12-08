from rest_framework import serializers

from .models import Station, Metering


class StationSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Station
        fields = (
            'id',
            'name',
            'created',
            'updated',
            'type',
            'notes',
            'altitude',
            'position',
            'country',
            'state',
            'county',
            'community',
            'city',
            'district',
            'owner',
            'last_metering',
        )


class MeteringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metering
        fields = (
            'station',
            'created',
            'pm25',
            'pm10',
            'temperature',
            'humidity',
        )
