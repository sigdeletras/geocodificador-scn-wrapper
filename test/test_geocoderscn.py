import pytest

from geocoderscn import GeocoderSCN

API_bad = 'https://testting/v1/search?text='


@pytest.fixture
def my_GeocoderSCN():
    my_geocoderSCN = GeocoderSCN('Acera Fuente de los Picadores 2 Córdoba')
    return my_geocoderSCN


@pytest.fixture
def my_GeocoderSCN_search(my_GeocoderSCN):
    my_GeocoderSCN.search()
    return my_GeocoderSCN


@pytest.fixture
def my_GeocoderSCN_search_wrong_url(my_GeocoderSCN):
    my_GeocoderSCN.search(API_bad)
    return my_GeocoderSCN


@pytest.fixture
def my_GeocoderSCN_reverse():
    my_geocoderSCN_reverse = GeocoderSCN('40.416645598,-3.70381211')
    my_geocoderSCN_reverse.reverse()
    return my_geocoderSCN_reverse


@pytest.fixture
def my_GeocoderSCN_reverse_bad_list():
    my_geocoderSCN_reverse = GeocoderSCN('40.4166455983.70381211')
    my_geocoderSCN_reverse.reverse()
    return my_geocoderSCN_reverse


def test_class(my_GeocoderSCN):
    assert type(my_GeocoderSCN).__name__ == 'GeocoderSCN'


def test_attributes(my_GeocoderSCN):
    assert my_GeocoderSCN.search_text != ''
    assert my_GeocoderSCN.endpoint is None
    assert my_GeocoderSCN.feature_count == 0
    assert my_GeocoderSCN.api_data is None
    assert my_GeocoderSCN.status == 0
    assert my_GeocoderSCN.error is False
    assert my_GeocoderSCN.messages is None


def test_search(my_GeocoderSCN_search):
    assert my_GeocoderSCN_search.search_text != ''
    assert my_GeocoderSCN_search.endpoint != ''
    assert my_GeocoderSCN_search.api_data is not None
    assert my_GeocoderSCN_search.feature_count > 0
    assert my_GeocoderSCN_search.status == 200
    assert my_GeocoderSCN_search.error is False
    assert my_GeocoderSCN_search.messages == "it's all OK!"


def test_search_wrong_url(my_GeocoderSCN_search_wrong_url):
    assert my_GeocoderSCN_search_wrong_url.error is True


def test_reverse(my_GeocoderSCN_reverse):
    coor = my_GeocoderSCN_reverse.search_text.strip().split(',')
    assert type(coor) is list
    assert len(coor) == 2
    assert my_GeocoderSCN_reverse.endpoint != ''
    assert my_GeocoderSCN_reverse.api_data is not None
    assert my_GeocoderSCN_reverse.feature_count > 0
    assert my_GeocoderSCN_reverse.status == 200
    assert my_GeocoderSCN_reverse.error is False
    assert my_GeocoderSCN_reverse.messages == "it's all OK!"


def test_reverse(my_GeocoderSCN_reverse_bad_list):
    assert my_GeocoderSCN_reverse_bad_list.error is True


def test_get_list(my_GeocoderSCN_search, my_GeocoderSCN_reverse):
    search_list = my_GeocoderSCN_search.get_list()
    assert type(search_list) is list
    assert len(search_list) == my_GeocoderSCN_search.feature_count

def test_get_list_reverse(my_GeocoderSCN_reverse):
    search_list_reverse = my_GeocoderSCN_reverse.get_list()
    assert type(search_list_reverse) is list
    assert len(search_list_reverse) == my_GeocoderSCN_reverse.feature_count
