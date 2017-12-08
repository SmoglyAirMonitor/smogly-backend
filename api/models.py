import uuid

from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import models

from .utils import generate_token


class AbstractTimeTrackable(models.Model):
    """
    Abstract model for time trackable features.
    """

    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class AbstractLocation(models.Model):
    """
    Abstract model for location features.
    """

    position = gis_models.PointField(help_text='Exact position on map.', default=None, null=True)
    country = models.CharField(max_length=255, default='')
    state = models.CharField(help_text='administration level 1', max_length=255, default='')
    county = models.CharField(help_text='administration level 2', max_length=255, default='')
    community = models.CharField(help_text='administration level 3', max_length=255, default='')
    city = models.CharField(help_text='administration level 4', max_length=255, default='')
    district = models.CharField(help_text='administration level 5', max_length=255, default='')

    class Meta:
        abstract = True


class Station(AbstractTimeTrackable, AbstractLocation):
    """
    Model representing sensor station. Can be grouped using Project model.
    """

    TYPE_SMOGLY = 'smogly'
    TYPE_CUSTOM = 'custom'
    TYPE_AQICN = 'aqicn'
    TYPE_BASIC_SDS011 = 'basic-sds011'
    TYPE_CHOICES = (
        (TYPE_SMOGLY, 'SMOGLY'),
        (TYPE_CUSTOM, 'CUSTOM'),
        (TYPE_AQICN, 'AQICN'),
        (TYPE_BASIC_SDS011, 'BASIC-SDS011'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, default=TYPE_SMOGLY)
    notes = models.CharField(max_length=255)
    token = models.CharField(
        max_length=255,
        help_text='Token automatically generated while saving model, needed by Station to POST any data.',
        default=generate_token,
        unique=True
    )
    altitude = models.FloatField(help_text='Altitude of sensor location.', default=0)

    # Relationship Fields
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    @property
    def last_metering(self):
        """
        Return lastly created, serialized Metering object.
        We remove cache key while adding metering to given station.
        """
        if not cache.get(self.last_metering_cache_key):
            from api.serializers import MeteringSerializer
            last_metering = self.metering_set.first()
            cache.set(self.last_metering_cache_key, MeteringSerializer(last_metering).data)
        return cache.get(self.last_metering_cache_key)

    @property
    def last_metering_cache_key(self):
        return 'station-{}-last-metering'.format(self.pk)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{}'.format(self.id)

    def get_absolute_url(self):
        return reverse('api_station_detail', args=(self.id,))

    def get_update_url(self):
        return reverse('api_station_update', args=(self.id,))


class Metering(models.Model):
    """
    Model representing data submitted by sensor station.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    # Data Fields
    pm25 = models.IntegerField(
        help_text='PM 2.5 in ug/m^3'
    )
    pm10 = models.IntegerField(
        help_text='PM 10 in ug/m^3'
    )
    temperature = models.FloatField(
        help_text='Outside temperature, in C.',
        blank=True,
        default=None,
        null=True
    )
    humidity = models.FloatField(
        help_text='Outside relative humidity, in %.',
        blank=True,
        default=None,
        null=True
    )

    # Relationship Fields
    station = models.ForeignKey('api.Station')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'created={}, pm10={} [ug/m^3], pm25={} [ug/m^3], temperature={} [C], humidity={} [%]'.format(
            self.created,
            self.pm10,
            self.pm25,
            self.temperature,
            self.humidity,
        )

    def get_absolute_url(self):
        return reverse('api_metering_detail', args=(self.pk,))
