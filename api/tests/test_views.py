from django.contrib.gis.geos.point import Point
from rest_framework.reverse import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN
)
from rest_framework.test import APITestCase

from .factories import (
    Station,
    UserFactory,
    StationFactory,
    MeteringFactory
)
from ..serializers import StationSerializer, MeteringSerializer


class UserAuthBase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.jwt_url = reverse('api-token-auth')
        self.user_data = {
            'username': self.user.username,
            'password': UserFactory.DEFAULT_PASSWORD
        }

    def obtain_token_and_set_auth(self):
        response = self.client.post(self.jwt_url, self.user_data)
        return self.client.credentials(HTTP_AUTHORIZATION='JWT ' + response.data['token'])


class StationApiTests(UserAuthBase):
    def setUp(self):
        self.station = StationFactory.build()
        self.station_data = StationSerializer(self.station).data
        self.station_list_url = reverse('station-list')
        return super(StationApiTests, self).setUp()

    def create_station(self):
        self.obtain_token_and_set_auth()
        return self.client.post(self.station_list_url, self.station_data)

    def assertStationDataEqual(self, data):
        self.assertEqual(data['name'], self.station_data['name'])
        self.assertEqual(data['type'], self.station_data['type'])
        self.assertEqual(data['notes'], self.station_data['notes'])
        self.assertEqual(data['is_in_test_mode'], self.station_data['is_in_test_mode'])
        self.assertEqual(data['altitude'], self.station_data['altitude'])
        self.assertEqual(data['position'], self.station_data['position'])
        self.assertEqual(data['country'], self.station_data['country'])
        self.assertEqual(data['state'], self.station_data['state'])
        self.assertEqual(data['county'], self.station_data['county'])
        self.assertEqual(data['community'], self.station_data['community'])
        self.assertEqual(data['city'], self.station_data['city'])
        self.assertEqual(data['district'], self.station_data['district'])
        self.assertEqual(data['last_metering'], self.station_data['last_metering'])

    def test_station_create(self):
        self.assertEqual(Station.objects.count(), 0)
        api_response = self.create_station()
        self.assertEqual(api_response.status_code, HTTP_201_CREATED)
        self.assertEqual(Station.objects.count(), 1)

        created_station = Station.objects.get()
        created_station_data = StationSerializer(created_station).data
        self.assertStationDataEqual(created_station_data)
        self.assertEqual(created_station.owner, self.user)

    def test_list_view_filter_in_bbox(self):
        StationFactory.create(position=Point([20, 50]))
        StationFactory.create(position=Point([21, 51]))
        StationFactory.create(position=Point([0, 0]))

        api_response = self.client.get(
            self.station_list_url,
            data={
                'in_bbox': '19, 49, 22, 52'
            }
        )
        self.assertEqual(2, len(api_response.data['results']))


class MeteringApiTests(UserAuthBase):
    def setUp(self):
        self.existing_station = StationFactory.create()
        self.metering = MeteringFactory.build(station=self.existing_station)
        self.metering_data = MeteringSerializer(self.metering).data
        self.metering_list_url = reverse('metering-list')
        return super(MeteringApiTests, self).setUp()

    def test_add_metering(self):
        # test cache key removal before add_metering
        self.assertEqual(self.existing_station.last_metering, MeteringSerializer(None).data)
        self.assertEqual(self.existing_station.metering_set.count(), 0)

        metering_data = self.metering_data.copy()
        metering_data['token'] = self.existing_station.token
        api_response = self.client.post(self.metering_list_url, metering_data)

        self.assertEqual(api_response.status_code, HTTP_201_CREATED)
        self.assertEqual(self.existing_station.metering_set.count(), 1)

        # test cache key removal after add_metering
        self.assertEqual(
            self.existing_station.last_metering,
            MeteringSerializer(self.existing_station.metering_set.first()).data
        )

    def test_add_metering_no_token(self):
        api_response = self.client.post(self.metering_list_url, {})
        self.assertEqual(api_response.status_code, HTTP_403_FORBIDDEN)

    def test_add_metering_wrong_token(self):
        api_response = self.client.post(self.metering_list_url, {'token': 'xyz'})
        self.assertEqual(api_response.status_code, HTTP_403_FORBIDDEN)

    def test_add_metering_wrong_data(self):
        api_response = self.client.post(self.metering_list_url, {'token': self.existing_station.token})
        self.assertEqual(api_response.status_code, HTTP_400_BAD_REQUEST)
