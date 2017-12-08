# -*- coding: utf-8 -*-
import random

import factory
import factory.fuzzy
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.gis.geos import Point
from faker import Faker

from api.models import Station, Metering


class FuzzyFloatRound(factory.fuzzy.FuzzyFloat):
    """Random float within a given range with ndigits option, that will round fuzzer to ndigits."""

    def __init__(self, *args, **kwargs):
        self.ndigits = kwargs.pop('ndigits')

        super(FuzzyFloatRound, self).__init__(*args, **kwargs)

    def fuzz(self):
        fuzz = super(FuzzyFloatRound, self).fuzz()
        if self.ndigits:
            return round(fuzz, self.ndigits)
        return fuzz


class AbstractLocationFactory(factory.django.DjangoModelFactory):

    @factory.lazy_attribute
    def position(self):
        x = random.uniform(14.12297069999998, 24.14578300000009)
        y = random.uniform(49.00204680000022, 54.83578869999986)
        return Point([x, y])

    country = 'Polska'
    state = factory.fuzzy.FuzzyChoice(['Małopolska', 'Wielkopolska'])
    county = factory.fuzzy.FuzzyChoice(['nowotomyski', 'krakowski'])
    community = factory.fuzzy.FuzzyChoice(['Nowy Tomyśl', 'Kraków'])
    city = factory.fuzzy.FuzzyChoice(['Nowy Tomyśl', 'Kraków'])
    district = factory.fuzzy.FuzzyChoice(['Kazmierz', 'Nowa Huta', 'Krowodrza'])

    class Meta:
        abstract = True


class UserFactory(factory.django.DjangoModelFactory):
    DEFAULT_PASSWORD = 'very_dangerous_password'

    class Meta:
        model = get_user_model()
        exclude = ('DEFAULT_PASSWORD',)

    username = factory.LazyFunction(lambda: 'smoglyuser-%s' % Faker().uuid4())
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')

    @factory.lazy_attribute
    def password(self):
        """
        http://stackoverflow.com/questions/24748222/django-python-django-login-test-failed-with-factory-boy-and-authtools
        """
        return make_password(self.DEFAULT_PASSWORD)


class StationFactory(AbstractLocationFactory):
    name = factory.Sequence(lambda n: 'Smogly Station %04d' % n)
    type = factory.fuzzy.FuzzyChoice([type_choice[0] for type_choice in Station.TYPE_CHOICES])
    notes = factory.Faker('sentences', nb=3)
    altitude = FuzzyFloatRound(0.0, 300.0, ndigits=2)
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Station


class MeteringFactory(factory.django.DjangoModelFactory):
    pm25 = FuzzyFloatRound(0.0, 150.0, ndigits=2)
    pm10 = FuzzyFloatRound(0.0, 150.0, ndigits=2)
    temperature = FuzzyFloatRound(-25.0, 30.0, ndigits=2)
    humidity = FuzzyFloatRound(5.0, 99.0, ndigits=2)

    station = factory.SubFactory(StationFactory)
    
    class Meta:
        model = Metering
