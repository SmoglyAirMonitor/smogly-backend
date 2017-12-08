from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from tqdm import tqdm

from api.tests.factories import StationFactory, MeteringFactory


class Command(BaseCommand):
    DEFAULT_STATIONS = 10
    DEFAULT_METERINGS = 5000
    DEFAULT_METERING_DELTA = timezone.timedelta(minutes=15)

    help = 'Populate models with some data, see arguments for possible details.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-s',
            '--stations',
            action='store',
            default=self.__class__.DEFAULT_STATIONS,
            help='How many Stations to create? default={}.'.format(
                self.__class__.DEFAULT_STATIONS
            ),
            type=int
        )
        parser.add_argument(
            '-m',
            '--meterings',
            action='store',
            default=self.__class__.DEFAULT_METERINGS,
            help='How many Meterings for each Station to create? default={}.'.format(
                self.__class__.DEFAULT_METERINGS
            ),
            type=int
        )

    @transaction.atomic()
    def handle(self, *args, **options):
        total = options['stations'] * options['meterings']
        with tqdm(total=total) as progress_bar:
            for _ in range(0, options['stations']):
                station = StationFactory.create()
                for i in range(0, options['meterings']):
                    created = timezone.now() - i * self.__class__.DEFAULT_METERING_DELTA
                    MeteringFactory.create(station=station, created=created)
                    progress_bar.update(1)
