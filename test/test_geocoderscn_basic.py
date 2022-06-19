import pytest

from geocoderscn import GeocoderSCN


def test_attributes():
    my_geocoderSCN = GeocoderSCN('Plaza de las Tendillas 1 Córdoba')
    assert my_geocoderSCN.search_text != ''
    assert my_geocoderSCN.endpoint is None
    assert my_geocoderSCN.feature_count == 0
    assert my_geocoderSCN.api_data is None
    assert my_geocoderSCN.status == 0
    assert my_geocoderSCN.error is False
    assert my_geocoderSCN.messages is None


